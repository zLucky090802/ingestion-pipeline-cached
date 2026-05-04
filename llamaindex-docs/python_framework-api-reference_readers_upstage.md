# Upstage
##  UpstageLayoutAnalysisReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/upstage/#llama_index.readers.upstage.UpstageLayoutAnalysisReader "Permanent link")
Bases: 
Upstage Layout Analysis Reader.
To use, you should have the environment variable `UPSTAGE_API_KEY` set with your API key or pass it as a named parameter to the constructor.
Example
.. code-block:: python

```
from llama_index.readers.file import UpstageLayoutAnalysisReader

reader = UpstageLayoutAnalysisReader()

docs = reader.load_data("path/to/file.pdf")

```
Source code in `llama-index-integrations/readers/llama-index-readers-upstage/llama_index/readers/upstage/base.py`  
| 
```
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
```
 | 
```
classUpstageLayoutAnalysisReader(BaseReader):
"""
    Upstage Layout Analysis Reader.

    To use, you should have the environment variable `UPSTAGE_API_KEY`
    set with your API key or pass it as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from llama_index.readers.file import UpstageLayoutAnalysisReader

            reader = UpstageLayoutAnalysisReader()

            docs = reader.load_data("path/to/file.pdf")

    """

    def__init__(
        self,
        api_key: Optional[str] = None,
        use_ocr: bool = False,
        exclude: list = ["header", "footer"],
    ):
"""
        Initializes an instance of the Upstage class.

        Args:
            api_key (str, optional): The API key for accessing the Upstage API.
                                     Defaults to None, in which case it will be
                                     fetched from the environment variable
                                     `UPSTAGE_API_KEY`.
            use_ocr (bool, optional): Extract text from images in the document.
                                      Defaults to False. (Use text info in PDF file)
            exclude (list, optional): Exclude specific elements from the output.
                                      Defaults to [] (all included).

        """
        self.api_key = get_from_param_or_env(
            "UPSTAGE_API_KEY", api_key, "UPSTAGE_API_KEY"
        )
        self.use_ocr = use_ocr
        self.exclude = exclude

        validate_api_key(self.api_key)

    def_get_response(self, files: Dict) -> List:
"""
        Sends a POST request to the API endpoint with the provided files and
        returns the response.

        Args:
            files (dict): A dictionary containing the files to be sent in the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ValueError: If there is an error in the API call.

        """
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            options = {"ocr": self.use_ocr}
            response = requests.post(
                LAYOUT_ANALYSIS_URL, headers=headers, files=files, data=options
            )
            response.raise_for_status()

            result = response.json().get("elements", [])

            return [
                element for element in result if element["category"] not in self.exclude
            ]

        except requests.RequestException as req_err:
            # Handle any request-related exceptions
            print(f"Request Exception: {req_err}")
            raise ValueError(f"Failed to send request to Upstage API: {req_err}")
        except json.JSONDecodeError as json_err:
            # Handle JSON decode errors
            print(f"JSON Decode Error: {json_err}")
            raise ValueError(f"Failed to decode JSON response: {json_err}")

    def_split_and_request(
        self,
        full_docs: fitzDocument,
        start_page: int,
        num_pages: int,
    ) -> List:
"""
        Splits the full pdf document into partial pages and sends a request to the
        server.

        Args:
            full_docs (str): The full document to be split and requested.
            start_page (int): The starting page number for splitting the document.
            num_pages (int, optional): The number of pages to split the document
                                       into.
                                       Defaults to DEFAULT_NUMBER_OF_PAGE.

        Returns:
            response: The response from the server.

        """
        with fitz.open() as chunk_pdf:
            chunk_pdf.insert_pdf(
                full_docs,
                from_page=start_page,
                to_page=start_page + num_pages - 1,
            )
            pdf_bytes = chunk_pdf.write()

        with io.BytesIO(pdf_bytes) as f:
            return self._get_response({"document": f})

    def_element_document(
        self, element: Dict, output_type: OutputType, split: SplitType
    ) -> Document:
"""
        Converts an elements into a Document object.

        Args:
            element (Dict): The element to be converted into a Document object.
            output_type (OutputType): The output type of the document.
            split (SplitType): The split type of the document.

        Returns:
            Document: A Document object representing the element with its content
                      and metadata.

        """
        return Document(
            text=(parse_output(element, output_type)),
            extra_info={
                "page": element["page"],
                "id": element["id"],
                "type": output_type,
                "split": split,
                "bounding_box": json.dumps(element["bounding_box"]),
            },
        )

    def_page_document(
        self, elements: List, output_type: OutputType, split: SplitType
    ) -> List[Document]:
"""
        Combines elements with the same page number into a single Document object.

        Args:
            elements (List): A list of elements containing page numbers.
            output_type (OutputType): The output type of the document.
            split (SplitType): The split type of the document.

        Returns:
            List[Document]: A list of Document objects, each representing a page
                            with its content and metadata.

        """
        _docs = []
        pages = sorted({x["page"] for x in elements})

        page_group = [
            [element for element in elements if element["page"] == x] for x in pages
        ]

        for group in page_group:
            page_content = " ".join(
                [parse_output(element, output_type) for element in group]
            )

            _docs.append(
                Document(
                    text=page_content.strip(),
                    extra_info={
                        "page": group[0]["page"],
                        "type": output_type,
                        "split": split,
                    },
                )
            )

        return _docs

    deflazy_load_data(
        self,
        file_path: Union[str, Path, List[str], List[Path]],
        output_type: Union[OutputType, dict] = "html",
        split: SplitType = "none",
    ) -> Iterable[Document]:
"""
        Load data from a file or list of files lazily.

        Args:
            file_path (Union[str, Path, List[str], List[Path]]): The path or list of paths to the file(s) to load.
            output_type (Union[OutputType, dict], optional): The desired output type. Defaults to "html".
                - If a dict is provided, it should be in the format {"category": "output_type", ...}.
                - The category could possibly include the following:
                    - "paragraph"
                    - "caption"
                    - "table"
                    - "figure"
                    - "equation"
                    - "footer"
                    - "header"
                - The output_type can be "text" or "html".
            split (SplitType, optional): The type of splitting to apply. Defaults to "none".

        Returns:
            List[Document]: A list of Document objects containing the loaded data.

        Raises:
            ValueError: If an invalid split type is provided or if file_path is required.

        """
        # Check if the file path is a list of paths
        if isinstance(file_path, list):
            for path in file_path:
                docs = self.load_data(path, output_type, split)
                yield from docs

        else:
            num_pages = DEFAULT_NUMBER_OF_PAGE

            if not file_path:
                raise ValueError("file_path is required.")

            validate_file_path(file_path)

            full_docs = fitz.open(file_path)
            number_of_pages = full_docs.page_count

            if split == "none":
                if full_docs.is_pdf:
                    result = ""
                    start_page = 0
                    for _ in range(number_of_pages):
                        if start_page >= number_of_pages:
                            break

                        elements = self._split_and_request(
                            full_docs, start_page, num_pages
                        )
                        for element in elements:
                            result += parse_output(element, output_type)

                        start_page += num_pages

                else:
                    with open(file_path, "rb") as f:
                        elements = self._get_response({"document": f})

                    result = ""
                    for element in elements:
                        result += parse_output(element, output_type)

                yield Document(
                    text=result,
                    extra_info={
                        "total_pages": number_of_pages,
                        "type": output_type,
                        "split": split,
                    },
                )

            elif split == "element":
                if full_docs.is_pdf:
                    start_page = 0
                    for _ in range(number_of_pages):
                        if start_page >= number_of_pages:
                            break

                        elements = self._split_and_request(
                            full_docs, start_page, num_pages
                        )
                        for element in elements:
                            yield self._element_document(element, output_type, split)

                        start_page += num_pages

                else:
                    with open(file_path, "rb") as f:
                        elements = self._get_response({"document": f})

                    for element in elements:
                        yield self._element_document(element, output_type, split)

            elif split == "page":
                if full_docs.is_pdf:
                    start_page = 0
                    for _ in range(number_of_pages):
                        if start_page >= number_of_pages:
                            break

                        elements = self._split_and_request(
                            full_docs, start_page, num_pages
                        )
                        yield from self._page_document(elements, output_type, split)

                        start_page += num_pages
                else:
                    with open(file_path, "rb") as f:
                        elements = self._get_response({"document": f})

                    yield from self._page_document(elements, output_type, split)

            else:
                raise ValueError(f"Invalid split type: {split}")

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/upstage/#llama_index.readers.upstage.UpstageLayoutAnalysisReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    file_path: Union[, , [], []],
    output_type: Union[OutputType, ] = "html",
    split: SplitType = "none",
) -> Iterable[]

```

Load data from a file or list of files lazily.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_path`  |  `Union[str, Path, List[str], List[Path]]`  |  The path or list of paths to the file(s) to load.  |  _required_  |  
|  `output_type`  |  `Union[OutputType, dict]`  |  The desired output type. Defaults to "html". - If a dict is provided, it should be in the format {"category": "output_type", ...}. - The category could possibly include the following: - "paragraph" - "caption" - "table" - "figure" - "equation" - "footer" - "header" - The output_type can be "text" or "html".  |  `'html'`  |  
|  `split`  |  `SplitType`  |  The type of splitting to apply. Defaults to "none".  |  `'none'`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Iterable[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  List[Document]: A list of Document objects containing the loaded data.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If an invalid split type is provided or if file_path is required.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-upstage/llama_index/readers/upstage/base.py`  
| 
```
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
```
 | 
```
deflazy_load_data(
    self,
    file_path: Union[str, Path, List[str], List[Path]],
    output_type: Union[OutputType, dict] = "html",
    split: SplitType = "none",
) -> Iterable[Document]:
"""
    Load data from a file or list of files lazily.

    Args:
        file_path (Union[str, Path, List[str], List[Path]]): The path or list of paths to the file(s) to load.
        output_type (Union[OutputType, dict], optional): The desired output type. Defaults to "html".
            - If a dict is provided, it should be in the format {"category": "output_type", ...}.
            - The category could possibly include the following:
                - "paragraph"
                - "caption"
                - "table"
                - "figure"
                - "equation"
                - "footer"
                - "header"
            - The output_type can be "text" or "html".
        split (SplitType, optional): The type of splitting to apply. Defaults to "none".

    Returns:
        List[Document]: A list of Document objects containing the loaded data.

    Raises:
        ValueError: If an invalid split type is provided or if file_path is required.

    """
    # Check if the file path is a list of paths
    if isinstance(file_path, list):
        for path in file_path:
            docs = self.load_data(path, output_type, split)
            yield from docs

    else:
        num_pages = DEFAULT_NUMBER_OF_PAGE

        if not file_path:
            raise ValueError("file_path is required.")

        validate_file_path(file_path)

        full_docs = fitz.open(file_path)
        number_of_pages = full_docs.page_count

        if split == "none":
            if full_docs.is_pdf:
                result = ""
                start_page = 0
                for _ in range(number_of_pages):
                    if start_page >= number_of_pages:
                        break

                    elements = self._split_and_request(
                        full_docs, start_page, num_pages
                    )
                    for element in elements:
                        result += parse_output(element, output_type)

                    start_page += num_pages

            else:
                with open(file_path, "rb") as f:
                    elements = self._get_response({"document": f})

                result = ""
                for element in elements:
                    result += parse_output(element, output_type)

            yield Document(
                text=result,
                extra_info={
                    "total_pages": number_of_pages,
                    "type": output_type,
                    "split": split,
                },
            )

        elif split == "element":
            if full_docs.is_pdf:
                start_page = 0
                for _ in range(number_of_pages):
                    if start_page >= number_of_pages:
                        break

                    elements = self._split_and_request(
                        full_docs, start_page, num_pages
                    )
                    for element in elements:
                        yield self._element_document(element, output_type, split)

                    start_page += num_pages

            else:
                with open(file_path, "rb") as f:
                    elements = self._get_response({"document": f})

                for element in elements:
                    yield self._element_document(element, output_type, split)

        elif split == "page":
            if full_docs.is_pdf:
                start_page = 0
                for _ in range(number_of_pages):
                    if start_page >= number_of_pages:
                        break

                    elements = self._split_and_request(
                        full_docs, start_page, num_pages
                    )
                    yield from self._page_document(elements, output_type, split)

                    start_page += num_pages
            else:
                with open(file_path, "rb") as f:
                    elements = self._get_response({"document": f})

                yield from self._page_document(elements, output_type, split)

        else:
            raise ValueError(f"Invalid split type: {split}")

```
 |  
| --- | --- |  
##  UpstageDocumentParseReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/upstage/#llama_index.readers.upstage.UpstageDocumentParseReader "Permanent link")
Bases: 
Upstage Document Parse Reader.
To use, you should have the environment variable `UPSTAGE_API_KEY` set with your API key or pass it as a named parameter to the constructor.
Example
.. code-block:: python

```
from llama_index.readers.file import UpstageDocumentParseReader

reader = UpstageDocumentParseReader()

docs = reader.load_data("path/to/file.pdf")

```
Source code in `llama-index-integrations/readers/llama-index-readers-upstage/llama_index/readers/upstage/document_parse.py`  
| 
```
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
```
 | 
```
classUpstageDocumentParseReader(BaseReader):
"""
    Upstage Document Parse Reader.

    To use, you should have the environment variable `UPSTAGE_API_KEY`
    set with your API key or pass it as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from llama_index.readers.file import UpstageDocumentParseReader

            reader = UpstageDocumentParseReader()

            docs = reader.load_data("path/to/file.pdf")

    """

    def__init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DOCUMENT_PARSE_BASE_URL,
        model: str = DOCUMENT_PARSE_DEFAULT_MODEL,
        split: SplitType = "none",
        ocr: OCR = "auto",
        output_format: OutputFormat = "html",
        coordinates: bool = True,
        base64_encoding: List[Category] = [],
    ):
"""
        Initializes an instance of the Upstage Document Parse Reader class.

        Args:
            api_key (str, optional): The API key for accessing the Upstage API.
                                     Defaults to None, in which case it will be
                                     fetched from the environment variable
                                     `UPSTAGE_API_KEY`.
            base_url (str, optional): The base URL for accessing the Upstage API.
            split (SplitType, optional): The type of splitting to be applied.
                                         Defaults to "none" (no splitting).
            model (str): The model to be used for the document parse.
                         Defaults to "document-parse".
            ocr (OCRMode, optional): Extract text from images in the document using OCR.
                                     If the value is "force", OCR is used to extract
                                     text from an image. If the value is "auto", text is
                                     extracted from a PDF. (An error will occur if the
                                     value is "auto" and the input is NOT in PDF format)
            output_format (OutputFormat, optional): Format of the inference results.
            coordinates (bool, optional): Whether to include the coordinates of the
                                          OCR in the output.
            base64_encoding (List[Category], optional): The category of the elements to
                                                        be encoded in base64.

        """
        self.api_key = get_from_param_or_env(
            "UPSTAGE_API_KEY", api_key, "UPSTAGE_API_KEY"
        )
        self.base_url = base_url
        self.model = model
        self.split = split
        self.ocr = ocr
        self.output_format = output_format
        self.coordinates = coordinates
        self.base64_encoding = base64_encoding

    def_get_response(
        self,
        files: Dict,
    ) -> List:
"""
        Sends a POST request to the API endpoint with the provided files and
        returns the response.

        Args:
            files (dict): A dictionary containing the files to be sent in the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ValueError: If there is an error in the API call.

        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            response = requests.post(
                self.base_url,
                headers=headers,
                files=files,
                data={
                    "ocr": self.ocr,
                    "model": self.model,
                    "output_formats": f"['{self.output_format}']",
                    "coordinates": self.coordinates,
                    "base64_encoding": f"{self.base64_encoding}",
                },
            )
            response.raise_for_status()
            return response.json().get("elements", [])

        except requests.HTTPError as e:
            raise ValueError(f"HTTP error: {e.response.text}")
        except requests.RequestException as e:
            # Handle any request-related exceptions
            raise ValueError(f"Failed to send request: {e}")
        except json.JSONDecodeError as e:
            # Handle JSON decode errors
            raise ValueError(f"Failed to decode JSON response: {e}")
        except Exception as e:
            # Handle any other exceptions
            raise ValueError(f"An error occurred: {e}")

    def_split_and_request(
        self,
        full_docs: fitzDocument,
        start_page: int,
        num_pages: int,
    ) -> List:
"""
        Splits the full pdf document into partial pages and sends a request to the
        server.

        Args:
            full_docs (str): The full document to be split and requested.
            start_page (int): The starting page number for splitting the document.
            num_pages (int, optional): The number of pages to split the document
                                       into.
                                       Defaults to DEFAULT_NUMBER_OF_PAGE.

        Returns:
            response: The response from the server.

        """
        with fitz.open() as chunk_pdf:
            chunk_pdf.insert_pdf(
                full_docs,
                from_page=start_page,
                to_page=start_page + num_pages - 1,
            )
            pdf_bytes = chunk_pdf.write()

        with io.BytesIO(pdf_bytes) as buffer:
            return self._get_response({"document": buffer})

    def_element_document(self, element: Dict) -> Document:
"""
        Converts an elements into a Document object.

        Args:
            element (Dict): The element to be converted into a Document object.

        Returns:
            Document: A Document object representing the element with its content
                      and metadata.

        """
        extra_info = {
            "page": element["page"],
            "id": element["id"],
            "output_format": self.output_format,
            "split": self.split,
            "category": element.get("category"),
        }
        if element.get("coordinates") is not None:
            extra_info["coordinates"] = element.get("coordinates")
        if element.get("base64_encoding") is not None:
            extra_info["base64_encoding"] = element.get("base64_encoding")

        return Document(
            text=(parse_output(element, self.output_format)), extra_info=extra_info
        )

    def_page_document(self, elements: List) -> List[Document]:
"""
        Combines elements with the same page number into a single Document object.

        Args:
            elements (List): A list of elements containing page numbers.

        Returns:
            List[Document]: A list of Document objects, each representing a page
                            with its content and metadata.

        """
        _docs = []
        pages = sorted({x["page"] for x in elements})

        page_group = [
            [element for element in elements if element["page"] == x] for x in pages
        ]

        for group in page_group:
            page_content = " ".join(
                [parse_output(element, self.output_format) for element in group]
            )

            coordinates = [
                element.get("coordinates")
                for element in group
                if element.get("coordinates") is not None
            ]

            base64_encodings = [
                element.get("base64_encoding")
                for element in group
                if element.get("base64_encoding") is not None
            ]
            extra_info = {
                "page": group[0]["page"],
                "output_format": self.output_format,
                "split": self.split,
            }

            if coordinates:
                extra_info["coordinates"] = coordinates

            if base64_encodings:
                extra_info["base64_encodings"] = base64_encodings

            _docs.append(
                Document(
                    text=page_content.strip(),
                    extra_info=extra_info,
                )
            )

        return _docs

    deflazy_load_data(
        self,
        file_path: Union[str, Path, List[str], List[Path]],
    ) -> Iterable[Document]:
"""
        Load data from a file or list of files lazily.

        Args:
            file_path (Union[str, Path, List[str], List[Path]]): The path or list of paths to the file(s) to load.

        Returns:
            List[Document]: A list of Document objects containing the loaded data.

        Raises:
            ValueError: If an invalid split type is provided or if file_path is required.

        """
        # Check if the file path is a list of paths
        if isinstance(file_path, list):
            for path in file_path:
                docs = self.load_data(path)
                yield from docs

        else:
            num_pages = DEFAULT_NUMBER_OF_PAGE

            if not file_path:
                raise ValueError("file_path is required.")

            validate_file_path(file_path)

            full_docs = fitz.open(file_path)
            number_of_pages = full_docs.page_count

            if self.split == "none":
                if full_docs.is_pdf:
                    result = ""
                    start_page = 0
                    for _ in range(number_of_pages):
                        if start_page >= number_of_pages:
                            break

                        elements = self._split_and_request(
                            full_docs, start_page, num_pages
                        )
                        for element in elements:
                            result += parse_output(element, self.output_format)

                        start_page += num_pages

                else:
                    with open(file_path, "rb") as f:
                        elements = self._get_response({"document": f})

                    result = ""
                    for element in elements:
                        result += parse_output(element, self.output_format)

                yield Document(
                    text=result,
                    extra_info={
                        "total_pages": number_of_pages,
                        "type": self.output_format,
                        "split": self.split,
                    },
                )

            elif self.split == "element":
                if full_docs.is_pdf:
                    start_page = 0
                    for _ in range(number_of_pages):
                        if start_page >= number_of_pages:
                            break

                        elements = self._split_and_request(
                            full_docs, start_page, num_pages
                        )
                        for element in elements:
                            yield self._element_document(element)

                        start_page += num_pages

                else:
                    with open(file_path, "rb") as f:
                        elements = self._get_response({"document": f})

                    for element in elements:
                        yield self._element_document(element)

            elif self.split == "page":
                if full_docs.is_pdf:
                    start_page = 0
                    for _ in range(number_of_pages):
                        if start_page >= number_of_pages:
                            break

                        elements = self._split_and_request(
                            full_docs, start_page, num_pages
                        )
                        yield from self._page_document(elements)

                        start_page += num_pages
                else:
                    with open(file_path, "rb") as f:
                        elements = self._get_response({"document": f})

                    yield from self._page_document(elements)

            else:
                raise ValueError(f"Invalid split type: {self.split}")

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/upstage/#llama_index.readers.upstage.UpstageDocumentParseReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    file_path: Union[, , [], []]
) -> Iterable[]

```

Load data from a file or list of files lazily.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_path`  |  `Union[str, Path, List[str], List[Path]]`  |  The path or list of paths to the file(s) to load.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `Iterable[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  List[Document]: A list of Document objects containing the loaded data.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If an invalid split type is provided or if file_path is required.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-upstage/llama_index/readers/upstage/document_parse.py`  
| 
```
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
```
 | 
```
deflazy_load_data(
    self,
    file_path: Union[str, Path, List[str], List[Path]],
) -> Iterable[Document]:
"""
    Load data from a file or list of files lazily.

    Args:
        file_path (Union[str, Path, List[str], List[Path]]): The path or list of paths to the file(s) to load.

    Returns:
        List[Document]: A list of Document objects containing the loaded data.

    Raises:
        ValueError: If an invalid split type is provided or if file_path is required.

    """
    # Check if the file path is a list of paths
    if isinstance(file_path, list):
        for path in file_path:
            docs = self.load_data(path)
            yield from docs

    else:
        num_pages = DEFAULT_NUMBER_OF_PAGE

        if not file_path:
            raise ValueError("file_path is required.")

        validate_file_path(file_path)

        full_docs = fitz.open(file_path)
        number_of_pages = full_docs.page_count

        if self.split == "none":
            if full_docs.is_pdf:
                result = ""
                start_page = 0
                for _ in range(number_of_pages):
                    if start_page >= number_of_pages:
                        break

                    elements = self._split_and_request(
                        full_docs, start_page, num_pages
                    )
                    for element in elements:
                        result += parse_output(element, self.output_format)

                    start_page += num_pages

            else:
                with open(file_path, "rb") as f:
                    elements = self._get_response({"document": f})

                result = ""
                for element in elements:
                    result += parse_output(element, self.output_format)

            yield Document(
                text=result,
                extra_info={
                    "total_pages": number_of_pages,
                    "type": self.output_format,
                    "split": self.split,
                },
            )

        elif self.split == "element":
            if full_docs.is_pdf:
                start_page = 0
                for _ in range(number_of_pages):
                    if start_page >= number_of_pages:
                        break

                    elements = self._split_and_request(
                        full_docs, start_page, num_pages
                    )
                    for element in elements:
                        yield self._element_document(element)

                    start_page += num_pages

            else:
                with open(file_path, "rb") as f:
                    elements = self._get_response({"document": f})

                for element in elements:
                    yield self._element_document(element)

        elif self.split == "page":
            if full_docs.is_pdf:
                start_page = 0
                for _ in range(number_of_pages):
                    if start_page >= number_of_pages:
                        break

                    elements = self._split_and_request(
                        full_docs, start_page, num_pages
                    )
                    yield from self._page_document(elements)

                    start_page += num_pages
            else:
                with open(file_path, "rb") as f:
                    elements = self._get_response({"document": f})

                yield from self._page_document(elements)

        else:
            raise ValueError(f"Invalid split type: {self.split}")

```
 |  
| --- | --- |  
options: members: - UpstageDocumentReader
