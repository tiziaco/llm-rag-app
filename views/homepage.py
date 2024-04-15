import streamlit as st

from .components.sidebar import render_sidebar
from .components.chat import render_chat


def render_homepage():
	st.title("🤖 Chat Bot")

	## Sidebar
	render_sidebar()
	## Chat
	render_chat()

	# st.experimental_set_query_params()  # Ensures that the app stops when the user closes the browser tab

	# # Register a callback to return the connection when the app stops
	# st.experimental_add_app_handler("on_stop", rag.db.return_connection, rag.conn)