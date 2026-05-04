# Airbyte hubspot
##  AirbyteHubspotReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/airbyte_hubspot/#llama_index.readers.airbyte_hubspot.AirbyteHubspotReader "Permanent link")
Bases: 
AirbyteHubspotReader reader.
Retrieve documents from Hubspot
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |  `Mapping[str, Any]`  |  The config object for the hubspot source.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-airbyte-hubspot/llama_index/readers/airbyte_hubspot/base.py`  
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
classAirbyteHubspotReader(AirbyteCDKReader):
"""
    AirbyteHubspotReader reader.

    Retrieve documents from Hubspot

    Args:
        config: The config object for the hubspot source.

    """

    def__init__(
        self,
        config: Mapping[str, Any],
        record_handler: Optional[RecordHandler] = None,
    ) -> None:
"""Initialize with parameters."""
        importsource_hubspot

        super().__init__(
            source_class=source_hubspot.SourceHubspot,
            config=config,
            record_handler=record_handler,
        )

```
 |  
| --- | --- |  
options: members: - AirbyteHubspotReader
