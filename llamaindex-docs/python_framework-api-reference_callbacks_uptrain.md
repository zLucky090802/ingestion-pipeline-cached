# Uptrain
##  UpTrainCallbackHandler [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/uptrain/#llama_index.callbacks.uptrain.UpTrainCallbackHandler "Permanent link")
Bases: 
UpTrain callback handler.
This class is responsible for handling the UpTrain API and logging events to UpTrain.
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-uptrain/llama_index/callbacks/uptrain/base.py`  
| 
```
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
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
```
 | 
```
classUpTrainCallbackHandler(BaseCallbackHandler):
"""
    UpTrain callback handler.

    This class is responsible for handling the UpTrain API and logging events to UpTrain.

    """

    def__init__(
        self,
        api_key: str,
        key_type: Literal["uptrain", "openai"],
        project_name: str = "uptrain_llamaindex",
    ) -> None:
"""Initialize the UpTrain callback handler."""
        try:
            fromuptrainimport APIClient, EvalLLM, Settings
        except ImportError:
            raise ImportError(
                "UpTrainCallbackHandler requires the 'uptrain' package. "
                "Please install it using 'pip install uptrain'."
            )
        nest_asyncio.apply()
        super().__init__(
            event_starts_to_ignore=[],
            event_ends_to_ignore=[],
        )
        self.schema = UpTrainDataSchema(project_name=project_name)
        self._event_pairs_by_id: Dict[str, List[CBEvent]] = defaultdict(list)
        self._trace_map: Dict[str, List[str]] = defaultdict(list)

        # Based on whether the user enters an UpTrain API key or an OpenAI API key, the client is initialized
        # If both are entered, the UpTrain API key is used
        if key_type == "uptrain":
            settings = Settings(uptrain_access_token=api_key)
            self.uptrain_client = APIClient(settings=settings)
        elif key_type == "openai":
            settings = Settings(openai_api_key=api_key)
            self.uptrain_client = EvalLLM(settings=settings)
        else:
            raise ValueError("Invalid key type: Must be 'uptrain' or 'openai'")

    defuptrain_evaluate(
        self,
        evaluation_name: str,
        data: List[Dict[str, str]],
        checks: List[str],
    ) -> None:
"""Run an evaluation on the UpTrain server using UpTrain client."""
        if self.uptrain_client.__class__.__name__ == "APIClient":
            uptrain_result = self.uptrain_client.log_and_evaluate(
                project_name=self.schema.project_name,
                evaluation_name=evaluation_name,
                data=data,
                checks=checks,
            )
        else:
            uptrain_result = self.uptrain_client.evaluate(
                project_name=self.schema.project_name,
                evaluation_name=evaluation_name,
                data=data,
                checks=checks,
            )
        self.schema.uptrain_results[self.schema.project_name].append(uptrain_result)

        score_name_map = {
            "score_context_relevance": "Context Relevance Score",
            "score_factual_accuracy": "Factual Accuracy Score",
            "score_response_completeness": "Response Completeness Score",
            "score_sub_query_completeness": "Sub Query Completeness Score",
            "score_context_reranking": "Context Reranking Score",
            "score_context_conciseness": "Context Conciseness Score",
        }

        # Print the results
        for row in uptrain_result:
            columns = list(row.keys())
            for column in columns:
                if column == "question":
                    print(f"\nQuestion: {row[column]}")
                elif column == "response":
                    print(f"Response: {row[column]}\n")
                elif column.startswith("score"):
                    if column in score_name_map:
                        print(f"{score_name_map[column]}: {row[column]}")
                    else:
                        print(f"{column}: {row[column]}")
            print()

    defon_event_start(
        self,
        event_type: CBEventType,
        payload: Any = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
"""Run when an event starts and return id of event."""
        event = CBEvent(event_type, payload=payload, id_=event_id)
        self._event_pairs_by_id[event.id_].append(event)

        if event_type is CBEventType.QUERY:
            self.schema.question = payload["query_str"]
        if event_type is CBEventType.TEMPLATING and "template_vars" in payload:
            template_vars = payload["template_vars"]
            self.schema.context = template_vars.get("context_str", "")
        elif event_type is CBEventType.RERANKING and "nodes" in payload:
            self.schema.eval_types.add("reranking")
            # Store old context data
            self.schema.old_context = [node.text for node in payload["nodes"]]
        elif event_type is CBEventType.SUB_QUESTION:
            # For the first sub question, store parent question and parent id
            if "sub_question" not in self.schema.eval_types:
                self.schema.parent_question = self.schema.question
                self.schema.eval_types.add("sub_question")
            # Store sub question data - question and parent id
            self.schema.sub_question_parent_id = parent_id
        return event_id

    defon_event_end(
        self,
        event_type: CBEventType,
        payload: Any = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
"""Run when an event ends."""
        try:
            fromuptrainimport Evals
        except ImportError:
            raise ImportError(
                "UpTrainCallbackHandler requires the 'uptrain' package. "
                "Please install it using 'pip install uptrain'."
            )
        event = CBEvent(event_type, payload=payload, id_=event_id)
        self._event_pairs_by_id[event.id_].append(event)
        self._trace_map = defaultdict(list)
        if event_id == self.schema.sub_question_parent_id:
            # Perform individual evaluations for sub questions (but send all sub questions at once)
            self.uptrain_evaluate(
                evaluation_name="sub_question_answering",
                data=list(self.schema.sub_question_map.values()),
                checks=[
                    Evals.CONTEXT_RELEVANCE,
                    Evals.FACTUAL_ACCURACY,
                    Evals.RESPONSE_COMPLETENESS,
                ],
            )
            # Perform evaluation for question and all sub questions (as a whole)
            sub_questions = [
                sub_question["question"]
                for sub_question in self.schema.sub_question_map.values()
            ]
            sub_questions_formatted = "\n".join(
                [
                    f"{index}. {string}"
                    for index, string in enumerate(sub_questions, start=1)
                ]
            )
            self.uptrain_evaluate(
                evaluation_name="sub_query_completeness",
                data=[
                    {
                        "question": self.schema.parent_question,
                        "sub_questions": sub_questions_formatted,
                    }
                ],
                checks=[Evals.SUB_QUERY_COMPLETENESS],
            )
            self.schema.eval_types.remove("sub_question")
        # Should not be called for sub questions
        if (
            event_type is CBEventType.SYNTHESIZE
            and "sub_question" not in self.schema.eval_types
        ):
            self.schema.response = payload["response"].response
            # Perform evaluation for synthesization
            if "reranking" in self.schema.eval_types:
                if self.schema.reranking_type == "rerank":
                    evaluation_name = "question_answering_rerank"
                else:
                    evaluation_name = "question_answering_resize"
                self.schema.eval_types.remove("reranking")
            else:
                evaluation_name = "question_answering"
            self.uptrain_evaluate(
                evaluation_name=evaluation_name,
                data=[
                    {
                        "question": self.schema.question,
                        "context": self.schema.context,
                        "response": self.schema.response,
                    }
                ],
                checks=[
                    Evals.CONTEXT_RELEVANCE,
                    Evals.FACTUAL_ACCURACY,
                    Evals.RESPONSE_COMPLETENESS,
                ],
            )

        elif event_type is CBEventType.RERANKING:
            # Store new context data
            self.schema.new_context = [node.text for node in payload["nodes"]]
            if len(self.schema.old_context) == len(self.schema.new_context):
                self.schema.reranking_type = "rerank"
                context = "\n".join(
                    [
                        f"{index}. {string}"
                        for index, string in enumerate(self.schema.old_context, start=1)
                    ]
                )
                reranked_context = "\n".join(
                    [
                        f"{index}. {string}"
                        for index, string in enumerate(self.schema.new_context, start=1)
                    ]
                )
                # Perform evaluation for reranking
                self.uptrain_evaluate(
                    evaluation_name="context_reranking",
                    data=[
                        {
                            "question": self.schema.question,
                            "context": context,
                            "reranked_context": reranked_context,
                        }
                    ],
                    checks=[
                        Evals.CONTEXT_RERANKING,
                    ],
                )
            else:
                self.schema.reranking_type = "resize"
                context = "\n".join(self.schema.old_context)
                concise_context = "\n".join(self.schema.new_context)
                # Perform evaluation for resizing
                self.uptrain_evaluate(
                    evaluation_name="context_conciseness",
                    data=[
                        {
                            "question": self.schema.question,
                            "context": context,
                            "concise_context": concise_context,
                        }
                    ],
                    checks=[
                        Evals.CONTEXT_CONCISENESS,
                    ],
                )
        elif event_type is CBEventType.SUB_QUESTION:
            # Store sub question data
            self.schema.sub_question_map[event_id]["question"] = payload[
                "sub_question"
            ].sub_q.sub_question
            self.schema.sub_question_map[event_id]["context"] = (
                payload["sub_question"].sources[0].node.text
            )
            self.schema.sub_question_map[event_id]["response"] = payload[
                "sub_question"
            ].answer

    defstart_trace(self, trace_id: Optional[str] = None) -> None:
        self._trace_map = defaultdict(list)
        return super().start_trace(trace_id)

    defend_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        self._trace_map = trace_map or defaultdict(list)
        return super().end_trace(trace_id, trace_map)

    defbuild_trace_map(
        self,
        cur_event_id: str,
        trace_map: Any,
    ) -> Dict[str, Any]:
        event_pair = self._event_pairs_by_id[cur_event_id]
        if event_pair:
            event_data = {
                "event_type": event_pair[0].event_type,
                "event_id": event_pair[0].id_,
                "children": {},
            }
            trace_map[cur_event_id] = event_data

        child_event_ids = self._trace_map[cur_event_id]
        for child_event_id in child_event_ids:
            self.build_trace_map(child_event_id, event_data["children"])
        return trace_map

```
 |  
| --- | --- |  
###  uptrain_evaluate [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/uptrain/#llama_index.callbacks.uptrain.UpTrainCallbackHandler.uptrain_evaluate "Permanent link")

```
uptrain_evaluate(
    evaluation_name: ,
    data: [[, ]],
    checks: [],
) -> None

```

Run an evaluation on the UpTrain server using UpTrain client.
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-uptrain/llama_index/callbacks/uptrain/base.py`  
| 
```
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
```
 | 
```
defuptrain_evaluate(
    self,
    evaluation_name: str,
    data: List[Dict[str, str]],
    checks: List[str],
) -> None:
"""Run an evaluation on the UpTrain server using UpTrain client."""
    if self.uptrain_client.__class__.__name__ == "APIClient":
        uptrain_result = self.uptrain_client.log_and_evaluate(
            project_name=self.schema.project_name,
            evaluation_name=evaluation_name,
            data=data,
            checks=checks,
        )
    else:
        uptrain_result = self.uptrain_client.evaluate(
            project_name=self.schema.project_name,
            evaluation_name=evaluation_name,
            data=data,
            checks=checks,
        )
    self.schema.uptrain_results[self.schema.project_name].append(uptrain_result)

    score_name_map = {
        "score_context_relevance": "Context Relevance Score",
        "score_factual_accuracy": "Factual Accuracy Score",
        "score_response_completeness": "Response Completeness Score",
        "score_sub_query_completeness": "Sub Query Completeness Score",
        "score_context_reranking": "Context Reranking Score",
        "score_context_conciseness": "Context Conciseness Score",
    }

    # Print the results
    for row in uptrain_result:
        columns = list(row.keys())
        for column in columns:
            if column == "question":
                print(f"\nQuestion: {row[column]}")
            elif column == "response":
                print(f"Response: {row[column]}\n")
            elif column.startswith("score"):
                if column in score_name_map:
                    print(f"{score_name_map[column]}: {row[column]}")
                else:
                    print(f"{column}: {row[column]}")
        print()

```
 |  
| --- | --- |  
###  on_event_start [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/uptrain/#llama_index.callbacks.uptrain.UpTrainCallbackHandler.on_event_start "Permanent link")

```
on_event_start(
    event_type: ,
    payload:  = None,
    event_id:  = "",
    parent_id:  = "",
    **kwargs: 
) -> 

```

Run when an event starts and return id of event.
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-uptrain/llama_index/callbacks/uptrain/base.py`  
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
```
 | 
```
defon_event_start(
    self,
    event_type: CBEventType,
    payload: Any = None,
    event_id: str = "",
    parent_id: str = "",
    **kwargs: Any,
) -> str:
"""Run when an event starts and return id of event."""
    event = CBEvent(event_type, payload=payload, id_=event_id)
    self._event_pairs_by_id[event.id_].append(event)

    if event_type is CBEventType.QUERY:
        self.schema.question = payload["query_str"]
    if event_type is CBEventType.TEMPLATING and "template_vars" in payload:
        template_vars = payload["template_vars"]
        self.schema.context = template_vars.get("context_str", "")
    elif event_type is CBEventType.RERANKING and "nodes" in payload:
        self.schema.eval_types.add("reranking")
        # Store old context data
        self.schema.old_context = [node.text for node in payload["nodes"]]
    elif event_type is CBEventType.SUB_QUESTION:
        # For the first sub question, store parent question and parent id
        if "sub_question" not in self.schema.eval_types:
            self.schema.parent_question = self.schema.question
            self.schema.eval_types.add("sub_question")
        # Store sub question data - question and parent id
        self.schema.sub_question_parent_id = parent_id
    return event_id

```
 |  
| --- | --- |  
###  on_event_end [#](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/uptrain/#llama_index.callbacks.uptrain.UpTrainCallbackHandler.on_event_end "Permanent link")

```
on_event_end(
    event_type: ,
    payload:  = None,
    event_id:  = "",
    **kwargs: 
) -> None

```

Run when an event ends.
Source code in `llama-index-integrations/callbacks/llama-index-callbacks-uptrain/llama_index/callbacks/uptrain/base.py`  
| 
```
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
298
299
300
301
302
303
304
```
 | 
```
defon_event_end(
    self,
    event_type: CBEventType,
    payload: Any = None,
    event_id: str = "",
    **kwargs: Any,
) -> None:
"""Run when an event ends."""
    try:
        fromuptrainimport Evals
    except ImportError:
        raise ImportError(
            "UpTrainCallbackHandler requires the 'uptrain' package. "
            "Please install it using 'pip install uptrain'."
        )
    event = CBEvent(event_type, payload=payload, id_=event_id)
    self._event_pairs_by_id[event.id_].append(event)
    self._trace_map = defaultdict(list)
    if event_id == self.schema.sub_question_parent_id:
        # Perform individual evaluations for sub questions (but send all sub questions at once)
        self.uptrain_evaluate(
            evaluation_name="sub_question_answering",
            data=list(self.schema.sub_question_map.values()),
            checks=[
                Evals.CONTEXT_RELEVANCE,
                Evals.FACTUAL_ACCURACY,
                Evals.RESPONSE_COMPLETENESS,
            ],
        )
        # Perform evaluation for question and all sub questions (as a whole)
        sub_questions = [
            sub_question["question"]
            for sub_question in self.schema.sub_question_map.values()
        ]
        sub_questions_formatted = "\n".join(
            [
                f"{index}. {string}"
                for index, string in enumerate(sub_questions, start=1)
            ]
        )
        self.uptrain_evaluate(
            evaluation_name="sub_query_completeness",
            data=[
                {
                    "question": self.schema.parent_question,
                    "sub_questions": sub_questions_formatted,
                }
            ],
            checks=[Evals.SUB_QUERY_COMPLETENESS],
        )
        self.schema.eval_types.remove("sub_question")
    # Should not be called for sub questions
    if (
        event_type is CBEventType.SYNTHESIZE
        and "sub_question" not in self.schema.eval_types
    ):
        self.schema.response = payload["response"].response
        # Perform evaluation for synthesization
        if "reranking" in self.schema.eval_types:
            if self.schema.reranking_type == "rerank":
                evaluation_name = "question_answering_rerank"
            else:
                evaluation_name = "question_answering_resize"
            self.schema.eval_types.remove("reranking")
        else:
            evaluation_name = "question_answering"
        self.uptrain_evaluate(
            evaluation_name=evaluation_name,
            data=[
                {
                    "question": self.schema.question,
                    "context": self.schema.context,
                    "response": self.schema.response,
                }
            ],
            checks=[
                Evals.CONTEXT_RELEVANCE,
                Evals.FACTUAL_ACCURACY,
                Evals.RESPONSE_COMPLETENESS,
            ],
        )

    elif event_type is CBEventType.RERANKING:
        # Store new context data
        self.schema.new_context = [node.text for node in payload["nodes"]]
        if len(self.schema.old_context) == len(self.schema.new_context):
            self.schema.reranking_type = "rerank"
            context = "\n".join(
                [
                    f"{index}. {string}"
                    for index, string in enumerate(self.schema.old_context, start=1)
                ]
            )
            reranked_context = "\n".join(
                [
                    f"{index}. {string}"
                    for index, string in enumerate(self.schema.new_context, start=1)
                ]
            )
            # Perform evaluation for reranking
            self.uptrain_evaluate(
                evaluation_name="context_reranking",
                data=[
                    {
                        "question": self.schema.question,
                        "context": context,
                        "reranked_context": reranked_context,
                    }
                ],
                checks=[
                    Evals.CONTEXT_RERANKING,
                ],
            )
        else:
            self.schema.reranking_type = "resize"
            context = "\n".join(self.schema.old_context)
            concise_context = "\n".join(self.schema.new_context)
            # Perform evaluation for resizing
            self.uptrain_evaluate(
                evaluation_name="context_conciseness",
                data=[
                    {
                        "question": self.schema.question,
                        "context": context,
                        "concise_context": concise_context,
                    }
                ],
                checks=[
                    Evals.CONTEXT_CONCISENESS,
                ],
            )
    elif event_type is CBEventType.SUB_QUESTION:
        # Store sub question data
        self.schema.sub_question_map[event_id]["question"] = payload[
            "sub_question"
        ].sub_q.sub_question
        self.schema.sub_question_map[event_id]["context"] = (
            payload["sub_question"].sources[0].node.text
        )
        self.schema.sub_question_map[event_id]["response"] = payload[
            "sub_question"
        ].answer

```
 |  
| --- | --- |  
options: members: - UpTrainCallbackHandler
