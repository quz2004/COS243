------
<!--- markdown-next --->
### Install Packages

------
<!--- code-next --->
```python
%pip install -q llama-index==0.10.18 llama-index-llms-groq==0.1.3 groq==0.4.2 llama-index-embeddings-huggingface==0.2.0
```

<!--- code-out#0001 --->

------
<!--- markdown-next --->
### Import Libraries

------
<!--- code-next --->
```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ServiceContext,
    load_index_from_storage
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq
# import os
# from dotenv import load_dotenv
# load_dotenv()
import warnings
warnings.filterwarnings('ignore')
```

<!--- code-out#0002 --->

------
<!--- code-next --->
```python
from google.colab import userdata
GROQ_API_KEY = userdata.get('GROQ_API_KEY')

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

------
<!--- markdown-next --->
### Data Ingestion

------
<!--- code-next --->
```python
!wget https://myweb.sabanciuniv.edu/rdehkharghani/files/2016/02/The-Morgan-Kaufmann-Series-in-Data-Management-Systems-Jiawei-Han-Micheline-Kamber-Jian-Pei-Data-Mining.-Concepts-and-Techniques-3rd-Edition-Morgan-Kaufmann-2011.pdf
```

<!--- code-out#0003 --->

------
<!--- code-next --->
```python
# data ingestion
reader = SimpleDirectoryReader(input_files=["./The-Morgan-Kaufmann-Series-in-Data-Management-Systems-Jiawei-Han-Micheline-Kamber-Jian-Pei-Data-Mining.-Concepts-and-Techniques-3rd-Edition-Morgan-Kaufmann-2011.pdf"])
documents = reader.load_data()
```

------
<!--- markdown-next --->
- `input_files` is a list!

------
<!--- markdown-next --->
https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader/

------
<!--- code-next --->
```python
len(documents) #
```

<!--- code-out#0004 --->

------
<!--- code-next --->
```python
documents[30].metadata
```

<!--- code-out#0005 --->

------
<!--- markdown-next --->
### Chunking

------
<!--- code-next --->
```python
text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
nodes = text_splitter.get_nodes_from_documents(documents, show_progress=True)
```

<!--- code-out#0006 --->

------
<!--- markdown-next --->
https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/modules/

------
<!--- code-next --->
```python
len(nodes)
```

<!--- code-out#0007 --->

------
<!--- code-next --->
```python
nodes[0].metadata
```

<!--- code-out#0008 --->

------
<!--- markdown-next --->
https://chunkviz.up.railway.app/

------
<!--- markdown-next --->
### Embedding Model

------
<!--- code-next --->
```python
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
```

<!--- code-out#0009 --->

------
<!--- markdown-next --->
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

------
<!--- markdown-next --->
https://huggingface.co/spaces/mteb/leaderboard

------
<!--- markdown-next --->
## Embedding illustration



------
<!--- code-next --->
```python
import numpy as np

from tabulate import tabulate

# Initialize the embedding model
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Sample texts
texts = [
    "The weather is nice today.",
    "I love eating pizza for dinner.",
    "Apple just released iPhone 17",
    "This red apple smells good",
    "Tesla stock rises as Trump wins the election",
    "Should I Sell My Individual Stocks and Reinvest in S&P 500/Nasdaq 100?"
]

# Generate embeddings for the texts
embeddings = [embed_model.get_text_embedding(text) for text in texts]

# Function to calculate cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Calculate similarities and prepare table data
table_data = []
for i in range(len(texts)):
    row = [f"Text {i+1}"]
    for j in range(len(texts)):
        if i == j:
            row.append("1.0000")
        elif j > i:
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            row.append(f"{similarity:.4f}")
        else:
            row.append("")
    table_data.append(row)

# Prepare headers
headers = [""] + [f"Text {i+1}" for i in range(len(texts))]

# Print the table
print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Print the text content for reference
print("\nText content:")
for i, text in enumerate(texts, 1):
    print(f"Text {i}: {text}")
```

<!--- code-out#0010 --->

------
<!--- markdown-next --->
HuggingFaceEmbedding in LlamaIndex is compatible with a wide range of embedding models available on the Hugging Face Hub. Here are some popular and high-performing models you can use:

1. BAAI/bge models:
   - "BAAI/bge-small-en-v1.5"
   - "BAAI/bge-base-en-v1.5"
   - "BAAI/bge-large-en-v1.5"

2. Sentence-transformers models:
   - "sentence-transformers/all-MiniLM-L6-v2"
   - "sentence-transformers/all-mpnet-base-v2"
   - "sentence-transformers/multi-qa-mpnet-base-dot-v1"

3. Instructor models:
   - "hkunlp/instructor-xl"
   - "hkunlp/instructor-large"

4. E5 models:
   - "intfloat/e5-large-v2"
   - "intfloat/multilingual-e5-large"

5. Multilingual models:
   - "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
   - "intfloat/multilingual-e5-large-instruct"

6. Domain-specific models:
   - "pritamdeka/S-PubMedBert-MS-MARCO" (for biomedical text)
   - "nlpaueb/legal-bert-small-uncased" (for legal text)



------
<!--- markdown-next --->

To use these models, you can simply specify the model name when initializing HuggingFaceEmbedding:

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
```

When choosing a model, consider factors such as:

1. Performance on relevant benchmarks (e.g., MTEB leaderboard)
2. Model size and inference speed
3. Language support (monolingual vs. multilingual)
4. Domain relevance
5. Compute resources available

It's also worth noting that you can use the Massive Text Embedding Benchmark (MTEB) Leaderboard to find the best performing models for your specific use case.

------
<!--- markdown-next --->
https://huggingface.co/spaces/mteb/leaderboard

------
<!--- markdown-next --->
### Define LLM Model

------
<!--- code-next --->
```python
llm = Groq(model="llama-3.1-70b-versatile", api_key=GROQ_API_KEY)
```

------
<!--- markdown-next --->
https://console.groq.com/docs/models

------
<!--- markdown-next --->
https://console.groq.com/keys

------
<!--- markdown-next --->
### Configure Service Context

------
<!--- code-next --->
```python
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)
```

------
<!--- markdown-next --->
### Create Vector Store Index

------
<!--- code-next --->
```python
vector_index = VectorStoreIndex.from_documents(documents, show_progress=True, service_context=service_context, node_parser=nodes)
```

<!--- code-out#0011 --->

------
<!--- markdown-next --->
https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/

------
<!--- markdown-next --->
#### Persist/Save Index

------
<!--- code-next --->
```python
from google.colab import drive
drive.mount('/content/drive')
```

<!--- code-out#0012 --->

------
<!--- code-next --->
```python
!mkdir /content/drive/MyDrive/Gen.AI/DB
```

------
<!--- code-next --->
```python
vectDB = "/content/drive/MyDrive/Gen.AI/DB/textbookstorage"
```

------
<!--- code-next --->
```python
vector_index.storage_context.persist(persist_dir=vectDB)
```

------
<!--- markdown-next --->
#### Define Storage Context

------
<!--- code-next --->
```python
storage_context = StorageContext.from_defaults(persist_dir=vectDB)
```

------
<!--- markdown-next --->
https://docs.llamaindex.ai/en/stable/api_reference/storage/storage_context/

------
<!--- markdown-next --->
#### Load Index

------
<!--- code-next --->
```python
index = load_index_from_storage(storage_context, service_context=service_context)
```

------
<!--- markdown-next --->
### Define Query Engine

------
<!--- code-next --->
```python
query_engine = index.as_query_engine(service_context=service_context)
```

------
<!--- markdown-next --->
https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/

------
<!--- markdown-next --->
#### Feed in user query

------
<!--- markdown-next --->
https://docs.llamaindex.ai/en/stable/examples/prompts/prompts_rag/#viewingcustomizing-prompts

------
<!--- code-next --->
```python
query = "Explain cosine similarity"
resp = query_engine.query(query)
```

------
<!--- code-next --->
```python
import textwrap

def Print(text, width=80, **args):
    lines = text.split('\n')  # Split the text into lines based on original line breaks
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(textwrap.wrap(line, width=width))  # Wrap each line individually
    print('\n'.join(wrapped_lines), **args)


```

------
<!--- code-next --->
```python
Print(resp.response)
```

<!--- code-out#0013 --->

------
<!--- markdown-next --->
### Get Source

------
<!--- code-next --->
```python
for node in resp.source_nodes:
    # Access the TextNode object directly
    text_node = node.node

    # Assuming metadata is stored within the TextNode's metadata
    source = text_node.metadata.get('file_name') # Access metadata using .metadata.get()
    page = text_node.metadata.get('page_label')  # Access metadata using .metadata.get()

    Print(f"Source: {source}")
    Print(f"Page: {page}")
```

<!--- code-out#0014 --->

------
<!--- code-next --->
```python
query = """Create concept check questions and answer about cosine similarity.
Format output in markdown with 2 line breaks to separate markdown entities"""
resp = query_engine.query(query)
Print(resp.response)
```

<!--- code-out#0015 --->

------
<!--- markdown-next --->
https://itsjb13.medium.com/building-a-rag-chatbot-using-llamaindex-groq-with-llama3-chainlit-b1709f770f55

------
<!--- markdown-next --->
https://docs.llamaindex.ai/en/stable/optimizing/production_rag/

