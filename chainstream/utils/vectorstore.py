import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
from langchain_community.vectorstores import FAISS
from chainstream.models import embeddings


class VectorStore:
    def __init__(self, vs_name: str = "primaryindex", vs_passphrase=None) -> None:
        load_dotenv()
        if vs_passphrase is not None:
            vscreds = VSCredentials()
            access = vscreds.request_access(vs_name, vs_passphrase)
            if access == False:
                raise ValueError("No access Granted")
            elif access is None:
                creds = vscreds.load()
                creds.append({
                    "vs_name": vs_name,
                    "vs_passphrase": vs_passphrase
                })
                vscreds.save(creds=creds)

        self.index_path = (
            os.environ.get(
                "PROJECT_DATA_DIR", os.path.expanduser("~/Downloads/3S-SE-AI/")
            )
            + "vectorstore/"
            + vs_name
        )
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

    def save_state(self) -> bool:
        if self.index_path.split("/")[-1] == "_":
            return False
        try:
            self.index.save_local(self.index_path)
            return True
        except BaseException as e:
            print(e)
            return False


class VSCredentials:
    def __init__(self) -> None:
        load_dotenv()
        self.file_path = (
            os.environ.get(
                "PROJECT_DATA_DIR", os.path.expanduser("~/Downloads/3S-SE-AI/")
            )
            + "vectorstore/"
            + "creds.json"
        )

    def load(self) -> List[Dict[str, str]]:
        import json

        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except BaseException as e:
            return [{"vs_name": "primaryindex", "vs_passphrase": "admin"}]

    def save(self, creds: List[Dict[str, str]]) -> bool:
        import json

        try:
            with open(self.file_path, "w") as f:
                json.dump(creds, f)
                return True
        except BaseException as e:
            print(e)
            return False
        
    def request_access(self, vs_name: str, vs_passphrase: str) -> Optional[bool]:
        """Return None if vs_name not found otherwise boolean confirming or denying access
        """
        creds = self.load()
        for cred in creds:
            if cred["vs_name"] == vs_name:
                return cred["vs_passphrase"] == vs_passphrase
        return None
    
def ls():
    load_dotenv()
    path = os.environ.get(
            "PROJECT_DATA_DIR", os.path.expanduser("~/Downloads/3S-SE-AI/")
    ) + "vectorstore/"
    names = []
    try:
        for entry in os.listdir(path):
            if os.path.isdir(os.path.join(path, entry)):
                names.append(entry)
    except BaseException as e:
        print(e)
    return names