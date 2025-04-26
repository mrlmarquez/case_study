import os

import sys

os.chdir("/mount/src/case_study/src")
sys.path.append("/mount/src/case_study/src/")

from case_study.rag.langchain.loader import load_contracts, load_rules
from case_study.ui.app import start


if __name__ == "__main__":
    print("loading rules")
    load_rules()
    print("loading contracts")
    load_contracts()
    print("starting app...")
    start()
