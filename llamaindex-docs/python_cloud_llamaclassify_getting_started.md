[Skip to content](https://developers.llamaindex.ai/llamaparse/classify/#_top)
Guide
Classify
[Overview of Classify](https://developers.llamaindex.ai/llamaparse/classify/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Overview of Classify
Learn what the Classification API is, how rules work, and how to run classifications using the client SDK.
Classify lets you automatically categorize documents into types you define (for example: invoice, receipt, contract) using natural-language rules.
Classify is currently in beta and is subject to breaking changes.
## Use Cases
[Section titled “Use Cases”](https://developers.llamaindex.ai/llamaparse/classify/#use-cases)
  * **Use as a pre-processing step**
    * **Before extraction** : Classify first, then run schema-specific extraction (e.g., invoice vs. contract) with different LlamaExtract agents to improve accuracy and reduce cost.
    * **Before parsing** : Classify first, then run LlamaParse over labeled files with finely tuned parse settings for each classified category to improve accuracy and reduce cost.
    * **Before indexing** : Classify first, then send classified files into appropriate LlamaCloud indices with tailored chunking, metadata, and access controls to improve retrieval quality.
  * **Intake routing for back-office documents** : Auto-separate invoices, receipts, purchase orders, and bank statements to the right queues, storage buckets, or approval workflows.
  * **Dataset curation** : Auto-tag large archives into meaningful categories to create labeled subsets for model training.


## Concepts
[Section titled “Concepts”](https://developers.llamaindex.ai/llamaparse/classify/#concepts)
  * **Rule** : A content-based criterion for a document type. Each rule has:
    * `type`: the label to assign. Must contain only alphanumeric characters, spaces, hyphens, and underscores. For example: “invoice”, “sec_filing”, “Tax Return”, “10-K”.
    * `description`: a natural-language description of the content that should match this type.
  * **Parsing configuration (optional)** : Controls how we parse documents before classification (e.g., language, page limits). Useful for speed/accuracy tradeoffs.
  * **Results** : For each file you get a `type` (predicted), `confidence` (0.0–1.0), and `reasoning` (step-by-step explanation).


## Classification Modes
[Section titled “Classification Modes”](https://developers.llamaindex.ai/llamaparse/classify/#classification-modes)
Classify offers two modes to balance speed, cost, and accuracy:  
| Mode  | Credits per Page  | Best For  |  
| --- | --- | --- |  
| **Fast**  | 1  | Text-heavy documents where layout and visual elements are not important  |  
| **Multimodal**  | 2  | Documents with hand-written text, images, charts, or visual content  |  
Fast mode uses text-based classification, making it cost-effective. It works well for documents where content, not layout, determines the type.
Multimodal mode uses vision models to analyze both text and visual elements in your documents. Use this mode if you need higher accuracy on visually rich documents.
To use Multimodal mode, set the `mode` parameter to `"MULTIMODAL"` when creating a classify job. See the [SDK guide](https://developers.llamaindex.ai/llamaparse/classify/sdk) for usage examples.
## Typical flow
[Section titled “Typical flow”](https://developers.llamaindex.ai/llamaparse/classify/#typical-flow)
  1. Upload your files to LlamaCloud
  2. Create rules for your target classes
  3. Create a classify job with the file ids and rules
  4. Fetch results and consume the predictions


## Next steps
[Section titled “Next steps”](https://developers.llamaindex.ai/llamaparse/classify/#next-steps)
  * Make sure you have an API key: [Get an API key](https://developers.llamaindex.ai/cloud/general/api_key)
  * Jump straight to the SDK guide to run your first job using [the SDK](https://developers.llamaindex.ai/llamaparse/classify/sdk)
  * For use with other languages, see our [API reference](https://developers.llamaindex.ai/reference/resources/classify/)


  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


