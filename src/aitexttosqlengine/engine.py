from __future__ import annotations

import re
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.tools import tool

from aitexttosqlengine.documents import DOCUMENTS

load_dotenv()


class TextToSQLEngine:
    def __init__(self, embedding_model: str = "text-embedding-3-small", llm_model: str = "gpt-5.4-mini", temperature: float = 0.0):
        self.vectorstore = Chroma.from_texts(
            texts=DOCUMENTS,
            embedding=OpenAIEmbeddings(model=embedding_model),
        )
        self.llm = ChatOpenAI(model_name=llm_model, temperature=temperature)
        self.search_tool = self._build_search_tool()
        self.agent = create_agent(self.llm, tools=[self.search_tool])
        self.instructions = self._default_instructions()

    def _build_search_tool(self):
        @tool
        def search(query: str) -> list[Any]:
            """Search the schema documents and return the top matching table descriptions."""
            return self.vectorstore.similarity_search(query, k=2)

        return search

    def _default_instructions(self) -> str:
        return """
You're a text to sql generator.
You're given a question from a user and your task is to answer it.

If you want to look up information, use the search function.
Use as many keywords from the user question as possible when making first requests.

Make multiple searches. First perform search, analyze the results
and then perform more searches.

At the end, ask if there are other areas that the user wants to explore.
"""

    def generate_sql(self, query: str) -> str | None:
        messages = [
            HumanMessage(content=self.instructions),
            HumanMessage(content=query),
        ]

        response = self.agent.invoke({"messages": messages})
        answer = self._extract_last_ai_message(response)
        return self._extract_sql(answer)

    def _extract_last_ai_message(self, response: dict[str, Any]) -> str:
        answer = ""
        for msg in reversed(response.get("messages", [])):
            if isinstance(msg, AIMessage) and msg.content:
                answer = msg.content
                break
        return answer

    def _extract_sql(self, text: str) -> str | None:
        match = re.search(r"```sql\s*(.*?)\s*```", text, re.DOTALL)
        return match.group(1).strip() if match else None
