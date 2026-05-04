# Topic
##  TopicNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/topic/#llama_index.node_parser.topic.TopicNodeParser "Permanent link")
Bases: 
Topic Based node parser.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-topic/llama_index/node_parser/topic/base.py`  
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
```
 | 
```
classTopicNodeParser(NodeParser):
"""Topic Based node parser."""

    max_chunk_size: int = Field(
        default=1000,
        description="The maximum number of tokens in a chunk.",
    )

    window_size: int = Field(
        default=5,
        description="Paragraph sliding window size",
    )

    llm: LLM = Field(
        description="The LLM model to use for parsing.",
    )
    similarity_method: str = Field(
        default="llm",
        description="The method to use for determining if a new proposition belongs to the same topic. Choose 'llm' or 'embedding'.",
    )
    embed_model: SerializeAsAny[BaseEmbedding] = Field(
        description="The embedding model to use for determining similarity between propositions.",
    )
    similarity_threshold: float = Field(
        default=0.8,
        description="The threshold for determining similarity between propositions.",
    )
    tokenizer: Callable = Field(
        description="The tokenizer to use for tokenizing text.",
    )

    @classmethod
    defclass_name(cls) -> str:
        return "TopicNodeParser"

    @classmethod
    deffrom_defaults(
        cls,
        callback_manager: Optional[CallbackManager] = None,
        id_func: Optional[Callable[[int, Document], str]] = None,
        tokenizer: Optional[Callable] = None,
        max_chunk_size: int = 1000,
        window_size: int = 5,
        llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        similarity_method: str = "llm",
        similarity_threshold: float = 0.8,
    ) -> "TopicNodeParser":
"""Initialize with parameters."""
        fromllama_index.coreimport Settings

        callback_manager = callback_manager or CallbackManager([])
        id_func = id_func or default_id_func
        tokenizer = tokenizer or get_tokenizer()
        llm = llm or Settings.llm
        embed_model = embed_model or Settings.embed_model

        return cls(
            callback_manager=callback_manager,
            id_func=id_func,
            tokenizer=tokenizer,
            max_chunk_size=max_chunk_size,
            window_size=window_size,
            llm=llm,
            embed_model=embed_model,
            similarity_threshold=similarity_threshold,
            similarity_method=similarity_method,
        )

    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""Parse document into nodes."""
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            nodes = self.build_topic_based_nodes_from_documents([node])
            all_nodes.extend(nodes)

        return all_nodes

    defsplit_into_paragraphs(self, text: str) -> List[str]:
"""Split the document into paragraphs based on line breaks."""
        return re.split(r"\n\s*\n", text)

    defproposition_transfer(self, paragraph: str) -> List[str]:
"""
        Convert a paragraph into a list of self-sustaining statements using LLM.
        """
        messages = [
            ChatMessage(role="system", content=PROPOSITION_SYSTEM_PROMPT),
            ChatMessage(role="user", content=paragraph),
        ]

        response = str(self.llm.chat(messages))

        json_start = response.find("[")
        json_end = response.rfind("]") + 1
        if json_start != -1 and json_end != -1:
            json_content = response[json_start:json_end]
            # Parse the JSON response
            try:
                return json.loads(json_content)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON: {json_content}")
                return []
        else:
            print(f"No valid JSON found in the response: {response}")
            return []

    defis_same_topic_llm(self, current_chunk: List[str], new_proposition: str) -> bool:
"""
        Use zero-shot classification with LLM to determine if the new proposition belongs to the same topic.
        """
        current_text = " ".join(current_chunk)
        messages = [
            ChatMessage(role="system", content=TOPIC_CLASSIFICATION_SYSTEM_PROMPT),
            ChatMessage(
                role="user",
                content=f"Text 1: {current_text}\n\nText 2: {new_proposition}",
            ),
        ]

        response = self.llm.chat(messages)

        return "same topic" in str(response).lower()

    defis_same_topic_embedding(
        self, current_chunk: List[str], new_proposition: str
    ) -> bool:
"""
        Use embedding-based similarity to determine if the new proposition belongs to the same topic.
        """
        current_text = " ".join(current_chunk)
        current_text_embedding = self.embed_model.get_text_embedding(current_text)
        new_proposition_embedding = self.embed_model.get_text_embedding(new_proposition)

        similarity_score = similarity(current_text_embedding, new_proposition_embedding)
        return similarity_score  self.similarity_threshold

    defsemantic_chunking(self, paragraphs: List[str]) -> List[str]:
"""
        Perform semantic chunking on the given paragraphs.
        max_chunk_size: It is based on hard threshold of 1000 characters.
        As per paper the hard threshold that the longest chunk cannot excess the context length limitation of LLM.
        Here we are using 1000 tokens as the threshold.
        """
        chunks: List[str] = []
        current_chunk: List[str] = []
        current_chunk_size: int = 0
        half_window = self.window_size // 2
        # Cache for storing propositions
        proposition_cache: Dict[int, List[str]] = {}

        for i in range(len(paragraphs)):
            # Define the window range
            start_idx = max(0, i - half_window)
            end_idx = min(len(paragraphs), i + half_window + 1)

            # Generate and cache propositions for paragraphs in the window
            window_propositions = []
            for j in range(start_idx, end_idx):
                if j not in proposition_cache:
                    proposition_cache[j] = self.proposition_transfer(paragraphs[j])
                window_propositions.extend(proposition_cache[j])

            for prop in window_propositions:
                if current_chunk:
                    if self.similarity_method == "llm":
                        is_same_topic = self.is_same_topic_llm(current_chunk, prop)
                    elif self.similarity_method == "embedding":
                        is_same_topic = self.is_same_topic_embedding(
                            current_chunk, prop
                        )
                    else:
                        raise ValueError(
                            "Invalid similarity method. Choose 'llm' or 'embedding'."
                        )
                else:
                    is_same_topic = True

                if not current_chunk or (
                    is_same_topic
                    and current_chunk_size + len(self.tokenizer(prop))
                    <= self.max_chunk_size
                ):
                    current_chunk.append(prop)
                    current_chunk_size += len(prop)
                else:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [prop]
                    current_chunk_size = len(self.tokenizer(prop))

            # If we've reached the max chunk size, start a new chunk
            if current_chunk_size >= self.max_chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_chunk_size = 0

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    defbuild_topic_based_nodes_from_documents(
        self, documents: Sequence[Document]
    ) -> List[BaseNode]:
"""Build topic based nodes from documents."""
        all_nodes: List[BaseNode] = []
        for doc in documents:
            paragraphs = self.split_into_paragraphs(doc.text)
            chunks = self.semantic_chunking(paragraphs)
            nodes = build_nodes_from_splits(
                chunks,
                doc,
                id_func=self.id_func,
            )
            all_nodes.extend(nodes)

        return all_nodes

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/topic/#llama_index.node_parser.topic.TopicNodeParser.from_defaults "Permanent link")

```
from_defaults(
    callback_manager: Optional[] = None,
    id_func: Optional[
        Callable[[, ], ]
    ] = None,
    tokenizer: Optional[Callable] = None,
    max_chunk_size:  = 1000,
    window_size:  = 5,
    llm: Optional[] = None,
    embed_model: Optional[] = None,
    similarity_method:  = "llm",
    similarity_threshold: float = 0.8,
) -> 

```

Initialize with parameters.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-topic/llama_index/node_parser/topic/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    callback_manager: Optional[CallbackManager] = None,
    id_func: Optional[Callable[[int, Document], str]] = None,
    tokenizer: Optional[Callable] = None,
    max_chunk_size: int = 1000,
    window_size: int = 5,
    llm: Optional[LLM] = None,
    embed_model: Optional[BaseEmbedding] = None,
    similarity_method: str = "llm",
    similarity_threshold: float = 0.8,
) -> "TopicNodeParser":
"""Initialize with parameters."""
    fromllama_index.coreimport Settings

    callback_manager = callback_manager or CallbackManager([])
    id_func = id_func or default_id_func
    tokenizer = tokenizer or get_tokenizer()
    llm = llm or Settings.llm
    embed_model = embed_model or Settings.embed_model

    return cls(
        callback_manager=callback_manager,
        id_func=id_func,
        tokenizer=tokenizer,
        max_chunk_size=max_chunk_size,
        window_size=window_size,
        llm=llm,
        embed_model=embed_model,
        similarity_threshold=similarity_threshold,
        similarity_method=similarity_method,
    )

```
 |  
| --- | --- |  
###  split_into_paragraphs [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/topic/#llama_index.node_parser.topic.TopicNodeParser.split_into_paragraphs "Permanent link")

```
split_into_paragraphs(text: ) -> []

```

Split the document into paragraphs based on line breaks.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-topic/llama_index/node_parser/topic/base.py`  
| 
```
125
126
127
```
 | 
```
defsplit_into_paragraphs(self, text: str) -> List[str]:
"""Split the document into paragraphs based on line breaks."""
    return re.split(r"\n\s*\n", text)

```
 |  
| --- | --- |  
###  proposition_transfer [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/topic/#llama_index.node_parser.topic.TopicNodeParser.proposition_transfer "Permanent link")

```
proposition_transfer(paragraph: ) -> []

```

Convert a paragraph into a list of self-sustaining statements using LLM.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-topic/llama_index/node_parser/topic/base.py`  
| 
```
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
```
 | 
```
defproposition_transfer(self, paragraph: str) -> List[str]:
"""
    Convert a paragraph into a list of self-sustaining statements using LLM.
    """
    messages = [
        ChatMessage(role="system", content=PROPOSITION_SYSTEM_PROMPT),
        ChatMessage(role="user", content=paragraph),
    ]

    response = str(self.llm.chat(messages))

    json_start = response.find("[")
    json_end = response.rfind("]") + 1
    if json_start != -1 and json_end != -1:
        json_content = response[json_start:json_end]
        # Parse the JSON response
        try:
            return json.loads(json_content)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON: {json_content}")
            return []
    else:
        print(f"No valid JSON found in the response: {response}")
        return []

```
 |  
| --- | --- |  
###  is_same_topic_llm [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/topic/#llama_index.node_parser.topic.TopicNodeParser.is_same_topic_llm "Permanent link")

```
is_same_topic_llm(
    current_chunk: [], new_proposition: 
) -> 

```

Use zero-shot classification with LLM to determine if the new proposition belongs to the same topic.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-topic/llama_index/node_parser/topic/base.py`  
| 
```
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
defis_same_topic_llm(self, current_chunk: List[str], new_proposition: str) -> bool:
"""
    Use zero-shot classification with LLM to determine if the new proposition belongs to the same topic.
    """
    current_text = " ".join(current_chunk)
    messages = [
        ChatMessage(role="system", content=TOPIC_CLASSIFICATION_SYSTEM_PROMPT),
        ChatMessage(
            role="user",
            content=f"Text 1: {current_text}\n\nText 2: {new_proposition}",
        ),
    ]

    response = self.llm.chat(messages)

    return "same topic" in str(response).lower()

```
 |  
| --- | --- |  
###  is_same_topic_embedding [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/topic/#llama_index.node_parser.topic.TopicNodeParser.is_same_topic_embedding "Permanent link")

```
is_same_topic_embedding(
    current_chunk: [], new_proposition: 
) -> 

```

Use embedding-based similarity to determine if the new proposition belongs to the same topic.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-topic/llama_index/node_parser/topic/base.py`  
| 
```
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
defis_same_topic_embedding(
    self, current_chunk: List[str], new_proposition: str
) -> bool:
"""
    Use embedding-based similarity to determine if the new proposition belongs to the same topic.
    """
    current_text = " ".join(current_chunk)
    current_text_embedding = self.embed_model.get_text_embedding(current_text)
    new_proposition_embedding = self.embed_model.get_text_embedding(new_proposition)

    similarity_score = similarity(current_text_embedding, new_proposition_embedding)
    return similarity_score  self.similarity_threshold

```
 |  
| --- | --- |  
###  semantic_chunking [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/topic/#llama_index.node_parser.topic.TopicNodeParser.semantic_chunking "Permanent link")

```
semantic_chunking(paragraphs: []) -> []

```

Perform semantic chunking on the given paragraphs. max_chunk_size: It is based on hard threshold of 1000 characters. As per paper the hard threshold that the longest chunk cannot excess the context length limitation of LLM. Here we are using 1000 tokens as the threshold.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-topic/llama_index/node_parser/topic/base.py`  
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
```
 | 
```
defsemantic_chunking(self, paragraphs: List[str]) -> List[str]:
"""
    Perform semantic chunking on the given paragraphs.
    max_chunk_size: It is based on hard threshold of 1000 characters.
    As per paper the hard threshold that the longest chunk cannot excess the context length limitation of LLM.
    Here we are using 1000 tokens as the threshold.
    """
    chunks: List[str] = []
    current_chunk: List[str] = []
    current_chunk_size: int = 0
    half_window = self.window_size // 2
    # Cache for storing propositions
    proposition_cache: Dict[int, List[str]] = {}

    for i in range(len(paragraphs)):
        # Define the window range
        start_idx = max(0, i - half_window)
        end_idx = min(len(paragraphs), i + half_window + 1)

        # Generate and cache propositions for paragraphs in the window
        window_propositions = []
        for j in range(start_idx, end_idx):
            if j not in proposition_cache:
                proposition_cache[j] = self.proposition_transfer(paragraphs[j])
            window_propositions.extend(proposition_cache[j])

        for prop in window_propositions:
            if current_chunk:
                if self.similarity_method == "llm":
                    is_same_topic = self.is_same_topic_llm(current_chunk, prop)
                elif self.similarity_method == "embedding":
                    is_same_topic = self.is_same_topic_embedding(
                        current_chunk, prop
                    )
                else:
                    raise ValueError(
                        "Invalid similarity method. Choose 'llm' or 'embedding'."
                    )
            else:
                is_same_topic = True

            if not current_chunk or (
                is_same_topic
                and current_chunk_size + len(self.tokenizer(prop))
                <= self.max_chunk_size
            ):
                current_chunk.append(prop)
                current_chunk_size += len(prop)
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [prop]
                current_chunk_size = len(self.tokenizer(prop))

        # If we've reached the max chunk size, start a new chunk
        if current_chunk_size >= self.max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_chunk_size = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

```
 |  
| --- | --- |  
###  build_topic_based_nodes_from_documents [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/topic/#llama_index.node_parser.topic.TopicNodeParser.build_topic_based_nodes_from_documents "Permanent link")

```
build_topic_based_nodes_from_documents(
    documents: Sequence[],
) -> []

```

Build topic based nodes from documents.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-topic/llama_index/node_parser/topic/base.py`  
| 
```
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
```
 | 
```
defbuild_topic_based_nodes_from_documents(
    self, documents: Sequence[Document]
) -> List[BaseNode]:
"""Build topic based nodes from documents."""
    all_nodes: List[BaseNode] = []
    for doc in documents:
        paragraphs = self.split_into_paragraphs(doc.text)
        chunks = self.semantic_chunking(paragraphs)
        nodes = build_nodes_from_splits(
            chunks,
            doc,
            id_func=self.id_func,
        )
        all_nodes.extend(nodes)

    return all_nodes

```
 |  
| --- | --- |  
options: members: - TopicNodeParser
