from typing import Set
import nest_asyncio

nest_asyncio.apply()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def preprocess(data):
    return data
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = None
    if isinstance(data, str):
        splits = splitter.split_text(data)
    elif isinstance(data, dict):
        if "page_content" in data:
            splits = splitter.split_text(data["page_content"])
        elif "text" in data:
            splits = splitter.split_text(data["text"])
    else:
        splits = splitter.split_documents(data)
    return splits

def from_txt(file):
    from langchain_community.document_loaders import TextLoader
    loader = TextLoader(file, autodetect_encoding=True)
    docs = loader.load_and_split()
    return docs

def from_md(file):
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
    loader = UnstructuredMarkdownLoader(file)
    docs = loader.load_and_split()
    return docs

def from_pdf(file):
    from langchain_community.document_loaders import PyMuPDFLoader
    loader = PyMuPDFLoader(file)
    docs = loader.load_and_split()
    return docs

def from_pdf_url(url):
    import requests
    import tempfile
    response = requests.get(url)
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(response.content)
        docs = from_pdf(temp_file.name)
        return docs

def from_url(url):
    from langchain_community.document_loaders.async_html import AsyncHtmlLoader
    from langchain_community.document_transformers import Html2TextTransformer
    loader = AsyncHtmlLoader(url)
    docs = loader.load_and_split()
    docs_transformed = Html2TextTransformer().transform_documents(docs)
    return docs_transformed


async def research(query):
    from gpt_researcher import GPTResearcher
    researcher = GPTResearcher(query=query, report_type="research_report")
    research_data = await researcher.conduct_research()
    report = await research_data.write_report()
    return preprocess(report)
