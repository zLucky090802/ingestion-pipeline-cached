[Skip to content](https://developers.llamaindex.ai/llamaparse/#_top)
Guide
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# LlamaParse Platform Quickstart
Install the SDK, get an API key, and run your first call against Parse, Extract, Classify, Split, Sheets, or Index — all from one platform.
**Build document agents powered by agentic OCR.**
LlamaParse is the enterprise platform for turning documents into production AI pipelines. One API key, one SDK, and six composable products: **Parse** (agentic OCR), **Extract** (structured data), **Classify** , **Split** , **Sheets** , and **Index**.
## Install
[Section titled “Install”](https://developers.llamaindex.ai/llamaparse/#install)


Terminal window
```


pipinstallllama-cloud=2.1


```

Terminal window
```


npminstall@llamaindex/llama-cloud


```

Set your API key:
Terminal window
```


export LLAMA_CLOUD_API_KEY=llx-...


```

[Get an API key](https://developers.llamaindex.ai/llamaparse/general/api_key) from the [LlamaCloud dashboard](https://cloud.llamaindex.ai/).
## Which product do I want?
[Section titled “Which product do I want?”](https://developers.llamaindex.ai/llamaparse/#which-product-do-i-want)
Map what you’re trying to do to the right product:  
| I want to…  | Use  |  
| --- | --- |  
| Turn PDFs, scans, or images into clean LLM-ready text  |   |  
| Pull structured JSON out of documents that matches my schema  |   |  
| Route documents into categories with natural-language rules  |   |  
| Split concatenated documents into their logical parts  |   |  
| Work with spreadsheet-like data and reason over rows  |   |  
| Build a hosted vector search pipeline for RAG  |   |  
| New here? Start with **Parse** —it’s the foundation most pipelines build on. Or scroll down for a runnable snippet in every product below.  |  
## Quick Start
[Section titled “Quick Start”](https://developers.llamaindex.ai/llamaparse/#quick-start)


Agentic OCR and parsing for 130+ formats. Turn PDFs and scans into LLM-ready text—the foundation for document agents.
Python TypeScript

```


from llama_cloud import LlamaCloud





client = LlamaCloud()  # Uses LLAMA_CLOUD_API_KEY env var




# Upload and parse a document



file= client.files.create(file="document.pdf", purpose="parse")




result = client.parsing.parse(




file_id=file.id,




tier="agentic",




version="latest",




expand=["markdown"],





# Get markdown output



print(result.markdown.pages[0].markdown)


```


```


import LlamaCloud from'@llamaindex/llama-cloud';




import fs from'fs';





constclient=newLlamaCloud(); // Uses LLAMA_CLOUD_API_KEY env var




// Upload and parse a document



constfile=await client.files.create({




file: fs.createReadStream('document.pdf'),




purpose: 'parse',





constresult=await client.parsing.parse({




file_id: file.id,




tier: 'agentic',




version: 'latest',




expand: ['markdown']





// Get markdown output



console.log(result.markdown.pages[0].markdown);


```

[Full Guide](https://developers.llamaindex.ai/llamaparse/parse/getting_started/) | [Examples](https://developers.llamaindex.ai/llamaparse/parse/examples/) | [Tiers & Pricing](https://developers.llamaindex.ai/llamaparse/parse/guides/tiers/)
Structured data from documents with custom schemas. Feed agents with clean entities, tables, and fields.
Python TypeScript

```


from pydantic import BaseModel, Field




from llama_cloud import LlamaCloud




# Define your schema



classResume(BaseModel):




name: str= Field(description="Full name of candidate")




email: str= Field(description="Email address")




skills: list[str] = Field(description="Technical skills")





client = LlamaCloud()




# Upload and extract



file= client.files.create(file="resume.pdf", purpose="extract")




job = client.extract.create(




document_input_value=file.id,




config={




"extract_options": {




"data_schema": Resume.model_json_schema(),




"tier": "agentic",







print(job.extract_result)


```


```


import LlamaCloud from'@llamaindex/llama-cloud';




import { z } from'zod';




import fs from'fs';




// Define your schema with Zod



constResumeSchema= z.object({




name: z.string().describe('Full name of candidate'),




email: z.string().describe('Email address'),




skills: z.array(z.string()).describe('Technical skills'),






constclient=newLlamaCloud();




// Upload and extract



constfile=await client.files.create({




file: fs.createReadStream('resume.pdf'),




purpose: 'extract',





let job =await client.extract.create({




document_input_value: file.id,




config: {




extract_options: {




data_schema: ResumeSchema,




tier: 'agentic',







console.log(job.extract_result);


```

[Full Guide](https://developers.llamaindex.ai/llamaparse/extract/sdk/) | [Examples](https://developers.llamaindex.ai/llamaparse/extract/examples/) | [Schema Design](https://developers.llamaindex.ai/llamaparse/extract/guides/schema_design/)
Categorize documents with natural-language rules. Pre-processing for extraction, parsing, or indexing.
Python TypeScript

```


from llama_cloud import LlamaCloud





client = LlamaCloud()




# Upload a document



file= client.files.create(file="document.pdf", purpose="classify")




# Classify with natural language rules



result = client.classifier.classify(




file_ids=[file.id],




rules=[





"type": "invoice",




"description": "Documents with invoice numbers, line items, and totals"






"type": "receipt",




"description": "Short POS receipts with merchant and total"






"type": "contract",




"description": "Legal agreements with terms and signatures"






mode="FAST"# or "MULTIMODAL" for visual docs






for item in result.items:




print(f"Type: {item.result.type}, Confidence: {item.result.confidence}")


```


```


import LlamaCloud from'@llamaindex/llama-cloud';




import fs from'fs';





constclient=newLlamaCloud();




// Upload a document



constfile=await client.files.create({




file: fs.createReadStream('document.pdf'),




purpose: 'classify',





// Classify with natural language rules



constresult=await client.classifier.classify({




file_ids: [file.id],




rules: [





type: 'invoice',




description: 'Documents with invoice numbers, line items, and totals',






type: 'receipt',




description: 'Short POS receipts with merchant and total',






type: 'contract',




description: 'Legal agreements with terms and signatures',






mode: 'FAST', // or 'MULTIMODAL' for visual docs






for (constitemof result.items) {




if (item.result) {




console.log(`Type: ${item.result.type}, Confidence: ${item.result.confidence}`);




```

[Full Guide](https://developers.llamaindex.ai/llamaparse/classify/sdk/) | [Examples](https://developers.llamaindex.ai/llamaparse/classify/examples/)
Segment concatenated PDFs into logical sections. AI-powered classification to split combined documents.
Python TypeScript

```


from llama_cloud import LlamaCloud





client = LlamaCloud()




# Upload a combined PDF



file= client.files.create(file="combined.pdf", purpose="split")




# Split into logical sections



result =await client.beta.split.split(




categories=[





"name": "invoice",




"description": "Commercial document with line items and totals"






"name": "contract",




"description": "Legal agreement with terms and signatures"






document_input={"type": "file_id", "value": file.id},






for segment in result.result.segments:




print(f"Pages {segment.pages}: {segment.category} ({segment.confidence_category})")


```


```


import LlamaCloud from'@llamaindex/llama-cloud';




import fs from'fs';





constclient=newLlamaCloud();




// Upload a combined PDF



constfile=await client.files.create({




file: fs.createReadStream('combined.pdf'),




purpose: 'split',





// Split into logical sections



constresult=await client.beta.split.split({




categories: [





name: 'invoice',




description: 'Commercial document with line items and totals',






name: 'contract',




description: 'Legal agreement with terms and signatures',






document_input: { type: 'file_id', value: file.id },






for (constsegmentof result.result.segments) {




console.log(`Pages ${segment.pages}: ${segment.category} (${segment.confidence_category})`);



```

[Full Guide](https://developers.llamaindex.ai/llamaparse/split/getting_started/) | [Examples](https://developers.llamaindex.ai/llamaparse/split/examples/)
Extract tables and metadata from messy spreadsheets. Output as Parquet files with rich cell metadata.
Python TypeScript

```


from llama_cloud import LlamaCloud





client = LlamaCloud()




# Upload a spreadsheet



file= client.files.create(file="spreadsheet.xlsx", purpose="parse")




# Extract tables and regions



result = client.beta.sheets.parse(




file_id=file.id,




config={"generate_additional_metadata": True},





# Print extracted regions



print(f"Found {len(result.regions)} regions")




for region in result.regions:




print(f"  - {region.region_id}: {region.title} ({region.location})")


```


```


import LlamaCloud from'@llamaindex/llama-cloud';




import fs from'fs';





constclient=newLlamaCloud();




// Upload a spreadsheet



constfile=await client.files.create({




file: fs.createReadStream('spreadsheet.xlsx'),




purpose: 'parse',





// Extract tables and regions



constresult=await client.beta.sheets.parse({




file_id: file.id,




config: { generate_additional_metadata: true },





// Print extracted regions



console.log(`Found ${result.regions?.length||0} regions`);




for (constregionof result.regions || []) {




console.log(`  - ${region.region_id}: ${region.title} (${region.location})`);



```

[Full Guide](https://developers.llamaindex.ai/llamaparse/sheets/) | [Examples](https://developers.llamaindex.ai/llamaparse/sheets/examples/coding_agent/)
Ingest, chunk, and embed into searchable indexes. Power RAG and retrieval for document agents. Index is designed for UI-first setup with SDK integration. Start in the LlamaCloud dashboard to create your index, then integrate:
Python TypeScript

```


from llama_cloud import LlamaCloud





client = LlamaCloud()  # Uses LLAMA_CLOUD_API_KEY env var




# Retrieve relevant nodes from the index



results = client.pipelines.retrieve(




pipeline_id="your-pipeline-id",




query="Your query here",




# -- Customize search behavior --




# dense_similarity_top_k=20,




# sparse_similarity_top_k=20,




# alpha=0.5,




# -- Control reranking behavior --




# enable_reranking=True,




# rerank_top_n=5,






forin results.retrieval_nodes:




print(f"Score: {n.score}, Text: {n.node.text}")


```


```


import LlamaCloud from'@llamaindex/llama-cloud';





constclient=newLlamaCloud(); // Uses LLAMA_CLOUD_API_KEY env var




// Retrieve relevant nodes from the index



constresults=await client.pipelines.retrieve('your-pipeline-id', {




query: 'Your query here',




// -- Customize search behavior --




// dense_similarity_top_k: 20,




// sparse_similarity_top_k: 20,




// alpha: 0.5,




// -- Control reranking behavior --




// enable_reranking: true,




// rerank_top_n: 5,






for (constnodeof results.retrieval_nodes || []) {




console.log(`Score: ${node.score}, Text: ${node.node?.text}`);



```

[Full Guide](https://developers.llamaindex.ai/llamaparse/cloud-index/getting_started/) | [Examples](https://developers.llamaindex.ai/llamaparse/cloud-index/examples/)
## LlamaParse Agent Skills
[Section titled “LlamaParse Agent Skills”](https://developers.llamaindex.ai/llamaparse/#llamaparse-agent-skills)
[Download Skills](https://github.com/run-llama/llamaparse-agent-skills/releases/download/latest/skills-latest.zip)
### Available Skills
[Section titled “Available Skills”](https://developers.llamaindex.ai/llamaparse/#available-skills)
  * **llamaparse** : Advanced parsing for PDFs, docs, presentations and images (charts, tables, embedded visuals). Requires `LLAMA_CLOUD_API_KEY` and Node 18+.
  * **liteparse** : Local-first, fast parsing for text-dense PDFs and docs. No API key needed, requires `@llamaindex/liteparse` globally installed and Node 18+.


### Installation
[Section titled “Installation”](https://developers.llamaindex.ai/llamaparse/#installation)
You can install LlamaParse Agent Skills using the [`skills`](https://skills.sh) CLI:
Terminal window
```


npxskillsaddrun-llama/llamaparse-agent-skills


```

Or, if you wish to download only one skill:
Terminal window
```


npxskillsaddrun-llama/llamaparse-agent-skills--skillllamaparse# or the name of another skill


```

You can also download the skills folder in `.zip` format from [GitHub Releases](https://github.com/run-llama/llamaparse-agent-skills/releases/download/latest/skills-latest.zip).
## Resources
[Section titled “Resources”](https://developers.llamaindex.ai/llamaparse/#resources)
[ Python SDK ](https://github.com/run-llama/llama-cloud-py) pip install llama-cloud
[ TypeScript SDK ](https://github.com/run-llama/llama-cloud-ts) npm install @llamaindex/llama-cloud
  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


