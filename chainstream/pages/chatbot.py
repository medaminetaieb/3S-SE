def demo():
    import streamlit as st
    from chainstream.models.translation import detect_language, translate, load_t5
    from chainstream.utils import configuration
    from chainstream.chains.rag import answer
    from chainstream.utils.documents import from_url, from_research
    from chainstream.utils.web import related_links
    from chainstream.utils.vectorstore import VectorStore
    from copy import deepcopy
    import os

    # If vectorstores are not initialized, redirect to loading documents page
    if "vectorstores" not in st.session_state:
        st.session_state["vectorstores"] = [VectorStore(vs_name="_")]
    args = {} if "args" not in st.session_state else st.session_state["args"]
    for key, value in args.items():
        os.environ[key] = value
    config = configuration.load(args)
    model_options = [
        model_config["name"] for model_name, model_config in config["llms"].items()
    ]
    model_keys = list(config["llms"].keys())
    web_tool_options = [
        web_tool_config["name"]
        for web_tool_name, web_tool_config in config["web_tools"].items()
    ]
    web_tool_keys = list(config["web_tools"].keys())
    index = deepcopy(st.session_state["vectorstores"][0].index)
    if len(st.session_state["vectorstores"]) > 1:
        for tmp_index in st.session_state["vectorstores"][1:]:
            index.merge_from(tmp_index)
    translator = load_t5()

    with st.sidebar:
        llms = st.multiselect(
            "Select LLMs",
            model_options,
            default=None,
        )
        web_tools = st.multiselect(
            "Include web results from",
            web_tool_options,
            default=None,
        )

    st.title("💬 3S Chatbot")

    # st.caption("🚀 3S chatbot")
    def generate_response(input_text):
        if use_translator:
            lang = detect_language(input_text)
            if lang != "English":
                input_text = translate(text=input_text, translator=translator)
        responses = []
        links = set()
        for web_tool in [
            web_tool_keys[web_tool_options.index(web_tool_name)]
            for web_tool_name in web_tools
        ]:
            try:
                for link in related_links(
                    input_text, config["web_tools"][web_tool]["tool"]
                ):
                    links.add(link)
            except BaseException as e:
                print(e)
        links.discard("NA")
        for url in links:
            index.add_documents(from_url(url))
        if gptresearcher:
            docs = from_research(input_text)
            if docs is not None and len(docs) > 0:
                index.add_documents(docs)
        for llm_key in [
            model_keys[model_options.index(model_name)] for model_name in llms
        ]:
            try:
                answr = answer(input_text, config["llms"][llm_key]["model"], index)
                if use_translator and lang != "English":
                    answr = translate(
                        text=answr, target_language=lang, translator=translator
                    )
                responses.append(llm_key + ":" + answr + "\n")
            except BaseException as e:
                print(e)
        st.info("\n".join(responses))

    with st.form("my_form"):
        use_translator = st.checkbox("Translate across languages")
        text = st.text_area("Enter text:", "")
        if "OPENAI_API_KEY" in args and "TAVILY_API_KEY" in args:
            gptresearcher = st.checkbox("Enable GPTResearcher")
        if st.form_submit_button("Submit"):
            generate_response(text)
