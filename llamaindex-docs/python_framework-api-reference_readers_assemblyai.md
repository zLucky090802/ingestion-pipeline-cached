# Assemblyai
##  AssemblyAIAudioTranscriptReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/assemblyai/#llama_index.readers.assemblyai.AssemblyAIAudioTranscriptReader "Permanent link")
Bases: 
Reader for AssemblyAI audio transcripts.
It uses the AssemblyAI API to transcribe audio files and loads the transcribed text into one or more Documents, depending on the specified format.
To use, you should have the `assemblyai` python package installed, and the environment variable `ASSEMBLYAI_API_KEY` set with your API key. Alternatively, the API key can also be passed as an argument.
Audio files can be specified via an URL or a local file path.
Source code in `llama-index-integrations/readers/llama-index-readers-assemblyai/llama_index/readers/assemblyai/base.py`  
| 
```
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
```
 | 
```
classAssemblyAIAudioTranscriptReader(BaseReader):
"""
    Reader for AssemblyAI audio transcripts.

    It uses the AssemblyAI API to transcribe audio files
    and loads the transcribed text into one or more Documents,
    depending on the specified format.

    To use, you should have the ``assemblyai`` python package installed, and the
    environment variable ``ASSEMBLYAI_API_KEY`` set with your API key.
    Alternatively, the API key can also be passed as an argument.

    Audio files can be specified via an URL or a local file path.
    """

    def__init__(
        self,
        file_path: str,
        *,
        transcript_format: TranscriptFormat = TranscriptFormat.TEXT,
        config: Optional[assemblyai.TranscriptionConfig] = None,
        api_key: Optional[str] = None,
    ):
"""
        Initializes the AssemblyAI AudioTranscriptReader.

        Args:
            file_path: An URL or a local file path.
            transcript_format: Transcript format to use.
                See class ``TranscriptFormat`` for more info.
            config: Transcription options and features. If ``None`` is given,
                the Transcriber's default configuration will be used.
            api_key: AssemblyAI API key.

        """
        if api_key is not None:
            assemblyai.settings.api_key = api_key

        self.file_path = file_path
        self.transcript_format = transcript_format

        # Instantiating the Transcriber will raise a ValueError if no API key is set.
        self.transcriber = assemblyai.Transcriber(config=config)

    defload_data(self) -> List[Document]:
"""
        Transcribes the audio file and loads the transcript into documents.

        It uses the AssemblyAI API to transcribe the audio file and blocks until
        the transcription is finished.
        """
        transcript = self.transcriber.transcribe(self.file_path)

        if transcript.error:
            raise ValueError(f"Could not transcribe file: {transcript.error}")

        if self.transcript_format == TranscriptFormat.TEXT:
            return [Document(text=transcript.text, metadata=transcript.json_response)]
        elif self.transcript_format == TranscriptFormat.SENTENCES:
            sentences = transcript.get_sentences()
            return [
                Document(text=s.text, metadata=s.dict(exclude={"text"}))
                for s in sentences
            ]
        elif self.transcript_format == TranscriptFormat.PARAGRAPHS:
            paragraphs = transcript.get_paragraphs()
            return [
                Document(text=p.text, metadata=p.dict(exclude={"text"}))
                for p in paragraphs
            ]
        elif self.transcript_format == TranscriptFormat.SUBTITLES_SRT:
            return [Document(text=transcript.export_subtitles_srt())]
        elif self.transcript_format == TranscriptFormat.SUBTITLES_VTT:
            return [Document(text=transcript.export_subtitles_vtt())]
        else:
            raise ValueError("Unknown transcript format.")

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/assemblyai/#llama_index.readers.assemblyai.AssemblyAIAudioTranscriptReader.load_data "Permanent link")

```
load_data() -> []

```

Transcribes the audio file and loads the transcript into documents.
It uses the AssemblyAI API to transcribe the audio file and blocks until the transcription is finished.
Source code in `llama-index-integrations/readers/llama-index-readers-assemblyai/llama_index/readers/assemblyai/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""
    Transcribes the audio file and loads the transcript into documents.

    It uses the AssemblyAI API to transcribe the audio file and blocks until
    the transcription is finished.
    """
    transcript = self.transcriber.transcribe(self.file_path)

    if transcript.error:
        raise ValueError(f"Could not transcribe file: {transcript.error}")

    if self.transcript_format == TranscriptFormat.TEXT:
        return [Document(text=transcript.text, metadata=transcript.json_response)]
    elif self.transcript_format == TranscriptFormat.SENTENCES:
        sentences = transcript.get_sentences()
        return [
            Document(text=s.text, metadata=s.dict(exclude={"text"}))
            for s in sentences
        ]
    elif self.transcript_format == TranscriptFormat.PARAGRAPHS:
        paragraphs = transcript.get_paragraphs()
        return [
            Document(text=p.text, metadata=p.dict(exclude={"text"}))
            for p in paragraphs
        ]
    elif self.transcript_format == TranscriptFormat.SUBTITLES_SRT:
        return [Document(text=transcript.export_subtitles_srt())]
    elif self.transcript_format == TranscriptFormat.SUBTITLES_VTT:
        return [Document(text=transcript.export_subtitles_vtt())]
    else:
        raise ValueError("Unknown transcript format.")

```
 |  
| --- | --- |  
##  TranscriptFormat [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/assemblyai/#llama_index.readers.assemblyai.TranscriptFormat "Permanent link")
Bases: `Enum`
Transcript format to use for the document reader.
Source code in `llama-index-integrations/readers/llama-index-readers-assemblyai/llama_index/readers/assemblyai/base.py`  
| 
```
12
13
14
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
```
 | 
```
classTranscriptFormat(Enum):
"""Transcript format to use for the document reader."""

    TEXT = "text"
"""One document with the transcription text"""
    SENTENCES = "sentences"
"""Multiple documents, splits the transcription by each sentence"""
    PARAGRAPHS = "paragraphs"
"""Multiple documents, splits the transcription by each paragraph"""
    SUBTITLES_SRT = "subtitles_srt"
"""One document with the transcript exported in SRT subtitles format"""
    SUBTITLES_VTT = "subtitles_vtt"
"""One document with the transcript exported in VTT subtitles format"""

```
 |  
| --- | --- |  
###  TEXT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/assemblyai/#llama_index.readers.assemblyai.TranscriptFormat.TEXT "Permanent link")

```
TEXT = 'text'

```

One document with the transcription text
###  SENTENCES `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/assemblyai/#llama_index.readers.assemblyai.TranscriptFormat.SENTENCES "Permanent link")

```
SENTENCES = 'sentences'

```

Multiple documents, splits the transcription by each sentence
###  PARAGRAPHS `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/assemblyai/#llama_index.readers.assemblyai.TranscriptFormat.PARAGRAPHS "Permanent link")

```
PARAGRAPHS = 'paragraphs'

```

Multiple documents, splits the transcription by each paragraph
###  SUBTITLES_SRT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/assemblyai/#llama_index.readers.assemblyai.TranscriptFormat.SUBTITLES_SRT "Permanent link")

```
SUBTITLES_SRT = 'subtitles_srt'

```

One document with the transcript exported in SRT subtitles format
###  SUBTITLES_VTT `class-attribute` `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/assemblyai/#llama_index.readers.assemblyai.TranscriptFormat.SUBTITLES_VTT "Permanent link")

```
SUBTITLES_VTT = 'subtitles_vtt'

```

One document with the transcript exported in VTT subtitles format
options: members: - AssemblyAIAudioTranscriptReader
