import os

from llama_index.llms.ollama import Ollama
from .base import BaseRag
from .modules.db import Database

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