# Airbyte shopify
##  AirbyteShopifyReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/airbyte_shopify/#llama_index.readers.airbyte_shopify.AirbyteShopifyReader "Permanent link")
Bases: 
AirbyteShopifyReader reader.
Retrieve documents from Shopify
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |  `Mapping[str, Any]`  |  The config object for the shopify source.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-airbyte-shopify/llama_index/readers/airbyte_shopify/base.py`  
| 
```
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
```
 | 
```
classAirbyteShopifyReader(AirbyteCDKReader):
"""
    AirbyteShopifyReader reader.

    Retrieve documents from Shopify

    Args:
        config: The config object for the shopify source.

    """

    def__init__(
        self,
        config: Mapping[str, Any],
        record_handler: Optional[RecordHandler] = None,
    ) -> None:
"""Initialize with parameters."""
        importsource_shopify

        super().__init__(
            source_class=source_shopify.SourceShopify,
            config=config,
            record_handler=record_handler,
        )

```
 |  
| --- | --- |  
options: members: - AirbyteShopifyReader
