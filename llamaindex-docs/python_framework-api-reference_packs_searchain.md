# Searchain
##  SearChainPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/searchain/#llama_index.packs.searchain.SearChainPack "Permanent link")
Bases: 
Simple short form SearChain pack.
Source code in `llama-index-packs/llama-index-packs-searchain/llama_index/packs/searchain/base.py`  
| 
```
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
```
 | 
```
classSearChainPack(BaseLlamaPack):
"""Simple short form SearChain pack."""

    def__init__(
        self,
        data_path: str,
        dprtokenizer_path: str = "facebook/dpr-reader-multiset-base",  # download from https://huggingface.co/facebook/dpr-reader-multiset-base,
        dprmodel_path: str = "facebook/dpr-reader-multiset-base",  # download from https://huggingface.co/facebook/dpr-reader-multiset-base,
        crossencoder_name_or_path: str = "microsoft/MiniLM-L12-H384-uncased",  # down load from https://huggingface.co/microsoft/MiniLM-L12-H384-uncased,
        device: str = "cuda",
        **kwargs: Any,
    ) -> None:
"""Init params."""
        self.device = device
        self.crossencoder = CrossEncoder(crossencoder_name_or_path, device=self.device)
        self.documents = SimpleDirectoryReader(data_path).load_data()
        self.index = VectorStoreIndex.from_documents(self.documents)
        self.query_engine = self.index.as_query_engine()
        self.llm = OpenAI()

        self.dprtokenizer = DPRReaderTokenizer.from_pretrained(dprtokenizer_path)
        self.dprmodel = DPRReader.from_pretrained(dprmodel_path)
        self.dprmodel.eval()
        self.dprmodel.to(self.device)

    def_get_answer(self, query, texts, title):
        print("texts:" + texts)
        encoded_inputs = self.dprtokenizer(
            questions=[query],
            titles=[title],
            texts=[texts],
            return_tensors="pt",
            max_length=510,
        )
        outputs = self.dprmodel(**encoded_inputs.to(self.device))
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits
        relevance_logits = outputs.relevance_logits

        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()
        predict_answer_tokens = encoded_inputs.input_ids[
            0, answer_start_index : answer_end_index + 1
        ]
        answer = self.dprtokenizer.decode(predict_answer_tokens)
        return answer, relevance_logits

    def_ir(self, query, query_seen_list):
        flag_contibue_label = False
        query_list = query.split("\n")
        message = ""
        for idx in range(len(query_list)):
            query_item = query_list[idx]
            if "Query" in query_item and "]:" in query_item:
                temp = query_item.split("]")
                if len(temp)  2:
                    continue
                query_type = temp[0]
                query_item = temp[1]
                if ":" in query_item:
                    query_item = query_item[1:]
                if not _have_seen_or_not(
                    self.crossencoder, query_item, query_seen_list, query_type
                ):
                    now_reference = {}
                    query_seen_list.append(query_item)
                    response = str(self.query_engine.query(query_item))

                    answer, relevance_score = self._get_answer(
                        query=query_item, texts="", title=response
                    )
                    now_reference["query"] = query_item
                    now_reference["answer"] = answer
                    now_reference["reference"] = response
                    now_reference["ref_score"] = relevance_score
                    now_reference["idx"] = response

                    if "Unsolved" in query_type:
                        message = "[Unsolved Query]:{}<SEP>[Answer]:{}<SEP>[Reference]:{}<SEP>".format(
                            query_item, answer, response
                        )
                        flag_contibue_label = True
                        break
                    elif relevance_score  1.5:
                        answer_start_idx = idx + 1
                        predict_answer = ""
                        while answer_start_idx  len(query_list):
                            if "Answer" in query_list[answer_start_idx]:
                                predict_answer = query_list[answer_start_idx]
                                break
                            answer_start_idx += 1
                        match_label = _match_or_not(
                            prediction=predict_answer, ground_truth=answer
                        )
                        if match_label:
                            continue
                        else:
                            message = "[Query]:{}<SEP>[Answer]:{}<SEP>[Reference]:{}<SEP>".format(
                                query_item, answer, response
                            )
                            flag_contibue_label = True
                            break
        return message, flag_contibue_label, query_seen_list

    def_extract(self, message_keys_list):
        text = message_keys_list
        idx = len(text)
        while idx  0:
            idx = idx - 1
            item = text[idx]
            if item.role == "assistant" and "Final Content" in item.content:
                list_item = item.content.split("\n")
                for sp in list_item:
                    if "Final Content" in sp:
                        return item.content
        return "Sorry, I still cannot solve this question!"

    defexecute(self, data_path, start_idx):
        data = open(data_path)
        for k, example in enumerate(data):
            if k  start_idx:
                continue
            example = json.loads(example)
            q = example["question"]
            round_count = 0
            message_keys_list = [
                ChatMessage(
                    role="user",
                    content="""Construct a global reasoning chain for this complex [Question] : " {} " You should generate a query to the search engine based on what you already know at each step of the reasoning chain, starting with [Query]. If you know the answer for [Query], generate it starting with [Answer]. You can try to generate the final answer for the [Question] by referring to the [Query]-[Answer] pairs, starting with [Final Content]. If you don't know the answer, generate a query to search engine based on what you already know and do not know, starting with [Unsolved Query].
                        For example:
                        [Question]: "Where do greyhound buses that are in the birthplace of Spirit If...'s performer leave from? "
                        [Query 1]: Who is the performer of Spirit If... ?
                        If you don't know the answer:
                        [Unsolved Query]: Who is the performer of Spirit If... ?
                        If you know the answer:
                        [Answer 1]: The performer of Spirit If... is Kevin Drew.
                        [Query 2]: Where was Kevin Drew born?
                        If you don't know the answer:
                        [Unsolved Query]: Where was Kevin Drew born?
                        If you know the answer:
                        [Answer 2]: Toronto.
                        [Query 3]: Where do greyhound buses in Toronto leave from?
                        If you don't know the answer:
                        [Unsolved Query]: Where do greyhound buses in Toronto leave from?
                        If you know the answer:
                        [Answer 3]: Toronto Coach Terminal.
                        [Final Content]: The performer of Spirit If... is Kevin Drew [1]. Kevin Drew was born in Toronto [2]. Greyhound buses in Toronto leave from Toronto Coach Terminal [3]. So the final answer is Toronto Coach Terminal.

                        [Question]:"Which magazine was started first Arthur’s Magazine or First for Women?"
                        [Query 1]: When was Arthur’s Magazine started?
                        [Answer 1]: 1844.
                        [Query 2]: When was First for Women started?
                        [Answer 2]: 1989
                        [Final Content]: Arthur’s Magazine started in 1844 [1]. First for Women started in 1989 [2]. So Arthur’s Magazine was started first. So the answer is Arthur’s Magazi
                        [Question]: {}""".format(q, q),
                )
            ]
            feedback_answer = "continue"
            predict_answer = ""
            query_seen_list = []
            while round_count  5 and feedback_answer != "end":
                time.sleep(0.5)
                rsp = self.llm.chat(message_keys_list)
                round_count += 1
                input_str = str(rsp.message.content)
                message_keys_list.append(
                    ChatMessage(role="assistant", content=input_str)
                )
                predict_answer += input_str

                message, flag_contibue_label, query_seen_list = self._ir(
                    input_str, query_seen_list
                )
                if flag_contibue_label:
                    feedback = message
                else:
                    feedback = "end"

                if feedback == "end":
                    break
                # [Query]:xxxx<SEP>[Answer]:xxxx<SEP>[Reference]:xxxx<SEP>
                feedback_list = feedback.split("<SEP>")
                if "Unsolved Query" not in feedback:
                    new_prompt = """Reference: {} According to this Reference, the answer for "{}" should be "{}", you can change your answer based on the Reference and continue constructing the reasoning chain to give the final answer for [Question]:{}""".format(
                        feedback_list[0], feedback_list[1], q, feedback_list[2]
                    )
                else:
                    new_prompt = """Reference: {} According to this Reference, the answer for "{}" should be "{}", you can give your answer based on the Reference and continue constructing the reasoning chain to give the final answer for [Question]：{} """.format(
                        feedback_list[0], feedback_list[1], q, feedback_list[2]
                    )
                message_keys_list.append(ChatMessage(role="user", content=new_prompt))
            result = self._extract(message_keys_list)
            print(result)

        return -1

```
 |  
| --- | --- |  
options: members: - SearChainPack
