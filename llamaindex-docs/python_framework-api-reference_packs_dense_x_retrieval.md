# Dense x retrieval
##  DenseXRetrievalPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/dense_x_retrieval/#llama_index.packs.dense_x_retrieval.DenseXRetrievalPack "Permanent link")
Bases: 
Source code in `llama-index-packs/llama-index-packs-dense-x-retrieval/llama_index/packs/dense_x_retrieval/base.py`  
| 
```
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
```
 | 
```
classDenseXRetrievalPack(BaseLlamaPack):
    def__init__(
        self,
        documents: List[Document],
        proposition_llm: Optional[LLM] = None,
        query_llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        text_splitter: TextSplitter = SentenceSplitter(),
        similarity_top_k: int = 4,
        streaming: bool = False,
    ) -> None:
"""Init params."""
        self._proposition_llm = proposition_llm or OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=750,
        )

        Settings.embed_model = embed_model or OpenAIEmbedding(embed_batch_size=128)
        Settings.llm = query_llm or OpenAI()
        Settings.num_output = self._proposition_llm.metadata.num_output

        nodes = text_splitter.get_nodes_from_documents(documents)
        sub_nodes = self._gen_propositions(nodes)

        all_nodes = nodes + sub_nodes
        all_nodes_dict = {n.node_id: n for n in all_nodes}

        self.vector_index = VectorStoreIndex(all_nodes, show_progress=True)

        self.retriever = RecursiveRetriever(
            "vector",
            retriever_dict={
                "vector": self.vector_index.as_retriever(
                    similarity_top_k=similarity_top_k
                )
            },
            node_dict=all_nodes_dict,
        )

        self.query_engine = RetrieverQueryEngine.from_args(
            self.retriever, streaming=streaming
        )

    async def_aget_proposition(self, node: TextNode) -> List[TextNode]:
"""Get proposition."""
        inital_output = await self._proposition_llm.apredict(
            PROPOSITIONS_PROMPT, node_text=node.text
        )
        outputs = inital_output.split("\n")

        all_propositions = []

        for output in outputs:
            if not output.strip():
                continue
            if not output.strip().endswith("]"):
                if not output.strip().endswith('"') and not output.strip().endswith(
                    ","
                ):
                    output = output + '"'
                output = output + " ]"
            if not output.strip().startswith("["):
                if not output.strip().startswith('"'):
                    output = '"' + output
                output = "[ " + output

            try:
                propositions = json.loads(output)
            except Exception:
                # fallback to yaml
                try:
                    propositions = yaml.safe_load(output)
                except Exception:
                    # fallback to next output
                    continue

            if not isinstance(propositions, list):
                continue

            all_propositions.extend(propositions)

        assert isinstance(all_propositions, list)
        nodes = [TextNode(text=prop) for prop in all_propositions if prop]

        return [IndexNode.from_text_node(n, node.node_id) for n in nodes]

    def_gen_propositions(self, nodes: List[TextNode]) -> List[TextNode]:
"""Get propositions."""
        sub_nodes = asyncio.run(
            run_jobs(
                [self._aget_proposition(node) for node in nodes],
                show_progress=True,
                workers=8,
            )
        )

        # Flatten list
        return [node for sub_node in sub_nodes for node in sub_node]

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "query_engine": self.query_engine,
            "retriever": self.retriever,
        }

    defrun(self, query_str: str, **kwargs: Any) -> RESPONSE_TYPE:
"""Run the pipeline."""
        return self.query_engine.query(query_str)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/dense_x_retrieval/#llama_index.packs.dense_x_retrieval.DenseXRetrievalPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-dense-x-retrieval/llama_index/packs/dense_x_retrieval/base.py`  
| 
```
169
170
171
172
173
174
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "query_engine": self.query_engine,
        "retriever": self.retriever,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/dense_x_retrieval/#llama_index.packs.dense_x_retrieval.DenseXRetrievalPack.run "Permanent link")

```
run(query_str: , **kwargs: ) -> RESPONSE_TYPE

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-dense-x-retrieval/llama_index/packs/dense_x_retrieval/base.py`  
| 
```
176
177
178
```
 | 
```
defrun(self, query_str: str, **kwargs: Any) -> RESPONSE_TYPE:
"""Run the pipeline."""
    return self.query_engine.query(query_str)

```
 |  
| --- | --- |  
options: members: - DenseXRetrievalPack
