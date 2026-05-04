# Preprocess
##  PreprocessReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/preprocess/#llama_index.readers.preprocess.PreprocessReader "Permanent link")
Bases: 
Preprocess reader.
This reader has been discontinued. The Preprocess service is no longer available and the `pypreprocess` package is no longer maintained. Please remove this dependency from your projects.
Source code in `llama-index-integrations/readers/llama-index-readers-preprocess/llama_index/readers/preprocess/base.py`  
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
```
 | 
```
classPreprocessReader(BaseReader):
"""
    Preprocess reader.

    This reader has been discontinued. The Preprocess service is no longer
    available and the ``pypreprocess`` package is no longer maintained.
    Please remove this dependency from your projects.
    """

    def__init__(self, *args, **kwargs):
        raise RuntimeError(
            "The Preprocess service has been discontinued and is permanently"
            " unavailable. Please remove llama-index-readers-preprocess from"
            " your dependencies."
        )

    defload_data(self, **kwargs) -> List[Document]:
        raise RuntimeError(
            "The Preprocess service has been discontinued and is permanently"
            " unavailable."
        )

```
 |  
| --- | --- |  
options: members: - PreprocessReader
