# String iterable
##  StringIterableReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/string_iterable/#llama_index.readers.string_iterable.StringIterableReader "Permanent link")
Bases: 
String Iterable Reader.
Gets a list of documents, given an iterable (e.g. list) of strings.
Example
.. code-block:: python

```
from llama_index import TreeIndex
from llama_index.readers import StringIterableReader

documents = StringIterableReader().load_data(
    texts=["I went to the store", "I bought an apple"]
)
index = TreeIndex.from_documents(documents)
query_engine = index.as_query_engine()
query_engine.query("what did I buy?")

# response should be something like "You bought an apple."

```
Source code in `llama-index-integrations/readers/llama-index-readers-string-iterable/llama_index/readers/string_iterable/base.py`  
| 
```
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
```
 | 
```
classStringIterableReader(BasePydanticReader):
"""
    String Iterable Reader.

    Gets a list of documents, given an iterable (e.g. list) of strings.

    Example:
        .. code-block:: python

            from llama_index import TreeIndex
            from llama_index.readers import StringIterableReader

            documents = StringIterableReader().load_data(
                texts=["I went to the store", "I bought an apple"]

            index = TreeIndex.from_documents(documents)
            query_engine = index.as_query_engine()
            query_engine.query("what did I buy?")

            # response should be something like "You bought an apple."

    """

    is_remote: bool = False

    @classmethod
    defclass_name(cls) -> str:
        return "StringIterableReader"

    defload_data(self, texts: List[str]) -> List[Document]:
"""Load the data."""
        results = []
        for text in texts:
            results.append(Document(text=text))

        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/string_iterable/#llama_index.readers.string_iterable.StringIterableReader.load_data "Permanent link")

```
load_data(texts: []) -> []

```

Load the data.
Source code in `llama-index-integrations/readers/llama-index-readers-string-iterable/llama_index/readers/string_iterable/base.py`  
| 
```
38
39
40
41
42
43
44
```
 | 
```
defload_data(self, texts: List[str]) -> List[Document]:
"""Load the data."""
    results = []
    for text in texts:
        results.append(Document(text=text))

    return results

```
 |  
| --- | --- |  
options: members: - StringIterableReader
