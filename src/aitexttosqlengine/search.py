from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.tools import tool
from typing import Any

from aitexttosqlengine.documents import DOCUMENT_OBJECTS


class SchemaSearcher:
    def __init__(self):
        self.vectorstore = Chroma.from_documents(
           documents=DOCUMENT_OBJECTS,
           embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
            )

    def search(self, query: str, k: int = 2) -> list[Any]:
        """Search the schema documents and return the top matching tables"""
        return self.vectorstore.similarity_search(query, k=k)