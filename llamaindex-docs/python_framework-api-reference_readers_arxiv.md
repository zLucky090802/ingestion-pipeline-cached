# Arxiv
Init file.
##  ArxivReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/arxiv/#llama_index.readers.papers.ArxivReader "Permanent link")
Bases: 
Arxiv Reader.
Gets a search query, return a list of Documents of the top corresponding scientific papers on Arxiv.
Source code in `llama-index-integrations/readers/llama-index-readers-papers/llama_index/readers/papers/arxiv/base.py`  
| 
```
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
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
```
 | 
```
classArxivReader(BaseReader):
"""
    Arxiv Reader.

    Gets a search query, return a list of Documents of the top corresponding scientific papers on Arxiv.
    """

    def__init__(
        self,
    ) -> None:
"""Initialize with parameters."""
        super().__init__()

    def_hacky_hash(self, some_string):
        return hashlib.md5(some_string.encode("utf-8")).hexdigest()

    defload_data(
        self,
        search_query: str,
        papers_dir: Optional[str] = ".papers",
        max_results: Optional[int] = 10,
    ) -> List[Document]:
"""
        Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.

        Args:
            search_query (str): A topic to search for (e.g. "Artificial Intelligence").
            papers_dir (Optional[str]): Locally directory to store the papers
            max_results (Optional[int]): Maximum number of papers to fetch.

        Returns:
            List[Document]: A list of Document objects.

        """
        importarxiv

        arxiv_search = arxiv.Search(
            query=search_query,
            id_list=[],
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        search_results = list(arxiv_search.results())
        logging.debug(f"> Successfully fetched {len(search_results)} paperes")

        if not os.path.exists(papers_dir):
            os.makedirs(papers_dir)

        paper_lookup = {}
        for paper in search_results:
            # Hash filename to avoid bad characters in file path
            hashed_name = self._hacky_hash(f"{paper.title}{paper.entry_id}")
            filename = f"{hashed_name}.pdf"
            paper_lookup[filename] = {
                "Title of this paper": paper.title,
                "Authors": (", ").join([a.name for a in paper.authors]),
                "Date published": paper.published.strftime("%m/%d/%Y"),
                "URL": paper.entry_id,
                # "summary": paper.summary
            }
            paper.download_pdf(dirpath=papers_dir, filename=filename)
            logging.debug(f"> Downloading {filename}...")

        defget_paper_metadata(filename):
            return paper_lookup[os.path.basename(filename)]

        arxiv_documents = SimpleDirectoryReader(
            papers_dir,
            file_metadata=get_paper_metadata,
            exclude_hidden=False,  # default directory is hidden ".papers"
        ).load_data()
        # Include extra documents containing the abstracts
        abstract_documents = []
        for paper in search_results:
            d = (
                f"The following is a summary of the paper: {paper.title}\n\nSummary:"
                f" {paper.summary}"
            )
            abstract_documents.append(Document(text=d))

        # Delete downloaded papers
        try:
            for f in os.listdir(papers_dir):
                os.remove(os.path.join(papers_dir, f))
                logging.debug(f"> Deleted file: {f}")
            os.rmdir(papers_dir)
            logging.debug(f"> Deleted directory: {papers_dir}")
        except OSError:
            print("Unable to delete files or directory")

        return arxiv_documents + abstract_documents

    defload_papers_and_abstracts(
        self,
        search_query: str,
        papers_dir: Optional[str] = ".papers",
        max_results: Optional[int] = 10,
    ) -> Tuple[List[Document], List[Document]]:
"""
        Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.

        Args:
            search_query (str): A topic to search for (e.g. "Artificial Intelligence").
            papers_dir (Optional[str]): Locally directory to store the papers
            max_results (Optional[int]): Maximum number of papers to fetch.

        Returns:
            List[Document]: A list of Document objects representing the papers themselves
            List[Document]: A list of Document objects representing abstracts only

        """
        importarxiv

        arxiv_search = arxiv.Search(
            query=search_query,
            id_list=[],
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        search_results = list(arxiv_search.results())
        logging.debug(f"> Successfully fetched {len(search_results)} paperes")

        if not os.path.exists(papers_dir):
            os.makedirs(papers_dir)

        paper_lookup = {}
        for paper in search_results:
            # Hash filename to avoid bad characters in file path
            hashed_name = self._hacky_hash(f"{paper.title}{paper.entry_id}")
            filename = f"{hashed_name}.pdf"
            paper_lookup[filename] = {
                "Title of this paper": paper.title,
                "Authors": (", ").join([a.name for a in paper.authors]),
                "Date published": paper.published.strftime("%m/%d/%Y"),
                "URL": paper.entry_id,
                # "summary": paper.summary
            }
            paper.download_pdf(dirpath=papers_dir, filename=filename)
            logging.debug(f"> Downloading {filename}...")

        defget_paper_metadata(filename):
            return paper_lookup[os.path.basename(filename)]

        arxiv_documents = SimpleDirectoryReader(
            papers_dir,
            file_metadata=get_paper_metadata,
            exclude_hidden=False,  # default directory is hidden ".papers"
        ).load_data()
        # Include extra documents containing the abstracts
        abstract_documents = []
        for paper in search_results:
            d = (
                f"The following is a summary of the paper: {paper.title}\n\nSummary:"
                f" {paper.summary}"
            )
            abstract_documents.append(Document(text=d))

        # Delete downloaded papers
        try:
            for f in os.listdir(papers_dir):
                os.remove(os.path.join(papers_dir, f))
                logging.debug(f"> Deleted file: {f}")
            os.rmdir(papers_dir)
            logging.debug(f"> Deleted directory: {papers_dir}")
        except OSError:
            print("Unable to delete files or directory")

        return arxiv_documents, abstract_documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/arxiv/#llama_index.readers.papers.ArxivReader.load_data "Permanent link")

```
load_data(
    search_query: ,
    papers_dir: Optional[] = ".papers",
    max_results: Optional[] = 10,
) -> []

```

Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `search_query`  |  A topic to search for (e.g. "Artificial Intelligence").  |  _required_  |  
|  `papers_dir`  |  `Optional[str]`  |  Locally directory to store the papers  |  `'.papers'`  |  
|  `max_results`  |  `Optional[int]`  |  Maximum number of papers to fetch.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-papers/llama_index/readers/papers/arxiv/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    search_query: str,
    papers_dir: Optional[str] = ".papers",
    max_results: Optional[int] = 10,
) -> List[Document]:
"""
    Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.

    Args:
        search_query (str): A topic to search for (e.g. "Artificial Intelligence").
        papers_dir (Optional[str]): Locally directory to store the papers
        max_results (Optional[int]): Maximum number of papers to fetch.

    Returns:
        List[Document]: A list of Document objects.

    """
    importarxiv

    arxiv_search = arxiv.Search(
        query=search_query,
        id_list=[],
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    search_results = list(arxiv_search.results())
    logging.debug(f"> Successfully fetched {len(search_results)} paperes")

    if not os.path.exists(papers_dir):
        os.makedirs(papers_dir)

    paper_lookup = {}
    for paper in search_results:
        # Hash filename to avoid bad characters in file path
        hashed_name = self._hacky_hash(f"{paper.title}{paper.entry_id}")
        filename = f"{hashed_name}.pdf"
        paper_lookup[filename] = {
            "Title of this paper": paper.title,
            "Authors": (", ").join([a.name for a in paper.authors]),
            "Date published": paper.published.strftime("%m/%d/%Y"),
            "URL": paper.entry_id,
            # "summary": paper.summary
        }
        paper.download_pdf(dirpath=papers_dir, filename=filename)
        logging.debug(f"> Downloading {filename}...")

    defget_paper_metadata(filename):
        return paper_lookup[os.path.basename(filename)]

    arxiv_documents = SimpleDirectoryReader(
        papers_dir,
        file_metadata=get_paper_metadata,
        exclude_hidden=False,  # default directory is hidden ".papers"
    ).load_data()
    # Include extra documents containing the abstracts
    abstract_documents = []
    for paper in search_results:
        d = (
            f"The following is a summary of the paper: {paper.title}\n\nSummary:"
            f" {paper.summary}"
        )
        abstract_documents.append(Document(text=d))

    # Delete downloaded papers
    try:
        for f in os.listdir(papers_dir):
            os.remove(os.path.join(papers_dir, f))
            logging.debug(f"> Deleted file: {f}")
        os.rmdir(papers_dir)
        logging.debug(f"> Deleted directory: {papers_dir}")
    except OSError:
        print("Unable to delete files or directory")

    return arxiv_documents + abstract_documents

```
 |  
| --- | --- |  
###  load_papers_and_abstracts [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/arxiv/#llama_index.readers.papers.ArxivReader.load_papers_and_abstracts "Permanent link")

```
load_papers_and_abstracts(
    search_query: ,
    papers_dir: Optional[] = ".papers",
    max_results: Optional[] = 10,
) -> Tuple[[], []]

```

Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `search_query`  |  A topic to search for (e.g. "Artificial Intelligence").  |  _required_  |  
|  `papers_dir`  |  `Optional[str]`  |  Locally directory to store the papers  |  `'.papers'`  |  
|  `max_results`  |  `Optional[int]`  |  Maximum number of papers to fetch.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects representing the papers themselves  |  
|   |  List[Document]: A list of Document objects representing abstracts only  |  
Source code in `llama-index-integrations/readers/llama-index-readers-papers/llama_index/readers/papers/arxiv/base.py`  
| 
```
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
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
```
 | 
```
defload_papers_and_abstracts(
    self,
    search_query: str,
    papers_dir: Optional[str] = ".papers",
    max_results: Optional[int] = 10,
) -> Tuple[List[Document], List[Document]]:
"""
    Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.

    Args:
        search_query (str): A topic to search for (e.g. "Artificial Intelligence").
        papers_dir (Optional[str]): Locally directory to store the papers
        max_results (Optional[int]): Maximum number of papers to fetch.

    Returns:
        List[Document]: A list of Document objects representing the papers themselves
        List[Document]: A list of Document objects representing abstracts only

    """
    importarxiv

    arxiv_search = arxiv.Search(
        query=search_query,
        id_list=[],
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    search_results = list(arxiv_search.results())
    logging.debug(f"> Successfully fetched {len(search_results)} paperes")

    if not os.path.exists(papers_dir):
        os.makedirs(papers_dir)

    paper_lookup = {}
    for paper in search_results:
        # Hash filename to avoid bad characters in file path
        hashed_name = self._hacky_hash(f"{paper.title}{paper.entry_id}")
        filename = f"{hashed_name}.pdf"
        paper_lookup[filename] = {
            "Title of this paper": paper.title,
            "Authors": (", ").join([a.name for a in paper.authors]),
            "Date published": paper.published.strftime("%m/%d/%Y"),
            "URL": paper.entry_id,
            # "summary": paper.summary
        }
        paper.download_pdf(dirpath=papers_dir, filename=filename)
        logging.debug(f"> Downloading {filename}...")

    defget_paper_metadata(filename):
        return paper_lookup[os.path.basename(filename)]

    arxiv_documents = SimpleDirectoryReader(
        papers_dir,
        file_metadata=get_paper_metadata,
        exclude_hidden=False,  # default directory is hidden ".papers"
    ).load_data()
    # Include extra documents containing the abstracts
    abstract_documents = []
    for paper in search_results:
        d = (
            f"The following is a summary of the paper: {paper.title}\n\nSummary:"
            f" {paper.summary}"
        )
        abstract_documents.append(Document(text=d))

    # Delete downloaded papers
    try:
        for f in os.listdir(papers_dir):
            os.remove(os.path.join(papers_dir, f))
            logging.debug(f"> Deleted file: {f}")
        os.rmdir(papers_dir)
        logging.debug(f"> Deleted directory: {papers_dir}")
    except OSError:
        print("Unable to delete files or directory")

    return arxiv_documents, abstract_documents

```
 |  
| --- | --- |  
##  PubmedReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/arxiv/#llama_index.readers.papers.PubmedReader "Permanent link")
Bases: 
Pubmed Reader.
Gets a search query, return a list of Documents of the top corresponding scientific papers on Pubmed.
Source code in `llama-index-integrations/readers/llama-index-readers-papers/llama_index/readers/papers/pubmed/base.py`  
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
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
```
 | 
```
classPubmedReader(BaseReader):
"""
    Pubmed Reader.

    Gets a search query, return a list of Documents of the top corresponding scientific papers on Pubmed.
    """

    defload_data_bioc(
        self,
        search_query: str,
        max_results: Optional[int] = 10,
    ) -> List[Document]:
"""
        Search for a topic on Pubmed, fetch the text of the most relevant full-length papers.
        Uses the BoiC API, which has been down a lot.

        Args:
            search_query (str): A topic to search for (e.g. "Alzheimers").
            max_results (Optional[int]): Maximum number of papers to fetch.

        Returns:
            List[Document]: A list of Document objects.

        """
        fromdatetimeimport datetime

        importrequests
        fromdefusedxmlimport ElementTree as safe_xml

        pubmed_search = []
        parameters = {"tool": "tool", "email": "email", "db": "pmc"}
        parameters["term"] = search_query
        parameters["retmax"] = max_results
        resp = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params=parameters,
        )
        root = safe_xml.fromstring(resp.content)

        for elem in root.iter():
            if elem.tag == "Id":
                _id = elem.text
                try:
                    resp = requests.get(
                        f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC{_id}/ascii"
                    )
                    info = resp.json()
                    title = "Pubmed Paper"
                    try:
                        title = next(
                            [
                                p["text"]
                                for p in info["documents"][0]["passages"]
                                if p["infons"]["section_type"] == "TITLE"
                            ]
                        )
                    except KeyError:
                        pass
                    pubmed_search.append(
                        {
                            "title": title,
                            "url": (
                                f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{_id}/"
                            ),
                            "date": info["date"],
                            "documents": info["documents"],
                        }
                    )
                except Exception:
                    print(f"Unable to parse PMC{_id} or it does not exist")

        # Then get documents from Pubmed text, which includes abstracts
        pubmed_documents = []
        for paper in pubmed_search:
            for d in paper["documents"]:
                text = "\n".join([p["text"] for p in d["passages"]])
                pubmed_documents.append(
                    Document(
                        text=text,
                        extra_info={
                            "Title of this paper": paper["title"],
                            "URL": paper["url"],
                            "Date published": datetime.strptime(
                                paper["date"], "%Y%m%d"
                            ).strftime("%m/%d/%Y"),
                        },
                    )
                )

        return pubmed_documents

    defload_data(
        self,
        search_query: str,
        max_results: Optional[int] = 10,
    ) -> List[Document]:
"""
        Search for a topic on Pubmed, fetch the text of the most relevant full-length papers.

        Args:
            search_query (str): A topic to search for (e.g. "Alzheimers").
            max_results (Optional[int]): Maximum number of papers to fetch.


        Returns:
            List[Document]: A list of Document objects.

        """
        importtime

        importrequests

        pubmed_search = []
        parameters = {"tool": "tool", "email": "email", "db": "pmc"}
        parameters["term"] = search_query
        parameters["retmax"] = max_results
        resp = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params=parameters,
        )
        root = safe_xml.fromstring(resp.content)

        for elem in root.iter():
            if elem.tag == "Id":
                _id = elem.text
                url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?id={_id}&db=pmc"
                print(url)
                try:
                    resp = requests.get(url)
                    info = safe_xml.fromstring(resp.content)

                    raw_text = ""
                    title = ""
                    journal = ""
                    for element in info.iter():
                        if element.tag == "article-title":
                            title = element.text
                        elif element.tag == "journal-title":
                            journal = element.text

                        if element.text:
                            raw_text += element.text.strip() + " "

                    pubmed_search.append(
                        {
                            "title": title,
                            "journal": journal,
                            "url": (
                                f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{_id}/"
                            ),
                            "text": raw_text,
                        }
                    )
                    time.sleep(1)  # API rate limits
                except Exception as e:
                    print(f"Unable to parse PMC{_id} or it does not exist:", e)

        # Then get documents from Pubmed text, which includes abstracts
        pubmed_documents = []
        for paper in pubmed_search:
            pubmed_documents.append(
                Document(
                    text=paper["text"],
                    extra_info={
                        "Title of this paper": paper["title"],
                        "Journal it was published in:": paper["journal"],
                        "URL": paper["url"],
                    },
                )
            )

        return pubmed_documents

```
 |  
| --- | --- |  
###  load_data_bioc [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/arxiv/#llama_index.readers.papers.PubmedReader.load_data_bioc "Permanent link")

```
load_data_bioc(
    search_query: , max_results: Optional[] = 10
) -> []

```

Search for a topic on Pubmed, fetch the text of the most relevant full-length papers. Uses the BoiC API, which has been down a lot.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `search_query`  |  A topic to search for (e.g. "Alzheimers").  |  _required_  |  
|  `max_results`  |  `Optional[int]`  |  Maximum number of papers to fetch.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-papers/llama_index/readers/papers/pubmed/base.py`  
| 
```
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
```
 | 
```
defload_data_bioc(
    self,
    search_query: str,
    max_results: Optional[int] = 10,
) -> List[Document]:
"""
    Search for a topic on Pubmed, fetch the text of the most relevant full-length papers.
    Uses the BoiC API, which has been down a lot.

    Args:
        search_query (str): A topic to search for (e.g. "Alzheimers").
        max_results (Optional[int]): Maximum number of papers to fetch.

    Returns:
        List[Document]: A list of Document objects.

    """
    fromdatetimeimport datetime

    importrequests
    fromdefusedxmlimport ElementTree as safe_xml

    pubmed_search = []
    parameters = {"tool": "tool", "email": "email", "db": "pmc"}
    parameters["term"] = search_query
    parameters["retmax"] = max_results
    resp = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        params=parameters,
    )
    root = safe_xml.fromstring(resp.content)

    for elem in root.iter():
        if elem.tag == "Id":
            _id = elem.text
            try:
                resp = requests.get(
                    f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC{_id}/ascii"
                )
                info = resp.json()
                title = "Pubmed Paper"
                try:
                    title = next(
                        [
                            p["text"]
                            for p in info["documents"][0]["passages"]
                            if p["infons"]["section_type"] == "TITLE"
                        ]
                    )
                except KeyError:
                    pass
                pubmed_search.append(
                    {
                        "title": title,
                        "url": (
                            f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{_id}/"
                        ),
                        "date": info["date"],
                        "documents": info["documents"],
                    }
                )
            except Exception:
                print(f"Unable to parse PMC{_id} or it does not exist")

    # Then get documents from Pubmed text, which includes abstracts
    pubmed_documents = []
    for paper in pubmed_search:
        for d in paper["documents"]:
            text = "\n".join([p["text"] for p in d["passages"]])
            pubmed_documents.append(
                Document(
                    text=text,
                    extra_info={
                        "Title of this paper": paper["title"],
                        "URL": paper["url"],
                        "Date published": datetime.strptime(
                            paper["date"], "%Y%m%d"
                        ).strftime("%m/%d/%Y"),
                    },
                )
            )

    return pubmed_documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/arxiv/#llama_index.readers.papers.PubmedReader.load_data "Permanent link")

```
load_data(
    search_query: , max_results: Optional[] = 10
) -> []

```

Search for a topic on Pubmed, fetch the text of the most relevant full-length papers.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `search_query`  |  A topic to search for (e.g. "Alzheimers").  |  _required_  |  
|  `max_results`  |  `Optional[int]`  |  Maximum number of papers to fetch.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of Document objects.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-papers/llama_index/readers/papers/pubmed/base.py`  
| 
```
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
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
```
 | 
```
defload_data(
    self,
    search_query: str,
    max_results: Optional[int] = 10,
) -> List[Document]:
"""
    Search for a topic on Pubmed, fetch the text of the most relevant full-length papers.

    Args:
        search_query (str): A topic to search for (e.g. "Alzheimers").
        max_results (Optional[int]): Maximum number of papers to fetch.


    Returns:
        List[Document]: A list of Document objects.

    """
    importtime

    importrequests

    pubmed_search = []
    parameters = {"tool": "tool", "email": "email", "db": "pmc"}
    parameters["term"] = search_query
    parameters["retmax"] = max_results
    resp = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        params=parameters,
    )
    root = safe_xml.fromstring(resp.content)

    for elem in root.iter():
        if elem.tag == "Id":
            _id = elem.text
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?id={_id}&db=pmc"
            print(url)
            try:
                resp = requests.get(url)
                info = safe_xml.fromstring(resp.content)

                raw_text = ""
                title = ""
                journal = ""
                for element in info.iter():
                    if element.tag == "article-title":
                        title = element.text
                    elif element.tag == "journal-title":
                        journal = element.text

                    if element.text:
                        raw_text += element.text.strip() + " "

                pubmed_search.append(
                    {
                        "title": title,
                        "journal": journal,
                        "url": (
                            f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{_id}/"
                        ),
                        "text": raw_text,
                    }
                )
                time.sleep(1)  # API rate limits
            except Exception as e:
                print(f"Unable to parse PMC{_id} or it does not exist:", e)

    # Then get documents from Pubmed text, which includes abstracts
    pubmed_documents = []
    for paper in pubmed_search:
        pubmed_documents.append(
            Document(
                text=paper["text"],
                extra_info={
                    "Title of this paper": paper["title"],
                    "Journal it was published in:": paper["journal"],
                    "URL": paper["url"],
                },
            )
        )

    return pubmed_documents

```
 |  
| --- | --- |  
options: members: - ArxivReader - PubmedReader
