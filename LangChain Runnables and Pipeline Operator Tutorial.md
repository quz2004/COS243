# LangChain Runnables and Pipeline Operator Tutorial


### Introduction

In this tutorial, we'll explore LangChain's runnables and the pipeline operator. These powerful features allow you to create modular, efficient AI workflows.

### What are Runnables?

Runnables in LangChain are components that can be executed as part of a chain or pipeline. They form the building blocks of more complex AI applications.

### Creating a Basic Runnable

Let's start with a simple example:

```python
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

runnable = RunnableLambda(add_one)
```

Here, we've converted a plain Python function into a runnable object.

### Using Runnables

#### Direct Invocation

```python
result = runnable.invoke(1)  # returns 2
```

#### Batch Operations

```python
results = runnable.batch([1, 2, 3])  # returns [2, 3, 4]
```

### The Pipeline Operator

The pipeline operator (`|`) in LangChain allows you to chain runnables together.

#### Example:

```python
def multiply_by_two(x):
    return x * 2

multiply_by_two = RunnableLambda(multiply_by_two)
chain = add_one | multiply_by_two

result = chain.invoke(3)  # (3 + 1) * 2 = 8
```

### Plain Functions as Runnables

LangChain provides a decorator to easily convert functions into runnables:

```python
from langchain_core.runnables import chain

@chain
def custom_function(input_dict):
    # Process input_dict
    return result
```

### Building Complex Workflows

Let's create a more advanced example using LangChain components:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("Tell me a fact about {topic}")
model = ChatOpenAI()
output_parser = StrOutputParser()

chain = prompt | model | output_parser

result = chain.invoke({"topic": "space"})
```

This chain generates a fact about a given topic using a language model.

### Conclusion

Runnables and the pipeline operator in LangChain provide a flexible and powerful way to create modular AI workflows. By breaking down complex tasks into smaller, reusable components, you can build scalable and maintainable AI applications.
