import os
import streamlit as st

from llm_rag import rag

def render_sidebar():
	# Model selection box
	model = st.sidebar.selectbox(
		'Select a model',
		('llama2', 'mistral'))
	
	# Context text area
	context = st.sidebar.text_area("Context", rag.context)
	
	# Temperature slider
	temp = st.sidebar.slider("Temperature", 0.0, 1.0, rag.temperature, 0.01)
	
	# File uploader
	uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf"])
	if uploaded_file is not None:
		st.sidebar.write("PDF file uploaded!")
	
	# Apply button with callback
	if st.sidebar.button("Apply", on_click=rag.apply_model_change, args=(model, temp, context)):
		st.sidebar.write("Resetting the model...")