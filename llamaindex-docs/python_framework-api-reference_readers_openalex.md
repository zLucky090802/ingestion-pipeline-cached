# Openalex
Init file.
##  OpenAlexReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/openalex/#llama_index.readers.openalex.OpenAlexReader "Permanent link")
Bases: 
This class is used to search and import data from OpenAlex.
#### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/openalex/#llama_index.readers.openalex.OpenAlexReader--parameters "Permanent link")
email : str Email address to use for OpenAlex API
#### Attributes[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/openalex/#llama_index.readers.openalex.OpenAlexReader--attributes "Permanent link")
Works : pyalex.Works pyalex.Works object pyalex : pyalex pyalex object
Source code in `llama-index-integrations/readers/llama-index-readers-openalex/llama_index/readers/openalex/base.py`  
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
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
```
 | 
```
classOpenAlexReader(BaseReader):
"""
    This class is used to search and import data from OpenAlex.

    Parameters
    ----------
    email : str
        Email address to use for OpenAlex API

    Attributes
    ----------
    Works : pyalex.Works
        pyalex.Works object
    pyalex : pyalex
        pyalex object

    """

    def__init__(self, email) -> None:
        self.email = email

    def_search_openalex(self, query, fields):
        base_url = "https://api.openalex.org/works?search="
        fields_param = f"&select={fields}"
        email_param = f"&mailto={self.email}"
        full_url = base_url + query + fields_param + email_param
        try:
            response = requests.get(full_url, timeout=10)
            response.raise_for_status()  # Check if request is successful
            data = response.json()  # Parse JSON data
            if "error" in data:
                raise ValueError(f"API returned error: {data['error']}")
            return data
        except requests.exceptions.HTTPError as http_error:
            logger.error(f"HTTP error occurred: {http_error}")
        except requests.exceptions.RequestException as request_error:
            logger.error(f"Error occurred: {request_error}")
        except ValueError as value_error:
            logger.error(value_error)
        return None

    def_fulltext_search_openalex(self, query, fields):
        base_url = "https://api.openalex.org/works?filter=fulltext.search:"
        fields_param = f"&select={fields}"
        email_param = f"&mailto={self.email}"
        full_url = base_url + query + fields_param + email_param
        try:
            response = requests.get(full_url, timeout=10)
            response.raise_for_status()  # Check if request is successful
            data = response.json()  # Parse JSON data
            if "error" in data:
                raise ValueError(f"API returned error: {data['error']}")
            return data
        except requests.exceptions.HTTPError as http_error:
            logger.error(f"HTTP error occurred: {http_error}")
        except requests.exceptions.RequestException as request_error:
            logger.error(f"Error occurred: {request_error}")
        except ValueError as value_error:
            logger.error(value_error)
        return None

    def_invert_abstract(self, inv_index):
        if inv_index is not None:
            l_inv = [(w, p) for w, pos in inv_index.items() for p in pos]
            return " ".join(x[0] for x in sorted(l_inv, key=lambda x: x[1]))
        return None

    defload_data(self, query: str, full_text=False, fields=None) -> List[Document]:
        if fields is None:
            fields = "title,abstract_inverted_index,publication_year,keywords,authorships,primary_location"

        if full_text:
            works = self._fulltext_search_openalex(query, fields)
        else:
            works = self._search_openalex(query, fields)

        documents = []

        for work in works["results"]:
            if work["abstract_inverted_index"] is not None:
                abstract = self._invert_abstract(work["abstract_inverted_index"])
            else:
                abstract = None
            title = work.get("title", None)
            text = None
            # concat title and abstract
            if abstract and title:
                text = title + " " + abstract
            elif not abstract:
                text = title
            try:
                primary_location = work["primary_location"]["source"]["display_name"]
            except (KeyError, TypeError):
                primary_location = None

            metadata = {
                "title": work.get("title", None),
                "keywords": work.get("keywords", None),
                "primary_location": primary_location,
                "publication_year": work.get("publication_year", None),
                "authorships": [
                    item["author"]["display_name"] for item in work["authorships"]
                ],
            }

            documents.append(Document(text=text, extra_info=metadata))

        return documents

```
 |  
| --- | --- |  
options: members: - OpenAlexReader
