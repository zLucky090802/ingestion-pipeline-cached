# Whatsapp
##  WhatsappChatLoader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/whatsapp/#llama_index.readers.whatsapp.WhatsappChatLoader "Permanent link")
Bases: 
Whatsapp chat data loader.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `path`  |  Path to Whatsapp chat file.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-whatsapp/llama_index/readers/whatsapp/base.py`  
| 
```
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
```
 | 
```
classWhatsappChatLoader(BaseReader):
"""
    Whatsapp chat data loader.

    Args:
        path (str): Path to Whatsapp chat file.

    """

    def__init__(self, path: str):
"""Initialize with path."""
        self.file_path = path

    defload_data(self) -> List[Document]:
"""
        Parse Whatsapp file into Documents.
        """
        fromchatminer.chatparsersimport WhatsAppParser

        path = Path(self.file_path)

        parser = WhatsAppParser(path)
        parser.parse_file()
        df = parser.parsed_messages.get_df(as_pandas=True)

        logging.debug(f"> Number of messages: {len(df)}.")

        docs = []
        n = 0
        # note that `itertuples` assumes a pandas dataframe
        for row in df.itertuples():
            extra_info = {
                "source": str(path).split("/")[-1].replace(".txt", ""),
                "author": row.author,
                "timestamp": str(row.timestamp),
            }

            docs.append(
                Document(
                    text=str(row.timestamp)
                    + " "
                    + row.author
                    + ":"
                    + " "
                    + row.message,
                    extra_info=extra_info,
                )
            )

            n += 1
            logging.debug(f"Added {n} of {len(df)} messages.")

        logging.debug(f"> Document creation for {path} is complete.")
        return docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/whatsapp/#llama_index.readers.whatsapp.WhatsappChatLoader.load_data "Permanent link")

```
load_data() -> []

```

Parse Whatsapp file into Documents.
Source code in `llama-index-integrations/readers/llama-index-readers-whatsapp/llama_index/readers/whatsapp/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""
    Parse Whatsapp file into Documents.
    """
    fromchatminer.chatparsersimport WhatsAppParser

    path = Path(self.file_path)

    parser = WhatsAppParser(path)
    parser.parse_file()
    df = parser.parsed_messages.get_df(as_pandas=True)

    logging.debug(f"> Number of messages: {len(df)}.")

    docs = []
    n = 0
    # note that `itertuples` assumes a pandas dataframe
    for row in df.itertuples():
        extra_info = {
            "source": str(path).split("/")[-1].replace(".txt", ""),
            "author": row.author,
            "timestamp": str(row.timestamp),
        }

        docs.append(
            Document(
                text=str(row.timestamp)
                + " "
                + row.author
                + ":"
                + " "
                + row.message,
                extra_info=extra_info,
            )
        )

        n += 1
        logging.debug(f"Added {n} of {len(df)} messages.")

    logging.debug(f"> Document creation for {path} is complete.")
    return docs

```
 |  
| --- | --- |  
options: members: - WhatsappChatLoader
