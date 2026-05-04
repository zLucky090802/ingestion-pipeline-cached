# Openai
##  OpenAIImageGenerationToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/openai/#llama_index.tools.openai.OpenAIImageGenerationToolSpec "Permanent link")
Bases: 
OpenAI Image Generation tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-openai/llama_index/tools/openai/image_generation/base.py`  
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
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
```
 | 
```
classOpenAIImageGenerationToolSpec(BaseToolSpec):
"""OpenAI Image Generation tool spec."""

    spec_functions = ["image_generation"]

    def__init__(
        self, api_key: Optional[str] = None, cache_dir: Optional[str] = None
    ) -> None:
        try:
            fromopenaiimport OpenAI
        except ImportError:
            raise ImportError(
                "Please install openai with `pip install openai` to use this tool"
            )

"""Initialize with parameters."""
        self.client = OpenAI(api_key=api_key)
        self.cache_dir = cache_dir or DEFAULT_CACHE_DIR

    defget_cache_dir(self):
        return self.cache_dir

    defsave_base64_image(self, base64_str, image_name):
        try:
            fromioimport BytesIO

            fromPILimport Image
        except ImportError:
            raise ImportError(
                "Please install Pillow with `pip install Pillow` to use this tool"
            )
        cache_dir = self.cache_dir

        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Decode the base64 string
        image_data = base64.b64decode(base64_str)

        # Create an image from the decoded bytes and save it
        image_path = os.path.join(cache_dir, image_name)
        with Image.open(BytesIO(image_data)) as img:
            img.save(image_path)

        return image_path

    defimage_generation(
        self,
        text: str,
        model: Optional[str] = "dall-e-3",
        quality: Optional[str] = "standard",
        num_images: Optional[int] = 1,
        size: Optional[str] = DEFAULT_SIZE,
        style: Optional[str] = "vivid",
        timeout: Optional[int] = None,
        download: Optional[bool] = False,
    ) -> str:
"""
        This tool accepts a natural language string and will use OpenAI's DALL-E model to generate an image.

        Args:
            text: The text to generate an image from.

            model: The model to use for image generation. Defaults to `dall-e-3`.
                Must be one of `dall-e-2` or `dall-e-3`.

            num_images: The number of images to generate. Defaults to 1.
                Must be between 1 and 10. For `dall-e-3`, only `n=1` is supported.

            quality: The quality of the image that will be generated. Defaults to `standard`.
                Must be one of `standard` or `hd`. `hd` creates images with finer
                details and greater consistency across the image. This param is only supported
                for `dall-e-3`.

            size: The size of the generated images. Defaults to `1024x1024`.
                Must be one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`.
                Must be one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3` models.

            style: The style of the generated images. Defaults to `vivid`.
                Must be one of `vivid` or `natural`.
                Vivid causes the model to lean towards generating hyper-real and dramatic images.
                Natural causes the model to produce more natural, less hyper-real looking images.
                This param is only supported for `dall-e-3`.

            timeout: Override the client-level default timeout for this request, in seconds. Defaults to `None`.

            download: If `True`, the image will be downloaded to the cache directory. Defaults to `True`.

        """
        if size not in valid_sizes[model]:
            raise Exception(f"Invalid size for {model}: {size}")

        response = self.client.images.generate(
            prompt=text,
            n=num_images,
            model=model,
            quality=quality,
            size=size,
            response_format="b64_json" if download else "url",
            style=style,
            timeout=timeout,
        )
        if download:
            image_bytes = response.data[0].b64_json
            ext = get_extension(image_bytes)
            filename = f"{time.time()}.{ext}"

            return (self.save_base64_image(image_bytes, filename),)

        return response.data[0].url

```
 |  
| --- | --- |  
###  image_generation [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/openai/#llama_index.tools.openai.OpenAIImageGenerationToolSpec.image_generation "Permanent link")

```
image_generation(
    text: ,
    model: Optional[] = "dall-e-3",
    quality: Optional[] = "standard",
    num_images: Optional[] = 1,
    size: Optional[] = DEFAULT_SIZE,
    style: Optional[] = "vivid",
    timeout: Optional[] = None,
    download: Optional[] = False,
) -> 

```

This tool accepts a natural language string and will use OpenAI's DALL-E model to generate an image.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `text`  |  The text to generate an image from.  |  _required_  |  
|  `model`  |  `Optional[str]`  |  The model to use for image generation. Defaults to `dall-e-3`. Must be one of `dall-e-2` or `dall-e-3`.  |  `'dall-e-3'`  |  
|  `num_images`  |  `Optional[int]`  |  The number of images to generate. Defaults to 1. Must be between 1 and 10. For `dall-e-3`, only `n=1` is supported.  |  
|  `quality`  |  `Optional[str]`  |  The quality of the image that will be generated. Defaults to `standard`. Must be one of `standard` or `hd`. `hd` creates images with finer details and greater consistency across the image. This param is only supported for `dall-e-3`.  |  `'standard'`  |  
|  `size`  |  `Optional[str]`  |  The size of the generated images. Defaults to `1024x1024`. Must be one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`. Must be one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3` models.  |  `DEFAULT_SIZE`  |  
|  `style`  |  `Optional[str]`  |  The style of the generated images. Defaults to `vivid`. Must be one of `vivid` or `natural`. Vivid causes the model to lean towards generating hyper-real and dramatic images. Natural causes the model to produce more natural, less hyper-real looking images. This param is only supported for `dall-e-3`.  |  `'vivid'`  |  
|  `timeout`  |  `Optional[int]`  |  Override the client-level default timeout for this request, in seconds. Defaults to `None`.  |  `None`  |  
|  `download`  |  `Optional[bool]`  |  If `True`, the image will be downloaded to the cache directory. Defaults to `True`.  |  `False`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-openai/llama_index/tools/openai/image_generation/base.py`  
| 
```
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
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
```
 | 
```
defimage_generation(
    self,
    text: str,
    model: Optional[str] = "dall-e-3",
    quality: Optional[str] = "standard",
    num_images: Optional[int] = 1,
    size: Optional[str] = DEFAULT_SIZE,
    style: Optional[str] = "vivid",
    timeout: Optional[int] = None,
    download: Optional[bool] = False,
) -> str:
"""
    This tool accepts a natural language string and will use OpenAI's DALL-E model to generate an image.

    Args:
        text: The text to generate an image from.

        model: The model to use for image generation. Defaults to `dall-e-3`.
            Must be one of `dall-e-2` or `dall-e-3`.

        num_images: The number of images to generate. Defaults to 1.
            Must be between 1 and 10. For `dall-e-3`, only `n=1` is supported.

        quality: The quality of the image that will be generated. Defaults to `standard`.
            Must be one of `standard` or `hd`. `hd` creates images with finer
            details and greater consistency across the image. This param is only supported
            for `dall-e-3`.

        size: The size of the generated images. Defaults to `1024x1024`.
            Must be one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`.
            Must be one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3` models.

        style: The style of the generated images. Defaults to `vivid`.
            Must be one of `vivid` or `natural`.
            Vivid causes the model to lean towards generating hyper-real and dramatic images.
            Natural causes the model to produce more natural, less hyper-real looking images.
            This param is only supported for `dall-e-3`.

        timeout: Override the client-level default timeout for this request, in seconds. Defaults to `None`.

        download: If `True`, the image will be downloaded to the cache directory. Defaults to `True`.

    """
    if size not in valid_sizes[model]:
        raise Exception(f"Invalid size for {model}: {size}")

    response = self.client.images.generate(
        prompt=text,
        n=num_images,
        model=model,
        quality=quality,
        size=size,
        response_format="b64_json" if download else "url",
        style=style,
        timeout=timeout,
    )
    if download:
        image_bytes = response.data[0].b64_json
        ext = get_extension(image_bytes)
        filename = f"{time.time()}.{ext}"

        return (self.save_base64_image(image_bytes, filename),)

    return response.data[0].url

```
 |  
| --- | --- |  
options: members: - OpenAIImageGenerationToolSpec
