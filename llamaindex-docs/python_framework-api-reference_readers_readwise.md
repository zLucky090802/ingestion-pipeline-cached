# Readwise
Init file.
##  ReadwiseReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/readwise/#llama_index.readers.readwise.ReadwiseReader "Permanent link")
Bases: 
Reader for Readwise highlights.
Source code in `llama-index-integrations/readers/llama-index-readers-readwise/llama_index/readers/readwise/base.py`  
| 
```
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
```
 | 
```
classReadwiseReader(BaseReader):
"""
    Reader for Readwise highlights.
    """

    def__init__(self, api_key: str):
        self._api_key = api_key

    defload_data(
        self,
        updated_after: Optional[datetime.datetime] = None,
    ) -> List[Document]:
"""
        Load your Readwise.io highlights.

        Args:
            updated_after (datetime.datetime): The datetime to load highlights after. Useful for updating indexes over time.

        """
        readwise_response = _get_readwise_data(
            api_key=self._api_key, updated_after=updated_after
        )
        return [Document(text=json.dumps(d)) for d in readwise_response]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/readwise/#llama_index.readers.readwise.ReadwiseReader.load_data "Permanent link")

```
load_data(
    updated_after: Optional[datetime] = None,
) -> []

```

Load your Readwise.io highlights.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `updated_after`  |  `datetime`  |  The datetime to load highlights after. Useful for updating indexes over time.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-readwise/llama_index/readers/readwise/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    updated_after: Optional[datetime.datetime] = None,
) -> List[Document]:
"""
    Load your Readwise.io highlights.

    Args:
        updated_after (datetime.datetime): The datetime to load highlights after. Useful for updating indexes over time.

    """
    readwise_response = _get_readwise_data(
        api_key=self._api_key, updated_after=updated_after
    )
    return [Document(text=json.dumps(d)) for d in readwise_response]

```
 |  
| --- | --- |  
options: members: - ReadwiseReader
