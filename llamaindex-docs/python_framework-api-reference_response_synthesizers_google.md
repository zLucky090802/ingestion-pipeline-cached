# Google
##  GoogleTextSynthesizer [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/google/#llama_index.response_synthesizers.google.GoogleTextSynthesizer "Permanent link")
Bases: 
Google's Attributed Question and Answering service.
Given a user's query and a list of passages, Google's server will return a response that is grounded to the provided list of passages. It will not base the response on parametric memory.
Source code in `llama-index-integrations/response_synthesizers/llama-index-response-synthesizers-google/llama_index/response_synthesizers/google/base.py`  
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
```
 | 
```
classGoogleTextSynthesizer(BaseSynthesizer):
"""
    Google's Attributed Question and Answering service.

    Given a user's query and a list of passages, Google's server will return
    a response that is grounded to the provided list of passages. It will not
    base the response on parametric memory.
    """

    _client: Any
    _temperature: float
    _answer_style: Any
    _safety_setting: List[Any]

    def__init__(
        self,
        *,
        temperature: float,
        answer_style: Any,
        safety_setting: List[Any],
        **kwargs: Any,
    ):
"""
        Create a new Google AQA.

        Prefer to use the factory `from_defaults` instead for type safety.
        See `from_defaults` for more documentation.
        """
        try:
            importllama_index.vector_stores.google.genai_extensionasgenaix
        except ImportError:
            raise ImportError(_import_err_msg)

        super().__init__(
            llm=MockLLM(),
            output_cls=SynthesizedResponse,
            **kwargs,
        )

        self._client = genaix.build_generative_service()
        self._temperature = temperature
        self._answer_style = answer_style
        self._safety_setting = safety_setting

    # Type safe factory that is only available if Google is installed.
    @classmethod
    deffrom_defaults(
        cls,
        temperature: float = 0.7,
        answer_style: int = 1,
        safety_setting: List["genai.SafetySetting"] = [],
    ) -> "GoogleTextSynthesizer":
"""
        Create a new Google AQA.

        Example:
          responder = GoogleTextSynthesizer.create(
              temperature=0.7,
              answer_style=AnswerStyle.ABSTRACTIVE,
              safety_setting=[
                  SafetySetting(
                      category=HARM_CATEGORY_SEXUALLY_EXPLICIT,
                      threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,




        Args:
          temperature: 0.0 to 1.0.
          answer_style: See `google.ai.generativelanguage.GenerateAnswerRequest.AnswerStyle`
            The default is ABSTRACTIVE (1).
          safety_setting: See `google.ai.generativelanguage.SafetySetting`.

        Returns:
          an instance of GoogleTextSynthesizer.

        """
        return cls(
            temperature=temperature,
            answer_style=answer_style,
            safety_setting=safety_setting,
        )

    defget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> SynthesizedResponse:
"""
        Generate a grounded response on provided passages.

        Args:
            query_str: The user's question.
            text_chunks: A list of passages that should be used to answer the
                question.

        Returns:
            A `SynthesizedResponse` object.

        """
        try:
            importllama_index.vector_stores.google.genai_extensionasgenaix

            importgoogle.ai.generativelanguageasgenai
        except ImportError:
            raise ImportError(_import_err_msg)

        client = cast(genai.GenerativeServiceClient, self._client)
        response = genaix.generate_answer(
            prompt=query_str,
            passages=list(text_chunks),
            answer_style=self._answer_style,
            safety_settings=self._safety_setting,
            temperature=self._temperature,
            client=client,
        )

        return SynthesizedResponse(
            answer=response.answer,
            attributed_passages=[
                passage.text for passage in response.attributed_passages
            ],
            answerable_probability=response.answerable_probability,
        )

    async defaget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
        # TODO: Implement a true async version.
        return self.get_response(query_str, text_chunks, **response_kwargs)

    defsynthesize(
        self,
        query: QueryTextType,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        **response_kwargs: Any,
    ) -> Response:
"""
        Returns a grounded response based on provided passages.

        Returns:
            Response's `source_nodes` will begin with a list of attributed
            passages. These passages are the ones that were used to construct
            the grounded response. These passages will always have no score,
            the only way to mark them as attributed passages. Then, the list
            will follow with the originally provided passages, which will have
            a score from the retrieval.

            Response's `metadata` may also have have an entry with key
            `answerable_probability`, which is the model's estimate of the
            probability that its answer is correct and grounded in the input
            passages.

        """
        if len(nodes) == 0:
            return Response("Empty Response")

        if isinstance(query, str):
            query = QueryBundle(query_str=query)

        with self._callback_manager.event(
            CBEventType.SYNTHESIZE, payload={EventPayload.QUERY_STR: query.query_str}
        ) as event:
            internal_response = self.get_response(
                query_str=query.query_str,
                text_chunks=[
                    n.node.get_content(metadata_mode=MetadataMode.LLM) for n in nodes
                ],
                **response_kwargs,
            )

            additional_source_nodes = list(additional_source_nodes or [])

            external_response = self._prepare_external_response(
                internal_response, nodes + additional_source_nodes
            )

            event.on_end(payload={EventPayload.RESPONSE: external_response})

        return external_response

    async defasynthesize(
        self,
        query: QueryTextType,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
        **response_kwargs: Any,
    ) -> Response:
        # TODO: Implement a true async version.
        return self.synthesize(query, nodes, additional_source_nodes, **response_kwargs)

    def_prepare_external_response(
        self,
        response: SynthesizedResponse,
        source_nodes: List[NodeWithScore],
    ) -> Response:
        return Response(
            response=response.answer,
            source_nodes=[
                NodeWithScore(node=TextNode(text=passage))
                for passage in response.attributed_passages
            ]
            + source_nodes,
            metadata={
                "answerable_probability": response.answerable_probability,
            },
        )

    def_get_prompts(self) -> PromptDictType:
        # Not used.
        return {}

    def_update_prompts(self, prompts_dict: PromptDictType) -> None:
        # Not used.
        ...

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/google/#llama_index.response_synthesizers.google.GoogleTextSynthesizer.from_defaults "Permanent link")

```
from_defaults(
    temperature: float = 0.7,
    answer_style:  = 1,
    safety_setting: [SafetySetting] = [],
) -> 

```

Create a new Google AQA.
Example
responder = GoogleTextSynthesizer.create( temperature=0.7, answer_style=AnswerStyle.ABSTRACTIVE, safety_setting=[ SafetySetting( category=HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, ), ] )
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `temperature`  |  `float`  |  0.0 to 1.0.  |  `0.7`  |  
|  `answer_style`  |  See `google.ai.generativelanguage.GenerateAnswerRequest.AnswerStyle` The default is ABSTRACTIVE (1).  |  
|  `safety_setting`  |  `List[SafetySetting]`  |  See `google.ai.generativelanguage.SafetySetting`.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  an instance of GoogleTextSynthesizer.  |  
Source code in `llama-index-integrations/response_synthesizers/llama-index-response-synthesizers-google/llama_index/response_synthesizers/google/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    temperature: float = 0.7,
    answer_style: int = 1,
    safety_setting: List["genai.SafetySetting"] = [],
) -> "GoogleTextSynthesizer":
"""
    Create a new Google AQA.

    Example:
      responder = GoogleTextSynthesizer.create(
          temperature=0.7,
          answer_style=AnswerStyle.ABSTRACTIVE,
          safety_setting=[
              SafetySetting(
                  category=HARM_CATEGORY_SEXUALLY_EXPLICIT,
                  threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,




    Args:
      temperature: 0.0 to 1.0.
      answer_style: See `google.ai.generativelanguage.GenerateAnswerRequest.AnswerStyle`
        The default is ABSTRACTIVE (1).
      safety_setting: See `google.ai.generativelanguage.SafetySetting`.

    Returns:
      an instance of GoogleTextSynthesizer.

    """
    return cls(
        temperature=temperature,
        answer_style=answer_style,
        safety_setting=safety_setting,
    )

```
 |  
| --- | --- |  
###  get_response [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/google/#llama_index.response_synthesizers.google.GoogleTextSynthesizer.get_response "Permanent link")

```
get_response(
    query_str: ,
    text_chunks: Sequence[],
    **response_kwargs: 
) -> 

```

Generate a grounded response on provided passages.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query_str`  |  The user's question.  |  _required_  |  
|  `text_chunks`  |  `Sequence[str]`  |  A list of passages that should be used to answer the question.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  A `SynthesizedResponse` object.  |  
Source code in `llama-index-integrations/response_synthesizers/llama-index-response-synthesizers-google/llama_index/response_synthesizers/google/base.py`  
| 
```
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
defget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    **response_kwargs: Any,
) -> SynthesizedResponse:
"""
    Generate a grounded response on provided passages.

    Args:
        query_str: The user's question.
        text_chunks: A list of passages that should be used to answer the
            question.

    Returns:
        A `SynthesizedResponse` object.

    """
    try:
        importllama_index.vector_stores.google.genai_extensionasgenaix

        importgoogle.ai.generativelanguageasgenai
    except ImportError:
        raise ImportError(_import_err_msg)

    client = cast(genai.GenerativeServiceClient, self._client)
    response = genaix.generate_answer(
        prompt=query_str,
        passages=list(text_chunks),
        answer_style=self._answer_style,
        safety_settings=self._safety_setting,
        temperature=self._temperature,
        client=client,
    )

    return SynthesizedResponse(
        answer=response.answer,
        attributed_passages=[
            passage.text for passage in response.attributed_passages
        ],
        answerable_probability=response.answerable_probability,
    )

```
 |  
| --- | --- |  
###  synthesize [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/google/#llama_index.response_synthesizers.google.GoogleTextSynthesizer.synthesize "Permanent link")

```
synthesize(
    query: QueryTextType,
    nodes: [],
    additional_source_nodes: Optional[
        Sequence[]
    ] = None,
    **response_kwargs: 
) -> 

```

Returns a grounded response based on provided passages.
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  Response's `source_nodes` will begin with a list of attributed  |  
|   |  passages. These passages are the ones that were used to construct  |  
|   |  the grounded response. These passages will always have no score,  |  
|   |  the only way to mark them as attributed passages. Then, the list  |  
|   |  will follow with the originally provided passages, which will have  |  
|   |  a score from the retrieval.  |  
|   |  Response's `metadata` may also have have an entry with key  |  
|   |  `answerable_probability`, which is the model's estimate of the  |  
|   |  probability that its answer is correct and grounded in the input  |  
|   |  passages.  |  
Source code in `llama-index-integrations/response_synthesizers/llama-index-response-synthesizers-google/llama_index/response_synthesizers/google/base.py`  
| 
```
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
```
 | 
```
defsynthesize(
    self,
    query: QueryTextType,
    nodes: List[NodeWithScore],
    additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    **response_kwargs: Any,
) -> Response:
"""
    Returns a grounded response based on provided passages.

    Returns:
        Response's `source_nodes` will begin with a list of attributed
        passages. These passages are the ones that were used to construct
        the grounded response. These passages will always have no score,
        the only way to mark them as attributed passages. Then, the list
        will follow with the originally provided passages, which will have
        a score from the retrieval.

        Response's `metadata` may also have have an entry with key
        `answerable_probability`, which is the model's estimate of the
        probability that its answer is correct and grounded in the input
        passages.

    """
    if len(nodes) == 0:
        return Response("Empty Response")

    if isinstance(query, str):
        query = QueryBundle(query_str=query)

    with self._callback_manager.event(
        CBEventType.SYNTHESIZE, payload={EventPayload.QUERY_STR: query.query_str}
    ) as event:
        internal_response = self.get_response(
            query_str=query.query_str,
            text_chunks=[
                n.node.get_content(metadata_mode=MetadataMode.LLM) for n in nodes
            ],
            **response_kwargs,
        )

        additional_source_nodes = list(additional_source_nodes or [])

        external_response = self._prepare_external_response(
            internal_response, nodes + additional_source_nodes
        )

        event.on_end(payload={EventPayload.RESPONSE: external_response})

    return external_response

```
 |  
| --- | --- |  
##  SynthesizedResponse [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/google/#llama_index.response_synthesizers.google.SynthesizedResponse "Permanent link")
Bases: `BaseModel`
Response of `GoogleTextSynthesizer.get_response`.
Source code in `llama-index-integrations/response_synthesizers/llama-index-response-synthesizers-google/llama_index/response_synthesizers/google/base.py`  
| 
```
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
```
 | 
```
classSynthesizedResponse(BaseModel):
"""Response of `GoogleTextSynthesizer.get_response`."""

    answer: str
"""The grounded response to the user's question."""

    attributed_passages: List[str]
"""The list of passages the AQA model used for its response."""

    answerable_probability: float
"""The model's estimate of the probability that its answer is correct and grounded in the input passages."""

```
 |  
| --- | --- |  
###  answer `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/google/#llama_index.response_synthesizers.google.SynthesizedResponse.answer "Permanent link")

```
answer: 

```

The grounded response to the user's question.
###  attributed_passages `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/google/#llama_index.response_synthesizers.google.SynthesizedResponse.attributed_passages "Permanent link")

```
attributed_passages: []

```

The list of passages the AQA model used for its response.
###  answerable_probability `instance-attribute` [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/google/#llama_index.response_synthesizers.google.SynthesizedResponse.answerable_probability "Permanent link")

```
answerable_probability: float

```

The model's estimate of the probability that its answer is correct and grounded in the input passages.
##  set_google_config [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/google/#llama_index.response_synthesizers.google.set_google_config "Permanent link")

```
set_google_config(
    *,
    api_endpoint: Optional[] = None,
    user_agent: Optional[] = None,
    page_size: Optional[] = None,
    auth_credentials: Optional[Credentials] = None,
    **kwargs: 
) -> None

```

Set the configuration for Google Generative AI API.
Parameters are optional, Normally, the defaults should work fine. If provided, they will override the default values in the Config class. See the docstring in `genai_extension.py` for more details. auth_credentials: Optional["credentials.Credentials"] = None, Use this to pass Google Auth credentials such as using a service account. Refer to for auth credentials documentation: https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount.
Example
from google.oauth2 import service_account credentials = service_account.Credentials.from_service_account_file( "/path/to/service.json", scopes=[ "https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/generative-language.retriever", ], ) set_google_config(auth_credentials=credentials)
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-google/llama_index/vector_stores/google/base.py`  
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
```
 | 
```
defset_google_config(
    *,
    api_endpoint: Optional[str] = None,
    user_agent: Optional[str] = None,
    page_size: Optional[int] = None,
    auth_credentials: Optional["credentials.Credentials"] = None,
    **kwargs: Any,
) -> None:
"""
    Set the configuration for Google Generative AI API.

    Parameters are optional, Normally, the defaults should work fine.
    If provided, they will override the default values in the Config class.
    See the docstring in `genai_extension.py` for more details.
    auth_credentials: Optional["credentials.Credentials"] = None,
    Use this to pass Google Auth credentials such as using a service account.
    Refer to for auth credentials documentation:
    https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount.

    Example:
        from google.oauth2 import service_account
        credentials = service_account.Credentials.from_service_account_file(
            "/path/to/service.json",
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/generative-language.retriever",


        set_google_config(auth_credentials=credentials)

    """
    try:
        importllama_index.vector_stores.google.genai_extensionasgenaix
    except ImportError:
        raise ImportError(_import_err_msg)

    config_attrs = {
        "api_endpoint": api_endpoint,
        "user_agent": user_agent,
        "page_size": page_size,
        "auth_credentials": auth_credentials,
        "testing": kwargs.get("testing"),
    }
    attrs = {k: v for k, v in config_attrs.items() if v is not None}
    config = genaix.Config(**attrs)
    genaix.set_config(config)

```
 |  
| --- | --- |  
options: members: - GoogleTextSynthesizer
