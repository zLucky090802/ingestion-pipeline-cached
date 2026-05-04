# Macrometa gdn
##  MacrometaGDNReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/macrometa_gdn/#llama_index.readers.macrometa_gdn.MacrometaGDNReader "Permanent link")
Bases: 
Macrometa GDN Reader.
Reads vectors from Macrometa GDN
Source code in `llama-index-integrations/readers/llama-index-readers-macrometa-gdn/llama_index/readers/macrometa_gdn/base.py`  
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
75
76
77
78
79
80
81
82
83
84
85
86
87
```
 | 
```
classMacrometaGDNReader(BaseReader):
"""
    Macrometa GDN Reader.

    Reads vectors from Macrometa GDN


    """

    def__init__(self, url: str, apikey: str):
        self.url = url
        self.apikey = apikey

    defload_data(self, collection_list: List[str]) -> List[Document]:
"""
        Loads data from the input directory.

        Args:
            api: Macrometa GDN API key
            collection_name: Name of the collection to read from

        """
        if collection_list is None:
            raise ValueError("Must specify collection name(s)")

        results = []
        for collection_name in collection_list:
            collection = self._load_collection(collection_name)
            results.append(
                Document(
                    text=collection, extra_info={"collection_name": collection_name}
                )
            )
        return results

    def_load_collection(self, collection_name: str) -> str:
        all_documents = []
"""Loads a collection from the database.

        Args:
            collection_name: Name of the collection to read from

        """
        url = self.url + "/_fabric/_system/_api/cursor"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "apikey " + self.apikey,
        }

        data = {
            "batchSize": 1000,
            "ttl": 60,
            "query": "FOR doc IN " + collection_name + " RETURN doc",
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_json = response.json()
        if response.status_code == 201:
            all_documents.extend(response_json.get("result", []))

            while response_json.get("hasMore"):
                cursor_id = response_json.get("id")

                next_url = self.url + "/_fabric/_system/_api/cursor/" + cursor_id

                response = requests.put(next_url, headers=headers)

                if response.status_code == 200:
                    response_json = response.json()
                    all_documents.extend(response_json.get("result", []))
                else:
                    print(f"Request failed with status code {response.status_code}")
                    break
        else:
            print(f"Initial request failed with status code {response.status_code}")

        return str(all_documents)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/macrometa_gdn/#llama_index.readers.macrometa_gdn.MacrometaGDNReader.load_data "Permanent link")

```
load_data(collection_list: []) -> []

```

Loads data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api`  |  Macrometa GDN API key  |  _required_  |  
|  `collection_name`  |  Name of the collection to read from  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-macrometa-gdn/llama_index/readers/macrometa_gdn/base.py`  
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
```
 | 
```
defload_data(self, collection_list: List[str]) -> List[Document]:
"""
    Loads data from the input directory.

    Args:
        api: Macrometa GDN API key
        collection_name: Name of the collection to read from

    """
    if collection_list is None:
        raise ValueError("Must specify collection name(s)")

    results = []
    for collection_name in collection_list:
        collection = self._load_collection(collection_name)
        results.append(
            Document(
                text=collection, extra_info={"collection_name": collection_name}
            )
        )
    return results

```
 |  
| --- | --- |  
options: members: - MacrometaGDNReader
