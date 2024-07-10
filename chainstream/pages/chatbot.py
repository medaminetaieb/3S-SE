import streamlit as st
from streamlit_feedback import streamlit_feedback as st_feedback
from chainstream.models.translation import detect_language, translate, load_t5
from chainstream.utils import configuration
from chainstream.chains.rag import answer
from chainstream.utils.documents import from_url, from_research
from chainstream.utils.web import related_links
from chainstream.utils.vectorstore import VectorStore
from chainstream.models.ranking import submit_feedback, reranked
from copy import deepcopy
import os
from uuid import uuid4 as uuid


def demo():
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
        for tmp_vs in st.session_state["vectorstores"][1:]:
            try:
                index.merge_from(tmp_vs.index)
            except BaseException as e:
                print(e)
    translator = load_t5()

    with st.sidebar:
        calculate_scores = st.checkbox("Rank Answers")
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
        if "OPENAI_API_KEY" in args and "TAVILY_API_KEY" in args:
            gptresearcher = st.checkbox("Enable GPTResearcher")
        use_translator = st.checkbox("Translate across languages")

    st.title("💬 3S Chatbot")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "id": str(uuid()),
                "role": "assistant",
                "content": "Hi! How can I assist you?",
            }
        ]
    else:
        for message in st.session_state["messages"]:
            st.chat_message(message["role"]).write(message["content"])
            if "feedback" in message:
                st_feedback(
                    key=message["id"],
                    feedback_type="faces",
                    disable_with_score=message["feedback"],
                    on_submit=submit_feedback,
                    kwargs={"llm_key": message["content"].split(":")[0]},
                )

    if prompt := st.chat_input(placeholder="Enter your prompt"):
        q = prompt
        st.chat_message("user").write(q)
        if use_translator:
            lang = detect_language(q)
            if lang != "English":
                q = translate(text=q, translator=translator)
        st.session_state["messages"].append(
            {
                "id": str(uuid()),
                "role": "user",
                "content": q,
            }
        )
        links = set()
        for web_tool in [
            web_tool_keys[web_tool_options.index(web_tool_name)]
            for web_tool_name in web_tools
        ]:
            try:
                for link in related_links(q, config["web_tools"][web_tool]["tool"]):
                    links.add(link)
            except BaseException as e:
                print(e)
        links.discard("NA")
        for url in links:
            index.add_documents(from_url(url))
        if gptresearcher:
            docs = from_research(q)
            if docs is not None and len(docs) > 0:
                index.add_documents(docs)
        answrs = []
        for llm_key in [
            model_keys[model_options.index(model_name)] for model_name in llms
        ]:
            try:
                answr = answer(
                    question=q,
                    llm=config["llms"][llm_key]["model"],
                    vectorstore=index,
                    template=(
                        config["llms"][llm_key]["template"]
                        if "template" in config["llms"][llm_key]
                        else None
                    ),
                    prompt=(
                        config["llms"][llm_key]["prompt"]
                        if "prompt" in config["llms"][llm_key]
                        else None
                    ),
                )
                if use_translator and lang != "English":
                    answr["answer"] = translate(
                        text=answr["answer"],
                        target_language=lang,
                        translator=translator,
                    )
                answrs.append({"llm_key": llm_key, "answer": answr})
            except BaseException as e:
                print(e)
        for answr in reranked(
            answers=answrs,
            embeddings=(
                None
                if not calculate_scores
                else st.session_state["vectorstores"][0].embeddings
            ),
            config=None if not calculate_scores else config,
        ):
            st.chat_message("assistant").write(
                answr["llm_key"] + ":" + answr["answer"]["answer"]
            )
            msgid = str(uuid())
            st.session_state["messages"].append(
                {
                    "id": msgid,
                    "role": "assistant",
                    "content": answr["llm_key"] + ":" + answr["answer"]["answer"],
                    "feedback": st_feedback(
                        key=msgid,
                        feedback_type="faces",
                        on_submit=submit_feedback,
                        kwargs={"llm_key": answr["llm_key"]},
                    ),
                }
            )
