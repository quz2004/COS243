------
<!--- markdown-next --->
### Project Dependencies and Setup

- Create new env with packages in `requirements.txt`
```bash
gradio==4.44.1
gradio_client==1.3.0
langchain-ollama==0.2.0
llama-index==0.12.2
llama-index-agent-openai==0.4.0
llama-index-cli==0.4.0
llama-index-core==0.12.2
llama-index-embeddings-huggingface==0.4.0
llama-index-embeddings-openai==0.3.1
llama-index-indices-managed-llama-cloud==0.6.3
llama-index-legacy==0.9.48.post4
llama-index-llms-ollama==0.4.1
llama-index-llms-openai==0.3.2
llama-index-multi-modal-llms-openai==0.3.0
llama-index-program-openai==0.3.1
llama-index-question-gen-openai==0.3.0
llama-index-readers-file==0.4.0
llama-index-readers-llama-parse==0.4.0
ollama==0.3.3
```
# Local AI Librarian: Intelligent eBook Search and Management System

## Project Overview
Build a local AI-powered librarian application that enables intelligent searching and interaction with personal ebook collections using advanced RAG (Retrieval-Augmented Generation) techniques.

## Key Features
- Supports uploading/importing ebook collections
- Intelligent search with citations
- Conversation history management
- Gradio web interface
- Local AI processing using Phi3.5

## Technical Components
1. Document Loader
2. Vector Embedding Generation
3. RAG Query Engine
4. Gradio Interface
5. Conversation Tracking

## Implementation Steps

### 1. Environment Setup
- Install dependencies:
  ```bash
  pip install -q \
    llama-index \
    EbookLib \
    html2text \
    gradio \
    llama-index-embeddings-huggingface \
    llama-index-llms-ollama
  ```

### 2. Document Processing
- Use LlamaIndex's `SimpleDirectoryReader`
- Support multiple ebook formats (.epub, .pdf)
- Implement robust text extraction
- Chunk documents for efficient embedding

### 3. Embedding Generation
- Use lightweight embedding model (e.g., BAAI/bge-small-en-v1.5)
- Create vector index for semantic search
- Implement efficient indexing strategy

### 4. Query Engine
- Configure Phi3.5 from Ollama
- Implement RAG pipeline
- Force citation generation
- Handle conversation history

### 5. Gradio Interface Design
- Create upload/import functionality
- Design query interface with:
  - Search input
  - Conversation history display
  - Source citation display
  - Premade prompt examples

### 6. Additional Features
- Save/export conversation history
- Add documents to library from conversation
- Error handling for document processing

## Evaluation Criteria
- Accuracy of search results
- Citation quality
- User interface intuitiveness
- Performance with large document collections

## Recommended Testing Approach
1. Unit test each component independently
2. Integration testing of RAG pipeline
3. User acceptance testing with varied document types
4. Performance benchmarking

## Potential Extensions
- Support multimodal materials in lib collection
- Add books/webpages vie URL
- Search internet
- Implement advanced filtering
- Add metadata extraction
