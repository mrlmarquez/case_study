from uuid import uuid4
from langchain_chroma import Chroma
from langchain_nomic import NomicEmbeddings

VECTOR_STORE_FILEPATH = "data/{doc}_chroma_langchain_db"


class VectorStore:
    def __init__(self, doc_type="contracts"):
        self.filepath = VECTOR_STORE_FILEPATH.format(doc=doc_type)
        self.store = Chroma(
            collection_name=doc_type,
            embedding_function=NomicEmbeddings(
                model="nomic-embed-text-v1.5", inference_mode="local"
            ),
            persist_directory=self.filepath,  # Where to save data locally, remove if not necessary
        )
        self.retriever = self.store.as_retriever(
            search_type="mmr", search_kwargs={"k": 1, "fetch_k": 5}
        )

    def add(self, doc_splits):
        # uuids = [str(uuid4()) for _ in range(len(doc_splits))]
        self.store.add_documents(doc_splits)
