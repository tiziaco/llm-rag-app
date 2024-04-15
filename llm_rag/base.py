import os
import psycopg2
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

from llm_rag.modules.ingestion import VectorDBIngest
from llm_rag.modules.retriver import VectorDBRetriever

from . import logger

## Load environment variables
load_dotenv()

class BaseRag:
	@staticmethod
	def init_llm_parms():
		parms = {
			'model_name' : os.environ.get('DEFAULT_MODEL'),
			'temperature': os.environ.get('DEFAULT_TEMPERATURE'),
			'context' : os.environ.get('DEFAULT_CONTEXT')
			}
		return parms

	@staticmethod
	def init_rag_parms():
		parms = {
			'embed_name' : os.environ.get('EMBED_MODEL'),
			'embed_dim' : os.environ.get('EMBED_DIM'),
			'text_splitter': os.environ.get('DEFAULT_SPLITTER')
			}
		return parms
	
	@staticmethod
	def init_chat():
		return [
			{
				"role": "assistant",
				"content": os.environ.get('DEFAULT_CONTEXT'),
			}
		]

	@staticmethod
	def init_database():
		#logger.info("RAG: Initializing database connection...")
		conn = psycopg2.connect(
			dbname="postgres",
			host=os.environ.get('DB_HOST'),
			password=os.environ.get('DB_PASSWORD'),
			port=os.environ.get('DB_PORT'),
			user=os.environ.get('DB_USER'),
		)
		conn.autocommit = True
		logger.info("RAG: Database connection established.")
		return conn

	@staticmethod
	def init_vector_store():
		#logger.info("RAG: Initializing vector store...")
		vector_store = PGVectorStore.from_params(
			database=os.environ.get('DB_NAME'),
			host=os.environ.get('DB_HOST'),
			password=os.environ.get('DB_PASSWORD'),
			port=os.environ.get('DB_PORT'),
			user=os.environ.get('DB_USER'),
			table_name="llama2_hr_rag",
			embed_dim=384,  # openai embedding dimension
		)
		logger.info("RAG: Vector store initialized.")
		return vector_store

	@staticmethod
	def init_embeddings():
		#logger.info("RAG: Initializing embeddings...")
		embed_model = HuggingFaceEmbedding(model_name=os.environ.get('EMBED_MODEL'))
		logger.info("RAG: Embeddings initialized.")
		return embed_model

	@staticmethod
	def init_index(vector_store, embed_model):
		#logger.info("RAG: Initializing index...")
		index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)
		logger.info("RAG: Index initialized.")
		return index

	@staticmethod
	def init_ingestor(index, embed_model):
		#logger.info("RAG: Initializing ingestor...")
		ingest = VectorDBIngest(index=index, embed_model=embed_model)
		logger.info("RAG: Ingestor initialized.")
		return ingest

	@staticmethod
	def init_retriever(vector_store, embed_model):
		#logger.info("RAG: Initializing retriever...")
		retriever = VectorDBRetriever(vector_store=vector_store, embed_model=embed_model,
									  similarity_top_k=os.environ.get('TOP_K'))
		logger.info("RAG: Retriever initialized.")
		return retriever

	@staticmethod
	def init_llm():
		#logger.info("RAG: Initializing LLM model...")
		llm = Ollama(
			model=os.environ.get('DEFAULT_MODEL'), 
			request_timeout=30.0,
			temperature=os.environ.get('DEFAULT_TEMPERATURE'))
		logger.info("RAG: LLM model initialized.")
		return llm
