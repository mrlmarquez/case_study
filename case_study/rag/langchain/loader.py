import os
from tqdm import tqdm

from case_study.rag.langchain.rules_splitter import RulesTextSplitter
from case_study.rag.langchain.vector_store import VectorStore
from case_study.utils.files import load_text
from langchain_core.documents import Document


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
