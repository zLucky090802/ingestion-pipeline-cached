# Index
Base retriever.
##  BaseRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/#llama_index.core.base.base_retriever.BaseRetriever "Permanent link")
Bases: `PromptMixin`, `DispatcherSpanMixin`
Base retriever.
Source code in `llama-index-core/llama_index/core/base/base_retriever.py`  
| 
```
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
```
 | 
```
classBaseRetriever(PromptMixin, DispatcherSpanMixin):
"""Base retriever."""

    def__init__(
        self,
        callback_manager: Optional[CallbackManager] = None,
        object_map: Optional[Dict] = None,
        objects: Optional[List[IndexNode]] = None,
        verbose: bool = False,
    ) -> None:
        self.callback_manager = callback_manager or CallbackManager()

        if objects is not None:
            object_map = {obj.index_id: obj.obj for obj in objects}

        self.object_map = object_map or {}
        self._verbose = verbose

    def_check_callback_manager(self) -> None:
"""Check callback manager."""
        if not hasattr(self, "callback_manager"):
            self.callback_manager = Settings.callback_manager

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {}

    def_get_prompt_modules(self) -> PromptMixinType:
"""Get prompt modules."""
        return {}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""

    def_retrieve_from_object(
        self,
        obj: Any,
        query_bundle: QueryBundle,
        score: float,
    ) -> List[NodeWithScore]:
"""Retrieve nodes from object."""
        if self._verbose:
            print_text(
                f"Retrieving from object {obj.__class__.__name__} with query {query_bundle.query_str}\n",
                color="llama_pink",
            )
        if isinstance(obj, NodeWithScore):
            return [obj]
        elif isinstance(obj, BaseNode):
            return [NodeWithScore(node=obj, score=score)]
        elif isinstance(obj, BaseQueryEngine):
            response = obj.query(query_bundle)
            return [
                NodeWithScore(
                    node=TextNode(text=str(response), metadata=response.metadata or {}),
                    score=score,
                )
            ]
        elif isinstance(obj, BaseRetriever):
            return obj.retrieve(query_bundle)
        else:
            raise ValueError(f"Object {obj} is not retrievable.")

    async def_aretrieve_from_object(
        self,
        obj: Any,
        query_bundle: QueryBundle,
        score: float,
    ) -> List[NodeWithScore]:
"""Retrieve nodes from object."""
        if isinstance(obj, NodeWithScore):
            return [obj]
        elif isinstance(obj, BaseNode):
            return [NodeWithScore(node=obj, score=score)]
        elif isinstance(obj, BaseQueryEngine):
            response = await obj.aquery(query_bundle)
            return [
                NodeWithScore(
                    node=TextNode(text=str(response), metadata=response.metadata or {}),
                    score=score,
                )
            ]
        elif isinstance(obj, BaseRetriever):
            return await obj.aretrieve(query_bundle)
        else:
            raise ValueError(f"Object {obj} is not retrievable.")

    def_handle_recursive_retrieval(
        self, query_bundle: QueryBundle, nodes: List[NodeWithScore]
    ) -> List[NodeWithScore]:
        retrieved_nodes: List[NodeWithScore] = []
        for n in nodes:
            node = n.node
            score = n.score or 1.0
            if isinstance(node, IndexNode):
                obj = node.obj or self.object_map.get(node.index_id, None)
                if obj is not None:
                    if self._verbose:
                        print_text(
                            f"Retrieval entering {node.index_id}: {obj.__class__.__name__}\n",
                            color="llama_turquoise",
                        )
                    retrieved_nodes.extend(
                        self._retrieve_from_object(
                            obj, query_bundle=query_bundle, score=score
                        )
                    )
                else:
                    retrieved_nodes.append(n)
            else:
                retrieved_nodes.append(n)

        seen = set()
        return [
            n
            for n in retrieved_nodes
            if not (
                n.node.node_id in seen or seen.add(n.node.node_id)  # type: ignore[func-returns-value]
            )
        ]

    async def_ahandle_recursive_retrieval(
        self, query_bundle: QueryBundle, nodes: List[NodeWithScore]
    ) -> List[NodeWithScore]:
        retrieved_nodes: List[NodeWithScore] = []
        for n in nodes:
            node = n.node
            score = n.score or 1.0
            if isinstance(node, IndexNode):
                obj = node.obj or self.object_map.get(node.index_id, None)
                if obj is not None:
                    if self._verbose:
                        print_text(
                            f"Retrieval entering {node.index_id}: {obj.__class__.__name__}\n",
                            color="llama_turquoise",
                        )
                    # TODO: Add concurrent execution via `run_jobs()` ?
                    retrieved_nodes.extend(
                        await self._aretrieve_from_object(
                            obj, query_bundle=query_bundle, score=score
                        )
                    )
                else:
                    retrieved_nodes.append(n)
            else:
                retrieved_nodes.append(n)

        # remove any duplicates based on node_id
        seen = set()
        return [
            n
            for n in retrieved_nodes
            if not (
                n.node.node_id in seen or seen.add(n.node.node_id)  # type: ignore[func-returns-value]
            )
        ]

    @dispatcher.span
    defretrieve(self, str_or_query_bundle: QueryType) -> List[NodeWithScore]:
"""
        Retrieve nodes given query.

        Args:
            str_or_query_bundle (QueryType): Either a query string or
                a QueryBundle object.

        """
        self._check_callback_manager()
        dispatcher.event(
            RetrievalStartEvent(
                str_or_query_bundle=str_or_query_bundle,
            )
        )
        if isinstance(str_or_query_bundle, str):
            query_bundle = QueryBundle(str_or_query_bundle)
        else:
            query_bundle = str_or_query_bundle
        with self.callback_manager.as_trace("query"):
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as retrieve_event:
                nodes = self._retrieve(query_bundle)
                nodes = self._handle_recursive_retrieval(query_bundle, nodes)
                retrieve_event.on_end(
                    payload={EventPayload.NODES: nodes},
                )
        dispatcher.event(
            RetrievalEndEvent(
                str_or_query_bundle=str_or_query_bundle,
                nodes=nodes,
            )
        )
        return nodes

    @dispatcher.span
    async defaretrieve(self, str_or_query_bundle: QueryType) -> List[NodeWithScore]:
        self._check_callback_manager()

        dispatcher.event(
            RetrievalStartEvent(
                str_or_query_bundle=str_or_query_bundle,
            )
        )
        if isinstance(str_or_query_bundle, str):
            query_bundle = QueryBundle(str_or_query_bundle)
        else:
            query_bundle = str_or_query_bundle
        with self.callback_manager.as_trace("query"):
            with self.callback_manager.event(
                CBEventType.RETRIEVE,
                payload={EventPayload.QUERY_STR: query_bundle.query_str},
            ) as retrieve_event:
                nodes = await self._aretrieve(query_bundle=query_bundle)
                nodes = await self._ahandle_recursive_retrieval(
                    query_bundle=query_bundle, nodes=nodes
                )
                retrieve_event.on_end(
                    payload={EventPayload.NODES: nodes},
                )
        dispatcher.event(
            RetrievalEndEvent(
                str_or_query_bundle=str_or_query_bundle,
                nodes=nodes,
            )
        )
        return nodes

    @abstractmethod
    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""
        Retrieve nodes given query.

        Implemented by the user.

        """

    # TODO: make this abstract
    # @abstractmethod
    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""
        Asynchronously retrieve nodes given query.

        Implemented by the user.

        """
        return self._retrieve(query_bundle)

```
 |  
| --- | --- |  
###  retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/#llama_index.core.base.base_retriever.BaseRetriever.retrieve "Permanent link")

```
retrieve(
    str_or_query_bundle: QueryType,
) -> []

```

Retrieve nodes given query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_or_query_bundle`  |  `QueryType`  |  Either a query string or a QueryBundle object.  |  _required_  |  
Source code in `llama-index-core/llama_index/core/base/base_retriever.py`  
| 
```
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
```
 | 
```
@dispatcher.span
defretrieve(self, str_or_query_bundle: QueryType) -> List[NodeWithScore]:
"""
    Retrieve nodes given query.

    Args:
        str_or_query_bundle (QueryType): Either a query string or
            a QueryBundle object.

    """
    self._check_callback_manager()
    dispatcher.event(
        RetrievalStartEvent(
            str_or_query_bundle=str_or_query_bundle,
        )
    )
    if isinstance(str_or_query_bundle, str):
        query_bundle = QueryBundle(str_or_query_bundle)
    else:
        query_bundle = str_or_query_bundle
    with self.callback_manager.as_trace("query"):
        with self.callback_manager.event(
            CBEventType.RETRIEVE,
            payload={EventPayload.QUERY_STR: query_bundle.query_str},
        ) as retrieve_event:
            nodes = self._retrieve(query_bundle)
            nodes = self._handle_recursive_retrieval(query_bundle, nodes)
            retrieve_event.on_end(
                payload={EventPayload.NODES: nodes},
            )
    dispatcher.event(
        RetrievalEndEvent(
            str_or_query_bundle=str_or_query_bundle,
            nodes=nodes,
        )
    )
    return nodes

```
 |  
| --- | --- |  
options: members: - BaseRetriever
##  BaseImageRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/#llama_index.core.image_retriever.BaseImageRetriever "Permanent link")
Bases: `PromptMixin`, `DispatcherSpanMixin`
Base Image Retriever Abstraction.
Source code in `llama-index-core/llama_index/core/image_retriever.py`  
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
```
 | 
```
classBaseImageRetriever(PromptMixin, DispatcherSpanMixin):
"""Base Image Retriever Abstraction."""

    deftext_to_image_retrieve(
        self, str_or_query_bundle: QueryType
    ) -> List[NodeWithScore]:
"""
        Retrieve image nodes given query or single image input.

        Args:
            str_or_query_bundle (QueryType): a query text
            string or a QueryBundle object.

        """
        if isinstance(str_or_query_bundle, str):
            str_or_query_bundle = QueryBundle(query_str=str_or_query_bundle)
        return self._text_to_image_retrieve(str_or_query_bundle)

    @abstractmethod
    def_text_to_image_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""
        Retrieve image nodes or documents given query text.

        Implemented by the user.

        """

    defimage_to_image_retrieve(
        self, str_or_query_bundle: QueryType
    ) -> List[NodeWithScore]:
"""
        Retrieve image nodes given single image input.

        Args:
            str_or_query_bundle (QueryType): a image path
            string or a QueryBundle object.

        """
        if isinstance(str_or_query_bundle, str):
            # leave query_str as empty since we are using image_path for image retrieval
            str_or_query_bundle = QueryBundle(
                query_str="", image_path=str_or_query_bundle
            )
        return self._image_to_image_retrieve(str_or_query_bundle)

    @abstractmethod
    def_image_to_image_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""
        Retrieve image nodes or documents given image.

        Implemented by the user.

        """

    # Async Methods
    async defatext_to_image_retrieve(
        self,
        str_or_query_bundle: QueryType,
    ) -> List[NodeWithScore]:
        if isinstance(str_or_query_bundle, str):
            str_or_query_bundle = QueryBundle(query_str=str_or_query_bundle)
        return await self._atext_to_image_retrieve(str_or_query_bundle)

    @abstractmethod
    async def_atext_to_image_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""
        Async retrieve image nodes or documents given query text.

        Implemented by the user.

        """

    async defaimage_to_image_retrieve(
        self,
        str_or_query_bundle: QueryType,
    ) -> List[NodeWithScore]:
        if isinstance(str_or_query_bundle, str):
            # leave query_str as empty since we are using image_path for image retrieval
            str_or_query_bundle = QueryBundle(
                query_str="", image_path=str_or_query_bundle
            )
        return await self._aimage_to_image_retrieve(str_or_query_bundle)

    @abstractmethod
    async def_aimage_to_image_retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
"""
        Async retrieve image nodes or documents given image.

        Implemented by the user.

        """

```
 |  
| --- | --- |  
###  text_to_image_retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/#llama_index.core.image_retriever.BaseImageRetriever.text_to_image_retrieve "Permanent link")

```
text_to_image_retrieve(
    str_or_query_bundle: QueryType,
) -> []

```

Retrieve image nodes given query or single image input.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_or_query_bundle`  |  `QueryType`  |  a query text  |  _required_  |  
Source code in `llama-index-core/llama_index/core/image_retriever.py`  
| 
```
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
```
 | 
```
deftext_to_image_retrieve(
    self, str_or_query_bundle: QueryType
) -> List[NodeWithScore]:
"""
    Retrieve image nodes given query or single image input.

    Args:
        str_or_query_bundle (QueryType): a query text
        string or a QueryBundle object.

    """
    if isinstance(str_or_query_bundle, str):
        str_or_query_bundle = QueryBundle(query_str=str_or_query_bundle)
    return self._text_to_image_retrieve(str_or_query_bundle)

```
 |  
| --- | --- |  
###  image_to_image_retrieve [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/#llama_index.core.image_retriever.BaseImageRetriever.image_to_image_retrieve "Permanent link")

```
image_to_image_retrieve(
    str_or_query_bundle: QueryType,
) -> []

```

Retrieve image nodes given single image input.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `str_or_query_bundle`  |  `QueryType`  |  a image path  |  _required_  |  
Source code in `llama-index-core/llama_index/core/image_retriever.py`  
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
```
 | 
```
defimage_to_image_retrieve(
    self, str_or_query_bundle: QueryType
) -> List[NodeWithScore]:
"""
    Retrieve image nodes given single image input.

    Args:
        str_or_query_bundle (QueryType): a image path
        string or a QueryBundle object.

    """
    if isinstance(str_or_query_bundle, str):
        # leave query_str as empty since we are using image_path for image retrieval
        str_or_query_bundle = QueryBundle(
            query_str="", image_path=str_or_query_bundle
        )
    return self._image_to_image_retrieve(str_or_query_bundle)

```
 |  
| --- | --- |  
options: members: - BaseImageRetriever
