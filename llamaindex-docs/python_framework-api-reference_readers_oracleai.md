# Oracleai
##  OracleReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oracleai/#llama_index.readers.oracleai.OracleReader "Permanent link")
Bases: 
Read documents using OracleDocLoader Args: conn: Oracle Connection, params: Loader parameters.
Source code in `llama-index-integrations/readers/llama-index-readers-oracleai/llama_index/readers/oracleai/base.py`  
| 
```
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
```
 | 
```
classOracleReader(BaseReader):
"""
    Read documents using OracleDocLoader
    Args:
        conn: Oracle Connection,
        params: Loader parameters.
    """

    def__init__(self, conn: Connection, params: Dict[str, Any]):
        self.conn = conn
        self.params = json.loads(json.dumps(params))

    defload(self) -> List[Document]:
"""Load data into Document objects..."""
        try:
            importoracledb
        except ImportError as e:
            raise ImportError(
                "Unable to import oracledb, please install with "
                "`pip install -U oracledb`."
            ) frome

        ncols = 0
        results = []
        metadata = {}
        m_params = {"plaintext": "false"}

        try:
            # extract the parameters
            if self.params is not None:
                self.file = self.params.get("file")
                self.dir = self.params.get("dir")
                self.owner = self.params.get("owner")
                self.tablename = self.params.get("tablename")
                self.colname = self.params.get("colname")
            else:
                raise Exception("Missing loader parameters")

            oracledb.defaults.fetch_lobs = False

            if self.file:
                doc = OracleDocReader.read_file(self.conn, self.file, m_params)

                if doc is None:
                    return results

                results.append(doc)

            if self.dir:
                skip_count = 0
                if not (os.path.exists(self.dir) and os.path.isdir(self.dir)):
                    raise Exception("Directory does not exist or invalid.")
                else:
                    for file_name in os.listdir(self.dir):
                        file_path = os.path.join(self.dir, file_name)
                        if os.path.isfile(file_path):
                            doc = OracleDocReader.read_file(
                                self.conn, file_path, m_params
                            )

                            if doc is None:
                                skip_count = skip_count + 1
                                print(f"Total skipped: {skip_count}\n")
                            else:
                                results.append(doc)

            if self.tablename:
                try:
                    if self.owner is None or self.colname is None:
                        raise Exception("Missing owner or column name")

                    cursor = self.conn.cursor()
                    self.mdata_cols = self.params.get("mdata_cols")
                    if self.mdata_cols is not None:
                        if len(self.mdata_cols)  3:
                            raise Exception(
                                "Exceeds the max number of columns you can request for metadata."
                            )

                        # execute a query to get column data types
                        sql = (
                            "select column_name, data_type from all_tab_columns where owner = '"
                            + self.owner.upper()
                            + "' and "
                            + "table_name = '"
                            + self.tablename.upper()
                            + "'"
                        )

                        cursor.execute(sql)
                        rows = cursor.fetchall()
                        for row in rows:
                            if row[0] in self.mdata_cols:
                                if row[1] not in [
                                    "NUMBER",
                                    "BINARY_DOUBLE",
                                    "BINARY_FLOAT",
                                    "LONG",
                                    "DATE",
                                    "TIMESTAMP",
                                    "VARCHAR2",
                                ]:
                                    raise Exception(
                                        "The datatype for the column requested for metadata is not supported."
                                    )

                    self.mdata_cols_sql = ", rowid"
                    if self.mdata_cols is not None:
                        for col in self.mdata_cols:
                            self.mdata_cols_sql = self.mdata_cols_sql + ", " + col

                    # [TODO] use bind variables
                    sql = (
                        "select dbms_vector_chain.utl_to_text(t."
                        + self.colname
                        + ", json('"
                        + json.dumps(m_params)
                        + "')) mdata, dbms_vector_chain.utl_to_text(t."
                        + self.colname
                        + ") text"
                        + self.mdata_cols_sql
                        + " from "
                        + self.owner
                        + "."
                        + self.tablename
                        + " t"
                    )

                    cursor.execute(sql)
                    for row in cursor:
                        metadata = {}

                        if row is None:
                            doc_id = OracleDocReader.generate_object_id(
                                self.conn.username
                                + "$"
                                + self.owner
                                + "$"
                                + self.tablename
                                + "$"
                                + self.colname
                            )
                            metadata["_oid"] = doc_id
                            results.append(Document(text="", metadata=metadata))
                        else:
                            if row[0] is not None:
                                data = str(row[0])
                                if data.startswith(("<!DOCTYPE html", "<HTML>")):
                                    p = ParseOracleDocMetadata()
                                    p.feed(data)
                                    metadata = p.get_metadata()

                            doc_id = OracleDocReader.generate_object_id(
                                self.conn.username
                                + "$"
                                + self.owner
                                + "$"
                                + self.tablename
                                + "$"
                                + self.colname
                                + "$"
                                + str(row[2])
                            )
                            metadata["_oid"] = doc_id
                            metadata["_rowid"] = row[2]

                            # process projected metadata cols
                            if self.mdata_cols is not None:
                                ncols = len(self.mdata_cols)

                            for i in range(ncols):
                                if i == 0:
                                    metadata["_rowid"] = row[i + 2]
                                else:
                                    metadata[self.mdata_cols[i]] = row[i + 2]

                            if row[1] is None:
                                results.append(Document(text="", metadata=metadata))
                            else:
                                results.append(
                                    Document(text=str(row[1]), metadata=metadata)
                                )
                except Exception as ex:
                    print(f"An exception occurred :: {ex}")
                    traceback.print_exc()
                    cursor.close()
                    raise

            return results
        except Exception as ex:
            print(f"An exception occurred :: {ex}")
            traceback.print_exc()
            raise

    defload_data(self) -> List[Document]:
        return self.load()

```
 |  
| --- | --- |  
###  load [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oracleai/#llama_index.readers.oracleai.OracleReader.load "Permanent link")

```
load() -> []

```

Load data into Document objects...
Source code in `llama-index-integrations/readers/llama-index-readers-oracleai/llama_index/readers/oracleai/base.py`  
| 
```
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
```
 | 
```
defload(self) -> List[Document]:
"""Load data into Document objects..."""
    try:
        importoracledb
    except ImportError as e:
        raise ImportError(
            "Unable to import oracledb, please install with "
            "`pip install -U oracledb`."
        ) frome

    ncols = 0
    results = []
    metadata = {}
    m_params = {"plaintext": "false"}

    try:
        # extract the parameters
        if self.params is not None:
            self.file = self.params.get("file")
            self.dir = self.params.get("dir")
            self.owner = self.params.get("owner")
            self.tablename = self.params.get("tablename")
            self.colname = self.params.get("colname")
        else:
            raise Exception("Missing loader parameters")

        oracledb.defaults.fetch_lobs = False

        if self.file:
            doc = OracleDocReader.read_file(self.conn, self.file, m_params)

            if doc is None:
                return results

            results.append(doc)

        if self.dir:
            skip_count = 0
            if not (os.path.exists(self.dir) and os.path.isdir(self.dir)):
                raise Exception("Directory does not exist or invalid.")
            else:
                for file_name in os.listdir(self.dir):
                    file_path = os.path.join(self.dir, file_name)
                    if os.path.isfile(file_path):
                        doc = OracleDocReader.read_file(
                            self.conn, file_path, m_params
                        )

                        if doc is None:
                            skip_count = skip_count + 1
                            print(f"Total skipped: {skip_count}\n")
                        else:
                            results.append(doc)

        if self.tablename:
            try:
                if self.owner is None or self.colname is None:
                    raise Exception("Missing owner or column name")

                cursor = self.conn.cursor()
                self.mdata_cols = self.params.get("mdata_cols")
                if self.mdata_cols is not None:
                    if len(self.mdata_cols)  3:
                        raise Exception(
                            "Exceeds the max number of columns you can request for metadata."
                        )

                    # execute a query to get column data types
                    sql = (
                        "select column_name, data_type from all_tab_columns where owner = '"
                        + self.owner.upper()
                        + "' and "
                        + "table_name = '"
                        + self.tablename.upper()
                        + "'"
                    )

                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        if row[0] in self.mdata_cols:
                            if row[1] not in [
                                "NUMBER",
                                "BINARY_DOUBLE",
                                "BINARY_FLOAT",
                                "LONG",
                                "DATE",
                                "TIMESTAMP",
                                "VARCHAR2",
                            ]:
                                raise Exception(
                                    "The datatype for the column requested for metadata is not supported."
                                )

                self.mdata_cols_sql = ", rowid"
                if self.mdata_cols is not None:
                    for col in self.mdata_cols:
                        self.mdata_cols_sql = self.mdata_cols_sql + ", " + col

                # [TODO] use bind variables
                sql = (
                    "select dbms_vector_chain.utl_to_text(t."
                    + self.colname
                    + ", json('"
                    + json.dumps(m_params)
                    + "')) mdata, dbms_vector_chain.utl_to_text(t."
                    + self.colname
                    + ") text"
                    + self.mdata_cols_sql
                    + " from "
                    + self.owner
                    + "."
                    + self.tablename
                    + " t"
                )

                cursor.execute(sql)
                for row in cursor:
                    metadata = {}

                    if row is None:
                        doc_id = OracleDocReader.generate_object_id(
                            self.conn.username
                            + "$"
                            + self.owner
                            + "$"
                            + self.tablename
                            + "$"
                            + self.colname
                        )
                        metadata["_oid"] = doc_id
                        results.append(Document(text="", metadata=metadata))
                    else:
                        if row[0] is not None:
                            data = str(row[0])
                            if data.startswith(("<!DOCTYPE html", "<HTML>")):
                                p = ParseOracleDocMetadata()
                                p.feed(data)
                                metadata = p.get_metadata()

                        doc_id = OracleDocReader.generate_object_id(
                            self.conn.username
                            + "$"
                            + self.owner
                            + "$"
                            + self.tablename
                            + "$"
                            + self.colname
                            + "$"
                            + str(row[2])
                        )
                        metadata["_oid"] = doc_id
                        metadata["_rowid"] = row[2]

                        # process projected metadata cols
                        if self.mdata_cols is not None:
                            ncols = len(self.mdata_cols)

                        for i in range(ncols):
                            if i == 0:
                                metadata["_rowid"] = row[i + 2]
                            else:
                                metadata[self.mdata_cols[i]] = row[i + 2]

                        if row[1] is None:
                            results.append(Document(text="", metadata=metadata))
                        else:
                            results.append(
                                Document(text=str(row[1]), metadata=metadata)
                            )
            except Exception as ex:
                print(f"An exception occurred :: {ex}")
                traceback.print_exc()
                cursor.close()
                raise

        return results
    except Exception as ex:
        print(f"An exception occurred :: {ex}")
        traceback.print_exc()
        raise

```
 |  
| --- | --- |  
##  OracleTextSplitter [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oracleai/#llama_index.readers.oracleai.OracleTextSplitter "Permanent link")
Splitting text using Oracle chunker.
Source code in `llama-index-integrations/readers/llama-index-readers-oracleai/llama_index/readers/oracleai/base.py`  
| 
```
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
```
 | 
```
classOracleTextSplitter:
"""Splitting text using Oracle chunker."""

    def__init__(self, conn: Connection, params: Dict[str, Any]):
        self.conn = conn
        self.params = params

        try:
            importoracledb
        except ImportError as e:
            raise ImportError(
                "Unable to import oracledb, please install with "
                "`pip install -U oracledb`."
            ) frome

        self._oracledb = oracledb
        self._json = json

    defsplit_text(self, text: str) -> List[str]:
"""Split incoming text and return chunks."""
        splits = []

        try:
            cursor = self.conn.cursor()
            # returns strings or bytes instead of a locator
            self._oracledb.defaults.fetch_lobs = False

            cursor.setinputsizes(content=self._oracledb.CLOB)
            cursor.execute(
                "select t.* from dbms_vector_chain.utl_to_chunks(:content, json(:params)) t",
                content=text,
                params=self._json.dumps(self.params),
            )

            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                d = self._json.loads(row[0])
                splits.append(d["chunk_data"])

            return splits

        except Exception as ex:
            print(f"An exception occurred :: {ex}")
            traceback.print_exc()
            raise

```
 |  
| --- | --- |  
###  split_text [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oracleai/#llama_index.readers.oracleai.OracleTextSplitter.split_text "Permanent link")

```
split_text(text: ) -> []

```

Split incoming text and return chunks.
Source code in `llama-index-integrations/readers/llama-index-readers-oracleai/llama_index/readers/oracleai/base.py`  
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
426
427
428
429
430
431
432
433
```
 | 
```
defsplit_text(self, text: str) -> List[str]:
"""Split incoming text and return chunks."""
    splits = []

    try:
        cursor = self.conn.cursor()
        # returns strings or bytes instead of a locator
        self._oracledb.defaults.fetch_lobs = False

        cursor.setinputsizes(content=self._oracledb.CLOB)
        cursor.execute(
            "select t.* from dbms_vector_chain.utl_to_chunks(:content, json(:params)) t",
            content=text,
            params=self._json.dumps(self.params),
        )

        while True:
            row = cursor.fetchone()
            if row is None:
                break
            d = self._json.loads(row[0])
            splits.append(d["chunk_data"])

        return splits

    except Exception as ex:
        print(f"An exception occurred :: {ex}")
        traceback.print_exc()
        raise

```
 |  
| --- | --- |  
options: members: - OracleReader - OracleTextSplitter
