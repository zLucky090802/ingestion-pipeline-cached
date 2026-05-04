# Rankgpt rerank
##  RankGPTRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/rankgpt_rerank/#llama_index.postprocessor.rankgpt_rerank.RankGPTRerank "Permanent link")
Bases: 
RankGPT-based reranker.
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-rankgpt-rerank/llama_index/postprocessor/rankgpt_rerank/base.py`  
| 
```
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
```
 | 
```
classRankGPTRerank(BaseNodePostprocessor):
"""RankGPT-based reranker."""

    top_n: int = Field(default=5, description="Top N nodes to return from reranking.")
    llm: Optional[LLM] = None
    verbose: bool = Field(
        default=False, description="Whether to print intermediate steps."
    )
    rankgpt_rerank_prompt: BasePromptTemplate = Field(
        description="rankGPT rerank prompt."
    )

    def__init__(
        self,
        top_n: int = 5,
        llm: Optional[LLM] = None,
        verbose: bool = False,
        rankgpt_rerank_prompt: Optional[BasePromptTemplate] = None,
    ):
        rankgpt_rerank_prompt = rankgpt_rerank_prompt or RANKGPT_RERANK_PROMPT
        super().__init__(
            verbose=verbose,
            llm=llm,
            top_n=top_n,
            rankgpt_rerank_prompt=rankgpt_rerank_prompt,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "RankGPTRerank"

    def_ensure_llm(self) -> None:
        if not self.llm:
            try:
                fromllama_index.llms.openaiimport OpenAI

                self.llm = OpenAI(model="gpt-3.5-turbo-16k")
            except ImportError:
                raise RuntimeError(
                    "OpenAI LLM is not available. Please install `llama-index-llms-openai` "
                    "or provide an alternative LLM instance."
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
                model_name=self.llm.metadata.model_name,
            )
        )

        if query_bundle is None:
            raise ValueError("Query bundle must be provided.")

        items = {
            "query": query_bundle.query_str,
            "hits": [
                {"content": node.get_content(metadata_mode=MetadataMode.EMBED)}
                for node in nodes
            ],
        }

        messages = self.create_permutation_instruction(item=items)
        permutation = self.run_llm(messages=messages)
        if permutation.message is not None and permutation.message.content is not None:
            rerank_ranks = self._receive_permutation(
                items, str(permutation.message.content)
            )
            if self.verbose:
                print_text(f"After Reranking, new rank list for nodes: {rerank_ranks}")

            initial_results: List[NodeWithScore] = []

            for idx in rerank_ranks:
                initial_results.append(
                    NodeWithScore(node=nodes[idx].node, score=nodes[idx].score)
                )

            dispatcher.event(ReRankEndEvent(nodes=initial_results[: self.top_n]))
            return initial_results[: self.top_n]
        else:
            dispatcher.event(ReRankEndEvent(nodes=nodes[: self.top_n]))
            return nodes[: self.top_n]

    def_get_prompts(self) -> PromptDictType:
"""Get prompts."""
        return {"rankgpt_rerank_prompt": self.rankgpt_rerank_prompt}

    def_update_prompts(self, prompts: PromptDictType) -> None:
"""Update prompts."""
        if "rankgpt_rerank_prompt" in prompts:
            self.rankgpt_rerank_prompt = prompts["rankgpt_rerank_prompt"]

    def_get_prefix_prompt(self, query: str, num: int) -> List[ChatMessage]:
        return [
            ChatMessage(
                role="system",
                content="You are RankGPT, an intelligent assistant that can rank passages based on their relevancy to the query.",
            ),
            ChatMessage(
                role="user",
                content=f"I will provide you with {num} passages, each indicated by number identifier []. \nRank the passages based on their relevance to query: {query}.",
            ),
            ChatMessage(role="assistant", content="Okay, please provide the passages."),
        ]

    def_get_post_prompt(self, query: str, num: int) -> str:
        return self.rankgpt_rerank_prompt.format(query=query, num=num)

    defcreate_permutation_instruction(self, item: Dict[str, Any]) -> List[ChatMessage]:
        query = item["query"]
        num = len(item["hits"])

        messages = self._get_prefix_prompt(query, num)
        rank = 0
        for hit in item["hits"]:
            rank += 1
            content = hit["content"]
            content = content.replace("Title: Content: ", "")
            content = content.strip()
            # For Japanese should cut by character: content = content[:int(max_length)]
            content = " ".join(content.split()[:300])
            messages.append(ChatMessage(role="user", content=f"[{rank}] {content}"))
            messages.append(
                ChatMessage(role="assistant", content=f"Received passage [{rank}].")
            )
        messages.append(
            ChatMessage(role="user", content=self._get_post_prompt(query, num))
        )
        return messages

    defrun_llm(self, messages: Sequence[ChatMessage]) -> ChatResponse:
        self._ensure_llm()
        return self.llm.chat(messages)

    def_clean_response(self, response: str) -> str:
        new_response = ""
        for c in response:
            if not c.isdigit():
                new_response += " "
            else:
                new_response += c
        return new_response.strip()

    def_remove_duplicate(self, response: List[int]) -> List[int]:
        new_response = []
        for c in response:
            if c not in new_response:
                new_response.append(c)
        return new_response

    def_receive_permutation(self, item: Dict[str, Any], permutation: str) -> List[int]:
        rank_end = len(item["hits"])

        response = self._clean_response(permutation)
        response_list = [int(x) - 1 for x in response.split()]
        response_list = self._remove_duplicate(response_list)
        response_list = [ss for ss in response_list if ss in range(rank_end)]
        return response_list + [
            tt for tt in range(rank_end) if tt not in response_list
        ]  # add the rest of the rank

```
 |  
| --- | --- |  
options: members: - RankGPTRerank
