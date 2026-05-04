# Google rerank
##  GoogleRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/google_rerank/#llama_index.postprocessor.google_rerank.GoogleRerank "Permanent link")
Bases: 
Google Rerank postprocessor.
Uses Google's Discovery Engine Ranking API to rerank nodes based on query relevance.
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-google-rerank/llama_index/postprocessor/google_rerank/base.py`  
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
```
 | 
```
classGoogleRerank(BaseNodePostprocessor):
"""
    Google Rerank postprocessor.

    Uses Google's Discovery Engine Ranking API to rerank nodes
    based on query relevance.
    """

    model: str = Field(
        default=DEFAULT_MODEL,
        description="The ranking model to use.",
    )
    top_n: int = Field(default=2, description="Top N nodes to return.")
    project_id: Optional[str] = Field(
        default=None,
        description=(
            "Google Cloud project ID. Falls back to GOOGLE_CLOUD_PROJECT "
            "env var, then Application Default Credentials."
        ),
    )
    location: str = Field(
        default=DEFAULT_LOCATION,
        description="Google Cloud location for the ranking config.",
    )
    ranking_config: str = Field(
        default=DEFAULT_RANKING_CONFIG,
        description="Name of the ranking config resource.",
    )

    _client: Any = PrivateAttr()
    _async_client: Any = PrivateAttr()

    def__init__(
        self,
        model: str = DEFAULT_MODEL,
        top_n: int = 2,
        project_id: Optional[str] = None,
        location: str = DEFAULT_LOCATION,
        ranking_config: str = DEFAULT_RANKING_CONFIG,
        credentials: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model=model,
            top_n=top_n,
            project_id=project_id,
            location=location,
            ranking_config=ranking_config,
            **kwargs,
        )

        # Resolve project_id
        if self.project_id is None:
            self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if self.project_id is None:
            _, resolved_project = google.auth.default()
            self.project_id = resolved_project

        self._client = discoveryengine.RankServiceClient(credentials=credentials)
        self._async_client = discoveryengine.RankServiceAsyncClient(
            credentials=credentials
        )

    @classmethod
    defclass_name(cls) -> str:
        return "GoogleRerank"

    def_build_ranking_config_path(self) -> str:
        return (
            f"projects/{self.project_id}/locations/{self.location}"
            f"/rankingConfigs/{self.ranking_config}"
        )

    def_build_records(self, nodes: List[NodeWithScore]) -> list:
        records = []
        for i, node in enumerate(nodes):
            content = node.node.get_content(metadata_mode=MetadataMode.EMBED)
            records.append(
                discoveryengine.RankingRecord(
                    id=str(i),
                    content=content,
                )
            )
        return records

    @dispatcher.span
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
                model_name=self.model,
            )
        )

        if query_bundle is None:
            raise ValueError("Missing query bundle in extra info.")
        if len(nodes) == 0:
            return []

        records = self._build_records(nodes)
        top_n = min(self.top_n, len(nodes))

        request = discoveryengine.RankRequest(
            ranking_config=self._build_ranking_config_path(),
            model=self.model,
            top_n=top_n,
            query=query_bundle.query_str,
            records=records,
        )

        response = self._client.rank(request=request)

        new_nodes = []
        for record in response.records:
            index = int(record.id)
            new_nodes.append(
                NodeWithScore(
                    node=nodes[index].node,
                    score=record.score,
                )
            )

        dispatcher.event(ReRankEndEvent(nodes=new_nodes))
        return new_nodes

    @dispatcher.span
    async def_apostprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        dispatcher.event(
            ReRankStartEvent(
                query=query_bundle,
                nodes=nodes,
                top_n=self.top_n,
                model_name=self.model,
            )
        )

        if query_bundle is None:
            raise ValueError("Missing query bundle in extra info.")
        if len(nodes) == 0:
            return []

        records = self._build_records(nodes)
        top_n = min(self.top_n, len(nodes))

        request = discoveryengine.RankRequest(
            ranking_config=self._build_ranking_config_path(),
            model=self.model,
            top_n=top_n,
            query=query_bundle.query_str,
            records=records,
        )

        response = await self._async_client.rank(request=request)

        new_nodes = []
        for record in response.records:
            index = int(record.id)
            new_nodes.append(
                NodeWithScore(
                    node=nodes[index].node,
                    score=record.score,
                )
            )

        dispatcher.event(ReRankEndEvent(nodes=new_nodes))
        return new_nodes

```
 |  
| --- | --- |  
options: members: - GoogleRerank
