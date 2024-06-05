# llm-rag-app

This project is a full-stack web application that mimics the conversational experience of ChatGPT. It leverages a locally-run large language model (LLM) for core functionality and integrates a Retrieval-Augmented Generation (RAG) component to access and analyze PDF files.


## Key Features:

**Core Chat Functionalities:**

- **Text-based conversation:** Users can interact with the application through text prompts and receive responses in a chat-like interface.
- **Natural Language Processing (NLP):** The LLM is be able to understand the intent and context of user queries to provide relevant and informative responses.
- **Dialog history:** The application maintain a history of the conversation to allow for more coherent and relevant responses as the chat progresses.

**Advanced Features:**

- **Personality customization:** Users have the option to personalize the chat experience by defining different chat personalities or conversation styles for the LLM.
- **Local processing:** The application is connected to a local LLM model via Ollama server where the LLM is running. No information is sent to any external service.

**RAG Integration for PDF Analysis:**

- **PDF upload:** Users can upload PDF documents for analysis by the RAG component.
- **Keyword extraction:** The RAG component can identify and extract key terms and phrases from the uploaded PDFs.
- **Summarization:** The application provide summaries of the uploaded PDFs based on the extracted information.
- **Information retrieval:** The RAG component can be used to search and retrieve specific information from within the uploaded PDFs based on user queries.
- **Conversational integration:** The analysis of PDFs by RAG could be integrated into the chat conversation. For instance, the LLM could use the extracted information to answer user questions about the PDFs or guide them towards relevant sections.

## Architecture:
First, what is a RAG pipeline? Here's a breakdown of the workflow for a generic RAG application processing a PDF file:

**1. User Input:**

- The user uploads a PDF document through the application's interface.

**2. Preprocessing:**

- The uploaded PDF undergoes some preprocessing steps. This involves:
    - Removing irrelevant elements like headers, footers, or page numbers.
    - Text cleaning: Removing punctuation, stop words (common words with little meaning), and applying stemming/lemmatization (reducing words to their root form).
    - Splitting the document into smaller chunks via Semantic context. this will be useful later when retrieving the relevant informations.

**3. Document Representation:**

- The RAG system converts the different chunks text into a format suitable for analysis. This involve:
    - Tokenization: Breaking down the text into individual words or phrases.
    - Feature extraction: Creating numerical representations of the text that capture its meaning and relationships between words(vectorial representation).

**4. Retrieval:**

- The core of the RAG process:
    - The application utilizes the existing knowledge base of the pre-processed and indexed documents.
    - Based on the uploaded PDF's content, the RAG system searches the knowledge base to identify relevant passages or documents containing similar information relative to the user’s query.

**5. Augmentation:**

- Depending on the application's purpose, the retrieved information might be further processed:
    - Summarization: Generating a concise overview of the most relevant information from the retrieved documents.
    - Answer extraction: Identifying specific answers to user queries based on the retrieved passages.
    - Information filtering: Refining the retrieved information based on additional user input or context from the chat conversation (if applicable).

**6. Output:**

- The processed information from the PDF is presented to the user. This could involve:
    - Displaying retrieved text snippets or summaries within the application interface.
    - Integrating the information into the chat conversation, where the LLM might use it to answer user questions or guide them towards relevant sections of the PDF.

Here the complete architecture of the app:

**1. Front-End (Client-Side):**

The front-end is rendered via the Streamlit framework. It manages the following task:

- Handles user interaction through text input fields in the chat interface.
- Displays the conversation history and LLM responses.
- Provides options for uploading PDF document

**2. Back-End (Server-Side):**

It is made by the following components:

- **Streamlit App:** Runs on a server and interacts with both the LLM server and the RAG module.
- **Ollama Server:** Hosts and manages the LLM instance.
- **LlamaIndex pipeline:** Runs the RAG component responsible for PDF processing and information retrieval.

**3. Data Flow:**

- **User Input:** The user types a message in the Streamlit chat interface.
- **Streamlit App:**
    - Receives the user input when it types a message in the chat.
    - Forwards the user query to the RAG module for LLM processing.
- **LlamaIndex pipeline:**
    - Process the user query and retrieve the relevant chunks from the vector store index.
    - Include the retrieved chunks in the user query and sends the complete query to the Ollama server for LLM processing.
- **Ollama Server:**
    - Processes the user query through the LLM.
    - Streams the LLM response back to the Streamlit app.
- **Streamlit App:**
    - Receives the data streaming from the Ollama server.
    - Displays the LLM response in the chat interface.

## Usage

To use the chatbot, follow these steps:

1. **Install Ollama:**
   - If you haven't already, install Ollama by following the instructions provided on their official [website](https://ollama.com/download 'Link'). You can typically do this via package managers or by downloading the installer directly.

2. **Download a Model:**
   - Once Ollama is installed, download a suitable model for the chatbot. For instance, you can use Llama 3 8B. Use the following command or follow the steps outlined in the Ollama documentation:
     ```bash
     ollama download llama-3-8b
     ```

3. **Clone the Repository:**
   - Clone the repository containing the chatbot code to your local machine. Open a terminal and execute:
     ```bash
     git clone https://github.com/tiziaco/llm-rag-app.git
     ```
   - Navigate to the cloned repository:
     ```bash
     cd llm-rag-app
     ```
   - Ensure all dependencies are installed. You may need to set up a virtual environment and install requirements:
     ```bash
     python -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Run the Ollama Server:**
   - In a new terminal, start the Ollama server to serve the model. Typically, you can start the server with:
     ```bash
     ollama server start
     ```

5. **Run the Application:**
   - With the Ollama server running, open a new terminal in the project's folderand and start the chatbot application:
     ```bash
     python app.py
     ```

6. **Interact with the Chatbot Interface:**
   - Open your web browser and navigate to the interface where you can interact with the chatbot. The Streamlit application will provide the URL in the terminal, typically something like `http://localhost:8000`.
   - Start a conversation with the chatbot by typing your questions or prompts into the input field and hitting enter.


## Development

Feel free to extend this project by:

- Integrating additional functionality, such as direct PDF processing or different information extraction methods.
- Experimenting with different LLM and RAG configurations.
- Improving the user interface for a more intuitive experience.
