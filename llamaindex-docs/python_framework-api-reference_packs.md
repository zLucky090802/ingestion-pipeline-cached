# Index
Init file.
##  BaseLlamaPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/#llama_index.core.llama_pack.BaseLlamaPack "Permanent link")
Source code in `llama-index-core/llama_index/core/llama_pack/base.py`  
| 
```
 7
 8
 9
10
11
12
13
14
```
 | 
```
classBaseLlamaPack:
    @abstractmethod
    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""

    @abstractmethod
    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run."""

```
 |  
| --- | --- |  
###  get_modules `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/#llama_index.core.llama_pack.BaseLlamaPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-core/llama_index/core/llama_pack/base.py`  
| 
```
@abstractmethod
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""

```
 |  
| --- |  
###  run `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/#llama_index.core.llama_pack.BaseLlamaPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run.
Source code in `llama-index-core/llama_index/core/llama_pack/base.py`  
| 
```
12
13
14
```
 | 
```
@abstractmethod
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run."""

```
 |  
| --- | --- |  
##  download_llama_pack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/#llama_index.core.llama_pack.download_llama_pack "Permanent link")

```
download_llama_pack(
    llama_pack_class: ,
    download_dir: Optional[] = None,
    llama_pack_url:  = LLAMA_PACKS_CONTENTS_URL,
    refresh_cache:  = True,
) -> Optional[[]]

```

Download a single LlamaPack PyPi Package.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llama_pack_class`  |  The name of the LlamaPack class you want to download, such as `GmailOpenAIAgentPack`.  |  _required_  |  
|  `refresh_cache`  |  `bool`  |  If true, the local cache will be skipped and the loader will be fetched directly from the remote repo.  |  `True`  |  
|  `download_dir`  |  `Optional[str]`  |  Custom dirpath to download the pack into.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[Type[BaseLlamaPack[](https://developers.llamaindex.ai/python/framework-api-reference/packs/#llama_index.core.llama_pack.BaseLlamaPack "BaseLlamaPack \(llama_index.core.llama_pack.base.BaseLlamaPack\)")]]`  |  A Loader.  |  
Source code in `llama-index-core/llama_index/core/llama_pack/download.py`  
| 
```
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
66
67
68
69
70
71
72
73
74
```
 | 
```
defdownload_llama_pack(
    llama_pack_class: str,
    download_dir: Optional[str] = None,
    llama_pack_url: str = LLAMA_PACKS_CONTENTS_URL,
    refresh_cache: bool = True,
) -> Optional[Type[BaseLlamaPack]]:
"""
    Download a single LlamaPack PyPi Package.

    Args:
        llama_pack_class: The name of the LlamaPack class you want to download,
            such as `GmailOpenAIAgentPack`.
        refresh_cache: If true, the local cache will be skipped and the
            loader will be fetched directly from the remote repo.
        download_dir: Custom dirpath to download the pack into.

    Returns:
        A Loader.

    """
    pack_cls = None

    mappings_path = os.path.join(
        os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
        ),
        "command_line/mappings.json",
    )
    with open(mappings_path) as f:
        mappings = json.load(f)

    if llama_pack_class in mappings:
        new_import_parent = mappings[llama_pack_class]
        new_install_parent = new_import_parent.replace(".", "-").replace("_", "-")
    else:
        raise ValueError(f"Failed to find python package for class {llama_pack_class}")

    if not download_dir:
        pack_cls = download_integration(
            module_str=new_install_parent,
            module_import_str=new_import_parent,
            cls_name=llama_pack_class,
        )
    else:
        pack_cls = download_llama_pack_template(
            new_install_parent=new_install_parent,
            llama_pack_class=llama_pack_class,
            llama_pack_url=llama_pack_url,
            refresh_cache=refresh_cache,
            custom_path=download_dir,
        )
        track_download(llama_pack_class, "llamapack")
        if pack_cls is None:
            return None

        if not issubclass(pack_cls, BaseLlamaPack):
            raise ValueError(
                f"Pack class {pack_cls} must be a subclass of BaseLlamaPack."
            )

    return pack_cls

```
 |  
| --- | --- |
