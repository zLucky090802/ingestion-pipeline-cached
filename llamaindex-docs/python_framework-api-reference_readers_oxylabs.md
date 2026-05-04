# Oxylabs
##  OxylabsAmazonSearchReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oxylabs/#llama_index.readers.oxylabs.OxylabsAmazonSearchReader "Permanent link")
Bases: `OxylabsBaseReader`
Get data from the Amazon Search page.
https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/search
Source code in `llama-index-integrations/readers/llama-index-readers-oxylabs/llama_index/readers/oxylabs/amazon_search.py`  
| 
```
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
```
 | 
```
classOxylabsAmazonSearchReader(OxylabsBaseReader):
"""
    Get data from the Amazon Search page.

    https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/search
    """

    top_level_header: str = "Search Results"

    def__init__(self, username: str, password: str, **data) -> None:
        super().__init__(username=username, password=password, **data)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsAmazonSearchReader"

    defget_response(self, payload: dict[str, Any]) -> Response:
        return self.oxylabs_api.amazon.scrape_search(**payload)

    async defaget_response(self, payload: dict[str, Any]) -> Response:
        return await self.async_oxylabs_api.amazon.scrape_search(**payload)

```
 |  
| --- | --- |  
##  OxylabsAmazonPricingReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oxylabs/#llama_index.readers.oxylabs.OxylabsAmazonPricingReader "Permanent link")
Bases: `OxylabsBaseReader`
Get data about Amazon product offer listings.
https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/pricing
Source code in `llama-index-integrations/readers/llama-index-readers-oxylabs/llama_index/readers/oxylabs/amazon_pricing.py`  
| 
```
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
```
 | 
```
classOxylabsAmazonPricingReader(OxylabsBaseReader):
"""
    Get data about Amazon product offer listings.

    https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/pricing
    """

    top_level_header: str = "Product pricing data"

    def__init__(self, username: str, password: str, **data) -> None:
        super().__init__(username=username, password=password, **data)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsAmazonPricingReader"

    defget_response(self, payload: dict[str, Any]) -> Response:
        return self.oxylabs_api.amazon.scrape_pricing(**payload)

    async defaget_response(self, payload: dict[str, Any]) -> Response:
        return await self.async_oxylabs_api.amazon.scrape_pricing(**payload)

```
 |  
| --- | --- |  
##  OxylabsAmazonProductReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oxylabs/#llama_index.readers.oxylabs.OxylabsAmazonProductReader "Permanent link")
Bases: `OxylabsBaseReader`
Get data about Amazon product.
https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/product
Source code in `llama-index-integrations/readers/llama-index-readers-oxylabs/llama_index/readers/oxylabs/amazon_product.py`  
| 
```
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
```
 | 
```
classOxylabsAmazonProductReader(OxylabsBaseReader):
"""
    Get data about Amazon product.

    https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/product
    """

    top_level_header: str = "Products"

    def__init__(self, username: str, password: str, **data) -> None:
        super().__init__(username=username, password=password, **data)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsAmazonProductReader"

    defget_response(self, payload: dict[str, Any]) -> Response:
        return self.oxylabs_api.amazon.scrape_product(**payload)

    async defaget_response(self, payload: dict[str, Any]) -> Response:
        return await self.async_oxylabs_api.amazon.scrape_product(**payload)

```
 |  
| --- | --- |  
##  OxylabsAmazonSellersReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oxylabs/#llama_index.readers.oxylabs.OxylabsAmazonSellersReader "Permanent link")
Bases: `OxylabsBaseReader`
Get data about Amazon merchants.
https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/sellers
Source code in `llama-index-integrations/readers/llama-index-readers-oxylabs/llama_index/readers/oxylabs/amazon_sellers.py`  
| 
```
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
```
 | 
```
classOxylabsAmazonSellersReader(OxylabsBaseReader):
"""
    Get data about Amazon merchants.

    https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/sellers
    """

    top_level_header: str = "Sellers"

    def__init__(self, username: str, password: str, **data) -> None:
        super().__init__(username=username, password=password, **data)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsAmazonSellersReader"

    defget_response(self, payload: dict[str, Any]) -> Response:
        return self.oxylabs_api.amazon.scrape_sellers(**payload)

    async defaget_response(self, payload: dict[str, Any]) -> Response:
        return await self.async_oxylabs_api.amazon.scrape_sellers(**payload)

```
 |  
| --- | --- |  
##  OxylabsAmazonBestsellersReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oxylabs/#llama_index.readers.oxylabs.OxylabsAmazonBestsellersReader "Permanent link")
Bases: `OxylabsBaseReader`
Get data from Amazon Best Sellers pages.
https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/best-sellers
Source code in `llama-index-integrations/readers/llama-index-readers-oxylabs/llama_index/readers/oxylabs/amazon_bestsellers.py`  
| 
```
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
```
 | 
```
classOxylabsAmazonBestsellersReader(OxylabsBaseReader):
"""
    Get data from Amazon Best Sellers pages.

    https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/best-sellers
    """

    top_level_header: str = "Bestsellers"

    def__init__(self, username: str, password: str, **data) -> None:
        super().__init__(username=username, password=password, **data)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsAmazonBestsellersReader"

    defget_response(self, payload: dict[str, Any]) -> Response:
        return self.oxylabs_api.amazon.scrape_bestsellers(**payload)

    async defaget_response(self, payload: dict[str, Any]) -> Response:
        return await self.async_oxylabs_api.amazon.scrape_bestsellers(**payload)

```
 |  
| --- | --- |  
##  OxylabsAmazonReviewsReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oxylabs/#llama_index.readers.oxylabs.OxylabsAmazonReviewsReader "Permanent link")
Bases: `OxylabsBaseReader`
Get data about Amazon product reviews.
https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/reviews
Source code in `llama-index-integrations/readers/llama-index-readers-oxylabs/llama_index/readers/oxylabs/amazon_reviews.py`  
| 
```
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
```
 | 
```
classOxylabsAmazonReviewsReader(OxylabsBaseReader):
"""
    Get data about Amazon product reviews.

    https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/amazon/reviews
    """

    top_level_header: str = "Reviews"

    def__init__(self, username: str, password: str, **data) -> None:
        super().__init__(username=username, password=password, **data)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsAmazonReviewsReader"

    defget_response(self, payload: dict[str, Any]) -> Response:
        return self.oxylabs_api.amazon.scrape_reviews(**payload)

    async defaget_response(self, payload: dict[str, Any]) -> Response:
        return await self.async_oxylabs_api.amazon.scrape_reviews(**payload)

```
 |  
| --- | --- |  
##  OxylabsGoogleSearchReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oxylabs/#llama_index.readers.oxylabs.OxylabsGoogleSearchReader "Permanent link")
Bases: `OxylabsGoogleBaseReader`
Get Google Search results data.
https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/google/search/search
Source code in `llama-index-integrations/readers/llama-index-readers-oxylabs/llama_index/readers/oxylabs/google_search.py`  
| 
```
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
```
 | 
```
classOxylabsGoogleSearchReader(OxylabsGoogleBaseReader):
"""
    Get Google Search results data.

    https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/google/search/search
    """

    def__init__(self, username: str, password: str, **data) -> None:
        super().__init__(username=username, password=password, **data)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsGoogleSearchReader"

    defget_response(self, payload: dict[str, Any]) -> Response:
        return self.oxylabs_api.google.scrape_search(**payload)

    async defaget_response(self, payload: dict[str, Any]) -> Response:
        return await self.async_oxylabs_api.google.scrape_search(**payload)

```
 |  
| --- | --- |  
##  OxylabsGoogleAdsReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oxylabs/#llama_index.readers.oxylabs.OxylabsGoogleAdsReader "Permanent link")
Bases: `OxylabsGoogleBaseReader`
Get Google Search results data with paid ads.
https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/google/ads
Source code in `llama-index-integrations/readers/llama-index-readers-oxylabs/llama_index/readers/oxylabs/google_ads.py`  
| 
```
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
```
 | 
```
classOxylabsGoogleAdsReader(OxylabsGoogleBaseReader):
"""
    Get Google Search results data with paid ads.

    https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/google/ads
    """

    def__init__(self, username: str, password: str, **data) -> None:
        super().__init__(username=username, password=password, **data)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsGoogleAdsReader"

    defget_response(self, payload: dict[str, Any]) -> Response:
        return self.oxylabs_api.google.scrape_ads(**payload)

    async defaget_response(self, payload: dict[str, Any]) -> Response:
        return await self.async_oxylabs_api.google.scrape_ads(**payload)

```
 |  
| --- | --- |  
##  OxylabsYoutubeTranscriptReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/oxylabs/#llama_index.readers.oxylabs.OxylabsYoutubeTranscriptReader "Permanent link")
Bases: `OxylabsBaseReader`
Get YouTube video transcripts.
https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/youtube/youtube-transcript
Source code in `llama-index-integrations/readers/llama-index-readers-oxylabs/llama_index/readers/oxylabs/youtube_transcripts.py`  
| 
```
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
classOxylabsYoutubeTranscriptReader(OxylabsBaseReader):
"""
    Get YouTube video transcripts.

    https://developers.oxylabs.io/scraper-apis/web-scraper-api/targets/youtube/youtube-transcript
    """

    top_level_header: str = "YouTube video transcripts"

    def__init__(self, username: str, password: str, **data) -> None:
        super().__init__(username=username, password=password, **data)

    @classmethod
    defclass_name(cls) -> str:
        return "OxylabsYoutubeTranscriptReader"

    defget_response(self, payload: dict[str, Any]) -> Response:
        return self.oxylabs_api.youtube_transcript.scrape_transcript(**payload)

    async defaget_response(self, payload: dict[str, Any]) -> Response:
        return await self.async_oxylabs_api.youtube_transcript.scrape_transcript(
            **payload
        )

```
 |  
| --- | --- |  
options: members: - OxylabsBaseReader - OxylabsAmazonSearchReader - OxylabsAmazonPricingReader - OxylabsAmazonProductReader - OxylabsAmazonSellersReader - OxylabsAmazonBestsellersReader - OxylabsAmazonReviewsReader - OxylabsGoogleSearchReader - OxylabsGoogleAdsReader - OxylabsYoutubeTranscriptReader
