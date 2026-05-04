# Gcs
##  GCSReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gcs/#llama_index.readers.gcs.GCSReader "Permanent link")
Bases: , , 
A reader for Google Cloud Storage (GCS) files and directories.
This class allows reading files from GCS, listing resources, and retrieving resource information. It supports authentication via service account keys and implements various reader mixins.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `bucket`  |  The name of the GCS bucket.  |  
|  `Optional[str]`  |  The specific file key to read. If None, the entire bucket is parsed.  |  
| `prefix`  |  `Optional[str]`  |  The prefix to filter by when iterating through the bucket.  |  
| `recursive`  |  `bool`  |  Whether to recursively search in subdirectories.  |  
| `file_extractor`  |  `Optional[Dict[str, Union[str, BaseReader[](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader "BaseReader \(llama_index.core.readers.base.BaseReader\)")]]]`  |  Custom file extractors.  |  
| `required_exts`  |  `Optional[List[str]]`  |  List of required file extensions.  |  
| `filename_as_id`  |  `bool`  |  Whether to use the filename as the document ID.  |  
| `num_files_limit`  |  `Optional[int]`  |  Maximum number of files to read.  |  
| `file_metadata`  |  `Optional[Callable[[str], Dict]]`  |  Function to extract metadata from filenames.  |  
| `service_account_key`  |  `Optional[Dict[str, str]]`  |  Service account key as a dictionary.  |  
| `service_account_key_json`  |  `Optional[str]`  |  Service account key as a JSON string.  |  
| `service_account_key_path`  |  `Optional[str]`  |  Path to the service account key file.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gcs/llama_index/readers/gcs/base.py`  
| 
```
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
```
 | 
```
classGCSReader(BasePydanticReader, ResourcesReaderMixin, FileSystemReaderMixin):
"""
    A reader for Google Cloud Storage (GCS) files and directories.

    This class allows reading files from GCS, listing resources, and retrieving resource information.
    It supports authentication via service account keys and implements various reader mixins.

    Attributes:
        bucket (str): The name of the GCS bucket.
        key (Optional[str]): The specific file key to read. If None, the entire bucket is parsed.
        prefix (Optional[str]): The prefix to filter by when iterating through the bucket.
        recursive (bool): Whether to recursively search in subdirectories.
        file_extractor (Optional[Dict[str, Union[str, BaseReader]]]): Custom file extractors.
        required_exts (Optional[List[str]]): List of required file extensions.
        filename_as_id (bool): Whether to use the filename as the document ID.
        num_files_limit (Optional[int]): Maximum number of files to read.
        file_metadata (Optional[Callable[[str], Dict]]): Function to extract metadata from filenames.
        service_account_key (Optional[Dict[str, str]]): Service account key as a dictionary.
        service_account_key_json (Optional[str]): Service account key as a JSON string.
        service_account_key_path (Optional[str]): Path to the service account key file.

    """

    is_remote: bool = True

    bucket: str
    key: Optional[str] = None
    prefix: Optional[str] = ""
    recursive: bool = True
    file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = Field(
        default=None, exclude=True
    )
    required_exts: Optional[List[str]] = None
    filename_as_id: bool = True
    num_files_limit: Optional[int] = None
    file_metadata: Optional[FileMetadataCallable] = Field(default=None, exclude=True)
    service_account_key: Optional[Dict[str, str]] = None
    service_account_key_json: Optional[str] = None
    service_account_key_path: Optional[str] = None

    @classmethod
    defclass_name(cls) -> str:
"""Return the name of the class."""
        return "GCSReader"

    def_get_gcsfs(self):
"""
        Create and return a GCSFileSystem object.

        This method handles authentication using the provided service account credentials.

        Returns:
            GCSFileSystem: An authenticated GCSFileSystem object.

        Raises:
            ValueError: If no valid authentication method is provided.
            DefaultCredentialsError: If there's an issue with the provided credentials.

        """
        fromgcsfsimport GCSFileSystem

        try:
            if self.service_account_key is not None:
                creds = service_account.Credentials.from_service_account_info(
                    self.service_account_key, scopes=SCOPES
                )
            elif self.service_account_key_json is not None:
                creds = service_account.Credentials.from_service_account_info(
                    json.loads(self.service_account_key_json), scopes=SCOPES
                )
            elif self.service_account_key_path is not None:
                creds = service_account.Credentials.from_service_account_file(
                    self.service_account_key_path, scopes=SCOPES
                )
            else:
                logger.warning(
                    "No explicit credentials provided. Falling back to default credentials."
                )
                creds = None  # This will use default credentials

            return GCSFileSystem(token=creds)
        except DefaultCredentialsError as e:
            logger.error(f"Failed to authenticate with GCS: {e!s}")
            raise

    def_get_simple_directory_reader(self) -> SimpleDirectoryReader:
"""
        Create and return a SimpleDirectoryReader for GCS.

        This method sets up a SimpleDirectoryReader with the appropriate GCS filesystem
        and other configured parameters.

        Returns:
            SimpleDirectoryReader: A configured SimpleDirectoryReader for GCS.

        """
        gcsfs = self._get_gcsfs()

        input_dir = self.bucket
        input_files = None

        if self.key:
            input_files = [f"{self.bucket}/{self.key}"]
        elif self.prefix:
            input_dir = f"{input_dir}/{self.prefix}"

        return SimpleDirectoryReader(
            input_dir=input_dir,
            input_files=input_files,
            recursive=self.recursive,
            file_extractor=self.file_extractor,
            required_exts=self.required_exts,
            filename_as_id=self.filename_as_id,
            num_files_limit=self.num_files_limit,
            file_metadata=self.file_metadata,
            fs=gcsfs,
        )

    defload_data(self) -> List[Document]:
"""
        Load data from the specified GCS bucket or file.

        Returns:
            List[Document]: A list of loaded documents.

        Raises:
            Exception: If there's an error loading the data.

        """
        try:
            logger.info(f"Loading data from GCS bucket: {self.bucket}")
            return self._get_simple_directory_reader().load_data()
        except Exception as e:
            logger.error(f"Error loading data from GCS: {e!s}")
            raise

    deflist_resources(self, **kwargs) -> List[str]:
"""
        List resources in the specified GCS bucket or directory.

        Args:
            **kwargs: Additional arguments to pass to the underlying list_resources method.

        Returns:
            List[str]: A list of resource identifiers.

        Raises:
            Exception: If there's an error listing the resources.

        """
        try:
            logger.info(f"Listing resources in GCS bucket: {self.bucket}")
            return self._get_simple_directory_reader().list_resources(**kwargs)
        except Exception as e:
            logger.error(f"Error listing resources in GCS: {e!s}")
            raise

    defget_resource_info(self, resource_id: str, **kwargs) -> Dict:
"""
        Get information about a specific GCS resource.

        Args:
            resource_id (str): The identifier of the resource.
            **kwargs: Additional arguments to pass to the underlying info method.

        Returns:
            Dict: A dictionary containing resource information.

        Raises:
            Exception: If there's an error retrieving the resource information.

        """
        try:
            logger.info(f"Getting info for resource: {resource_id}")
            gcsfs = self._get_gcsfs()
            info_result = gcsfs.info(resource_id)

            info_dict = {
                "file_path": info_result.get("name"),
                "file_size": info_result.get("size"),
                "last_modified_date": info_result.get("updated"),
                "content_hash": info_result.get("md5Hash"),
                "content_type": info_result.get("contentType"),
                "storage_class": info_result.get("storageClass"),
                "etag": info_result.get("etag"),
                "generation": info_result.get("generation"),
                "created_date": info_result.get("timeCreated"),
            }

            # Convert datetime objects to ISO format strings
            for key in ["last_modified_date", "created_date"]:
                if isinstance(info_dict.get(key), datetime):
                    info_dict[key] = info_dict[key].isoformat()

            return {k: v for k, v in info_dict.items() if v is not None}
        except Exception as e:
            logger.error(f"Error getting resource info from GCS: {e!s}")
            raise

    defload_resource(self, resource_id: str, **kwargs) -> List[Document]:
"""
        Load a specific resource from GCS.

        Args:
            resource_id (str): The identifier of the resource to load.
            **kwargs: Additional arguments to pass to the underlying load_resource method.

        Returns:
            List[Document]: A list containing the loaded document.

        Raises:
            Exception: If there's an error loading the resource.

        """
        try:
            logger.info(f"Loading resource: {resource_id}")
            return self._get_simple_directory_reader().load_resource(
                resource_id, **kwargs
            )
        except Exception as e:
            logger.error(f"Error loading resource from GCS: {e!s}")
            raise

    defread_file_content(self, input_file: Path, **kwargs) -> bytes:
"""
        Read the content of a specific file from GCS.

        Args:
            input_file (Path): The path to the file to read.
            **kwargs: Additional arguments to pass to the underlying read_file_content method.

        Returns:
            bytes: The content of the file.

        Raises:
            Exception: If there's an error reading the file content.

        """
        try:
            logger.info(f"Reading file content: {input_file}")
            return self._get_simple_directory_reader().read_file_content(
                input_file, **kwargs
            )
        except Exception as e:
            logger.error(f"Error reading file content from GCS: {e!s}")
            raise

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gcs/#llama_index.readers.gcs.GCSReader.class_name "Permanent link")

```
class_name() -> 

```

Return the name of the class.
Source code in `llama-index-integrations/readers/llama-index-readers-gcs/llama_index/readers/gcs/base.py`  
| 
```
78
79
80
81
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Return the name of the class."""
    return "GCSReader"

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gcs/#llama_index.readers.gcs.GCSReader.load_data "Permanent link")

```
load_data() -> []

```

Load data from the specified GCS bucket or file.
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of loaded documents.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If there's an error loading the data.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gcs/llama_index/readers/gcs/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""
    Load data from the specified GCS bucket or file.

    Returns:
        List[Document]: A list of loaded documents.

    Raises:
        Exception: If there's an error loading the data.

    """
    try:
        logger.info(f"Loading data from GCS bucket: {self.bucket}")
        return self._get_simple_directory_reader().load_data()
    except Exception as e:
        logger.error(f"Error loading data from GCS: {e!s}")
        raise

```
 |  
| --- | --- |  
###  list_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gcs/#llama_index.readers.gcs.GCSReader.list_resources "Permanent link")

```
list_resources(**kwargs) -> []

```

List resources in the specified GCS bucket or directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `**kwargs`  |  Additional arguments to pass to the underlying list_resources method.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[str]`  |  List[str]: A list of resource identifiers.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If there's an error listing the resources.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gcs/llama_index/readers/gcs/base.py`  
| 
```
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
```
 | 
```
deflist_resources(self, **kwargs) -> List[str]:
"""
    List resources in the specified GCS bucket or directory.

    Args:
        **kwargs: Additional arguments to pass to the underlying list_resources method.

    Returns:
        List[str]: A list of resource identifiers.

    Raises:
        Exception: If there's an error listing the resources.

    """
    try:
        logger.info(f"Listing resources in GCS bucket: {self.bucket}")
        return self._get_simple_directory_reader().list_resources(**kwargs)
    except Exception as e:
        logger.error(f"Error listing resources in GCS: {e!s}")
        raise

```
 |  
| --- | --- |  
###  get_resource_info [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gcs/#llama_index.readers.gcs.GCSReader.get_resource_info "Permanent link")

```
get_resource_info(resource_id: , **kwargs) -> 

```

Get information about a specific GCS resource.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `resource_id`  |  The identifier of the resource.  |  _required_  |  
|  `**kwargs`  |  Additional arguments to pass to the underlying info method.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Dict`  |  `Dict`  |  A dictionary containing resource information.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If there's an error retrieving the resource information.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gcs/llama_index/readers/gcs/base.py`  
| 
```
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
```
 | 
```
defget_resource_info(self, resource_id: str, **kwargs) -> Dict:
"""
    Get information about a specific GCS resource.

    Args:
        resource_id (str): The identifier of the resource.
        **kwargs: Additional arguments to pass to the underlying info method.

    Returns:
        Dict: A dictionary containing resource information.

    Raises:
        Exception: If there's an error retrieving the resource information.

    """
    try:
        logger.info(f"Getting info for resource: {resource_id}")
        gcsfs = self._get_gcsfs()
        info_result = gcsfs.info(resource_id)

        info_dict = {
            "file_path": info_result.get("name"),
            "file_size": info_result.get("size"),
            "last_modified_date": info_result.get("updated"),
            "content_hash": info_result.get("md5Hash"),
            "content_type": info_result.get("contentType"),
            "storage_class": info_result.get("storageClass"),
            "etag": info_result.get("etag"),
            "generation": info_result.get("generation"),
            "created_date": info_result.get("timeCreated"),
        }

        # Convert datetime objects to ISO format strings
        for key in ["last_modified_date", "created_date"]:
            if isinstance(info_dict.get(key), datetime):
                info_dict[key] = info_dict[key].isoformat()

        return {k: v for k, v in info_dict.items() if v is not None}
    except Exception as e:
        logger.error(f"Error getting resource info from GCS: {e!s}")
        raise

```
 |  
| --- | --- |  
###  load_resource [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gcs/#llama_index.readers.gcs.GCSReader.load_resource "Permanent link")

```
load_resource(resource_id: , **kwargs) -> []

```

Load a specific resource from GCS.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `resource_id`  |  The identifier of the resource to load.  |  _required_  |  
|  `**kwargs`  |  Additional arguments to pass to the underlying load_resource method.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list containing the loaded document.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If there's an error loading the resource.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gcs/llama_index/readers/gcs/base.py`  
| 
```
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
```
 | 
```
defload_resource(self, resource_id: str, **kwargs) -> List[Document]:
"""
    Load a specific resource from GCS.

    Args:
        resource_id (str): The identifier of the resource to load.
        **kwargs: Additional arguments to pass to the underlying load_resource method.

    Returns:
        List[Document]: A list containing the loaded document.

    Raises:
        Exception: If there's an error loading the resource.

    """
    try:
        logger.info(f"Loading resource: {resource_id}")
        return self._get_simple_directory_reader().load_resource(
            resource_id, **kwargs
        )
    except Exception as e:
        logger.error(f"Error loading resource from GCS: {e!s}")
        raise

```
 |  
| --- | --- |  
###  read_file_content [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/gcs/#llama_index.readers.gcs.GCSReader.read_file_content "Permanent link")

```
read_file_content(input_file: , **kwargs) -> bytes

```

Read the content of a specific file from GCS.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_file`  |  `Path`  |  The path to the file to read.  |  _required_  |  
|  `**kwargs`  |  Additional arguments to pass to the underlying read_file_content method.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `bytes`  |  `bytes`  |  The content of the file.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `Exception`  |  If there's an error reading the file content.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-gcs/llama_index/readers/gcs/base.py`  
| 
```
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
defread_file_content(self, input_file: Path, **kwargs) -> bytes:
"""
    Read the content of a specific file from GCS.

    Args:
        input_file (Path): The path to the file to read.
        **kwargs: Additional arguments to pass to the underlying read_file_content method.

    Returns:
        bytes: The content of the file.

    Raises:
        Exception: If there's an error reading the file content.

    """
    try:
        logger.info(f"Reading file content: {input_file}")
        return self._get_simple_directory_reader().read_file_content(
            input_file, **kwargs
        )
    except Exception as e:
        logger.error(f"Error reading file content from GCS: {e!s}")
        raise

```
 |  
| --- | --- |  
options: members: - GCSReader
