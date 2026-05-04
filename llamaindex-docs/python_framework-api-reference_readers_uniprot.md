# Uniprot
UniProt reader for LlamaIndex.
##  UniProtReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/uniprot/#llama_index.readers.uniprot.UniProtReader "Permanent link")
Bases: 
UniProt reader for LlamaIndex.
Reads UniProt Swiss-Prot format files and converts them into LlamaIndex Documents. Each record is converted into a document with structured text and metadata.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `include_fields`  |  `Optional[Set[str]]`  |  Set of fields to include in the output. Defaults to all fields.  |  `None`  |  
|  `max_records`  |  `Optional[int]`  |  Maximum number of records to parse. If None, parse all records.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-uniprot/llama_index/readers/uniprot/base.py`  
| 
```
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
```
 | 
```
classUniProtReader(BaseReader):
"""
    UniProt reader for LlamaIndex.

    Reads UniProt Swiss-Prot format files and converts them into LlamaIndex Documents.
    Each record is converted into a document with structured text and metadata.

    Args:
        include_fields (Optional[Set[str]]): Set of fields to include in the output.
            Defaults to all fields.
        max_records (Optional[int]): Maximum number of records to parse.
            If None, parse all records.

    """

    # Mapping of field names to their two-letter codes in UniProt format
    FIELD_CODES = {
        "id": "ID",
        "accession": "AC",
        "description": "DE",
        "gene_names": "GN",
        "organism": "OS",
        "comments": "CC",
        "keywords": "KW",
        "features": "FT",
        "sequence_length": "SQ",
        "sequence_mw": "SQ",
        "taxonomy": "OC",
        "taxonomy_id": "OX",
        "citations": "RN",
        "cross_references": "DR",
    }

    def__init__(
        self,
        include_fields: Optional[Set[str]] = None,
        max_records: Optional[int] = None,
    ) -> None:
"""Initialize with arguments."""
        super().__init__()

        self.include_fields = include_fields or {
            "id",
            "accession",
            "description",
            "gene_names",
            "organism",
            "comments",
            "keywords",
            "sequence_length",
            "sequence_mw",
            "taxonomy",
            "taxonomy_id",
            "citations",
            "cross_references",
        }

        self.max_records = max_records

        # Field codes we need to parse
        self.include_field_codes = {
            code
            for field_name, code in self.FIELD_CODES.items()
            if field_name in self.include_fields
        }

    defload_data(
        self, input_file: str, extra_info: Optional[Dict] = {}
    ) -> List[Document]:
"""Load data from the input file."""
        documents = []
        record_count = 0

        for record_lines in self._read_records(input_file):
            if self.max_records is not None and record_count >= self.max_records:
                break

            record = self._parse_record(record_lines)
            if record:
                document = self._record_to_document(record)
                document.metadata.update(extra_info)
                documents.append(document)
                record_count += 1

        return documents

    deflazy_load_data(
        self, input_file: str, extra_info: Optional[Dict] = {}
    ) -> Generator[Document, None, None]:
"""
        Load data from the input file lazily, yielding one document at a time.

        This method is memory efficient as it processes one record at a time instead of
        loading all records into memory at once. It's particularly useful for large UniProt files.

        Args:
            input_file (str): Path to the UniProt file
            extra_info (Optional[Dict]): Additional metadata to add to each document

        Yields:
            Document: One document at a time

        """
        record_count = 0

        for record_lines in self._read_records(input_file):
            if self.max_records is not None and record_count >= self.max_records:
                break

            record = self._parse_record(record_lines)
            if record:
                document = self._record_to_document(record)
                document.metadata.update(extra_info)
                yield document
                record_count += 1

    def_parse_record(self, lines: List[str]) -> Optional[UniProtRecord]:
"""Parse a single UniProt record from lines."""
        if not lines:
            return None

        record = UniProtRecord(
            id="",
            accession=[],
            description="",
            gene_names=[],
            organism="",
            comments=[],
            keywords=[],
            features=[],
            sequence_length=0,
            sequence_mw=0,
            dates=[],
            taxonomy=[],
            taxonomy_id={},
            cross_references=[],
            citations=[],
        )

        current_field = None

        for line in lines:
            if not line.strip():
                continue

            if line.startswith("//"):
                break

            field = line[:2]

            if field not in self.include_field_codes and current_field != "citations":
                continue

            value = line[5:].strip().rstrip(";")

            if field != "RA":
                # Remove trailing period
                # Do not remove trailing period from authors names
                value = value.rstrip(".")

            if field == "ID":
                record.id = value.split()[0]
                current_field = "id"
            elif field == "AC":
                record.accession = [acc.strip() for acc in value.split(";")]
                current_field = "accession"
            elif field == "DE":
                record.description = value
                current_field = "description"
            elif field == "GN":
                record.gene_names = [name.strip() for name in value.split(";")]
                current_field = "gene_names"
            elif field == "OS":
                record.organism = value
                current_field = "organism"
            elif field == "CC":
                if value.startswith("-!-"):
                    record.comments.append(value[4:])
                elif value.startswith("---"):
                    # Skip separator lines
                    continue
                elif any(word in value.lower() for word in ["copyright", "license"]):
                    # Skip standard UniProt footer comments
                    continue
                else:
                    record.comments.append(value)
                current_field = "comments"
            elif field == "KW":
                # Handle multiple KW lines by extending the list
                record.keywords.extend([kw.strip() for kw in value.split(";")])
                current_field = "keywords"
            elif field == "FT":
                if value:
                    feature_parts = value.split()
                    if len(feature_parts) >= 2:
                        record.features.append(
                            {
                                "type": feature_parts[0],
                                "location": feature_parts[1],
                                "description": " ".join(feature_parts[2:])
                                if len(feature_parts)  2
                                else "",
                            }
                        )
                current_field = "features"
            elif field == "SQ":
                if "SEQUENCE" in value:
                    parts = value.split(";")
                    record.sequence_length = int(parts[0].split()[1])
                    record.sequence_mw = int(parts[1].split()[0])
                current_field = "sequence"
            elif field == "OC":
                record.taxonomy.extend(value.split("; "))
            elif field == "OX":
                # Parse taxonomy database qualifier and code
                # Format: OX   Taxonomy_database_Qualifier=Taxonomic code;
                parts = value.split("=")
                if len(parts) == 2:
                    record.taxonomy_id = {"database": parts[0], "code": parts[1]}
            elif field == "RN":
                # Start a new citation block
                current_citation = {
                    "number": value.strip("[]"),
                    "position": [],
                    "comment": [],
                    "cross_references": [],
                    "authors": "",
                    "title": "",
                    "location": [],
                }

                record.citations.append(current_citation)
                current_field = "citations"
            elif field == "RP" and current_field == "citations":
                current_citation["position"].append(value)
            elif field == "RC" and current_field == "citations":
                current_citation["comment"].append(value)
            elif field == "RX" and current_field == "citations":
                current_citation["cross_references"].append(value)
            elif field == "RA" and current_field == "citations":
                # Concatenate author lines with space
                current_citation["authors"] = (
                    current_citation["authors"] + " " + value
                ).strip()
            elif field == "RT" and current_field == "citations":
                # Concatenate title lines with space and remove quotes
                title = (current_citation["title"] + " " + value).strip()
                current_citation["title"] = title.strip('"')
            elif field == "RL" and current_field == "citations":
                current_citation["location"].append(value)
            elif field == "DR":
                # Parse database cross-references
                # Format: DR   RESOURCE_ABBREVIATION; RESOURCE_IDENTIFIER; OPTIONAL_INFORMATION_1[; OPTIONAL_INFORMATION_2][; OPTIONAL_INFORMATION_3].
                parts = value.split("; ")
                if len(parts) >= 2:
                    record.cross_references.append(
                        {
                            "abbrev": parts[0],
                            "id": parts[1],
                            "info": parts[2:],
                        }
                    )
                current_field = "cross_references"

        return record

    def_record_to_document(self, record: UniProtRecord) -> Document:
"""Convert a UniProt record to a LlamaIndex Document."""
        text_parts = []

        if "id" in self.include_fields:
            text_parts.append(f"Protein ID: {record.id}")
        if "accession" in self.include_fields:
            text_parts.append(f"Accession numbers: {', '.join(record.accession)}")
        if "description" in self.include_fields:
            text_parts.append(f"Description: {record.description}")
        if "gene_names" in self.include_fields:
            text_parts.append(f"Gene names: {', '.join(record.gene_names)}")
        if "organism" in self.include_fields:
            text_parts.append(f"Organism: {record.organism}")
        if "comments" in self.include_fields:
            text_parts.append("Comments:")
            text_parts.extend(f"- {comment}" for comment in record.comments)
        if "keywords" in self.include_fields:
            text_parts.append(f"Keywords: {', '.join(record.keywords)}")
        if "features" in self.include_fields:
            text_parts.append("Features:")
            text_parts.extend(
                f"- {feature['type']} ({feature['location']}): {feature['description']}"
                for feature in record.features
            )
        if "sequence_length" in self.include_fields:
            text_parts.append(f"Sequence length: {record.sequence_length} AA")
        if "sequence_mw" in self.include_fields:
            text_parts.append(f"Molecular weight: {record.sequence_mw} Da")
        if "taxonomy" in self.include_fields:
            # Clean up taxonomy by removing empty entries and joining with proper hierarchy
            clean_taxonomy = [t for t in record.taxonomy if t]
            text_parts.append("Taxonomy:")
            text_parts.append("  " + " > ".join(clean_taxonomy))
        if "taxonomy_id" in self.include_fields and record.taxonomy_id:
            text_parts.append(
                f"Taxonomy ID: {record.taxonomy_id['database']}{record.taxonomy_id['code']}"
            )
        if "cross_references" in self.include_fields:
            text_parts.append("Cross-references:")
            for ref in record.cross_references:
                text_parts.append(
                    f"- {ref['abbrev']}: {ref['id']}" + (f" - {'; '.join(ref['info'])}")
                )

        if "citations" in self.include_fields and record.citations:
            text_parts.append("Citations:")

            for citation in record.citations:
                text_parts.append(f"Reference {citation['number']}:")
                if citation["position"]:
                    text_parts.append("  Position: " + " ".join(citation["position"]))
                if citation["title"]:
                    text_parts.append("  Title: " + citation["title"])
                if citation["authors"]:
                    text_parts.append("  Authors: " + citation["authors"])
                if citation["location"]:
                    text_parts.append("  Location: " + " ".join(citation["location"]))
                if citation["comment"]:
                    text_parts.append("  Comments: " + " ".join(citation["comment"]))
                if citation["cross_references"]:
                    text_parts.append(
                        "  Cross-references: " + " ".join(citation["cross_references"])
                    )

        metadata = {
            "id": record.id,
        }

        return Document(text="\n".join(text_parts), metadata=metadata)

    def_read_records(self, file_path: str) -> Generator[List[str], None, None]:
"""Read UniProt records from file."""
        current_record = []

        with open(file_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("//"):
                    if current_record:
                        yield current_record
                        current_record = []
                else:
                    current_record.append(line)

            if current_record:
                yield current_record

    defcount_records(self, file_path: str) -> int:
"""
        Count the total number of protein records in the UniProt database file.

        Uses grep to efficiently count lines starting with "//" which is much faster
        than reading the file line by line.

        Args:
            file_path (str): Path to the UniProt database file

        Returns:
            int: Total number of protein records in the file

        """
        count = 0

        with open(file_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("//"):
                    count += 1

        return count

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/uniprot/#llama_index.readers.uniprot.UniProtReader.load_data "Permanent link")

```
load_data(
    input_file: , extra_info: Optional[] = {}
) -> []

```

Load data from the input file.
Source code in `llama-index-integrations/readers/llama-index-readers-uniprot/llama_index/readers/uniprot/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, input_file: str, extra_info: Optional[Dict] = {}
) -> List[Document]:
"""Load data from the input file."""
    documents = []
    record_count = 0

    for record_lines in self._read_records(input_file):
        if self.max_records is not None and record_count >= self.max_records:
            break

        record = self._parse_record(record_lines)
        if record:
            document = self._record_to_document(record)
            document.metadata.update(extra_info)
            documents.append(document)
            record_count += 1

    return documents

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/uniprot/#llama_index.readers.uniprot.UniProtReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    input_file: , extra_info: Optional[] = {}
) -> Generator[, None, None]

```

Load data from the input file lazily, yielding one document at a time.
This method is memory efficient as it processes one record at a time instead of loading all records into memory at once. It's particularly useful for large UniProt files.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_file`  |  Path to the UniProt file  |  _required_  |  
|  `extra_info`  |  `Optional[Dict]`  |  Additional metadata to add to each document  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |   |  One document at a time  |  
Source code in `llama-index-integrations/readers/llama-index-readers-uniprot/llama_index/readers/uniprot/base.py`  
| 
```
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
```
 | 
```
deflazy_load_data(
    self, input_file: str, extra_info: Optional[Dict] = {}
) -> Generator[Document, None, None]:
"""
    Load data from the input file lazily, yielding one document at a time.

    This method is memory efficient as it processes one record at a time instead of
    loading all records into memory at once. It's particularly useful for large UniProt files.

    Args:
        input_file (str): Path to the UniProt file
        extra_info (Optional[Dict]): Additional metadata to add to each document

    Yields:
        Document: One document at a time

    """
    record_count = 0

    for record_lines in self._read_records(input_file):
        if self.max_records is not None and record_count >= self.max_records:
            break

        record = self._parse_record(record_lines)
        if record:
            document = self._record_to_document(record)
            document.metadata.update(extra_info)
            yield document
            record_count += 1

```
 |  
| --- | --- |  
###  count_records [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/uniprot/#llama_index.readers.uniprot.UniProtReader.count_records "Permanent link")

```
count_records(file_path: ) -> 

```

Count the total number of protein records in the UniProt database file.
Uses grep to efficiently count lines starting with "//" which is much faster than reading the file line by line.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_path`  |  Path to the UniProt database file  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `int`  |  Total number of protein records in the file  |  
Source code in `llama-index-integrations/readers/llama-index-readers-uniprot/llama_index/readers/uniprot/base.py`  
| 
```
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
```
 | 
```
defcount_records(self, file_path: str) -> int:
"""
    Count the total number of protein records in the UniProt database file.

    Uses grep to efficiently count lines starting with "//" which is much faster
    than reading the file line by line.

    Args:
        file_path (str): Path to the UniProt database file

    Returns:
        int: Total number of protein records in the file

    """
    count = 0

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("//"):
                count += 1

    return count

```
 |  
| --- | --- |  
options: members: - UniProtReader
