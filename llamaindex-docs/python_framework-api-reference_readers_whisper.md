# Whisper
##  WhisperReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/whisper/#llama_index.readers.whisper.WhisperReader "Permanent link")
Bases: 
Whisper reader.
Reads audio files and transcribes them using the OpenAI Whisper API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  The OpenAI Whisper model to use. Defaults to "whisper-1".  |  `'whisper-1'`  |  
|  `api_key`  |  `Optional[str]`  |  The OpenAI API key to use. Uses OPENAI_API_KEY environment variable if not provided.  |  `None`  |  
|  `client`  |  `Optional[OpenAI]`  |  An existing OpenAI client to use.  |  `None`  |  
|  `async_client`  |  `Optional[AsyncOpenAI]`  |  An existing AsyncOpenAI client to use.  |  `None`  |  
|  `client_kwargs`  |  `Optional[dict]`  |  Additional keyword arguments to pass to the OpenAI client.  |  `None`  |  
|  `transcribe_kwargs`  |  `Optional[dict]`  |  Additional keyword arguments to pass to the transcribe method.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-whisper/llama_index/readers/whisper/base.py`  
| 
```
 15
 16
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
```
 | 
```
classWhisperReader(BaseReader):
"""
    Whisper reader.

    Reads audio files and transcribes them using the OpenAI Whisper API.

    Args:
        model (str): The OpenAI Whisper model to use. Defaults to "whisper-1".
        api_key (Optional[str]): The OpenAI API key to use. Uses OPENAI_API_KEY environment variable if not provided.
        client (Optional[OpenAI]): An existing OpenAI client to use.
        async_client (Optional[AsyncOpenAI]): An existing AsyncOpenAI client to use.
        client_kwargs (Optional[dict]): Additional keyword arguments to pass to the OpenAI client.
        transcribe_kwargs (Optional[dict]): Additional keyword arguments to pass to the transcribe method.

    """

    def__init__(
        self,
        model: str = "whisper-1",
        language: str = "en",
        prompt: Optional[str] = None,
        api_key: Optional[str] = None,
        client: Optional[OpenAI] = None,
        async_client: Optional[AsyncOpenAI] = None,
        client_kwargs: Optional[dict] = None,
        transcribe_kwargs: Optional[dict] = None,
    ) -> None:
"""Initialize with arguments."""
        super().__init__()
        client_kwargs = client_kwargs or {}
        self.model = model
        self.language = language
        self.prompt = prompt
        self.client = client or OpenAI(api_key=api_key, **client_kwargs)
        self.async_client = async_client or AsyncOpenAI(
            api_key=api_key, **client_kwargs
        )

        self.transcribe_kwargs = transcribe_kwargs or {}

    def_get_default_fs(self) -> LocalFileSystem:
"""Get the default filesystem."""
        return LocalFileSystem()

    def_get_file_path_or_bytes(
        self,
        input_file: Union[str, Path, bytes],
        fs: Optional[AbstractFileSystem] = None,
    ) -> Union[str, BytesIO]:
"""Get the file bytes."""
        fs = fs or self._get_default_fs()

        if isinstance(input_file, (str, Path)):
            abs_path = os.path.abspath(str(input_file))
            if not os.path.exists(abs_path):
                raise ValueError(f"File not found: {abs_path}")

            return abs_path
        elif isinstance(input_file, bytes):
            file_bytes = BytesIO(input_file)
            file_bytes.name = "audio.mp3"
            return file_bytes
        elif hasattr(input_file, "read"):  # File-like object
            return input_file
        else:
            raise ValueError("Invalid input file type")

    def_transcribe(
        self,
        file_path_or_bytes: Union[str, BytesIO],
        transcribe_kwargs: Optional[dict] = None,
    ) -> str:
"""Transcribe the audio file."""
        transcribe_kwargs = transcribe_kwargs or self.transcribe_kwargs

        if isinstance(file_path_or_bytes, str):
            # If it's a file path, open it directly
            with open(file_path_or_bytes, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=self.language,
                    response_format="text",
                    prompt=self.prompt,
                    **transcribe_kwargs,
                )
        else:
            # Handle BytesIO case (we'll improve this later)
            file_path_or_bytes.seek(0)
            response = self.client.audio.transcriptions.create(
                model=self.model,
                file=file_path_or_bytes,
                language=self.language,
                response_format="text",
                prompt=self.prompt,
                **transcribe_kwargs,
            )

        return response

    async def_transcribe_async(
        self,
        file_path_or_bytes: Union[str, BytesIO],
        transcribe_kwargs: Optional[dict] = None,
    ) -> str:
"""Transcribe the audio file asynchronously."""
        transcribe_kwargs = transcribe_kwargs or self.transcribe_kwargs

        if isinstance(file_path_or_bytes, str):
            # If it's a file path, open it directly
            with open(file_path_or_bytes, "rb") as audio_file:
                response = await self.async_client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=self.language,
                    response_format="text",
                    prompt=self.prompt,
                    **transcribe_kwargs,
                )
        else:
            # Handle BytesIO case (we'll improve this later)
            file_path_or_bytes.seek(0)
            response = await self.async_client.audio.transcriptions.create(
                model=self.model,
                file=file_path_or_bytes,
                language=self.language,
                response_format="text",
                prompt=self.prompt,
                **transcribe_kwargs,
            )

        return response

    defload_data(
        self,
        input_file: Union[str, Path, bytes],
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
        **transcribe_kwargs: dict,
    ) -> List[Document]:
"""Load data from the input file."""
        file_path_or_bytes = self._get_file_path_or_bytes(input_file, fs)

        text = self._transcribe(file_path_or_bytes, transcribe_kwargs)
        metadata = extra_info or {}
        return [Document(text=text, metadata=metadata)]

    async defaload_data(
        self,
        input_file: Union[str, Path, bytes],
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
        **transcribe_kwargs: dict,
    ) -> List[Document]:
"""Load data from the input file asynchronously."""
        file_path_or_bytes = self._get_file_path_or_bytes(input_file, fs)

        text = await self._transcribe_async(file_path_or_bytes, transcribe_kwargs)
        metadata = extra_info or {}
        return [Document(text=text, metadata=metadata)]

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/whisper/#llama_index.readers.whisper.WhisperReader.load_data "Permanent link")

```
load_data(
    input_file: Union[, , bytes],
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
    **transcribe_kwargs: 
) -> []

```

Load data from the input file.
Source code in `llama-index-integrations/readers/llama-index-readers-whisper/llama_index/readers/whisper/base.py`  
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
```
 | 
```
defload_data(
    self,
    input_file: Union[str, Path, bytes],
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
    **transcribe_kwargs: dict,
) -> List[Document]:
"""Load data from the input file."""
    file_path_or_bytes = self._get_file_path_or_bytes(input_file, fs)

    text = self._transcribe(file_path_or_bytes, transcribe_kwargs)
    metadata = extra_info or {}
    return [Document(text=text, metadata=metadata)]

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/whisper/#llama_index.readers.whisper.WhisperReader.aload_data "Permanent link")

```
aload_data(
    input_file: Union[, , bytes],
    extra_info: Optional[] = None,
    fs: Optional[AbstractFileSystem] = None,
    **transcribe_kwargs: 
) -> []

```

Load data from the input file asynchronously.
Source code in `llama-index-integrations/readers/llama-index-readers-whisper/llama_index/readers/whisper/base.py`  
| 
```
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
async defaload_data(
    self,
    input_file: Union[str, Path, bytes],
    extra_info: Optional[Dict] = None,
    fs: Optional[AbstractFileSystem] = None,
    **transcribe_kwargs: dict,
) -> List[Document]:
"""Load data from the input file asynchronously."""
    file_path_or_bytes = self._get_file_path_or_bytes(input_file, fs)

    text = await self._transcribe_async(file_path_or_bytes, transcribe_kwargs)
    metadata = extra_info or {}
    return [Document(text=text, metadata=metadata)]

```
 |  
| --- | --- |  
options: members: - WhisperReader
