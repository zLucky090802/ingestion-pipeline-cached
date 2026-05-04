# Vectara
##  VectaraIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraIndex "Permanent link")
Bases: `BaseManagedIndex`
Vectara Index.
The Vectara index implements a managed index that uses Vectara as the backend. Vectara performs a lot of the functions in traditional indexes in the backend: - breaks down a document into chunks (nodes) - Creates the embedding for each chunk (node) - Performs the search for the top k most similar nodes to a query - Optionally can perform summarization of the top k nodes
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/base.py`  
| 
```
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
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
```
 | 
```
classVectaraIndex(BaseManagedIndex):
"""
    Vectara Index.

    The Vectara index implements a managed index that uses Vectara as the backend.
    Vectara performs a lot of the functions in traditional indexes in the backend:
    - breaks down a document into chunks (nodes)
    - Creates the embedding for each chunk (node)
    - Performs the search for the top k most similar nodes to a query
    - Optionally can perform summarization of the top k nodes

    Args:
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.

    """

    def__init__(
        self,
        show_progress: bool = False,
        vectara_corpus_key: Optional[str] = None,
        vectara_api_key: Optional[str] = None,
        parallelize_ingest: bool = False,
        x_source_str: str = "llama_index",
        vectara_base_url: str = "https://api.vectara.io",
        vectara_verify_ssl: bool = True,
        **kwargs: Any,
    ) -> None:
"""Initialize the Vectara API."""
        self.parallelize_ingest = parallelize_ingest
        self._base_url = vectara_base_url.rstrip("/")

        index_struct = VectaraIndexStruct(
            index_id=str(vectara_corpus_key),
            summary="Vectara Index",
        )

        super().__init__(
            show_progress=show_progress,
            index_struct=index_struct,
            **kwargs,
        )

        self._vectara_corpus_key = vectara_corpus_key or str(
            os.environ.get("VECTARA_CORPUS_KEY")
        )

        self._vectara_api_key = vectara_api_key or os.environ.get("VECTARA_API_KEY")
        if self._vectara_corpus_key is None or self._vectara_api_key is None:
            _logger.warning(
                "Can't find Vectara credentials or corpus_key in environment."
            )
            raise ValueError("Missing Vectara credentials")
        else:
            _logger.debug(f"Using corpus key {self._vectara_corpus_key}")

        # identifies usage source for internal measurement
        self._x_source_str = x_source_str

        # setup requests session with max 3 retries and 90s timeout
        # for calling Vectara API
        self._session = requests.Session()
        if not vectara_verify_ssl:
            self._session.verify = False  # to ignore SSL verification
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self._session.mount("https://", adapter)
        self.vectara_api_timeout = 90
        self.doc_ids: List[str] = []

    def__del__(self) -> None:
"""Attempt to close the session when the object is garbage collected."""
        if hasattr(self, "_session") and self._session:
            self._session.close()
            self._session = None

    @lru_cache(maxsize=None)
    def_get_corpus_key(self, corpus_key: str) -> str:
"""
        Get the corpus key to use for the index.
        If corpus_key is provided, check if it is one of the valid corpus keys.
        If not, use the first corpus key in the list.
        """
        if corpus_key is not None:
            if corpus_key in self._vectara_corpus_key.split(","):
                return corpus_key
        return self._vectara_corpus_key.split(",")[0]

    def_get_post_headers(self) -> dict:
"""Returns headers that should be attached to each post request."""
        return {
            "x-api-key": self._vectara_api_key,
            "Content-Type": "application/json",
            "X-Source": self._x_source_str,
        }

    def_delete_doc(self, doc_id: str, corpus_key: Optional[str] = None) -> bool:
"""
        Delete a document from the Vectara corpus.

        Args:
            doc_id (str): ID of the document to delete.
            corpus_key (str): corpus key to delete the document from.

        Returns:
            bool: True if deletion was successful, False otherwise.

        """
        valid_corpus_key = self._get_corpus_key(corpus_key)
        body = {}
        response = self._session.delete(
            f"{self._base_url}/v2/corpora/{valid_corpus_key}/documents/{doc_id}",
            data=json.dumps(body),
            verify=True,
            headers=self._get_post_headers(),
            timeout=self.vectara_api_timeout,
        )

        if response.status_code != 204:
            _logger.error(
                f"Delete request failed for doc_id = {doc_id} with status code "
                f"{response.status_code}, text {response.json()['messages'][0]}"
            )
            return False
        return True

    def_index_doc(self, doc: dict, corpus_key) -> str:
        response = self._session.post(
            headers=self._get_post_headers(),
            url=f"{self._base_url}/v2/corpora/{corpus_key}/documents",
            data=json.dumps(doc),
            timeout=self.vectara_api_timeout,
            verify=True,
        )

        status_code = response.status_code
        if status_code == 201:
            return "E_SUCCEEDED"

        result = response.json()
        return result["messages"][0]

    def_insert(
        self,
        document: Optional[Document] = None,
        nodes: Optional[Sequence[Node]] = None,
        corpus_key: Optional[str] = None,
        **insert_kwargs: Any,
    ) -> None:
"""
        Insert a document into a corpus using Vectara's indexing API.

        Args:
            document (Document): a document to index using Vectara's Structured Document type.
            nodes (Sequence[Node]): a list of nodes representing document parts to index a document using Vectara's Core Document type.
            corpus_key (str): If multiple corpora are provided for this index, the corpus_key of the corpus you want to add the document to.

        """
        if document:
            # Use Structured Document type
            metadata = document.metadata.copy()
            metadata["framework"] = "llama_index"
            doc = {
                "id": document.id_,
                "type": "structured",
                "metadata": metadata,
                "sections": [{"text": document.text_resource.text}],
            }

            if "title" in insert_kwargs and insert_kwargs["title"]:
                doc["title"] = insert_kwargs["title"]

            if "description" in insert_kwargs and insert_kwargs["description"]:
                doc["description"] = insert_kwargs["description"]

            if (
                "max_chars_per_chunk" in insert_kwargs
                and insert_kwargs["max_chars_per_chunk"]
            ):
                doc["chunking_strategy"] = {
                    "type": "max_chars_chunking_strategy",
                    "max_chars_per_chunk": insert_kwargs["max_chars_per_chunk"],
                }

        elif nodes:
            # Use Core Document type
            metadata = insert_kwargs["doc_metadata"]
            metadata["framework"] = "llama_index"
            doc = {
                "id": insert_kwargs["doc_id"],
                "type": "core",
                "metadata": metadata,
                "document_parts": [
                    {"text": node.text_resource.text, "metadata": node.metadata}
                    for node in nodes
                ],
            }

        else:
            _logger.error(
                "Error indexing document. Must provide either a document or a list of nodes."
            )
            return

        valid_corpus_key = self._get_corpus_key(corpus_key)
        if self.parallelize_ingest:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(self._index_doc, doc, valid_corpus_key)
                ecode = future.result()
                if ecode != "E_SUCCEEDED":
                    _logger.error(
                        f"Error indexing document in Vectara with error code {ecode}"
                    )
            self.doc_ids.append(doc["id"])
        else:
            ecode = self._index_doc(doc, valid_corpus_key)
            if ecode != "E_SUCCEEDED":
                _logger.error(
                    f"Error indexing document in Vectara with error code {ecode}"
                )
            self.doc_ids.append(doc["id"])

    defadd_document(
        self,
        doc: Document,
        corpus_key: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        max_chars_per_chunk: Optional[int] = None,
    ) -> None:
"""
        Indexes a document into a corpus using the Vectara Structured Document format.

        Full API Docs: https://docs.vectara.com/docs/api-reference/indexing-apis/indexing#structured-document-object-definition

        Args:
            doc (Document): The document object to be indexed.
                You should provide the value you want for the document id in the corpus as the id_ member of this object.
                You should provide any document_metadata in the metadata member of this object.
            corpus_key (str): If multiple corpora are provided for this index, the corpus_key of the corpus you want to add the document to.
            title (str): The title of the document.
            description (str): The description of the document.
            max_chars_per_chunk (int): The maximum number of characters per chunk.

        """
        self._insert(
            document=doc,
            corpus_key=corpus_key,
            title=title,
            description=description,
            max_chars_per_chunk=max_chars_per_chunk,
        )

    defadd_nodes(
        self,
        nodes: Sequence[Node],
        document_id: str,
        document_metadata: Optional[Dict] = {},
        corpus_key: Optional[str] = None,
    ) -> None:
"""
        Indexes a document into a corpus using the Vectara Core Document format.

        Full API Docs: https://docs.vectara.com/docs/api-reference/indexing-apis/indexing#core-document-object-definition

        Args:
            nodes (Sequence[Node]): The user-specified document parts.
                You should provide any part_metadata in the metadata member of each node.
            document_id (str): The document id (must be unique for the corpus).
            document_metadata (Dict): The document_metadata to be associated with this document.
            corpus_key (str): If multiple corpora are provided for this index, the corpus_key of the corpus you want to add the document to.

        """
        self._insert(
            nodes=nodes,
            corpus_key=corpus_key,
            doc_id=document_id,
            doc_metadata=document_metadata,
        )

    definsert_file(
        self,
        file_path: str,
        metadata: Optional[dict] = None,
        chunking_strategy: Optional[dict] = None,
        enable_table_extraction: Optional[bool] = False,
        filename: Optional[str] = None,
        corpus_key: Optional[str] = None,
        **insert_kwargs: Any,
    ) -> Optional[str]:
"""
        Vectara provides a way to add files (binary or text) directly via our API
        where pre-processing and chunking occurs internally in an optimal way
        This method provides a way to use that API in Llama_index.

        # ruff: noqa: E501
        Full API Docs: https://docs.vectara.com/docs/rest-api/upload-file

        Args:
            file_path: local file path
                Files could be text, HTML, PDF, markdown, doc/docx, ppt/pptx, etc.
                see API docs for full list
            metadata: Optional dict of metadata associated with the file
            chunking_strategy: Optional dict specifying max number of characters per chunk
            enable_table_extraction: Optional bool specifying whether or not to extract tables from document
            filename: Optional string specifying the filename


        Returns:
            List of ids associated with each of the files indexed

        """
        if not os.path.exists(file_path):
            _logger.error(f"File {file_path} does not exist")
            return None

        if filename is None:
            filename = file_path.split("/")[-1]

        files = {"file": (filename, open(file_path, "rb"))}

        if metadata:
            metadata["framework"] = "llama_index"
            files["metadata"] = (None, json.dumps(metadata), "application/json")

        if chunking_strategy:
            files["chunking_strategy"] = (
                None,
                json.dumps(chunking_strategy),
                "application/json",
            )

        if enable_table_extraction:
            files["table_extraction_config"] = (
                None,
                json.dumps({"extract_tables": enable_table_extraction}),
                "application/json",
            )

        headers = self._get_post_headers()
        headers.pop("Content-Type")
        valid_corpus_key = self._get_corpus_key(corpus_key)
        response = self._session.post(
            f"{self._base_url}/v2/corpora/{valid_corpus_key}/upload_file",
            files=files,
            verify=True,
            headers=headers,
            timeout=self.vectara_api_timeout,
        )

        res = response.json()
        if response.status_code == 201:
            doc_id = res["id"]
            self.doc_ids.append(doc_id)
            return doc_id
        elif response.status_code == 400:
            _logger.info(f"File upload failed with error message {res['field_errors']}")
            return None
        else:
            _logger.info(f"File upload failed with error message {res['messages'][0]}")
            return None

    defdelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = True, **delete_kwargs: Any
    ) -> None:
"""
        Delete a document from a Vectara corpus.

        Args:
            ref_doc_id (str): ID of the document to delete
            delete_from_docstore (bool): Whether to delete the document from the corpus.
                If False, no change is made to the index or corpus.
            corpus_key (str): corpus key to delete the document from.
                This should be specified if there are multiple corpora in the index.

        """
        if delete_from_docstore:
            if "corpus_key" in delete_kwargs:
                self._delete_doc(
                    doc_id=ref_doc_id, corpus_key=delete_kwargs["corpus_key"]
                )
            else:
                self._delete_doc(doc_id=ref_doc_id)

    defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""
        Update a document's metadata in a Vectara corpus.

        Args:
            document (Document): The document to update.
                Make sure to include id_ argument for proper identification within the corpus.
            corpus_key (str): corpus key to modify the document from.
                This should be specified if there are multiple corpora in the index.
            metadata (dict): dictionary specifying any modifications or additions to the document's metadata.

        """
        if "metadata" in update_kwargs:
            if "corpus_key" in update_kwargs:
                valid_corpus_key = self._get_corpus_key(update_kwargs["corpus_key"])
            else:
                valid_corpus_key = self._get_corpus_key(corpus_key=None)

            doc_id = document.doc_id
            body = {"metadata": update_kwargs["metadata"]}
            response = self._session.patch(
                f"{self._base_url}/v2/corpora/{valid_corpus_key}/documents/{doc_id}",
                data=json.dumps(body),
                verify=True,
                headers=self._get_post_headers(),
                timeout=self.vectara_api_timeout,
            )

            if response.status_code != 200:
                _logger.error(
                    f"Update request failed for doc_id = {doc_id} with status code "
                    f"{response.status_code}, text {response.json()['messages'][0]}"
                )

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Return a Retriever for this managed index."""
        fromllama_index.indices.managed.vectara.retrieverimport (
            VectaraRetriever,
        )

        return VectaraRetriever(self, **kwargs)

    defas_chat_engine(self, **kwargs: Any) -> BaseChatEngine:
        kwargs["summary_enabled"] = True
        retriever = self.as_retriever(**kwargs)
        kwargs.pop("summary_enabled")
        fromllama_index.indices.managed.vectara.queryimport (
            VectaraChatEngine,
        )

        return VectaraChatEngine.from_args(retriever, **kwargs)  # type: ignore

    defas_query_engine(
        self, llm: Optional[LLMType] = None, **kwargs: Any
    ) -> BaseQueryEngine:
        if kwargs.get("summary_enabled", True):
            fromllama_index.indices.managed.vectara.queryimport (
                VectaraQueryEngine,
            )

            kwargs["summary_enabled"] = True
            retriever = self.as_retriever(**kwargs)
            return VectaraQueryEngine.from_args(retriever=retriever, **kwargs)  # type: ignore
        else:
            fromllama_index.core.query_engine.retriever_query_engineimport (
                RetrieverQueryEngine,
            )

            llm = (
                resolve_llm(llm, callback_manager=self._callback_manager)
                or Settings.llm
            )

            retriever = self.as_retriever(**kwargs)
            response_synthesizer = get_response_synthesizer(
                response_mode=ResponseMode.COMPACT,
                llm=llm,
            )
            return RetrieverQueryEngine.from_args(
                retriever=retriever,
                response_synthesizer=response_synthesizer,
                **kwargs,
            )

    @classmethod
    deffrom_documents(
        cls: Type[IndexType],
        documents: Sequence[Document],
        show_progress: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        transformations: Optional[List[TransformComponent]] = None,
        **kwargs: Any,
    ) -> IndexType:
"""Build a Vectara index from a sequence of documents."""
        index = cls(
            show_progress=show_progress,
            **kwargs,
        )

        for doc in documents:
            index.add_document(doc)

        return index

```
 |  
| --- | --- |  
###  add_document [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraIndex.add_document "Permanent link")

```
add_document(
    doc: ,
    corpus_key: Optional[] = None,
    title: Optional[] = None,
    description: Optional[] = None,
    max_chars_per_chunk: Optional[] = None,
) -> None

```

Indexes a document into a corpus using the Vectara Structured Document format.
Full API Docs: https://docs.vectara.com/docs/api-reference/indexing-apis/indexing#structured-document-object-definition
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `doc`  |   |  The document object to be indexed. You should provide the value you want for the document id in the corpus as the id_ member of this object. You should provide any document_metadata in the metadata member of this object.  |  _required_  |  
|  `corpus_key`  |  If multiple corpora are provided for this index, the corpus_key of the corpus you want to add the document to.  |  `None`  |  
|  `title`  |  The title of the document.  |  `None`  |  
|  `description`  |  The description of the document.  |  `None`  |  
|  `max_chars_per_chunk`  |  The maximum number of characters per chunk.  |  `None`  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/base.py`  
| 
```
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
```
 | 
```
defadd_document(
    self,
    doc: Document,
    corpus_key: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    max_chars_per_chunk: Optional[int] = None,
) -> None:
"""
    Indexes a document into a corpus using the Vectara Structured Document format.

    Full API Docs: https://docs.vectara.com/docs/api-reference/indexing-apis/indexing#structured-document-object-definition

    Args:
        doc (Document): The document object to be indexed.
            You should provide the value you want for the document id in the corpus as the id_ member of this object.
            You should provide any document_metadata in the metadata member of this object.
        corpus_key (str): If multiple corpora are provided for this index, the corpus_key of the corpus you want to add the document to.
        title (str): The title of the document.
        description (str): The description of the document.
        max_chars_per_chunk (int): The maximum number of characters per chunk.

    """
    self._insert(
        document=doc,
        corpus_key=corpus_key,
        title=title,
        description=description,
        max_chars_per_chunk=max_chars_per_chunk,
    )

```
 |  
| --- | --- |  
###  add_nodes [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraIndex.add_nodes "Permanent link")

```
add_nodes(
    nodes: Sequence[],
    document_id: ,
    document_metadata: Optional[] = {},
    corpus_key: Optional[] = None,
) -> None

```

Indexes a document into a corpus using the Vectara Core Document format.
Full API Docs: https://docs.vectara.com/docs/api-reference/indexing-apis/indexing#core-document-object-definition
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[Node[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Node "Node \(llama_index.core.schema.Node\)")]`  |  The user-specified document parts. You should provide any part_metadata in the metadata member of each node.  |  _required_  |  
|  `document_id`  |  The document id (must be unique for the corpus).  |  _required_  |  
|  `document_metadata`  |  `Dict`  |  The document_metadata to be associated with this document.  |  
|  `corpus_key`  |  If multiple corpora are provided for this index, the corpus_key of the corpus you want to add the document to.  |  `None`  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/base.py`  
| 
```
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
```
 | 
```
defadd_nodes(
    self,
    nodes: Sequence[Node],
    document_id: str,
    document_metadata: Optional[Dict] = {},
    corpus_key: Optional[str] = None,
) -> None:
"""
    Indexes a document into a corpus using the Vectara Core Document format.

    Full API Docs: https://docs.vectara.com/docs/api-reference/indexing-apis/indexing#core-document-object-definition

    Args:
        nodes (Sequence[Node]): The user-specified document parts.
            You should provide any part_metadata in the metadata member of each node.
        document_id (str): The document id (must be unique for the corpus).
        document_metadata (Dict): The document_metadata to be associated with this document.
        corpus_key (str): If multiple corpora are provided for this index, the corpus_key of the corpus you want to add the document to.

    """
    self._insert(
        nodes=nodes,
        corpus_key=corpus_key,
        doc_id=document_id,
        doc_metadata=document_metadata,
    )

```
 |  
| --- | --- |  
###  insert_file [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraIndex.insert_file "Permanent link")

```
insert_file(
    file_path: ,
    metadata: Optional[] = None,
    chunking_strategy: Optional[] = None,
    enable_table_extraction: Optional[] = False,
    filename: Optional[] = None,
    corpus_key: Optional[] = None,
    **insert_kwargs: 
) -> Optional[]

```

Vectara provides a way to add files (binary or text) directly via our API where pre-processing and chunking occurs internally in an optimal way This method provides a way to use that API in Llama_index.
#### ruff: noqa: E501[#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraIndex.insert_file--ruff-noqa-e501 "Permanent link")
Full API Docs: https://docs.vectara.com/docs/rest-api/upload-file
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_path`  |  local file path Files could be text, HTML, PDF, markdown, doc/docx, ppt/pptx, etc. see API docs for full list  |  _required_  |  
|  `metadata`  |  `Optional[dict]`  |  Optional dict of metadata associated with the file  |  `None`  |  
|  `chunking_strategy`  |  `Optional[dict]`  |  Optional dict specifying max number of characters per chunk  |  `None`  |  
|  `enable_table_extraction`  |  `Optional[bool]`  |  Optional bool specifying whether or not to extract tables from document  |  `False`  |  
|  `filename`  |  `Optional[str]`  |  Optional string specifying the filename  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Optional[str]`  |  List of ids associated with each of the files indexed  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/base.py`  
| 
```
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
```
 | 
```
definsert_file(
    self,
    file_path: str,
    metadata: Optional[dict] = None,
    chunking_strategy: Optional[dict] = None,
    enable_table_extraction: Optional[bool] = False,
    filename: Optional[str] = None,
    corpus_key: Optional[str] = None,
    **insert_kwargs: Any,
) -> Optional[str]:
"""
    Vectara provides a way to add files (binary or text) directly via our API
    where pre-processing and chunking occurs internally in an optimal way
    This method provides a way to use that API in Llama_index.

    # ruff: noqa: E501
    Full API Docs: https://docs.vectara.com/docs/rest-api/upload-file

    Args:
        file_path: local file path
            Files could be text, HTML, PDF, markdown, doc/docx, ppt/pptx, etc.
            see API docs for full list
        metadata: Optional dict of metadata associated with the file
        chunking_strategy: Optional dict specifying max number of characters per chunk
        enable_table_extraction: Optional bool specifying whether or not to extract tables from document
        filename: Optional string specifying the filename


    Returns:
        List of ids associated with each of the files indexed

    """
    if not os.path.exists(file_path):
        _logger.error(f"File {file_path} does not exist")
        return None

    if filename is None:
        filename = file_path.split("/")[-1]

    files = {"file": (filename, open(file_path, "rb"))}

    if metadata:
        metadata["framework"] = "llama_index"
        files["metadata"] = (None, json.dumps(metadata), "application/json")

    if chunking_strategy:
        files["chunking_strategy"] = (
            None,
            json.dumps(chunking_strategy),
            "application/json",
        )

    if enable_table_extraction:
        files["table_extraction_config"] = (
            None,
            json.dumps({"extract_tables": enable_table_extraction}),
            "application/json",
        )

    headers = self._get_post_headers()
    headers.pop("Content-Type")
    valid_corpus_key = self._get_corpus_key(corpus_key)
    response = self._session.post(
        f"{self._base_url}/v2/corpora/{valid_corpus_key}/upload_file",
        files=files,
        verify=True,
        headers=headers,
        timeout=self.vectara_api_timeout,
    )

    res = response.json()
    if response.status_code == 201:
        doc_id = res["id"]
        self.doc_ids.append(doc_id)
        return doc_id
    elif response.status_code == 400:
        _logger.info(f"File upload failed with error message {res['field_errors']}")
        return None
    else:
        _logger.info(f"File upload failed with error message {res['messages'][0]}")
        return None

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = True,
    **delete_kwargs: 
) -> None

```

Delete a document from a Vectara corpus.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  ID of the document to delete  |  _required_  |  
|  `delete_from_docstore`  |  `bool`  |  Whether to delete the document from the corpus. If False, no change is made to the index or corpus.  |  `True`  |  
|  `corpus_key`  |  corpus key to delete the document from. This should be specified if there are multiple corpora in the index.  |  _required_  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/base.py`  
| 
```
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
```
 | 
```
defdelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = True, **delete_kwargs: Any
) -> None:
"""
    Delete a document from a Vectara corpus.

    Args:
        ref_doc_id (str): ID of the document to delete
        delete_from_docstore (bool): Whether to delete the document from the corpus.
            If False, no change is made to the index or corpus.
        corpus_key (str): corpus key to delete the document from.
            This should be specified if there are multiple corpora in the index.

    """
    if delete_from_docstore:
        if "corpus_key" in delete_kwargs:
            self._delete_doc(
                doc_id=ref_doc_id, corpus_key=delete_kwargs["corpus_key"]
            )
        else:
            self._delete_doc(doc_id=ref_doc_id)

```
 |  
| --- | --- |  
###  update_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraIndex.update_ref_doc "Permanent link")

```
update_ref_doc(
    document: , **update_kwargs: 
) -> None

```

Update a document's metadata in a Vectara corpus.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `document`  |   |  The document to update. Make sure to include id_ argument for proper identification within the corpus.  |  _required_  |  
|  `corpus_key`  |  corpus key to modify the document from. This should be specified if there are multiple corpora in the index.  |  _required_  |  
|  `metadata`  |  `dict`  |  dictionary specifying any modifications or additions to the document's metadata.  |  _required_  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/base.py`  
| 
```
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
```
 | 
```
defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""
    Update a document's metadata in a Vectara corpus.

    Args:
        document (Document): The document to update.
            Make sure to include id_ argument for proper identification within the corpus.
        corpus_key (str): corpus key to modify the document from.
            This should be specified if there are multiple corpora in the index.
        metadata (dict): dictionary specifying any modifications or additions to the document's metadata.

    """
    if "metadata" in update_kwargs:
        if "corpus_key" in update_kwargs:
            valid_corpus_key = self._get_corpus_key(update_kwargs["corpus_key"])
        else:
            valid_corpus_key = self._get_corpus_key(corpus_key=None)

        doc_id = document.doc_id
        body = {"metadata": update_kwargs["metadata"]}
        response = self._session.patch(
            f"{self._base_url}/v2/corpora/{valid_corpus_key}/documents/{doc_id}",
            data=json.dumps(body),
            verify=True,
            headers=self._get_post_headers(),
            timeout=self.vectara_api_timeout,
        )

        if response.status_code != 200:
            _logger.error(
                f"Update request failed for doc_id = {doc_id} with status code "
                f"{response.status_code}, text {response.json()['messages'][0]}"
            )

```
 |  
| --- | --- |  
###  as_retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraIndex.as_retriever "Permanent link")

```
as_retriever(**kwargs: ) -> 

```

Return a Retriever for this managed index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/base.py`  
| 
```
461
462
463
464
465
466
467
```
 | 
```
defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Return a Retriever for this managed index."""
    fromllama_index.indices.managed.vectara.retrieverimport (
        VectaraRetriever,
    )

    return VectaraRetriever(self, **kwargs)

```
 |  
| --- | --- |  
###  from_documents `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraIndex.from_documents "Permanent link")

```
from_documents(
    documents: Sequence[],
    show_progress:  = False,
    callback_manager: Optional[] = None,
    transformations: Optional[
        []
    ] = None,
    **kwargs: 
) -> IndexType

```

Build a Vectara index from a sequence of documents.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/base.py`  
| 
```
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
```
 | 
```
@classmethod
deffrom_documents(
    cls: Type[IndexType],
    documents: Sequence[Document],
    show_progress: bool = False,
    callback_manager: Optional[CallbackManager] = None,
    transformations: Optional[List[TransformComponent]] = None,
    **kwargs: Any,
) -> IndexType:
"""Build a Vectara index from a sequence of documents."""
    index = cls(
        show_progress=show_progress,
        **kwargs,
    )

    for doc in documents:
        index.add_document(doc)

    return index

```
 |  
| --- | --- |  
##  VectaraAutoRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraAutoRetriever "Permanent link")
Bases: 
Managed Index auto retriever.
A retriever for a Vectara index that uses an LLM to automatically set filtering query parameters. Based on VectorStoreAutoRetriever, and uses some of the vector_store types that are associated with auto retrieval.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  Vectara Index instance  |  _required_  |  
|  `vector_store_info`  |   |  additional information about vector store content and supported metadata filters. The natural language description is used by an LLM to automatically set vector store query parameters.  |  _required_  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/retriever.py`  
| 
```
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
```
 | 
```
classVectaraAutoRetriever(VectorIndexAutoRetriever):
"""
    Managed Index auto retriever.

    A retriever for a Vectara index that uses an LLM to automatically set
    filtering query parameters.
    Based on VectorStoreAutoRetriever, and uses some of the vector_store
    types that are associated with auto retrieval.

    Args:
        index (VectaraIndex): Vectara Index instance
        vector_store_info (VectorStoreInfo): additional information about
            vector store content and supported metadata filters. The natural language
            description is used by an LLM to automatically set vector store query
            parameters.
        Other variables are the same as VectorStoreAutoRetriever or VectaraRetriever

    """

    def__init__(
        self,
        index: VectaraIndex,
        vector_store_info: VectorStoreInfo,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            index,
            vector_store_info,
            prompt_template_str=DEFAULT_VECTARA_QUERY_PROMPT_TMPL,
            **kwargs,
        )  # type: ignore
        self._index = index  # type: ignore
        self._kwargs = kwargs
        self._verbose = self._kwargs.get("verbose", False)
        self._explicit_filter = self._kwargs.pop("filter", "")

    def_build_retriever_from_spec(
        self, spec: VectorStoreQuerySpec
    ) -> Tuple[VectaraRetriever, QueryBundle]:
        query_bundle = self._get_query_bundle(spec.query)

        filter_list = [
            (filter.key, filter.operator.value, filter.value) for filter in spec.filters
        ]
        if self._verbose:
            print(f"Using query str: {spec.query}")
            print(f"Using implicit filters: {filter_list}")

        # create filter string from implicit filters
        if len(spec.filters) == 0:
            filter_str = ""
        else:
            filters = MetadataFilters(
                filters=[*spec.filters, *self._extra_filters.filters]
            )
            condition = " and " if filters.condition == FilterCondition.AND else " or "
            filter_str = condition.join(
                [
                    f"(doc.{f.key}{f.operator.value} '{f.value}')"
                    for f in filters.filters
                ]
            )

        # add explicit filter if specified
        if self._explicit_filter:
            if len(filter_str)  0:
                filter_str = f"({filter_str}) and ({self._explicit_filter})"
            else:
                filter_str = self._explicit_filter

        if self._verbose:
            print(f"final filter string: {filter_str}")

        return (
            VectaraRetriever(
                index=self._index,  # type: ignore
                filter=filter_str,
                **self._kwargs,
            ),
            query_bundle,
        )

    def_vectara_query(
        self,
        query_bundle: QueryBundle,
        **kwargs: Any,
    ) -> Tuple[List[NodeWithScore], str]:
        spec = self.generate_retrieval_spec(query_bundle)
        vectara_retriever, new_query = self._build_retriever_from_spec(
            VectorStoreQuerySpec(
                query=spec.query, filters=spec.filters, top_k=self._similarity_top_k
            )
        )
        return vectara_retriever._vectara_query(new_query, **kwargs)

```
 |  
| --- | --- |  
##  VectaraRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraRetriever "Permanent link")
Bases: 
Vectara Retriever.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  the Vectara Index  |  _required_  |  
|  `similarity_top_k`  |  number of top k results to return, defaults to 5.  |  
|  `offset`  |  number of results to skip, defaults to 0.  |  
|  `lambda_val`  |  `Union[List[float], float]`  |  for hybrid search. 0 = neural search only. 1 = keyword match only. In between values are a linear interpolation. Provide single value for one corpus or a list of values for each corpus.  |  `0.005`  |  
|  `semantics`  |  `Union[List[str], str]`  |  Indicates whether the query is intended as a query or response. Provide single value for one corpus or a list of values for each corpus.  |  `'default'`  |  
|  `custom_dimensions`  |  `Dict`  |  Custom dimensions for the query. See (https://docs.vectara.com/docs/learn/semantic-search/add-custom-dimensions) for more details about usage. Provide single dict for one corpus or a list of dicts for each corpus.  |  
|  `n_sentences_before`  |  number of sentences before the matched sentence to return in the node  |  
|  `n_sentences_after`  |  number of sentences after the matched sentence to return in the node  |  
|  `filter`  |  `Union[List[str], str]`  |  metadata filter (if specified). Provide single string for one corpus or a list of strings to specify the filter for each corpus (if multiple corpora).  |  
|  `reranker`  |  reranker to use: none, mmr, slingshot/multilingual_reranker_v1, userfn, or chain.  |  
|  `rerank_k`  |  number of results to fetch for Reranking, defaults to 50.  |  
|  `rerank_limit`  |  maximum number of results to return after reranking, defaults to 50. Don't specify this for chain reranking. Instead, put the "limit" parameter in the dict for each individual reranker.  |  `None`  |  
|  `rerank_cutoff`  |  `float`  |  minimum score threshold for results to include after reranking, defaults to 0. Don't specify this for chain reranking. Instead, put the "chain" parameter in the dict for each individual reranker.  |  `None`  |  
|  `mmr_diversity_bias`  |  `float`  |  number between 0 and 1 that determines the degree of diversity among the results with 0 corresponding to minimum diversity and 1 to maximum diversity. Defaults to 0.3.  |  `0.3`  |  
|  `udf_expression`  |  the user defined expression for reranking results. See (https://docs.vectara.com/docs/learn/user-defined-function-reranker) for more details about syntax for udf reranker expressions.  |  `None`  |  
|  `rerank_chain`  |  `List[Dict]`  |  a list of rerankers to be applied in a sequence and their associated parameters for the chain reranker. Each element should specify the "type" of reranker (mmr, slingshot, userfn) and any other parameters (e.g. "limit" or "cutoff" for any type, "diversity_bias" for mmr, and "user_function" for userfn). If using slingshot/multilingual_reranker_v1, it must be first in the list.  |  `None`  |  
|  `summary_enabled`  |  `bool`  |  whether to generate summaries or not. Defaults to False.  |  `False`  |  
|  `summary_response_lang`  |  language to use for summary generation.  |  `'eng'`  |  
|  `summary_num_results`  |  number of results to use for summary generation.  |  
|  `summary_prompt_name`  |  name of the prompt to use for summary generation. To use Vectara's Mockingbird LLM designed specifically for RAG, set to "mockingbird-1.0-2024-07-16". If you are indexing documents with tables, we recommend "vectara-summary-table-query-ext-dec-2024-gpt-4o". See (https://docs.vectara.com/docs/learn/grounded-generation/select-a-summarizer) for all available prompts.  |  `'vectara-summary-ext-24-05-med-omni'`  |  
|  `prompt_text`  |  the custom prompt, using appropriate prompt variables and functions. See (https://docs.vectara.com/docs/1.0/prompts/custom-prompts-with-metadata) for more details.  |  `None`  |  
|  `max_response_chars`  |  the desired maximum number of characters for the generated summary.  |  `None`  |  
|  `max_tokens`  |  the maximum number of tokens to be returned by the LLM.  |  `None`  |  
|  `temperature`  |  `float`  |  The sampling temperature; higher values lead to more randomness.  |  `None`  |  
|  `frequency_penalty`  |  `float`  |  How much to penalize repeating tokens in the response, reducing likelihood of repeating the same line.  |  `None`  |  
|  `presence_penalty`  |  `float`  |  How much to penalize repeating tokens in the response, increasing the diversity of topics.  |  `None`  |  
|  `citations_style`  |  The style of the citations in the summary generation, either "numeric", "html", "markdown", or "none". Defaults to None.  |  `None`  |  
|  `citations_url_pattern`  |  URL pattern for html and markdown citations. If non-empty, specifies the URL pattern to use for citations; e.g. "{doc.url}". See (https://docs.vectara.com/docs/api-reference/search-apis/search #citation-format-in-summary) for more details. Defaults to None.  |  `None`  |  
|  `citations_text_pattern`  |  The displayed text for citations. If not specified, numeric citations are displayed for text.  |  `None`  |  
|  `save_history`  |  `bool`  |  Whether to save the query in history. Defaults to False.  |  `False`  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/retriever.py`  
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
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
```
 | 
```
classVectaraRetriever(BaseRetriever):
"""
    Vectara Retriever.

    Args:
        index (VectaraIndex): the Vectara Index
        similarity_top_k (int): number of top k results to return, defaults to 5.
        offset (int): number of results to skip, defaults to 0.
        lambda_val (Union[List[float], float]): for hybrid search.
            0 = neural search only.
            1 = keyword match only.
            In between values are a linear interpolation.
            Provide single value for one corpus or a list of values for each corpus.
        semantics (Union[List[str], str]): Indicates whether the query is intended as a query or response.
            Provide single value for one corpus or a list of values for each corpus.
        custom_dimensions (Dict): Custom dimensions for the query.
            See (https://docs.vectara.com/docs/learn/semantic-search/add-custom-dimensions)
            for more details about usage.
            Provide single dict for one corpus or a list of dicts for each corpus.
        n_sentences_before (int):
            number of sentences before the matched sentence to return in the node
        n_sentences_after (int):
            number of sentences after the matched sentence to return in the node
        filter (Union[List[str], str]): metadata filter (if specified). Provide single string for one corpus
            or a list of strings to specify the filter for each corpus (if multiple corpora).
        reranker (str): reranker to use: none, mmr, slingshot/multilingual_reranker_v1, userfn, or chain.
        rerank_k (int): number of results to fetch for Reranking, defaults to 50.
        rerank_limit (int): maximum number of results to return after reranking, defaults to 50.
            Don't specify this for chain reranking. Instead, put the "limit" parameter in the dict for each individual reranker.
        rerank_cutoff (float): minimum score threshold for results to include after reranking, defaults to 0.
            Don't specify this for chain reranking. Instead, put the "chain" parameter in the dict for each individual reranker.
        mmr_diversity_bias (float): number between 0 and 1 that determines the degree
            of diversity among the results with 0 corresponding
            to minimum diversity and 1 to maximum diversity.
            Defaults to 0.3.
        udf_expression (str): the user defined expression for reranking results.
            See (https://docs.vectara.com/docs/learn/user-defined-function-reranker)
            for more details about syntax for udf reranker expressions.
        rerank_chain (List[Dict]): a list of rerankers to be applied in a sequence and their associated parameters
            for the chain reranker. Each element should specify the "type" of reranker (mmr, slingshot, userfn)
            and any other parameters (e.g. "limit" or "cutoff" for any type,  "diversity_bias" for mmr, and "user_function" for userfn).
            If using slingshot/multilingual_reranker_v1, it must be first in the list.
        summary_enabled (bool): whether to generate summaries or not. Defaults to False.
        summary_response_lang (str): language to use for summary generation.
        summary_num_results (int): number of results to use for summary generation.
        summary_prompt_name (str): name of the prompt to use for summary generation.
            To use Vectara's Mockingbird LLM designed specifically for RAG, set to "mockingbird-1.0-2024-07-16".
            If you are indexing documents with tables, we recommend "vectara-summary-table-query-ext-dec-2024-gpt-4o".
            See (https://docs.vectara.com/docs/learn/grounded-generation/select-a-summarizer) for all available prompts.
        prompt_text (str): the custom prompt, using appropriate prompt variables and functions.
            See (https://docs.vectara.com/docs/1.0/prompts/custom-prompts-with-metadata)
            for more details.
        max_response_chars (int): the desired maximum number of characters for the generated summary.
        max_tokens (int): the maximum number of tokens to be returned by the LLM.
        temperature (float): The sampling temperature; higher values lead to more randomness.
        frequency_penalty (float): How much to penalize repeating tokens in the response, reducing likelihood of repeating the same line.
        presence_penalty (float): How much to penalize repeating tokens in the response, increasing the diversity of topics.
        citations_style (str): The style of the citations in the summary generation,
            either "numeric", "html", "markdown", or "none". Defaults to None.
        citations_url_pattern (str): URL pattern for html and markdown citations.
            If non-empty, specifies the URL pattern to use for citations; e.g. "{doc.url}".
            See (https://docs.vectara.com/docs/api-reference/search-apis/search
                 #citation-format-in-summary) for more details. Defaults to None.
        citations_text_pattern (str): The displayed text for citations.
            If not specified, numeric citations are displayed for text.
        save_history (bool): Whether to save the query in history. Defaults to False.

    """

    def__init__(
        self,
        index: VectaraIndex,
        similarity_top_k: int = 10,
        offset: int = 0,
        lambda_val: Union[List[float], float] = 0.005,
        semantics: Union[List[str], str] = "default",
        custom_dimensions: Union[List[Dict], Dict] = {},
        n_sentences_before: int = 2,
        n_sentences_after: int = 2,
        filter: Union[List[str], str] = "",
        reranker: VectaraReranker = VectaraReranker.NONE,
        rerank_k: int = 50,
        rerank_limit: Optional[int] = None,
        rerank_cutoff: Optional[float] = None,
        mmr_diversity_bias: float = 0.3,
        udf_expression: str = None,
        rerank_chain: List[Dict] = None,
        summary_enabled: bool = False,
        summary_response_lang: str = "eng",
        summary_num_results: int = 7,
        summary_prompt_name: str = "vectara-summary-ext-24-05-med-omni",
        prompt_text: Optional[str] = None,
        max_response_chars: Optional[int] = None,
        max_tokens: Optional[int] = None,
        llm_name: Optional[str] = None,
        temperature: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        citations_style: Optional[str] = None,
        citations_url_pattern: Optional[str] = None,
        citations_text_pattern: Optional[str] = None,
        save_history: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        x_source_str: str = "llama_index",
        **kwargs: Any,
    ) -> None:
"""Initialize params."""
        self._index = index
        self._similarity_top_k = similarity_top_k
        self._offset = offset
        self._lambda_val = lambda_val
        self._semantics = semantics
        self._custom_dimensions = custom_dimensions
        self._n_sentences_before = n_sentences_before
        self._n_sentences_after = n_sentences_after
        self._filter = filter
        self._citations_style = citations_style
        self._citations_url_pattern = citations_url_pattern
        self._citations_text_pattern = citations_text_pattern
        self._save_history = save_history

        self._conv_id = None
        self._x_source_str = x_source_str

        if reranker in [
            VectaraReranker.MMR,
            VectaraReranker.SLINGSHOT,
            VectaraReranker.SLINGSHOT_ALT_NAME,
            VectaraReranker.UDF,
            VectaraReranker.CHAIN,
            VectaraReranker.NONE,
        ]:
            self._rerank = True
            self._reranker = reranker
            self._rerank_k = rerank_k
            self._rerank_limit = rerank_limit
            self._rerank_cutoff = rerank_cutoff

            if self._reranker == VectaraReranker.MMR:
                self._mmr_diversity_bias = mmr_diversity_bias

            elif self._reranker == VectaraReranker.UDF:
                self._udf_expression = udf_expression

            elif self._reranker == VectaraReranker.CHAIN:
                self._rerank_chain = rerank_chain
                for sub_reranker in self._rerank_chain:
                    if sub_reranker["type"] in [
                        VectaraReranker.SLINGSHOT,
                        VectaraReranker.SLINGSHOT_ALT_NAME,
                    ]:
                        sub_reranker["type"] = "customer_reranker"
                        sub_reranker["reranker_name"] = "Rerank_Multilingual_v1"

        else:
            self._rerank = False

        if summary_enabled:
            self._summary_enabled = True
            self._summary_response_lang = summary_response_lang
            self._summary_num_results = summary_num_results
            self._summary_prompt_name = summary_prompt_name
            self._prompt_text = prompt_text
            self._max_response_chars = max_response_chars
            self._max_tokens = max_tokens
            self._llm_name = llm_name
            self._temperature = temperature
            self._frequency_penalty = frequency_penalty
            self._presence_penalty = presence_penalty

        else:
            self._summary_enabled = False
        super().__init__(callback_manager)

    def_get_post_headers(self) -> dict:
"""Returns headers that should be attached to each post request."""
        return {
            "x-api-key": self._index._vectara_api_key,
            "Content-Type": "application/json",
            "X-Source": self._x_source_str,
        }

    @property
    defsimilarity_top_k(self) -> int:
"""Return similarity top k."""
        return self._similarity_top_k

    @similarity_top_k.setter
    defsimilarity_top_k(self, similarity_top_k: int) -> None:
"""Set similarity top k."""
        self._similarity_top_k = similarity_top_k

    def_retrieve(
        self,
        query_bundle: QueryBundle,
        **kwargs: Any,
    ) -> List[NodeWithScore]:
"""
        Retrieve top k most similar nodes.

        Args:
            query_bundle: Query Bundle

        """
        return self._vectara_query(query_bundle, **kwargs)[0]  # return top_nodes only

    def_build_vectara_query_body(
        self,
        query_str: str,
        **kwargs: Any,
    ) -> Dict:
        data = {
            "query": query_str,
            "search": {
                "offset": self._offset,
                "limit": self._rerank_k if self._rerank else self._similarity_top_k,
                "context_configuration": {
                    "sentences_before": self._n_sentences_before,
                    "sentences_after": self._n_sentences_after,
                },
            },
        }

        corpora_config = [
            {"corpus_key": corpus_key}
            for corpus_key in self._index._vectara_corpus_key.split(",")
        ]

        for i in range(len(corpora_config)):
            corpora_config[i]["custom_dimensions"] = (
                self._custom_dimensions[i]
                if isinstance(self._custom_dimensions, list)
                else self._custom_dimensions
            )
            corpora_config[i]["metadata_filter"] = (
                self._filter[i] if isinstance(self._filter, list) else self._filter
            )
            corpora_config[i]["lexical_interpolation"] = (
                self._lambda_val[i]
                if isinstance(self._lambda_val, list)
                else self._lambda_val
            )
            corpora_config[i]["semantics"] = (
                self._semantics[i]
                if isinstance(self._semantics, list)
                else self._semantics
            )

        data["search"]["corpora"] = corpora_config

        if self._rerank:
            rerank_config = {}

            if self._reranker in [
                VectaraReranker.SLINGSHOT,
                VectaraReranker.SLINGSHOT_ALT_NAME,
            ]:
                rerank_config["type"] = "customer_reranker"
                rerank_config["reranker_name"] = "Rerank_Multilingual_v1"
            else:
                rerank_config["type"] = self._reranker

            if self._reranker == VectaraReranker.MMR:
                rerank_config["diversity_bias"] = self._mmr_diversity_bias

            elif self._reranker == VectaraReranker.UDF:
                rerank_config["user_function"] = self._udf_expression

            elif self._reranker == VectaraReranker.CHAIN:
                rerank_config["rerankers"] = self._rerank_chain

            if self._rerank_limit:
                rerank_config["limit"] = self._rerank_limit
            if self._rerank_cutoff and self._reranker != VectaraReranker.CHAIN:
                rerank_config["cutoff"] = self._rerank_cutoff

            data["search"]["reranker"] = rerank_config

        if self._summary_enabled:
            summary_config = {
                "response_language": self._summary_response_lang,
                "max_used_search_results": self._summary_num_results,
                "generation_preset_name": self._summary_prompt_name,
                "enable_factual_consistency_score": True,
            }
            if self._prompt_text:
                summary_config["prompt_template"] = self._prompt_text
            if self._max_response_chars:
                summary_config["max_response_characters"] = self._max_response_chars

            model_parameters = {}
            if self._max_tokens:
                model_parameters["max_tokens"] = self._max_tokens
            if self._temperature:
                model_parameters["temperature"] = self._temperature
            if self._frequency_penalty:
                model_parameters["frequency_penalty"] = self._frequency_penalty
            if self._presence_penalty:
                model_parameters["presence_penalty"] = self._presence_penalty
            if self._llm_name:
                model_parameters["llm_name"] = self._llm_name

            if len(model_parameters)  0:
                summary_config["model_parameters"] = model_parameters

            citations_config = {}
            if self._citations_style:
                if self._citations_style in ["numeric", "none"]:
                    citations_config["style"] = self._citations_style
                elif (
                    self._citations_style in ["html", "markdown"]
                    and self._citations_url_pattern
                ):
                    citations_config["style"] = self._citations_style
                    citations_config["url_pattern"] = self._citations_url_pattern
                    citations_config["text_pattern"] = self._citations_text_pattern
                else:
                    _logger.warning(
                        f"Invalid citations style {self._citations_style}. Must be one of 'numeric', 'html', 'markdown', or 'none'."
                    )

            if len(citations_config)  0:
                summary_config["citations"] = citations_config

            data["generation"] = summary_config
            data["save_history"] = self._save_history

        return data

    def_vectara_stream(
        self,
        query_bundle: QueryBundle,
        chat: bool = False,
        conv_id: Optional[str] = None,
        verbose: bool = False,
        callback_func: Callable[[List, Dict], None] = None,
        **kwargs: Any,
    ) -> StreamingResponse:
"""
        Query Vectara index to get for top k most similar nodes.

        Args:
            query_bundle: Query Bundle
            chat: whether to use chat API in Vectara
            conv_id: conversation ID, if adding to existing chat

        """
        body = self._build_vectara_query_body(query_bundle.query_str)
        body["stream_response"] = True
        if verbose:
            print(f"Vectara streaming query request body: {body}")

        if chat:
            body["chat"] = {"store": True}
            if conv_id or self._conv_id:
                conv_id = conv_id or self._conv_id
                response = self._index._session.post(
                    headers=self._get_post_headers(),
                    url=f"{self._index._base_url}/v2/chats/{conv_id}/turns",
                    data=json.dumps(body),
                    timeout=self._index.vectara_api_timeout,
                    stream=True,
                )
            else:
                response = self._index._session.post(
                    headers=self._get_post_headers(),
                    url=f"{self._index._base_url}/v2/chats",
                    data=json.dumps(body),
                    timeout=self._index.vectara_api_timeout,
                    stream=True,
                )

        else:
            response = self._index._session.post(
                headers=self._get_post_headers(),
                url=f"{self._index._base_url}/v2/query",
                data=json.dumps(body),
                timeout=self._index.vectara_api_timeout,
                stream=True,
            )

        if response.status_code != 200:
            result = response.json()
            if response.status_code == 400:
                if "messages" in result:
                    _logger.error(
                        f"Query failed (code {response.status_code}), reason {result['messages'][0]}"
                    )
                else:
                    _logger.error(
                        f"Query failed (code {response.status_code}), err response {result}"
                    )
            return None

        defprocess_chunks(response):
            source_nodes = []
            response_metadata = {}

            deftext_generator() -> TokenGen:
                for line in response.iter_lines():
                    line = line.decode("utf-8")
                    if line:
                        key, value = line.split(":", 1)
                        if key == "data":
                            line = json.loads(value)
                            if line["type"] == "generation_chunk":
                                yield line["generation_chunk"]

                            elif line["type"] == "factual_consistency_score":
                                response_metadata["fcs"] = line[
                                    "factual_consistency_score"
                                ]

                            elif line["type"] == "search_results":
                                search_results = line["search_results"]
                                source_nodes.extend(
                                    [
                                        NodeWithScore(
                                            node=Node(
                                                text_resource=MediaResource(
                                                    text=search_result["text"]
                                                ),
                                                id_=search_result["document_id"],
                                                metadata={
                                                    # Metadata from the matched part
                                                    **search_result.get(
                                                        "part_metadata", {}
                                                    ),
                                                    # Document-level metadata
                                                    "document": search_result.get(
                                                        "document_metadata", {}
                                                    ),
                                                },
                                            ),
                                            score=search_result["score"],
                                        )
                                        for search_result in search_results[
                                            : self._similarity_top_k
                                        ]
                                    ]
                                )

                            elif line["type"] == "chat_info":
                                self._conv_id = line["chat_id"]
                                response_metadata["chat_id"] = line["chat_id"]

                if callback_func:
                    callback_func(source_nodes, response_metadata)

            return text_generator(), source_nodes, response_metadata

        response_chunks, response_nodes, response_metadata = process_chunks(response)

        return StreamingResponse(
            response_gen=response_chunks,
            source_nodes=response_nodes,
            metadata=response_metadata,
        )

    def_vectara_query(
        self,
        query_bundle: QueryBundle,
        chat: bool = False,
        conv_id: Optional[str] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> Tuple[List[NodeWithScore], Dict, str]:
"""
        Query Vectara index to get for top k most similar nodes.

        Args:
            query: Query Bundle
            chat: whether to use chat API in Vectara
            conv_id: conversation ID, if adding to existing chat
            verbose: whether to print verbose output (e.g. for debugging)
            Additional keyword arguments

        Returns:
            List[NodeWithScore]: list of nodes with scores
            Dict: summary
            str: conversation ID, if applicable

        """
        data = self._build_vectara_query_body(query_bundle.query_str)

        if verbose:
            print(f"Vectara query request body: {data}")

        if chat:
            data["chat"] = {"store": True}
            if conv_id:
                response = self._index._session.post(
                    headers=self._get_post_headers(),
                    url=f"{self._index._base_url}/v2/chats/{conv_id}/turns",
                    data=json.dumps(data),
                    timeout=self._index.vectara_api_timeout,
                )
            else:
                response = self._index._session.post(
                    headers=self._get_post_headers(),
                    url=f"{self._index._base_url}/v2/chats",
                    data=json.dumps(data),
                    timeout=self._index.vectara_api_timeout,
                )

        else:
            response = self._index._session.post(
                headers=self._get_post_headers(),
                url=f"{self._index._base_url}/v2/query",
                data=json.dumps(data),
                timeout=self._index.vectara_api_timeout,
            )

        result = response.json()
        if response.status_code != 200:
            if "messages" in result:
                _logger.error(
                    f"Query failed (code {response.status_code}), reason {result['messages'][0]}"
                )
            else:
                _logger.error(
                    f"Query failed (code {response.status_code}), err response {result}"
                )
            return [], {"text": ""}, ""

        if "warnings" in result:
            _logger.warning(f"Query warning(s) {(', ').join(result['warnings'])}")

        if verbose:
            print(f"Vectara query response: {result}")

        if self._summary_enabled:
            summary = {
                "text": result["answer"] if chat else result["summary"],
                "fcs": result.get("factual_consistency_score"),
            }
        else:
            summary = None

        search_results = result["search_results"]
        top_nodes = [
            NodeWithScore(
                node=Node(
                    text_resource=MediaResource(text=search_result["text"]),
                    id_=search_result["document_id"],
                    metadata={
                        # Metadata from the matched part
                        **search_result.get("part_metadata", {}),
                        # Document-level metadata
                        "document": search_result.get("document_metadata", {}),
                    },
                ),
                score=search_result["score"],
            )
            for search_result in search_results[: self._similarity_top_k]
        ]

        conv_id = result["chat_id"] if chat else None

        return top_nodes, summary, conv_id

    async def_avectara_query(
        self,
        query_bundle: QueryBundle,
        chat: bool = False,
        conv_id: Optional[str] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> Tuple[List[NodeWithScore], Dict]:
"""
        Asynchronously query Vectara index to get for top k most similar nodes.

        Args:
            query: Query Bundle
            chat: whether to use chat API in Vectara
            conv_id: conversation ID, if adding to existing chat
            verbose: whether to print verbose output (e.g. for debugging)
            Additional keyword arguments

        Returns:
            List[NodeWithScore]: list of nodes with scores
            Dict: summary

        """
        return await self._vectara_query(query_bundle, chat, conv_id, verbose, **kwargs)

```
 |  
| --- | --- |  
###  similarity_top_k `property` `writable` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraRetriever.similarity_top_k "Permanent link")

```
similarity_top_k: 

```

Return similarity top k.
##  VectaraQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraQueryEngine "Permanent link")
Bases: 
Retriever query engine for Vectara.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever`  |   |  A retriever object.  |  _required_  |  
|  `streaming`  |  `bool`  |  whether to use streaming mode.  |  `False`  |  
|  `summary_response_lang`  |  response language for summary (ISO 639-2 code)  |  `'eng'`  |  
|  `summary_num_results`  |  number of results to use for summary generation.  |  
|  `summary_prompt_name`  |  name of the prompt to use for summary generation.  |  `'vectara-summary-ext-24-05-med-omni'`  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/query.py`  
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
```
 | 
```
classVectaraQueryEngine(BaseQueryEngine):
"""
    Retriever query engine for Vectara.

    Args:
        retriever (VectaraRetriever): A retriever object.
        streaming: whether to use streaming mode.
        summary_response_lang: response language for summary (ISO 639-2 code)
        summary_num_results: number of results to use for summary generation.
        summary_prompt_name: name of the prompt to use for summary generation.

    """

    def__init__(
        self,
        retriever: VectaraRetriever,
        streaming: bool = False,
        node_postprocessors: Optional[List[BaseNodePostprocessor]] = None,
        callback_manager: Optional[CallbackManager] = None,
        summary_enabled: bool = False,
        summary_response_lang: str = "eng",
        summary_num_results: int = 5,
        summary_prompt_name: str = "vectara-summary-ext-24-05-med-omni",
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
        self._retriever = retriever
        self._streaming = streaming
        self._summary_enabled = summary_enabled
        self._summary_response_lang = summary_response_lang
        self._summary_num_results = summary_num_results
        self._summary_prompt_name = summary_prompt_name
        self._node_postprocessors = node_postprocessors or []
        self._verbose = verbose
        super().__init__(callback_manager=callback_manager)

    @classmethod
    deffrom_args(
        cls,
        retriever: VectaraRetriever,
        streaming: bool = False,
        summary_enabled: bool = False,
        **kwargs: Any,
    ) -> "VectaraQueryEngine":
"""
        Initialize a VectaraQueryEngine object.".

        Args:
            retriever (VectaraRetriever): A Vectara retriever object.
            summary_enabled: is summary enabled

        """
        return cls(
            retriever=retriever,
            streaming=streaming,
            summary_enabled=summary_enabled,
            **kwargs,
        )

    def_apply_node_postprocessors(
        self, nodes: List[NodeWithScore], query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        for node_postprocessor in self._node_postprocessors:
            nodes = node_postprocessor.postprocess_nodes(
                nodes, query_bundle=query_bundle
            )
        return nodes

    defretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = self._retriever.retrieve(query_bundle)
        return self._apply_node_postprocessors(nodes, query_bundle=query_bundle)

    async defaretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        nodes = await self._retriever.aretrieve(query_bundle)
        return self._apply_node_postprocessors(nodes, query_bundle=query_bundle)

    defwith_retriever(self, retriever: VectaraRetriever) -> "VectaraQueryEngine":
        return VectaraQueryEngine(
            retriever=retriever,
            summary_enabled=self._summary_enabled,
            summary_response_lang=self._summary_response_lang,
            summary_num_results=self._summary_num_results,
            summary_prompt_name=self._summary_prompt_name,
            verbose=self._verbose,
        )

    def_query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
"""Answer a query."""
        kwargs = (
            {
                "response_language": self._summary_response_lang,
                "max_used_search_results": self._summary_num_results,
                "generation_preset_name": self._summary_prompt_name,
            }
            if self._summary_enabled
            else {}
        )

        if self._streaming:
            query_response = self._retriever._vectara_stream(
                query_bundle, chat=False, verbose=self._verbose
            )
        else:
            nodes, response, _ = self._retriever._vectara_query(
                query_bundle, verbose=self._verbose, **kwargs
            )
            query_response = Response(
                response=response["text"],
                source_nodes=nodes,
                metadata={"fcs": response.get("fcs", None)},
            )

        return query_response

    async def_aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        return self._query(query_bundle)

    @property
    defretriever(self) -> BaseRetriever:
"""Get the retriever object."""
        return self._retriever

    # required for PromptMixin
    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt modules."""
        return {}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""

```
 |  
| --- | --- |  
###  retriever `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraQueryEngine.retriever "Permanent link")

```
retriever: 

```

Get the retriever object.
###  from_args `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vectara/#llama_index.indices.managed.vectara.VectaraQueryEngine.from_args "Permanent link")

```
from_args(
    retriever: ,
    streaming:  = False,
    summary_enabled:  = False,
    **kwargs: 
) -> 

```

Initialize a VectaraQueryEngine object.".
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `retriever`  |   |  A Vectara retriever object.  |  _required_  |  
|  `summary_enabled`  |  `bool`  |  is summary enabled  |  `False`  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vectara/llama_index/indices/managed/vectara/query.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_args(
    cls,
    retriever: VectaraRetriever,
    streaming: bool = False,
    summary_enabled: bool = False,
    **kwargs: Any,
) -> "VectaraQueryEngine":
"""
    Initialize a VectaraQueryEngine object.".

    Args:
        retriever (VectaraRetriever): A Vectara retriever object.
        summary_enabled: is summary enabled

    """
    return cls(
        retriever=retriever,
        streaming=streaming,
        summary_enabled=summary_enabled,
        **kwargs,
    )

```
 |  
| --- | --- |  
options: members: - VectaraIndex
