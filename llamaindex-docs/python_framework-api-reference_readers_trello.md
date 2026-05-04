# Trello
##  TrelloReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/trello/#llama_index.readers.trello.TrelloReader "Permanent link")
Bases: 
Trello reader. Reads data from Trello boards and cards.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  Trello API key.  |  _required_  |  
|  `api_token`  |  Trello API token.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-trello/llama_index/readers/trello/base.py`  
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
```
 | 
```
classTrelloReader(BaseReader):
"""
    Trello reader. Reads data from Trello boards and cards.

    Args:
        api_key (str): Trello API key.
        api_token (str): Trello API token.

    """

    def__init__(self, api_key: str, api_token: str) -> None:
"""Initialize Trello reader."""
        self.api_key = api_key
        self.api_token = api_token

    defload_data(self, board_id: str) -> List[Document]:
"""
        Load data from a Trello board.

        Args:
            board_id (str): Trello board ID.


        Returns:
            List[Document]: List of documents representing Trello cards.

        """
        fromtrelloimport TrelloClient

        client = TrelloClient(api_key=self.api_key, token=self.api_token)
        board = client.get_board(board_id)
        cards = board.get_cards()

        documents = []
        for card in cards:
            document = Document(
                doc_id=card.name,
                text=card.description,
                extra_info={
                    "id": card.id,
                    "url": card.url,
                    "due_date": card.due_date,
                    "labels": [label.name for label in card.labels],
                },
            )
            documents.append(document)

        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/trello/#llama_index.readers.trello.TrelloReader.load_data "Permanent link")

```
load_data(board_id: ) -> []

```

Load data from a Trello board.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `board_id`  |  Trello board ID.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents representing Trello cards.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-trello/llama_index/readers/trello/base.py`  
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
```
 | 
```
defload_data(self, board_id: str) -> List[Document]:
"""
    Load data from a Trello board.

    Args:
        board_id (str): Trello board ID.


    Returns:
        List[Document]: List of documents representing Trello cards.

    """
    fromtrelloimport TrelloClient

    client = TrelloClient(api_key=self.api_key, token=self.api_token)
    board = client.get_board(board_id)
    cards = board.get_cards()

    documents = []
    for card in cards:
        document = Document(
            doc_id=card.name,
            text=card.description,
            extra_info={
                "id": card.id,
                "url": card.url,
                "due_date": card.due_date,
                "labels": [label.name for label in card.labels],
            },
        )
        documents.append(document)

    return documents

```
 |  
| --- | --- |  
options: members: - TrelloReader
