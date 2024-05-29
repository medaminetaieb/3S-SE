import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from chainstream.models import embeddings


class VectorStore:
    def __init__(self, index_name: str = "primaryindex") -> None:
        load_dotenv()
        self.index_path = os.environ.get(
            "PROJECT_DATA_DIR",
            os.path.expanduser("~/Downloads/3S-SE-AI/")
        ) + "vectorstore/" + index_name
        self.embeddings = embeddings.load(prefer_cuda=False)

        try:
            self.index = FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        except BaseException as e:
            self.index = FAISS.from_texts(
                ["Standard Sharing Software"],
                self.embeddings,
            )

    def save_state(self):
        try:
            self.index.save_local(self.index_path)
        except BaseException as e:
            print(e)