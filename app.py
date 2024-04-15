from views.homepage import render_homepage
from llm_rag import rag

if __name__ == "__main__":
	render_homepage()
	#rag.db.return_connection(rag.conn)