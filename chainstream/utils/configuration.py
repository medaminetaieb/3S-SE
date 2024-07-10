from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import ChatVertexAI
from langchain_fireworks import ChatFireworks
from langchain_cohere import ChatCohere
from langchain_mistralai import ChatMistralAI
from langchain_together import ChatTogether
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


def load(args={}):
    config = {
        "llms": {},
        "web_tools": {},
    }

    if "OPENAI_API_KEY" in args:
        try:
            config["llms"]["openai-gpt-4o"] = {
                "name": "GPT-4o (OpenAI)",
                "model": ChatOpenAI(model="gpt-4o", api_key=args["OPENAI_API_KEY"]),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["openai-gpt-4-turbo"] = {
                "name": "GPT-4 Turbo (OpenAI)",
                "model": ChatOpenAI(
                    model="gpt-4-turbo", api_key=args["OPENAI_API_KEY"]
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["openai-gpt-3.5-turbo"] = {
                "name": "GPT-3.5 Turbo (OpenAI)",
                "model": ChatOpenAI(
                    model="gpt-3.5-turbo", api_key=args["OPENAI_API_KEY"]
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
    if "ANTHROPIC_API_KEY" in args:
        try:
            config["llms"]["anthropic-claude-3.5-sonnet"] = {
                "name": "Claude 3.5 Sonnet (Anthropic)",
                "model": ChatAnthropic(
                    model="claude-3-5-sonnet-20240620",
                    api_key=args["ANTHROPIC_API_KEY"],
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
    if "COHERE_API_KEY" in args:
        try:
            config["llms"]["cohere-command-r-plus"] = {
                "name": "Command R+ (Cohere)",
                "model": ChatCohere(
                    model="command-r-plus", cohere_api_key=args["COHERE_API_KEY"]
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["cohere-command-r"] = {
                "name": "Command R (Cohere)",
                "model": ChatCohere(
                    model="command-r", cohere_api_key=args["COHERE_API_KEY"]
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["cohere-command"] = {
                "name": "Command (Cohere)",
                "model": ChatCohere(
                    model="command", cohere_api_key=args["COHERE_API_KEY"]
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
    if "FIREWORKS_API_KEY" in args:
        try:
            config["llms"]["fireworks-firellava-13b"] = {
                "name": "FireLLaVa-13B (Fireworks)",
                "model": ChatFireworks(
                    model="accounts/fireworks/models/firellava-13b",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["fireworks-mistral-moe-8x22b-instruct"] = {
                "name": "Mistral MoE 8x22B Instruct (Fireworks)",
                "model": ChatFireworks(
                    model="accounts/fireworks/models/mixtral-8x22b-instruct",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
                "prompt": hub.pull("rlm/rag-prompt-mistral"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["fireworks-yi-large"] = {
                "name": "Yi-Large (Fireworks)",
                "model": ChatFireworks(
                    model="accounts/fireworks/models/yi-large",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["fireworks-llama-3-70b-instruct"] = {
                "name": "Llama 3 70B Instruct (Fireworks)",
                "model": ChatFireworks(
                    model="accounts/fireworks/models/llama-v3-70b-instruct",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
                "prompt": hub.pull("rlm/rag-prompt-llama"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["fireworks-chronos-hermes-13b-v2"] = {
                "name": "Chronos Hermes 13B v2 (Fireworks)",
                "model": ChatFireworks(
                    model="accounts/fireworks/models/chronos-hermes-13b-v2",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["fireworks-zephyr-7b-beta"] = {
                "name": "Zephyr 7B Beta (Fireworks)",
                "model": ChatFireworks(
                    model="accounts/fireworks/models/zephyr-7b-beta",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
                "template": """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. {context} Question: {question} Helpful Answer:""",
            }
        except BaseException as e:
            print(e)
    if "MISTRAL_API_KEY" in args:
        try:
            config["llms"]["mistral-open-mixtral-8x22b"] = {
                "name": "Mixtral 8x22B (Mistral)",
                "model": ChatMistralAI(
                    model="open-mixtral-8x22b",
                    mistral_api_key=args["MISTRAL_API_KEY"],
                ),
                "prompt": hub.pull("rlm/rag-prompt-mistral"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["mistral-large"] = {
                "name": "Mistral Large (Mistral)",
                "model": ChatMistralAI(
                    model="mistral-large-latest",
                    mistral_api_key=args["MISTRAL_API_KEY"],
                ),
                "prompt": hub.pull("rlm/rag-prompt-mistral"),
            }
        except BaseException as e:
            print(e)
    if "TOGETHER_API_KEY" in args:
        try:
            config["llms"]["together-deepseek-67b"] = {
                "name": "DeepSeek 67B (Together)",
                "model": ChatTogether(
                    together_api_key=args["TOGETHER_API_KEY"],
                    model="deepseek-ai/deepseek-llm-67b-chat",
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["together-nous-capybara"] = {
                "name": "Nous Capybara v1.9 (Together)",
                "model": ChatTogether(
                    together_api_key=args["TOGETHER_API_KEY"],
                    model="NousResearch/Nous-Capybara-7B-V1p9",
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["together-qwen-1.5"] = {
                "name": "Qwen 1.5 110B (Together)",
                "model": ChatTogether(
                    together_api_key=args["TOGETHER_API_KEY"],
                    model="Qwen/Qwen1.5-110B-Chat",
                ),
                "prompt": hub.pull("rlm/rag-prompt"),
            }
        except BaseException as e:
            print(e)
    if "GROQ_API_KEY" in args:
        try:
            config["llms"]["groq-gemma2-9b"] = {
                "name": "Gemma 2 9b (Groq)",
                "model": ChatGroq(
                    api_key=args["GROQ_API_KEY"],
                    model="gemma2-9b-it",
                ),
                "template": """You are an expert in answering user questions. You always understand user questions well, and then provide high-quality answers based on the information provided in the context.

                If the provided context does not contain relevant information, just respond "I could not find the answer based on the context you provided."

                User question: {question}

                Context:
                {context}
                """,
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["groq-llama-3-70b"] = {
                "name": "LLaMA3 70b (Groq)",
                "model": ChatGroq(
                    api_key=args["GROQ_API_KEY"],
                    model="llama3-70b-8192",
                ),
                "prompt": hub.pull("rlm/rag-prompt-llama"),
            }
        except BaseException as e:
            print(e)
    if "GOOGLE_CSE_ID" in args and "GOOGLE_API_KEY" in args:
        try:
            config["web_tools"]["google"] = {
                "name": "Google",
                "tool": Tool(
                    name="google_search",
                    description="Search Google for recent results.",
                    func=GoogleSearchAPIWrapper(
                        google_api_key=args["GOOGLE_API_KEY"],
                        google_cse_id=args["GOOGLE_CSE_ID"],
                    ).run,
                ),
            }
        except BaseException as e:
            print(e)
    if "BING_SUBSCRIPTION_KEY" in args and "BING_SEARCH_URL" in args:
        try:
            config["web_tools"]["bing"] = {
                "name": "Bing",
                "tool": Tool(
                    name="bing_search",
                    description="Search Bing for recent results.",
                    func=BingSearchAPIWrapper(
                        bing_search_url=args["BING_SEARCH_URL"],
                        bing_subscription_key=args["BING_SUBSCRIPTION_KEY"],
                    ).results,
                ),
            }
        except BaseException as e:
            print(e)
    try:
        config["web_tools"]["duckduckgo"] = {
            "name": "DuckDuckGo",
            "tool": Tool(
                name="duckduckgo_search",
                description="Search DuckDuckGo for recent results.",
                func=DuckDuckGoSearchAPIWrapper().run,
            ),
        }
    except BaseException as e:
        print(e)

    return config
