# Jaguar
##  JaguarVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore "Permanent link")
Bases: 
Jaguar vector store.
See http://www.jaguardb.com See http://github.com/fserv/jaguar-sdk
Examples:
`pip install llama-index-vector-stores-jaguar`

```
fromllama_index.vector_stores.jaguarimport JaguarVectorStore
vectorstore = JaguarVectorStore(
    pod = 'vdb',
    store = 'mystore',
    vector_index = 'v',
    vector_type = 'cosine_fraction_float',
    vector_dimension = 1536,
    url='http://192.168.8.88:8080/fwww/',
)

```

Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
classJaguarVectorStore(BasePydanticVectorStore):
"""
    Jaguar vector store.

    See http://www.jaguardb.com
    See http://github.com/fserv/jaguar-sdk

    Examples:
        `pip install llama-index-vector-stores-jaguar`

        ```python
        from llama_index.vector_stores.jaguar import JaguarVectorStore
        vectorstore = JaguarVectorStore(
            pod = 'vdb',
            store = 'mystore',
            vector_index = 'v',
            vector_type = 'cosine_fraction_float',
            vector_dimension = 1536,
            url='http://192.168.8.88:8080/fwww/',

        ```

    """

    stores_text: bool = True

    _pod: str = PrivateAttr()
    _store: str = PrivateAttr()
    _vector_index: str = PrivateAttr()
    _vector_type: str = PrivateAttr()
    _vector_dimension: int = PrivateAttr()
    _jag: JaguarHttpClient = PrivateAttr()
    _token: str = PrivateAttr()

    def__init__(
        self,
        pod: str,
        store: str,
        vector_index: str,
        vector_type: str,
        vector_dimension: int,
        url: str,
    ):
"""
        Constructor of JaguarVectorStore.

        Args:
            pod: str:  name of the pod (database)
            store: str:  name of vector store in the pod
            vector_index: str:  name of vector index of the store
            vector_type: str:  type of the vector index
            vector_dimension: int:  dimension of the vector index
            url: str:  URL end point of jaguar http server

        """
        super().__init__(stores_text=True)
        self._pod = self._sanitize_input(pod)
        self._store = self._sanitize_input(store)
        self._vector_index = self._sanitize_input(vector_index)
        self._vector_type = self._sanitize_input(vector_type)
        self._vector_dimension = vector_dimension
        self._jag = JaguarHttpClient(url)
        self._token = ""

    def__del__(self) -> None:
        pass

    @classmethod
    defclass_name(cls) -> str:
        return "JaguarVectorStore"

    @property
    defclient(self) -> Any:
"""Get client."""
        return self._jag

    def_sanitize_input(self, value: str) -> str:
"""Sanitize input to prevent SQL injection."""
        forbidden_chars = ['"', ";", "--", "/*", "*/"]
        sanitized = value.replace("'", "\\'")
        for char in forbidden_chars:
            sanitized = sanitized.replace(char, "")
        return sanitized

    defadd(
        self,
        nodes: Sequence[BaseNode],
        **add_kwargs: Any,
    ) -> List[str]:
"""
        Add nodes to index.

        Args:
            nodes: List[BaseNode]: list of nodes with embeddings

        """
        use_node_metadata = add_kwargs.get("use_node_metadata", False)
        ids = []
        for node in nodes:
            text = node.get_text()
            embedding = node.get_embedding()
            if use_node_metadata is True:
                metadata = node.metadata
            else:
                metadata = None
            zid = self.add_text(text, embedding, metadata, **add_kwargs)
            ids.append(zid)

        return ids

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
        Delete nodes using with ref_doc_id.

        Args:
            ref_doc_id (str): The doc_id of the document to delete.

        """
        podstore = self._pod + "." + self._store
        q = (
            "delete from "
            + podstore
            + " where zid='"
            + self._sanitize_input(ref_doc_id)
            + "'"
        )
        self.run(q)

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
        Query index for top k most similar nodes.

        Args:
            query: VectorStoreQuery object
            kwargs:  may contain 'where', 'metadata_fields', 'args', 'fetch_k'

        """
        embedding = query.query_embedding
        k = query.similarity_top_k
        (nodes, ids, simscores) = self.similarity_search_with_score(
            embedding, k=k, form="node", **kwargs
        )
        return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=simscores)

    defload_documents(
        self, embedding: List[float], k: int, **kwargs: Any
    ) -> List[Document]:
"""
        Query index to load top k most similar documents.

        Args:
            embedding: a list of floats
            k: topK number
            kwargs:  may contain 'where', 'metadata_fields', 'args', 'fetch_k'

        """
        return cast(
            List[Document],
            self.similarity_search_with_score(embedding, k=k, form="doc", **kwargs),
        )

    defcreate(
        self,
        metadata_fields: str,
        text_size: int,
    ) -> None:
"""
        Create the vector store on the backend database.

        Args:
            metadata_fields (str):  exrta metadata columns and types
        Returns:
            True if successful; False if not successful

        """
        podstore = self._pod + "." + self._store

"""
        v:text column is required.
        """
        q = "create store "
        q += podstore
        q += f" ({self._vector_index} vector({self._vector_dimension},"
        q += f" '{self._vector_type}'),"
        q += f"  v:text char({text_size}),"
        q += self._sanitize_input(metadata_fields) + ")"
        self.run(q)

    defadd_text(
        self,
        text: str,
        embedding: List[float],
        metadata: Optional[dict] = None,
        **kwargs: Any,
    ) -> str:
"""
        Add  texts through the embeddings and add to the vectorstore.

        Args:
          texts: text string to add to the jaguar vector store.
          embedding: embedding vector of the text, list of floats
          metadata: {'file_path': '../data/paul_graham/paul_graham_essay.txt',
                          'file_name': 'paul_graham_essay.txt',
                          'file_type': 'text/plain',
                          'file_size': 75042,
                          'creation_date': '2023-12-24',
                          'last_modified_date': '2023-12-24',
                          'last_accessed_date': '2023-12-28'}
          kwargs: vector_index=name_of_vector_index
                  file_column=name_of_file_column
                  metadata={...}

        Returns:
            id from adding the text into the vectorstore

        """
        text = self._sanitize_input(text)
        vcol = self._vector_index
        filecol = kwargs.get("file_column", "")
        text_tag = kwargs.get("text_tag", "")

        if text_tag != "":
            text = text_tag + " " + text

        podstorevcol = self._pod + "." + self._store + "." + vcol
        q = "textcol " + podstorevcol
        js = self.run(q)
        if js == "":
            return ""
        textcol = js["data"]

        zid = ""
        if metadata is None:
            ### no metadata and no files to upload
            str_vec = [str(x) for x in embedding]
            values_comma = self._sanitize_input(",".join(str_vec))
            podstore = self._pod + "." + self._store
            q = "insert into " + podstore + " ("
            q += vcol + "," + textcol + ") values ('" + values_comma
            q += "','" + text + "')"
            js = self.run(q, False)
            zid = js["zid"]
        else:
            str_vec = [str(x) for x in embedding]
            nvec, vvec, filepath = self._parseMeta(metadata, filecol)
            if filecol != "":
                rc = self._jag.postFile(self._token, filepath, 1)
                if not rc:
                    return ""
            names_comma = ",".join(nvec)
            names_comma += "," + vcol
            names_comma = self._sanitize_input(names_comma)
            ## col1,col2,col3,vecl

            if vvec is not None and len(vvec)  0:
                values_comma = "'" + "','".join(vvec) + "'"
            else:
                values_comma = "'" + "','".join(vvec) + "'"

            ### 'va1','val2','val3'
            values_comma += ",'" + ",".join(str_vec) + "'"
            values_comma = self._sanitize_input(values_comma)
            ### 'v1,v2,v3'
            podstore = self._pod + "." + self._store
            q = "insert into " + podstore + " ("
            q += names_comma + "," + textcol + ") values (" + values_comma
            q += ",'" + text + "')"
            if filecol != "":
                js = self.run(q, True)
            else:
                js = self.run(q, False)
            zid = js["zid"]

        return zid

    defsimilarity_search_with_score(
        self,
        embedding: Optional[List[float]],
        k: int = 3,
        form: str = "node",
        **kwargs: Any,
    ) -> Union[Tuple[List[TextNode], List[str], List[float]], List[Document]]:
"""
        Return nodes most similar to query embedding, along with ids and scores.

        Args:
            embedding: embedding of text to look up.
            k: Number of nodes to return. Defaults to 3.
            form: if "node", return Tuple[List[TextNode], List[str], List[float]]
                  if "doc", return List[Document]
            kwargs: may have where, metadata_fields, args, fetch_k
        Returns:
            Tuple(list of nodes, list of ids, list of similaity scores)

        """
        where = kwargs.get("where")
        metadata_fields = kwargs.get("metadata_fields")

        args = kwargs.get("args")
        fetch_k = kwargs.get("fetch_k", -1)

        vcol = self._vector_index
        vtype = self._vector_type
        if embedding is None:
            return ([], [], [])
        str_embeddings = [str(f) for f in embedding]
        qv_comma = self._sanitize_input(",".join(str_embeddings))
        podstore = self._pod + "." + self._store
        q = (
            "select similarity("
            + vcol
            + ",'"
            + qv_comma
            + "','topk="
            + str(k)
            + ",fetch_k="
            + str(fetch_k)
            + ",type="
            + vtype
        )
        q += ",with_score=yes,with_text=yes"
        if args is not None:
            q += "," + args

        if metadata_fields is not None:
            x = "&".join(metadata_fields)
            q += ",metadata=" + x

        q += "') from " + podstore

        if where is not None:
            q += " where " + self._sanitize_input(where)

        jarr = self.run(q)

        if jarr is None:
            return ([], [], [])

        nodes = []
        ids = []
        simscores = []
        docs = []
        for js in jarr:
            score = js["score"]
            text = js["text"]
            zid = js["zid"]

            md = {}
            md["zid"] = zid
            if metadata_fields is not None:
                for m in metadata_fields:
                    mv = js[m]
                    md[m] = mv

            if form == "node":
                node = TextNode(
                    id_=zid,
                    text=text,
                    metadata=md,
                )
                nodes.append(node)
                ids.append(zid)
                simscores.append(float(score))
            else:
                doc = Document(
                    id_=zid,
                    text=text,
                    metadata=md,
                )
                docs.append(doc)

        if form == "node":
            return (nodes, ids, simscores)
        else:
            return docs

    defis_anomalous(
        self,
        node: BaseNode,
        **kwargs: Any,
    ) -> bool:
"""
        Detect if given text is anomalous from the dataset.

        Args:
            query: Text to detect if it is anomaly
        Returns:
            True or False

        """
        vcol = self._vector_index
        vtype = self._vector_type
        str_embeddings = [str(f) for f in node.get_embedding()]
        qv_comma = ",".join(str_embeddings)
        podstore = self._pod + "." + self._store
        q = "select anomalous(" + vcol + ", '" + qv_comma + "', 'type=" + vtype + "')"
        q += " from " + podstore

        js = self.run(q)
        if isinstance(js, list) and len(js) == 0:
            return False
        jd = json.loads(js[0])
        return jd["anomalous"] == "YES"

    defrun(self, query: str, withFile: bool = False) -> dict:
"""
        Run any query statement in jaguardb.

        Args:
            query (str): query statement to jaguardb
        Returns:
            None for invalid token, or
            json result string

        """
        if self._token == "":
            logger.error(f"E0005 error run({query})")
            return {}

        resp = self._jag.post(query, self._token, withFile)
        txt = resp.text
        try:
            return json.loads(txt)
        except Exception:
            return {}

    defcount(self) -> int:
"""
        Count records of a store in jaguardb.

        Args: no args
        Returns: (int) number of records in pod store
        """
        podstore = self._pod + "." + self._store
        q = "select count() from " + podstore
        js = self.run(q)
        if isinstance(js, list) and len(js) == 0:
            return 0
        jd = json.loads(js[0])
        return int(jd["data"])

    defclear(self) -> None:
"""
        Delete all records in jaguardb.

        Args: No args
        Returns: None
        """
        podstore = self._pod + "." + self._store
        q = "truncate store " + podstore
        self.run(q)

    defdrop(self) -> None:
"""
        Drop or remove a store in jaguardb.

        Args: no args
        Returns: None
        """
        podstore = self._pod + "." + self._store
        q = "drop store " + podstore
        self.run(q)

    defprt(self, msg: str) -> None:
        nows = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/tmp/debugjaguar.log", "a") as file:
            print(f"{nows} msg={msg}", file=file, flush=True)

    deflogin(
        self,
        jaguar_api_key: Optional[str] = "",
    ) -> bool:
"""
        Login to jaguar server with a jaguar_api_key or let self._jag find a key.

        Args:
            optional jaguar_api_key (str): API key of user to jaguardb server
        Returns:
            True if successful; False if not successful

        """
        if jaguar_api_key == "":
            jaguar_api_key = self._jag.getApiKey()
        self._jaguar_api_key = jaguar_api_key
        self._token = self._jag.login(jaguar_api_key)
        if self._token == "":
            logger.error("E0001 error init(): invalid jaguar_api_key")
            return False
        return True

    deflogout(self) -> None:
"""
        Logout to cleanup resources.

        Args: no args
        Returns: None
        """
        self._jag.logout(self._token)

    def_parseMeta(self, nvmap: dict, filecol: str) -> Tuple[List[str], List[str], str]:
        filepath = ""
        if filecol == "":
            nvec = list(nvmap.keys())
            vvec = list(nvmap.values())
        else:
            nvec = []
            vvec = []
            if filecol in nvmap:
                nvec.append(filecol)
                vvec.append(nvmap[filecol])
                filepath = nvmap[filecol]

            for k, v in nvmap.items():
                if k != filecol:
                    nvec.append(k)
                    vvec.append(v)

        return nvec, vvec, filepath

```
 |  
| --- | --- |  
###  client `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.client "Permanent link")

```
client: 

```

Get client.
###  add [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.add "Permanent link")

```
add(
    nodes: Sequence[], **add_kwargs: 
) -> []

```

Add nodes to index.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `Sequence[BaseNode[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.BaseNode "BaseNode \(llama_index.core.schema.BaseNode\)")]`  |  List[BaseNode]: list of nodes with embeddings  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defadd(
    self,
    nodes: Sequence[BaseNode],
    **add_kwargs: Any,
) -> List[str]:
"""
    Add nodes to index.

    Args:
        nodes: List[BaseNode]: list of nodes with embeddings

    """
    use_node_metadata = add_kwargs.get("use_node_metadata", False)
    ids = []
    for node in nodes:
        text = node.get_text()
        embedding = node.get_embedding()
        if use_node_metadata is True:
            metadata = node.metadata
        else:
            metadata = None
        zid = self.add_text(text, embedding, metadata, **add_kwargs)
        ids.append(zid)

    return ids

```
 |  
| --- | --- |  
###  delete [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.delete "Permanent link")

```
delete(ref_doc_id: , **delete_kwargs: ) -> None

```

Delete nodes using with ref_doc_id.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `ref_doc_id`  |  The doc_id of the document to delete.  |  _required_  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
"""
    Delete nodes using with ref_doc_id.

    Args:
        ref_doc_id (str): The doc_id of the document to delete.

    """
    podstore = self._pod + "." + self._store
    q = (
        "delete from "
        + podstore
        + " where zid='"
        + self._sanitize_input(ref_doc_id)
        + "'"
    )
    self.run(q)

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.query "Permanent link")

```
query(
    query: , **kwargs: 
) -> 

```

Query index for top k most similar nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |   |  VectorStoreQuery object  |  _required_  |  
|  `kwargs`  |  may contain 'where', 'metadata_fields', 'args', 'fetch_k'  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
"""
    Query index for top k most similar nodes.

    Args:
        query: VectorStoreQuery object
        kwargs:  may contain 'where', 'metadata_fields', 'args', 'fetch_k'

    """
    embedding = query.query_embedding
    k = query.similarity_top_k
    (nodes, ids, simscores) = self.similarity_search_with_score(
        embedding, k=k, form="node", **kwargs
    )
    return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=simscores)

```
 |  
| --- | --- |  
###  load_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.load_documents "Permanent link")

```
load_documents(
    embedding: [float], k: , **kwargs: 
) -> []

```

Query index to load top k most similar documents.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `embedding`  |  `List[float]`  |  a list of floats  |  _required_  |  
|  topK number  |  _required_  |  
|  `kwargs`  |  may contain 'where', 'metadata_fields', 'args', 'fetch_k'  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defload_documents(
    self, embedding: List[float], k: int, **kwargs: Any
) -> List[Document]:
"""
    Query index to load top k most similar documents.

    Args:
        embedding: a list of floats
        k: topK number
        kwargs:  may contain 'where', 'metadata_fields', 'args', 'fetch_k'

    """
    return cast(
        List[Document],
        self.similarity_search_with_score(embedding, k=k, form="doc", **kwargs),
    )

```
 |  
| --- | --- |  
###  create [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.create "Permanent link")

```
create(metadata_fields: , text_size: ) -> None

```

Create the vector store on the backend database.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `metadata_fields`  |  exrta metadata columns and types  |  _required_  |  
Returns: True if successful; False if not successful
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defcreate(
    self,
    metadata_fields: str,
    text_size: int,
) -> None:
"""
    Create the vector store on the backend database.

    Args:
        metadata_fields (str):  exrta metadata columns and types
    Returns:
        True if successful; False if not successful

    """
    podstore = self._pod + "." + self._store

"""
    v:text column is required.
    """
    q = "create store "
    q += podstore
    q += f" ({self._vector_index} vector({self._vector_dimension},"
    q += f" '{self._vector_type}'),"
    q += f"  v:text char({text_size}),"
    q += self._sanitize_input(metadata_fields) + ")"
    self.run(q)

```
 |  
| --- | --- |  
###  add_text [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.add_text "Permanent link")

```
add_text(
    text: ,
    embedding: [float],
    metadata: Optional[] = None,
    **kwargs: 
) -> 

```

Add texts through the embeddings and add to the vectorstore.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `texts`  |  text string to add to the jaguar vector store.  |  _required_  |  
|  `embedding`  |  `List[float]`  |  embedding vector of the text, list of floats  |  _required_  |  
|  `metadata`  |  `Optional[dict]`  |  {'file_path': '../data/paul_graham/paul_graham_essay.txt', 'file_name': 'paul_graham_essay.txt', 'file_type': 'text/plain', 'file_size': 75042, 'creation_date': '2023-12-24', 'last_modified_date': '2023-12-24', 'last_accessed_date': '2023-12-28'}  |  `None`  |  
|  `kwargs`  |  vector_index=name_of_vector_index file_column=name_of_file_column metadata={...}  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  id from adding the text into the vectorstore  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defadd_text(
    self,
    text: str,
    embedding: List[float],
    metadata: Optional[dict] = None,
    **kwargs: Any,
) -> str:
"""
    Add  texts through the embeddings and add to the vectorstore.

    Args:
      texts: text string to add to the jaguar vector store.
      embedding: embedding vector of the text, list of floats
      metadata: {'file_path': '../data/paul_graham/paul_graham_essay.txt',
                      'file_name': 'paul_graham_essay.txt',
                      'file_type': 'text/plain',
                      'file_size': 75042,
                      'creation_date': '2023-12-24',
                      'last_modified_date': '2023-12-24',
                      'last_accessed_date': '2023-12-28'}
      kwargs: vector_index=name_of_vector_index
              file_column=name_of_file_column
              metadata={...}

    Returns:
        id from adding the text into the vectorstore

    """
    text = self._sanitize_input(text)
    vcol = self._vector_index
    filecol = kwargs.get("file_column", "")
    text_tag = kwargs.get("text_tag", "")

    if text_tag != "":
        text = text_tag + " " + text

    podstorevcol = self._pod + "." + self._store + "." + vcol
    q = "textcol " + podstorevcol
    js = self.run(q)
    if js == "":
        return ""
    textcol = js["data"]

    zid = ""
    if metadata is None:
        ### no metadata and no files to upload
        str_vec = [str(x) for x in embedding]
        values_comma = self._sanitize_input(",".join(str_vec))
        podstore = self._pod + "." + self._store
        q = "insert into " + podstore + " ("
        q += vcol + "," + textcol + ") values ('" + values_comma
        q += "','" + text + "')"
        js = self.run(q, False)
        zid = js["zid"]
    else:
        str_vec = [str(x) for x in embedding]
        nvec, vvec, filepath = self._parseMeta(metadata, filecol)
        if filecol != "":
            rc = self._jag.postFile(self._token, filepath, 1)
            if not rc:
                return ""
        names_comma = ",".join(nvec)
        names_comma += "," + vcol
        names_comma = self._sanitize_input(names_comma)
        ## col1,col2,col3,vecl

        if vvec is not None and len(vvec)  0:
            values_comma = "'" + "','".join(vvec) + "'"
        else:
            values_comma = "'" + "','".join(vvec) + "'"

        ### 'va1','val2','val3'
        values_comma += ",'" + ",".join(str_vec) + "'"
        values_comma = self._sanitize_input(values_comma)
        ### 'v1,v2,v3'
        podstore = self._pod + "." + self._store
        q = "insert into " + podstore + " ("
        q += names_comma + "," + textcol + ") values (" + values_comma
        q += ",'" + text + "')"
        if filecol != "":
            js = self.run(q, True)
        else:
            js = self.run(q, False)
        zid = js["zid"]

    return zid

```
 |  
| --- | --- |  
###  similarity_search_with_score [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.similarity_search_with_score "Permanent link")

```
similarity_search_with_score(
    embedding: Optional[[float]],
    k:  = 3,
    form:  = "node",
    **kwargs: 
) -> Union[
    Tuple[[], [], [float]],
    [],
]

```

Return nodes most similar to query embedding, along with ids and scores.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `embedding`  |  `Optional[List[float]]`  |  embedding of text to look up.  |  _required_  |  
|  Number of nodes to return. Defaults to 3.  |  
|  `form`  |  if "node", return Tuple[List[TextNode], List[str], List[float]] if "doc", return List[Document]  |  `'node'`  |  
|  `kwargs`  |  may have where, metadata_fields, args, fetch_k  |  
Returns: Tuple(list of nodes, list of ids, list of similaity scores)
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defsimilarity_search_with_score(
    self,
    embedding: Optional[List[float]],
    k: int = 3,
    form: str = "node",
    **kwargs: Any,
) -> Union[Tuple[List[TextNode], List[str], List[float]], List[Document]]:
"""
    Return nodes most similar to query embedding, along with ids and scores.

    Args:
        embedding: embedding of text to look up.
        k: Number of nodes to return. Defaults to 3.
        form: if "node", return Tuple[List[TextNode], List[str], List[float]]
              if "doc", return List[Document]
        kwargs: may have where, metadata_fields, args, fetch_k
    Returns:
        Tuple(list of nodes, list of ids, list of similaity scores)

    """
    where = kwargs.get("where")
    metadata_fields = kwargs.get("metadata_fields")

    args = kwargs.get("args")
    fetch_k = kwargs.get("fetch_k", -1)

    vcol = self._vector_index
    vtype = self._vector_type
    if embedding is None:
        return ([], [], [])
    str_embeddings = [str(f) for f in embedding]
    qv_comma = self._sanitize_input(",".join(str_embeddings))
    podstore = self._pod + "." + self._store
    q = (
        "select similarity("
        + vcol
        + ",'"
        + qv_comma
        + "','topk="
        + str(k)
        + ",fetch_k="
        + str(fetch_k)
        + ",type="
        + vtype
    )
    q += ",with_score=yes,with_text=yes"
    if args is not None:
        q += "," + args

    if metadata_fields is not None:
        x = "&".join(metadata_fields)
        q += ",metadata=" + x

    q += "') from " + podstore

    if where is not None:
        q += " where " + self._sanitize_input(where)

    jarr = self.run(q)

    if jarr is None:
        return ([], [], [])

    nodes = []
    ids = []
    simscores = []
    docs = []
    for js in jarr:
        score = js["score"]
        text = js["text"]
        zid = js["zid"]

        md = {}
        md["zid"] = zid
        if metadata_fields is not None:
            for m in metadata_fields:
                mv = js[m]
                md[m] = mv

        if form == "node":
            node = TextNode(
                id_=zid,
                text=text,
                metadata=md,
            )
            nodes.append(node)
            ids.append(zid)
            simscores.append(float(score))
        else:
            doc = Document(
                id_=zid,
                text=text,
                metadata=md,
            )
            docs.append(doc)

    if form == "node":
        return (nodes, ids, simscores)
    else:
        return docs

```
 |  
| --- | --- |  
###  is_anomalous [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.is_anomalous "Permanent link")

```
is_anomalous(node: , **kwargs: ) -> 

```

Detect if given text is anomalous from the dataset.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Text to detect if it is anomaly  |  _required_  |  
Returns: True or False
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defis_anomalous(
    self,
    node: BaseNode,
    **kwargs: Any,
) -> bool:
"""
    Detect if given text is anomalous from the dataset.

    Args:
        query: Text to detect if it is anomaly
    Returns:
        True or False

    """
    vcol = self._vector_index
    vtype = self._vector_type
    str_embeddings = [str(f) for f in node.get_embedding()]
    qv_comma = ",".join(str_embeddings)
    podstore = self._pod + "." + self._store
    q = "select anomalous(" + vcol + ", '" + qv_comma + "', 'type=" + vtype + "')"
    q += " from " + podstore

    js = self.run(q)
    if isinstance(js, list) and len(js) == 0:
        return False
    jd = json.loads(js[0])
    return jd["anomalous"] == "YES"

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.run "Permanent link")

```
run(query: , withFile:  = False) -> 

```

Run any query statement in jaguardb.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  query statement to jaguardb  |  _required_  |  
Returns: None for invalid token, or json result string
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defrun(self, query: str, withFile: bool = False) -> dict:
"""
    Run any query statement in jaguardb.

    Args:
        query (str): query statement to jaguardb
    Returns:
        None for invalid token, or
        json result string

    """
    if self._token == "":
        logger.error(f"E0005 error run({query})")
        return {}

    resp = self._jag.post(query, self._token, withFile)
    txt = resp.text
    try:
        return json.loads(txt)
    except Exception:
        return {}

```
 |  
| --- | --- |  
###  count [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.count "Permanent link")

```
count() -> 

```

Count records of a store in jaguardb.
Args: no args Returns: (int) number of records in pod store
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defcount(self) -> int:
"""
    Count records of a store in jaguardb.

    Args: no args
    Returns: (int) number of records in pod store
    """
    podstore = self._pod + "." + self._store
    q = "select count() from " + podstore
    js = self.run(q)
    if isinstance(js, list) and len(js) == 0:
        return 0
    jd = json.loads(js[0])
    return int(jd["data"])

```
 |  
| --- | --- |  
###  clear [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.clear "Permanent link")

```
clear() -> None

```

Delete all records in jaguardb.
Args: No args Returns: None
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defclear(self) -> None:
"""
    Delete all records in jaguardb.

    Args: No args
    Returns: None
    """
    podstore = self._pod + "." + self._store
    q = "truncate store " + podstore
    self.run(q)

```
 |  
| --- | --- |  
###  drop [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.drop "Permanent link")

```
drop() -> None

```

Drop or remove a store in jaguardb.
Args: no args Returns: None
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
defdrop(self) -> None:
"""
    Drop or remove a store in jaguardb.

    Args: no args
    Returns: None
    """
    podstore = self._pod + "." + self._store
    q = "drop store " + podstore
    self.run(q)

```
 |  
| --- | --- |  
###  login [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.login "Permanent link")

```
login(jaguar_api_key: Optional[] = '') -> 

```

Login to jaguar server with a jaguar_api_key or let self._jag find a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `optional jaguar_api_key`  |  API key of user to jaguardb server  |  _required_  |  
Returns: True if successful; False if not successful
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
```
 | 
```
deflogin(
    self,
    jaguar_api_key: Optional[str] = "",
) -> bool:
"""
    Login to jaguar server with a jaguar_api_key or let self._jag find a key.

    Args:
        optional jaguar_api_key (str): API key of user to jaguardb server
    Returns:
        True if successful; False if not successful

    """
    if jaguar_api_key == "":
        jaguar_api_key = self._jag.getApiKey()
    self._jaguar_api_key = jaguar_api_key
    self._token = self._jag.login(jaguar_api_key)
    if self._token == "":
        logger.error("E0001 error init(): invalid jaguar_api_key")
        return False
    return True

```
 |  
| --- | --- |  
###  logout [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/jaguar/#llama_index.vector_stores.jaguar.JaguarVectorStore.logout "Permanent link")

```
logout() -> None

```

Logout to cleanup resources.
Args: no args Returns: None
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-jaguar/llama_index/vector_stores/jaguar/base.py`  
| 
```
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
deflogout(self) -> None:
"""
    Logout to cleanup resources.

    Args: no args
    Returns: None
    """
    self._jag.logout(self._token)

```
 |  
| --- | --- |  
options: members: - JaguarVectorStore
