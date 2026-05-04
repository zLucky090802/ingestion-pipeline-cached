# Stripe docs
##  StripeDocsReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/stripe_docs/#llama_index.readers.stripe_docs.StripeDocsReader "Permanent link")
Bases: 
Asynchronous Stripe documentation reader.
Reads pages from the Stripe documentation based on the sitemap.xml.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `html_to_text`  |  `bool`  |  Whether to convert HTML to text.  |  `False`  |  
|  `limit`  |  Maximum number of concurrent requests.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-stripe-docs/llama_index/readers/stripe_docs/base.py`  
| 
```
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
```
 | 
```
classStripeDocsReader(BaseReader):
"""
    Asynchronous Stripe documentation reader.

    Reads pages from the Stripe documentation based on the sitemap.xml.

    Args:
        html_to_text (bool): Whether to convert HTML to text.
        limit (int): Maximum number of concurrent requests.

    """

    def__init__(self, html_to_text: bool = False, limit: int = 10) -> None:
        self._async_loader = AsyncWebPageReader(html_to_text=html_to_text, limit=limit)
        self._html_to_text = html_to_text
        self._limit = limit

    def_load_url(self, url: str) -> str:
        return urllib.request.urlopen(url).read()

    def_load_sitemap(self) -> str:
        return self._load_url(STRIPE_SITEMAP_URL)

    def_parse_sitemap(
        self, raw_sitemap: str, filters: List[str] = DEFAULT_FILTERS
    ) -> List:
        root_sitemap = fromstring(raw_sitemap)
        sitemap_partition_urls = []
        sitemap_urls = []

        for sitemap in root_sitemap.findall(f"{{{XML_SITEMAP_SCHEMA}}}sitemap"):
            loc = sitemap.find(f"{{{XML_SITEMAP_SCHEMA}}}loc").text
            sitemap_partition_urls.append(loc)

        for sitemap_partition_url in sitemap_partition_urls:
            sitemap_partition = fromstring(self._load_url(sitemap_partition_url))

            # Find all <url /> and iterate through them
            for url in sitemap_partition.findall(f"{{{XML_SITEMAP_SCHEMA}}}url"):
                loc = url.find(f"{{{XML_SITEMAP_SCHEMA}}}loc").text

                contains_filter = any(filter in loc for filter in filters)

                if contains_filter:
                    sitemap_urls.append(loc)

        return sitemap_urls

    defload_data(self, filters: List[str] = DEFAULT_FILTERS) -> List[Document]:
        sitemap = self._load_sitemap()
        sitemap_urls = self._parse_sitemap(sitemap, filters)

        return self._async_loader.load_data(urls=sitemap_urls)

```
 |  
| --- | --- |  
options: members: - StripeDocsReader
