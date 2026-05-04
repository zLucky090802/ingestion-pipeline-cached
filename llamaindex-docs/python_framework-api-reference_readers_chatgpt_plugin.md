# Chatgpt plugin
##  ChatGPTRetrievalPluginReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/chatgpt_plugin/#llama_index.readers.chatgpt_plugin.ChatGPTRetrievalPluginReader "Permanent link")
Bases: 
ChatGPT Retrieval Plugin reader.
Source code in `llama-index-integrations/readers/llama-index-readers-chatgpt-plugin/llama_index/readers/chatgpt_plugin/base.py`  
| 
```
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
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
```
 | 
```
classChatGPTRetrievalPluginReader(BaseReader):
"""ChatGPT Retrieval Plugin reader."""

    def__init__(
        self,
        endpoint_url: str,
        bearer_token: Optional[str] = None,
        retries: Optional[Retry] = None,
        batch_size: int = 100,
    ) -> None:
"""Chatgpt Retrieval Plugin."""
        self._endpoint_url = endpoint_url
        self._bearer_token = bearer_token or os.getenv("BEARER_TOKEN")
        self._retries = retries
        self._batch_size = batch_size

        self._s = requests.Session()
        self._s.mount("http://", HTTPAdapter(max_retries=self._retries))

    defload_data(
        self,
        query: str,
        top_k: int = 10,
        separate_documents: bool = True,
        **kwargs: Any,
    ) -> List[Document]:
"""Load data from ChatGPT Retrieval Plugin."""
        headers = {"Authorization": f"Bearer {self._bearer_token}"}
        queries = [{"query": query, "top_k": top_k}]
        res = requests.post(
            f"{self._endpoint_url}/query", headers=headers, json={"queries": queries}
        )
        documents: List[Document] = []
        for query_result in res.json()["results"]:
            for result in query_result["results"]:
                result_id = result["id"]
                result_txt = result["text"]
                result_embedding = result["embedding"]
                document = Document(
                    text=result_txt,
                    id_=result_id,
                    embedding=result_embedding,
                )
                documents.append(document)

            # NOTE: there should only be one query
            break

        if not separate_documents:
            text_list = [doc.get_content() for doc in documents]
            text = "\n\n".join(text_list)
            documents = [Document(text=text)]

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/chatgpt_plugin/#llama_index.readers.chatgpt_plugin.ChatGPTRetrievalPluginReader.load_data "Permanent link")

```
load_data(
    query: ,
    top_k:  = 10,
    separate_documents:  = True,
    **kwargs: 
) -> []

```

Load data from ChatGPT Retrieval Plugin.
Source code in `llama-index-integrations/readers/llama-index-readers-chatgpt-plugin/llama_index/readers/chatgpt_plugin/base.py`  
| 
```
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
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
```
 | 
```
defload_data(
    self,
    query: str,
    top_k: int = 10,
    separate_documents: bool = True,
    **kwargs: Any,
) -> List[Document]:
"""Load data from ChatGPT Retrieval Plugin."""
    headers = {"Authorization": f"Bearer {self._bearer_token}"}
    queries = [{"query": query, "top_k": top_k}]
    res = requests.post(
        f"{self._endpoint_url}/query", headers=headers, json={"queries": queries}
    )
    documents: List[Document] = []
    for query_result in res.json()["results"]:
        for result in query_result["results"]:
            result_id = result["id"]
            result_txt = result["text"]
            result_embedding = result["embedding"]
            document = Document(
                text=result_txt,
                id_=result_id,
                embedding=result_embedding,
            )
            documents.append(document)

        # NOTE: there should only be one query
        break

    if not separate_documents:
        text_list = [doc.get_content() for doc in documents]
        text = "\n\n".join(text_list)
        documents = [Document(text=text)]

    return documents

```
 |  
| --- | --- |  
options: members: - ChatGPTRetrievalPluginReader
