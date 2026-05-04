# Azure translate
##  AzureTranslateToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/azure_translate/#llama_index.tools.azure_translate.AzureTranslateToolSpec "Permanent link")
Bases: 
Azure Translate tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-azure-translate/llama_index/tools/azure_translate/base.py`  
| 
```
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
30
31
32
33
34
35
36
37
38
```
 | 
```
classAzureTranslateToolSpec(BaseToolSpec):
"""Azure Translate tool spec."""

    spec_functions = ["translate"]

    def__init__(self, api_key: str, region: str) -> None:
"""Initialize with parameters."""
        self.headers = {
            "Ocp-Apim-Subscription-Key": api_key,
            "Ocp-Apim-Subscription-Region": region,
            "Content-type": "application/json",
        }

    deftranslate(self, text: str, language: str):
"""
        Use this tool to translate text from one language to another.
        The source language will be automatically detected. You need to specify the target language
        using a two character language code.

        Args:
            language (str): Target translation language.

        """
        request = requests.post(
            ENDPOINT_BASE_URL,
            params={"api-version": "3.0", "to": language},
            headers=self.headers,
            json=[{"text": text}],
        )
        return request.json()

```
 |  
| --- | --- |  
###  translate [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/azure_translate/#llama_index.tools.azure_translate.AzureTranslateToolSpec.translate "Permanent link")

```
translate(text: , language: )

```

Use this tool to translate text from one language to another. The source language will be automatically detected. You need to specify the target language using a two character language code.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `language`  |  Target translation language.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-azure-translate/llama_index/tools/azure_translate/base.py`  
| 
```
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
```
 | 
```
deftranslate(self, text: str, language: str):
"""
    Use this tool to translate text from one language to another.
    The source language will be automatically detected. You need to specify the target language
    using a two character language code.

    Args:
        language (str): Target translation language.

    """
    request = requests.post(
        ENDPOINT_BASE_URL,
        params={"api-version": "3.0", "to": language},
        headers=self.headers,
        json=[{"text": text}],
    )
    return request.json()

```
 |  
| --- | --- |  
options: members: - AzureTranslateToolSpec
