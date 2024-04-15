import os
import streamlit as st

from .callbacks import stream_data
from llm_rag import rag

def render_chat():

	# Display chat messages from history on app rerun
	for message in rag.chat_history[1:]:
		with st.chat_message(message["role"]):
			st.markdown(message["content"])

	# Accept user input
	if prompt := st.chat_input("What's up?"):
		# Add user message to chat history
		rag.chat_history.append({"role": "user", "content": prompt})
		# Display user message in chat message container
		with st.chat_message("user"):
			st.markdown(prompt)

		# Display assistant response in chat message container
		with st.chat_message("assistant"):
			response = st.write_stream(stream_data)
		if isinstance(response, str):
			rag.chat_history.append({"role": "assistant", "content": response})