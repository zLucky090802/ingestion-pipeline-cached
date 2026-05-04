# Mondaydotcom
##  MondayReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mondaydotcom/#llama_index.readers.mondaydotcom.MondayReader "Permanent link")
Bases: 
monday.com reader. Reads board's data by a GraphQL query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  monday.com API key.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-mondaydotcom/llama_index/readers/mondaydotcom/base.py`  
| 
```
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
88
89
90
91
```
 | 
```
classMondayReader(BaseReader):
"""
    monday.com reader. Reads board's data by a GraphQL query.

    Args:
        api_key (str): monday.com API key.

    """

    def__init__(self, api_key: str) -> None:
"""Initialize monday.com reader."""
        self.api_key = api_key
        self.api_url = "https://api.monday.com/v2"

    def_parse_item_values(self, cv) -> Dict[str, str]:
        data = {}
        data["title"] = cv["title"]
        data["value"] = cv["text"]

        return data

    def_parse_data(self, item) -> Dict[str, str]:
        data = {}
        data["id"] = item["id"]
        data["name"] = item["name"]
        data["values"] = list(map(self._parse_item_values, list(item["column_values"])))

        return data

    def_perform_request(self, board_id) -> Dict[str, str]:
        headers = {"Authorization": self.api_key}
        query = """
            query{
                boards(ids: [%d]){
                    name,
                    items{

                        name,
                        column_values{
                            title,




            } """ % (board_id)
        data = {"query": query}

        response = requests.post(url=self.api_url, json=data, headers=headers)
        return response.json()

    defload_data(self, board_id: int) -> List[Document]:
"""
        Load board data by board_id.

        Args:
            board_id (int): monday.com board id.


        Returns:
            List[Document]: List of items as documents.
            [{id, name, values: [{title, value}]}]

        """
        json_response = self._perform_request(board_id)
        board_data = json_response["data"]["boards"][0]

        board_data["name"]
        items_array = list(board_data["items"])
        parsed_items = list(map(self._parse_data, list(items_array)))
        result = []
        for item in parsed_items:
            text = f"name: {item['name']}"
            for item_value in item["values"]:
                if item_value["value"]:
                    text += f", {item_value['title']}: {item_value['value']}"
            result.append(
                Document(
                    text=text, extra_info={"board_id": board_id, "item_id": item["id"]}
                )
            )

        return result

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/mondaydotcom/#llama_index.readers.mondaydotcom.MondayReader.load_data "Permanent link")

```
load_data(board_id: ) -> []

```

Load board data by board_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `board_id`  |  monday.com board id.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of items as documents.  |  
|   |  [{id, name, values: [{title, value}]}]  |  
Source code in `llama-index-integrations/readers/llama-index-readers-mondaydotcom/llama_index/readers/mondaydotcom/base.py`  
| 
```
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
88
89
90
91
```
 | 
```
defload_data(self, board_id: int) -> List[Document]:
"""
    Load board data by board_id.

    Args:
        board_id (int): monday.com board id.


    Returns:
        List[Document]: List of items as documents.
        [{id, name, values: [{title, value}]}]

    """
    json_response = self._perform_request(board_id)
    board_data = json_response["data"]["boards"][0]

    board_data["name"]
    items_array = list(board_data["items"])
    parsed_items = list(map(self._parse_data, list(items_array)))
    result = []
    for item in parsed_items:
        text = f"name: {item['name']}"
        for item_value in item["values"]:
            if item_value["value"]:
                text += f", {item_value['title']}: {item_value['value']}"
        result.append(
            Document(
                text=text, extra_info={"board_id": board_id, "item_id": item["id"]}
            )
        )

    return result

```
 |  
| --- | --- |  
options: members: - MondayReader
