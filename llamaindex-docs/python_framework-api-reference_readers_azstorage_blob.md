# Azstorage blob
##  AzStorageBlobReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/azstorage_blob/#llama_index.readers.azstorage_blob.AzStorageBlobReader "Permanent link")
Bases: , , 
General reader for any Azure Storage Blob file or directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `container_name`  |  name of the container for the blob.  |  _required_  |  
|  `blob`  |  `Optional[str]`  |  name of the file to download. If none specified this loader will iterate through list of blobs in the container.  |  _required_  |  
|  `name_starts_with`  |  `Optional[str]`  |  filter the list of blobs to download to only those whose names begin with the specified string.  |  _required_  |  
|  `include`  |  (Union[str, List[str], None]): Specifies one or more additional datasets to include in the response. Options include: 'snapshots', 'metadata', 'uncommittedblobs', 'copy', 'deleted', 'deletedwithversions', 'tags', 'versions', 'immutabilitypolicy', 'legalhold'.  |  _required_  |  
|  `file_extractor`  |  `Optional[Dict[str, Union[str, BaseReader[](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader "BaseReader \(llama_index.core.readers.base.BaseReader\)")]]]`  |  A mapping of file extension to a BaseReader class that specifies how to convert that file to text. See `SimpleDirectoryReader` for more details, or call this path `llama_index.readers.file.base.DEFAULT_FILE_READER_CLS`.  |  _required_  |  
|  `connection_string`  |  A connection string which can be found under a storage account's "Access keys" security tab. This parameter  |  _required_  |  
|  `account_url`  |  URI to the storage account, may include SAS token.  |  _required_  |  
|  `credential`  |  `Union[str, Dict[str, str], AzureNamedKeyCredential, AzureSasCredential, TokenCredential, None] = None`  |  The credentials with which to authenticate. This is optional if the account URL already has a SAS token.  |  _required_  |  
|  `file_metadata_fn`  |  `Optional[Callable[str, Dict]]`  |  A function that takes in a filename and returns a Dict of metadata for the Document. Default is None.  |  _required_  |  
|  `filename_as_id`  |  `bool`  |  Whether to use the filename as the document id. False by default.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-azstorage-blob/llama_index/readers/azstorage_blob/base.py`  
| 
```
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
```
 | 
```
classAzStorageBlobReader(
    BasePydanticReader, ResourcesReaderMixin, FileSystemReaderMixin
):
"""
    General reader for any Azure Storage Blob file or directory.

    Args:
        container_name (str): name of the container for the blob.
        blob (Optional[str]): name of the file to download. If none specified
            this loader will iterate through list of blobs in the container.
        name_starts_with (Optional[str]): filter the list of blobs to download
            to only those whose names begin with the specified string.
        include: (Union[str, List[str], None]): Specifies one or more additional
            datasets to include in the response. Options include: 'snapshots',
            'metadata', 'uncommittedblobs', 'copy', 'deleted',
            'deletedwithversions', 'tags', 'versions', 'immutabilitypolicy',
            'legalhold'.
        file_extractor (Optional[Dict[str, Union[str, BaseReader]]]): A mapping of file
            extension to a BaseReader class that specifies how to convert that file
            to text. See `SimpleDirectoryReader` for more details, or call this path ```llama_index.readers.file.base.DEFAULT_FILE_READER_CLS```.
        connection_string (str): A connection string which can be found under a storage account's "Access keys" security tab. This parameter
        can be used in place of both the account URL and credential.
        account_url (str): URI to the storage account, may include SAS token.
        credential (Union[str, Dict[str, str], AzureNamedKeyCredential, AzureSasCredential, TokenCredential, None] = None):
            The credentials with which to authenticate. This is optional if the account URL already has a SAS token.
        file_metadata_fn (Optional[Callable[str, Dict]]): A function that takes
            in a filename and returns a Dict of metadata for the Document.
            Default is None.
        filename_as_id (bool): Whether to use the filename as the document id.
            False by default.

    """

    container_name: str
    prefix: Optional[str] = ""
    blob: Optional[str] = None
    name_starts_with: Optional[str] = None
    include: Optional[Any] = None
    file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = Field(
        default=None, exclude=True
    )
    connection_string: Optional[str] = None
    account_url: Optional[str] = None
    credential: Optional[Any] = None
    is_remote: bool = True
    file_metadata_fn: Optional[FileMetadataCallable] = Field(default=None, exclude=True)
    filename_as_id: bool = True

    # Not in use. As part of the TODO below. Is part of the kwargs.
    # self.preloaded_data_path = kwargs.get('preloaded_data_path', None)

    @classmethod
    defclass_name(cls) -> str:
        return "AzStorageBlobReader"

    def_get_container_client(self):
        if self.connection_string:
            return ContainerClient.from_connection_string(
                conn_str=self.connection_string,
                container_name=self.container_name,
            )
        return ContainerClient(
            self.account_url, self.container_name, credential=self.credential
        )

    def_download_files_and_extract_metadata(self, temp_dir: str) -> Dict[str, Any]:
"""Download files from Azure Storage Blob and extract metadata."""
        container_client = self._get_container_client()
        blob_meta = {}

        if self.blob:
            blobs_list = [self.blob]
        else:
            blobs_list = container_client.list_blobs(
                self.name_starts_with, self.include
            )

        for obj in blobs_list:
            sanitized_file_name = obj.name.replace("/", "-") if not self.blob else obj
            download_file_path = os.path.join(temp_dir, sanitized_file_name)
            logger.info(f"Start download of {sanitized_file_name}")
            start_time = time.time()
            blob_client = container_client.get_blob_client(obj)
            stream = blob_client.download_blob()
            with open(file=download_file_path, mode="wb") as download_file:
                stream.readinto(download_file)
            blob_meta[sanitized_file_name] = blob_client.get_blob_properties()
            end_time = time.time()
            logger.debug(
                f"{sanitized_file_name} downloaded in {end_time-start_time} seconds."
            )

        return blob_meta

    def_extract_blob_metadata(self, file_metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta: dict = file_metadata

        creation_time = meta.get("creation_time")
        creation_time = creation_time.strftime("%Y-%m-%d") if creation_time else None

        last_modified = meta.get("last_modified")
        last_modified = last_modified.strftime("%Y-%m-%d") if last_modified else None

        last_accessed_on = meta.get("last_accessed_on")
        last_accessed_on = (
            last_accessed_on.strftime("%Y-%m-%d") if last_accessed_on else None
        )

        extracted_meta = {
            "file_name": meta.get("name"),
            "file_type": meta.get("content_settings", {}).get("content_type"),
            "file_size": meta.get("size"),
            "creation_date": creation_time,
            "last_modified_date": last_modified,
            "last_accessed_date": last_accessed_on,
            "container": meta.get("container"),
        }

        extracted_meta.update(meta.get("metadata") or {})
        extracted_meta.update(meta.get("tags") or {})

        return extracted_meta

    def_load_documents_with_metadata(
        self, files_metadata: Dict[str, Any], temp_dir: str
    ) -> List[Document]:
"""Load documents from a directory and extract metadata."""

        defget_metadata(file_name: str) -> Dict[str, Any]:
            sanitized_file_name = os.path.basename(file_name)
            metadata_sanitized = files_metadata.get(sanitized_file_name, {})
            try:
                json_str = json.dumps(metadata_sanitized, cls=SanitizedJSONEncoder)
                clean_metadata = json.loads(json_str)
            except (TypeError, ValueError) as e:
                logger.error(
                    f"Failed to serialize/deserialize metadata for '{sanitized_file_name}': {e}"
                )
                clean_metadata = {}
            return dict(**clean_metadata)

        loader = SimpleDirectoryReader(
            input_dir=temp_dir,
            file_extractor=self.file_extractor,
            file_metadata=self.file_metadata_fn or get_metadata,
            filename_as_id=self.filename_as_id,
        )

        return loader.load_data()

    deflist_resources(self, *args: Any, **kwargs: Any) -> List[str]:
"""List all the blobs in the container."""
        blobs_list = self._get_container_client().list_blobs(
            name_starts_with=self.name_starts_with, include=self.include
        )

        return [blob.name for blob in blobs_list]

    defget_resource_info(self, resource_id: str, **kwargs: Any) -> Dict:
"""Get metadata for a specific blob."""
        container_client = self._get_container_client()
        blob_client = container_client.get_blob_client(resource_id)
        blob_meta = blob_client.get_blob_properties()

        info_dict = {
            **self._extract_blob_metadata(blob_meta),
            "file_path": str(resource_id).replace(":", "/"),
        }

        return {
            meta_key: meta_value
            for meta_key, meta_value in info_dict.items()
            if meta_value is not None
        }

    defload_resource(self, resource_id: str, **kwargs: Any) -> List[Document]:
        try:
            container_client = self._get_container_client()
            blob_client = container_client.get_blob_client(resource_id)
            stream = blob_client.download_blob()
            with tempfile.TemporaryDirectory() as temp_dir:
                download_file_path = os.path.join(
                    temp_dir, resource_id.replace("/", "-")
                )
                with open(file=download_file_path, mode="wb") as download_file:
                    stream.readinto(download_file)
                return self._load_documents_with_metadata(
                    {resource_id: blob_client.get_blob_properties()}, temp_dir
                )
        except Exception as e:
            logger.error(
                f"Error loading resource {resource_id} from AzStorageBlob: {e}"
            )
            raise

    defread_file_content(self, input_file: Path, **kwargs) -> bytes:
"""Read the content of a file from Azure Storage Blob."""
        container_client = self._get_container_client()
        blob_client = container_client.get_blob_client(input_file)
        stream = blob_client.download_blob()
        return stream.readall()

    defload_data(self) -> List[Document]:
"""Load file(s) from Azure Storage Blob."""
        total_download_start_time = time.time()

        with tempfile.TemporaryDirectory() as temp_dir:
            files_metadata = self._download_files_and_extract_metadata(temp_dir)

            total_download_end_time = time.time()

            total_elapsed_time = math.ceil(
                total_download_end_time - total_download_start_time
            )

            logger.info(
                f"Downloading completed in approximately {total_elapsed_time//60}min"
                f" {total_elapsed_time%60}s."
            )

            logger.info("Document creation starting")

            return self._load_documents_with_metadata(files_metadata, temp_dir)

```
 |  
| --- | --- |  
###  list_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/azstorage_blob/#llama_index.readers.azstorage_blob.AzStorageBlobReader.list_resources "Permanent link")

```
list_resources(*args: , **kwargs: ) -> []

```

List all the blobs in the container.
Source code in `llama-index-integrations/readers/llama-index-readers-azstorage-blob/llama_index/readers/azstorage_blob/base.py`  
| 
```
211
212
213
214
215
216
217
```
 | 
```
deflist_resources(self, *args: Any, **kwargs: Any) -> List[str]:
"""List all the blobs in the container."""
    blobs_list = self._get_container_client().list_blobs(
        name_starts_with=self.name_starts_with, include=self.include
    )

    return [blob.name for blob in blobs_list]

```
 |  
| --- | --- |  
###  get_resource_info [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/azstorage_blob/#llama_index.readers.azstorage_blob.AzStorageBlobReader.get_resource_info "Permanent link")

```
get_resource_info(resource_id: , **kwargs: ) -> 

```

Get metadata for a specific blob.
Source code in `llama-index-integrations/readers/llama-index-readers-azstorage-blob/llama_index/readers/azstorage_blob/base.py`  
| 
```
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
```
 | 
```
defget_resource_info(self, resource_id: str, **kwargs: Any) -> Dict:
"""Get metadata for a specific blob."""
    container_client = self._get_container_client()
    blob_client = container_client.get_blob_client(resource_id)
    blob_meta = blob_client.get_blob_properties()

    info_dict = {
        **self._extract_blob_metadata(blob_meta),
        "file_path": str(resource_id).replace(":", "/"),
    }

    return {
        meta_key: meta_value
        for meta_key, meta_value in info_dict.items()
        if meta_value is not None
    }

```
 |  
| --- | --- |  
###  read_file_content [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/azstorage_blob/#llama_index.readers.azstorage_blob.AzStorageBlobReader.read_file_content "Permanent link")

```
read_file_content(input_file: , **kwargs) -> bytes

```

Read the content of a file from Azure Storage Blob.
Source code in `llama-index-integrations/readers/llama-index-readers-azstorage-blob/llama_index/readers/azstorage_blob/base.py`  
| 
```
256
257
258
259
260
261
```
 | 
```
defread_file_content(self, input_file: Path, **kwargs) -> bytes:
"""Read the content of a file from Azure Storage Blob."""
    container_client = self._get_container_client()
    blob_client = container_client.get_blob_client(input_file)
    stream = blob_client.download_blob()
    return stream.readall()

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/azstorage_blob/#llama_index.readers.azstorage_blob.AzStorageBlobReader.load_data "Permanent link")

```
load_data() -> []

```

Load file(s) from Azure Storage Blob.
Source code in `llama-index-integrations/readers/llama-index-readers-azstorage-blob/llama_index/readers/azstorage_blob/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""Load file(s) from Azure Storage Blob."""
    total_download_start_time = time.time()

    with tempfile.TemporaryDirectory() as temp_dir:
        files_metadata = self._download_files_and_extract_metadata(temp_dir)

        total_download_end_time = time.time()

        total_elapsed_time = math.ceil(
            total_download_end_time - total_download_start_time
        )

        logger.info(
            f"Downloading completed in approximately {total_elapsed_time//60}min"
            f" {total_elapsed_time%60}s."
        )

        logger.info("Document creation starting")

        return self._load_documents_with_metadata(files_metadata, temp_dir)

```
 |  
| --- | --- |  
options: members: - AzStorageBlobReader
