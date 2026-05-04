# Ibm
##  WatsonxRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/ibm/#llama_index.postprocessor.ibm.WatsonxRerank "Permanent link")
Bases: 
IBM watsonx.ai Rerank.
Example
`pip install llama-index-postprocessor-ibm`

```
fromllama_index.postprocessor.ibmimport WatsonxRerank
watsonx_llm = WatsonxRerank(
    model_id="<RERANK MODEL>",
    url="https://us-south.ml.cloud.ibm.com",
    apikey="*****",
    project_id="*****",
)

```

Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-ibm/llama_index/postprocessor/ibm/base.py`  
| 
```
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
```
 | 
```
classWatsonxRerank(BaseNodePostprocessor):
"""
    IBM watsonx.ai Rerank.

    Example:
        `pip install llama-index-postprocessor-ibm`

        ```python

        from llama_index.postprocessor.ibm import WatsonxRerank
        watsonx_llm = WatsonxRerank(
            model_id="<RERANK MODEL>",
            url="https://us-south.ml.cloud.ibm.com",
            apikey="*****",
            project_id="*****",

        ```

    """

    model_id: str = Field(description="Type of model to use.")

    top_n: Optional[int] = Field(
        default=None,
        description="Number of top results to return.",
    )

    truncate_input_tokens: Optional[int] = Field(
        default=None,
        description="""Represents the maximum number of input tokens accepted.""",
    )

    project_id: Optional[str] = Field(
        default=None,
        description="ID of the Watson Studio project.",
        frozen=True,
    )

    space_id: Optional[str] = Field(
        default=None, description="ID of the Watson Studio space.", frozen=True
    )

    url: Optional[SecretStr] = Field(
        default=None,
        description="Url to the IBM watsonx.ai for IBM Cloud or the IBM watsonx.ai software instance.",
        frozen=True,
    )

    apikey: Optional[SecretStr] = Field(
        default=None,
        description="API key to the IBM watsonx.ai for IBM Cloud or the IBM watsonx.ai software instance.",
        frozen=True,
    )

    token: Optional[SecretStr] = Field(
        default=None,
        description="Token to the IBM watsonx.ai software instance.",
        frozen=True,
    )

    password: Optional[SecretStr] = Field(
        default=None,
        description="Password to the IBM watsonx.ai software instance.",
        frozen=True,
    )

    username: Optional[SecretStr] = Field(
        default=None,
        description="Username to the IBM watsonx.ai software instance.",
        frozen=True,
    )

    instance_id: Optional[SecretStr] = Field(
        default=None,
        description="Instance_id of CPD instance",
        frozen=True,
        deprecated="The `instance_id` parameter is deprecated and will no longer be utilized for logging to the IBM watsonx.ai software instance.",
    )

    version: Optional[SecretStr] = Field(
        default=None,
        description="Version of the IBM watsonx.ai software instance.",
        frozen=True,
    )

    verify: Union[str, bool, None] = Field(
        default=None,
        description="""
        User can pass as verify one of following:
        the path to a CA_BUNDLE file
        the path of directory with certificates of trusted CAs
        True - default path to truststore will be taken
        False - no verification will be made
        """,
        frozen=True,
    )

    _client: Optional[APIClient] = PrivateAttr()
    _watsonx_rerank: Rerank = PrivateAttr()

    def__init__(
        self,
        model_id: Optional[str] = None,
        top_n: Optional[int] = None,
        truncate_input_tokens: Optional[int] = None,
        project_id: Optional[str] = None,
        space_id: Optional[str] = None,
        url: Optional[str] = None,
        apikey: Optional[str] = None,
        token: Optional[str] = None,
        password: Optional[str] = None,
        username: Optional[str] = None,
        version: Optional[str] = None,
        verify: Union[str, bool, None] = None,
        api_client: Optional[APIClient] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
"""
        Initialize watsonx.ai Rerank.
        """
        callback_manager = callback_manager or CallbackManager([])

        creds = (
            resolve_watsonx_credentials(
                url=url,
                apikey=apikey,
                token=token,
                username=username,
                password=password,
            )
            if not isinstance(api_client, APIClient)
            else {}
        )

        super().__init__(
            model_id=model_id,
            top_n=top_n,
            truncate_input_tokens=truncate_input_tokens,
            project_id=project_id,
            space_id=space_id,
            url=creds.get("url"),
            apikey=creds.get("apikey"),
            token=creds.get("token"),
            password=creds.get("password"),
            username=creds.get("username"),
            version=version,
            verify=verify,
            _client=api_client,
            callback_manager=callback_manager,
            **kwargs,
        )

        self._client = api_client
        self._watsonx_rerank = Rerank(
            model_id=model_id,
            params=self.params,
            credentials=(
                Credentials.from_dict(
                    {
                        key: value.get_secret_value() if value else None
                        for key, value in self._get_credential_kwargs().items()
                    },
                    _verify=self.verify,
                )
                if creds
                else None
            ),
            project_id=self.project_id,
            space_id=self.space_id,
            verify=verify,
            api_client=api_client,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get Class Name."""
        return "WatsonxRerank"

    def_get_credential_kwargs(self) -> Dict[str, SecretStr | None]:
        return {
            "url": self.url,
            "apikey": self.apikey,
            "token": self.token,
            "password": self.password,
            "username": self.username,
            "version": self.version,
        }

    @property
    defparams(self) -> RerankParameters:
        rerank_return_options: RerankReturnOptions = RerankReturnOptions(
            top_n=self.top_n,
            inputs=False,
            query=False,
        )
        return RerankParameters(
            truncate_input_tokens=self.truncate_input_tokens,
            return_options=rerank_return_options,
        )

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        dispatcher.event(
            ReRankStartEvent(
                query=query_bundle,
                nodes=nodes,
                top_n=self.top_n,
                model_name=self.model_id,
            )
        )

        if query_bundle is None:
            raise ValueError("Query bundle must be provided.")
        if len(nodes) == 0:
            return []

        texts = [
            node.node.get_content(metadata_mode=MetadataMode.EMBED) for node in nodes
        ]
        results = self._watsonx_rerank.generate(
            query=query_bundle.query_str,
            inputs=texts,
            params=self.params,
        )

        new_nodes = []
        for result in results.get("results", []):
            new_node_with_score = NodeWithScore(
                node=nodes[result["index"]].node,
                score=result["score"],
            )
            new_nodes.append(new_node_with_score)

        dispatcher.event(ReRankEndEvent(nodes=new_nodes))
        return new_nodes

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/ibm/#llama_index.postprocessor.ibm.WatsonxRerank.class_name "Permanent link")

```
class_name() -> 

```

Get Class Name.
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-ibm/llama_index/postprocessor/ibm/base.py`  
| 
```
209
210
211
212
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get Class Name."""
    return "WatsonxRerank"

```
 |  
| --- | --- |  
options: members: - WatsonxRerank
