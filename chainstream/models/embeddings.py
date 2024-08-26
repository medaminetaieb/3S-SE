from multiprocessing import freeze_support
import os
from dotenv import load_dotenv
from torch import cuda
from langchain_huggingface import HuggingFaceEmbeddings
from chainstream.models.utils import localize


def load(model_name="sentence-transformers/all-mpnet-base-v2", prefer_cuda=True):
    load_dotenv()
    # freeze_support()
    model_path = localize(os.environ.get("EMBEDDINGS_MODEL_NAME", model_name))
    try:
        return HuggingFaceEmbeddings(
            model_name=model_path,
            show_progress=True,
            # multi_process=True,
            model_kwargs={
                "device": (
                    f"cuda:{cuda.current_device()}"
                    if prefer_cuda and cuda.is_available()
                    else "cpu"
                )
            },
            encode_kwargs={"normalize_embeddings": True},
        )
    except cuda.OutOfMemoryError as e:
        return HuggingFaceEmbeddings(
            model_name=model_path,
            show_progress=True,
            # multi_process=True,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={"normalize_embeddings": True},
        )
