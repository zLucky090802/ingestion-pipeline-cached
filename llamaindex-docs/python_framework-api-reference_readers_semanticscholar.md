# Semanticscholar
##  SemanticScholarReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/semanticscholar/#llama_index.readers.semanticscholar.SemanticScholarReader "Permanent link")
Bases: 
A class to read and process data from Semantic Scholar API ...
#### Methods[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/semanticscholar/#llama_index.readers.semanticscholar.SemanticScholarReader--methods "Permanent link")
**init**(): Instantiate the SemanticScholar object
load_data(query: str, limit: int = 10, returned_fields: list = ["title", "abstract", "venue", "year", "paperId", "citationCount", "openAccessPdf", "authors"]) -> list: Loads data from Semantic Scholar based on the query and returned_fields
Source code in `llama-index-integrations/readers/llama-index-readers-semanticscholar/llama_index/readers/semanticscholar/base.py`  
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
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
```
 | 
```
classSemanticScholarReader(BaseReader):
"""
    A class to read and process data from Semantic Scholar API
    ...

    Methods
    -------
    __init__():
       Instantiate the SemanticScholar object

    load_data(query: str, limit: int = 10, returned_fields: list = ["title", "abstract", "venue", "year", "paperId", "citationCount", "openAccessPdf", "authors"]) -> list:
        Loads data from Semantic Scholar based on the query and returned_fields

    """

    def__init__(self, timeout=10, api_key=None, base_dir="pdfs") -> None:
"""
        Instantiate the SemanticScholar object.
        """
        importarxiv

        fromsemanticscholarimport SemanticScholar

        self.arxiv = arxiv
        self.base_dir = base_dir
        self.s2 = SemanticScholar(timeout, api_key)
        # check for base dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def_clear_cache(self):
"""
        Delete the .citation* folder.
        """
        importshutil

        shutil.rmtree("./.citation*")

    def_download_pdf(self, paper_id, url: str, base_dir="pdfs"):
        logger = logging.getLogger()
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                " like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            )
        }
        # Making a GET request
        response = requests.get(url, headers=headers, stream=True)
        content_type = response.headers["Content-Type"]

        # As long as the content-type is application/pdf, this will download the file
        if "application/pdf" in content_type:
            os.makedirs(base_dir, exist_ok=True)
            file_path = os.path.join(base_dir, f"{paper_id}.pdf")
            # check if the file already exists
            if os.path.exists(file_path):
                logger.info(f"{file_path} already exists")
                return file_path
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            logger.info(f"Downloaded pdf from {url}")
            return file_path
        else:
            logger.warning(f"{url} was not downloaded: protected")
            return None

    def_get_full_text_docs(self, documents: List[Document]) -> List[Document]:
        fromPyPDF2import PdfReader

"""
        Gets the full text of the documents from Semantic Scholar

        Parameters
        ----------
        documents: list
            The list of Document object that contains the search results

        Returns
        -------
        list
            The list of Document object that contains the search results with full text

        Raises
        ------
        Exception
            If there is an error while getting the full text

        """
        full_text_docs = []
        for paper in documents:
            metadata = paper.extra_info
            url = metadata["openAccessPdf"]
            externalIds = metadata["externalIds"]
            paper_id = metadata["paperId"]
            file_path = None
            persist_dir = os.path.join(self.base_dir, f"{paper_id}.pdf")
            if url and not os.path.exists(persist_dir):
                # Download the document first
                file_path = self._download_pdf(metadata["paperId"], url, persist_dir)

            if (
                not url
                and externalIds
                and "ArXiv" in externalIds
                and not os.path.exists(persist_dir)
            ):
                # download the pdf from arxiv
                file_path = self._download_pdf_from_arxiv(
                    paper_id, externalIds["ArXiv"]
                )

            # Then, check if it's a valid PDF. If it's not, skip to the next document.
            if file_path:
                try:
                    pdf = PdfReader(open(file_path, "rb"))
                except Exception as e:
                    logging.error(
                        f"Failed to read pdf with exception: {e}. Skipping document..."
                    )
                    continue

                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                full_text_docs.append(Document(text=text, extra_info=metadata))

        return full_text_docs

    def_download_pdf_from_arxiv(self, paper_id, arxiv_id):
        paper = next(self.arxiv.Search(id_list=[arxiv_id], max_results=1).results())
        paper.download_pdf(dirpath=self.base_dir, filename=paper_id + ".pdf")
        return os.path.join(self.base_dir, f"{paper_id}.pdf")

    defload_data(
        self,
        query,
        limit,
        full_text=False,
        returned_fields=[
            "title",
            "abstract",
            "venue",
            "year",
            "paperId",
            "citationCount",
            "openAccessPdf",
            "authors",
            "externalIds",
        ],
    ) -> List[Document]:
"""
        Loads data from Semantic Scholar based on the entered query and returned_fields.

        Parameters
        ----------
        query: str
            The search query for the paper
        limit: int, optional
            The number of maximum results returned (default is 10)
        returned_fields: list, optional
            The list of fields to be returned from the search

        Returns
        -------
        list
            The list of Document object that contains the search results

        Raises
        ------
        Exception
            If there is an error while performing the search

        """
        try:
            results = self.s2.search_paper(query, limit=limit, fields=returned_fields)
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            logging.error(
                "Failed to fetch data from Semantic Scholar with exception: %s", e
            )
            raise
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)
            raise

        documents = []

        for item in results[:limit]:
            openAccessPdf = getattr(item, "openAccessPdf", None)
            abstract = getattr(item, "abstract", None)
            title = getattr(item, "title", None)
            text = None
            # concat title and abstract
            if abstract and title:
                text = title + " " + abstract
            elif not abstract:
                text = title

            metadata = {
                "title": title,
                "venue": getattr(item, "venue", None),
                "year": getattr(item, "year", None),
                "paperId": getattr(item, "paperId", None),
                "citationCount": getattr(item, "citationCount", None),
                "openAccessPdf": openAccessPdf.get("url") if openAccessPdf else None,
                "authors": [author["name"] for author in getattr(item, "authors", [])],
                "externalIds": getattr(item, "externalIds", None),
            }
            documents.append(Document(text=text, extra_info=metadata))

        if full_text:
            full_text_documents = self._get_full_text_docs(documents)
            documents.extend(full_text_documents)
        return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/semanticscholar/#llama_index.readers.semanticscholar.SemanticScholarReader.load_data "Permanent link")

```
load_data(
    query,
    limit,
    full_text=False,
    returned_fields=[
        "title",
        "abstract",
        "venue",
        "year",
        "paperId",
        "citationCount",
        "openAccessPdf",
        "authors",
        "externalIds",
    ],
) -> []

```

Loads data from Semantic Scholar based on the entered query and returned_fields.
##### Parameters[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/semanticscholar/#llama_index.readers.semanticscholar.SemanticScholarReader.load_data--parameters "Permanent link")
query: str The search query for the paper limit: int, optional The number of maximum results returned (default is 10) returned_fields: list, optional The list of fields to be returned from the search
##### Returns[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/semanticscholar/#llama_index.readers.semanticscholar.SemanticScholarReader.load_data--returns "Permanent link")
list The list of Document object that contains the search results
##### Raises[#](https://developers.llamaindex.ai/python/framework-api-reference/readers/semanticscholar/#llama_index.readers.semanticscholar.SemanticScholarReader.load_data--raises "Permanent link")
Exception If there is an error while performing the search
Source code in `llama-index-integrations/readers/llama-index-readers-semanticscholar/llama_index/readers/semanticscholar/base.py`  
| 
```
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
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
```
 | 
```
defload_data(
    self,
    query,
    limit,
    full_text=False,
    returned_fields=[
        "title",
        "abstract",
        "venue",
        "year",
        "paperId",
        "citationCount",
        "openAccessPdf",
        "authors",
        "externalIds",
    ],
) -> List[Document]:
"""
    Loads data from Semantic Scholar based on the entered query and returned_fields.

    Parameters
    ----------
    query: str
        The search query for the paper
    limit: int, optional
        The number of maximum results returned (default is 10)
    returned_fields: list, optional
        The list of fields to be returned from the search

    Returns
    -------
    list
        The list of Document object that contains the search results

    Raises
    ------
    Exception
        If there is an error while performing the search

    """
    try:
        results = self.s2.search_paper(query, limit=limit, fields=returned_fields)
    except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
        logging.error(
            "Failed to fetch data from Semantic Scholar with exception: %s", e
        )
        raise
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        raise

    documents = []

    for item in results[:limit]:
        openAccessPdf = getattr(item, "openAccessPdf", None)
        abstract = getattr(item, "abstract", None)
        title = getattr(item, "title", None)
        text = None
        # concat title and abstract
        if abstract and title:
            text = title + " " + abstract
        elif not abstract:
            text = title

        metadata = {
            "title": title,
            "venue": getattr(item, "venue", None),
            "year": getattr(item, "year", None),
            "paperId": getattr(item, "paperId", None),
            "citationCount": getattr(item, "citationCount", None),
            "openAccessPdf": openAccessPdf.get("url") if openAccessPdf else None,
            "authors": [author["name"] for author in getattr(item, "authors", [])],
            "externalIds": getattr(item, "externalIds", None),
        }
        documents.append(Document(text=text, extra_info=metadata))

    if full_text:
        full_text_documents = self._get_full_text_docs(documents)
        documents.extend(full_text_documents)
    return documents

```
 |  
| --- | --- |  
options: members: - SemanticScholarReader
