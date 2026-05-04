# Openinference
##  OpenInferenceCallbackHandler [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/openinference/#llama_index.callbacks.openinference.OpenInferenceCallbackHandler "Permanent link")
Bases: 
Callback handler for storing generation data in OpenInference format. OpenInference is an open standard for capturing and storing AI model inferences. It enables production LLMapp servers to seamlessly integrate with LLM observability solutions such as Arize and Phoenix.
For more information on the specification, see https://github.com/Arize-ai/open-inference-spec
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-openinference/llama_index/callbacks/openinference/base.py`  
| 
```
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
298
299
300
```
 | 
```
classOpenInferenceCallbackHandler(BaseCallbackHandler):
"""
    Callback handler for storing generation data in OpenInference format.
    OpenInference is an open standard for capturing and storing AI model
    inferences. It enables production LLMapp servers to seamlessly integrate
    with LLM observability solutions such as Arize and Phoenix.

    For more information on the specification, see
    https://github.com/Arize-ai/open-inference-spec
    """

    def__init__(
        self,
        callback: Optional[Callable[[List[QueryData], List[NodeData]], None]] = None,
    ) -> None:
"""
        Initializes the OpenInferenceCallbackHandler.

        Args:
            callback (Optional[Callable[[List[QueryData], List[NodeData]], None]], optional): A
            callback function that will be called when a query trace is
            completed, often used for logging or persisting query data.

        """
        super().__init__(event_starts_to_ignore=[], event_ends_to_ignore=[])
        self._callback = callback
        self._trace_data = TraceData()
        self._query_data_buffer: List[QueryData] = []
        self._node_data_buffer: List[NodeData] = []

    defstart_trace(self, trace_id: Optional[str] = None) -> None:
        if trace_id == "query" or trace_id == "chat":
            self._trace_data = TraceData()
            self._trace_data.query_data.timestamp = datetime.now().isoformat()
            self._trace_data.query_data.id = _generate_random_id()

    defend_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        if trace_id == "query" or trace_id == "chat":
            self._query_data_buffer.append(self._trace_data.query_data)
            self._node_data_buffer.extend(self._trace_data.node_datas)
            self._trace_data = TraceData()
            if self._callback is not None:
                self._callback(self._query_data_buffer, self._node_data_buffer)

    defon_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        if payload is not None:
            if event_type is CBEventType.QUERY:
                query_text = payload[EventPayload.QUERY_STR]
                self._trace_data.query_data.query_text = query_text
            elif event_type is CBEventType.LLM:
                if prompt := payload.get(EventPayload.PROMPT, None):
                    self._trace_data.query_data.llm_prompt = prompt
                if messages := payload.get(EventPayload.MESSAGES, None):
                    self._trace_data.query_data.llm_messages = [
                        (m.role.value, m.content) for m in messages
                    ]
                    # For chat engines there is no query event and thus the
                    # query text will be None, in this case we set the query
                    # text to the last message passed to the LLM
                    if self._trace_data.query_data.query_text is None:
                        self._trace_data.query_data.query_text = messages[-1].content
        return event_id

    defon_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        if payload is None:
            return
        if event_type is CBEventType.RETRIEVE:
            for node_with_score in payload[EventPayload.NODES]:
                node = node_with_score.node
                score = node_with_score.score
                self._trace_data.query_data.node_ids.append(node.hash)
                self._trace_data.query_data.scores.append(score)
                self._trace_data.node_datas.append(
                    NodeData(
                        id=node.hash,
                        node_text=node.text,
                    )
                )
        elif event_type is CBEventType.LLM:
            if self._trace_data.query_data.response_text is None:
                if response := payload.get(EventPayload.RESPONSE, None):
                    if isinstance(response, ChatResponse):
                        # If the response is of class ChatResponse the string
                        # representation has the format "<role>: <message>",
                        # but we want just the message
                        response_text = response.message.content
                    else:
                        response_text = str(response)
                    self._trace_data.query_data.response_text = response_text
                elif completion := payload.get(EventPayload.COMPLETION, None):
                    self._trace_data.query_data.response_text = str(completion)
        elif event_type is CBEventType.EMBEDDING:
            self._trace_data.query_data.query_embedding = payload[
                EventPayload.EMBEDDINGS
            ][0]

    defflush_query_data_buffer(self) -> List[QueryData]:
"""
        Clears the query data buffer and returns the data.

        Returns:
            List[QueryData]: The query data.

        """
        query_data_buffer = self._query_data_buffer
        self._query_data_buffer = []
        return query_data_buffer

    defflush_node_data_buffer(self) -> List[NodeData]:
"""
        Clears the node data buffer and returns the data.

        Returns:
            List[NodeData]: The node data.

        """
        node_data_buffer = self._node_data_buffer
        self._node_data_buffer = []
        return node_data_buffer

```
 |  
| --- | --- |  
###  flush_query_data_buffer [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/openinference/#llama_index.callbacks.openinference.OpenInferenceCallbackHandler.flush_query_data_buffer "Permanent link")

```
flush_query_data_buffer() -> [QueryData]

```

Clears the query data buffer and returns the data.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[QueryData]`  |  List[QueryData]: The query data.  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-openinference/llama_index/callbacks/openinference/base.py`  
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
```
 | 
```
defflush_query_data_buffer(self) -> List[QueryData]:
"""
    Clears the query data buffer and returns the data.

    Returns:
        List[QueryData]: The query data.

    """
    query_data_buffer = self._query_data_buffer
    self._query_data_buffer = []
    return query_data_buffer

```
 |  
| --- | --- |  
###  flush_node_data_buffer [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/openinference/#llama_index.callbacks.openinference.OpenInferenceCallbackHandler.flush_node_data_buffer "Permanent link")

```
flush_node_data_buffer() -> [NodeData]

```

Clears the node data buffer and returns the data.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[NodeData]`  |  List[NodeData]: The node data.  |  
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-openinference/llama_index/callbacks/openinference/base.py`  
| 
```
290
291
292
293
294
295
296
297
298
299
300
```
 | 
```
defflush_node_data_buffer(self) -> List[NodeData]:
"""
    Clears the node data buffer and returns the data.

    Returns:
        List[NodeData]: The node data.

    """
    node_data_buffer = self._node_data_buffer
    self._node_data_buffer = []
    return node_data_buffer

```
 |  
| --- | --- |  
options: members: - OpenInferenceCallbackHandler
