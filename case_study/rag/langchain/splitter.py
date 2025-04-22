from langchain.text_splitter import RecursiveCharacterTextSplitter


class TextSplitter:
    def __init__(self, chunk_size, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def split(self, text):
        doc_splits = self.text_splitter.create_documents(text)
        return doc_splits
