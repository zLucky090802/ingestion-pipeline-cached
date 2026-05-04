# Text to image
##  TextToImageToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/text_to_image/#llama_index.tools.text_to_image.TextToImageToolSpec "Permanent link")
Bases: 
Text to Image tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-text-to-image/llama_index/tools/text_to_image/base.py`  
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
```
 | 
```
classTextToImageToolSpec(BaseToolSpec):
"""Text to Image tool spec."""

    spec_functions = ["generate_images", "show_images", "generate_image_variation"]

    def__init__(self, api_key: Optional[str] = None) -> None:
        if api_key:
            openai.api_key = api_key

    defgenerate_images(
        self, prompt: str, n: Optional[int] = 1, size: Optional[str] = "256x256"
    ) -> List[str]:
"""
        Pass a prompt to OpenAIs text to image API to produce an image from the supplied query.

        Args:
            prompt (str): The prompt to generate an image(s) based on
            n (int): The number of images to generate. Defaults to 1.
            size (str): The size of the image(s) to generate. Defaults to 256x256. Other accepted values are 1024x1024 and 512x512

        When handling the urls returned from this function, NEVER strip any parameters or try to modify the url, they are necessary for authorization to view the image

        """
        try:
            response = openai.Image.create(prompt=prompt, n=n, size=size)
            return [image["url"] for image in response["data"]]
        except openai.error.OpenAIError as e:
            return e.error

    defgenerate_image_variation(
        self, url: str, n: Optional[int] = 1, size: Optional[str] = "256x256"
    ) -> str:
"""
        Accepts the url of an image and uses OpenAIs api to generate a variation of the image.
        This tool can take smaller images and create higher resolution variations, or vice versa.

        When passing a url from "generate_images" ALWAYS pass the url exactly as it was returned from the function, including ALL query parameters
        args:
            url (str): The url of the image to create a variation of
            n (int): The number of images to generate. Defaults to 1.
            size (str): The size of the image(s) to generate. Defaults to 256x256. Other accepted values are 1024x1024 and 512x512
        """
        try:
            response = openai.Image.create_variation(
                image=BytesIO(requests.get(url).content).getvalue(), n=n, size=size
            )
            return [image["url"] for image in response["data"]]
        except openai.error.OpenAIError as e:
            return e.error

    defshow_images(self, urls: List[str]):
"""
        Use this function to display image(s) using pyplot and pillow. This works in a jupyter notebook.

        Args:
            urls (str): The url(s) of the image(s) to show

        """
        importmatplotlib.pyplotasplt
        fromPILimport Image

        for url in urls:
            plt.figure()
            plt.imshow(Image.open(BytesIO(requests.get(url).content)))
        return "images rendered successfully"

```
 |  
| --- | --- |  
###  generate_images [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/text_to_image/#llama_index.tools.text_to_image.TextToImageToolSpec.generate_images "Permanent link")

```
generate_images(
    prompt: ,
    n: Optional[] = 1,
    size: Optional[] = "256x256",
) -> []

```

Pass a prompt to OpenAIs text to image API to produce an image from the supplied query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt`  |  The prompt to generate an image(s) based on  |  _required_  |  
|  The number of images to generate. Defaults to 1.  |  
|  `size`  |  The size of the image(s) to generate. Defaults to 256x256. Other accepted values are 1024x1024 and 512x512  |  `'256x256'`  |  
When handling the urls returned from this function, NEVER strip any parameters or try to modify the url, they are necessary for authorization to view the image
Source code in `llama-index-integrations/tools/llama-index-tools-text-to-image/llama_index/tools/text_to_image/base.py`  
| 
```
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
defgenerate_images(
    self, prompt: str, n: Optional[int] = 1, size: Optional[str] = "256x256"
) -> List[str]:
"""
    Pass a prompt to OpenAIs text to image API to produce an image from the supplied query.

    Args:
        prompt (str): The prompt to generate an image(s) based on
        n (int): The number of images to generate. Defaults to 1.
        size (str): The size of the image(s) to generate. Defaults to 256x256. Other accepted values are 1024x1024 and 512x512

    When handling the urls returned from this function, NEVER strip any parameters or try to modify the url, they are necessary for authorization to view the image

    """
    try:
        response = openai.Image.create(prompt=prompt, n=n, size=size)
        return [image["url"] for image in response["data"]]
    except openai.error.OpenAIError as e:
        return e.error

```
 |  
| --- | --- |  
###  generate_image_variation [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/text_to_image/#llama_index.tools.text_to_image.TextToImageToolSpec.generate_image_variation "Permanent link")

```
generate_image_variation(
    url: ,
    n: Optional[] = 1,
    size: Optional[] = "256x256",
) -> 

```

Accepts the url of an image and uses OpenAIs api to generate a variation of the image. This tool can take smaller images and create higher resolution variations, or vice versa.
When passing a url from "generate_images" ALWAYS pass the url exactly as it was returned from the function, including ALL query parameters args: url (str): The url of the image to create a variation of n (int): The number of images to generate. Defaults to 1. size (str): The size of the image(s) to generate. Defaults to 256x256. Other accepted values are 1024x1024 and 512x512
Source code in `llama-index-integrations/tools/llama-index-tools-text-to-image/llama_index/tools/text_to_image/base.py`  
| 
```
40
41
42
43
44
45
46
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
```
 | 
```
defgenerate_image_variation(
    self, url: str, n: Optional[int] = 1, size: Optional[str] = "256x256"
) -> str:
"""
    Accepts the url of an image and uses OpenAIs api to generate a variation of the image.
    This tool can take smaller images and create higher resolution variations, or vice versa.

    When passing a url from "generate_images" ALWAYS pass the url exactly as it was returned from the function, including ALL query parameters
    args:
        url (str): The url of the image to create a variation of
        n (int): The number of images to generate. Defaults to 1.
        size (str): The size of the image(s) to generate. Defaults to 256x256. Other accepted values are 1024x1024 and 512x512
    """
    try:
        response = openai.Image.create_variation(
            image=BytesIO(requests.get(url).content).getvalue(), n=n, size=size
        )
        return [image["url"] for image in response["data"]]
    except openai.error.OpenAIError as e:
        return e.error

```
 |  
| --- | --- |  
###  show_images [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/text_to_image/#llama_index.tools.text_to_image.TextToImageToolSpec.show_images "Permanent link")

```
show_images(urls: [])

```

Use this function to display image(s) using pyplot and pillow. This works in a jupyter notebook.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `urls`  |  The url(s) of the image(s) to show  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-text-to-image/llama_index/tools/text_to_image/base.py`  
| 
```
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
```
 | 
```
defshow_images(self, urls: List[str]):
"""
    Use this function to display image(s) using pyplot and pillow. This works in a jupyter notebook.

    Args:
        urls (str): The url(s) of the image(s) to show

    """
    importmatplotlib.pyplotasplt
    fromPILimport Image

    for url in urls:
        plt.figure()
        plt.imshow(Image.open(BytesIO(requests.get(url).content)))
    return "images rendered successfully"

```
 |  
| --- | --- |  
options: members: - TextToImageToolSpec
