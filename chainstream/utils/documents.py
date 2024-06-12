from typing import Set, List
import nest_asyncio

nest_asyncio.apply()


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def from_xml(file_path: str):
    from langchain_community.document_loaders import UnstructuredXMLLoader

    loader = UnstructuredXMLLoader(file_path)
    docs = loader.load_and_split()
    return docs


def from_epub(file_path: str):
    from langchain_community.document_loaders import UnstructuredEPubLoader

    loader = UnstructuredEPubLoader(file_path, mode="elements")
    docs = loader.load_and_split()
    return docs


def from_txt(file_path: str):
    from langchain_community.document_loaders import TextLoader

    loader = TextLoader(file_path, autodetect_encoding=True)
    docs = loader.load_and_split()
    return docs


def from_md(file_path: str):
    from langchain_community.document_loaders import UnstructuredMarkdownLoader

    loader = UnstructuredMarkdownLoader(file_path)
    docs = loader.load_and_split()
    return docs


def from_pdf(file_path: str):
    from langchain_community.document_loaders import PyMuPDFLoader

    loader = PyMuPDFLoader(file_path)
    docs = loader.load_and_split()
    return docs


def from_docx(file_path: str):
    from langchain_community.document_loaders import Docx2txtLoader

    loader = Docx2txtLoader(file_path)
    docs = loader.load_and_split()
    return docs


def from_pptx(file_path: str):
    from langchain_community.document_loaders import UnstructuredPowerPointLoader

    loader = UnstructuredPowerPointLoader(file_path, mode="elements")
    docs = loader.load_and_split()
    return docs


def from_pdf_url(url: str):
    import requests
    import tempfile

    response = requests.get(url)
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(response.content)
        docs = from_pdf(temp_file.name)
        return docs


def from_url(url: str, enable_js=False):
    if enable_js:
        from langchain_community.document_loaders import PlaywrightURLLoader

        loader = PlaywrightURLLoader(
            urls=[url],
            remove_selectors=["header", "footer"],
            continue_on_failure=True,
            headless=True,
        )
        docs = loader.load_and_split()
        return docs
    from langchain_community.document_loaders.async_html import AsyncHtmlLoader
    from langchain_community.document_transformers import Html2TextTransformer

    loader = AsyncHtmlLoader(url)
    docs = loader.load_and_split()
    docs_transformed = Html2TextTransformer().transform_documents(docs)
    return docs_transformed


def from_recursive_url(url_parts: List[str]):
    from langchain_community.document_loaders.recursive_url_loader import (
        RecursiveUrlLoader,
    )

    loader = RecursiveUrlLoader(
        url=url_parts[0],
        max_depth=None if not url_parts[1].isdigit() else int(url_parts[1]),
        use_async=True,
        check_response_status=True,
        continue_on_failure=True,
        autoset_encoding=True,
    )
    docs = loader.load_and_split()
    return docs


def from_youtube_url(url: str):
    from langchain_community.document_loaders import YoutubeLoader

    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    docs = loader.load_and_split()
    return docs


def from_arxiv_url(url: str):
    from langchain_community.document_loaders import ArxivLoader

    loader = ArxivLoader(query=url.split("/")[-1], load_max_docs=2)
    docs = loader.load_and_split()
    return docs


def from_research(query: str):
    from gpt_researcher import GPTResearcher
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    import asyncio

    loop = asyncio.get_event_loop()
    try:
        researcher = GPTResearcher(query=query, report_type="research_report")
        research_task = loop.run_until_complete(researcher.conduct_research())
        research_data_task = loop.run_until_complete(
            research_task.result().write_report()
        )
        docs = RecursiveCharacterTextSplitter().create_documents(
            texts=[research_data_task.report],  # Access report from research_data_task
            metadatas=[{"source": "GPTResearcher"}],
        )
        return docs
    except BaseException as e:
        print(e)
    finally:
        loop.close()  # Close the event loop after use
