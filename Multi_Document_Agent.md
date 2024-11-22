------
<!--- markdown-next --->
# Llamaindex with Multi-Document Agents

In this notebook we will look into Building RAG when you have a large number of documents using `DocumentAgents` concept with `ReAct Agent`.

------
<!--- markdown-next --->
### Installation

------
<!--- code-next --->
```python
%pip install -q llama-index
%pip install -q llama-index-llms-groq
%pip install -q llama-index-embeddings-huggingface

```

------
<!--- markdown-next --->
### Set Logging

------
<!--- code-next --->
```python
# NOTE: This is ONLY necessary in jupyter notebook.
# Details: Jupyter runs an event-loop behind the scenes.
#          This results in nested event-loops when we start an event-loop to make async queries.
#          This is normally not allowed, we use nest_asyncio to allow it for convenience.
import nest_asyncio

nest_asyncio.apply()

import logging
import sys

# Set up the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set logger level to INFO

# Clear out any existing handlers
logger.handlers = []

# Set up the StreamHandler to output to sys.stdout (Colab's output)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)  # Set handler level to INFO

# Add the handler to the logger
logger.addHandler(handler)

from IPython.display import display, HTML

```

------
<!--- markdown-next --->
### Setup and imports

------
<!--- code-next --->
```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage
)
from llama_index.core.settings import Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

```

<!--- code-out#0001 --->

------
<!--- code-next --->
```python
from google.colab import userdata

llm = Groq(model="llama3-groq-70b-8192-tool-use-preview", api_key=userdata.get('GROQ_API_KEY'))
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

```

<!--- code-out#0002 --->

------
<!--- code-next --->
```python
from llama_index.core import Settings
Settings.llm = llm
Settings.embed_model = embed_model
Settings.chunk_size = 512

```

------
<!--- markdown-next --->
### Download Documents

We will use Wikipedia pages of `Toronto`, `Seattle`, `Chicago`, `Boston`, `Houston` cities and build RAG pipeline.

------
<!--- code-next --->
```python
wiki_titles = ["Toronto", "Seattle", "Chicago", "Boston", "Houston"]

from pathlib import Path

import requests

for title in wiki_titles:
    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts",
            # 'exintro': True,
            "explaintext": True,
        },
    ).json()
    page = next(iter(response["query"]["pages"].values()))
    wiki_text = page["extract"]

    data_path = Path("data")
    if not data_path.exists():
        Path.mkdir(data_path)

    with open(data_path / f"{title}.txt", "w") as fp:
        fp.write(wiki_text)

```

------
<!--- markdown-next --->
### Load Document

------
<!--- code-next --->
```python
# Load all wiki documents

from llama_index.core import SimpleDirectoryReader

city_docs = {}
for wiki_title in wiki_titles:
    city_docs[wiki_title] = SimpleDirectoryReader(
        input_files=[f"data/{wiki_title}.txt"]
    ).load_data()

```

------
<!--- markdown-next --->
#### Build ReAct Agent for each city

------
<!--- code-next --->
```python
from llama_index.core.agent import ReActAgent
from llama_index.core import VectorStoreIndex, SummaryIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata

# Build agents dictionary
agents = {}

for wiki_title in wiki_titles:
    # build vector index
    vector_index = VectorStoreIndex.from_documents(
        city_docs[wiki_title],
    )
    # build summary index
    summary_index = SummaryIndex.from_documents(
        city_docs[wiki_title],
    )
    # define query engines
    vector_query_engine = vector_index.as_query_engine()
    summary_query_engine = summary_index.as_query_engine()

    # define tools
    query_engine_tools = [
        QueryEngineTool(
            query_engine=vector_query_engine,
            metadata=ToolMetadata(
                name="vector_tool",
                description=(
                    f"Useful for retrieving specific context from {wiki_title}"
                ),
            ),
        ),
        QueryEngineTool(
            query_engine=summary_query_engine,
            metadata=ToolMetadata(
                name="summary_tool",
                description=(
                    "Useful for summarization questions related to"
                    f" {wiki_title}"
                ),
            ),
        ),
    ]

    # build agent
    agent = ReActAgent.from_tools(
        query_engine_tools,
        llm=llm,
        verbose=True,
    )

    agents[wiki_title] = agent

```

<!--- code-out#0003 --->

------
<!--- markdown-next --->
#### Define IndexNode for each of these Agents

------
<!--- code-next --->
```python
from llama_index.core.schema import IndexNode

# define top-level nodes
objects = []
for wiki_title in wiki_titles:
    # define index node that links to these agents
    wiki_summary = (
        f"This content contains Wikipedia articles about {wiki_title}. Use"
        " this index if you need to lookup specific facts about"
        f" {wiki_title}.\nDo not use this index if you want to analyze"
        " multiple cities."
    )
    node = IndexNode(
        text=wiki_summary, index_id=wiki_title, obj=agents[wiki_title]
    )
    objects.append(node)

```

------
<!--- markdown-next --->
#### Define Top-Level Retriever to choose an Agent

------
<!--- code-next --->
```python
vector_index = VectorStoreIndex(
    objects=objects,
)
query_engine = vector_index.as_query_engine(similarity_top_k=1, verbose=True)

```

<!--- code-out#0004 --->


------
<!--- markdown-next --->
#### Test Queries

Should choose a vector tool/ summary tool for a specific agent based on the query.

------
<!--- code-next --->
```python
# Helper function for print
def print_response(response):
    display(HTML(f'<p style="font-size:20px">{response.response}</p>'))
```

------
<!--- code-next --->
```python
# should use Toronto agent -> vector tool
response = query_engine.query("What is the population of Toronto?")

```

<!--- code-out#0005 --->

------
<!--- code-next --->
```python
print_response(response)
```

<!--- code-out#0006 --->

------
<!--- code-next --->
```python
# should use Houston agent -> vector tool
response = query_engine.query("Who and when was Houston founded?")

```

<!--- code-out#0007 --->

------
<!--- code-next --->
```python
print_response(response)
```

<!--- code-out#0008 --->

------
<!--- code-next --->
```python
# should use Boston agent -> summary tool
response = query_engine.query("Summarize about the sports teams in Boston")

```

<!--- code-out#0009 --->

------
<!--- code-next --->
```python
print_response(response)
```

<!--- code-out#0010 --->

------
<!--- code-next --->
```python
# should use Seattle agent -> summary tool
response = query_engine.query(
    "Give me a summary on all the positive aspects of Chicago"
)

```

<!--- code-out#0011 --->

------
<!--- code-next --->
```python
print_response(response)
```

<!--- code-out#0012 --->

------
<!--- code-next --->
```python

```

