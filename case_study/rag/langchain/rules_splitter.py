from langchain.text_splitter import RecursiveCharacterTextSplitter


class RulesTextSplitter:
    def __init__(self, chunk_size, chunk_overlap=50):
        pattern = r"([0-9]+)\. "
        self.text_splitter = RecursiveCharacterTextSplitter(
            is_separator_regex=True,
            separators=[pattern],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            keep_separator=False,
        )

    def split(self, text):
        doc_splits = self.text_splitter.create_documents([text])
        return doc_splits
