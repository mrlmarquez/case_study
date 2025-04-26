import os
import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

VECTOR_STORE_FILEPATH = "data/{doc}_chroma_langchain_db"


class VectorStore:
    def __init__(self, doc_type="contracts"):
        self.filepath = VECTOR_STORE_FILEPATH.format(doc=doc_type)
        client = chromadb.PersistentClient(path=self.filepath)
        self.collection_name = doc_type

        self.collection = client.get_or_create_collection(doc_type)
        self.store = Chroma(
            collection_name=doc_type,
            embedding_function=OpenAIEmbeddings(),
            client=client,  # Where to save data locally, remove if not necessary
        )

        self.retriever = self.store.as_retriever(
            search_type="mmr", search_kwargs={"k": 1, "fetch_k": 5}
        )
        print(f"{doc_type} collection initialized with size {self.collection.count()}")

    def add(self, doc_splits):
        # uuids = [str(uuid4()) for _ in range(len(doc_splits))]
        print(f"Current collection count: {self.collection.count()}")
        self.store.add_documents(doc_splits)
        print(
            f"{len(doc_splits)} added to {self.collection_name} collection (size:{self.collection.count()})"
        )


class GCPChroma:
    def __init__(self, doc_type="contracts"):
        CHROMA_ENDPOINT = os.getenv("CHROMA_ENDPOINT")
        CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
        client = chromadb.HttpClient(
            host=CHROMA_ENDPOINT,
            port=443,
            ssl=True,
            settings=Settings(
                chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                chroma_client_auth_credentials=CHROMA_API_KEY,
                anonymized_telemetry=False,
            ),
        )

        self.store = Chroma(
            client=client,
            collection_name=doc_type,
            embedding_function=OpenAIEmbeddings(),
        )

        self.retriever = self.store.as_retriever(
            search_type="mmr", search_kwargs={"k": 1, "fetch_k": 5}
        )

    def add(self, doc_splits):
        # uuids = [str(uuid4()) for _ in range(len(doc_splits))]
        self.store.add_documents(doc_splits)
