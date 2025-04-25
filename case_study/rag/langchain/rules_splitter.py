from langchain.text_splitter import NLTKTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RulesTextSplitter:
    def __init__(self, chunk_size, chunk_overlap=50):
        separators = ["\n\n", "\n"]
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=separators, chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def split(self, text):
        doc_splits = self.text_splitter.create_documents([text])
        return doc_splits
