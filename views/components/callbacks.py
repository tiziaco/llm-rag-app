import streamlit as st

from typing import Iterator, Dict
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

from llm_rag import rag


def stream_data() -> Iterator[Dict]:
	""" 
	Iterator that streams the answere from the LLM server.
	"""
	messages = [
		ChatMessage(role=mess["role"], content=mess["content"])
		for mess in rag.chat_history
	]
	stream = rag.llm.stream_chat(messages)
	for r in stream:
		yield r.delta