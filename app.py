import streamlit as st
from chainstream.utils.vectorstore import VectorStore
from chainstream.models.translation import detect_language, translate, load_t5
from chainstream.chains.rag import answer
from chainstream.utils.documents import (
    from_url,
    from_pdf_url,
    from_pdf,
    from_txt,
    from_md,
)
from chainstream.utils.web import related_links, is_pdf_link
from chainstream.utils import configuration
import os
import streamlit as st
from dotenv import load_dotenv


def init_env():
    load_dotenv()
    args = {} if "args" not in st.session_state else st.session_state["args"]
    with st.form(key="env"):
        OPENAI_API_KEY = st.text_input(
            label="OPENAI_API_KEY",
            value=(
                args["OPENAI_API_KEY"]
                if "OPENAI_API_KEY" in args
                else os.environ.get("OPENAI_API_KEY", "")
            ),
        )
        ANTHROPIC_API_KEY = st.text_input(
            label="ANTHROPIC_API_KEY",
            value=(
                args["ANTHROPIC_API_KEY"]
                if "ANTHROPIC_API_KEY" in args
                else os.environ.get("ANTHROPIC_API_KEY", "")
            ),
        )
        COHERE_API_KEY = st.text_input(
            label="COHERE_API_KEY",
            value=(
                args["COHERE_API_KEY"]
                if "COHERE_API_KEY" in args
                else os.environ.get("COHERE_API_KEY", "")
            ),
        )
        FIREWORKS_API_KEY = st.text_input(
            label="FIREWORKS_API_KEY",
            value=(
                args["FIREWORKS_API_KEY"]
                if "FIREWORKS_API_KEY" in args
                else os.environ.get("FIREWORKS_API_KEY", "")
            ),
        )
        MISTRAL_API_KEY = st.text_input(
            label="MISTRAL_API_KEY",
            value=(
                args["MISTRAL_API_KEY"]
                if "MISTRAL_API_KEY" in args
                else os.environ.get("MISTRAL_API_KEY", "")
            ),
        )
        GOOGLE_CSE_ID = st.text_input(
            label="GOOGLE_CSE_ID",
            value=(
                args["GOOGLE_CSE_ID"]
                if "GOOGLE_CSE_ID" in args
                else os.environ.get("GOOGLE_CSE_ID", "")
            ),
        )
        GOOGLE_API_KEY = st.text_input(
            label="GOOGLE_API_KEY",
            value=(
                args["GOOGLE_API_KEY"]
                if "GOOGLE_API_KEY" in args
                else os.environ.get("GOOGLE_API_KEY", "")
            ),
        )
        BING_SUBSCRIPTION_KEY = st.text_input(
            label="BING_SUBSCRIPTION_KEY",
            value=(
                args["BING_SUBSCRIPTION_KEY"]
                if "BING_SUBSCRIPTION_KEY" in args
                else os.environ.get("BING_SUBSCRIPTION_KEY", "")
            ),
        )
        BING_SEARCH_URL = st.text_input(
            label="BING_SEARCH_URL",
            value=(
                args["BING_SEARCH_URL"]
                if "BING_SEARCH_URL" in args
                else os.environ.get("BING_SEARCH_URL", "")
            ),
        )
        TAVILY_API_KEY = st.text_input(
            label="TAVILY_API_KEY",
            value=(
                args["TAVILY_API_KEY"]
                if "TAVILY_API_KEY" in args
                else os.environ.get("TAVILY_API_KEY", "")
            ),
        )
        submitted = st.form_submit_button(label="Confirm")
        if submitted:
            if len(OPENAI_API_KEY) > 0:
                args["OPENAI_API_KEY"] = OPENAI_API_KEY
            elif "OPENAI_API_KEY" in args:
                del args["OPENAI_API_KEY"]
            if len(ANTHROPIC_API_KEY) > 0:
                args["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
            elif "ANTHROPIC_API_KEY" in args:
                del args["ANTHROPIC_API_KEY"]
            if len(COHERE_API_KEY) > 0:
                args["COHERE_API_KEY"] = COHERE_API_KEY
            elif "COHERE_API_KEY" in args:
                del args["COHERE_API_KEY"]
            if len(FIREWORKS_API_KEY) > 0:
                args["FIREWORKS_API_KEY"] = FIREWORKS_API_KEY
            elif "FIREWORKS_API_KEY" in args:
                del args["FIREWORKS_API_KEY"]
            if len(MISTRAL_API_KEY) > 0:
                args["MISTRAL_API_KEY"] = MISTRAL_API_KEY
            elif "MISTRAL_API_KEY" in args:
                del args["MISTRAL_API_KEY"]
            if len(GOOGLE_CSE_ID) > 0:
                args["GOOGLE_CSE_ID"] = GOOGLE_CSE_ID
            elif "GOOGLE_CSE_ID" in args:
                del args["GOOGLE_CSE_ID"]
            if len(GOOGLE_API_KEY) > 0:
                args["GOOGLE_API_KEY"] = GOOGLE_API_KEY
            elif "GOOGLE_API_KEY" in args:
                del args["GOOGLE_API_KEY"]
            if len(BING_SUBSCRIPTION_KEY) > 0:
                args["BING_SUBSCRIPTION_KEY"] = BING_SUBSCRIPTION_KEY
            elif "BING_SUBSCRIPTION_KEY" in args:
                del args["BING_SUBSCRIPTION_KEY"]
            if len(BING_SEARCH_URL) > 0:
                args["BING_SEARCH_URL"] = BING_SEARCH_URL
            elif "BING_SEARCH_URL" in args:
                del args["BING_SEARCH_URL"]
            if len(TAVILY_API_KEY) > 0:
                args["TAVILY_API_KEY"] = TAVILY_API_KEY
            elif "TAVILY_API_KEY" in args:
                del args["TAVILY_API_KEY"]
            st.json(args)
            st.session_state["args"] = args


def import_docs():
    import tempfile
    import logging
    import os

    logging.basicConfig(
        level=logging.DEBUG,
        filename=os.environ.get(
            "PROJECT_DATA_DIR", os.path.expanduser("~/Downloads/3S-SE-AI/")
        )
        + "app.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    if "vectorstore" not in st.session_state:
        st.session_state["vectorstore"] = VectorStore()
    vectorstore = st.session_state["vectorstore"]
    with st.form(key="importdocs"):
        input_urls = st.text_area(
            "Input urls separated by newline",
        )
        uploaded_files = st.file_uploader(
            "Choose one or multiple files",
            accept_multiple_files=True,
            type=["pdf", "txt", "md"],
        )
        submitted = st.form_submit_button(label="Load into DB")
        if submitted:
            docs = []
            if input_urls is not None and len(input_urls) > 0:
                for url in set(input_urls.splitlines()):
                    try:
                        if is_pdf_link(url):
                            docs.extend(from_pdf_url(url))
                        else:
                            docs.extend(from_url(url))
                    except BaseException as e:
                        print(e)
            if uploaded_files is not None:
                for uploaded_file in uploaded_files:
                    try:
                        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                            temp_file.write(uploaded_file.getbuffer())
                            file_extension = os.path.splitext(uploaded_file.name)[1]
                            if file_extension == ".pdf":
                                docs.extend(from_pdf(temp_file.name))
                            elif file_extension == ".txt":
                                docs.extend(from_txt(temp_file.name))
                            elif file_extension == ".md":
                                docs.extend(from_md(temp_file.name))
                    except BaseException as e:
                        logging.error(f"Error processing file: {e}")
            if len(docs) > 0:
                vectorstore.index.add_documents(docs)
    with st.sidebar:
        if st.button("Save VectorDB state"):
            vectorstore.save_state()
        if st.button("Reload VectorDB from local disk"):
            vectorstore = VectorStore()


def chatbot_demo():
    args = {} if "args" not in st.session_state else st.session_state["args"]
    config = configuration.load(args)
    if "vectorstore" not in st.session_state:
        st.session_state["vectorstore"] = VectorStore()
    vectorstore = st.session_state["vectorstore"]
    translator = load_t5()

    with st.sidebar:
        llms = st.multiselect(
            "Select LLMs", [model_key for model_key in config["llms"].keys()], []
        )
        web_tools = st.multiselect(
            "Include web results from",
            [web_tool_key for web_tool_key in config["web_tools"].keys()],
            [],
        )

    st.title("💬 3S Chatbot")

    # st.caption("🚀 3S chatbot")
    def generate_response(input_text):
        lang = detect_language(input_text)
        if lang != "English":
            input_text = translate(text=input_text, translator=translator)
        responses = []
        links = set()
        for web_tool in web_tools:
            for link in related_links(
                input_text, config["web_tools"][web_tool]["tool"]
            ):
                links.add(link)
        links.discard("NA")
        for url in links:
            vectorstore.index.add_documents(from_url(url))
        for llm_key in llms:
            try:
                answr = answer(
                    input_text, config["llms"][llm_key]["model"], vectorstore.index
                )
                if lang != "English":
                    answr = translate(
                        text=answr, target_language=lang, translator=translator
                    )
                responses.append(llm_key + ":" + answr + "\n")
            except BaseException as e:
                print(e)
        st.info("\n".join(responses))

    with st.form("my_form"):
        text = st.text_area("Enter text:", "")
        submitted = st.form_submit_button("Submit")
        generate_response(text)


st.set_page_config(page_title="Chatbot", page_icon="💬")
page_names_to_funcs = {
    "Environment Setup": init_env,
    "Import documents": import_docs,
    "Chatbot": chatbot_demo,
}
demo_name = st.sidebar.selectbox("Naviagate Pages", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
