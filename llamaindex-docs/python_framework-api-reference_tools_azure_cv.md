# Azure cv
##  AzureCVToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/azure_cv/#llama_index.tools.azure_cv.AzureCVToolSpec "Permanent link")
Bases: 
Azure Cognitive Vision tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-azure-cv/llama_index/tools/azure_cv/base.py`  
| 
```
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
39
40
41
42
43
44
45
46
47
48
```
 | 
```
classAzureCVToolSpec(BaseToolSpec):
"""Azure Cognitive Vision tool spec."""

    spec_functions = ["process_image"]

    def__init__(
        self,
        resource: str,
        api_key: str,
        language: Optional[str] = "en",
        api_version: Optional[str] = "2023-04-01-preview",
    ) -> None:
"""Initialize with parameters."""
        self.api_key = api_key
        self.cv_url = CV_URL_TMPL.format(resource=resource)
        self.language = language
        self.api_version = api_version

    defprocess_image(self, url: str, features: List[str]):
"""
        This tool accepts an image url or file and can process and return a variety of text depending on the use case.
        You can use the features argument to configure what text you want returned.

        Args:
            url (str): The url for the image to caption
            features (List[str]): Instructions on how to process the image. Valid keys are tags, objects, read, caption

        """
        response = requests.post(
            f"{self.cv_url}?features={','.join(features)}&language={self.language}&api-version={self.api_version}",
            headers={"Ocp-Apim-Subscription-Key": self.api_key},
            json={"url": url},
        )
        response_json = response.json()
        if "read" in features:
            response_json["readResult"] = response_json["readResult"]["content"]

        return response_json

```
 |  
| --- | --- |  
###  process_image [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/azure_cv/#llama_index.tools.azure_cv.AzureCVToolSpec.process_image "Permanent link")

```
process_image(url: , features: [])

```

This tool accepts an image url or file and can process and return a variety of text depending on the use case. You can use the features argument to configure what text you want returned.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  The url for the image to caption  |  _required_  |  
|  `features`  |  `List[str]`  |  Instructions on how to process the image. Valid keys are tags, objects, read, caption  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-azure-cv/llama_index/tools/azure_cv/base.py`  
| 
```
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
39
40
41
42
43
44
45
46
47
48
```
 | 
```
defprocess_image(self, url: str, features: List[str]):
"""
    This tool accepts an image url or file and can process and return a variety of text depending on the use case.
    You can use the features argument to configure what text you want returned.

    Args:
        url (str): The url for the image to caption
        features (List[str]): Instructions on how to process the image. Valid keys are tags, objects, read, caption

    """
    response = requests.post(
        f"{self.cv_url}?features={','.join(features)}&language={self.language}&api-version={self.api_version}",
        headers={"Ocp-Apim-Subscription-Key": self.api_key},
        json={"url": url},
    )
    response_json = response.json()
    if "read" in features:
        response_json["readResult"] = response_json["readResult"]["content"]

    return response_json

```
 |  
| --- | --- |  
options: members: - AzureCVToolSpec
