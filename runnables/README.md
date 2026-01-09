# Deep Dive: Runnables in LangChain

## 📖 Overview

This guide provides a deep dive into **Runnables** in LangChain. It explains the evolution of the framework, the limitations of the "Chain" architecture, and how Runnables solve the problem of standardization to simplify the development of LLM-based applications.

> **Key Takeaway:** Understanding Runnables is essential for mastering modern LangChain (v0.3+), as they form the backbone of how components interact.

---

## 📑 Table of Contents

1. [The Evolution of LangChain](https://www.google.com/search?q=%23-the-evolution-of-langchain)
2. [The Problem: The "Chain" Era](https://www.google.com/search?q=%23-the-problem-the-chain-era)
3. [The Root Cause: Non-Standardization](https://www.google.com/search?q=%23-the-root-cause-non-standardization)
4. [The Solution: Runnables](https://www.google.com/search?q=%23-the-solution-runnables)
5. [The Standard Interface](https://www.google.com/search?q=%23-the-standard-interface)
6. [Code Demonstration: The "Old Way"](https://www.google.com/search?q=%23-code-demonstration-the-old-way)

---

## 📜 The Evolution of LangChain

To understand Runnables, we must look at the history of the framework:

### Phase 1: API Abstraction

When LLMs (like ChatGPT) exploded in popularity, various providers (OpenAI, Google, Mistral) emerged with different APIs. LangChain's first value proposition was **Abstraction**: creating a single framework that allowed developers to swap LLMs with minimal code changes.

### Phase 2: The Component Ecosystem

Building real-world apps (like PDF Readers or Agents) required more than just an LLM. It required a pipeline. LangChain introduced specific components for every step:

* **Document Loaders** (Loading data)
* **Text Splitters** (Chunking data)
* **Embedding Models** (Vectorizing data)
* **Vector Stores** (Storing embeddings)
* **Retrievers** (Semantic search)

### Phase 3: The Era of Chains

LangChain noticed common patterns in how developers connected these components. To automate this, they introduced **Chains**.

* **LLMChain:** Connects a Prompt Template → LLM.
* **RetrievalQAChain:** Encapsulates the RAG pipeline (Retrieve → Prompt → LLM).

---

## ⚠️ The Problem: The "Chain" Era

While Chains initially helped, they eventually caused significant issues:

1. **Proliferation of Chains:** LangChain created a specific chain for every use case (Math Chain, SQL Chain, API Chain, etc.).
2. **Maintenance Nightmare:** The codebase became massive and difficult to maintain.
3. **Steep Learning Curve:** Developers struggled to know *which* chain to use.
4. **Rigidity:** It was difficult to customize the internals of a pre-built chain.

---

## 🔍 The Root Cause: Non-Standardization

The fundamental issue was that the original components were **not standardized**. They were developed independently and used different method names:

| Component | Method Name |
| --- | --- |
| **LLM** | `.predict()` |
| **PromptTemplate** | `.format()` |
| **Retriever** | `.get_relevant_documents()` |
| **Parser** | `.parse()` |

Because every component spoke a "different language," LangChain had to write manual wrapper code (Chains) just to glue them together.

---

## ✅ The Solution: Runnables

LangChain rebuilt their ecosystem around the concept of **Runnables**.

### What is a Runnable?

A Runnable is a **Unit of Work**. It is a protocol that ensures every component follows a **Common Interface**.

### The Lego Analogy

* **Unit of Work:** Each Lego block has a specific purpose.
* **Common Interface:** All blocks have the same studs/tubes, allowing them to connect regardless of shape.
* **Composability:** You can build a small structure, and then treat that structure as a single block to build something even bigger.

In LangChain, this allows for **Infinite Nesting**. A chain of Runnables is *itself* a Runnable.

---

## ⚙️ The Standard Interface

All Runnables must implement the following core methods. This guarantees that the output of one component can automatically become the input of the next.

* **`invoke(input)`**: Takes a single input and returns a single output.
* **`batch([inputs])`**: Processes a list of inputs simultaneously.
* **`stream(input)`**: Streams the output chunks back to the user (crucial for LLM latency).

---

## 💻 Code Demonstration: The "Old Way"

*This conceptual demo illustrates the **problem** Runnables solve. In the old system (simulated below via "Nakli" or "Dummy" classes), components had arbitrary method names, making them impossible to chain automatically.*

### 1. The Dummy LLM (`NakliLLM`)

Uses `.predict()` instead of a standard method.

```python
import random

class NakliLLM:
    def __init__(self):
        print("LLM Created")
    
    # Non-standard method name
    def predict(self, prompt):
        replies = ["That is interesting", "I don't know", "LangChain is cool"]
        return random.choice(replies)

# Usage
llm = NakliLLM()
response = llm.predict("Hello")
print(response)

```

### 2. The Dummy Prompt (`NakliPromptTemplate`)

Uses `.format()` instead of a standard method.

```python
class NakliPromptTemplate:
    def __init__(self, template, input_variables):
        self.template = template
        self.variables = input_variables
    
    # Non-standard method name
    def format(self, input_dict):
        return self.template.format(**input_dict)

# Usage
prompt = NakliPromptTemplate("Tell me a joke about {topic}", ["topic"])
formatted_text = prompt.format({'topic': 'AI'})
print(formatted_text)

```

**The Takeaway:** Because `.predict()` and `.format()` are different method names, you cannot simply pipe them together. You need a "Glue" layer. **Runnables remove the need for this glue by forcing everyone to use `.invoke()`.**