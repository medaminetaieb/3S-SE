def demo():
    import streamlit as st
    import os
    from dotenv import load_dotenv

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
        TOGETHER_API_KEY = st.text_input(
            label="TOGETHER_API_KEY",
            value=(
                args["TOGETHER_API_KEY"]
                if "TOGETHER_API_KEY" in args
                else os.environ.get("TOGETHER_API_KEY", "")
            ),
        )
        GROQ_API_KEY = st.text_input(
            label="GROQ_API_KEY",
            value=(
                args["GROQ_API_KEY"]
                if "GROQ_API_KEY" in args
                else os.environ.get("GROQ_API_KEY", "")
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
        if st.form_submit_button(label="Confirm"):
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
            if len(TOGETHER_API_KEY) > 0:
                args["TOGETHER_API_KEY"] = TOGETHER_API_KEY
            elif "TOGETHER_API_KEY" in args:
                del args["TOGETHER_API_KEY"]
            if len(GROQ_API_KEY) > 0:
                args["GROQ_API_KEY"] = GROQ_API_KEY
            elif "GROQ_API_KEY" in args:
                del args["GROQ_API_KEY"]
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
