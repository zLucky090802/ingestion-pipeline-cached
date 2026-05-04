# Make com
##  MakeWrapper [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/make_com/#llama_index.readers.make_com.MakeWrapper "Permanent link")
Bases: 
Make reader.
Source code in `llama-index-integrations/readers/llama-index-readers-make-com/llama_index/readers/make_com/base.py`  
| 
```
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
```
 | 
```
classMakeWrapper(BaseReader):
"""Make reader."""

    defload_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
"""
        Load data from the input directory.

        NOTE: This is not implemented.

        """
        raise NotImplementedError("Cannot load documents from Make.com API.")

    defpass_response_to_webhook(
        self, webhook_url: str, response: Response, query: Optional[str] = None
    ) -> None:
"""
        Pass response object to webhook.

        Args:
            webhook_url (str): Webhook URL.
            response (Response): Response object.
            query (Optional[str]): Query. Defaults to None.

        """
        response_text = response.response
        source_nodes = [n.dict() for n in response.source_nodes]
        json_dict = {
            "response": response_text,
            "source_nodes": source_nodes,
            "query": query,
        }
        r = requests.post(webhook_url, json=json_dict)
        r.raise_for_status()

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/make_com/#llama_index.readers.make_com.MakeWrapper.load_data "Permanent link")

```
load_data(*args: , **load_kwargs: ) -> []

```

Load data from the input directory.
NOTE: This is not implemented.
Source code in `llama-index-integrations/readers/llama-index-readers-make-com/llama_index/readers/make_com/base.py`  
| 
```
19
20
21
22
23
24
25
26
```
 | 
```
defload_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
"""
    Load data from the input directory.

    NOTE: This is not implemented.

    """
    raise NotImplementedError("Cannot load documents from Make.com API.")

```
 |  
| --- | --- |  
###  pass_response_to_webhook [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/make_com/#llama_index.readers.make_com.MakeWrapper.pass_response_to_webhook "Permanent link")

```
pass_response_to_webhook(
    webhook_url: ,
    response: ,
    query: Optional[] = None,
) -> None

```

Pass response object to webhook.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `webhook_url`  |  Webhook URL.  |  _required_  |  
|  `response`  |   |  Response object.  |  _required_  |  
|  `query`  |  `Optional[str]`  |  Query. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-make-com/llama_index/readers/make_com/base.py`  
| 
```
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
```
 | 
```
defpass_response_to_webhook(
    self, webhook_url: str, response: Response, query: Optional[str] = None
) -> None:
"""
    Pass response object to webhook.

    Args:
        webhook_url (str): Webhook URL.
        response (Response): Response object.
        query (Optional[str]): Query. Defaults to None.

    """
    response_text = response.response
    source_nodes = [n.dict() for n in response.source_nodes]
    json_dict = {
        "response": response_text,
        "source_nodes": source_nodes,
        "query": query,
    }
    r = requests.post(webhook_url, json=json_dict)
    r.raise_for_status()

```
 |  
| --- | --- |  
options: members: - MakeWrapper
