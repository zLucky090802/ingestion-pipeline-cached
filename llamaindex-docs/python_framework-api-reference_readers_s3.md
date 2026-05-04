# S3
##  S3Reader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/s3/#llama_index.readers.s3.S3Reader "Permanent link")
Bases: , , 
General reader for any S3 file or directory.
If key is not set, the entire bucket (filtered by prefix) is parsed.
Args: bucket (str): the name of your S3 bucket key (Optional[str]): the name of the specific file. If none is provided, this loader will iterate through the entire bucket. prefix (Optional[str]): the prefix to filter by in the case that the loader iterates through the entire bucket. Defaults to empty string. recursive (bool): Whether to recursively search in subdirectories. True by default. file_extractor (Optional[Dict[str, BaseReader]]): A mapping of file extension to a BaseReader class that specifies how to convert that file to text. See `SimpleDirectoryReader` for more details. required_exts (Optional[List[str]]): List of required extensions. Default is None. num_files_limit (Optional[int]): Maximum number of files to read. Default is None. file_metadata (Optional[Callable[str, Dict]]): A function that takes in a filename and returns a Dict of metadata for the Document. Default is None. aws_access_id (Optional[str]): provide AWS access key directly. aws_access_secret (Optional[str]): provide AWS access key directly. region_name (Optional[str]): AWS region for the S3 bucket. If not provided, the default environment region or AWS config will be used. s3_endpoint_url (Optional[str]): provide S3 endpoint URL directly.
Source code in `llama-index-integrations/readers/llama-index-readers-s3/llama_index/readers/s3/base.py`  
| 
```
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
225
226
```
 | 
```
classS3Reader(BasePydanticReader, ResourcesReaderMixin, FileSystemReaderMixin):
"""
    General reader for any S3 file or directory.

    If key is not set, the entire bucket (filtered by prefix) is parsed.

    Args:
    bucket (str): the name of your S3 bucket
    key (Optional[str]): the name of the specific file. If none is provided,
        this loader will iterate through the entire bucket.
    prefix (Optional[str]): the prefix to filter by in the case that the loader
        iterates through the entire bucket. Defaults to empty string.
    recursive (bool): Whether to recursively search in subdirectories.
        True by default.
    file_extractor (Optional[Dict[str, BaseReader]]): A mapping of file
        extension to a BaseReader class that specifies how to convert that file
        to text. See `SimpleDirectoryReader` for more details.
    required_exts (Optional[List[str]]): List of required extensions.
        Default is None.
    num_files_limit (Optional[int]): Maximum number of files to read.
        Default is None.
    file_metadata (Optional[Callable[str, Dict]]): A function that takes
        in a filename and returns a Dict of metadata for the Document.
        Default is None.
    aws_access_id (Optional[str]): provide AWS access key directly.
    aws_access_secret (Optional[str]): provide AWS access key directly.
    region_name (Optional[str]): AWS region for the S3 bucket. If not provided,
    the default environment region or AWS config will be used.
    s3_endpoint_url (Optional[str]): provide S3 endpoint URL directly.

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
    aws_access_id: Optional[str] = None
    aws_access_secret: Optional[str] = None
    aws_session_token: Optional[str] = None
    region_name: Optional[str] = None
    s3_endpoint_url: Optional[str] = None
    custom_reader_path: Optional[str] = None
    invalidate_s3fs_cache: bool = True

    @classmethod
    defclass_name(cls) -> str:
        return "S3Reader"

    def_get_s3fs(self):
        froms3fsimport S3FileSystem

        client_kwargs = {}
        if isinstance(self.region_name, str) and self.region_name.strip():
            client_kwargs["region_name"] = self.region_name.strip()

        s3fs = S3FileSystem(
            key=self.aws_access_id,
            endpoint_url=self.s3_endpoint_url,
            secret=self.aws_access_secret,
            token=self.aws_session_token,
            client_kwargs=client_kwargs or None,
        )
        if self.invalidate_s3fs_cache:
            s3fs.invalidate_cache()

        return s3fs

    def_get_simple_directory_reader(self) -> SimpleDirectoryReader:
        # we don't want to keep the reader as a field in the class to keep it serializable
        s3fs = self._get_s3fs()

        input_dir = self.bucket
        input_files = None

        if self.key:
            input_files = [f"{self.bucket}/{self.key}"]
        elif self.prefix:
            input_dir = f"{input_dir}/{self.prefix}"

        return SimpleDirectoryReader(
            input_dir=input_dir,
            input_files=input_files,
            file_extractor=self.file_extractor,
            required_exts=self.required_exts,
            filename_as_id=self.filename_as_id,
            num_files_limit=self.num_files_limit,
            file_metadata=self.file_metadata,
            recursive=self.recursive,
            fs=s3fs,
        )

    def_load_s3_files_as_docs(self) -> List[Document]:
"""Load file(s) from S3."""
        loader = self._get_simple_directory_reader()
        return loader.load_data()

    async def_aload_s3_files_as_docs(self) -> List[Document]:
"""Asynchronously load file(s) from S3."""
        loader = self._get_simple_directory_reader()
        return await loader.aload_data()

    def_adjust_documents(self, documents: List[Document]) -> List[Document]:
        for doc in documents:
            if self.s3_endpoint_url:
                doc.id_ = self.s3_endpoint_url + "_" + doc.id_
            else:
                doc.id_ = "s3_" + doc.id_
        return documents

    defload_data(self, custom_temp_subdir: str = None) -> List[Document]:
"""
        Load the file(s) from S3.

        Args:
            custom_temp_subdir (str, optional): This parameter is deprecated and unused. Defaults to None.

        Returns:
            List[Document]: A list of documents loaded from S3.

        """
        if custom_temp_subdir is not None:
            warnings.warn(
                "The `custom_temp_subdir` parameter is deprecated and unused. Please remove it from your code.",
                DeprecationWarning,
            )

        documents = self._load_s3_files_as_docs()
        return self._adjust_documents(documents)

    async defaload_data(self, custom_temp_subdir: str = None) -> List[Document]:
"""
        Asynchronously load the file(s) from S3.

        Args:
            custom_temp_subdir (str, optional): This parameter is deprecated and unused. Defaults to None.

        Returns:
            List[Document]: A list of documents loaded from S3.

        """
        if custom_temp_subdir is not None:
            warnings.warn(
                "The `custom_temp_subdir` parameter is deprecated and unused. Please remove it from your code.",
                DeprecationWarning,
            )

        documents = await self._aload_s3_files_as_docs()
        return self._adjust_documents(documents)

    deflist_resources(self, **kwargs) -> List[str]:
        simple_directory_reader = self._get_simple_directory_reader()
        return simple_directory_reader.list_resources(**kwargs)

    defget_resource_info(self, resource_id: str, **kwargs) -> Dict:
        # can't use SimpleDirectoryReader.get_resource_info because it lacks some fields
        fs = self._get_s3fs()
        info_result = fs.info(resource_id)

        last_modified_date = info_result.get("LastModified")
        if last_modified_date and isinstance(last_modified_date, datetime):
            last_modified_date = last_modified_date.astimezone(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        else:
            last_modified_date = None

        info_dict = {
            "file_path": str(resource_id),
            "file_size": info_result.get("size"),
            "last_modified_date": last_modified_date,
            "content_hash": info_result.get("ETag"),
        }

        # Ignore None values
        return {
            meta_key: meta_value
            for meta_key, meta_value in info_dict.items()
            if meta_value is not None
        }

    defload_resource(self, resource_id: str, **kwargs) -> List[Document]:
        simple_directory_reader = self._get_simple_directory_reader()
        docs = simple_directory_reader.load_resource(resource_id, **kwargs)
        return self._adjust_documents(docs)

    defread_file_content(self, input_file: Path, **kwargs) -> bytes:
        simple_directory_reader = self._get_simple_directory_reader()
        return simple_directory_reader.read_file_content(input_file, **kwargs)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/s3/#llama_index.readers.s3.S3Reader.load_data "Permanent link")

```
load_data(custom_temp_subdir:  = None) -> []

```

Load the file(s) from S3.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `custom_temp_subdir`  |  This parameter is deprecated and unused. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents loaded from S3.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-s3/llama_index/readers/s3/base.py`  
| 
```
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
```
 | 
```
defload_data(self, custom_temp_subdir: str = None) -> List[Document]:
"""
    Load the file(s) from S3.

    Args:
        custom_temp_subdir (str, optional): This parameter is deprecated and unused. Defaults to None.

    Returns:
        List[Document]: A list of documents loaded from S3.

    """
    if custom_temp_subdir is not None:
        warnings.warn(
            "The `custom_temp_subdir` parameter is deprecated and unused. Please remove it from your code.",
            DeprecationWarning,
        )

    documents = self._load_s3_files_as_docs()
    return self._adjust_documents(documents)

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/s3/#llama_index.readers.s3.S3Reader.aload_data "Permanent link")

```
aload_data(
    custom_temp_subdir:  = None,
) -> []

```

Asynchronously load the file(s) from S3.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `custom_temp_subdir`  |  This parameter is deprecated and unused. Defaults to None.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents loaded from S3.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-s3/llama_index/readers/s3/base.py`  
| 
```
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
```
 | 
```
async defaload_data(self, custom_temp_subdir: str = None) -> List[Document]:
"""
    Asynchronously load the file(s) from S3.

    Args:
        custom_temp_subdir (str, optional): This parameter is deprecated and unused. Defaults to None.

    Returns:
        List[Document]: A list of documents loaded from S3.

    """
    if custom_temp_subdir is not None:
        warnings.warn(
            "The `custom_temp_subdir` parameter is deprecated and unused. Please remove it from your code.",
            DeprecationWarning,
        )

    documents = await self._aload_s3_files_as_docs()
    return self._adjust_documents(documents)

```
 |  
| --- | --- |  
options: members: - S3Reader
