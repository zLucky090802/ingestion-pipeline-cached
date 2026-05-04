# Airbyte salesforce
##  AirbyteSalesforceReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/airbyte_salesforce/#llama_index.readers.airbyte_salesforce.AirbyteSalesforceReader "Permanent link")
Bases: 
AirbyteSalesforceReader reader.
Retrieve documents from Salesforce
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |  `Mapping[str, Any]`  |  The config object for the salesforce source.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-airbyte-salesforce/llama_index/readers/airbyte_salesforce/base.py`  
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
classAirbyteSalesforceReader(AirbyteCDKReader):
"""
    AirbyteSalesforceReader reader.

    Retrieve documents from Salesforce

    Args:
        config: The config object for the salesforce source.

    """

    def__init__(
        self,
        config: Mapping[str, Any],
        record_handler: Optional[RecordHandler] = None,
    ) -> None:
"""Initialize with parameters."""
        importsource_salesforce

        super().__init__(
            source_class=source_salesforce.SourceSalesforce,
            config=config,
            record_handler=record_handler,
        )

```
 |  
| --- | --- |  
options: members: - AirbyteSalesforceReader
