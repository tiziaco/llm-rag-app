from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core import get_response_synthesizer
from llama_index.core import PromptTemplate

from .. import logger


qa_prompt = PromptTemplate(
	"Context information is below.\n"
	"---------------------\n"
	"{context_str}\n"
	"---------------------\n"
	"Given the context information and not prior knowledge, "
	"answer the query.\n"
	"Query: {query_str}\n"
	"Answer: "
)

class RAGQueryEngine():
	"""
	A class to handle retrieving relevant text chunks, 
	crafting prompts, and making LLM requests.
	"""

	def __init__(self, retriever: BaseRetriever, llm_model):
		"""
		Initialize the QueryEngine with a retriever object and an LLM model.

		Args:
			retriever (object): 
				An object that can retrieve relevant text chunks based on a query.
			llm_model (object): 
				An object representing the LLM model you'll use for generation.
		"""
		
		self.retriever = retriever
		self.llm_model = llm_model
		self.qa_prompt = qa_prompt
		self.response_synthesizer = get_response_synthesizer(response_mode="compact", streaming=True, llm=self.llm_model)
		self.memory_buffer = ChatMemoryBuffer.from_defaults(token_limit=2000)

	def custom_query(self, query_str: str):
		# Retrieve relevant text chunks
		nodes = self.retriever.retrieve(query_str)
		# Prepare context string
		context_str = "\n\n".join([n.node.get_content() for n in nodes])
		# Update memory buffer (optional, depending on your use case)
		self.update_memory_buffer(query_str, context_str)
		# Craft the final prompt
		query = qa_prompt.format(context_str=context_str, query_str=query_str)
		# Make the request to the LLM model
		response_obj = self.response_synthesizer.synthesize(query, nodes)
		return response_obj

	def query(self, user_query, max_context_length=1024):
		"""
		Processes a user query and generates a response using the LLM model.

		Args:
			user_query (str): The user's query.
			max_context_length (int, optional): The maximum allowed length for the context string.
				Defaults to 1024.

		Returns:
			str: The generated response from the LLM model.
		"""

		# Retrieve relevant text chunks
		retrieved_documents = self.retriever.query(user_query)

		# Prepare context string
		context_string = self.prepare_context(retrieved_documents, max_context_length)

		# Craft the prompt
		prompt = self.create_prompt(context_string)

		# Update memory buffer (optional, depending on your use case)
		self.update_memory_buffer(user_query, context_string)

		# Make the request to the LLM model
		llm_response = self.llm_model.generate(prompt)

		return llm_response

	def prepare_context(self, retrieved_nodes, max_length):
		"""
		Prepares the context string by concatenating retrieved documents with separators.

		Args:
			retrieved_documents (list): A list of retrieved documents (or passages).
			max_length (int): The maximum allowed length for the context string.

		Returns:
			str: The prepared context string.
		"""

		context_string = "\n\n".join([n.node.get_content() for n in retrieved_nodes])

		# Truncate if necessary
		if len(context_string) > max_length:
			context_string = context_string[:max_length] + "..."

		return context_string


	def update_memory_buffer(self, user_query, context_string):
		"""
		Updates the memory buffer with the user query and context string (optional).

		Args:
			user_query (str): The user's query.
			context_string (str): The prepared context string.
		"""

		# Implement your logic here to update the memory buffer based on your requirements.
		# You might want to consider:
		#  - Adding user queries and context strings as separate entries
		#  - Limiting the buffer size and clearing older entries

		self.memory_buffer.put(user_query)
