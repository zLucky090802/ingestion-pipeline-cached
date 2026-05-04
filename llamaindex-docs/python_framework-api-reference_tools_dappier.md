# Dappier
##  DappierAIRecommendationsToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierAIRecommendationsToolSpec "Permanent link")
Bases: 
Dappier AI Recommendations tool spec.
Provides AI-powered recommendations across various domains such as Sports News, Lifestyle News, iHeartDogs, iHeartCats, GreenMonster, WISH-TV and 9 and 10 News.
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/ai_recommendations/base.py`  
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
```
 | 
```
classDappierAIRecommendationsToolSpec(BaseToolSpec):
"""
    Dappier AI Recommendations tool spec.

    Provides AI-powered recommendations across various domains such as Sports News,
    Lifestyle News, iHeartDogs, iHeartCats, GreenMonster, WISH-TV and 9 and 10 News.
    """

    spec_functions = [
        "get_sports_news_recommendations",
        "get_lifestyle_news_recommendations",
        "get_iheartdogs_recommendations",
        "get_iheartcats_recommendations",
        "get_greenmonster_recommendations",
        "get_wishtv_recommendations",
        "get_nine_and_ten_news_recommendations",
    ]

    def__init__(self, api_key: Optional[str] = None) -> None:
"""
        Initialize the Dappier AI Recommendations tool spec.

        To obtain an API key, visit: https://platform.dappier.com/profile/api-keys
        """
        fromdappierimport Dappier

        self.api_key = api_key or os.environ.get("DAPPIER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it as a parameter or set DAPPIER_API_KEY in environment variables.\n"
                "To obtain an API key, visit: https://platform.dappier.com/profile/api-keys"
            )

        self.client = Dappier(api_key=self.api_key)

    defget_sports_news_recommendations(
        self,
        query: str,
        similarity_top_k: int = 10,
        ref: Optional[str] = None,
        num_articles_ref: int = 0,
        search_algorithm: Literal[
            "most_recent", "semantic", "most_recent_semantic", "trending"
        ] = "most_recent",
    ) -> str:
"""
        Retrieves sports news.

        Args:
            query (str): Query to fetch sports news.
            similarity_top_k (int): Number of documents to return.
            ref (Optional[str]): Site domain where recommendations should be displayed.
            num_articles_ref (int): Minimum number of articles to return from the reference domain.
            search_algorithm (str): The search algorithm to use.

        Returns:
            str: A response message for the user specified query.

        """
        data_model_id = "dm_01j0pb465keqmatq9k83dthx34"  # Sports News
        response = self.client.get_ai_recommendations(
            query=query,
            data_model_id=data_model_id,
            similarity_top_k=similarity_top_k,
            ref=ref,
            num_articles_ref=num_articles_ref,
            search_algorithm=search_algorithm,
        )
        return format_results(response)

    defget_lifestyle_news_recommendations(
        self,
        query: str,
        similarity_top_k: int = 10,
        ref: Optional[str] = None,
        num_articles_ref: int = 0,
        search_algorithm: Literal[
            "most_recent", "semantic", "most_recent_semantic", "trending"
        ] = "most_recent",
    ) -> str:
"""
        Retrieves lifestyle news.

        Args:
            query (str): Query to fetch lifestyle news.
            similarity_top_k (int): Number of documents to return.
            ref (Optional[str]): Site domain where recommendations should be displayed.
            num_articles_ref (int): Minimum number of articles to return from the reference domain.
            search_algorithm (str): The search algorithm to use.

        Returns:
            str: A response message for the user specified query.

        """
        data_model_id = "dm_01j0q82s4bfjmsqkhs3ywm3x6y"  # Lifestyle News
        response = self.client.get_ai_recommendations(
            query=query,
            data_model_id=data_model_id,
            similarity_top_k=similarity_top_k,
            ref=ref,
            num_articles_ref=num_articles_ref,
            search_algorithm=search_algorithm,
        )
        return format_results(response)

    defget_iheartdogs_recommendations(
        self,
        query: str,
        similarity_top_k: int = 10,
        ref: Optional[str] = None,
        num_articles_ref: int = 0,
        search_algorithm: Literal[
            "most_recent", "semantic", "most_recent_semantic", "trending"
        ] = "most_recent",
    ) -> str:
"""
        Retrieves iHeartDogs articles - a dog care expert.

        Args:
            query (str): Query to fetch dog care articles.
            similarity_top_k (int): Number of documents to return.
            ref (Optional[str]): Site domain where recommendations should be displayed.
            num_articles_ref (int): Minimum number of articles to return from the reference domain.
            search_algorithm (str): The search algorithm to use.

        Returns:
            str: A response message for the user specified query.

        """
        data_model_id = "dm_01j1sz8t3qe6v9g8ad102kvmqn"  # iHeartDogs AI
        response = self.client.get_ai_recommendations(
            query=query,
            data_model_id=data_model_id,
            similarity_top_k=similarity_top_k,
            ref=ref,
            num_articles_ref=num_articles_ref,
            search_algorithm=search_algorithm,
        )
        return format_results(response)

    defget_iheartcats_recommendations(
        self,
        query: str,
        similarity_top_k: int = 10,
        ref: Optional[str] = None,
        num_articles_ref: int = 0,
        search_algorithm: Literal[
            "most_recent", "semantic", "most_recent_semantic", "trending"
        ] = "most_recent",
    ) -> str:
"""
        Retrieves iHeartCats articles - a cat care expert.

        Args:
            query (str): Query to fetch cat care articles.
            similarity_top_k (int): Number of documents to return.
            ref (Optional[str]): Site domain where recommendations should be displayed.
            num_articles_ref (int): Minimum number of articles to return from the reference domain.
            search_algorithm (str): The search algorithm to use.

        Returns:
            str: A response message for the user specified query.

        """
        data_model_id = "dm_01j1sza0h7ekhaecys2p3y0vmj"  # iHeartCats AI
        response = self.client.get_ai_recommendations(
            query=query,
            data_model_id=data_model_id,
            similarity_top_k=similarity_top_k,
            ref=ref,
            num_articles_ref=num_articles_ref,
            search_algorithm=search_algorithm,
        )
        return format_results(response)

    defget_greenmonster_recommendations(
        self,
        query: str,
        similarity_top_k: int = 10,
        ref: Optional[str] = None,
        num_articles_ref: int = 0,
        search_algorithm: Literal[
            "most_recent", "semantic", "most_recent_semantic", "trending"
        ] = "most_recent",
    ) -> str:
"""
        Retrieves GreenMonster articles - Compassionate Living Guide.

        Args:
            query (str): Query to fetch compassionate living guides.
            similarity_top_k (int): Number of documents to return.
            ref (Optional[str]): Site domain where recommendations should be displayed.
            num_articles_ref (int): Minimum number of articles to return from the reference domain.
            search_algorithm (str): The search algorithm to use.

        Returns:
            str: A response message for the user specified query.

        """
        data_model_id = "dm_01j5xy9w5sf49bm6b1prm80m27"  # GreenMonster
        response = self.client.get_ai_recommendations(
            query=query,
            data_model_id=data_model_id,
            similarity_top_k=similarity_top_k,
            ref=ref,
            num_articles_ref=num_articles_ref,
            search_algorithm=search_algorithm,
        )
        return format_results(response)

    defget_wishtv_recommendations(
        self,
        query: str,
        similarity_top_k: int = 10,
        ref: Optional[str] = None,
        num_articles_ref: int = 0,
        search_algorithm: Literal[
            "most_recent", "semantic", "most_recent_semantic", "trending"
        ] = "most_recent",
    ) -> str:
"""
        Retrieves news articles.

        Args:
            query (str): Query to fetch news articles.
            similarity_top_k (int): The number of top documents to retrieve based on similarity. Defaults to 10.
            ref (Optional[str]): The site domain where recommendations should be displayed. Defaults to None.
            num_articles_ref (int): Minimum number of articles to return from the reference domain. Defaults to 0.
            search_algorithm (str): The search algorithm to use. Defaults to "most_recent".

        Returns:
            str: A response message for the user specified query.

        """
        data_model_id = "dm_01jagy9nqaeer9hxx8z1sk1jx6"  # WISH-TV AI
        response = self.client.get_ai_recommendations(
            query=query,
            data_model_id=data_model_id,
            similarity_top_k=similarity_top_k,
            ref=ref,
            num_articles_ref=num_articles_ref,
            search_algorithm=search_algorithm,
        )
        return format_results(response)

    defget_nine_and_ten_news_recommendations(
        self,
        query: str,
        similarity_top_k: int = 10,
        ref: Optional[str] = None,
        num_articles_ref: int = 0,
        search_algorithm: Literal[
            "most_recent", "semantic", "most_recent_semantic", "trending"
        ] = "most_recent",
    ) -> str:
"""
        Retrieves up-to-date local news for Northern Michigan, Cadillac and
        Traverse City.

        Args:
            query (str): Query to fetch local news.
            similarity_top_k (int): Number of documents to return.
            ref (Optional[str]): Site domain where recommendations should be displayed.
            num_articles_ref (int): Minimum number of articles to return from the reference domain.
            search_algorithm (str): The search algorithm to use.

        Returns:
            str: A response message for the user specified query.

        """
        data_model_id = "dm_01jhtt138wf1b9j8jwswye99y5"  # 9 and 10 News
        response = self.client.get_ai_recommendations(
            query=query,
            data_model_id=data_model_id,
            similarity_top_k=similarity_top_k,
            ref=ref,
            num_articles_ref=num_articles_ref,
            search_algorithm=search_algorithm,
        )
        return format_results(response)

```
 |  
| --- | --- |  
###  get_sports_news_recommendations [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierAIRecommendationsToolSpec.get_sports_news_recommendations "Permanent link")

```
get_sports_news_recommendations(
    query: ,
    similarity_top_k:  = 10,
    ref: Optional[] = None,
    num_articles_ref:  = 0,
    search_algorithm: Literal[
        "most_recent",
        "semantic",
        "most_recent_semantic",
        "trending",
    ] = "most_recent",
) -> 

```

Retrieves sports news.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query to fetch sports news.  |  _required_  |  
|  `similarity_top_k`  |  Number of documents to return.  |  
|  `ref`  |  `Optional[str]`  |  Site domain where recommendations should be displayed.  |  `None`  |  
|  `num_articles_ref`  |  Minimum number of articles to return from the reference domain.  |  
|  `search_algorithm`  |  The search algorithm to use.  |  `'most_recent'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A response message for the user specified query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/ai_recommendations/base.py`  
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
```
 | 
```
defget_sports_news_recommendations(
    self,
    query: str,
    similarity_top_k: int = 10,
    ref: Optional[str] = None,
    num_articles_ref: int = 0,
    search_algorithm: Literal[
        "most_recent", "semantic", "most_recent_semantic", "trending"
    ] = "most_recent",
) -> str:
"""
    Retrieves sports news.

    Args:
        query (str): Query to fetch sports news.
        similarity_top_k (int): Number of documents to return.
        ref (Optional[str]): Site domain where recommendations should be displayed.
        num_articles_ref (int): Minimum number of articles to return from the reference domain.
        search_algorithm (str): The search algorithm to use.

    Returns:
        str: A response message for the user specified query.

    """
    data_model_id = "dm_01j0pb465keqmatq9k83dthx34"  # Sports News
    response = self.client.get_ai_recommendations(
        query=query,
        data_model_id=data_model_id,
        similarity_top_k=similarity_top_k,
        ref=ref,
        num_articles_ref=num_articles_ref,
        search_algorithm=search_algorithm,
    )
    return format_results(response)

```
 |  
| --- | --- |  
###  get_lifestyle_news_recommendations [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierAIRecommendationsToolSpec.get_lifestyle_news_recommendations "Permanent link")

```
get_lifestyle_news_recommendations(
    query: ,
    similarity_top_k:  = 10,
    ref: Optional[] = None,
    num_articles_ref:  = 0,
    search_algorithm: Literal[
        "most_recent",
        "semantic",
        "most_recent_semantic",
        "trending",
    ] = "most_recent",
) -> 

```

Retrieves lifestyle news.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query to fetch lifestyle news.  |  _required_  |  
|  `similarity_top_k`  |  Number of documents to return.  |  
|  `ref`  |  `Optional[str]`  |  Site domain where recommendations should be displayed.  |  `None`  |  
|  `num_articles_ref`  |  Minimum number of articles to return from the reference domain.  |  
|  `search_algorithm`  |  The search algorithm to use.  |  `'most_recent'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A response message for the user specified query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/ai_recommendations/base.py`  
| 
```
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
```
 | 
```
defget_lifestyle_news_recommendations(
    self,
    query: str,
    similarity_top_k: int = 10,
    ref: Optional[str] = None,
    num_articles_ref: int = 0,
    search_algorithm: Literal[
        "most_recent", "semantic", "most_recent_semantic", "trending"
    ] = "most_recent",
) -> str:
"""
    Retrieves lifestyle news.

    Args:
        query (str): Query to fetch lifestyle news.
        similarity_top_k (int): Number of documents to return.
        ref (Optional[str]): Site domain where recommendations should be displayed.
        num_articles_ref (int): Minimum number of articles to return from the reference domain.
        search_algorithm (str): The search algorithm to use.

    Returns:
        str: A response message for the user specified query.

    """
    data_model_id = "dm_01j0q82s4bfjmsqkhs3ywm3x6y"  # Lifestyle News
    response = self.client.get_ai_recommendations(
        query=query,
        data_model_id=data_model_id,
        similarity_top_k=similarity_top_k,
        ref=ref,
        num_articles_ref=num_articles_ref,
        search_algorithm=search_algorithm,
    )
    return format_results(response)

```
 |  
| --- | --- |  
###  get_iheartdogs_recommendations [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierAIRecommendationsToolSpec.get_iheartdogs_recommendations "Permanent link")

```
get_iheartdogs_recommendations(
    query: ,
    similarity_top_k:  = 10,
    ref: Optional[] = None,
    num_articles_ref:  = 0,
    search_algorithm: Literal[
        "most_recent",
        "semantic",
        "most_recent_semantic",
        "trending",
    ] = "most_recent",
) -> 

```

Retrieves iHeartDogs articles - a dog care expert.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query to fetch dog care articles.  |  _required_  |  
|  `similarity_top_k`  |  Number of documents to return.  |  
|  `ref`  |  `Optional[str]`  |  Site domain where recommendations should be displayed.  |  `None`  |  
|  `num_articles_ref`  |  Minimum number of articles to return from the reference domain.  |  
|  `search_algorithm`  |  The search algorithm to use.  |  `'most_recent'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A response message for the user specified query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/ai_recommendations/base.py`  
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
```
 | 
```
defget_iheartdogs_recommendations(
    self,
    query: str,
    similarity_top_k: int = 10,
    ref: Optional[str] = None,
    num_articles_ref: int = 0,
    search_algorithm: Literal[
        "most_recent", "semantic", "most_recent_semantic", "trending"
    ] = "most_recent",
) -> str:
"""
    Retrieves iHeartDogs articles - a dog care expert.

    Args:
        query (str): Query to fetch dog care articles.
        similarity_top_k (int): Number of documents to return.
        ref (Optional[str]): Site domain where recommendations should be displayed.
        num_articles_ref (int): Minimum number of articles to return from the reference domain.
        search_algorithm (str): The search algorithm to use.

    Returns:
        str: A response message for the user specified query.

    """
    data_model_id = "dm_01j1sz8t3qe6v9g8ad102kvmqn"  # iHeartDogs AI
    response = self.client.get_ai_recommendations(
        query=query,
        data_model_id=data_model_id,
        similarity_top_k=similarity_top_k,
        ref=ref,
        num_articles_ref=num_articles_ref,
        search_algorithm=search_algorithm,
    )
    return format_results(response)

```
 |  
| --- | --- |  
###  get_iheartcats_recommendations [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierAIRecommendationsToolSpec.get_iheartcats_recommendations "Permanent link")

```
get_iheartcats_recommendations(
    query: ,
    similarity_top_k:  = 10,
    ref: Optional[] = None,
    num_articles_ref:  = 0,
    search_algorithm: Literal[
        "most_recent",
        "semantic",
        "most_recent_semantic",
        "trending",
    ] = "most_recent",
) -> 

```

Retrieves iHeartCats articles - a cat care expert.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query to fetch cat care articles.  |  _required_  |  
|  `similarity_top_k`  |  Number of documents to return.  |  
|  `ref`  |  `Optional[str]`  |  Site domain where recommendations should be displayed.  |  `None`  |  
|  `num_articles_ref`  |  Minimum number of articles to return from the reference domain.  |  
|  `search_algorithm`  |  The search algorithm to use.  |  `'most_recent'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A response message for the user specified query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/ai_recommendations/base.py`  
| 
```
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
```
 | 
```
defget_iheartcats_recommendations(
    self,
    query: str,
    similarity_top_k: int = 10,
    ref: Optional[str] = None,
    num_articles_ref: int = 0,
    search_algorithm: Literal[
        "most_recent", "semantic", "most_recent_semantic", "trending"
    ] = "most_recent",
) -> str:
"""
    Retrieves iHeartCats articles - a cat care expert.

    Args:
        query (str): Query to fetch cat care articles.
        similarity_top_k (int): Number of documents to return.
        ref (Optional[str]): Site domain where recommendations should be displayed.
        num_articles_ref (int): Minimum number of articles to return from the reference domain.
        search_algorithm (str): The search algorithm to use.

    Returns:
        str: A response message for the user specified query.

    """
    data_model_id = "dm_01j1sza0h7ekhaecys2p3y0vmj"  # iHeartCats AI
    response = self.client.get_ai_recommendations(
        query=query,
        data_model_id=data_model_id,
        similarity_top_k=similarity_top_k,
        ref=ref,
        num_articles_ref=num_articles_ref,
        search_algorithm=search_algorithm,
    )
    return format_results(response)

```
 |  
| --- | --- |  
###  get_greenmonster_recommendations [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierAIRecommendationsToolSpec.get_greenmonster_recommendations "Permanent link")

```
get_greenmonster_recommendations(
    query: ,
    similarity_top_k:  = 10,
    ref: Optional[] = None,
    num_articles_ref:  = 0,
    search_algorithm: Literal[
        "most_recent",
        "semantic",
        "most_recent_semantic",
        "trending",
    ] = "most_recent",
) -> 

```

Retrieves GreenMonster articles - Compassionate Living Guide.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query to fetch compassionate living guides.  |  _required_  |  
|  `similarity_top_k`  |  Number of documents to return.  |  
|  `ref`  |  `Optional[str]`  |  Site domain where recommendations should be displayed.  |  `None`  |  
|  `num_articles_ref`  |  Minimum number of articles to return from the reference domain.  |  
|  `search_algorithm`  |  The search algorithm to use.  |  `'most_recent'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A response message for the user specified query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/ai_recommendations/base.py`  
| 
```
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
```
 | 
```
defget_greenmonster_recommendations(
    self,
    query: str,
    similarity_top_k: int = 10,
    ref: Optional[str] = None,
    num_articles_ref: int = 0,
    search_algorithm: Literal[
        "most_recent", "semantic", "most_recent_semantic", "trending"
    ] = "most_recent",
) -> str:
"""
    Retrieves GreenMonster articles - Compassionate Living Guide.

    Args:
        query (str): Query to fetch compassionate living guides.
        similarity_top_k (int): Number of documents to return.
        ref (Optional[str]): Site domain where recommendations should be displayed.
        num_articles_ref (int): Minimum number of articles to return from the reference domain.
        search_algorithm (str): The search algorithm to use.

    Returns:
        str: A response message for the user specified query.

    """
    data_model_id = "dm_01j5xy9w5sf49bm6b1prm80m27"  # GreenMonster
    response = self.client.get_ai_recommendations(
        query=query,
        data_model_id=data_model_id,
        similarity_top_k=similarity_top_k,
        ref=ref,
        num_articles_ref=num_articles_ref,
        search_algorithm=search_algorithm,
    )
    return format_results(response)

```
 |  
| --- | --- |  
###  get_wishtv_recommendations [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierAIRecommendationsToolSpec.get_wishtv_recommendations "Permanent link")

```
get_wishtv_recommendations(
    query: ,
    similarity_top_k:  = 10,
    ref: Optional[] = None,
    num_articles_ref:  = 0,
    search_algorithm: Literal[
        "most_recent",
        "semantic",
        "most_recent_semantic",
        "trending",
    ] = "most_recent",
) -> 

```

Retrieves news articles.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query to fetch news articles.  |  _required_  |  
|  `similarity_top_k`  |  The number of top documents to retrieve based on similarity. Defaults to 10.  |  
|  `ref`  |  `Optional[str]`  |  The site domain where recommendations should be displayed. Defaults to None.  |  `None`  |  
|  `num_articles_ref`  |  Minimum number of articles to return from the reference domain. Defaults to 0.  |  
|  `search_algorithm`  |  The search algorithm to use. Defaults to "most_recent".  |  `'most_recent'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A response message for the user specified query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/ai_recommendations/base.py`  
| 
```
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
```
 | 
```
defget_wishtv_recommendations(
    self,
    query: str,
    similarity_top_k: int = 10,
    ref: Optional[str] = None,
    num_articles_ref: int = 0,
    search_algorithm: Literal[
        "most_recent", "semantic", "most_recent_semantic", "trending"
    ] = "most_recent",
) -> str:
"""
    Retrieves news articles.

    Args:
        query (str): Query to fetch news articles.
        similarity_top_k (int): The number of top documents to retrieve based on similarity. Defaults to 10.
        ref (Optional[str]): The site domain where recommendations should be displayed. Defaults to None.
        num_articles_ref (int): Minimum number of articles to return from the reference domain. Defaults to 0.
        search_algorithm (str): The search algorithm to use. Defaults to "most_recent".

    Returns:
        str: A response message for the user specified query.

    """
    data_model_id = "dm_01jagy9nqaeer9hxx8z1sk1jx6"  # WISH-TV AI
    response = self.client.get_ai_recommendations(
        query=query,
        data_model_id=data_model_id,
        similarity_top_k=similarity_top_k,
        ref=ref,
        num_articles_ref=num_articles_ref,
        search_algorithm=search_algorithm,
    )
    return format_results(response)

```
 |  
| --- | --- |  
###  get_nine_and_ten_news_recommendations [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierAIRecommendationsToolSpec.get_nine_and_ten_news_recommendations "Permanent link")

```
get_nine_and_ten_news_recommendations(
    query: ,
    similarity_top_k:  = 10,
    ref: Optional[] = None,
    num_articles_ref:  = 0,
    search_algorithm: Literal[
        "most_recent",
        "semantic",
        "most_recent_semantic",
        "trending",
    ] = "most_recent",
) -> 

```

Retrieves up-to-date local news for Northern Michigan, Cadillac and Traverse City.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query to fetch local news.  |  _required_  |  
|  `similarity_top_k`  |  Number of documents to return.  |  
|  `ref`  |  `Optional[str]`  |  Site domain where recommendations should be displayed.  |  `None`  |  
|  `num_articles_ref`  |  Minimum number of articles to return from the reference domain.  |  
|  `search_algorithm`  |  The search algorithm to use.  |  `'most_recent'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A response message for the user specified query.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/ai_recommendations/base.py`  
| 
```
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
```
 | 
```
defget_nine_and_ten_news_recommendations(
    self,
    query: str,
    similarity_top_k: int = 10,
    ref: Optional[str] = None,
    num_articles_ref: int = 0,
    search_algorithm: Literal[
        "most_recent", "semantic", "most_recent_semantic", "trending"
    ] = "most_recent",
) -> str:
"""
    Retrieves up-to-date local news for Northern Michigan, Cadillac and
    Traverse City.

    Args:
        query (str): Query to fetch local news.
        similarity_top_k (int): Number of documents to return.
        ref (Optional[str]): Site domain where recommendations should be displayed.
        num_articles_ref (int): Minimum number of articles to return from the reference domain.
        search_algorithm (str): The search algorithm to use.

    Returns:
        str: A response message for the user specified query.

    """
    data_model_id = "dm_01jhtt138wf1b9j8jwswye99y5"  # 9 and 10 News
    response = self.client.get_ai_recommendations(
        query=query,
        data_model_id=data_model_id,
        similarity_top_k=similarity_top_k,
        ref=ref,
        num_articles_ref=num_articles_ref,
        search_algorithm=search_algorithm,
    )
    return format_results(response)

```
 |  
| --- | --- |  
##  DappierRealTimeSearchToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierRealTimeSearchToolSpec "Permanent link")
Bases: 
Dappier Real Time Search tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/real_time_search/base.py`  
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
```
 | 
```
classDappierRealTimeSearchToolSpec(BaseToolSpec):
"""Dappier Real Time Search tool spec."""

    spec_functions = ["search_real_time_data", "search_stock_market_data"]

    def__init__(self, api_key: Optional[str] = None) -> None:
"""
        Initialize the Dappier Real Time Search tool spec.

        To obtain an API key, visit: https://platform.dappier.com/profile/api-keys
        """
        fromdappierimport Dappier

        self.api_key = api_key or os.environ.get("DAPPIER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it as a parameter or set DAPPIER_API_KEY in environment variables.\n"
                "To obtain an API key, visit: https://platform.dappier.com/profile/api-keys"
            )

        self.client = Dappier(api_key=self.api_key)

    defsearch_real_time_data(self, query: str) -> str:
"""
        Performs a real-time data search.

        Args:
            query (str): The user-provided input string for retrieving
            real-time google web search results including the latest news,
            weather, travel, deals and more.

        Returns:
            str: A response message containing the real-time data results.

        """
        ai_model_id = "am_01j0rzq4tvfscrgzwac7jv1p4c"
        response = self.client.search_real_time_data(
            query=query, ai_model_id=ai_model_id
        )
        return response.message if response else "No real-time data found."

    defsearch_stock_market_data(self, query: str) -> str:
"""
        Performs a stock market data search.

        Args:
            query (str): The user-provided input string for retrieving
            real-time financial news, stock prices, and trades from polygon.io,
            with AI-powered insights and up-to-the-minute updates to keep you
            informed on all your financial interests.

        Returns:
            str: A response message containing the stock market data results.

        """
        ai_model_id = "am_01j749h8pbf7ns8r1bq9s2evrh"
        response = self.client.search_real_time_data(
            query=query, ai_model_id=ai_model_id
        )
        return response.message if response else "No stock market data found."

```
 |  
| --- | --- |  
###  search_real_time_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierRealTimeSearchToolSpec.search_real_time_data "Permanent link")

```
search_real_time_data(query: ) -> 

```

Performs a real-time data search.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The user-provided input string for retrieving  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A response message containing the real-time data results.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/real_time_search/base.py`  
| 
```
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
```
 | 
```
defsearch_real_time_data(self, query: str) -> str:
"""
    Performs a real-time data search.

    Args:
        query (str): The user-provided input string for retrieving
        real-time google web search results including the latest news,
        weather, travel, deals and more.

    Returns:
        str: A response message containing the real-time data results.

    """
    ai_model_id = "am_01j0rzq4tvfscrgzwac7jv1p4c"
    response = self.client.search_real_time_data(
        query=query, ai_model_id=ai_model_id
    )
    return response.message if response else "No real-time data found."

```
 |  
| --- | --- |  
###  search_stock_market_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/dappier/#llama_index.tools.dappier.DappierRealTimeSearchToolSpec.search_stock_market_data "Permanent link")

```
search_stock_market_data(query: ) -> 

```

Performs a stock market data search.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The user-provided input string for retrieving  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  A response message containing the stock market data results.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-dappier/llama_index/tools/dappier/real_time_search/base.py`  
| 
```
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
```
 | 
```
defsearch_stock_market_data(self, query: str) -> str:
"""
    Performs a stock market data search.

    Args:
        query (str): The user-provided input string for retrieving
        real-time financial news, stock prices, and trades from polygon.io,
        with AI-powered insights and up-to-the-minute updates to keep you
        informed on all your financial interests.

    Returns:
        str: A response message containing the stock market data results.

    """
    ai_model_id = "am_01j749h8pbf7ns8r1bq9s2evrh"
    response = self.client.search_real_time_data(
        query=query, ai_model_id=ai_model_id
    )
    return response.message if response else "No stock market data found."

```
 |  
| --- | --- |  
options: members: - DappierAIRecommendationsToolSpec - DappierRealTimeSearchToolSpec
