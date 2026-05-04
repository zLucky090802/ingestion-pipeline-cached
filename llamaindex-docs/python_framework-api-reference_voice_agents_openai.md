# Openai
##  OpenAIVoiceAgent [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgent "Permanent link")
Bases: `BaseVoiceAgent`
> **NOTE** : _This API is a BETA, and thus might be subject to changes_.
Interface for the OpenAI Realtime Conversation integration with LlamaIndex.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
|  `Optional[BaseVoiceAgentWebsocket]`  |  A pre-defined websocket to use. Defaults to None. In case of doubt, it is advised to leave this argument as None and pass ws_url and model.  |  
| `interface`  |  `Optional[BaseVoiceAgentInterface]`  |  Audio I/O interface. Defaults to None. In case of doubt, it is advised to leave this argument as None.  |  
| `api_key`  |  `Optional[str]`  |  The OpenAI API key. Defaults to the environmental variable OPENAI_API_KEY if the value is None.  |  
| `ws_url`  |  The URL for the OpenAI Realtime Conversation websocket. Defaults to: 'wss://api.openai.com/v1/realtime'.  |  
| `model`  |  The conversational model. Defaults to: 'gpt-4o-realtime-preview'.  |  
| `tools`  |   |  Tools to equip the agent with.  |  
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/base.py`  
| 
```
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
284
285
286
287
288
289
290
291
292
293
294
295
296
297
```
 | 
```
classOpenAIVoiceAgent(BaseVoiceAgent):
"""
    >**NOTE**: *This API is a BETA, and thus might be subject to changes*.

    Interface for the OpenAI Realtime Conversation integration with LlamaIndex.

    Attributes:
        ws (Optional[BaseVoiceAgentWebsocket]): A pre-defined websocket to use. Defaults to None. In case of doubt, it is advised to leave this argument as None and pass ws_url and model.
        interface (Optional[BaseVoiceAgentInterface]): Audio I/O interface. Defaults to None. In case of doubt, it is advised to leave this argument as None.
        api_key (Optional[str]): The OpenAI API key. Defaults to the environmental variable OPENAI_API_KEY if the value is None.
        ws_url (str): The URL for the OpenAI Realtime Conversation websocket. Defaults to: 'wss://api.openai.com/v1/realtime'.
        model (str): The conversational model. Defaults to: 'gpt-4o-realtime-preview'.
        tools (List[BaseTool]): Tools to equip the agent with.

    """

    def__init__(
        self,
        ws: Optional[BaseVoiceAgentWebsocket] = None,
        interface: Optional[BaseVoiceAgentInterface] = None,
        api_key: Optional[str] = None,
        ws_url: Optional[str] = None,
        model: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
    ) -> None:
        super().__init__(
            ws=ws, interface=interface, ws_url=ws_url, api_key=api_key, tools=tools
        )
        if not self.ws:
            if not model:
                model = DEFAULT_MODEL
            if not self.ws_url:
                self.ws_url = DEFAULT_WS_URL
            url = self.ws_url + "?model=" + model
            openai_api_key = os.getenv("OPENAI_API_KEY", None) or self.api_key
            if not openai_api_key:
                raise ValueError(
                    "The OPENAI_API_KEY is neither passed from the function arguments nor from environmental variables"
                )
            self.ws: OpenAIVoiceAgentWebsocket = OpenAIVoiceAgentWebsocket(
                uri=url, api_key=openai_api_key, on_msg=self.handle_message
            )
        if not self.interface:
            self.interface: OpenAIVoiceAgentInterface = OpenAIVoiceAgentInterface(
                on_audio_callback=self.send
            )
        self.recv_thread: Optional[threading.Thread] = None

    async defstart(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
"""
        Start the conversation and all related processes.

        Args:
            **kwargs (Any): You can pass all the keyword arguments related to initializing a session, except for `tools`, which is inferred from the `tools` attribute of the class. Find a reference for these arguments and their type [on OpenAI official documentation](https://platform.openai.com/docs/api-reference/realtime-client-events/session/update).

        """
        self.ws.connect()

        session = ConversationSession.model_validate(kwargs)
        logger.info(f"Session: {session}")

        if self.tools is not None:
            openai_conv_tools: List[ConversationTool] = []

            for tool in self.tools:
                params_dict = tool.metadata.get_parameters_dict()
                tool_params = ToolParameters.model_validate(params_dict)
                conv_tool = ConversationTool(
                    name=tool.metadata.get_name(),
                    description=tool.metadata.description,
                    parameters=tool_params,
                )
                openai_conv_tools.append(conv_tool)

            session.tools = openai_conv_tools

        update_session_event = ConversationSessionUpdate(
            type_t="session.update",
            session=session,
        )
        self._events.append(update_session_event)
        self._messages.append(ChatMessage(role="system", content=session.instructions))
        # Send initial request to start the conversation
        await self.ws.send(update_session_event.model_dump(by_alias=True))

        # Start processing microphone audio
        self.audio_thread = threading.Thread(target=self.interface.output)
        self.audio_thread.start()

        # Start audio streams (mic and speaker)
        self.interface.start()
        print("The agent is ready to have a conversation")

    async defsend(self, audio: bytes, *args: Any, **kwargs: Any) -> None:
"""
        Callback function to send audio data to the OpenAI Conversation Websocket.

        Args:
            mic_chunk (bytes): the incoming audio stream from the user's input device.

        """
        encoded_chunk = base64.b64encode(audio).decode("utf-8")
        audio_event = ConversationInputEvent(
            type_t="input_audio_buffer.append", audio=encoded_chunk
        )
        self._events.append(audio_event)
        self._messages.append(
            ChatMessage(role=MessageRole.USER, blocks=[AudioBlock(audio=audio)])
        )
        await self.ws.send(audio_event.model_dump(by_alias=True))

    async defhandle_message(self, message: dict, *args: Any, **kwargs: Any) -> None:
"""
        Handle incoming message from OpenAI Conversation Websocket.

        Args:
            message (dict): The message from the websocket.

        """
        message["type_t"] = message.pop("type")
        func_res_ev: Optional[SendFunctionItemEvent] = None
        if message["type_t"] == "response.audio.delta":
            event: BaseVoiceAgentEvent = ConversationDeltaEvent.model_validate(message)
            audio_content = base64.b64decode(message["delta"])
            self._messages.append(
                ChatMessage(
                    role=MessageRole.ASSISTANT, blocks=[AudioBlock(audio=audio_content)]
                )
            )
            self.interface.receive(audio_content)

        elif message["type_t"] == "response.text.delta":
            event = ConversationDeltaEvent.model_validate(message)
            self._messages.append(
                ChatMessage(
                    role=MessageRole.ASSISTANT, blocks=[TextBlock(text=event.delta)]
                )
            )

        elif message["type_t"] == "response.audio_transcript.delta":
            event = ConversationDeltaEvent.model_validate(message)
            self._messages.append(
                ChatMessage(
                    role=MessageRole.ASSISTANT, blocks=[TextBlock(text=event.delta)]
                )
            )

        elif message["type_t"] == "response.text.done":
            event = ConversationDoneEvent.model_validate(message)

        elif message["type_t"] == "response.audio_transcript.done":
            event = ConversationDoneEvent.model_validate(message)

        elif message["type_t"] == "response.audio.done":
            event = ConversationDoneEvent.model_validate(message)

        elif message["type_t"] == "response.function_call_arguments.done":
            event = FunctionCallDoneEvent.model_validate(message)
            if not event.name:
                if self.tools and len(self.tools) == 1:
                    tool_output = self.tools[0](**event.arguments)
                    output = tool_output.raw_output
                    func_res_it = FunctionResultItem(
                        type_t="function_call_output",
                        call_id=event.call_id,
                        output=str(output),
                    )
                    func_res_ev = SendFunctionItemEvent(
                        type_t="conversation.item.create", item=func_res_it
                    )
                    await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
                elif self.tools and len(self.tools)  1:
                    if "tool_name" not in event.arguments:
                        func_res_it = FunctionResultItem(
                            type_t="function_call_output",
                            call_id=event.call_id,
                            output="There are multiple tools and there is not tool name specified. Please pass 'tool_name' as an argument.",
                        )
                        func_res_ev = SendFunctionItemEvent(
                            type_t="conversation.item.create", item=func_res_it
                        )
                        await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
                    else:
                        tool = get_tool_by_name(
                            self.tools, name=event.arguments["tool_name"]
                        )
                        tool_output = tool(**event.arguments)
                        output = tool_output.raw_output
                        func_res_it = FunctionResultItem(
                            type_t="function_call_output",
                            call_id=event.call_id,
                            output=str(output),
                        )
                        func_res_ev = SendFunctionItemEvent(
                            type_t="conversation.item.create", item=func_res_it
                        )
                        await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
                else:
                    func_res_it = FunctionResultItem(
                        type_t="function_call_output",
                        call_id=event.call_id,
                        output="Seems like there are no tools available at this time.",
                    )
                    func_res_ev = SendFunctionItemEvent(
                        type_t="conversation.item.create", item=func_res_it
                    )
                    await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
            else:
                if self.tools:
                    tool = get_tool_by_name(self.tools, name=event.name)
                    tool_output = tool(**event.arguments)
                    output = tool_output.raw_output
                    func_res_it = FunctionResultItem(
                        type_t="function_call_output",
                        call_id=event.call_id,
                        output=str(output),
                    )
                    func_res_ev = SendFunctionItemEvent(
                        type_t="conversation.item.create", item=func_res_it
                    )
                    await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
                else:
                    func_res_it = FunctionResultItem(
                        type_t="function_call_output",
                        call_id=event.call_id,
                        output="Seems like there are no tools available at this time.",
                    )
                    func_res_ev = SendFunctionItemEvent(
                        type_t="conversation.item.create", item=func_res_it
                    )
                    await self.ws.send(data=func_res_ev.model_dump(by_alias=True))

        else:
            return
        self._events.append(event)
        if func_res_ev:
            self._events.append(func_res_ev)

    async defstop(self) -> None:
"""
        Stop the conversation and close all the related processes.
        """
        # Signal threads to stop
        self.interface._stop_event.set()
        await self.ws.close()

        # Stop audio streams
        self.interface.stop()

        # Join threads to ensure they exit cleanly
        if self.audio_thread:
            self.audio_thread.join()

    async definterrupt(self) -> None:
"""
        Interrupts the input/output audio streaming.
        """
        self.interface.interrupt()

```
 |  
| --- | --- |  
###  start [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgent.start "Permanent link")

```
start(*args: , **kwargs: [, ]) -> None

```

Start the conversation and all related processes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `**kwargs`  |  You can pass all the keyword arguments related to initializing a session, except for `tools`, which is inferred from the `tools` attribute of the class. Find a reference for these arguments and their type [on OpenAI official documentation](https://platform.openai.com/docs/api-reference/realtime-client-events/session/update).  |  
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/base.py`  
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
```
 | 
```
async defstart(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
"""
    Start the conversation and all related processes.

    Args:
        **kwargs (Any): You can pass all the keyword arguments related to initializing a session, except for `tools`, which is inferred from the `tools` attribute of the class. Find a reference for these arguments and their type [on OpenAI official documentation](https://platform.openai.com/docs/api-reference/realtime-client-events/session/update).

    """
    self.ws.connect()

    session = ConversationSession.model_validate(kwargs)
    logger.info(f"Session: {session}")

    if self.tools is not None:
        openai_conv_tools: List[ConversationTool] = []

        for tool in self.tools:
            params_dict = tool.metadata.get_parameters_dict()
            tool_params = ToolParameters.model_validate(params_dict)
            conv_tool = ConversationTool(
                name=tool.metadata.get_name(),
                description=tool.metadata.description,
                parameters=tool_params,
            )
            openai_conv_tools.append(conv_tool)

        session.tools = openai_conv_tools

    update_session_event = ConversationSessionUpdate(
        type_t="session.update",
        session=session,
    )
    self._events.append(update_session_event)
    self._messages.append(ChatMessage(role="system", content=session.instructions))
    # Send initial request to start the conversation
    await self.ws.send(update_session_event.model_dump(by_alias=True))

    # Start processing microphone audio
    self.audio_thread = threading.Thread(target=self.interface.output)
    self.audio_thread.start()

    # Start audio streams (mic and speaker)
    self.interface.start()
    print("The agent is ready to have a conversation")

```
 |  
| --- | --- |  
###  send [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgent.send "Permanent link")

```
send(audio: bytes, *args: , **kwargs: ) -> None

```

Callback function to send audio data to the OpenAI Conversation Websocket.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `mic_chunk`  |  `bytes`  |  the incoming audio stream from the user's input device.  |  _required_  |  
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/base.py`  
| 
```
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
async defsend(self, audio: bytes, *args: Any, **kwargs: Any) -> None:
"""
    Callback function to send audio data to the OpenAI Conversation Websocket.

    Args:
        mic_chunk (bytes): the incoming audio stream from the user's input device.

    """
    encoded_chunk = base64.b64encode(audio).decode("utf-8")
    audio_event = ConversationInputEvent(
        type_t="input_audio_buffer.append", audio=encoded_chunk
    )
    self._events.append(audio_event)
    self._messages.append(
        ChatMessage(role=MessageRole.USER, blocks=[AudioBlock(audio=audio)])
    )
    await self.ws.send(audio_event.model_dump(by_alias=True))

```
 |  
| --- | --- |  
###  handle_message [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgent.handle_message "Permanent link")

```
handle_message(
    message: , *args: , **kwargs: 
) -> None

```

Handle incoming message from OpenAI Conversation Websocket.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `message`  |  `dict`  |  The message from the websocket.  |  _required_  |  
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/base.py`  
| 
```
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
```
 | 
```
async defhandle_message(self, message: dict, *args: Any, **kwargs: Any) -> None:
"""
    Handle incoming message from OpenAI Conversation Websocket.

    Args:
        message (dict): The message from the websocket.

    """
    message["type_t"] = message.pop("type")
    func_res_ev: Optional[SendFunctionItemEvent] = None
    if message["type_t"] == "response.audio.delta":
        event: BaseVoiceAgentEvent = ConversationDeltaEvent.model_validate(message)
        audio_content = base64.b64decode(message["delta"])
        self._messages.append(
            ChatMessage(
                role=MessageRole.ASSISTANT, blocks=[AudioBlock(audio=audio_content)]
            )
        )
        self.interface.receive(audio_content)

    elif message["type_t"] == "response.text.delta":
        event = ConversationDeltaEvent.model_validate(message)
        self._messages.append(
            ChatMessage(
                role=MessageRole.ASSISTANT, blocks=[TextBlock(text=event.delta)]
            )
        )

    elif message["type_t"] == "response.audio_transcript.delta":
        event = ConversationDeltaEvent.model_validate(message)
        self._messages.append(
            ChatMessage(
                role=MessageRole.ASSISTANT, blocks=[TextBlock(text=event.delta)]
            )
        )

    elif message["type_t"] == "response.text.done":
        event = ConversationDoneEvent.model_validate(message)

    elif message["type_t"] == "response.audio_transcript.done":
        event = ConversationDoneEvent.model_validate(message)

    elif message["type_t"] == "response.audio.done":
        event = ConversationDoneEvent.model_validate(message)

    elif message["type_t"] == "response.function_call_arguments.done":
        event = FunctionCallDoneEvent.model_validate(message)
        if not event.name:
            if self.tools and len(self.tools) == 1:
                tool_output = self.tools[0](**event.arguments)
                output = tool_output.raw_output
                func_res_it = FunctionResultItem(
                    type_t="function_call_output",
                    call_id=event.call_id,
                    output=str(output),
                )
                func_res_ev = SendFunctionItemEvent(
                    type_t="conversation.item.create", item=func_res_it
                )
                await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
            elif self.tools and len(self.tools)  1:
                if "tool_name" not in event.arguments:
                    func_res_it = FunctionResultItem(
                        type_t="function_call_output",
                        call_id=event.call_id,
                        output="There are multiple tools and there is not tool name specified. Please pass 'tool_name' as an argument.",
                    )
                    func_res_ev = SendFunctionItemEvent(
                        type_t="conversation.item.create", item=func_res_it
                    )
                    await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
                else:
                    tool = get_tool_by_name(
                        self.tools, name=event.arguments["tool_name"]
                    )
                    tool_output = tool(**event.arguments)
                    output = tool_output.raw_output
                    func_res_it = FunctionResultItem(
                        type_t="function_call_output",
                        call_id=event.call_id,
                        output=str(output),
                    )
                    func_res_ev = SendFunctionItemEvent(
                        type_t="conversation.item.create", item=func_res_it
                    )
                    await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
            else:
                func_res_it = FunctionResultItem(
                    type_t="function_call_output",
                    call_id=event.call_id,
                    output="Seems like there are no tools available at this time.",
                )
                func_res_ev = SendFunctionItemEvent(
                    type_t="conversation.item.create", item=func_res_it
                )
                await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
        else:
            if self.tools:
                tool = get_tool_by_name(self.tools, name=event.name)
                tool_output = tool(**event.arguments)
                output = tool_output.raw_output
                func_res_it = FunctionResultItem(
                    type_t="function_call_output",
                    call_id=event.call_id,
                    output=str(output),
                )
                func_res_ev = SendFunctionItemEvent(
                    type_t="conversation.item.create", item=func_res_it
                )
                await self.ws.send(data=func_res_ev.model_dump(by_alias=True))
            else:
                func_res_it = FunctionResultItem(
                    type_t="function_call_output",
                    call_id=event.call_id,
                    output="Seems like there are no tools available at this time.",
                )
                func_res_ev = SendFunctionItemEvent(
                    type_t="conversation.item.create", item=func_res_it
                )
                await self.ws.send(data=func_res_ev.model_dump(by_alias=True))

    else:
        return
    self._events.append(event)
    if func_res_ev:
        self._events.append(func_res_ev)

```
 |  
| --- | --- |  
###  stop [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgent.stop "Permanent link")

```
stop() -> None

```

Stop the conversation and close all the related processes.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/base.py`  
| 
```
278
279
280
281
282
283
284
285
286
287
288
289
290
291
```
 | 
```
async defstop(self) -> None:
"""
    Stop the conversation and close all the related processes.
    """
    # Signal threads to stop
    self.interface._stop_event.set()
    await self.ws.close()

    # Stop audio streams
    self.interface.stop()

    # Join threads to ensure they exit cleanly
    if self.audio_thread:
        self.audio_thread.join()

```
 |  
| --- | --- |  
###  interrupt [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgent.interrupt "Permanent link")

```
interrupt() -> None

```

Interrupts the input/output audio streaming.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/base.py`  
| 
```
293
294
295
296
297
```
 | 
```
async definterrupt(self) -> None:
"""
    Interrupts the input/output audio streaming.
    """
    self.interface.interrupt()

```
 |  
| --- | --- |  
##  OpenAIVoiceAgentWebsocket [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentWebsocket "Permanent link")
Bases: `BaseVoiceAgentWebsocket`
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/websocket.py`  
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
```
 | 
```
classOpenAIVoiceAgentWebsocket(BaseVoiceAgentWebsocket):
    def__init__(
        self, uri: str, api_key: str, on_msg: Optional[Callable] = None
    ) -> None:
        super().__init__(uri=uri)
        self.api_key = api_key
        self.on_msg = on_msg
        self.send_queue: asyncio.Queue = asyncio.Queue()
        self._stop_event = threading.Event()
        self.loop_thread: Optional[threading.Thread] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None

    defconnect(self) -> None:
"""Start the socket loop in a new thread."""
        self.loop_thread = threading.Thread(target=self._run_socket_loop, daemon=True)
        self.loop_thread.start()

    async defaconnect(self) -> None:
"""Method not implemented."""
        raise NotImplementedError(
            f"This method has not been implemented for {self.__qualname__}"
        )

    def_run_socket_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._socket_loop())

    async def_socket_loop(self) -> None:
"""Establish connection and run send/recv loop."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "realtime=v1",
        }

        try:
            async with websockets.connect(self.uri, additional_headers=headers) as ws:
                self.ws = ws  # Safe: now created inside this thread + loop

                # Create separate tasks for sending and receiving
                recv_task = asyncio.create_task(self._recv_loop(ws))
                send_task = asyncio.create_task(self._send_loop(ws))

                try:
                    # Run both tasks concurrently until one completes or fails
                    await asyncio.gather(recv_task, send_task)
                except Exception as e:
                    logging.error(f"Error in socket tasks: {e}")
                finally:
                    # Clean up any remaining tasks
                    recv_task.cancel()
                    send_task.cancel()
                    await asyncio.gather(recv_task, send_task, return_exceptions=True)

        except Exception as e:
            logging.error(f"Failed to connect to WebSocket: {e}")

    async def_recv_loop(self, ws) -> None:
"""Handle incoming messages."""
        try:
            while not self._stop_event.is_set():
                try:
                    message = await ws.recv()
                    logging.info(f"Received message: {message}")
                    if message and self.on_msg:
                        await self.on_msg(json.loads(message))
                except ConnectionClosedError:
                    logging.error("WebSocket connection closed.")
                    break
        except Exception as e:
            logging.error(f"Error in receive loop: {e}")

    async def_send_loop(self, ws) -> None:
"""Handle outgoing messages."""
        try:
            while not self._stop_event.is_set():
                try:
                    # Wait for a message to send with a timeout to check stop_event
                    try:
                        message = await asyncio.wait_for(
                            self.send_queue.get(), timeout=0.1
                        )
                        await ws.send(json.dumps(message))
                    except asyncio.TimeoutError:
                        # Timeout is expected - just continue to check stop_event
                        continue
                except ConnectionClosedError:
                    logging.error("WebSocket connection closed.")
                    break
        except Exception as e:
            logging.error(f"Error in send loop: {e}")

    async defsend(self, data: Any) -> None:
"""Enqueue a message for sending."""
        if self.loop:
            self.loop.call_soon_threadsafe(self.send_queue.put_nowait, data)

    async defclose(self) -> None:
"""Stop the loop and close the WebSocket."""
        self._stop_event.set()
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.loop_thread:
            self.loop_thread.join()
            logging.info("WebSocket loop thread terminated.")

```
 |  
| --- | --- |  
###  connect [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentWebsocket.connect "Permanent link")

```
connect() -> None

```

Start the socket loop in a new thread.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/websocket.py`  
| 
```
29
30
31
32
```
 | 
```
defconnect(self) -> None:
"""Start the socket loop in a new thread."""
    self.loop_thread = threading.Thread(target=self._run_socket_loop, daemon=True)
    self.loop_thread.start()

```
 |  
| --- | --- |  
###  aconnect [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentWebsocket.aconnect "Permanent link")

```
aconnect() -> None

```

Method not implemented.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/websocket.py`  
| 
```
34
35
36
37
38
```
 | 
```
async defaconnect(self) -> None:
"""Method not implemented."""
    raise NotImplementedError(
        f"This method has not been implemented for {self.__qualname__}"
    )

```
 |  
| --- | --- |  
###  send [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentWebsocket.send "Permanent link")

```
send(data: ) -> None

```

Enqueue a message for sending.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/websocket.py`  
| 
```
109
110
111
112
```
 | 
```
async defsend(self, data: Any) -> None:
"""Enqueue a message for sending."""
    if self.loop:
        self.loop.call_soon_threadsafe(self.send_queue.put_nowait, data)

```
 |  
| --- | --- |  
###  close [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentWebsocket.close "Permanent link")

```
close() -> None

```

Stop the loop and close the WebSocket.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/websocket.py`  
| 
```
114
115
116
117
118
119
120
121
```
 | 
```
async defclose(self) -> None:
"""Stop the loop and close the WebSocket."""
    self._stop_event.set()
    if self.loop:
        self.loop.call_soon_threadsafe(self.loop.stop)
    if self.loop_thread:
        self.loop_thread.join()
        logging.info("WebSocket loop thread terminated.")

```
 |  
| --- | --- |  
##  OpenAIVoiceAgentInterface [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentInterface "Permanent link")
Bases: `BaseVoiceAgentInterface`
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/audio_interface.py`  
| 
```
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
```
 | 
```
classOpenAIVoiceAgentInterface(BaseVoiceAgentInterface):
    def__init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        rate: int = RATE,
        format: int = FORMAT,
        on_audio_callback: Optional[Callable] = None,
    ):
        self.chunk_size = chunk_size
        self.rate = rate
        self.format = format
        self.audio_buffer = bytearray()
        self.mic_queue: queue.Queue = queue.Queue()
        self.mic_on_at: Union[int, float] = 0
        self.mic_active: Optional[bool] = None
        self._stop_event = threading.Event()
        self.p = pyaudio.PyAudio()
        self.on_audio_callback = on_audio_callback  # Callback for audio data

    def_microphone_callback(
        self, in_data: Any, frame_count: int, time_info: Any, status: Any
    ) -> Tuple[None, Any]:
"""Microphone callback that queues audio chunks."""
        if time.time()  self.mic_on_at:
            if not self.mic_active:
                self.mic_active = True

            self.mic_queue.put(in_data)
        else:
            if self.mic_active:
                self.mic_active = False

        return (None, pyaudio.paContinue)

    def_speaker_callback(
        self, in_data: Any, frame_count: int, time_info: Any, status: Any
    ) -> Tuple[bytes, Any]:
"""Speaker callback that plays audio."""
        bytes_needed = frame_count * 2
        current_buffer_size = len(self.audio_buffer)

        if current_buffer_size >= bytes_needed:
            audio_chunk = bytes(self.audio_buffer[:bytes_needed])
            self.audio_buffer = self.audio_buffer[bytes_needed:]
            self.mic_on_at = time.time() + REENGAGE_DELAY_MS / 1000
        else:
            audio_chunk = bytes(self.audio_buffer) + b"\x00" * (
                bytes_needed - current_buffer_size
            )
            self.audio_buffer.clear()

        return (audio_chunk, pyaudio.paContinue)

    defstart(self) -> None:
"""Start microphone and speaker streams."""
        self.mic_stream = self.p.open(
            format=self.format,
            channels=1,
            rate=self.rate,
            input=True,
            stream_callback=self._microphone_callback,
            frames_per_buffer=self.chunk_size,
        )
        self.spkr_stream = self.p.open(
            format=self.format,
            channels=1,
            rate=self.rate,
            output=True,
            stream_callback=self._speaker_callback,
            frames_per_buffer=self.chunk_size,
        )
        self.mic_stream.start_stream()
        self.spkr_stream.start_stream()

    defstop(self) -> None:
"""Stop and close audio streams."""
        self.mic_stream.stop_stream()
        self.mic_stream.close()

        self.spkr_stream.stop_stream()
        self.spkr_stream.close()

        self.p.terminate()

    definterrupt(self) -> None:
"""Interrupts active input/output audio streaming."""
        if self.spkr_stream.is_active():
            self.spkr_stream.stop_stream()

        if self.mic_active:
            self.mic_stream.stop_stream()

    defoutput(self) -> None:
"""Process microphone audio and call back when new audio is ready."""
        while not self._stop_event.is_set():
            if not self.mic_queue.empty():
                mic_chunk = self.mic_queue.get()
                if self.on_audio_callback:
                    asyncio.run(self.on_audio_callback(mic_chunk))
            else:
                time.sleep(0.05)

    defreceive(self, data: bytes, *args, **kwargs) -> None:
"""Appends audio data to the buffer for playback."""
        self.audio_buffer.extend(data)

```
 |  
| --- | --- |  
###  start [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentInterface.start "Permanent link")

```
start() -> None

```

Start microphone and speaker streams.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/audio_interface.py`  
| 
```
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
```
 | 
```
defstart(self) -> None:
"""Start microphone and speaker streams."""
    self.mic_stream = self.p.open(
        format=self.format,
        channels=1,
        rate=self.rate,
        input=True,
        stream_callback=self._microphone_callback,
        frames_per_buffer=self.chunk_size,
    )
    self.spkr_stream = self.p.open(
        format=self.format,
        channels=1,
        rate=self.rate,
        output=True,
        stream_callback=self._speaker_callback,
        frames_per_buffer=self.chunk_size,
    )
    self.mic_stream.start_stream()
    self.spkr_stream.start_stream()

```
 |  
| --- | --- |  
###  stop [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentInterface.stop "Permanent link")

```
stop() -> None

```

Stop and close audio streams.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/audio_interface.py`  
| 
```
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
defstop(self) -> None:
"""Stop and close audio streams."""
    self.mic_stream.stop_stream()
    self.mic_stream.close()

    self.spkr_stream.stop_stream()
    self.spkr_stream.close()

    self.p.terminate()

```
 |  
| --- | --- |  
###  interrupt [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentInterface.interrupt "Permanent link")

```
interrupt() -> None

```

Interrupts active input/output audio streaming.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/audio_interface.py`  
| 
```
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
definterrupt(self) -> None:
"""Interrupts active input/output audio streaming."""
    if self.spkr_stream.is_active():
        self.spkr_stream.stop_stream()

    if self.mic_active:
        self.mic_stream.stop_stream()

```
 |  
| --- | --- |  
###  output [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentInterface.output "Permanent link")

```
output() -> None

```

Process microphone audio and call back when new audio is ready.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/audio_interface.py`  
| 
```
113
114
115
116
117
118
119
120
121
```
 | 
```
defoutput(self) -> None:
"""Process microphone audio and call back when new audio is ready."""
    while not self._stop_event.is_set():
        if not self.mic_queue.empty():
            mic_chunk = self.mic_queue.get()
            if self.on_audio_callback:
                asyncio.run(self.on_audio_callback(mic_chunk))
        else:
            time.sleep(0.05)

```
 |  
| --- | --- |  
###  receive [#](https://developers.llamaindex.ai/python/framework-api-reference/voice_agents/openai/#llama_index.voice_agents.openai.OpenAIVoiceAgentInterface.receive "Permanent link")

```
receive(data: bytes, *args, **kwargs) -> None

```

Appends audio data to the buffer for playback.
Source code in `llama-index-integrations/voice_agents/llama-index-voice-agents-openai/llama_index/voice_agents/openai/audio_interface.py`  
| 
```
123
124
125
```
 | 
```
defreceive(self, data: bytes, *args, **kwargs) -> None:
"""Appends audio data to the buffer for playback."""
    self.audio_buffer.extend(data)

```
 |  
| --- | --- |  
options: members: - OpenAIConversation
