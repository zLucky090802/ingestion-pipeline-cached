[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#_top)
LlamaIndex Framework
Component Guides
Loading
Documents And Nodes
[Defining and Customizing Documents](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Defining and Customizing Documents
## Defining Documents
[Section titled “Defining Documents”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#defining-documents)
Documents can either be created automatically via data loaders, or constructed manually.
By default, all of our [data loaders](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector) (including those offered on LlamaHub) return `Document` objects through the `load_data` function.

```


from llama_index.core import SimpleDirectoryReader





documents = SimpleDirectoryReader("./data").load_data()


```

You can also choose to construct documents manually. LlamaIndex exposes the `Document` struct.

```


from llama_index.core import Document





text_list = [text1, text2, ...]




documents = [Document(text=t) forin text_list]


```

To speed up prototyping and development, you can also quickly create a document using some default text:

```


document = Document.example()


```

## Customizing Documents
[Section titled “Customizing Documents”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#customizing-documents)
This section covers various ways to customize `Document` objects. Since the `Document` object is a subclass of our `TextNode` object, all these settings and details apply to the `TextNode` object class as well.
### Metadata
[Section titled “Metadata”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#metadata)
Documents also offer the chance to include useful metadata. Using the `metadata` dictionary on each document, additional information can be included to help inform responses and track down sources for query responses. This information can be anything, such as filenames or categories. If you are integrating with a vector database, keep in mind that some vector databases require that the keys must be strings, and the values must be flat (either `str`, `float`, or `int`).
Any information set in the `metadata` dictionary of each document will show up in the `metadata` of each source node created from the document. Additionally, this information is included in the nodes, enabling the index to utilize it on queries and responses. By default, the metadata is injected into the text for both embedding and LLM model calls.
There are a few ways to set up this dictionary:
  1. In the document constructor:



```


document = Document(




text="text",




metadata={"filename": "<doc_file_name>", "category": "<category>"},



```

  1. After the document is created:



```


document.metadata = {"filename": "<doc_file_name>"}


```

  1. Set the filename automatically using the `SimpleDirectoryReader` and `file_metadata` hook. This will automatically run the hook on each document to set the `metadata` field:



```


from llama_index.core import SimpleDirectoryReader





filename_fn =lambda filename: {"file_name": filename}




# automatically sets the metadata of each document according to filename_fn



documents = SimpleDirectoryReader(




"./data", file_metadata=filename_fn



).load_data()

```

### Customizing the id
[Section titled “Customizing the id”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#customizing-the-id)
As detailed in the section [Document Management](https://developers.llamaindex.ai/python/framework/module_guides/indexing/document_management), the `doc_id` is used to enable efficient refreshing of documents in the index. When using the `SimpleDirectoryReader`, you can automatically set the doc `doc_id` to be the full path to each document:

```


from llama_index.core import SimpleDirectoryReader





documents = SimpleDirectoryReader("./data", filename_as_id=True).load_data()




print([x.doc_id forin documents])


```

You can also set the `doc_id` of any `Document` directly!

```


document.doc_id ="My new document id!"


```

Note: the ID can also be set through the `node_id` or `id_` property on a Document object, similar to a `TextNode` object.
### Advanced - Metadata Customization
[Section titled “Advanced - Metadata Customization”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#advanced---metadata-customization)
A key detail mentioned above is that by default, any metadata you set is included in the embeddings generation and LLM.
#### Customizing LLM Metadata Text
[Section titled “Customizing LLM Metadata Text”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#customizing-llm-metadata-text)
Typically, a document might have many metadata keys, but you might not want all of them visible to the LLM during response synthesis. In the above examples, we may not want the LLM to read the `file_name` of our document. However, the `file_name` might include information that will help generate better embeddings. A key advantage of doing this is to bias the embeddings for retrieval without changing what the LLM ends up reading.
We can exclude it like so:

```


document.excluded_llm_metadata_keys = ["file_name"]


```

Then, we can test what the LLM will actually end up reading using the `get_content()` function and specifying `MetadataMode.LLM`:

```


from llama_index.core.schema import MetadataMode





print(document.get_content(metadata_mode=MetadataMode.LLM))


```

#### Customizing Embedding Metadata Text
[Section titled “Customizing Embedding Metadata Text”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#customizing-embedding-metadata-text)
Similar to customizing the metadata visible to the LLM, we can also customize the metadata visible to embeddings. In this case, you can specifically exclude metadata visible to the embedding model, in case you DON’T want particular text to bias the embeddings.

```


document.excluded_embed_metadata_keys = ["file_name"]


```

Then, we can test what the embedding model will actually end up reading using the `get_content()` function and specifying `MetadataMode.EMBED`:

```


from llama_index.core.schema import MetadataMode





print(document.get_content(metadata_mode=MetadataMode.EMBED))


```

#### Customizing Metadata Format
[Section titled “Customizing Metadata Format”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#customizing-metadata-format)
As you know by now, metadata is injected into the actual text of each document/node when sent to the LLM or embedding model. By default, the format of this metadata is controlled by three attributes:
  1. `Document.metadata_seperator` -> default = `"\n"`


When concatenating all key/value fields of your metadata, this field controls the separator between each key/value pair.
  1. `Document.metadata_template` -> default = `"{key}: {value}"`


This attribute controls how each key/value pair in your metadata is formatted. The two variables `key` and `value` string keys are required.
  1. `Document.text_template` -> default = `{metadata_str}\n\n{content}`


Once your metadata is converted into a string using `metadata_seperator` and `metadata_template`, this templates controls what that metadata looks like when joined with the text content of your document/node. The `metadata` and `content` string keys are required.
### Summary
[Section titled “Summary”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#summary)
Knowing all this, let’s create a short example using all this power:

```


from llama_index.core import Document




from llama_index.core.schema import MetadataMode





document = Document(




text="This is a super-customized document",




metadata={




"file_name": "super_secret_document.txt",




"category": "finance",




"author": "LlamaIndex",





excluded_llm_metadata_keys=["file_name"],




metadata_seperator="::",




metadata_template="{key}=>{value}",




text_template="Metadata: {metadata_str}\n-----\nContent: {content}",






print(




"The LLM sees this: \n",




document.get_content(metadata_mode=MetadataMode.LLM),





print(




"The Embedding model sees this: \n",




document.get_content(metadata_mode=MetadataMode.EMBED),



```

### Advanced - Automatic Metadata Extraction
[Section titled “Advanced - Automatic Metadata Extraction”](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/#advanced---automatic-metadata-extraction)
We have [initial examples](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor) of using LLMs themselves to perform metadata extraction.
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


