# Raft dataset
##  RAFTDatasetPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raft_dataset/#llama_index.packs.raft_dataset.RAFTDatasetPack "Permanent link")
Bases: 
RAFT Dataset Generator pack.
Source code in `llama-index-packs/llama-index-packs-raft-dataset/llama_index/packs/raft_dataset/base.py`  
| 
```
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
```
 | 
```
classRAFTDatasetPack(BaseLlamaPack):
"""RAFT Dataset Generator pack."""

    def__init__(
        self,
        file_path: str,
        llm: Any = None,
        embed_model: Any = None,
        num_questions_per_chunk: int = 5,
        num_distract_docs: int = 3,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        default_breakpoint_percentile_threshold=DEFAULT_BREAKPOINT_PERCENTILE_THRESHOLD,
    ):
        self.file_path = file_path
        self.num_questions_per_chunk = num_questions_per_chunk
        self.num_distract_docs = num_distract_docs
        self.chunk_size = chunk_size
        self.default_breakpoint_percentile_threshold = (
            default_breakpoint_percentile_threshold
        )
        self.ds = None
        self.llm = OpenAI(temperature=0, n=1, model="gpt-4") if llm is None else llm
        self.embed_model = OpenAIEmbedding() if embed_model is None else embed_model

    defstrip_str(self, s) -> str:
"""
        Helper function for helping format strings returned by GPT-4.
        """
        if s.startswith("assistant:"):  # Check if the string starts with 'assistant '
            s = s.replace("assistant:", "", 1)  # Replace the first occurrence

        start_index, end_index = 0, len(s) - 1
        beg_found = False
        for i in range(len(s)):
            if s[i].isalpha():
                if not beg_found:
                    start_index = i
                    beg_found = True
                else:
                    end_index = i
        end_index += 2
        return s[start_index : min(end_index, len(s))]

    defencode_question_gen(self, question, chunk) -> List[str]:
"""
        Encode multiple prompt instructions into a single string for the general case.
        """
        prompt = f"""
            Question: {question}\nContext: {chunk}\n
            Answer this question using the information given in the context above. Here is things to pay attention to:
            - First provide step-by-step reasoning on how to answer the question.
            - In the reasoning, if you need to copy paste some sentences from the context, include them in ##begin_quote## and ##end_quote##. This would mean that things outside of ##begin_quote## and ##end_quote## are not directly copy paste from the context.
            - End your response with final answer in the form <ANSWER>: $answer, the answer should be succinct.
        """
        return [
            ChatMessage(
                role="system",
                content="You are a helpful question answerer who can provide an answer given a question and relevant context.",
            ),
            ChatMessage(role="user", content=prompt),
        ]

    defgenerate_label(self, question, context) -> str:
"""
        Generates the label / answer to `question` using `context` and GPT-4.
        """
        question_messages = self.encode_question_gen(question, context)
        response = self.llm.chat(question_messages)
        return str(response)

    defgenerate_instructions_gen(self, chunk, x=5) -> List[str]:
"""
        Generates `x` questions / use cases for `chunk`. Used when the input document is of general types
        `pdf`, `json`, or `txt`.
        """
        messages = [
            ChatMessage(
                role="system",
                content="You are a synthetic question-answer pair generator. Given a chunk of context about some topic(s), generate %s example questions a user could ask and would be answered using information from the chunk. For example, if the given context was a Wikipedia paragraph about the United States, an example question could be 'How many states are in the United States?'. The questions should be able to be answered in a few words or less."
                % (x),
            ),
            ChatMessage(role="user", content=str(chunk)),
        ]

        queries = str(self.llm.chat(messages)).split("\n")
        questions = [self.strip_str(q) for q in queries]
        questions = [q for q in questions if any(c.isalpha() for c in q)][:x]

        num_questions_generated = len(questions)
        if num_questions_generated  x:
            warnings.warn(
                f"Fewer questions generated ({num_questions_generated}) "
                f"than requested ({x})."
            )

        return questions

    defget_chunks(self, file_path: str, chunk_size: int) -> List[str]:
"""
        Takes in a `file_path`, retrieves the document, breaks it down into chunks of size
        `chunk_size`, and returns the chunks.
        """
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        splitter = SemanticSplitterNodeParser(
            buffer_size=1,
            breakpoint_percentile_threshold=self.default_breakpoint_percentile_threshold,
            embed_model=self.embed_model,
        )
        nodes = splitter.get_nodes_from_documents(documents)

        return [node.get_content() for node in nodes]

    defadd_chunk_to_dataset(
        self,
        chunks: List,
        chunk: str,
        x: int = 5,
        num_distract: int = 3,
        p: float = 1.0,
    ):
"""
        Given a chunk, create {Q, A, D} triplets and add them to the dataset.
        """
        i = chunks.index(chunk)
        qs = self.generate_instructions_gen(chunk, x)
        for q in qs:
            datapt = {
                "id": None,
                "type": None,
                "question": None,
                "context": None,
                "oracle_context": None,
                "cot_answer": None,
            }

            datapt["id"] = f"seed_task_{0ifnotself.dselseself.ds.num_rows}"
            datapt["type"] = "general"
            datapt["question"] = q

            # add distractor docs
            docs = [chunk]
            indices = list(range(len(chunks)))
            indices.remove(i)
            for j in random.sample(indices, num_distract):
                docs.append(chunks[j])
            # decides whether to add oracle document
            oracle = random.uniform(0, 1)  p
            if not oracle:
                docs[0] = chunks[random.sample(indices, 1)[0]]
            random.shuffle(docs)

            d = {"title": [], "sentences": []}

            d["title"].append(["placeholder_title"] * (num_distract + 1))
            d["sentences"].append(docs)
            datapt["context"] = d
            datapt["oracle_context"] = chunk

            # add answer to q
            datapt["cot_answer"] = self.generate_label(q, chunk)

            # construct model instruction
            context = ""
            for doc in docs:
                context += "<DOCUMENT>" + str(doc) + "</DOCUMENT>\n"
            context += q
            datapt["instruction"] = context

            # add to dataset
            if not self.ds:
                # init ds
                datapt["id"] = [datapt["id"]]
                datapt["type"] = [datapt["type"]]
                datapt["question"] = [datapt["question"]]
                datapt["context"] = [datapt["context"]]
                datapt["oracle_context"] = [datapt["oracle_context"]]
                datapt["cot_answer"] = [datapt["cot_answer"]]
                datapt["instruction"] = [datapt["instruction"]]
                self.ds = Dataset.from_dict(datapt)
            else:
                self.ds = self.ds.add_item(datapt)

    defrun(self) -> Any:
"""Run the pipeline."""
        chunks = self.get_chunks(self.file_path, self.chunk_size)

        logger.info(f"Number of chunks created: {len(chunks)}")

        self.num_distract_docs = (
            min(self.num_distract_docs, len(chunks)) - 1
        )  # should be less than number of chunks/ nodes created

        for index, chunk in enumerate(chunks):
            logger.info(f"Processing chunk: {index}")
            self.add_chunk_to_dataset(
                chunks, chunk, self.num_questions_per_chunk, self.num_distract_docs
            )

        return self.ds

```
 |  
| --- | --- |  
###  strip_str [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raft_dataset/#llama_index.packs.raft_dataset.RAFTDatasetPack.strip_str "Permanent link")

```
strip_str(s) -> 

```

Helper function for helping format strings returned by GPT-4.
Source code in `llama-index-packs/llama-index-packs-raft-dataset/llama_index/packs/raft_dataset/base.py`  
| 
```
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
```
 | 
```
defstrip_str(self, s) -> str:
"""
    Helper function for helping format strings returned by GPT-4.
    """
    if s.startswith("assistant:"):  # Check if the string starts with 'assistant '
        s = s.replace("assistant:", "", 1)  # Replace the first occurrence

    start_index, end_index = 0, len(s) - 1
    beg_found = False
    for i in range(len(s)):
        if s[i].isalpha():
            if not beg_found:
                start_index = i
                beg_found = True
            else:
                end_index = i
    end_index += 2
    return s[start_index : min(end_index, len(s))]

```
 |  
| --- | --- |  
###  encode_question_gen [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raft_dataset/#llama_index.packs.raft_dataset.RAFTDatasetPack.encode_question_gen "Permanent link")

```
encode_question_gen(question, chunk) -> []

```

Encode multiple prompt instructions into a single string for the general case.
Source code in `llama-index-packs/llama-index-packs-raft-dataset/llama_index/packs/raft_dataset/base.py`  
| 
```
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
```
 | 
```
defencode_question_gen(self, question, chunk) -> List[str]:
"""
    Encode multiple prompt instructions into a single string for the general case.
    """
    prompt = f"""
        Question: {question}\nContext: {chunk}\n
        Answer this question using the information given in the context above. Here is things to pay attention to:
        - First provide step-by-step reasoning on how to answer the question.
        - In the reasoning, if you need to copy paste some sentences from the context, include them in ##begin_quote## and ##end_quote##. This would mean that things outside of ##begin_quote## and ##end_quote## are not directly copy paste from the context.
        - End your response with final answer in the form <ANSWER>: $answer, the answer should be succinct.
    """
    return [
        ChatMessage(
            role="system",
            content="You are a helpful question answerer who can provide an answer given a question and relevant context.",
        ),
        ChatMessage(role="user", content=prompt),
    ]

```
 |  
| --- | --- |  
###  generate_label [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raft_dataset/#llama_index.packs.raft_dataset.RAFTDatasetPack.generate_label "Permanent link")

```
generate_label(question, context) -> 

```

Generates the label / answer to `question` using `context` and GPT-4.
Source code in `llama-index-packs/llama-index-packs-raft-dataset/llama_index/packs/raft_dataset/base.py`  
| 
```
90
91
92
93
94
95
96
```
 | 
```
defgenerate_label(self, question, context) -> str:
"""
    Generates the label / answer to `question` using `context` and GPT-4.
    """
    question_messages = self.encode_question_gen(question, context)
    response = self.llm.chat(question_messages)
    return str(response)

```
 |  
| --- | --- |  
###  generate_instructions_gen [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raft_dataset/#llama_index.packs.raft_dataset.RAFTDatasetPack.generate_instructions_gen "Permanent link")

```
generate_instructions_gen(chunk, x=5) -> []

```

Generates `x` questions / use cases for `chunk`. Used when the input document is of general types `pdf`, `json`, or `txt`.
Source code in `llama-index-packs/llama-index-packs-raft-dataset/llama_index/packs/raft_dataset/base.py`  
| 
```
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
```
 | 
```
defgenerate_instructions_gen(self, chunk, x=5) -> List[str]:
"""
    Generates `x` questions / use cases for `chunk`. Used when the input document is of general types
    `pdf`, `json`, or `txt`.
    """
    messages = [
        ChatMessage(
            role="system",
            content="You are a synthetic question-answer pair generator. Given a chunk of context about some topic(s), generate %s example questions a user could ask and would be answered using information from the chunk. For example, if the given context was a Wikipedia paragraph about the United States, an example question could be 'How many states are in the United States?'. The questions should be able to be answered in a few words or less."
            % (x),
        ),
        ChatMessage(role="user", content=str(chunk)),
    ]

    queries = str(self.llm.chat(messages)).split("\n")
    questions = [self.strip_str(q) for q in queries]
    questions = [q for q in questions if any(c.isalpha() for c in q)][:x]

    num_questions_generated = len(questions)
    if num_questions_generated  x:
        warnings.warn(
            f"Fewer questions generated ({num_questions_generated}) "
            f"than requested ({x})."
        )

    return questions

```
 |  
| --- | --- |  
###  get_chunks [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raft_dataset/#llama_index.packs.raft_dataset.RAFTDatasetPack.get_chunks "Permanent link")

```
get_chunks(file_path: , chunk_size: ) -> []

```

Takes in a `file_path`, retrieves the document, breaks it down into chunks of size `chunk_size`, and returns the chunks.
Source code in `llama-index-packs/llama-index-packs-raft-dataset/llama_index/packs/raft_dataset/base.py`  
| 
```
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
```
 | 
```
defget_chunks(self, file_path: str, chunk_size: int) -> List[str]:
"""
    Takes in a `file_path`, retrieves the document, breaks it down into chunks of size
    `chunk_size`, and returns the chunks.
    """
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    splitter = SemanticSplitterNodeParser(
        buffer_size=1,
        breakpoint_percentile_threshold=self.default_breakpoint_percentile_threshold,
        embed_model=self.embed_model,
    )
    nodes = splitter.get_nodes_from_documents(documents)

    return [node.get_content() for node in nodes]

```
 |  
| --- | --- |  
###  add_chunk_to_dataset [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raft_dataset/#llama_index.packs.raft_dataset.RAFTDatasetPack.add_chunk_to_dataset "Permanent link")

```
add_chunk_to_dataset(
    chunks: ,
    chunk: ,
    x:  = 5,
    num_distract:  = 3,
    p: float = 1.0,
)

```

Given a chunk, create {Q, A, D} triplets and add them to the dataset.
Source code in `llama-index-packs/llama-index-packs-raft-dataset/llama_index/packs/raft_dataset/base.py`  
| 
```
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
```
 | 
```
defadd_chunk_to_dataset(
    self,
    chunks: List,
    chunk: str,
    x: int = 5,
    num_distract: int = 3,
    p: float = 1.0,
):
"""
    Given a chunk, create {Q, A, D} triplets and add them to the dataset.
    """
    i = chunks.index(chunk)
    qs = self.generate_instructions_gen(chunk, x)
    for q in qs:
        datapt = {
            "id": None,
            "type": None,
            "question": None,
            "context": None,
            "oracle_context": None,
            "cot_answer": None,
        }

        datapt["id"] = f"seed_task_{0ifnotself.dselseself.ds.num_rows}"
        datapt["type"] = "general"
        datapt["question"] = q

        # add distractor docs
        docs = [chunk]
        indices = list(range(len(chunks)))
        indices.remove(i)
        for j in random.sample(indices, num_distract):
            docs.append(chunks[j])
        # decides whether to add oracle document
        oracle = random.uniform(0, 1)  p
        if not oracle:
            docs[0] = chunks[random.sample(indices, 1)[0]]
        random.shuffle(docs)

        d = {"title": [], "sentences": []}

        d["title"].append(["placeholder_title"] * (num_distract + 1))
        d["sentences"].append(docs)
        datapt["context"] = d
        datapt["oracle_context"] = chunk

        # add answer to q
        datapt["cot_answer"] = self.generate_label(q, chunk)

        # construct model instruction
        context = ""
        for doc in docs:
            context += "<DOCUMENT>" + str(doc) + "</DOCUMENT>\n"
        context += q
        datapt["instruction"] = context

        # add to dataset
        if not self.ds:
            # init ds
            datapt["id"] = [datapt["id"]]
            datapt["type"] = [datapt["type"]]
            datapt["question"] = [datapt["question"]]
            datapt["context"] = [datapt["context"]]
            datapt["oracle_context"] = [datapt["oracle_context"]]
            datapt["cot_answer"] = [datapt["cot_answer"]]
            datapt["instruction"] = [datapt["instruction"]]
            self.ds = Dataset.from_dict(datapt)
        else:
            self.ds = self.ds.add_item(datapt)

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/raft_dataset/#llama_index.packs.raft_dataset.RAFTDatasetPack.run "Permanent link")

```
run() -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-raft-dataset/llama_index/packs/raft_dataset/base.py`  
| 
```
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
```
 | 
```
defrun(self) -> Any:
"""Run the pipeline."""
    chunks = self.get_chunks(self.file_path, self.chunk_size)

    logger.info(f"Number of chunks created: {len(chunks)}")

    self.num_distract_docs = (
        min(self.num_distract_docs, len(chunks)) - 1
    )  # should be less than number of chunks/ nodes created

    for index, chunk in enumerate(chunks):
        logger.info(f"Processing chunk: {index}")
        self.add_chunk_to_dataset(
            chunks, chunk, self.num_questions_per_chunk, self.num_distract_docs
        )

    return self.ds

```
 |  
| --- | --- |  
options: members: - RAFTDatasetPack
