# Self rag
##  SelfRAGQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/self_rag/#llama_index.packs.self_rag.SelfRAGQueryEngine "Permanent link")
Bases: 
Simple short form self RAG query engine.
Source code in `llama-index-packs/llama-index-packs-self-rag/llama_index/packs/self_rag/base.py`  
| 
```
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
289
290
291
```
 | 
```
classSelfRAGQueryEngine(CustomQueryEngine):
"""Simple short form self RAG query engine."""

    llm: Any = Field(default=None, description="llm")
    retriever: BaseRetriever = Field(default=None, description="retriever")
    generate_kwargs: Dict = Field(default=None, description="llm generation arguments")
    verbose: bool = Field(default=True, description="Verbose.")

    def__init__(
        self,
        model_path: str,
        retriever: BaseRetriever,
        verbose: bool = False,
        model_kwargs: Dict = None,
        generate_kwargs: Dict = None,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        super().__init__(verbose=verbose, **kwargs)
        model_kwargs = model_kwargs or _MODEL_KWARGS
        self.generate_kwargs = generate_kwargs or _GENERATE_KWARGS
        try:
            fromllama_cppimport Llama
        except ImportError:
            raise ImportError(_IMPORT_ERROR_MSG)
        self.llm = Llama(model_path=model_path, verbose=verbose, **model_kwargs)
        self.retriever = retriever

    def_run_critic(self, paragraphs: List[str]) -> CriticOutput:
"""
        Run Critic component, the llm will generate responses based on the paragraphs and then evaluate them.

        Args:
            paragraphs (List[str]): List of paragraphs to evaluate

        Returns:
            CriticOutput: Paragraphs final score, LLM predictions and source nodes

        """
        paragraphs_final_score = {}
        llm_response_text = {}
        source_nodes = []

        for p_idx, paragraph in enumerate(paragraphs):
            pred = self.llm(paragraph, **self.generate_kwargs)
            # Cache llm answer
            llm_response_text[p_idx] = pred["choices"][0]["text"]

            logprobs = pred["choices"][0]["logprobs"]
            pred_log_probs = logprobs["top_logprobs"]
            # Compute isRel score, on the first predicted token
            isRel_score = _relevance_score(pred_log_probs[0])

            # Compute isSup score
            isSup_score = _is_supported_score(logprobs["tokens"], pred_log_probs)

            # Compute isUse score
            isUse_score = _is_useful_score(logprobs["tokens"], pred_log_probs)

            paragraphs_final_score[p_idx] = (
                isRel_score + isSup_score + 0.5 * isUse_score
            )
            # Add the paragraph as source node with its relevance score
            source_nodes.append(
                NodeWithScore(
                    node=TextNode(text=paragraph, id_=str(p_idx)),
                    score=isRel_score,
                )
            )

            if self.verbose:
                print_text(
                    f"Input: {paragraph}\nPrediction: {llm_response_text[p_idx]}\nScore: {paragraphs_final_score[p_idx]}\n",
                    color="blue",
                )
                print_text(
                    f"{p_idx+1}/{len(paragraphs)} paragraphs done\n\n", color="blue"
                )

        return CriticOutput(llm_response_text, paragraphs_final_score, source_nodes)

    defcustom_query(self, query_str: str) -> Response:
"""Run self-RAG."""
        response = self.llm(prompt=_format_prompt(query_str), **_GENERATE_KWARGS)
        answer = response["choices"][0]["text"]
        source_nodes = []

        if "[Retrieval]" in answer:
            if self.verbose:
                print_text("Retrieval required\n", color="blue")
            documents = self.retriever.retrieve(query_str)
            if self.verbose:
                print_text(f"Received: {len(documents)} documents\n", color="blue")
            paragraphs = [
                _format_prompt(query_str, document.node.text) for document in documents
            ]

            if self.verbose:
                print_text("Start evaluation\n", color="blue")

            critic_output = self._run_critic(paragraphs)

            paragraphs_final_score = critic_output.paragraphs_final_score
            llm_response_per_paragraph = critic_output.llm_response_per_paragraph
            source_nodes = critic_output.source_nodes

            if self.verbose:
                print_text("End evaluation\n", color="blue")

            best_paragraph_id = max(
                paragraphs_final_score, key=paragraphs_final_score.get
            )
            answer = llm_response_per_paragraph[best_paragraph_id]
            if self.verbose:
                print_text(f"Selected the best answer: {answer}\n", color="blue")

        answer = _postprocess_answer(answer)
        if self.verbose:
            print_text(f"Final answer: {answer}\n", color="green")
        return Response(response=str(answer), source_nodes=source_nodes)

```
 |  
| --- | --- |  
###  custom_query [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/self_rag/#llama_index.packs.self_rag.SelfRAGQueryEngine.custom_query "Permanent link")

```
custom_query(query_str: ) -> 

```

Run self-RAG.
Source code in `llama-index-packs/llama-index-packs-self-rag/llama_index/packs/self_rag/base.py`  
| 
```
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
289
290
291
```
 | 
```
defcustom_query(self, query_str: str) -> Response:
"""Run self-RAG."""
    response = self.llm(prompt=_format_prompt(query_str), **_GENERATE_KWARGS)
    answer = response["choices"][0]["text"]
    source_nodes = []

    if "[Retrieval]" in answer:
        if self.verbose:
            print_text("Retrieval required\n", color="blue")
        documents = self.retriever.retrieve(query_str)
        if self.verbose:
            print_text(f"Received: {len(documents)} documents\n", color="blue")
        paragraphs = [
            _format_prompt(query_str, document.node.text) for document in documents
        ]

        if self.verbose:
            print_text("Start evaluation\n", color="blue")

        critic_output = self._run_critic(paragraphs)

        paragraphs_final_score = critic_output.paragraphs_final_score
        llm_response_per_paragraph = critic_output.llm_response_per_paragraph
        source_nodes = critic_output.source_nodes

        if self.verbose:
            print_text("End evaluation\n", color="blue")

        best_paragraph_id = max(
            paragraphs_final_score, key=paragraphs_final_score.get
        )
        answer = llm_response_per_paragraph[best_paragraph_id]
        if self.verbose:
            print_text(f"Selected the best answer: {answer}\n", color="blue")

    answer = _postprocess_answer(answer)
    if self.verbose:
        print_text(f"Final answer: {answer}\n", color="green")
    return Response(response=str(answer), source_nodes=source_nodes)

```
 |  
| --- | --- |  
##  SelfRAGPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/self_rag/#llama_index.packs.self_rag.SelfRAGPack "Permanent link")
Bases: 
Simple short form Self-RAG pack.
Source code in `llama-index-packs/llama-index-packs-self-rag/llama_index/packs/self_rag/base.py`  
| 
```
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
```
 | 
```
classSelfRAGPack(BaseLlamaPack):
"""Simple short form Self-RAG pack."""

    def__init__(
        self,
        model_path: str,
        retriever: BaseRetriever,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        self.query_engine = SelfRAGQueryEngine(model_path, retriever, verbose)

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "query_engine": self.query_engine,
            "llm": self.query_engine.llm,
            "retriever": self.query_engine.retriever,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/self_rag/#llama_index.packs.self_rag.SelfRAGPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-self-rag/llama_index/packs/self_rag/base.py`  
| 
```
307
308
309
310
311
312
313
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "query_engine": self.query_engine,
        "llm": self.query_engine.llm,
        "retriever": self.query_engine.retriever,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/self_rag/#llama_index.packs.self_rag.SelfRAGPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-self-rag/llama_index/packs/self_rag/base.py`  
| 
```
315
316
317
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.query_engine.query(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - SelfRAGPack
