def demo():
    import tempfile
    import logging
    import os
    import streamlit as st
    from chainstream.utils.vectorstore import VectorStore, ls
    from chainstream.utils.documents import (
        from_url,
        from_recursive_url,
        from_youtube_url,
        from_arxiv_url,
        from_pdf_url,
        from_pdf,
        from_docx,
        from_pptx,
        from_txt,
        from_md,
        from_xml,
        from_epub,
    )
    from chainstream.utils.web import (
        is_pdf_link,
        is_youtube_link,
        is_arxiv_link,
    )

    logging.basicConfig(
        level=logging.DEBUG,
        filename=os.environ.get(
            "PROJECT_DATA_DIR", os.path.expanduser("~/Downloads/3S-SE-AI/")
        )
        + "app.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    if "vectorstores" not in st.session_state:
        st.session_state["vectorstores"] = [VectorStore(vs_name="_")]
    vectorstores = st.session_state["vectorstores"]
    with st.form("auth"):
        vs_name = st.text_input("VectoStore Name", "")
        vs_passphrase = st.text_input("VectorStore Passphrase", "", type="password")
        submitted = st.form_submit_button("Authenticate and Load")
        if submitted:
            if len(vs_name) > 0 and len(vs_passphrase) > 0:
                try:
                    tmp = VectorStore(vs_name=vs_name, vs_passphrase=vs_passphrase)
                    if tmp is not None:
                        vectorstores[0] = tmp
                        st.session_state["vectorstores"] = vectorstores
                except BaseException as e:
                    print(e)
                    st.error("Failed to authenticate", icon="🚨")
            else:
                st.error("Please enter credentials", icon="🚨")
    with st.form(key="importdocs"):
        input_urls = st.text_area(
            "Input urls separated by newline",
        )
        uploaded_files = st.file_uploader(
            "Choose one or multiple files",
            accept_multiple_files=True,
            type=["pdf", "docx", "pptx", "txt", "md", "xml", "epub"],
        )
        submitted = st.form_submit_button(label="Load and Save into DB")
        if submitted:
            docs = []
            if input_urls is not None and len(input_urls) > 0:
                for url in set(input_urls.splitlines()):
                    try:
                        if is_pdf_link(url):
                            docs.extend(from_pdf_url(url))
                        elif is_youtube_link(url):
                            docs.extend(from_youtube_url(url))
                        elif is_arxiv_link(url):
                            docs.extend(from_arxiv_url(url))
                        elif " " in url:
                            url_parts = url.split()
                            if len(url_parts) > 0:
                                if len(url_parts) == 1:
                                    docs.extend(from_url(url_parts[0], enable_js=True))
                                else:
                                    docs.extend(from_recursive_url(url_parts))
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
                            elif file_extension == ".xml":
                                docs.extend(from_xml(temp_file.name))
                            elif file_extension == ".epub":
                                docs.extend(from_epub(temp_file.name))
                            elif file_extension == ".docx":
                                docs.extend(from_docx(temp_file.name))
                            elif file_extension == ".pptx":
                                docs.extend(from_pptx(temp_file.name))
                    except BaseException as e:
                        logging.error(f"Error processing file: {e}")
            if len(docs) > 0:
                vectorstores[0].index.add_documents(docs)
            if vectorstores[0].save_state():
                st.success("Vectorstore state saved", icon="✅")
            else:
                st.error("Please authenticate your vectorstore first", icon="🚨")
    with st.sidebar:
        vss = st.multiselect(
            "Available Vector Stores",
            ls(),
            default=(
                []
                if len(vectorstores) <= 1
                else [vs.index_path.split("/")[-1] for vs in vectorstores[1:]]
            ),
        )
        if st.button("Load Vector Stores"):
            vectorstores[:] = vectorstores[:1]
            for name in vss:
                vectorstores.append(VectorStore(name))
            st.success("Vector Stores loaded", icon="✅")
