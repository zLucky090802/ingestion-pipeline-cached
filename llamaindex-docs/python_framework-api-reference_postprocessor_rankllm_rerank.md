# Rankllm rerank
##  RankLLMRerank [#](https://developers.llamaindex.ai/python/framework-api-reference/postprocessor/rankllm_rerank/#llama_index.postprocessor.rankllm_rerank.RankLLMRerank "Permanent link")
Bases: 
RankLLM reranking suite. This class allows access to several reranking models supported by RankLLM. To use a model offered by the RankLLM suite, pass the desired model's hugging face path, found at https://huggingface.co/castorini. e.g., to access LiT5-Distill-base, pass 'castorini/LiT5-Distill-base' as the model name (https://huggingface.co/castorini/LiT5-Distill-base).
Below are all the rerankers supported with the model name to be passed as an argument to the constructor. Some model have convenience names for ease of use: Listwise: - OSLLM (Open Source LLM). Takes in a valid Hugging Face model name. e.g., 'Qwen/Qwen2.5-7B-Instruct' - RankZephyr. model='rank_zephyr' or 'castorini/rank_zephyr_7b_v1_full' - RankVicuna. model='rank_zephyr' or 'castorini/rank_vicuna_7b_v1' - RankGPT. Takes in a valid gpt model. e.g., 'gpt-3.5-turbo', 'gpt-4','gpt-3' - GenAI. Takes in a valid gemini model. e.g., 'gemini-2.0-flash' Pairwise: - DuoT5. model='duot5' Pointwise: - MonoT5. model='monot5'
Source code in `llama-index-integrations/postprocessor/llama-index-postprocessor-rankllm-rerank/llama_index/postprocessor/rankllm_rerank/base.py`  
| 
```
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
```
 | 
```
classRankLLMRerank(BaseNodePostprocessor):
"""
    RankLLM reranking suite. This class allows access to several reranking models supported by RankLLM. To use a model offered by the RankLLM suite, pass the desired model's hugging face path, found at https://huggingface.co/castorini. e.g., to access LiT5-Distill-base, pass 'castorini/LiT5-Distill-base' as the model name (https://huggingface.co/castorini/LiT5-Distill-base).

    Below are all the rerankers supported with the model name to be passed as an argument to the constructor. Some model have convenience names for ease of use:
        Listwise:
            - OSLLM (Open Source LLM). Takes in a valid Hugging Face model name. e.g., 'Qwen/Qwen2.5-7B-Instruct'
            - RankZephyr. model='rank_zephyr' or 'castorini/rank_zephyr_7b_v1_full'
            - RankVicuna. model='rank_zephyr' or 'castorini/rank_vicuna_7b_v1'
            - RankGPT. Takes in a valid gpt model. e.g., 'gpt-3.5-turbo', 'gpt-4','gpt-3'
            - GenAI. Takes in a valid gemini model. e.g., 'gemini-2.0-flash'
        Pairwise:
            - DuoT5. model='duot5'
        Pointwise:
            - MonoT5. model='monot5'
    """

    model: str = Field(description="Model name.", default="rank_zephyr")
    top_n: Optional[int] = Field(
        description="Number of nodes to return sorted by reranking score."
    )
    window_size: int = Field(
        description="Reranking window size. Applicable only for listwise and pairwise models.",
        default=20,
    )
    batch_size: Optional[int] = Field(
        description="Reranking batch size. Applicable only for pointwise models."
    )
    context_size: int = Field(
        description="Maximum number of tokens for the context window.", default=4096
    )
    prompt_mode: PromptMode = Field(
        description="Prompt format and strategy used when invoking the reranking model.",
        default=PromptMode.RANK_GPT,
    )
    num_gpus: int = Field(
        description="Number of GPUs to use for inference if applicable.", default=1
    )
    num_few_shot_examples: int = Field(
        description="Number of few-shot examples to include in the prompt.", default=0
    )
    few_shot_file: Optional[str] = Field(
        description="Path to a file containing few-shot examples, used if few-shot prompting is enabled.",
        default=None,
    )
    use_logits: bool = Field(
        description="Whether to use raw logits for reranking scores instead of probabilities.",
        default=False,
    )
    use_alpha: bool = Field(
        description="Whether to apply an alpha scaling factor in the reranking score calculation.",
        default=False,
    )
    variable_passages: bool = Field(
        description="Whether to allow passages of variable lengths instead of fixed-size chunks.",
        default=False,
    )
    stride: int = Field(
        description="Stride to use when sliding over long documents for reranking.",
        default=10,
    )
    use_azure_openai: bool = Field(
        description="Whether to use Azure OpenAI instead of the standard OpenAI API.",
        default=False,
    )

    _reranker: Any = PrivateAttr()

    @classmethod
    defclass_name(cls) -> str:
        return "RankLLMRerank"

    def_postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
        kwargs = {
            "model_path": self.model,
            "default_model_coordinator": None,
            "context_size": self.context_size,
            "prompt_mode": self.prompt_mode,
            "num_gpus": self.num_gpus,
            "use_logits": self.use_logits,
            "use_alpha": self.use_alpha,
            "num_few_shot_examples": self.num_few_shot_examples,
            "few_shot_file": self.few_shot_file,
            "variable_passages": self.variable_passages,
            "interactive": False,
            "window_size": self.window_size,
            "stride": self.stride,
            "use_azure_openai": self.use_azure_openai,
        }
        model_coordinator = Reranker.create_model_coordinator(**kwargs)
        self._reranker = Reranker(model_coordinator)

        dispatcher.event(
            ReRankStartEvent(
                query=query_bundle,
                nodes=nodes,
                top_n=self.top_n,
                model_name=self.model,
            )
        )

        docs = [
            (node.get_content(metadata_mode=MetadataMode.EMBED), node.get_score())
            for node in nodes
        ]

        request = Request(
            query=Query(
                text=query_bundle.query_str,
                qid=1,
            ),
            candidates=[
                Candidate(
                    docid=index,
                    score=doc[1],
                    doc={
                        "body": doc[0],
                        "headings": "",
                        "title": "",
                        "url": "",
                    },
                )
                for index, doc in enumerate(docs)
            ],
        )

        # scores are maintained the same as generated from the retriever
        permutation = self._reranker.rerank(
            request,
            rank_end=len(request.candidates),
            rank_start=0,
            shuffle_candidates=False,
            logging=False,
            top_k_retrieve=len(request.candidates),
        )

        new_nodes: List[NodeWithScore] = []
        for candidate in permutation.candidates:
            id: int = int(candidate.docid)
            new_nodes.append(NodeWithScore(node=nodes[id].node, score=nodes[id].score))

        if self.top_n is None:
            dispatcher.event(ReRankEndEvent(nodes=new_nodes))
            return new_nodes
        else:
            dispatcher.event(ReRankEndEvent(nodes=new_nodes[: self.top_n]))
            return new_nodes[: self.top_n]

```
 |  
| --- | --- |  
options: members: - CLASS
