import os
from typing import Iterator, Dict

from llama_index.llms.ollama import Ollama
from .base import BaseRag
from .modules.db import Database
from .modules.query import RAGQueryEngine
from llama_index.core.llms import ChatMessage

from . import logger

class Rag(BaseRag):
	def __init__(self):
		# Init parameters
		self.llm_parms = BaseRag.init_llm_parms()
		self.rag_parms = BaseRag.init_rag_parms()
		# Init sub-modules
		self.db = Database()
		self.conn = self.db.get_connection()
		self.vector_store = BaseRag.init_vector_store()
		self.embed_model = BaseRag.init_embeddings()
		self.llm = BaseRag.init_llm()
		self.index = BaseRag.init_index(self.vector_store, self.embed_model)
		# Init modules
		self.ingest = BaseRag.init_ingestor(self.index, self.embed_model)
		self.retriever = BaseRag.init_retriever(self.vector_store, self.embed_model)
		self.query_engine = RAGQueryEngine(self.retriever, self.llm)
		# Init system attributes
		self.chat_history = BaseRag.init_chat()
	
	@property
	def llm_model(self):
		return self.llm_parms.get('model_name', None)
	
	@property
	def context(self):
		return self.llm_parms.get('context', None)
	
	@property
	def temperature(self):
		return float(self.llm_parms.get('temperature', None))
	
	def modify_parms(self, key, value):
		if key in self.llm_parms.keys():
			self.llm_parms[key] = value
	
	def clean_chat_history(self):
		# Clear existing messages
		self.chat_history = []
		# Update context message
		self.chat_history.append({
			"role": "assistant",
			"content": self.context
		})
	
	def apply_model_change(self, model, temp, context):
		reinit_model = False

		if model != self.llm_model:
			self.modify_parms('model', model)
			reinit_model = True
		if temp != self.temperature:
			self.modify_parms('temperature', temp)
			reinit_model = True
		if context != self.context:
			self.modify_parms('context', context)
			reinit_model = True
		if reinit_model:
			self.llm = Ollama(model=self.llm_model, request_timeout=30.0, temperature=self.temperature)
		
		# Clear the chat and set the new context
		self.clean_chat_history()
	
	def get_last_user_message(self):
		"""
		This function retrieves the content of the last element with 
		role 'user' from a list of dictionaries.

		Returns:
			str: The last user message or None if not found.
		"""

		# Iterate in reverse order to find the last element with role 'user'
		for element in reversed(self.chat_history):
			if element.get("role") == "user":
				return element["content"]

		# No element with role 'user' found
		return None
	
	def stream_query_complete(self) -> Iterator[Dict]:
		"""
		Retrive the context from the vectorstore, craft a prompt and
		send it to the LLM for completion.
		"""
		query_str = self.get_last_user_message()
		streaming_response = self.query_engine.custom_query(query_str)
		for text in streaming_response.response_gen:
			yield text
	
	def stream_chat(self) -> Iterator[Dict]:
		""" 
		Iterator that streams the answere from the LLM server.
		"""
		messages = [
			ChatMessage(role=mess["role"], content=mess["content"])
			for mess in self.chat_history
		]
		stream = self.llm.stream_chat(messages)
		for r in stream:
			yield r.delta