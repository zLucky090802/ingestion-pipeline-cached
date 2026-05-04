[Skip to content](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#_top)
LlamaIndex Framework
Component Guides
Loading
Node Parsers
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Node Parser Modules
## File-Based Node Parsers
[Section titled “File-Based Node Parsers”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#file-based-node-parsers)
There are several file-based node parsers, that will create nodes based on the type of content that is being parsed (JSON, Markdown, etc.)
The simplest flow is to combine the `FlatFileReader` with the `SimpleFileNodeParser` to automatically use the best node parser for each type of content. Then, you may want to chain the file-based node parser with a text-based node parser to account for the actual length of the text.
### SimpleFileNodeParser
[Section titled “SimpleFileNodeParser”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#simplefilenodeparser)

```


from llama_index.core.node_parser import SimpleFileNodeParser




from llama_index.readers.file import FlatReader




from pathlib import Path





md_docs = FlatReader().load_data(Path("./test.md"))





parser = SimpleFileNodeParser()




md_nodes = parser.get_nodes_from_documents(md_docs)


```

### HTMLNodeParser
[Section titled “HTMLNodeParser”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#htmlnodeparser)
This node parser uses `beautifulsoup` to parse raw HTML.
By default, it will parse a select subset of HTML tags, but you can override this.
The default tags are: `["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "b", "i", "u", "section"]`

```


from llama_index.core.node_parser import HTMLNodeParser





parser = HTMLNodeParser(tags=["p", "h1"])  # optional list of tags




nodes = parser.get_nodes_from_documents(html_docs)


```

### JSONNodeParser
[Section titled “JSONNodeParser”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#jsonnodeparser)
The `JSONNodeParser` parses raw JSON.

```


from llama_index.core.node_parser import JSONNodeParser





parser = JSONNodeParser()





nodes = parser.get_nodes_from_documents(json_docs)


```

### MarkdownNodeParser
[Section titled “MarkdownNodeParser”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#markdownnodeparser)
The `MarkdownNodeParser` parses raw markdown text.

```


from llama_index.core.node_parser import MarkdownNodeParser





parser = MarkdownNodeParser()





nodes = parser.get_nodes_from_documents(markdown_docs)


```

## Text-Splitters
[Section titled “Text-Splitters”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#text-splitters)
### CodeSplitter
[Section titled “CodeSplitter”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#codesplitter)
Splits raw code-text based on the language it is written in.
Check the full list of [supported languages here](https://github.com/grantjenks/py-tree-sitter-languages#license).

```


from llama_index.core.node_parser import CodeSplitter





splitter = CodeSplitter(




language="python",




chunk_lines=40# lines per chunk




chunk_lines_overlap=15# lines overlap between chunks




max_chars=1500# max chars per chunk





nodes = splitter.get_nodes_from_documents(documents)


```

### LangchainNodeParser
[Section titled “LangchainNodeParser”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#langchainnodeparser)
You can also wrap any existing text splitter from langchain with a node parser.

```


from langchain.text_splitter import RecursiveCharacterTextSplitter




from llama_index.core.node_parser import LangchainNodeParser





parser = LangchainNodeParser(RecursiveCharacterTextSplitter())




nodes = parser.get_nodes_from_documents(documents)


```

### Chunker
[Section titled “Chunker”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#chunker)
The `Chunker` is a multi purpose node parser that wraps around the [chonkie](https://docs.chonkie.ai/) chunkers. you can initialize your parser using an alias for any of the supported chonkie chunking strategies, the full list of valid aliases can be accessed via `Chunker.valid_chunker_types` attribute.

```


from llama_index.node_parser.chonkie import Chunker





parser = Chunker("recursive", chunk_size=2048)




nodes = parser.get_nodes_from_documents(documents)


```

you can also directly pass in a chonkie chunker instance to initialize the parser.

```


from chonkie import RecursiveChunker




from llama_index.node_parser.chonkie import Chunker





chonkie_chunker = RecursiveChunker()




parser = Chunker(chonkie_chunker)




nodes = parser.get_nodes_from_documents(documents)


```

### SentenceSplitter
[Section titled “SentenceSplitter”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#sentencesplitter)
The `SentenceSplitter` attempts to split text while respecting the boundaries of sentences.

```


from llama_index.core.node_parser import SentenceSplitter





splitter = SentenceSplitter(




chunk_size=1024,




chunk_overlap=20,





nodes = splitter.get_nodes_from_documents(documents)


```

### SentenceWindowNodeParser
[Section titled “SentenceWindowNodeParser”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#sentencewindownodeparser)
The `SentenceWindowNodeParser` is similar to other node parsers, except that it splits all documents into individual sentences. The resulting nodes also contain the surrounding “window” of sentences around each node in the metadata. Note that this metadata will not be visible to the LLM or embedding model.
This is most useful for generating embeddings that have a very specific scope. Then, combined with a `MetadataReplacementNodePostProcessor`, you can replace the sentence with it’s surrounding context before sending the node to the LLM.
An example of setting up the parser with default settings is below. In practice, you would usually only want to adjust the window size of sentences.

```


from llama_index.core.node_parser import SentenceWindowNodeParser





node_parser = SentenceWindowNodeParser.from_defaults(




# how many sentences on either side to capture




window_size=3,




# the metadata key that holds the window of surrounding sentences




window_metadata_key="window",




# the metadata key that holds the original sentence




original_text_metadata_key="original_sentence",



```

A full example can be found [here in combination with the `MetadataReplacementNodePostProcessor`](https://developers.llamaindex.ai/python/examples/node_postprocessor/metadatareplacementdemo).
### SemanticSplitterNodeParser
[Section titled “SemanticSplitterNodeParser”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#semanticsplitternodeparser)
“Semantic chunking” is a new concept proposed Greg Kamradt in his video tutorial on 5 levels of embedding chunking: <https://youtu.be/8OJC21T2SL4?t=1933>.
Instead of chunking text with a **fixed** chunk size, the semantic splitter adaptively picks the breakpoint in-between sentences using embedding similarity. This ensures that a “chunk” contains sentences that are semantically related to each other.
We adapted it into a LlamaIndex module.
Check out our notebook below!
Caveats:
  * The regex primarily works for English sentences
  * You may have to tune the breakpoint percentile threshold.



```


from llama_index.core.node_parser import SemanticSplitterNodeParser




from llama_index.embeddings.openai import OpenAIEmbedding





embed_model = OpenAIEmbedding()




splitter = SemanticSplitterNodeParser(




buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model



```

A full example can be found in our [guide on using the `SemanticSplitterNodeParser`](https://developers.llamaindex.ai/python/examples/node_parsers/semantic_chunking).
### TokenTextSplitter
[Section titled “TokenTextSplitter”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#tokentextsplitter)
The `TokenTextSplitter` attempts to split to a consistent chunk size according to raw token counts.

```


from llama_index.core.node_parser import TokenTextSplitter





splitter = TokenTextSplitter(




chunk_size=1024,




chunk_overlap=20,




separator=" ",





nodes = splitter.get_nodes_from_documents(documents)


```

## Relation-Based Node Parsers
[Section titled “Relation-Based Node Parsers”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#relation-based-node-parsers)
### HierarchicalNodeParser
[Section titled “HierarchicalNodeParser”](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#hierarchicalnodeparser)
This node parser will chunk nodes into hierarchical nodes. This means a single input will be chunked into several hierarchies of chunk sizes, with each node containing a reference to it’s parent node.
When combined with the `AutoMergingRetriever`, this enables us to automatically replace retrieved nodes with their parents when a majority of children are retrieved. This process provides the LLM with more complete context for response synthesis.

```


from llama_index.core.node_parser import HierarchicalNodeParser





node_parser = HierarchicalNodeParser.from_defaults(




chunk_sizes=[2048, 512, 128]



```

A full example can be found [here in combination with the `AutoMergingRetriever`](https://developers.llamaindex.ai/python/examples/retrievers/auto_merging_retriever).
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


