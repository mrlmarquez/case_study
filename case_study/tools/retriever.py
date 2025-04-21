from smolagents import Tool


class RetrieverTool(Tool):
    name = "retriever"
    description = "Uses semantic search to retrieve the parts of the documentation that could be most relevant to answer your query."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be semantically close to your target documents. Use the affirmative form rather than a question.",
        }
    }
    output_type = "string"

    def __init__(self, vector_db, **kwargs):  # Add vector_db as an argument
        super().__init__(**kwargs)
        self.vector_db = vector_db  # Store the vector database

    def forward(self, query: str) -> str:
        assert isinstance(query, str), "Your search query must be a string"
        docs = self.vector_db.similarity_search(query, k=4)  # Perform search here
        return "\nRetrieved documents:\n" + "".join(
            [
                f"\n\n===== Document {str(i)} =====\n" + doc.page_content
                for i, doc in enumerate(docs)
            ]
        )
