------
<!--- markdown-next --->
# Llamaindex Cookbook with Llama3 through Groq



Meta developed and released the Meta [Llama 3](https://ai.meta.com/blog/meta-llama-3/) family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8 and 70B sizes. The Llama 3 instruction tuned models are optimized for dialogue use cases and outperform many of the available open source chat models on common industry benchmarks.

In this notebook, we demonstrate how to use Llama3 with LlamaIndex for a comprehensive set of use cases.
1. Basic completion / chat
2. Basic RAG (Vector Search, Summarization)
3. Advanced RAG (Routing)
4. Text-to-SQL
5. Structured Data Extraction
6. Chat Engine + Memory
7. Agents


We use Llama3-8B and Llama3-70B through Groq.

------
<!--- markdown-next --->
## Installation and Setup

------
<!--- code-next --->
```python
!pip install -q llama-index llama-index-llms-groq  llama-index-embeddings-huggingface   llama-parse
```

<!--- code-out#0001 --->

------
<!--- code-next --->
```python
import nest_asyncio

nest_asyncio.apply()
```

------
<!--- markdown-next --->
### Setup LLM using Groq

To use Groq, you need to make sure that `GROQ_API_KEY` is specified as an environment variable.

------
<!--- code-next --->
```python
import os
from google.colab import userdata
GROQ_API_KEY = userdata.get('GROQ_API_KEY')
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
```

------
<!--- code-next --->
```python
from llama_index.llms.groq import Groq

llm = Groq(model="llama3-8b-8192", api_key=GROQ_API_KEY)
llm_70b = Groq(model="llama-3.1-70b-versatile", api_key=GROQ_API_KEY)
```

------
<!--- markdown-next --->
### Setup Embedding Model

------
<!--- code-next --->
```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
```

<!--- code-out#0002 --->

------
<!--- markdown-next --->
### Define Global Settings Configuration

In LlamaIndex, you can define global settings so you don't have to pass the LLM / embedding model objects everywhere.

------
<!--- code-next --->
```python
from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model
```

------
<!--- markdown-next --->
### Download Data

Here you'll download data that's used in section 2 and onwards.

We'll download a book "The Theory never dies"

------
<!--- code-next --->
```python
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

def download_google_drive_file(file_id, destination_path):
    # Authenticate and create the Drive API client
    auth.authenticate_user()
    drive_service = build('drive', 'v3')

    # Request the file metadata
    file_metadata = drive_service.files().get(fileId=file_id).execute()
    file_name = file_metadata['name']

    # Download the file
    request = drive_service.files().get_media(fileId=file_id)
    file_content = io.BytesIO()
    downloader = MediaIoBaseDownload(file_content, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    # Save the file
    file_content.seek(0)
    with open(destination_path, 'wb') as f:
        f.write(file_content.read())

    print(f"File {file_name} downloaded successfully to {destination_path}")

# Example usage
file_id = '10y-4IHuloL8tnB_bsqnW_7khPec515CX'  #  file ID
book_path = '/content/data/The Theory That Would Not Die How Bayes Rule Cracked the Enigma Code, Hunted Down Russian Submarines, and Emerged Triumphant from Two Centuries of Controversy by Sharon Bertsch McGrayne.pdf'  # Destination in Colab

download_google_drive_file(file_id, book_path)
```

<!--- code-out#0003 --->

------
<!--- code-next --->
```python
!mkdir data
!wget https://drive.google.com/file/d/10y-4IHuloL8tnB_bsqnW_7khPec515CX/view?usp=sharing

```

<!--- code-out#0004 --->

------
<!--- markdown-next --->
### Load Data

We load data using LlamaParse by default, but you can also choose to opt for our free pypdf reader (in SimpleDirectoryReader by default) if you don't have an account!

1. LlamaParse: Signup for an account here: [cloud.llamaindex.ai](https://cloud.llamaindex.ai). You get 1k free pages a day, and paid plan is 7k free pages + 0.3c per additional page. LlamaParse is a good option if you want to parse complex documents, like PDFs with charts, tables, and more.

2. Default PDF Parser (In `SimpleDirectoryReader`). If you don't want to signup for an account / use a PDF service, just use the default PyPDF reader bundled in our file loader. It's a good choice for getting started!

------
<!--- code-next --->
```python
from llama_parse import LlamaParse
LLAMAINDEX_API_KEY = userdata.get('LLAMAINDEX_API_KEY')

"""
docs_bayes = LlamaParse(result_type="text", api_key=LLAMAINDEX_API_KEY).load_data(book_path)
)
"""

from llama_index.core import SimpleDirectoryReader

docs_bayes = SimpleDirectoryReader(input_files=[book_path]).load_data()
```

------
<!--- markdown-next --->
## 1. Basic Completion and Chat

------
<!--- code-next --->
```python
import textwrap
from pprint import pprint

def Print(text, width=80, **args):
    lines = text.split('\n')  # Split the text into lines based on original line breaks
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(textwrap.wrap(line, width=width))  # Wrap each line individually
    print('\n'.join(wrapped_lines), **args)

```

------
<!--- markdown-next --->
### Call complete with a prompt (LLM only, no RAG)

------
<!--- code-next --->
```python
response = llm.complete("do you like Thomas Bayes?")

Print((response).text)
```

<!--- code-out#0005 --->

------
<!--- code-next --->
```python
stream_response = llm.stream_complete(
    "you're a Bayesian fan. tell me why you like Bayesian more than Frequentists"
)

for t in stream_response:
    print(t.delta, end="")
```

<!--- code-out#0006 --->

------
<!--- markdown-next --->
### Call chat with a list of messages (LLM only, no RAG)

------
<!--- code-next --->
```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(role="system", content="You are a Bayesian fan."),
    ChatMessage(role="user", content="Write a verse."),
]
response = llm.chat(messages)
```

------
<!--- code-next --->
```python
print(response)
```

<!--- code-out#0007 --->

------
<!--- markdown-next --->
## 2. Basic RAG (Vector Search, Summarization)

------
<!--- markdown-next --->
### Basic RAG (Vector Search)

------
<!--- code-next --->
```python

from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(docs_bayes)
query_engine = index.as_query_engine(similarity_top_k=5)
```

------
<!--- code-next --->
```python
response = query_engine.query("Tell me about 5 Applications of Bayes Theorem")
```

------
<!--- code-next --->
```python
pprint(str(response))
```

<!--- code-out#0008 --->

------
<!--- code-next --->
```python
def GetSources(response):
  for node in response.source_nodes:
      # Access the TextNode object directly
      text_node = node.node

      # Assuming metadata is stored within the TextNode's metadata
      source = text_node.metadata.get('file_name') # Access metadata using .metadata.get()
      page = text_node.metadata.get('page_label')  # Access metadata using .metadata.get()

      Print(f"Source: {source[:30]}...")
      Print(f"Page: {page}")

GetSources(response)
```

<!--- code-out#0009 --->

------
<!--- markdown-next --->
### Basic RAG (Summarization)

------
<!--- code-next --->
```python
from llama_index.core import SummaryIndex

summary_index = SummaryIndex.from_documents(docs_bayes)
summary_engine = summary_index.as_query_engine()
```

------
<!--- code-next --->
```python
response = summary_engine.query(
    """Given info from the provided sources, analyze how Bayesian probability transformed
    from a controversial mathematical concept to a critical tool in military intelligence"""
)
```

------
<!--- code-next --->
```python
Print(str(response))
```

<!--- code-out#0010 --->

------
<!--- code-next --->
```python
GetSources(response)
```

<!--- code-out#0011 --->

------
<!--- markdown-next --->
## 3. Advanced RAG (Routing)

------
<!--- markdown-next --->
### Build a Router that can choose whether to do vector search or summarization

------
<!--- code-next --->
```python
from llama_index.core.tools import QueryEngineTool, ToolMetadata

vector_tool = QueryEngineTool(
    index.as_query_engine(),
    metadata=ToolMetadata(
        name="vector_search",
        description="Useful for searching for specific facts.",
    ),
)

summary_tool = QueryEngineTool(
    index.as_query_engine(response_mode="tree_summarize"),
    metadata=ToolMetadata(
        name="summary",
        description="Useful for summarizing an entire document.",
    ),
)
```

------
<!--- code-next --->
```python
from llama_index.core.query_engine import RouterQueryEngine

query_engine = RouterQueryEngine.from_defaults(
    [vector_tool, summary_tool], select_multi=False, verbose=True, llm=llm_70b
)

response = query_engine.query(
    "Tell me about the specific details about Alan Turing's cryptographic methods at Bletchley Park"
)
```

<!--- code-out#0012 --->

------
<!--- code-next --->
```python
pprint(response)
```

<!--- code-out#0013 --->

------
<!--- code-next --->
```python
response = query_engine.query(
    "Provide a comprehensive overview of how Bayesian probability evolved from"
    " a theoretical concept to a critical wartime intelligence tool"
    )
print(response)

```

<!--- code-out#0014 --->

------
<!--- markdown-next --->
## 4. Text-to-SQL

Here, we download and use a sample SQLite database with 11 tables, with various info about music, playlists, and customers. We will limit to a select few tables for this test.

------
<!--- code-next --->
```python
!wget "https://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip" -O "./data/chinook.zip"
!unzip "./data/chinook.zip"
```

<!--- code-out#0015 --->

------
<!--- code-next --->
```python
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
    column,
)

engine = create_engine("sqlite:///chinook.db")
```

------
<!--- code-next --->
```python
from llama_index.core import SQLDatabase

sql_database = SQLDatabase(engine)
```

------
<!--- code-next --->
```python
from llama_index.core.indices.struct_store import NLSQLTableQueryEngine

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["albums", "tracks", "artists"],
    llm=llm_70b,
)
```

------
<!--- code-next --->
```python
response = query_engine.query("What are some albums?")

print(response)
```

<!--- code-out#0016 --->

------
<!--- code-next --->
```python
response = query_engine.query("What are some artists? Limit it to 5.")

pprint(response)
```

<!--- code-out#0017 --->

------
<!--- markdown-next --->
This last query should be a more complex join

------
<!--- code-next --->
```python
response = query_engine.query(
    "What are some tracks from the artist AC/DC? Limit it to 3"
)

pprint(response)
```

<!--- code-out#0018 --->

------
<!--- code-next --->
```python
pprint(response.metadata["sql_query"])
```

<!--- code-out#0019 --->

------
<!--- markdown-next --->
## 5. Structured Data Extraction

An important use case for function calling is extracting structured objects. LlamaIndex provides an intuitive interface for this through `structured_predict` - simply define the target Pydantic class (can be nested), and given a prompt, we extract out the desired object.

**NOTE**: Since there's no native function calling support with Llama3, the structured extraction is performed by prompting the LLM + output parsing.

------
<!--- code-next --->
```python
from llama_index.llms.groq import Groq
from llama_index.core.prompts import PromptTemplate
from pydantic import BaseModel


class Restaurant(BaseModel):
    """A restaurant with name, city, and cuisine."""

    name: str
    city: str
    cuisine: str


llm = Groq(model="llama3-8b-8192",
           pydantic_program_mode="llm",
           api_key=GROQ_API_KEY)
# pydantic_program_mode="llm": This argument sets the behavior of the Groq object
# when it works with pydantic models. pydantic is used for data validation and
# parsing, making sure the data received is in the expected format.
# Here, it instructs the Groq object to use the LLM itself for handling pydantic
# operations. This allows you to structure the LLM's responses using pydantic model
# definitions.

prompt_tmpl = PromptTemplate(
    "Generate a restaurant in a given city {city_name}"
)
```

------
<!--- code-next --->
```python
restaurant_obj = llm.structured_predict(
    Restaurant, prompt_tmpl, city_name="Miami"
)
print(restaurant_obj)
```

<!--- code-out#0020 --->

------
<!--- markdown-next --->

1. The `Restaurant` class is passed as the first argument to `structured_predict`. This tells the method what Pydantic model structure to expect in the output.

2. Internally, the `structured_predict` method likely constructs a more complex prompt that includes:
   - The original prompt template ("Generate a restaurant in a given city Miami")
   - Information about the `Restaurant` model structure (name, city, cuisine)

3. The constructed prompt might look something like this:

   ```
   Generate a restaurant in a given city Miami

   Please provide the information in the following format:
   {
     "name": "Restaurant name",
     "city": "Miami",
     "cuisine": "Type of cuisine"
   }
   ```

4. This enhanced prompt is then sent to the Groq LLM (llama3-8b-8192 in this case).

5. The LLM generates a response based on this prompt, attempting to structure its output according to the specified format.

6. The `structured_predict` method then takes the LLM's output and attempts to parse it into a `Restaurant` object, validating the data against the Pydantic model's rules.

By passing the `Restaurant` class to `structured_predict`, you're essentially instructing the method to both guide the LLM in producing a structured output and to validate and parse that output into a Pydantic model instance. This process combines the power of the LLM's text generation with Pydantic's data validation capabilities, resulting in a structured `restaurant_obj` that conforms to the `Restaurant` model specification.


------
<!--- markdown-next --->
## 6. Adding Chat History to RAG (Chat Engine)

In this section we create a stateful chatbot from a RAG pipeline, with our chat engine abstraction.

Unlike a stateless query engine, the chat engine maintains conversation history (through a memory module like buffer memory). It performs retrieval given a condensed question, and feeds the condensed question + context + chat history into the final LLM prompt.

Related resource: https://docs.llamaindex.ai/en/stable/examples/chat_engine/chat_engine_condense_plus_context/

------
<!--- code-next --->
```python
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine

memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

chat_engine = CondensePlusContextChatEngine.from_defaults(
    index.as_retriever(),
    memory=memory,
    llm=llm,
    context_prompt=(
        "You are a chatbot, able to have normal interactions, as well as talk"
        " about the Kendrick and Drake beef."
        "Here are the relevant documents for the context:\n"
        "{context_str}"
        "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
    ),
    verbose=True,
)
```

------
<!--- markdown-next --->
The `context_str` is  a placeholder within the `context_prompt` string that will be filled in later by the `CondensePlusContextChatEngine`.

Here's how the `context_str` gets its value:

1. The `CondensePlusContextChatEngine` is initialized with a retriever (created from the index) and the `context_prompt` template.

2. When a user query is received, the chat engine uses the retriever to fetch relevant documents from the index.

3. The retrieved documents are then processed and combined into a single string, which becomes the `context_str`.

4. The chat engine then uses this `context_str` to fill in the placeholder in the `context_prompt` template.

5. This filled-in prompt, now containing the actual context information, is then sent to the language model (LLM) along with the user's query.

The `{context_str}` placeholder in the prompt template allows for dynamic insertion of relevant context for each query, without having to modify the prompt template itself. This process happens internally within the `CondensePlusContextChatEngine`, which handles the retrieval, context insertion, and interaction with the LLM.


------
<!--- code-next --->
```python
response = chat_engine.chat(
    "Tell me about the songs Drake released in the beef."
)
print(str(response))
```

<!--- code-out#0021 --->

------
<!--- code-next --->
```python
response = chat_engine.chat("What about Kendrick?")
print(str(response))
```

<!--- code-out#0022 --->

------
<!--- markdown-next --->
## 7. Agents

Here we build agents with Llama 3. We perform RAG over simple functions as well as the documents above.

------
<!--- markdown-next --->
### Agents And Tools

------
<!--- code-next --->
```python
import json
from typing import Sequence, List

from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.agent import ReActAgent

import nest_asyncio

nest_asyncio.apply()
```

------
<!--- markdown-next --->
### Define Tools

------
<!--- code-next --->
```python
def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b


def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


def subtract(a: int, b: int) -> int:
    """Subtract two integers and returns the result integer"""
    return a - b


def divide(a: int, b: int) -> int:
    """Divides two integers and returns the result integer"""
    return a / b


multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)
subtract_tool = FunctionTool.from_defaults(fn=subtract)
divide_tool = FunctionTool.from_defaults(fn=divide)
```

------
<!--- markdown-next --->
### ReAct Agent

------
<!--- code-next --->
```python
agent = ReActAgent.from_tools(
    [multiply_tool, add_tool, subtract_tool, divide_tool],
    llm=llm_70b,
    verbose=True,
)
```

------
<!--- markdown-next --->
### Querying

------
<!--- code-next --->
```python
response = agent.chat("What is (121 + 2) * 5?")
print(str(response))
```

<!--- code-out#0023 --->

------
<!--- markdown-next --->
### ReAct Agent With RAG QueryEngine Tools

------
<!--- code-next --->
```python
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

from llama_index.core.tools import QueryEngineTool, ToolMetadata
```

------
<!--- markdown-next --->
### Create ReAct Agent using RAG QueryEngine Tools

------
<!--- code-next --->
```python
bayes_tool = QueryEngineTool(
    index.as_query_engine(),
    metadata=ToolMetadata(
        name="bayes_search",
        description="Useful for searching over Thomas Bayes' life.",
    ),
)

wwii_tool = QueryEngineTool(
    index.as_query_engine(),
    metadata=ToolMetadata(
        name="wwii_search",
        description="Useful for searching over WWII related information.",
    ),
)

query_engine_tools = [bayes_tool, wwii_tool]
```

------
<!--- code-next --->
```python
agent = ReActAgent.from_tools(
    query_engine_tools,  ## TODO: define query tools
    llm=llm_70b,
    verbose=True,
)
```

------
<!--- markdown-next --->
### Querying

------
<!--- code-next --->
```python
response = agent.chat("Tell me about Thomas Bayse early work on theology"
" and how this is related to Bayes theorem")
print(str(response))
```

<!--- code-out#0024 --->

------
<!--- code-next --->
```python
response = agent.chat("Tell me about interaction between Alan Turing and Claude Shannon"
                      " and how this impact Shannon's work on information theory"
)
print(str(response))
```

<!--- code-out#0025 --->

------
<!--- code-next --->
```python
response = agent.chat("Tell me about how Bayes theorem is used in Midway Battle"
)
print(str(response))
```

<!--- code-out#0026 --->

