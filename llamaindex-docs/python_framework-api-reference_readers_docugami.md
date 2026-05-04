# Docugami
##  DocugamiReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader "Permanent link")
Bases: 
Docugami reader.
Reads Documents as nodes in a Document XML Knowledge Graph, from Docugami.
Source code in `llama-index-integrations/readers/llama-index-readers-docugami/llama_index/readers/docugami/base.py`  
| 
```
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
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
```
 | 
```
classDocugamiReader(BaseReader):
"""
    Docugami reader.

    Reads Documents as nodes in a Document XML Knowledge Graph, from Docugami.

    """

    api: str = DEFAULT_API_ENDPOINT
"""The Docugami API endpoint to use."""

    access_token: Optional[str] = os.environ.get("DOCUGAMI_API_KEY")
"""The Docugami API access token to use."""

    max_text_length = 4096
"""Max length of chunk text returned."""

    min_text_length: int = 32
"""Threshold under which chunks are appended to next to avoid over-chunking."""

    max_metadata_length = 512
"""Max length of metadata text returned."""

    include_xml_tags: bool = False
"""Set to true for XML tags in chunk output text."""

    parent_hierarchy_levels: int = 0
"""Set appropriately to get parent chunks using the chunk hierarchy."""

    parent_id_key: str = "doc_id"
"""Metadata key for parent doc ID."""

    sub_chunk_tables: bool = False
"""Set to True to return sub-chunks within tables."""

    whitespace_normalize_text: bool = True
"""Set to False if you want to full whitespace formatting in the original
    XML doc, including indentation."""

    docset_id: Optional[str]
"""The Docugami API docset ID to use."""

    document_ids: Optional[Sequence[str]]
"""The Docugami API document IDs to use."""

    file_paths: Optional[Sequence[Union[Path, str]]]
"""The local file paths to use."""

    include_project_metadata_in_doc_metadata: bool = True
"""Set to True if you want to include the project metadata in the doc metadata."""

    def__init__(
        self,
        api: str = DEFAULT_API_ENDPOINT,
        access_token: Optional[str] = os.environ.get("DOCUGAMI_API_KEY"),
        max_text_length=4096,
        min_text_length: int = 32,
        max_metadata_length=512,
        include_xml_tags: bool = False,
        parent_hierarchy_levels: int = 0,
        parent_id_key: str = "doc_id",
        sub_chunk_tables: bool = False,
        whitespace_normalize_text: bool = True,
        docset_id: Optional[str] = None,
        document_ids: Optional[Sequence[str]] = None,
        file_paths: Optional[Sequence[Union[Path, str]]] = None,
        include_project_metadata_in_doc_metadata: bool = True,
    ):
        self.api = api
        self.access_token = access_token
        self.max_text_length = max_text_length
        self.min_text_length = min_text_length
        self.max_metadata_length = max_metadata_length
        self.include_xml_tags = include_xml_tags
        self.parent_hierarchy_levels = parent_hierarchy_levels
        self.parent_id_key = parent_id_key
        self.sub_chunk_tables = sub_chunk_tables
        self.whitespace_normalize_text = whitespace_normalize_text
        self.docset_id = docset_id
        self.document_ids = document_ids
        self.file_paths = file_paths
        self.include_project_metadata_in_doc_metadata = (
            include_project_metadata_in_doc_metadata
        )

    def_parse_dgml(
        self,
        content: bytes,
        document_name: Optional[str] = None,
        additional_doc_metadata: Optional[Mapping] = None,
    ) -> List[Document]:
"""Parse a single DGML document into a list of Documents."""
        try:
            fromlxmlimport etree
        except ImportError:
            raise ImportError(
                "Could not import lxml python package. "
                "Please install it with `pip install lxml`."
            )

        # helpers
        def_xpath_qname_for_chunk(chunk: Any) -> str:
"""Get the xpath qname for a chunk."""
            qname = f"{chunk.prefix}:{chunk.tag.split('}')[-1]}"

            parent = chunk.getparent()
            if parent is not None:
                doppelgangers = [x for x in parent if x.tag == chunk.tag]
                if len(doppelgangers)  1:
                    idx_of_self = doppelgangers.index(chunk)
                    qname = f"{qname}[{idx_of_self+1}]"

            return qname

        def_xpath_for_chunk(chunk: Any) -> str:
"""Get the xpath for a chunk."""
            ancestor_chain = chunk.xpath("ancestor-or-self::*")
            return "/" + "/".join(_xpath_qname_for_chunk(x) for x in ancestor_chain)

        def_structure_value(node: Any) -> Optional[str]:
"""Get the structure value for a node."""
            return (
                "table"
                if node.tag == TABLE_NAME
                else node.attrib["structure"]
                if "structure" in node.attrib
                else None
            )

        def_build_framework_chunk(dg_chunk: Chunk) -> Document:
            # Adding dg_chunk.text + dg_chunk.xpath should prevent hash collision between two chunks that have the same text but a different xpath
            text = dg_chunk.xpath + "\n" + dg_chunk.text
            _hashed_id = hashlib.md5(text.encode()).hexdigest()
            metadata = {
                XPATH_KEY: dg_chunk.xpath,
                ID_KEY: _hashed_id,
                DOCUMENT_NAME_KEY: document_name,
                STRUCTURE_KEY: dg_chunk.structure,
                TAG_KEY: dg_chunk.tag,
            }

            text = dg_chunk.text
            if additional_doc_metadata:
                if self.include_project_metadata_in_doc_metadata:
                    metadata.update(additional_doc_metadata)

            return Document(
                text=text[: self.max_text_length],
                metadata=metadata,
                excluded_llm_metadata_keys=[XPATH_KEY, ID_KEY, STRUCTURE_KEY],
            )

        # Parse the tree and return chunks
        tree = etree.parse(io.BytesIO(content))
        root = tree.getroot()

        dg_chunks = get_chunks(
            root,
            min_text_length=self.min_text_length,
            max_text_length=self.max_text_length,
            whitespace_normalize_text=self.whitespace_normalize_text,
            sub_chunk_tables=self.sub_chunk_tables,
            include_xml_tags=self.include_xml_tags,
            parent_hierarchy_levels=self.parent_hierarchy_levels,
        )

        framework_chunks: Dict[str, Document] = {}
        for dg_chunk in dg_chunks:
            framework_chunk = _build_framework_chunk(dg_chunk)
            chunk_id = framework_chunk.metadata.get(ID_KEY)
            if chunk_id:
                framework_chunks[chunk_id] = framework_chunk
                if dg_chunk.parent:
                    framework_parent_chunk = _build_framework_chunk(dg_chunk.parent)
                    parent_id = framework_parent_chunk.metadata.get(ID_KEY)
                    if parent_id and framework_parent_chunk.text:
                        framework_chunk.metadata[self.parent_id_key] = parent_id
                        framework_chunks[parent_id] = framework_parent_chunk

        return list(framework_chunks.values())

    def_document_details_for_docset_id(self, docset_id: str) -> List[Dict]:
"""Gets all document details for the given docset ID."""
        url = f"{self.api}/docsets/{docset_id}/documents"
        all_documents = []

        while url:
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            if response.ok:
                data = response.json()
                all_documents.extend(data["documents"])
                url = data.get("next", None)
            else:
                raise Exception(
                    f"Failed to download {url} (status: {response.status_code})"
                )

        return all_documents

    def_project_details_for_docset_id(self, docset_id: str) -> List[Dict]:
"""Gets all project details for the given docset ID."""
        url = f"{self.api}/projects?docset.id={docset_id}"
        all_projects = []

        while url:
            response = requests.request(
                "GET",
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                data={},
            )
            if response.ok:
                data = response.json()
                all_projects.extend(data["projects"])
                url = data.get("next", None)
            else:
                raise Exception(
                    f"Failed to download {url} (status: {response.status_code})"
                )

        return all_projects

    def_metadata_for_project(self, project: Dict) -> Dict:
"""Gets project metadata for all files."""
        project_id = project.get(ID_KEY)

        url = f"{self.api}/projects/{project_id}/artifacts/latest"
        all_artifacts = []

        per_file_metadata: Dict = {}
        while url:
            response = requests.request(
                "GET",
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                data={},
            )
            if response.ok:
                data = response.json()
                all_artifacts.extend(data["artifacts"])
                url = data.get("next", None)
            elif response.status_code == 404:
                # Not found is ok, just means no published projects
                return per_file_metadata
            else:
                raise Exception(
                    f"Failed to download {url} (status: {response.status_code})"
                )

        for artifact in all_artifacts:
            artifact_name = artifact.get("name")
            artifact_url = artifact.get("url")
            artifact_doc = artifact.get("document")

            if artifact_name == "report-values.xml" and artifact_url and artifact_doc:
                doc_id = artifact_doc[ID_KEY]
                metadata: Dict = {}

                # The evaluated XML for each document is named after the project
                response = requests.request(
                    "GET",
                    f"{artifact_url}/content",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    data={},
                )

                if response.ok:
                    try:
                        fromlxmlimport etree
                    except ImportError:
                        raise ImportError(
                            "Could not import lxml python package. "
                            "Please install it with `pip install lxml`."
                        )
                    artifact_tree = etree.parse(io.BytesIO(response.content))
                    artifact_root = artifact_tree.getroot()
                    ns = artifact_root.nsmap
                    entries = artifact_root.xpath("//pr:Entry", namespaces=ns)
                    for entry in entries:
                        heading = entry.xpath("./pr:Heading", namespaces=ns)[0].text
                        value = " ".join(
                            entry.xpath("./pr:Value", namespaces=ns)[0].itertext()
                        ).strip()
                        metadata[heading] = value[: self.max_metadata_length]
                    per_file_metadata[doc_id] = metadata
                else:
                    raise Exception(
                        f"Failed to download {artifact_url}/content "
                        + "(status: {response.status_code})"
                    )

        return per_file_metadata

    def_load_chunks_for_document(
        self,
        document_id: str,
        docset_id: str,
        document_name: Optional[str] = None,
        additional_metadata: Optional[Mapping] = None,
    ) -> List[Document]:
"""Load chunks for a document."""
        url = f"{self.api}/docsets/{docset_id}/documents/{document_id}/dgml"

        response = requests.request(
            "GET",
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            data={},
        )

        if response.ok:
            return self._parse_dgml(
                content=response.content,
                document_name=document_name,
                additional_doc_metadata=additional_metadata,
            )
        else:
            raise Exception(
                f"Failed to download {url} (status: {response.status_code})"
            )

    defload_data(
        self,
        docset_id: str,
        document_ids: Optional[List[str]] = None,
        access_token: Optional[str] = None,
    ) -> List[Document]:
"""
        Load data the given docset_id in Docugami.

        Args:
            docset_id (str): Document set ID to load data for.
            document_ids (Optional[List[str]]): Optional list of document ids to load data for.
                                    If not specified, all documents from docset_id are loaded.

        """
        chunks: List[Document] = []

        if access_token:
            self.access_token = access_token

        if not self.access_token:
            raise Exception(
                "Please specify access token as argument or set the DOCUGAMI_API_KEY"
                " env var."
            )

        _document_details = self._document_details_for_docset_id(docset_id)
        if document_ids:
            _document_details = [
                d for d in _document_details if d[ID_KEY] in document_ids
            ]

        _project_details = self._project_details_for_docset_id(docset_id)
        combined_project_metadata: Dict[str, Dict] = {}
        if _project_details and self.include_project_metadata_in_doc_metadata:
            # If there are any projects for this docset and the caller requested
            # project metadata, load it.
            for project in _project_details:
                metadata = self._metadata_for_project(project)
                for file_id in metadata:
                    if file_id not in combined_project_metadata:
                        combined_project_metadata[file_id] = metadata[file_id]
                    else:
                        combined_project_metadata[file_id].update(metadata[file_id])

        for doc in _document_details:
            doc_id = doc[ID_KEY]
            doc_name = doc.get(DOCUMENT_NAME_KEY)
            doc_metadata = combined_project_metadata.get(doc_id)
            chunks += self._load_chunks_for_document(
                document_id=doc_id,
                docset_id=docset_id,
                document_name=doc_name,
                additional_metadata=doc_metadata,
            )

        return chunks

```
 |  
| --- | --- |  
###  api `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.api "Permanent link")

```
api:  = 

```

The Docugami API endpoint to use.
###  access_token `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.access_token "Permanent link")

```
access_token: Optional[] = access_token

```

The Docugami API access token to use.
###  max_text_length `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.max_text_length "Permanent link")

```
max_text_length = max_text_length

```

Max length of chunk text returned.
###  min_text_length `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.min_text_length "Permanent link")

```
min_text_length:  = min_text_length

```

Threshold under which chunks are appended to next to avoid over-chunking.
###  max_metadata_length `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.max_metadata_length "Permanent link")

```
max_metadata_length = max_metadata_length

```

Max length of metadata text returned.
###  include_xml_tags `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.include_xml_tags "Permanent link")

```
include_xml_tags:  = include_xml_tags

```

Set to true for XML tags in chunk output text.
###  parent_hierarchy_levels `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.parent_hierarchy_levels "Permanent link")

```
parent_hierarchy_levels:  = parent_hierarchy_levels

```

Set appropriately to get parent chunks using the chunk hierarchy.
###  parent_id_key `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.parent_id_key "Permanent link")

```
parent_id_key:  = parent_id_key

```

Metadata key for parent doc ID.
###  sub_chunk_tables `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.sub_chunk_tables "Permanent link")

```
sub_chunk_tables:  = sub_chunk_tables

```

Set to True to return sub-chunks within tables.
###  whitespace_normalize_text `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.whitespace_normalize_text "Permanent link")

```
whitespace_normalize_text:  = whitespace_normalize_text

```

Set to False if you want to full whitespace formatting in the original XML doc, including indentation.
###  docset_id `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.docset_id "Permanent link")

```
docset_id: Optional[] = docset_id

```

The Docugami API docset ID to use.
###  document_ids `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.document_ids "Permanent link")

```
document_ids: Optional[Sequence[]] = document_ids

```

The Docugami API document IDs to use.
###  file_paths `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.file_paths "Permanent link")

```
file_paths: Optional[Sequence[Union[, ]]] = (
    file_paths
)

```

The local file paths to use.
###  include_project_metadata_in_doc_metadata `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.include_project_metadata_in_doc_metadata "Permanent link")

```
include_project_metadata_in_doc_metadata:  = (
    include_project_metadata_in_doc_metadata
)

```

Set to True if you want to include the project metadata in the doc metadata.
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/docugami/#llama_index.readers.docugami.DocugamiReader.load_data "Permanent link")

```
load_data(
    docset_id: ,
    document_ids: Optional[[]] = None,
    access_token: Optional[] = None,
) -> []

```

Load data the given docset_id in Docugami.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `docset_id`  |  Document set ID to load data for.  |  _required_  |  
|  `document_ids`  |  `Optional[List[str]]`  |  Optional list of document ids to load data for. If not specified, all documents from docset_id are loaded.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-docugami/llama_index/readers/docugami/base.py`  
| 
```
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
```
 | 
```
defload_data(
    self,
    docset_id: str,
    document_ids: Optional[List[str]] = None,
    access_token: Optional[str] = None,
) -> List[Document]:
"""
    Load data the given docset_id in Docugami.

    Args:
        docset_id (str): Document set ID to load data for.
        document_ids (Optional[List[str]]): Optional list of document ids to load data for.
                                If not specified, all documents from docset_id are loaded.

    """
    chunks: List[Document] = []

    if access_token:
        self.access_token = access_token

    if not self.access_token:
        raise Exception(
            "Please specify access token as argument or set the DOCUGAMI_API_KEY"
            " env var."
        )

    _document_details = self._document_details_for_docset_id(docset_id)
    if document_ids:
        _document_details = [
            d for d in _document_details if d[ID_KEY] in document_ids
        ]

    _project_details = self._project_details_for_docset_id(docset_id)
    combined_project_metadata: Dict[str, Dict] = {}
    if _project_details and self.include_project_metadata_in_doc_metadata:
        # If there are any projects for this docset and the caller requested
        # project metadata, load it.
        for project in _project_details:
            metadata = self._metadata_for_project(project)
            for file_id in metadata:
                if file_id not in combined_project_metadata:
                    combined_project_metadata[file_id] = metadata[file_id]
                else:
                    combined_project_metadata[file_id].update(metadata[file_id])

    for doc in _document_details:
        doc_id = doc[ID_KEY]
        doc_name = doc.get(DOCUMENT_NAME_KEY)
        doc_metadata = combined_project_metadata.get(doc_id)
        chunks += self._load_chunks_for_document(
            document_id=doc_id,
            docset_id=docset_id,
            document_name=doc_name,
            additional_metadata=doc_metadata,
        )

    return chunks

```
 |  
| --- | --- |  
options: members: - DocugamiReader
