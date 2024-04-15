import os
import numpy as np
from pathlib import Path

from llama_index.readers.file import PyMuPDFReader
from llama_index.core import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser.text import SemanticSplitterNodeParser


class VectorDBIngest:
	def __init__(self,
			index,
			embed_model: HuggingFaceEmbedding):
		self.index = index
		self.text_parser = SemanticSplitterNodeParser(embed_model=embed_model)
		self.loader = PyMuPDFReader()

	def import_pdf(self, file_path:str):
		print("Ingestor: Importing document...")
		documents = self.loader.load(file_path=file_path)
		print("Ingestor: Creating nodes...")
		nodes = self.text_parser.get_nodes_from_documents(documents,True)
		self.index.insert_nodes(nodes)