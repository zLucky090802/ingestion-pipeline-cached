# Azure speech
##  AzureSpeechToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/azure_speech/#llama_index.tools.azure_speech.AzureSpeechToolSpec "Permanent link")
Bases: 
Azure Speech tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-azure-speech/llama_index/tools/azure_speech/base.py`  
| 
```
 9
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
```
 | 
```
classAzureSpeechToolSpec(BaseToolSpec):
"""Azure Speech tool spec."""

    spec_functions = ["speech_to_text", "text_to_speech"]

    def__init__(
        self, region: str, speech_key: str, language: Optional[str] = "en-US"
    ) -> None:
        importazure.cognitiveservices.speechasspeechsdk

"""Initialize with parameters."""
        self.config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
        self.config.speech_recognition_language = language

    deftext_to_speech(self, text: str) -> None:
"""
        This tool accepts a natural language string and will use Azure speech services to create an
        audio version of the text, and play it on the users computer.

        Args:
            text (str): The text to play

        """
        importazure.cognitiveservices.speechasspeechsdk

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.config)
        result = speech_synthesizer.speak_text(text)

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            speechsdk.AudioDataStream(result)
            return "Audio playback complete."
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
                return None
            return None
        return None

    def_transcribe(self, speech_recognizer) -> List[str]:
        done = False
        results = []

        defstop_cb(evt) -> None:
"""Callback that stop continuous recognition."""
            speech_recognizer.stop_continuous_recognition_async()
            nonlocal done
            done = True

        speech_recognizer.recognized.connect(
            lambda evt, results=results: results.append(evt.result.text)
        )
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition_async()
        while not done:
            time.sleep(0.5)

        return results

    defspeech_to_text(self, filename: str) -> List[str]:
"""
        This tool accepts a filename for a speech audio file and uses Azure to transcribe it into text.

        Args:
            filename (str): The name of the file to transcribe

        """
        importazure.cognitiveservices.speechasspeechsdk

        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.config,
            audio_config=speechsdk.audio.AudioConfig(filename=filename),
        )
        return self._transcribe(speech_recognizer)

```
 |  
| --- | --- |  
###  text_to_speech [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/azure_speech/#llama_index.tools.azure_speech.AzureSpeechToolSpec.text_to_speech "Permanent link")

```
text_to_speech(text: ) -> None

```

This tool accepts a natural language string and will use Azure speech services to create an audio version of the text, and play it on the users computer.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text`  |  The text to play  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-azure-speech/llama_index/tools/azure_speech/base.py`  
| 
```
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
```
 | 
```
deftext_to_speech(self, text: str) -> None:
"""
    This tool accepts a natural language string and will use Azure speech services to create an
    audio version of the text, and play it on the users computer.

    Args:
        text (str): The text to play

    """
    importazure.cognitiveservices.speechasspeechsdk

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.config)
    result = speech_synthesizer.speak_text(text)

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        speechsdk.AudioDataStream(result)
        return "Audio playback complete."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
            return None
        return None
    return None

```
 |  
| --- | --- |  
###  speech_to_text [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/azure_speech/#llama_index.tools.azure_speech.AzureSpeechToolSpec.speech_to_text "Permanent link")

```
speech_to_text(filename: ) -> []

```

This tool accepts a filename for a speech audio file and uses Azure to transcribe it into text.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `filename`  |  The name of the file to transcribe  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-azure-speech/llama_index/tools/azure_speech/base.py`  
| 
```
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
```
 | 
```
defspeech_to_text(self, filename: str) -> List[str]:
"""
    This tool accepts a filename for a speech audio file and uses Azure to transcribe it into text.

    Args:
        filename (str): The name of the file to transcribe

    """
    importazure.cognitiveservices.speechasspeechsdk

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=self.config,
        audio_config=speechsdk.audio.AudioConfig(filename=filename),
    )
    return self._transcribe(speech_recognizer)

```
 |  
| --- | --- |  
options: members: - AzureSpeechToolSpec
