import subprocess
import os

subprocess.run(
    [
        "pip",
        "install",
        "-r",
        os.path.dirname(os.path.abspath(__file__)) + "/requirements.txt",
        "--upgrade",
    ]
)

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
subprocess.run(["playwright", "install-deps"])
subprocess.run(["playwright", "install"])
