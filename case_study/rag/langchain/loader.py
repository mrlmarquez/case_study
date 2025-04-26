import json
import os
from tqdm import tqdm

from case_study.rag.langchain.rules_splitter import RulesTextSplitter
from case_study.rag.langchain.splitter import TextSplitter
from case_study.rag.langchain.vector_store import GCPChroma, VectorStore
from case_study.utils.files import load_text


DOCS_DIR = "data/rules"


def load_rules():
    vector_store = VectorStore(doc_type="rules")
    docs = []
    for filename in tqdm(os.listdir(DOCS_DIR)):
        if filename.endswith(".txt"):
            file_path = os.path.join(DOCS_DIR, filename)
            text = load_text(file_path)
            docs.append(text)
    print(f"Loaded {len(docs)} txt documents")

    text_splitter = RulesTextSplitter(chunk_size=512)
    print("\nSplitting documents into chunks")
    for i, doc in enumerate(docs):
        doc_chunks = text_splitter.split(doc)
        print(f"Doc {i + 1}: {len(doc_chunks)} chunks")
        vector_store.add(doc_chunks)


def load_contracts():
    vector_store = VectorStore(doc_type="contracts")  # GCPChroma(doc_type="contracts")
    text_splitter = TextSplitter(chunk_size=512, chunk_overlap=50)

    for filename in tqdm(os.listdir("data/contracts")):
        if filename.endswith(".txt"):
            file_path = os.path.join("data/contracts", filename)
            text = load_text(file_path)

            contracts_metadata = _read_contracts_metadata(contract_filename=filename)
            splitted_text = text_splitter.split([text])

            for chunk in splitted_text:
                chunk.metadata = contracts_metadata

            vector_store.add(splitted_text)


def _read_contracts_metadata(contract_filename, file="data/contracts_metadata.json"):
    with open(file) as f:
        d = json.load(f)
        for item in d:
            if item.get("contract_file") == contract_filename:
                return item

        return None
