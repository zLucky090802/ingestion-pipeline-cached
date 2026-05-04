# Elevenlabs
##  ElevenLabsToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/elevenlabs/#llama_index.tools.elevenlabs.ElevenLabsToolSpec "Permanent link")
Bases: 
ElevenLabs tool spec for text-to-speech synthesis.
Source code in `llama-index-integrations/tools/llama-index-tools-elevenlabs/llama_index/tools/elevenlabs/base.py`  
| 
```



 10
 11
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
```
 | 
```
classElevenLabsToolSpec(BaseToolSpec):
"""ElevenLabs tool spec for text-to-speech synthesis."""

    spec_functions = ["get_voices", "text_to_speech"]

    def__init__(
        self, api_key: str, base_url: Optional[str] = "https://api.elevenlabs.io"
    ) -> None:
"""
        Initialize with parameters.

        Args:
            api_key (str): Your ElevenLabs API key
            base_url (Optional[str]): The base url of elevenlabs

        """
        self.api_key = api_key
        self.base_url = base_url

    defget_voices(self) -> List[dict]:
"""
        Get list of available voices from ElevenLabs.

        Returns:
            List[dict]: List of available voices with their details

        """
        fromelevenlabsimport ElevenLabs

        # Create the client
        client = ElevenLabs(base_url=self.base_url, api_key=self.api_key)

        # Get the voices
        response = client.voices.get_all()

        # Return the dumped voice models as dict
        return [voice.model_dump() for voice in response.voices]

    deftext_to_speech(
        self,
        text: str,
        output_path: str,
        voice_id: Optional[str] = None,
        voice_stability: Optional[float] = None,
        voice_similarity_boost: Optional[float] = None,
        voice_style: Optional[float] = None,
        voice_use_speaker_boost: Optional[bool] = None,
        model_id: Optional[str] = "eleven_monolingual_v1",
    ) -> str:
"""
        Convert text to speech using ElevenLabs API.

        Args:
            text (str): The text to convert to speech
            output_path (str): Where to save the output file
            output_path (str): Path to save the audio file. If None, generates one
            voice_id (Optional[str]): Override the default voice ID
            voice_stability (Optional[float]): The stability setting of the voice
            voice_similarity_boost (Optional[float]): The similarity boost setting of the voice
            voice_style: (Optional[float]): The style setting of the voice
            voice_use_speaker_boost (Optional[bool]): Whether to use speaker boost or not
            model_id (Optional[str]): Override the default model ID

        Returns:
            str: Path to the generated audio file

        """
        fromelevenlabsimport ElevenLabs, VoiceSettings
        fromelevenlabs.clientimport DEFAULT_VOICE

        # Create client
        client = ElevenLabs(base_url=self.base_url, api_key=self.api_key)

        # Default the settings if not supplied
        if voice_stability is None:
            voice_stability = DEFAULT_VOICE.settings.stability

        if voice_similarity_boost is None:
            voice_similarity_boost = DEFAULT_VOICE.settings.similarity_boost

        if voice_style is None:
            voice_style = DEFAULT_VOICE.settings.style

        if voice_use_speaker_boost is None:
            voice_use_speaker_boost = DEFAULT_VOICE.settings.use_speaker_boost

        # Create the VoiceSettings
        voice_settings = VoiceSettings(
            stability=voice_stability,
            similarity_boost=voice_similarity_boost,
            style=voice_style,
            use_speaker_boost=voice_use_speaker_boost,
        )

        # Generate audio
        audio = client.generate(
            text=text, voice=voice_id, voice_settings=voice_settings, model=model_id
        )

        # Save the audio
        with open(output_path, "wb") as fp:
            fp.write(b"".join(audio))

        # Return the save location
        return output_path

```
 |  
| --- | --- |  
###  get_voices [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/elevenlabs/#llama_index.tools.elevenlabs.ElevenLabsToolSpec.get_voices "Permanent link")

```
get_voices() -> []

```

Get list of available voices from ElevenLabs.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[dict]`  |  List[dict]: List of available voices with their details  |  
Source code in `llama-index-integrations/tools/llama-index-tools-elevenlabs/llama_index/tools/elevenlabs/base.py`  
| 
```
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
```
 | 
```
defget_voices(self) -> List[dict]:
"""
    Get list of available voices from ElevenLabs.

    Returns:
        List[dict]: List of available voices with their details

    """
    fromelevenlabsimport ElevenLabs

    # Create the client
    client = ElevenLabs(base_url=self.base_url, api_key=self.api_key)

    # Get the voices
    response = client.voices.get_all()

    # Return the dumped voice models as dict
    return [voice.model_dump() for voice in response.voices]

```
 |  
| --- | --- |  
###  text_to_speech [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/elevenlabs/#llama_index.tools.elevenlabs.ElevenLabsToolSpec.text_to_speech "Permanent link")

```
text_to_speech(
    text: ,
    output_path: ,
    voice_id: Optional[] = None,
    voice_stability: Optional[float] = None,
    voice_similarity_boost: Optional[float] = None,
    voice_style: Optional[float] = None,
    voice_use_speaker_boost: Optional[] = None,
    model_id: Optional[] = "eleven_monolingual_v1",
) -> 

```

Convert text to speech using ElevenLabs API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text`  |  The text to convert to speech  |  _required_  |  
|  `output_path`  |  Where to save the output file  |  _required_  |  
|  `output_path`  |  Path to save the audio file. If None, generates one  |  _required_  |  
|  `voice_id`  |  `Optional[str]`  |  Override the default voice ID  |  `None`  |  
|  `voice_stability`  |  `Optional[float]`  |  The stability setting of the voice  |  `None`  |  
|  `voice_similarity_boost`  |  `Optional[float]`  |  The similarity boost setting of the voice  |  `None`  |  
|  `voice_style`  |  `Optional[float]`  |  (Optional[float]): The style setting of the voice  |  `None`  |  
|  `voice_use_speaker_boost`  |  `Optional[bool]`  |  Whether to use speaker boost or not  |  `None`  |  
|  `model_id`  |  `Optional[str]`  |  Override the default model ID  |  `'eleven_monolingual_v1'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Path to the generated audio file  |  
Source code in `llama-index-integrations/tools/llama-index-tools-elevenlabs/llama_index/tools/elevenlabs/base.py`  
| 
```
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
```
 | 
```
deftext_to_speech(
    self,
    text: str,
    output_path: str,
    voice_id: Optional[str] = None,
    voice_stability: Optional[float] = None,
    voice_similarity_boost: Optional[float] = None,
    voice_style: Optional[float] = None,
    voice_use_speaker_boost: Optional[bool] = None,
    model_id: Optional[str] = "eleven_monolingual_v1",
) -> str:
"""
    Convert text to speech using ElevenLabs API.

    Args:
        text (str): The text to convert to speech
        output_path (str): Where to save the output file
        output_path (str): Path to save the audio file. If None, generates one
        voice_id (Optional[str]): Override the default voice ID
        voice_stability (Optional[float]): The stability setting of the voice
        voice_similarity_boost (Optional[float]): The similarity boost setting of the voice
        voice_style: (Optional[float]): The style setting of the voice
        voice_use_speaker_boost (Optional[bool]): Whether to use speaker boost or not
        model_id (Optional[str]): Override the default model ID

    Returns:
        str: Path to the generated audio file

    """
    fromelevenlabsimport ElevenLabs, VoiceSettings
    fromelevenlabs.clientimport DEFAULT_VOICE

    # Create client
    client = ElevenLabs(base_url=self.base_url, api_key=self.api_key)

    # Default the settings if not supplied
    if voice_stability is None:
        voice_stability = DEFAULT_VOICE.settings.stability

    if voice_similarity_boost is None:
        voice_similarity_boost = DEFAULT_VOICE.settings.similarity_boost

    if voice_style is None:
        voice_style = DEFAULT_VOICE.settings.style

    if voice_use_speaker_boost is None:
        voice_use_speaker_boost = DEFAULT_VOICE.settings.use_speaker_boost

    # Create the VoiceSettings
    voice_settings = VoiceSettings(
        stability=voice_stability,
        similarity_boost=voice_similarity_boost,
        style=voice_style,
        use_speaker_boost=voice_use_speaker_boost,
    )

    # Generate audio
    audio = client.generate(
        text=text, voice=voice_id, voice_settings=voice_settings, model=model_id
    )

    # Save the audio
    with open(output_path, "wb") as fp:
        fp.write(b"".join(audio))

    # Return the save location
    return output_path

```
 |  
| --- | --- |  
options: members: - ElevenLabsToolSpec
