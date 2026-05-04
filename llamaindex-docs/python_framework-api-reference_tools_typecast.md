# Typecast
##  TypecastToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/typecast/#llama_index.tools.typecast.TypecastToolSpec "Permanent link")
Bases: 
Typecast tool spec for text-to-speech synthesis with emotion control.
Source code in `llama-index-integrations/tools/llama-index-tools-typecast/llama_index/tools/typecast/base.py`  
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
```
 | 
```
classTypecastToolSpec(BaseToolSpec):
"""Typecast tool spec for text-to-speech synthesis with emotion control."""

    spec_functions = ["get_voices", "get_voice", "text_to_speech"]

    def__init__(self, api_key: str, host: Optional[str] = None) -> None:
"""
        Initialize with parameters.

        Args:
            api_key (str): Your Typecast API key
            host (Optional[str]): The base url of Typecast API (default: https://api.typecast.ai)

        """
        self.api_key = api_key
        self.host = host

    defget_voices(
        self,
        model: Optional[str] = None,
        gender: Optional[str] = None,
        age: Optional[str] = None,
        use_case: Optional[str] = None,
    ) -> List[dict]:
"""
        Get list of available voices from Typecast (V2 API).

        Args:
            model (Optional[str]): Filter by model name (e.g., "ssfm-v21", "ssfm-v30")
            gender (Optional[str]): Filter by gender ("male" or "female")
            age (Optional[str]): Filter by age group ("child", "teenager", "young_adult", "middle_age", "elder")
            use_case (Optional[str]): Filter by use case category (e.g., "Audiobook", "Game", "Podcast")

        Returns:
            List[dict]: List of available voices with their details including:
                - voice_id: Unique voice identifier
                - voice_name: Human-readable name
                - models: List of supported models with emotions
                - gender: Voice gender (optional)
                - age: Voice age group (optional)
                - use_cases: List of suitable use cases (optional)

        Raises:
            TypecastError: If API request fails

        """
        # Create the client
        client = Typecast(host=self.host, api_key=self.api_key)

        # Build filter if any parameters provided
        filter_obj = None
        if any([model, gender, age, use_case]):
            filter_obj = VoicesV2Filter(
                model=model,
                gender=gender,
                age=age,
                use_cases=use_case,
            )

        # Get the voices using V2 API
        response = client.voices_v2(filter=filter_obj)

        # Return the dumped voice models as dict
        return [voice.model_dump() for voice in response]

    defget_voice(self, voice_id: str) -> dict:
"""
        Get details of a specific voice from Typecast (V2 API).

        Args:
            voice_id (str): The voice ID to get details for (e.g., "tc_62a8975e695ad26f7fb514d1")

        Returns:
            dict: Voice details including:
                - voice_id: Unique voice identifier
                - voice_name: Human-readable name
                - models: List of supported models with emotions
                - gender: Voice gender (optional)
                - age: Voice age group (optional)
                - use_cases: List of suitable use cases (optional)

        Raises:
            NotFoundError: If voice not found
            TypecastError: If API request fails

        """
        # Create the client
        client = Typecast(host=self.host, api_key=self.api_key)

        # Get the voice using V2 API
        response = client.voice_v2(voice_id)

        # Return the dumped voice model as dict
        return response.model_dump()

    deftext_to_speech(
        self,
        text: str,
        voice_id: str,
        output_path: str,
        model: str = "ssfm-v21",
        language: Optional[str] = None,
        emotion_preset: Optional[str] = "normal",
        emotion_intensity: Optional[float] = 1.0,
        volume: Optional[int] = 100,
        audio_pitch: Optional[int] = 0,
        audio_tempo: Optional[float] = 1.0,
        audio_format: Optional[str] = "wav",
        seed: Optional[int] = None,
    ) -> str:
"""
        Convert text to speech using Typecast API.

        Args:
            text (str): The text to convert to speech
            voice_id (str): The voice ID to use (e.g., "tc_62a8975e695ad26f7fb514d1")
            output_path (str): Path to save the audio file
            model (str): Voice model name (default: "ssfm-v21")
            language (Optional[str]): Language code (ISO 639-3, e.g., "eng", "kor")
            emotion_preset (Optional[str]): Emotion preset (normal, happy, sad, angry)
            emotion_intensity (Optional[float]): Emotion intensity (0.0 to 2.0)
            volume (Optional[int]): Volume (0 to 200, default: 100)
            audio_pitch (Optional[int]): Audio pitch (-12 to 12, default: 0)
            audio_tempo (Optional[float]): Audio tempo (0.5 to 2.0, default: 1.0)
            audio_format (Optional[str]): Audio format (wav or mp3, default: wav)
            seed (Optional[int]): Random seed for reproducible results

        Returns:
            str: Path to the generated audio file

        Raises:
            ValueError: If parameters are invalid
            BadRequestError: If request parameters are invalid
            UnauthorizedError: If API authentication fails
            PaymentRequiredError: If API quota exceeded
            NotFoundError: If resource not found
            UnprocessableEntityError: If validation error
            InternalServerError: If Typecast API server error
            TypecastError: If other API error occurs
            IOError: If file save fails

        """
        # Validate parameters
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        if not voice_id:
            raise ValueError("Voice ID is required")
        if not output_path:
            raise ValueError("Output path is required")

        # Create client
        client = Typecast(host=self.host, api_key=self.api_key)

        # Build the request
        request = TTSRequest(
            voice_id=voice_id,
            text=text,
            model=model,
            language=language,
            prompt=Prompt(
                emotion_preset=emotion_preset,
                emotion_intensity=emotion_intensity,
            ),
            output=Output(
                volume=volume,
                audio_pitch=audio_pitch,
                audio_tempo=audio_tempo,
                audio_format=audio_format,
            ),
            seed=seed,
        )

        # Generate audio
        response = client.text_to_speech(request)

        # Save the audio
        with open(output_path, "wb") as fp:
            fp.write(response.audio_data)

        # Return the save location
        return output_path

```
 |  
| --- | --- |  
###  get_voices [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/typecast/#llama_index.tools.typecast.TypecastToolSpec.get_voices "Permanent link")

```
get_voices(
    model: Optional[] = None,
    gender: Optional[] = None,
    age: Optional[] = None,
    use_case: Optional[] = None,
) -> []

```

Get list of available voices from Typecast (V2 API).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model`  |  `Optional[str]`  |  Filter by model name (e.g., "ssfm-v21", "ssfm-v30")  |  `None`  |  
|  `gender`  |  `Optional[str]`  |  Filter by gender ("male" or "female")  |  `None`  |  
|  `age`  |  `Optional[str]`  |  Filter by age group ("child", "teenager", "young_adult", "middle_age", "elder")  |  `None`  |  
|  `use_case`  |  `Optional[str]`  |  Filter by use case category (e.g., "Audiobook", "Game", "Podcast")  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[dict]`  |  List[dict]: List of available voices with their details including: - voice_id: Unique voice identifier - voice_name: Human-readable name - models: List of supported models with emotions - gender: Voice gender (optional) - age: Voice age group (optional) - use_cases: List of suitable use cases (optional)  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `TypecastError`  |  If API request fails  |  
Source code in `llama-index-integrations/tools/llama-index-tools-typecast/llama_index/tools/typecast/base.py`  
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
```
 | 
```
defget_voices(
    self,
    model: Optional[str] = None,
    gender: Optional[str] = None,
    age: Optional[str] = None,
    use_case: Optional[str] = None,
) -> List[dict]:
"""
    Get list of available voices from Typecast (V2 API).

    Args:
        model (Optional[str]): Filter by model name (e.g., "ssfm-v21", "ssfm-v30")
        gender (Optional[str]): Filter by gender ("male" or "female")
        age (Optional[str]): Filter by age group ("child", "teenager", "young_adult", "middle_age", "elder")
        use_case (Optional[str]): Filter by use case category (e.g., "Audiobook", "Game", "Podcast")

    Returns:
        List[dict]: List of available voices with their details including:
            - voice_id: Unique voice identifier
            - voice_name: Human-readable name
            - models: List of supported models with emotions
            - gender: Voice gender (optional)
            - age: Voice age group (optional)
            - use_cases: List of suitable use cases (optional)

    Raises:
        TypecastError: If API request fails

    """
    # Create the client
    client = Typecast(host=self.host, api_key=self.api_key)

    # Build filter if any parameters provided
    filter_obj = None
    if any([model, gender, age, use_case]):
        filter_obj = VoicesV2Filter(
            model=model,
            gender=gender,
            age=age,
            use_cases=use_case,
        )

    # Get the voices using V2 API
    response = client.voices_v2(filter=filter_obj)

    # Return the dumped voice models as dict
    return [voice.model_dump() for voice in response]

```
 |  
| --- | --- |  
###  get_voice [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/typecast/#llama_index.tools.typecast.TypecastToolSpec.get_voice "Permanent link")

```
get_voice(voice_id: ) -> 

```

Get details of a specific voice from Typecast (V2 API).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `voice_id`  |  The voice ID to get details for (e.g., "tc_62a8975e695ad26f7fb514d1")  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `dict`  |  `dict`  |  Voice details including: - voice_id: Unique voice identifier - voice_name: Human-readable name - models: List of supported models with emotions - gender: Voice gender (optional) - age: Voice age group (optional) - use_cases: List of suitable use cases (optional)  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `NotFoundError`  |  If voice not found  |  
|  `TypecastError`  |  If API request fails  |  
Source code in `llama-index-integrations/tools/llama-index-tools-typecast/llama_index/tools/typecast/base.py`  
| 
```
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
```
 | 
```
defget_voice(self, voice_id: str) -> dict:
"""
    Get details of a specific voice from Typecast (V2 API).

    Args:
        voice_id (str): The voice ID to get details for (e.g., "tc_62a8975e695ad26f7fb514d1")

    Returns:
        dict: Voice details including:
            - voice_id: Unique voice identifier
            - voice_name: Human-readable name
            - models: List of supported models with emotions
            - gender: Voice gender (optional)
            - age: Voice age group (optional)
            - use_cases: List of suitable use cases (optional)

    Raises:
        NotFoundError: If voice not found
        TypecastError: If API request fails

    """
    # Create the client
    client = Typecast(host=self.host, api_key=self.api_key)

    # Get the voice using V2 API
    response = client.voice_v2(voice_id)

    # Return the dumped voice model as dict
    return response.model_dump()

```
 |  
| --- | --- |  
###  text_to_speech [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/typecast/#llama_index.tools.typecast.TypecastToolSpec.text_to_speech "Permanent link")

```
text_to_speech(
    text: ,
    voice_id: ,
    output_path: ,
    model:  = "ssfm-v21",
    language: Optional[] = None,
    emotion_preset: Optional[] = "normal",
    emotion_intensity: Optional[float] = 1.0,
    volume: Optional[] = 100,
    audio_pitch: Optional[] = 0,
    audio_tempo: Optional[float] = 1.0,
    audio_format: Optional[] = "wav",
    seed: Optional[] = None,
) -> 

```

Convert text to speech using Typecast API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text`  |  The text to convert to speech  |  _required_  |  
|  `voice_id`  |  The voice ID to use (e.g., "tc_62a8975e695ad26f7fb514d1")  |  _required_  |  
|  `output_path`  |  Path to save the audio file  |  _required_  |  
|  `model`  |  Voice model name (default: "ssfm-v21")  |  `'ssfm-v21'`  |  
|  `language`  |  `Optional[str]`  |  Language code (ISO 639-3, e.g., "eng", "kor")  |  `None`  |  
|  `emotion_preset`  |  `Optional[str]`  |  Emotion preset (normal, happy, sad, angry)  |  `'normal'`  |  
|  `emotion_intensity`  |  `Optional[float]`  |  Emotion intensity (0.0 to 2.0)  |  `1.0`  |  
|  `volume`  |  `Optional[int]`  |  Volume (0 to 200, default: 100)  |  `100`  |  
|  `audio_pitch`  |  `Optional[int]`  |  Audio pitch (-12 to 12, default: 0)  |  
|  `audio_tempo`  |  `Optional[float]`  |  Audio tempo (0.5 to 2.0, default: 1.0)  |  `1.0`  |  
|  `audio_format`  |  `Optional[str]`  |  Audio format (wav or mp3, default: wav)  |  `'wav'`  |  
|  `seed`  |  `Optional[int]`  |  Random seed for reproducible results  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Path to the generated audio file  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If parameters are invalid  |  
|  `BadRequestError`  |  If request parameters are invalid  |  
|  `UnauthorizedError`  |  If API authentication fails  |  
|  `PaymentRequiredError`  |  If API quota exceeded  |  
|  `NotFoundError`  |  If resource not found  |  
|  `UnprocessableEntityError`  |  If validation error  |  
|  `InternalServerError`  |  If Typecast API server error  |  
|  `TypecastError`  |  If other API error occurs  |  
|  `IOError`  |  If file save fails  |  
Source code in `llama-index-integrations/tools/llama-index-tools-typecast/llama_index/tools/typecast/base.py`  
| 
```
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
```
 | 
```
deftext_to_speech(
    self,
    text: str,
    voice_id: str,
    output_path: str,
    model: str = "ssfm-v21",
    language: Optional[str] = None,
    emotion_preset: Optional[str] = "normal",
    emotion_intensity: Optional[float] = 1.0,
    volume: Optional[int] = 100,
    audio_pitch: Optional[int] = 0,
    audio_tempo: Optional[float] = 1.0,
    audio_format: Optional[str] = "wav",
    seed: Optional[int] = None,
) -> str:
"""
    Convert text to speech using Typecast API.

    Args:
        text (str): The text to convert to speech
        voice_id (str): The voice ID to use (e.g., "tc_62a8975e695ad26f7fb514d1")
        output_path (str): Path to save the audio file
        model (str): Voice model name (default: "ssfm-v21")
        language (Optional[str]): Language code (ISO 639-3, e.g., "eng", "kor")
        emotion_preset (Optional[str]): Emotion preset (normal, happy, sad, angry)
        emotion_intensity (Optional[float]): Emotion intensity (0.0 to 2.0)
        volume (Optional[int]): Volume (0 to 200, default: 100)
        audio_pitch (Optional[int]): Audio pitch (-12 to 12, default: 0)
        audio_tempo (Optional[float]): Audio tempo (0.5 to 2.0, default: 1.0)
        audio_format (Optional[str]): Audio format (wav or mp3, default: wav)
        seed (Optional[int]): Random seed for reproducible results

    Returns:
        str: Path to the generated audio file

    Raises:
        ValueError: If parameters are invalid
        BadRequestError: If request parameters are invalid
        UnauthorizedError: If API authentication fails
        PaymentRequiredError: If API quota exceeded
        NotFoundError: If resource not found
        UnprocessableEntityError: If validation error
        InternalServerError: If Typecast API server error
        TypecastError: If other API error occurs
        IOError: If file save fails

    """
    # Validate parameters
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    if not voice_id:
        raise ValueError("Voice ID is required")
    if not output_path:
        raise ValueError("Output path is required")

    # Create client
    client = Typecast(host=self.host, api_key=self.api_key)

    # Build the request
    request = TTSRequest(
        voice_id=voice_id,
        text=text,
        model=model,
        language=language,
        prompt=Prompt(
            emotion_preset=emotion_preset,
            emotion_intensity=emotion_intensity,
        ),
        output=Output(
            volume=volume,
            audio_pitch=audio_pitch,
            audio_tempo=audio_tempo,
            audio_format=audio_format,
        ),
        seed=seed,
    )

    # Generate audio
    response = client.text_to_speech(request)

    # Save the audio
    with open(output_path, "wb") as fp:
        fp.write(response.audio_data)

    # Return the save location
    return output_path

```
 |  
| --- | --- |  
options: members: - TypecastToolSpec
