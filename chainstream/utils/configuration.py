def load(args={}):
    from langchain_openai import ChatOpenAI
    from langchain_anthropic import ChatAnthropic
    from langchain_google_vertexai import ChatVertexAI
    from langchain_fireworks import ChatFireworks
    from langchain_cohere import ChatCohere
    from langchain_mistralai import ChatMistralAI
    from chainstream.models.generation import phi3
    from langchain_core.tools import Tool
    from langchain_google_community import GoogleSearchAPIWrapper
    from langchain_community.utilities import BingSearchAPIWrapper
    from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

    config = {
        "llms": {},
        "web_tools": {},
    }

    if "OPENAI_API_KEY" in args:
        try:
            config["llms"]["gpt"] = {
                "name": "GPT 3.5 Turbo",
                "model": ChatOpenAI(
                    model="gpt-3.5-turbo", openai_api_key=args["OPENAI_API_KEY"]
                ),
            }
        except BaseException as e:
            print(e)
    if "ANTHROPIC_API_KEY" in args:
        try:
            config["llms"]["claude"] = {
                "name": "Claude 3 Sonnet",
                "model": ChatAnthropic(
                    model="claude-3-sonnet-20240229",
                    anthropic_api_key=args["ANTHROPIC_API_KEY"],
                ),
            }
        except BaseException as e:
            print(e)
    if "GOOGLE_API_KEY" in args:
        try:
            config["llms"]["gemini"] = {
                "name": "Gemini Pro",
                "model": ChatVertexAI(
                    model="gemini-pro", google_api_key=args["GOOGLE_API_KEY"]
                ),
            }
        except BaseException as e:
            print(e)
    if "COHERE_API_KEY" in args:
        try:
            config["llms"]["cohere"] = {
                "name": "Cohere Command-r",
                "model": ChatCohere(
                    model="command-r", cohere_api_key=args["COHERE_API_KEY"]
                ),
            }
        except BaseException as e:
            print(e)
    if "FIREWORKS_API_KEY" in args:
        try:
            config["llms"]["firellava"] = {
                "name": "FireLLaVa-13B",
                "model": ChatFireworks(
                    model="accounts/fireworks/models/firellava-13b",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
            }
        except BaseException as e:
            print(e)
        # config["llms"]["mixtral"] = {
        # "name": "Mixtral 8x7B Instruct",
        # "model": ChatFireworks(model="accounts/fireworks/models/mixtral-8x7b-instruct", fireworks_api_key=args["FIREWORKS_API_KEY"]),
        # }
        try:
            config["llms"]["llama"] = {
                "name": "LlaMa 3 70B Instruct",
                "model": ChatFireworks(
                    model="accounts/fireworks/models/llama-v3-70b-instruct",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
            }
        except BaseException as e:
            print(e)
        # config["llms"]["gemma"] = {
        # "name": "Gemma 7B Instruct",
        # "model": ChatFireworks(model="accounts/fireworks/models/gemma-7b-it", fireworks_api_key=args["FIREWORKS_API_KEY"]),
        # }
        try:
            config["llms"]["zephyr"] = {
                "name": "StableLM 2 Zephyr 1.6B",
                "model": ChatFireworks(
                    model="accounts/stability/models/stablelm-2-zephyr-2b",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
            }
        except BaseException as e:
            print(e)
        try:
            config["llms"]["yi"] = {
                "name": "Capybara 34B",
                "model": ChatFireworks(
                    model="accounts/fireworks/models/yi-34b-200k-capybara",
                    fireworks_api_key=args["FIREWORKS_API_KEY"],
                ),
            }
        except BaseException as e:
            print(e)
    if "MISTRAL_API_KEY" in args:
        try:
            config["llms"]["Mistral"] = {
                "name": "Mistral",
                "model": ChatMistralAI(
                    model="mistral-large-latest",
                    mistral_api_key=args["MISTRAL_API_KEY"],
                ),
            }
        except BaseException as e:
            print(e)
    try:
        config["llms"]["phi3"] = {
            "name": "Phi 3",
            "model": phi3(prefer_cuda=False),
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
