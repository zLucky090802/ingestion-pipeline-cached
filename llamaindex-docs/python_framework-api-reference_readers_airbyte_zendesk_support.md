# Airbyte zendesk support
##  AirbyteZendeskSupportReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/airbyte_zendesk_support/#llama_index.readers.airbyte_zendesk_support.AirbyteZendeskSupportReader "Permanent link")
Bases: 
AirbyteZendeskSupportReader reader.
Retrieve documents from ZendeskSupport
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |  `Mapping[str, Any]`  |  The config object for the zendesk_support source.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-airbyte-zendesk-support/llama_index/readers/airbyte_zendesk_support/base.py`  
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
classAirbyteZendeskSupportReader(AirbyteCDKReader):
"""
    AirbyteZendeskSupportReader reader.

    Retrieve documents from ZendeskSupport

    Args:
        config: The config object for the zendesk_support source.

    """

    def__init__(
        self,
        config: Mapping[str, Any],
        record_handler: Optional[RecordHandler] = None,
    ) -> None:
"""Initialize with parameters."""
        importsource_zendesk_support

        super().__init__(
            source_class=source_zendesk_support.SourceZendeskSupport,
            config=config,
            record_handler=record_handler,
        )

```
 |  
| --- | --- |  
options: members: - AirbyteZendeskSupportReader
