# Gemini live
##  GeminiLiveVoiceAgent [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgent "Permanent link")
Bases: `BaseVoiceAgent`
Gemini Live Voice Agent.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/base.py`  
| 
```
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
```
 | 
```
classGeminiLiveVoiceAgent(BaseVoiceAgent):
"""
    Gemini Live Voice Agent.
    """

    def__init__(
        self,
        model: Optional[str] = None,
        interface: Optional[GeminiLiveVoiceAgentInterface] = None,
        api_key: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
    ):
        self.model: str = model or DEFAULT_MODEL
        self._client: Optional[Client] = None
        self.session: Optional[AsyncSession] = None
        self._quitflag: bool = False
        interface = interface or GeminiLiveVoiceAgentInterface()
        super().__init__(api_key=api_key, tools=tools, interface=interface)
        if self.tools is not None:
            self.gemini_tools: List[Dict[str, List[Dict[str, str]]]] = (
                tools_to_gemini_tools(tools)
            )
            self._functions_dict: Dict[
                str, Callable[[Dict[str, Any], str, str], types.FunctionResponse]
            ] = tools_to_functions_dict(self.tools)
        else:
            self.gemini_tools = []
            self._functions_dict = {}

    @property
    defclient(self) -> Client:
        if not self._client:
            try:
                package_v = version("llama-index-voice-agents-gemini-live")
            except PackageNotFoundError:
                package_v = "0.0.0"

            self._client = Client(
                api_key=self.api_key,
                http_options={
                    "api_version": "v1beta",
                    "headers": {"x-goog-api-client": f"llamaindex/{package_v}"},
                },
            )
        return self._client

    def_signal_exit(self):
        logging.info("Preparing exit...")
        self._quitflag = True

    @override
    async def_start(self, session: AsyncSession) -> None:
"""
        Start the voice agent.
        """
        self.interface.start(session=session)

    async def_run_loop(self) -> None:
        logging.info("The agent is ready for the conversation")
        logging.info("Type q and press enter to stop the conversation at any time")
        while not self._quitflag:
            text = await asyncio.to_thread(
                input,
                "",
            )
            if text == "q":
                self._signal_exit()
            await self.session.send(input=text or ".", end_of_turn=True)
        logging.info("Session has been successfully closed")
        await self.interrupt()
        await self.stop()

    async defsend(self) -> None:
"""
        Send audio to the websocket underlying the voice agent.
        """
        while True:
            msg = await self.interface.out_queue.get()
            await self.session.send(input=msg)

    @override
    async defhandle_message(self) -> Any:
"""
        Handle incoming message.

        Args:
            message (Any): incoming message (should be dict, but it is kept open also for other types).
            *args: Can take any positional argument.
            **kwargs: Can take any keyword argument.

        Returns:
            out (Any): This function can return any output.

        """
        while True:
            turn = self.session.receive()
            async for response in turn:
                if response.server_content:
                    if data := response.data:
                        await self.interface.receive(data=data)
                        self._messages.append(
                            ChatMessage(
                                role="assistant", blocks=[AudioBlock(audio=data)]
                            )
                        )
                        self._events.append(
                            AudioReceivedEvent(type_t="audio_received", data=data)
                        )
                        continue
                    if text := response.text:
                        self._messages.append(
                            ChatMessage(role="assistant", blocks=[TextBlock(text=text)])
                        )
                        self._events.append(
                            TextReceivedEvent(type_t="text_received", text=text)
                        )
                elif tool_call := response.tool_call:
                    function_responses: List[types.FunctionResponse] = []
                    for fn_call in tool_call.function_calls:
                        self._events.append(
                            ToolCallEvent(
                                type_t="tool_call",
                                tool_name=fn_call.name,
                                tool_args=fn_call.args,
                            )
                        )
                        result = self._functions_dict[fn_call.name](
                            fn_call.args, fn_call.id, fn_call.name
                        )
                        self._events.append(
                            ToolCallResultEvent(
                                type_t="tool_call_result",
                                tool_name=result.name,
                                tool_result=result.response,
                            )
                        )
                        function_responses.append(result)
                    await self.session.send_tool_response(
                        function_responses=function_responses
                    )
            while not self.interface.audio_in_queue.empty():
                await self.interrupt()

    async defstart(self):
        try:
            async with (
                self.client.aio.live.connect(
                    model=self.model,
                    config={
                        "response_modalities": ["AUDIO"],
                        "tools": self.gemini_tools,
                    },
                ) as session,
                asyncio.TaskGroup() as tg,
            ):
                self.session = session
                await self._start(session=session)

                _run_loop = tg.create_task(self._run_loop())
                tg.create_task(self.send())
                tg.create_task(self.interface._microphone_callback())
                tg.create_task(self.handle_message())
                tg.create_task(self.interface.output())

                await _run_loop
                raise asyncio.CancelledError("User requested exit")

        except asyncio.CancelledError:
            pass
        except ExceptionGroup as EG:
            await self.stop()

    async definterrupt(self) -> None:
"""
        Interrupt the input/output audio flow.

        Args:
            None
        Returns:
            out (None): This function does not return anything.

        """
        self.interface.interrupt()

    async defstop(self) -> None:
"""
        Stop the conversation with the voice agent.

        Args:
            None
        Returns:
            out (None): This function does not return anything.

        """
        self.interface.stop()

```
 |  
| --- | --- |  
###  send [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgent.send "Permanent link")

```
send() -> None

```

Send audio to the websocket underlying the voice agent.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/base.py`  
| 
```
100
101
102
103
104
105
106
```
 | 
```
async defsend(self) -> None:
"""
    Send audio to the websocket underlying the voice agent.
    """
    while True:
        msg = await self.interface.out_queue.get()
        await self.session.send(input=msg)

```
 |  
| --- | --- |  
###  handle_message [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgent.handle_message "Permanent link")

```
handle_message() -> 

```

Handle incoming message.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `message`  |  incoming message (should be dict, but it is kept open also for other types).  |  _required_  |  
|  `*args`  |  Can take any positional argument.  |  _required_  |  
|  `**kwargs`  |  Can take any keyword argument.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `out`  |  This function can return any output.  |  
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/base.py`  
| 
```
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
```
 | 
```
@override
async defhandle_message(self) -> Any:
"""
    Handle incoming message.

    Args:
        message (Any): incoming message (should be dict, but it is kept open also for other types).
        *args: Can take any positional argument.
        **kwargs: Can take any keyword argument.

    Returns:
        out (Any): This function can return any output.

    """
    while True:
        turn = self.session.receive()
        async for response in turn:
            if response.server_content:
                if data := response.data:
                    await self.interface.receive(data=data)
                    self._messages.append(
                        ChatMessage(
                            role="assistant", blocks=[AudioBlock(audio=data)]
                        )
                    )
                    self._events.append(
                        AudioReceivedEvent(type_t="audio_received", data=data)
                    )
                    continue
                if text := response.text:
                    self._messages.append(
                        ChatMessage(role="assistant", blocks=[TextBlock(text=text)])
                    )
                    self._events.append(
                        TextReceivedEvent(type_t="text_received", text=text)
                    )
            elif tool_call := response.tool_call:
                function_responses: List[types.FunctionResponse] = []
                for fn_call in tool_call.function_calls:
                    self._events.append(
                        ToolCallEvent(
                            type_t="tool_call",
                            tool_name=fn_call.name,
                            tool_args=fn_call.args,
                        )
                    )
                    result = self._functions_dict[fn_call.name](
                        fn_call.args, fn_call.id, fn_call.name
                    )
                    self._events.append(
                        ToolCallResultEvent(
                            type_t="tool_call_result",
                            tool_name=result.name,
                            tool_result=result.response,
                        )
                    )
                    function_responses.append(result)
                await self.session.send_tool_response(
                    function_responses=function_responses
                )
        while not self.interface.audio_in_queue.empty():
            await self.interrupt()

```
 |  
| --- | --- |  
###  interrupt [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgent.interrupt "Permanent link")

```
interrupt() -> None

```

Interrupt the input/output audio flow.
Returns: out (None): This function does not return anything.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/base.py`  
| 
```
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
```
 | 
```
async definterrupt(self) -> None:
"""
    Interrupt the input/output audio flow.

    Args:
        None
    Returns:
        out (None): This function does not return anything.

    """
    self.interface.interrupt()

```
 |  
| --- | --- |  
###  stop [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgent.stop "Permanent link")

```
stop() -> None

```

Stop the conversation with the voice agent.
Returns: out (None): This function does not return anything.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/base.py`  
| 
```
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
```
 | 
```
async defstop(self) -> None:
"""
    Stop the conversation with the voice agent.

    Args:
        None
    Returns:
        out (None): This function does not return anything.

    """
    self.interface.stop()

```
 |  
| --- | --- |  
##  GeminiLiveVoiceAgentInterface [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgentInterface "Permanent link")
Bases: `BaseVoiceAgentInterface`
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/audio_interface.py`  
| 
```
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
```
 | 
```
classGeminiLiveVoiceAgentInterface(BaseVoiceAgentInterface):
    def__init__(self) -> None:
        self.audio_in_queue: Optional[asyncio.Queue] = None
        self.out_queue: Optional[asyncio.Queue] = None

        self.session: Optional[AsyncSession] = None
        self.audio_stream: Optional[pyaudio.Stream] = None

    def_speaker_callback(self, *args: Any, **kwargs: Any) -> Any:
"""
        Callback function for the audio output device.

        Args:
            *args: Can take any positional argument.
            **kwargs: Can take any keyword argument.

        Returns:
            out (Any): This function can return any output.

        """

    @override
    async def_microphone_callback(self) -> None:
"""
        Callback function for the audio input device.

        Args:
            *args: Can take any positional argument.
            **kwargs: Can take any keyword argument.

        Returns:
            out (Any): This function can return any output.

        """
        mic_info = pya.get_default_input_device_info()
        self.audio_stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )
        if __debug__:
            kwargs = {"exception_on_overflow": False}
        else:
            kwargs = {}
        while True:
            data = await asyncio.to_thread(self.audio_stream.read, CHUNK_SIZE, **kwargs)
            await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})

    @override
    defstart(self, session: AsyncSession) -> None:
"""
        Start the interface.

        Args:
            session (AsyncSession): the session to which the API is bound.

        """
        self.session = session
        self.audio_in_queue = asyncio.Queue()
        self.out_queue = asyncio.Queue(maxsize=5)

    defstop(self) -> None:
"""
        Stop the interface.

        Args:
            None
        Returns:
            out (None): This function does not return anything.

        """
        if self.audio_stream:
            self.audio_stream.close()
        else:
            raise ValueError("Audio stream has never been opened, cannot be closed.")

    definterrupt(self) -> None:
"""
        Interrupt the interface.

        Args:
            None
        Returns:
            out (None): This function does not return anything.

        """
        self.audio_in_queue.get_nowait()

    @override
    async defoutput(self, *args: Any, **kwargs: Any) -> Any:
"""
        Process and output the audio.

        Args:
            *args: Can take any positional argument.
            **kwargs: Can take any keyword argument.

        Returns:
            out (Any): This function can return any output.

        """
        stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=RECEIVE_SAMPLE_RATE,
            output=True,
        )
        while True:
            bytestream = await self.audio_in_queue.get()
            await asyncio.to_thread(stream.write, bytestream)

    @override
    async defreceive(self, data: bytes) -> Any:
"""
        Receive audio data.

        Args:
            data (Any): received audio data (generally as bytes or str, but it is kept open also to other types).
            *args: Can take any positional argument.
            **kwargs: Can take any keyword argument.

        Returns:
            out (Any): This function can return any output.

        """
        self.audio_in_queue.put_nowait(data)

```
 |  
| --- | --- |  
###  start [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgentInterface.start "Permanent link")

```
start(session: AsyncSession) -> None

```

Start the interface.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `session`  |  `AsyncSession`  |  the session to which the API is bound.  |  _required_  |  
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/audio_interface.py`  
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
```
 | 
```
@override
defstart(self, session: AsyncSession) -> None:
"""
    Start the interface.

    Args:
        session (AsyncSession): the session to which the API is bound.

    """
    self.session = session
    self.audio_in_queue = asyncio.Queue()
    self.out_queue = asyncio.Queue(maxsize=5)

```
 |  
| --- | --- |  
###  stop [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgentInterface.stop "Permanent link")

```
stop() -> None

```

Stop the interface.
Returns: out (None): This function does not return anything.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/audio_interface.py`  
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
```
 | 
```
defstop(self) -> None:
"""
    Stop the interface.

    Args:
        None
    Returns:
        out (None): This function does not return anything.

    """
    if self.audio_stream:
        self.audio_stream.close()
    else:
        raise ValueError("Audio stream has never been opened, cannot be closed.")

```
 |  
| --- | --- |  
###  interrupt [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgentInterface.interrupt "Permanent link")

```
interrupt() -> None

```

Interrupt the interface.
Returns: out (None): This function does not return anything.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/audio_interface.py`  
| 
```
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
```
 | 
```
definterrupt(self) -> None:
"""
    Interrupt the interface.

    Args:
        None
    Returns:
        out (None): This function does not return anything.

    """
    self.audio_in_queue.get_nowait()

```
 |  
| --- | --- |  
###  output [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgentInterface.output "Permanent link")

```
output(*args: , **kwargs: ) -> 

```

Process and output the audio.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `*args`  |  Can take any positional argument.  |  
|  `**kwargs`  |  Can take any keyword argument.  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `out`  |  This function can return any output.  |  
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/audio_interface.py`  
| 
```
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
```
 | 
```
@override
async defoutput(self, *args: Any, **kwargs: Any) -> Any:
"""
    Process and output the audio.

    Args:
        *args: Can take any positional argument.
        **kwargs: Can take any keyword argument.

    Returns:
        out (Any): This function can return any output.

    """
    stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=RECEIVE_SAMPLE_RATE,
        output=True,
    )
    while True:
        bytestream = await self.audio_in_queue.get()
        await asyncio.to_thread(stream.write, bytestream)

```
 |  
| --- | --- |  
###  receive [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/gemini_live/#llama_index.voice_agents.gemini_live.GeminiLiveVoiceAgentInterface.receive "Permanent link")

```
receive(data: bytes) -> 

```

Receive audio data.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `data`  |  received audio data (generally as bytes or str, but it is kept open also to other types).  |  _required_  |  
|  `*args`  |  Can take any positional argument.  |  _required_  |  
|  `**kwargs`  |  Can take any keyword argument.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `out`  |  This function can return any output.  |  
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-gemini-live/llama_index/voice_agents/gemini_live/audio_interface.py`  
| 
```
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
```
 | 
```
@override
async defreceive(self, data: bytes) -> Any:
"""
    Receive audio data.

    Args:
        data (Any): received audio data (generally as bytes or str, but it is kept open also to other types).
        *args: Can take any positional argument.
        **kwargs: Can take any keyword argument.

    Returns:
        out (Any): This function can return any output.

    """
    self.audio_in_queue.put_nowait(data)

```
 |  
| --- | --- |  
options: members: - GeminiLiveVoiceAgent
