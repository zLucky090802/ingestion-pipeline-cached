# Llama dataset metadata
##  LlamaDatasetMetadataPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/llama_dataset_metadata/#llama_index.packs.llama_dataset_metadata.LlamaDatasetMetadataPack "Permanent link")
Bases: 
A llamapack for creating and saving the necessary metadata files for submitting a llamadataset: card.json and README.md.
Source code in `llama-index-packs/llama-index-packs-llama-dataset-metadata/llama_index/packs/llama_dataset_metadata/base.py`  
| 
```
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
```
 | 
```
classLlamaDatasetMetadataPack(BaseLlamaPack):
"""
    A llamapack for creating and saving the necessary metadata files for
    submitting a llamadataset: card.json and README.md.
    """

    defrun(
        self,
        index: BaseIndex,
        benchmark_df: pd.DataFrame,
        rag_dataset: "LabelledRagDataset",
        name: str,
        description: str,
        baseline_name: str,
        source_urls: Optional[List[str]] = None,
        code_url: Optional[str] = None,
    ):
"""
        Main usage for a llamapack. This will build the card.json and README.md
        and save them to local disk.

        Args:
            index (BaseIndex): the index from which query_engine is derived and
                used in the rag evaluation.
            benchmark_df (pd.DataFrame): the benchmark dataframe after using
                RagEvaluatorPack
            rag_dataset (LabelledRagDataset): the LabelledRagDataset used for
                evaluations
            name (str): The name of the new dataset e.g., "Paul Graham Essay Dataset"
            baseline_name (str): The name of the baseline e.g., "llamaindex"
            description (str): The description of the new dataset.
            source_urls (Optional[List[str]], optional): _description_. Defaults to None.
            code_url (Optional[str], optional): _description_. Defaults to None.

        """
        readme_obj = Readme(name=name)
        card_obj = DatasetCard.from_rag_evaluation(
            index=index,
            benchmark_df=benchmark_df,
            rag_dataset=rag_dataset,
            name=name,
            description=description,
            baseline_name=baseline_name,
            source_urls=source_urls,
            code_url=code_url,
        )

        # save card.json
        with open("card.json", "w") as f:
            json.dump(card_obj.dict(by_alias=True), f)

        # save README.md
        with open("README.md", "w") as f:
            f.write(readme_obj.create_readme())

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/llama_dataset_metadata/#llama_index.packs.llama_dataset_metadata.LlamaDatasetMetadataPack.run "Permanent link")

```
run(
    index: ,
    benchmark_df: DataFrame,
    rag_dataset: ,
    name: ,
    description: ,
    baseline_name: ,
    source_urls: Optional[[]] = None,
    code_url: Optional[] = None,
)

```

Main usage for a llamapack. This will build the card.json and README.md and save them to local disk.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index`  |   |  the index from which query_engine is derived and used in the rag evaluation.  |  _required_  |  
|  `benchmark_df`  |  `DataFrame`  |  the benchmark dataframe after using RagEvaluatorPack  |  _required_  |  
|  `rag_dataset`  |   |  the LabelledRagDataset used for evaluations  |  _required_  |  
|  `name`  |  The name of the new dataset e.g., "Paul Graham Essay Dataset"  |  _required_  |  
|  `baseline_name`  |  The name of the baseline e.g., "llamaindex"  |  _required_  |  
|  `description`  |  The description of the new dataset.  |  _required_  |  
|  `source_urls`  |  `Optional[List[str]]`  |  _description_. Defaults to None.  |  `None`  |  
|  `code_url`  |  `Optional[str]`  |  _description_. Defaults to None.  |  `None`  |  
Source code in `llama-index-packs/llama-index-packs-llama-dataset-metadata/llama_index/packs/llama_dataset_metadata/base.py`  
| 
```
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
```
 | 
```
defrun(
    self,
    index: BaseIndex,
    benchmark_df: pd.DataFrame,
    rag_dataset: "LabelledRagDataset",
    name: str,
    description: str,
    baseline_name: str,
    source_urls: Optional[List[str]] = None,
    code_url: Optional[str] = None,
):
"""
    Main usage for a llamapack. This will build the card.json and README.md
    and save them to local disk.

    Args:
        index (BaseIndex): the index from which query_engine is derived and
            used in the rag evaluation.
        benchmark_df (pd.DataFrame): the benchmark dataframe after using
            RagEvaluatorPack
        rag_dataset (LabelledRagDataset): the LabelledRagDataset used for
            evaluations
        name (str): The name of the new dataset e.g., "Paul Graham Essay Dataset"
        baseline_name (str): The name of the baseline e.g., "llamaindex"
        description (str): The description of the new dataset.
        source_urls (Optional[List[str]], optional): _description_. Defaults to None.
        code_url (Optional[str], optional): _description_. Defaults to None.

    """
    readme_obj = Readme(name=name)
    card_obj = DatasetCard.from_rag_evaluation(
        index=index,
        benchmark_df=benchmark_df,
        rag_dataset=rag_dataset,
        name=name,
        description=description,
        baseline_name=baseline_name,
        source_urls=source_urls,
        code_url=code_url,
    )

    # save card.json
    with open("card.json", "w") as f:
        json.dump(card_obj.dict(by_alias=True), f)

    # save README.md
    with open("README.md", "w") as f:
        f.write(readme_obj.create_readme())

```
 |  
| --- | --- |  
options: members: - LlamaDatasetMetadataPack
