import subprocess
import os
import nltk

subprocess.run(
    [
        "pip",
        "install",
        "-r",
        os.path.dirname(os.path.abspath(__file__)) + "/requirements.txt",
        "--upgrade",
    ]
)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
subprocess.run(["playwright", "install-deps"])
subprocess.run(["playwright", "install"])
