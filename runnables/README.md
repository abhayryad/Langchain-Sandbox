# Deep Dive: Runnables in LangChain

## 📖 Overview

This guide provides a deep dive into **Runnables**, a highly technical but crucial concept in the LangChain framework (covering v0.1, v0.2, and v0.3).

The guide explains the evolution of LangChain, why the original "Chain" architecture became problematic, and how Runnables solve the issue of standardization to simplify the development of LLM-based applications.

> **Key Takeaway:** Chains work behind the scenes *because* they are built using Runnables. Understanding Runnables is essential to effectively use the modern LangChain library.

---

## 📑 Table of Contents

1. [Historical Context: The Rise of LLM Apps](https://www.google.com/search?q=%23-1-historical-context-the-rise-of-llm-apps)
2. [The Component Era](https://www.google.com/search?q=%23-2-the-component-era)
3. [The "Chain" Era & The Problem](https://www.google.com/search?q=%23-3-the-chain-era--the-problem)
4. [The Root Cause: Non-Standardization](https://www.google.com/search?q=%23-4-the-root-cause-non-standardization)
5. [The Solution: Runnables](https://www.google.com/search?q=%23-5-the-solution-runnables)
6. [The Standard Interface](https://www.google.com/search?q=%23-6-the-standard-interface)
7. [Code Demonstration: The "Old Way"](https://www.google.com/search?q=%23-7-code-demonstration-the-old-way)

---

## 🗓️ 1. Historical Context: The Rise of LLM Apps

To understand why Runnables exist, we must look at the timeline starting in **November 2022**.

* **The Catalyst:** ChatGPT was released, and OpenAI opened its APIs to the public.
* **The Prediction:** The LangChain team realized there would be a massive demand for applications that could understand human text (Chatbots, PDF Readers, AI Agents).
* **Phase 1: API Abstraction**
* **The Issue:** Companies like Google, Anthropic, and Mistral began building their own LLMs, each with a completely different API structure.
* **The Solution:** LangChain created a framework to abstraction these differences. It allowed developers to swap LLM providers with minimal code changes, fueling LangChain's initial popularity.



---

## 🧩 2. The Component Era

LangChain quickly realized that interacting with an LLM was only a small part of building a real application. A complete pipeline (e.g., a PDF Reader) requires many steps:

1. **Loading** the PDF.
2. **Splitting** the text into chunks.
3. **Generating Embeddings** for those chunks.
4. **Storing** them in a Vector Database.
5. **Retrieving** relevant chunks (Semantic Search).
6. **Sending** context to the LLM.
7. **Parsing** the response.

To solve this, LangChain introduced specialized **Components**:

* **Document Loaders** & **Text Splitters**
* **Embedding Models** & **Vector Stores**
* **Retrievers** & **Output Parsers**
* **Memory**

**Impact:** Complex applications (like RAG pipelines) could now be built in very few lines of code (e.g., ~36 lines).

---

## 🔗 3. The "Chain" Era & The Problem

### The "Eureka" Moment

Developers were repeating the same patterns—such as always formatting a prompt before sending it to an LLM. To automate this, LangChain introduced **Chains**.

* **LLMChain:** Automatically connects a `PromptTemplate` to an `LLM`.
* **RetrievalQAChain:** Encapsulates the entire RAG logic (Retrieval + Prompting + LLM), reducing code further (e.g., to 32 lines).

### The Proliferation Problem

LangChain began creating a specific chain for every conceivable use case:

* *Math Chain, SQL Database Chain, API Chain, Sequential Chain, etc.*

### The Consequences (Technical Debt)

While intended to help, this approach backfired:

1. **Bloat:** The codebase became massive and a nightmare to maintain.
2. **Confusion:** The documentation became overwhelming.
3. **Steep Learning Curve:** New engineers struggled to know *which* specific chain to use for their task.
4. **Irony:** A tool meant to simplify development inadvertently made it harder due to rigidity.

---

## 🔍 4. The Root Cause: Non-Standardization

The fundamental issue was that the original components were **not standardized**. They were developed independently and used different method names ("languages"):

| Component | Method Name used |
| --- | --- |
| **LLM** | `.predict()` |
| **PromptTemplate** | `.format()` |
| **Retriever** | `.get_relevant_documents()` |
| **Parser** | `.parse()` |

**The Friction:** Because components didn't share a common interface, they couldn't automatically "talk" to each other. LangChain had to write manual "glue code" (Chains) just to connect them.

---

## ✅ 5. The Solution: Runnables

LangChain rebuilt their ecosystem around the concept of **Runnables** to fix the standardization issue.

### Definition of a Runnable

A Runnable is a **Unit of Work** that follows a strict protocol. It transforms the library into a set of "Lego Blocks."

### The Lego Analogy

* **Unit of Work:** Each Lego block has a specific purpose.
* **Common Interface:** All Lego blocks share the same studs and tubes. This allows them to connect regardless of their shape or internal function.
* **Connectability:** The output of one Runnable automatically becomes the input of the next.
* **Composability (Nesting):** A structure made of connected Lego blocks can *itself* be treated as a larger Lego block. Similarly, a Chain of Runnables is itself a Runnable, allowing for **infinite nesting**.

---

## ⚙️ 6. The Standard Interface

All Runnables must implement the following core methods. This guarantees seamless interaction:

* **`invoke(input)`**: The standard call. Takes a single input and returns a single output.
* **`batch([inputs])`**: Processes a list of inputs simultaneously (parallel processing).
* **`stream(input)`**: Streams the output chunks back to the user (essential for reducing perceived latency in LLMs).

---

## 💻 7. Code Demonstration: The "Old Way"

*This conceptual demo illustrates the **problem** Runnables solve. It simulates the old, non-standardized system where manual glue code was required.*

### The Dummy LLM (`NakliLLM`)

Uses the non-standard `.predict()` method.

```python
import random

class NakliLLM:
    def __init__(self):
        print("LLM Created")
    
    # Non-standard method name
    def predict(self, prompt):
        replies = ["That is interesting", "I don't know", "LangChain is cool"]
        return random.choice(replies)

```

### The Dummy Prompt (`NakliPromptTemplate`)

Uses the non-standard `.format()` method.

```python
class NakliPromptTemplate:
    def __init__(self, template, input_variables):
        self.template = template
        self.variables = input_variables
    
    # Non-standard method name
    def format(self, input_dict):
        return self.template.format(**input_dict)

```

### The Takeaway

In this "Old Way," you cannot simply pipe `NakliPromptTemplate` into `NakliLLM` because `.format()` and `.predict()` are different commands. You would need to write a wrapper function to handle the data hand-off.

**Runnables remove this need by forcing every component to use `.invoke()`.**