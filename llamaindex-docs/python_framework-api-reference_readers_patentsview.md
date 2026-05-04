# Patentsview
##  PatentsviewReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/patentsview/#llama_index.readers.patentsview.PatentsviewReader "Permanent link")
Bases: 
Patentsview reader.
Read patent abstract.
Source code in `llama-index-integrations/readers/llama-index-readers-patentsview/llama_index/readers/patentsview/base.py`  
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
```
 | 
```
classPatentsviewReader(BaseReader):
"""
    Patentsview reader.

    Read patent abstract.

    """

    def__init__(
        self,
        api_key: Optional[str] = None,
    ):
"""Initialize with request body."""
        self.json = {
            "q": {"patent_id": None},
            "f": ["patent_id", "patent_abstract"],
            "o": {"size": 1000},  # API's max return
        }

        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = os.getenv("PATENTSVIEW_API_KEY", None)
            if self.api_key is None:
                raise ValueError("The API key [PATENTSVIEW_API_KEY] is required.")

        self.headers = {"X-Api-Key": self.api_key}

    defload_data(self, patent_number: List[str]) -> List[Document]:
"""
        Load patent abstract given list of patent numbers.

        Args:
            patent_number: List[str]: List of patent numbers, e.g., 8848839.

        Returns:
            List[Document]: A list of Document objects, each including the abstract for a patent.

        """
        if not patent_number:
            raise ValueError("Please input patent number")

        if len(patent_number)  1000:
            raise ValueError(
                f"List patent number size is too large: {len(patent_number)} elements. Maximum allowed is 1000."
            )

        self.json["q"]["patent_id"] = patent_number

        response = requests.post(BASE_URL, json=self.json, headers=self.headers)
        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 60))
            logging.info(f"Throttled. Retrying in {wait}s...")
            time.sleep(wait)
            response = requests.post(BASE_URL, json=self.json, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            patents = data.get("patents", [])

            results = []
            for patent in patents:
                metadata = {"patent_id": patent["patent_id"]}
                results.append(
                    Document(text=patent["patent_abstract"], metadata=metadata)
                )

        else:
            raise Exception(f"Request failed with status code: {response.status_code}")

        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/patentsview/#llama_index.readers.patentsview.PatentsviewReader.load_data "Permanent link")

```
load_data(patent_number: []) -> []

```

Load patent abstract given list of patent numbers.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `patent_number`  |  `List[str]`  |  List[str]: List of patent numbers, e.g., 8848839.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects, each including the abstract for a patent.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-patentsview/llama_index/readers/patentsview/base.py`  
| 
```
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
```
 | 
```
defload_data(self, patent_number: List[str]) -> List[Document]:
"""
    Load patent abstract given list of patent numbers.

    Args:
        patent_number: List[str]: List of patent numbers, e.g., 8848839.

    Returns:
        List[Document]: A list of Document objects, each including the abstract for a patent.

    """
    if not patent_number:
        raise ValueError("Please input patent number")

    if len(patent_number)  1000:
        raise ValueError(
            f"List patent number size is too large: {len(patent_number)} elements. Maximum allowed is 1000."
        )

    self.json["q"]["patent_id"] = patent_number

    response = requests.post(BASE_URL, json=self.json, headers=self.headers)
    if response.status_code == 429:
        wait = int(response.headers.get("Retry-After", 60))
        logging.info(f"Throttled. Retrying in {wait}s...")
        time.sleep(wait)
        response = requests.post(BASE_URL, json=self.json, headers=self.headers)

    if response.status_code == 200:
        data = response.json()
        patents = data.get("patents", [])

        results = []
        for patent in patents:
            metadata = {"patent_id": patent["patent_id"]}
            results.append(
                Document(text=patent["patent_abstract"], metadata=metadata)
            )

    else:
        raise Exception(f"Request failed with status code: {response.status_code}")

    return results

```
 |  
| --- | --- |  
options: members: - PatentsviewReader
