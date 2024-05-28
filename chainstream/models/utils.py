import os
from huggingface_hub import snapshot_download
from dotenv import load_dotenv


load_dotenv()

def localize(model_name):
    try:
        model_path = os.environ.get(
            "PROJECT_DATA_DIR",
            os.path.expanduser("~/Downloads/3S-SE-AI/")
        ) + model_name
        snapshot_download(
            repo_id=model_name,
            local_dir=model_path
        )
        return model_path
    except BaseException as e:
        print(e)
