# Minio
##  BotoMinioReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/minio/#llama_index.readers.minio.BotoMinioReader "Permanent link")
Bases: 
General reader for any S3 file or directory. A loader that fetches a file or iterates through a directory on minio using boto3.
Source code in `llama-index-integrations/readers/llama-index-readers-minio/llama_index/readers/minio/boto3_client/base.py`  
| 
```
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
```
 | 
```
classBotoMinioReader(BaseReader):
"""
    General reader for any S3 file or directory.
    A loader that fetches a file or iterates through a directory on minio using boto3.

    """

    def__init__(
        self,
        *args: Any,
        bucket: str,
        key: Optional[str] = None,
        prefix: Optional[str] = "",
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
        required_exts: Optional[List[str]] = None,
        filename_as_id: bool = False,
        num_files_limit: Optional[int] = None,
        file_metadata: Optional[Callable[[str], Dict]] = None,
        aws_access_id: Optional[str] = None,
        aws_access_secret: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        s3_endpoint_url: Optional[str] = "https://s3.amazonaws.com",
        **kwargs: Any,
    ) -> None:
"""
        Initialize S3 bucket and key, along with credentials if needed.

        If key is not set, the entire bucket (filtered by prefix) is parsed.

        Args:
        bucket (str): the name of your S3 bucket
        key (Optional[str]): the name of the specific file. If none is provided,
            this loader will iterate through the entire bucket.
        prefix (Optional[str]): the prefix to filter by in the case that the loader
            iterates through the entire bucket. Defaults to empty string.
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
        s3_endpoint_url (Optional[str]): provide S3 endpoint URL directly.

        """
        super().__init__(*args, **kwargs)

        self.bucket = bucket
        self.key = key
        self.prefix = prefix

        self.file_extractor = file_extractor
        self.required_exts = required_exts
        self.filename_as_id = filename_as_id
        self.num_files_limit = num_files_limit
        self.file_metadata = file_metadata

        self.aws_access_id = aws_access_id
        self.aws_access_secret = aws_access_secret
        self.aws_session_token = aws_session_token
        self.s3_endpoint_url = s3_endpoint_url

    defload_data(self) -> List[Document]:
"""Load file(s) from S3."""
        importboto3

        s3_client = boto3.client(
            "s3",
            endpoint_url=self.s3_endpoint_url,
            aws_access_key_id=self.aws_access_id,
            aws_secret_access_key=self.aws_access_secret,
            aws_session_token=self.aws_session_token,
            config=boto3.session.Config(signature_version="s3v4"),
            verify=False,
        )
        s3 = boto3.resource(
            "s3",
            endpoint_url=self.s3_endpoint_url,
            aws_access_key_id=self.aws_access_id,
            aws_secret_access_key=self.aws_access_secret,
            aws_session_token=self.aws_session_token,
            config=boto3.session.Config(signature_version="s3v4"),
            verify=False,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            if self.key:
                suffix = Path(self.key).suffix
                filepath = f"{temp_dir}/{next(tempfile._get_candidate_names())}{suffix}"
                s3_client.download_file(self.bucket, self.key, filepath)
            else:
                bucket = s3.Bucket(self.bucket)
                for i, obj in enumerate(bucket.objects.filter(Prefix=self.prefix)):
                    if self.num_files_limit is not None and i  self.num_files_limit:
                        break

                    suffix = Path(obj.key).suffix

                    is_dir = obj.key.endswith("/")  # skip folders
                    is_bad_ext = (
                        self.required_exts is not None
                        and suffix not in self.required_exts  # skip other extensions
                    )

                    if is_dir or is_bad_ext:
                        continue

                    filepath = (
                        f"{temp_dir}/{next(tempfile._get_candidate_names())}{suffix}"
                    )
                    s3_client.download_file(self.bucket, obj.key, filepath)

            loader = SimpleDirectoryReader(
                temp_dir,
                file_extractor=self.file_extractor,
                required_exts=self.required_exts,
                filename_as_id=self.filename_as_id,
                num_files_limit=self.num_files_limit,
                file_metadata=self.file_metadata,
            )

            return loader.load_data()

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/minio/#llama_index.readers.minio.BotoMinioReader.load_data "Permanent link")

```
load_data() -> []

```

Load file(s) from S3.
Source code in `llama-index-integrations/readers/llama-index-readers-minio/llama_index/readers/minio/boto3_client/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""Load file(s) from S3."""
    importboto3

    s3_client = boto3.client(
        "s3",
        endpoint_url=self.s3_endpoint_url,
        aws_access_key_id=self.aws_access_id,
        aws_secret_access_key=self.aws_access_secret,
        aws_session_token=self.aws_session_token,
        config=boto3.session.Config(signature_version="s3v4"),
        verify=False,
    )
    s3 = boto3.resource(
        "s3",
        endpoint_url=self.s3_endpoint_url,
        aws_access_key_id=self.aws_access_id,
        aws_secret_access_key=self.aws_access_secret,
        aws_session_token=self.aws_session_token,
        config=boto3.session.Config(signature_version="s3v4"),
        verify=False,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        if self.key:
            suffix = Path(self.key).suffix
            filepath = f"{temp_dir}/{next(tempfile._get_candidate_names())}{suffix}"
            s3_client.download_file(self.bucket, self.key, filepath)
        else:
            bucket = s3.Bucket(self.bucket)
            for i, obj in enumerate(bucket.objects.filter(Prefix=self.prefix)):
                if self.num_files_limit is not None and i  self.num_files_limit:
                    break

                suffix = Path(obj.key).suffix

                is_dir = obj.key.endswith("/")  # skip folders
                is_bad_ext = (
                    self.required_exts is not None
                    and suffix not in self.required_exts  # skip other extensions
                )

                if is_dir or is_bad_ext:
                    continue

                filepath = (
                    f"{temp_dir}/{next(tempfile._get_candidate_names())}{suffix}"
                )
                s3_client.download_file(self.bucket, obj.key, filepath)

        loader = SimpleDirectoryReader(
            temp_dir,
            file_extractor=self.file_extractor,
            required_exts=self.required_exts,
            filename_as_id=self.filename_as_id,
            num_files_limit=self.num_files_limit,
            file_metadata=self.file_metadata,
        )

        return loader.load_data()

```
 |  
| --- | --- |  
##  MinioReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/minio/#llama_index.readers.minio.MinioReader "Permanent link")
Bases: 
General reader for any Minio file or directory.
Source code in `llama-index-integrations/readers/llama-index-readers-minio/llama_index/readers/minio/minio_client/base.py`  
| 
```
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
```
 | 
```
classMinioReader(BaseReader):
"""General reader for any Minio file or directory."""

    def__init__(
        self,
        *args: Any,
        bucket: str,
        key: Optional[str] = None,
        prefix: Optional[str] = "",
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
        required_exts: Optional[List[str]] = None,
        filename_as_id: bool = False,
        num_files_limit: Optional[int] = None,
        file_metadata: Optional[Callable[[str], Dict]] = None,
        minio_endpoint: Optional[str] = None,
        minio_secure: bool = False,
        minio_cert_check: bool = True,
        minio_access_key: Optional[str] = None,
        minio_secret_key: Optional[str] = None,
        minio_session_token: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
"""
        Initialize Minio bucket and key, along with credentials if needed.

        If key is not set, the entire bucket (filtered by prefix) is parsed.

        Args:
        bucket (str): the name of your Minio bucket
        key (Optional[str]): the name of the specific file. If none is provided,
            this loader will iterate through the entire bucket.
        prefix (Optional[str]): the prefix to filter by in the case that the loader
            iterates through the entire bucket. Defaults to empty string.
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
        minio_endpoint (Optional[str]): The Minio endpoint. Default is None.
        minio_port (Optional[int]): The Minio port. Default is None.
        minio_access_key (Optional[str]): The Minio access key. Default is None.
        minio_secret_key (Optional[str]): The Minio secret key. Default is None.
        minio_session_token (Optional[str]): The Minio session token.
        minio_secure: MinIO server runs in TLS mode
        minio_cert_check: allows the usage of a self-signed cert for MinIO server

        """
        super().__init__(*args, **kwargs)

        self.bucket = bucket
        self.key = key
        self.prefix = prefix

        self.file_extractor = file_extractor
        self.required_exts = required_exts
        self.filename_as_id = filename_as_id
        self.num_files_limit = num_files_limit
        self.file_metadata = file_metadata

        self.minio_endpoint = minio_endpoint
        self.minio_secure = minio_secure
        self.minio_cert_check = minio_cert_check
        self.minio_access_key = minio_access_key
        self.minio_secret_key = minio_secret_key
        self.minio_session_token = minio_session_token

    defload_data(self) -> List[Document]:
"""Load file(s) from Minio."""
        fromminioimport Minio

        minio_client = Minio(
            self.minio_endpoint,
            secure=self.minio_secure,
            cert_check=self.minio_cert_check,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            session_token=self.minio_session_token,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            if self.key:
                suffix = Path(self.key).suffix
                _, filepath = tempfile.mkstemp(dir=temp_dir, suffix=suffix)
                minio_client.fget_object(
                    bucket_name=self.bucket, object_name=self.key, file_path=filepath
                )
            else:
                objects = minio_client.list_objects(
                    bucket_name=self.bucket, prefix=self.prefix, recursive=True
                )
                for i, obj in enumerate(objects):
                    file_name = obj.object_name.split("/")[-1]
                    if self.num_files_limit is not None and i  self.num_files_limit:
                        break

                    suffix = Path(obj.object_name).suffix

                    is_dir = obj.object_name.endswith("/")  # skip folders
                    is_bad_ext = (
                        self.required_exts is not None
                        and suffix not in self.required_exts  # skip other extensions
                    )

                    if is_dir or is_bad_ext:
                        continue

                    filepath = f"{temp_dir}/{file_name}"
                    minio_client.fget_object(self.bucket, obj.object_name, filepath)

            loader = SimpleDirectoryReader(
                temp_dir,
                file_extractor=self.file_extractor,
                required_exts=self.required_exts,
                filename_as_id=self.filename_as_id,
                num_files_limit=self.num_files_limit,
                file_metadata=self.file_metadata,
            )

            return loader.load_data()

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/minio/#llama_index.readers.minio.MinioReader.load_data "Permanent link")

```
load_data() -> []

```

Load file(s) from Minio.
Source code in `llama-index-integrations/readers/llama-index-readers-minio/llama_index/readers/minio/minio_client/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""Load file(s) from Minio."""
    fromminioimport Minio

    minio_client = Minio(
        self.minio_endpoint,
        secure=self.minio_secure,
        cert_check=self.minio_cert_check,
        access_key=self.minio_access_key,
        secret_key=self.minio_secret_key,
        session_token=self.minio_session_token,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        if self.key:
            suffix = Path(self.key).suffix
            _, filepath = tempfile.mkstemp(dir=temp_dir, suffix=suffix)
            minio_client.fget_object(
                bucket_name=self.bucket, object_name=self.key, file_path=filepath
            )
        else:
            objects = minio_client.list_objects(
                bucket_name=self.bucket, prefix=self.prefix, recursive=True
            )
            for i, obj in enumerate(objects):
                file_name = obj.object_name.split("/")[-1]
                if self.num_files_limit is not None and i  self.num_files_limit:
                    break

                suffix = Path(obj.object_name).suffix

                is_dir = obj.object_name.endswith("/")  # skip folders
                is_bad_ext = (
                    self.required_exts is not None
                    and suffix not in self.required_exts  # skip other extensions
                )

                if is_dir or is_bad_ext:
                    continue

                filepath = f"{temp_dir}/{file_name}"
                minio_client.fget_object(self.bucket, obj.object_name, filepath)

        loader = SimpleDirectoryReader(
            temp_dir,
            file_extractor=self.file_extractor,
            required_exts=self.required_exts,
            filename_as_id=self.filename_as_id,
            num_files_limit=self.num_files_limit,
            file_metadata=self.file_metadata,
        )

        return loader.load_data()

```
 |  
| --- | --- |  
options: members: - BotoMinioReader - MinioReader
