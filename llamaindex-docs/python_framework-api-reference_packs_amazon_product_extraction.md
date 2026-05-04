# Amazon product extraction
##  AmazonProductExtractionPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/amazon_product_extraction/#llama_index.packs.amazon_product_extraction.AmazonProductExtractionPack "Permanent link")
Bases: 
Product extraction pack.
Given a website url of a product (e.g. Amazon page), screenshot it, and use GPT-4V to extract structured outputs.
Source code in `llama-index-packs/llama-index-packs-amazon-product-extraction/llama_index/packs/amazon_product_extraction/base.py`  
| 
```
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
```
 | 
```
classAmazonProductExtractionPack(BaseLlamaPack):
"""
    Product extraction pack.

    Given a website url of a product (e.g. Amazon page), screenshot it,
    and use GPT-4V to extract structured outputs.

    """

    def__init__(
        self,
        website_url: str,
        tmp_file_path: str = "./tmp.png",
        screenshot_width: int = 1200,
        screenshot_height: int = 800,
        prompt_template_str: str = DEFAULT_PROMPT_TEMPLATE_STR,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        self.website_url = website_url
        # download image to temporary file
        asyncio.get_event_loop().run_until_complete(
            _screenshot_page(
                website_url,
                tmp_file_path,
                width=screenshot_width,
                height=screenshot_height,
            )
        )

        # put your local directory here
        self.image_documents = SimpleDirectoryReader(
            input_files=[tmp_file_path]
        ).load_data()

        # initialize openai pydantic program
        self.openai_mm_llm = OpenAIMultiModal(
            model="gpt-4-vision-preview", max_new_tokens=1000
        )
        self.openai_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(Product),
            image_documents=self.image_documents,
            prompt_template_str=prompt_template_str,
            llm=self.openai_mm_llm,
            verbose=True,
        )

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {
            "openai_program": self.openai_program,
            "openai_mm_llm": self.openai_mm_llm,
            "image_documents": self.image_documents,
        }

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        return self.openai_program(*args, **kwargs)

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/amazon_product_extraction/#llama_index.packs.amazon_product_extraction.AmazonProductExtractionPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-amazon-product-extraction/llama_index/packs/amazon_product_extraction/base.py`  
| 
```
 94
 95
 96
 97
 98
 99
100
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {
        "openai_program": self.openai_program,
        "openai_mm_llm": self.openai_mm_llm,
        "image_documents": self.image_documents,
    }

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/amazon_product_extraction/#llama_index.packs.amazon_product_extraction.AmazonProductExtractionPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-amazon-product-extraction/llama_index/packs/amazon_product_extraction/base.py`  
| 
```
102
103
104
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    return self.openai_program(*args, **kwargs)

```
 |  
| --- | --- |  
options: members: - AmazonProductExtractionPack
