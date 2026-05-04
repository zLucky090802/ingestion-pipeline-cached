# Dad jokes
Init file.
##  DadJokesReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dad_jokes/#llama_index.readers.dad_jokes.DadJokesReader "Permanent link")
Bases: 
Dad jokes reader.
Reads a random dad joke.
Source code in `llama-index-integrations/readers/llama-index-readers-dad-jokes/llama_index/readers/dad_jokes/base.py`  
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
```
 | 
```
classDadJokesReader(BaseReader):
"""
    Dad jokes reader.

    Reads a random dad joke.

    """

    def_get_random_dad_joke(self):
        response = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        json_data = response.json()
        return json_data["joke"]

    defload_data(self) -> List[Document]:
"""
        Return a random dad joke.

        Args:
            None.

        """
        return [Document(text=self._get_random_dad_joke())]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/dad_jokes/#llama_index.readers.dad_jokes.DadJokesReader.load_data "Permanent link")

```
load_data() -> []

```

Return a random dad joke.
Source code in `llama-index-integrations/readers/llama-index-readers-dad-jokes/llama_index/readers/dad_jokes/base.py`  
| 
```
26
27
28
29
30
31
32
33
34
```
 | 
```
defload_data(self) -> List[Document]:
"""
    Return a random dad joke.

    Args:
        None.

    """
    return [Document(text=self._get_random_dad_joke())]

```
 |  
| --- | --- |  
options: members: - DadJokesReader
