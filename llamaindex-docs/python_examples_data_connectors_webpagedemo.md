[Skip to content](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#_top)
# Web Page Reader 
Demonstrates our web page reader.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


%pip install llama-index llama-index-readers-web


```


```


import logging




import sys





logging.basicConfig(stream=sys.stdout, level=logging.INFO)




logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


```

#### Using SimpleWebPageReader
[Section titled “Using SimpleWebPageReader”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-simplewebpagereader)

```


from llama_index.core import SummaryIndex




from llama_index.readers.web import SimpleWebPageReader




from IPython.display import Markdown, display




import os


```


```


# NOTE: the html_to_text=True option requires html2text to be installed


```


```


documents = SimpleWebPageReader(html_to_text=True).load_data(




["http://paulgraham.com/worked.html"]



```


```


documents[0]


```


```


index = SummaryIndex.from_documents(documents)


```


```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")


```


```


display(Markdown(f"<b>{response}</b>"))


```

# Using Spider Reader 🕷
[Section titled “Using Spider Reader 🕷”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-spider-reader)
[Spider](https://spider.cloud/?ref=llama_index) is the [fastest](https://github.com/spider-rs/spider/blob/main/benches/BENCHMARKS.md#benchmark-results) crawler. It converts any website into pure HTML, markdown, metadata or text while enabling you to crawl with custom actions using AI.
Spider allows you to use high performance proxies to prevent detection, caches AI actions, webhooks for crawling status, scheduled crawls etc…
**Prerequisites:** you need to have a Spider api key to use this loader. You can get one on [spider.cloud](https://spider.cloud).

```

# Scrape single URL



from llama_index.readers.web import SpiderWebReader





spider_reader = SpiderWebReader(




api_key="YOUR_API_KEY"# Get one at https://spider.cloud




mode="scrape",




# params={} # Optional parameters see more on https://spider.cloud/docs/api






documents = spider_reader.load_data(url="https://spider.cloud")




print(documents)


```


```

[Document(id_='54a6ecf3-b33e-41e9-8cec-48657aa2ed9b', embedding=None, metadata={'description': 'Collect data rapidly from any website. Seamlessly scrape websites and get data tailored for LLM workloads.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 101750, 'keywords': None, 'pathname': '/', 'resource_type': 'html', 'title': 'Spider - Fastest Web Crawler', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/index.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Spider - Fastest Web Crawler[Spider v1 Logo Spider ](/)[Pricing](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)The World\'s Fastest and Cheapest Crawler API==========View Demo* Basic* StreamingExample requestPythonCopy```import requests, osheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}json_data = {"limit":50,"url":"http://www.example.com"}response = requests.post(\'https://api.spider.cloud/crawl\',  headers=headers,  json=json_data)print(response.json())```Example ResponseUnmatched Speed----------### 5secs  ###To crawl 200 pages### 21x  ###Faster than FireCrawl### 150x  ###Faster than Apify Benchmarks displaying performance between Spider Cloud, Firecrawl, and Apify.[See framework benchmarks ](https://github.com/spider-rs/spider/blob/main/benches/BENCHMARKS.md)Foundations for Crawling Effectively----------### Leading in performance ###Spider is written in Rust and runs in full concurrency to achieve crawling dozens of pages in secs.### Optimal response format ###Get clean and formatted markdown, HTML, or text content for fine-tuning or training AI models.### Caching ###Further boost speed by caching repeated web page crawls.### Smart Mode ###Spider dynamically switches to Headless Chrome when it needs to.Beta### Scrape with AI ###Do custom browser scripting and data extraction using the latest AI models.### Best crawler for LLMs ###Don\'t let crawling and scraping be the highest latency in your LLM & AI agent stack.### Scrape with no headaches ###* Proxy rotations* Agent headers* Avoid anti-bot detections* Headless chrome* Markdown LLM Responses### The Fastest Web Crawler ###* Powered by [spider-rs](https://github.com/spider-rs/spider)* Do 20,000 pages in seconds* Full concurrency* Powerful and simple API* 5,000 requests per minute### Do more with AI ###* Custom browser scripting* Advanced data extraction* Data pipelines* Perfect for LLM and AI Agents* Accurate website labeling[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n')]

```

Crawl domain following all deeper subpages

```

# Crawl domain with deeper crawling following subpages



from llama_index.readers.web import SpiderWebReader





spider_reader = SpiderWebReader(




api_key="YOUR_API_KEY",




mode="crawl",




# params={} # Optional parameters see more on https://spider.cloud/docs/api






documents = spider_reader.load_data(url="https://spider.cloud")




print(documents)


```


```

[Document(id_='63f7ccbf-c6c8-4f69-80f7-f6763f761a39', embedding=None, metadata={'description': 'Our privacy policy and how it plays a part in the data collected.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 26647, 'keywords': None, 'pathname': '/privacy', 'resource_type': 'html', 'title': 'Privacy', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/privacy.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text="Privacy[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)Privacy Policy==========Learn about how we take privacy with the Spider project.[Spider](https://spider.cloud) offers a cutting-edge data scraping service with powerful AI capabilities. Our data collecting platform is designed to help users maximize the benefits of data collection while embracing the advancements in AI technology. With our innovative tools, we provide a seamless and fast interactive experience. This privacy policy details Spider's approach to product development, deployment, and usage, encompassing the Crawler, AI products, and features.[AI Development at Spider----------](#ai-development-at-spider)Spider leverages a robust combination of proprietary code, open-source frameworks, and synthetic datasets to train its cutting-edge products. To continuously improve our offerings, Spider may utilize inputs from user-generated prompts and content, obtained from trusted third-party providers. By harnessing this diverse data, Spider can deliver highly precise and pertinent recommendations to our valued users. While the foundational data crawling aspect of Spider is openly available on Github, the dashboard and AI components remain closed source. Spider respects all robots.txt files declared on websites allowing data to be extracted without harming the website.[Security, Privacy, and Trust----------](#security-privacy-and-trust)At Spider, our utmost priority is the development and implementation of Crawlers, AI technologies, and products that adhere to ethical, moral, and legal standards. We are dedicated to creating a secure and respectful environment for all users. Safeguarding user data and ensuring transparency in its usage are core principles we uphold. In line with this commitment, we provide the following important disclosures when utilizing our AI-related products:* Spider ensures comprehensive disclosure of features that utilize third-party AI platforms. To provide clarity, these integrations will be clearly indicated through distinct markers, designations, explanatory notes that appear when hovering, references to the underlying codebase, or any other suitable form of notification as determined by the system. Our commitment to transparency aims to keep users informed about the involvement of third-party AI platforms in our products.* We collect and use personal data as set forth in our [Privacy Policy](https://spider.cloud/privacy) which governs the collection and usage of personal data. If you choose to input personal data into our AI products, please be aware that such information may be processed through third-party AI providers. For any inquiries or concerns regarding data privacy, feel free to reach out to us at [Spider Help Github](https://github.com/orgs/spider-rs/discussions). We are here to assist you.* Except for user-generated prompts and/or content as inputs, Spider does not use customer data, including the code related to the use of Spider's deployment services, to train or finetune any models used.* We periodically review and update our policies and procedures in an effort to comply with applicable data protection regulations and industry standards.* We use reasonable measures designed to maintain the safety of users and avoid harm to people and the environment. Spider's design and development process includes considerations for ethical, security, and regulatory requirements with certain safeguards to prevent and report misuse or abuse.[Third-Party Service Providers----------](#third-party-service-providers)In providing AI products and services, we leverage various third-party providers in the AI space to enhance our services and capabilities, and will continue to do so for certain product features.This page will be updated from time to time with information about Spider's use of AI. The current list of third-party AI providers integrated into Spider is as follows:* [Anthropic](https://console.anthropic.com/legal/terms)* [Azure Cognitive Services](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy)* [Cohere](https://cohere.com/terms-of-use)* [ElevenLabs](https://elevenlabs.io/terms)* [Hugging Face](https://huggingface.co/terms-of-service)* [Meta AI](https://www.facebook.com/policies_center/)* [OpenAI](https://openai.com/policies)* [Pinecone](https://www.pinecone.io/terms)* [Replicate](https://replicate.com/terms)We prioritize the safety of our users and take appropriate measures to avoid harm both to individuals and the environment. Our design and development processes incorporate considerations for ethical practices, security protocols, and regulatory requirements, along with established safeguards to prevent and report any instances of misuse or abuse. We are committed to maintaining a secure and respectful environment and upholding responsible practices throughout our services.[Acceptable Use----------](#acceptable-use)Spider's products are intended to provide helpful and respectful responses to user prompts and queries while collecting data along the web. We don't allow the use of our Scraper or AI tools, products and services for the following usages:* Denial of Service Attacks* Illegal activity* Inauthentic, deceptive, or impersonation behavior* Any other use that would violate Spider's standard published policies, codes of conduct, or terms of service.Any violation of this Spider AI Policy or any Spider policies or terms of service may result in termination of use of services at Spider's sole discretion. We will review and update this Spider AI Policy so that it remains relevant and effective. If you have feedback or would like to report any concerns or issues related to the use of AI systems, please reach out to [support@spider.cloud](mailto:support@spider.cloud).[More Information----------](#more-information)To learn more about Spider's integration of AI capabilities into products and features, check out the following resources:* [Spider-Rust](https://github.com/spider-rs)* [Spider](/)* [About](/)[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='18e4d35d-ff48-4d00-b924-abab7a06fbec', embedding=None, metadata={'description': 'Learn how to crawl and scrape websites with the fastest web crawler built for the job.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 27058, 'keywords': None, 'pathname': '/guides', 'resource_type': 'html', 'title': 'Spider Guides', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/guides.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Spider Guides[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)Spider Guides==========Learn how to crawl and scrape websites easily.(4) Total Guides* [  Spider v1 Logo  Spider Platform  ----------  How to use the platform to collect data from the internet fast, affordable, and unblockable.  ](/guides/spider)* [  Spider v1 Logo  Spider API  ----------  How to use the Spider API to curate data from any source blazing fast. The most advanced crawler that handles all workloads of all sizes.  ](/guides/spider-api)* [  Spider v1 Logo  Extract Contacts  ----------  Get contact information from any website in real time with AI. The only way to accurately get dynamic information from websites.  ](/guides/pipelines-extract-contacts)* [  Spider v1 Logo  Website Archiving  ----------  The programmable time machine that can store pages and all assets for easy website archiving.  ](/guides/website-archiving)[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='b10c6402-bc35-4fec-b97c-fa30bde54ce8', embedding=None, metadata={'description': 'Complete reference documentation for the Spider API. Includes code snippets and examples for quickly getting started with the system.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 195426, 'keywords': None, 'pathname': '/docs/api', 'resource_type': 'html', 'title': 'Spider API Reference', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/docs*_*api.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Spider API Reference[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)API Reference==========The Spider API is based on REST. Our API is predictable, returns [JSON-encoded](http://www.json.org/) responses, uses standard HTTP response codes, authentication, and verbs. Set your API secret key in the `authorization` header to commence. You can use the `content-type` header with `application/json`, `application/xml`, `text/csv`, and `application/jsonl` for shaping the response.The Spider API supports multi domain actions. You can work with multiple domains per request by adding the urls comma separated.The Spider API differs for every account as we release new versions and tailor functionality. You can add `v1` before any path to pin to the version.Just getting started?----------Check out our [development quickstart](/guides/spider-api) guide.Not a developer?----------Use Spiders [no-code options or apps](/guides/spider) to get started with Spider and to do more with your Spider account no code required.Base UrlJSONCopy```https://api.spider.cloud```Crawl websites==========Start crawling a website(s) to collect resources.POST https://api.spider.cloud/crawlRequest body* url\xa0required\xa0string  ----------  The URI resource to crawl. This can be a comma split list for multiple urls.  Test Url* request\xa0string  ----------  The request type to perform. Possible values are `http`, `chrome`, and `smart`. Use `smart` to perform HTTP request by default until JavaScript rendering is needed for the HTML.  HTTP* limit\xa0number  ----------  The maximum amount of pages allowed to crawl per website. Remove the value or set it to 0 to crawl all pages.  Crawl Limit* depth\xa0number  ----------  The crawl limit for maximum depth. If zero, no limit will be applied.  Crawl DepthSet Example* cache\xa0boolean  ----------  Use HTTP caching for the crawl to speed up repeated runs.  Set Example* budget\xa0object  ----------  Object that has paths with a counter for limiting the amount of pages example `{"*":1}` for only crawling the root page. The wildcard matches all routes and you can set child paths preventing a depth level, example of limiting `{ "/docs/colors": 10, "/docs/": 100 }` which only allows a max of 100 pages if the route matches `/docs/:pathname` and only 10 pages if it matches `/docs/colors/:pathname`.  Crawl Budget  Set Example* locale\xa0string  ----------  The locale to use for request, example `en-US`.  Set Example* cookies\xa0string  ----------  Add HTTP cookies to use for request.  Set Example* stealth\xa0boolean  ----------  Use stealth mode for headless chrome request to help prevent being blocked. The default is enabled on chrome.  Set Example* headers\xa0string  ----------  Forward HTTP headers to use for all request. The object is expected to be a map of key value pairs.  Set Example* metadata\xa0boolean  ----------  Boolean to store metadata about the pages and content found. This could help improve AI interopt. Defaults to false unless you have the website already stored with the configuration enabled.  Set Example* viewport\xa0object  ----------  Configure the viewport for chrome. Defaults to 800x600.  Set Example* encoding\xa0string  ----------  The type of encoding to use like `UTF-8`, `SHIFT_JIS`, or etc.  Set Example* subdomains\xa0boolean  ----------  Allow subdomains to be included.  Set Example* user\\_agent\xa0string  ----------  Add a custom HTTP user agent to the request.  Set Example* store\\_data\xa0boolean  ----------  Boolean to determine if storage should be used. If set this takes precedence over `storageless`. Defaults to false.  Set Example* gpt\\_config\xa0object  ----------  Use AI to generate actions to perform during the crawl. You can pass an array for the`"prompt"` to chain steps.  Set Example* fingerprint\xa0boolean  ----------  Use advanced fingerprint for chrome.  Set Example* storageless\xa0boolean  ----------  Boolean to prevent storing any type of data for the request including storage and AI vectors embedding. Defaults to false unless you have the website already stored.  Set Example* readability\xa0boolean  ----------  Use [readability](https://github.com/mozilla/readability) to pre-process the content for reading. This may drastically improve the content for LLM usage.  Set Example* return\\_format\xa0string  ----------  The format to return the data in. Possible values are `markdown`, `raw`, `text`, and `html2text`. Use `raw` to return the default format of the page like `HTML` etc.  Raw* proxy\\_enabled\xa0boolean  ----------  Enable high performance premium proxies for the request to prevent being blocked at the network level.  Set Example* query\\_selector\xa0string  ----------  The CSS query selector to use when extracting content from the markup.  Test Query Selector* full\\_resources\xa0boolean  ----------  Crawl and download all the resources for a website.  Set Example* request\\_timeout\xa0number  ----------  The timeout to use for request. Timeouts can be from 5-60. The default is 30 seconds.  Set Example* run\\_in\\_background\xa0boolean  ----------  Run the request in the background. Useful if storing data and wanting to trigger crawls to the dashboard. This has no effect if storageless is set.  Set ExampleShow More Properties* Basic* StreamingExample requestPythonCopy```import requests, osheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}json_data = {"limit":50,"url":"http://www.example.com"}response = requests.post(\'https://api.spider.cloud/crawl\',  headers=headers,  json=json_data)print(response.json())```ResponseCopy```[  {    "content": "<html>...",    "error": null,    "status": 200,    "url": "http://www.example.com"  },  // more content...]```Crawl websites get links==========Start crawling a website(s) to collect links found.POST https://api.spider.cloud/linksRequest body* url\xa0required\xa0string  ----------  The URI resource to crawl. This can be a comma split list for multiple urls.  Test Url* request\xa0string  ----------  The request type to perform. Possible values are `http`, `chrome`, and `smart`. Use `smart` to perform HTTP request by default until JavaScript rendering is needed for the HTML.  HTTP* limit\xa0number  ----------  The maximum amount of pages allowed to crawl per website. Remove the value or set it to 0 to crawl all pages.  Crawl Limit* depth\xa0number  ----------  The crawl limit for maximum depth. If zero, no limit will be applied.  Crawl DepthSet Example* cache\xa0boolean  ----------  Use HTTP caching for the crawl to speed up repeated runs.  Set Example* budget\xa0object  ----------  Object that has paths with a counter for limiting the amount of pages example `{"*":1}` for only crawling the root page. The wildcard matches all routes and you can set child paths preventing a depth level, example of limiting `{ "/docs/colors": 10, "/docs/": 100 }` which only allows a max of 100 pages if the route matches `/docs/:pathname` and only 10 pages if it matches `/docs/colors/:pathname`.  Crawl Budget  Set Example* locale\xa0string  ----------  The locale to use for request, example `en-US`.  Set Example* cookies\xa0string  ----------  Add HTTP cookies to use for request.  Set Example* stealth\xa0boolean  ----------  Use stealth mode for headless chrome request to help prevent being blocked. The default is enabled on chrome.  Set Example* headers\xa0string  ----------  Forward HTTP headers to use for all request. The object is expected to be a map of key value pairs.  Set Example* metadata\xa0boolean  ----------  Boolean to store metadata about the pages and content found. This could help improve AI interopt. Defaults to false unless you have the website already stored with the configuration enabled.  Set Example* viewport\xa0object  ----------  Configure the viewport for chrome. Defaults to 800x600.  Set Example* encoding\xa0string  ----------  The type of encoding to use like `UTF-8`, `SHIFT_JIS`, or etc.  Set Example* subdomains\xa0boolean  ----------  Allow subdomains to be included.  Set Example* user\\_agent\xa0string  ----------  Add a custom HTTP user agent to the request.  Set Example* store\\_data\xa0boolean  ----------  Boolean to determine if storage should be used. If set this takes precedence over `storageless`. Defaults to false.  Set Example* gpt\\_config\xa0object  ----------  Use AI to generate actions to perform during the crawl. You can pass an array for the`"prompt"` to chain steps.  Set Example* fingerprint\xa0boolean  ----------  Use advanced fingerprint for chrome.  Set Example* storageless\xa0boolean  ----------  Boolean to prevent storing any type of data for the request including storage and AI vectors embedding. Defaults to false unless you have the website already stored.  Set Example* readability\xa0boolean  ----------  Use [readability](https://github.com/mozilla/readability) to pre-process the content for reading. This may drastically improve the content for LLM usage.  Set Example* return\\_format\xa0string  ----------  The format to return the data in. Possible values are `markdown`, `raw`, `text`, and `html2text`. Use `raw` to return the default format of the page like `HTML` etc.  Raw* proxy\\_enabled\xa0boolean  ----------  Enable high performance premium proxies for the request to prevent being blocked at the network level.  Set Example* query\\_selector\xa0string  ----------  The CSS query selector to use when extracting content from the markup.  Test Query Selector* full\\_resources\xa0boolean  ----------  Crawl and download all the resources for a website.  Set Example* request\\_timeout\xa0number  ----------  The timeout to use for request. Timeouts can be from 5-60. The default is 30 seconds.  Set Example* run\\_in\\_background\xa0boolean  ----------  Run the request in the background. Useful if storing data and wanting to trigger crawls to the dashboard. This has no effect if storageless is set.  Set ExampleShow More Properties* Basic* StreamingExample requestPythonCopy```import requests, osheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}json_data = {"limit":50,"url":"http://www.example.com"}response = requests.post(\'https://api.spider.cloud/links\',  headers=headers,  json=json_data)print(response.json())```ResponseCopy```[  {    "content": "",    "error": null,    "status": 200,    "url": "http://www.example.com"  },  // more content...]```Screenshot websites==========Start taking screenshots of website(s) to collect images to base64 or binary.POST https://api.spider.cloud/screenshotRequest bodyGeneralSpecific* url\xa0required\xa0string  ----------  The URI resource to crawl. This can be a comma split list for multiple urls.  Test Url* request\xa0string  ----------  The request type to perform. Possible values are `http`, `chrome`, and `smart`. Use `smart` to perform HTTP request by default until JavaScript rendering is needed for the HTML.  HTTP* limit\xa0number  ----------  The maximum amount of pages allowed to crawl per website. Remove the value or set it to 0 to crawl all pages.  Crawl Limit* depth\xa0number  ----------  The crawl limit for maximum depth. If zero, no limit will be applied.  Crawl DepthSet Example* cache\xa0boolean  ----------  Use HTTP caching for the crawl to speed up repeated runs.  Set Example* budget\xa0object  ----------  Object that has paths with a counter for limiting the amount of pages example `{"*":1}` for only crawling the root page. The wildcard matches all routes and you can set child paths preventing a depth level, example of limiting `{ "/docs/colors": 10, "/docs/": 100 }` which only allows a max of 100 pages if the route matches `/docs/:pathname` and only 10 pages if it matches `/docs/colors/:pathname`.  Crawl Budget  Set Example* locale\xa0string  ----------  The locale to use for request, example `en-US`.  Set Example* cookies\xa0string  ----------  Add HTTP cookies to use for request.  Set Example* stealth\xa0boolean  ----------  Use stealth mode for headless chrome request to help prevent being blocked. The default is enabled on chrome.  Set Example* headers\xa0string  ----------  Forward HTTP headers to use for all request. The object is expected to be a map of key value pairs.  Set Example* metadata\xa0boolean  ----------  Boolean to store metadata about the pages and content found. This could help improve AI interopt. Defaults to false unless you have the website already stored with the configuration enabled.  Set Example* viewport\xa0object  ----------  Configure the viewport for chrome. Defaults to 800x600.  Set Example* encoding\xa0string  ----------  The type of encoding to use like `UTF-8`, `SHIFT_JIS`, or etc.  Set Example* subdomains\xa0boolean  ----------  Allow subdomains to be included.  Set Example* user\\_agent\xa0string  ----------  Add a custom HTTP user agent to the request.  Set Example* store\\_data\xa0boolean  ----------  Boolean to determine if storage should be used. If set this takes precedence over `storageless`. Defaults to false.  Set Example* gpt\\_config\xa0object  ----------  Use AI to generate actions to perform during the crawl. You can pass an array for the`"prompt"` to chain steps.  Set Example* fingerprint\xa0boolean  ----------  Use advanced fingerprint for chrome.  Set Example* storageless\xa0boolean  ----------  Boolean to prevent storing any type of data for the request including storage and AI vectors embedding. Defaults to false unless you have the website already stored.  Set Example* readability\xa0boolean  ----------  Use [readability](https://github.com/mozilla/readability) to pre-process the content for reading. This may drastically improve the content for LLM usage.  Set Example* return\\_format\xa0string  ----------  The format to return the data in. Possible values are `markdown`, `raw`, `text`, and `html2text`. Use `raw` to return the default format of the page like `HTML` etc.  Raw* proxy\\_enabled\xa0boolean  ----------  Enable high performance premium proxies for the request to prevent being blocked at the network level.  Set Example* query\\_selector\xa0string  ----------  The CSS query selector to use when extracting content from the markup.  Test Query Selector* full\\_resources\xa0boolean  ----------  Crawl and download all the resources for a website.  Set Example* request\\_timeout\xa0number  ----------  The timeout to use for request. Timeouts can be from 5-60. The default is 30 seconds.  Set Example* run\\_in\\_background\xa0boolean  ----------  Run the request in the background. Useful if storing data and wanting to trigger crawls to the dashboard. This has no effect if storageless is set.  Set ExampleShow More Properties* Basic* StreamingExample requestPythonCopy```import requests, osheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}json_data = {"limit":50,"url":"http://www.example.com"}response = requests.post(\'https://api.spider.cloud/screenshot\',  headers=headers,  json=json_data)print(response.json())```ResponseCopy```[  {    "content": "base64...",    "error": null,    "status": 200,    "url": "http://www.example.com"  },  // more content...]```Pipelines----------Create powerful workflows with our pipeline API endpoints. Use AI to extract contacts from any website or filter links with prompts with ease.Crawl websites and extract contacts==========Start crawling a website(s) to collect all contacts found leveraging AI.POST https://api.spider.cloud/pipeline/extract-contactsRequest bodyGeneralSpecific* url\xa0required\xa0string  ----------  The URI resource to crawl. This can be a comma split list for multiple urls.  Test Url* request\xa0string  ----------  The request type to perform. Possible values are `http`, `chrome`, and `smart`. Use `smart` to perform HTTP request by default until JavaScript rendering is needed for the HTML.  HTTP* limit\xa0number  ----------  The maximum amount of pages allowed to crawl per website. Remove the value or set it to 0 to crawl all pages.  Crawl Limit* depth\xa0number  ----------  The crawl limit for maximum depth. If zero, no limit will be applied.  Crawl DepthSet Example* cache\xa0boolean  ----------  Use HTTP caching for the crawl to speed up repeated runs.  Set Example* budget\xa0object  ----------  Object that has paths with a counter for limiting the amount of pages example `{"*":1}` for only crawling the root page. The wildcard matches all routes and you can set child paths preventing a depth level, example of limiting `{ "/docs/colors": 10, "/docs/": 100 }` which only allows a max of 100 pages if the route matches `/docs/:pathname` and only 10 pages if it matches `/docs/colors/:pathname`.  Crawl Budget  Set Example* locale\xa0string  ----------  The locale to use for request, example `en-US`.  Set Example* cookies\xa0string  ----------  Add HTTP cookies to use for request.  Set Example* stealth\xa0boolean  ----------  Use stealth mode for headless chrome request to help prevent being blocked. The default is enabled on chrome.  Set Example* headers\xa0string  ----------  Forward HTTP headers to use for all request. The object is expected to be a map of key value pairs.  Set Example* metadata\xa0boolean  ----------  Boolean to store metadata about the pages and content found. This could help improve AI interopt. Defaults to false unless you have the website already stored with the configuration enabled.  Set Example* viewport\xa0object  ----------  Configure the viewport for chrome. Defaults to 800x600.  Set Example* encoding\xa0string  ----------  The type of encoding to use like `UTF-8`, `SHIFT_JIS`, or etc.  Set Example* subdomains\xa0boolean  ----------  Allow subdomains to be included.  Set Example* user\\_agent\xa0string  ----------  Add a custom HTTP user agent to the request.  Set Example* store\\_data\xa0boolean  ----------  Boolean to determine if storage should be used. If set this takes precedence over `storageless`. Defaults to false.  Set Example* gpt\\_config\xa0object  ----------  Use AI to generate actions to perform during the crawl. You can pass an array for the`"prompt"` to chain steps.  Set Example* fingerprint\xa0boolean  ----------  Use advanced fingerprint for chrome.  Set Example* storageless\xa0boolean  ----------  Boolean to prevent storing any type of data for the request including storage and AI vectors embedding. Defaults to false unless you have the website already stored.  Set Example* readability\xa0boolean  ----------  Use [readability](https://github.com/mozilla/readability) to pre-process the content for reading. This may drastically improve the content for LLM usage.  Set Example* return\\_format\xa0string  ----------  The format to return the data in. Possible values are `markdown`, `raw`, `text`, and `html2text`. Use `raw` to return the default format of the page like `HTML` etc.  Raw* proxy\\_enabled\xa0boolean  ----------  Enable high performance premium proxies for the request to prevent being blocked at the network level.  Set Example* query\\_selector\xa0string  ----------  The CSS query selector to use when extracting content from the markup.  Test Query Selector* full\\_resources\xa0boolean  ----------  Crawl and download all the resources for a website.  Set Example* request\\_timeout\xa0number  ----------  The timeout to use for request. Timeouts can be from 5-60. The default is 30 seconds.  Set Example* run\\_in\\_background\xa0boolean  ----------  Run the request in the background. Useful if storing data and wanting to trigger crawls to the dashboard. This has no effect if storageless is set.  Set ExampleShow More Properties* Basic* StreamingExample requestPythonCopy```import requests, osheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}json_data = {"limit":50,"url":"http://www.example.com"}response = requests.post(\'https://api.spider.cloud/pipeline/extract-contacts\',  headers=headers,  json=json_data)print(response.json())```ResponseCopy```[  {    "content": [{ "full_name": "John Doe", "email": "johndoe@gmail.com", "phone": "555-555-555", "title": "Baker"}, ...],    "error": null,    "status": 200,    "url": "http://www.example.com"  },  // more content...]```Label website==========Crawl a website and accurately categorize it using AI.POST https://api.spider.cloud/pipeline/labelRequest bodyGeneralSpecific* url\xa0required\xa0string  ----------  The URI resource to crawl. This can be a comma split list for multiple urls.  Test Url* request\xa0string  ----------  The request type to perform. Possible values are `http`, `chrome`, and `smart`. Use `smart` to perform HTTP request by default until JavaScript rendering is needed for the HTML.  HTTP* limit\xa0number  ----------  The maximum amount of pages allowed to crawl per website. Remove the value or set it to 0 to crawl all pages.  Crawl Limit* depth\xa0number  ----------  The crawl limit for maximum depth. If zero, no limit will be applied.  Crawl DepthSet Example* cache\xa0boolean  ----------  Use HTTP caching for the crawl to speed up repeated runs.  Set Example* budget\xa0object  ----------  Object that has paths with a counter for limiting the amount of pages example `{"*":1}` for only crawling the root page. The wildcard matches all routes and you can set child paths preventing a depth level, example of limiting `{ "/docs/colors": 10, "/docs/": 100 }` which only allows a max of 100 pages if the route matches `/docs/:pathname` and only 10 pages if it matches `/docs/colors/:pathname`.  Crawl Budget  Set Example* locale\xa0string  ----------  The locale to use for request, example `en-US`.  Set Example* cookies\xa0string  ----------  Add HTTP cookies to use for request.  Set Example* stealth\xa0boolean  ----------  Use stealth mode for headless chrome request to help prevent being blocked. The default is enabled on chrome.  Set Example* headers\xa0string  ----------  Forward HTTP headers to use for all request. The object is expected to be a map of key value pairs.  Set Example* metadata\xa0boolean  ----------  Boolean to store metadata about the pages and content found. This could help improve AI interopt. Defaults to false unless you have the website already stored with the configuration enabled.  Set Example* viewport\xa0object  ----------  Configure the viewport for chrome. Defaults to 800x600.  Set Example* encoding\xa0string  ----------  The type of encoding to use like `UTF-8`, `SHIFT_JIS`, or etc.  Set Example* subdomains\xa0boolean  ----------  Allow subdomains to be included.  Set Example* user\\_agent\xa0string  ----------  Add a custom HTTP user agent to the request.  Set Example* store\\_data\xa0boolean  ----------  Boolean to determine if storage should be used. If set this takes precedence over `storageless`. Defaults to false.  Set Example* gpt\\_config\xa0object  ----------  Use AI to generate actions to perform during the crawl. You can pass an array for the`"prompt"` to chain steps.  Set Example* fingerprint\xa0boolean  ----------  Use advanced fingerprint for chrome.  Set Example* storageless\xa0boolean  ----------  Boolean to prevent storing any type of data for the request including storage and AI vectors embedding. Defaults to false unless you have the website already stored.  Set Example* readability\xa0boolean  ----------  Use [readability](https://github.com/mozilla/readability) to pre-process the content for reading. This may drastically improve the content for LLM usage.  Set Example* return\\_format\xa0string  ----------  The format to return the data in. Possible values are `markdown`, `raw`, `text`, and `html2text`. Use `raw` to return the default format of the page like `HTML` etc.  Raw* proxy\\_enabled\xa0boolean  ----------  Enable high performance premium proxies for the request to prevent being blocked at the network level.  Set Example* query\\_selector\xa0string  ----------  The CSS query selector to use when extracting content from the markup.  Test Query Selector* full\\_resources\xa0boolean  ----------  Crawl and download all the resources for a website.  Set Example* request\\_timeout\xa0number  ----------  The timeout to use for request. Timeouts can be from 5-60. The default is 30 seconds.  Set Example* run\\_in\\_background\xa0boolean  ----------  Run the request in the background. Useful if storing data and wanting to trigger crawls to the dashboard. This has no effect if storageless is set.  Set ExampleShow More Properties* Basic* StreamingExample requestPythonCopy```import requests, osheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}json_data = {"limit":50,"url":"http://www.example.com"}response = requests.post(\'https://api.spider.cloud/pipeline/label\',  headers=headers,  json=json_data)print(response.json())```ResponseCopy```[  {    "content": ["Government"],    "error": null,    "status": 200,    "url": "http://www.example.com"  },  // more content...]```Crawl State==========Get the state of the crawl for the domain.POST https://api.spider.cloud/crawl/statusRequest body* url\xa0required\xa0string  ----------  The URI resource to crawl. This can be a comma split list for multiple urls.  Test UrlShow More Properties* Basic* StreamingExample requestPythonCopy```import requests, osheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}response = requests.post(\'https://api.spider.cloud/crawl/status\',  headers=headers)print(response.json())```ResponseCopy```  {    "content": {        "data": {          "id": "195bf2f2-2821-421d-b89c-f27e57ca71fh",          "user_id": "6bd06efa-bb0a-4f1f-a29f-05db0c4b1bfg",          "domain": "example.com",          "url": "https://example.com/",          "links":1,          "credits_used": 3,          "mode":2,          "crawl_duration": 340,          "message": null,          "request_user_agent": "Spider",          "level": "info",          "status_code": 0,          "created_at": "2024-04-21T01:21:32.886863+00:00",          "updated_at": "2024-04-21T01:21:32.886863+00:00"        },        "error": ""      },    "error": null,    "status": 200,    "url": "http://www.example.com"  }```Credits Available==========Get the remaining credits available.GET https://api.spider.cloud/credits* Basic* StreamingExample requestPythonCopy```import requests, osheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}response = requests.post(\'https://api.spider.cloud/credits\',  headers=headers)print(response.json())```ResponseCopy```{ "credits": 52566 }```[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='44b350c3-f907-4767-84ec-a73fe59c190c', embedding=None, metadata={'description': 'End User License Agreement for the Spiderwebai and the spider project.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 20123, 'keywords': None, 'pathname': '/eula', 'resource_type': 'html', 'title': 'EULA', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/eula.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='EULA[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)End User License Agreement==========Our end user license agreement may change from time to time as we build out the software.Right to Ban----------Part of making sure the Spider is being used for the right purpose we will not allow malicious acts to be done with the system. If we find that you are using the tool to hack, crawl illegal pages, porn, or anything that falls into this line will be banned from the system. You can reach out to us to weigh out your reasons on why you should not be banned.License----------You can use the API and service to build ontop of. Replicating the features and re-selling the service is not allowed. We do not provide any custom license for the platform and encourage users to use our system to handle any crawling, scraping, or data curation needs for speed and cost effectiveness.### Adjustments to Plans ###The software is very new and while we figure out what we can charge to maintain the systems the plans may change. We will send out a notification of the changes in our [Discord](https://discord.gg/5bDPDxwTn3) or Github. For the most part plans will increase drastically with things set to scale costs that allow more usage for everyone. Spider is a product of[A11yWatch LLC](https://a11ywatch.com) the web accessibility tool. The crawler engine of Spider powers the curation for A11yWatch allowing auditing websites accessibility compliance extremely fast.#### Contact ####For information about how to contact Spider, please reach out to email below.[support@spider.cloud](mailto:support@spider.cloud)[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='445c0c76-bfd5-4f89-a439-fbdeb8077a4c', embedding=None, metadata={'description': 'Spider is the fastest web crawler written in Rust. The Cloud version is a hosted version of open-source project.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 139080, 'keywords': None, 'pathname': '/about', 'resource_type': 'html', 'title': 'About', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/about.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='About[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider) About==========Spider is the fastest web crawler written in Rust. The Cloud version is a hosted version of open-source project. Spider Features----------Our features that facilitate website scraping and provide swift insights in one platform. Deliver astonishing results using our powerful API.### Fast Unblockable Scraping ###When it comes to speed, the Spider project is the fastest web crawler available to the public. Utilize the foundation of open-source tools and make the most of your budget to scrape content effectively.Collecting Data Logo### Gain Website Insights with AI ###Enhance your crawls with AI to obtain relevant information fast from any website.AI Search### Extract Data Using Webhooks ###Set up webhooks across your websites to deliver the desired information anywhere you need.News Logo[A11yWatch](https://a11ywatch.com)maintains the project and the hosting for the service.[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='1a2d63a5-0315-4c5b-8fed-8ac460b82cc7', embedding=None, metadata={'description': 'Add the amount of credits you want to purchase for scraping the internet with AI and LLM data curation abilities fast.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 23083, 'keywords': None, 'pathname': '/credits/new', 'resource_type': 'html', 'title': 'Purchase Spider Credits', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/credits*_*new.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Purchase Spider Credits[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)Add credits==========Add credits to start crawling any website today.|Default|      Features      |       Amount       ||-------|--------------------|--------------------||Default| Scraping Websites  |$0.03 / gb bandwidth|| Extra |  Premium Proxies   |$0.01 / gb bandwidth|| Extra |Javascript Rendering|$0.01 / gb bandwidth|| Extra |    Data Storage    |  $0.30 / gb month  || Extra |      AI Chat       | $0.01 input/output |[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='6701b47a-0000-4111-8b5b-c77b01937a7d', embedding=None, metadata={'description': 'Collect data rapidly from any website. Seamlessly scrape websites and get data tailored for LLM workloads.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 101750, 'keywords': None, 'pathname': '/', 'resource_type': 'html', 'title': 'Spider - Fastest Web Crawler', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/index.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Spider - Fastest Web Crawler[Spider v1 Logo Spider ](/)[Pricing](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)The World\'s Fastest and Cheapest Crawler API==========View Demo* Basic* StreamingExample requestPythonCopy```import requests, osheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}json_data = {"limit":50,"url":"http://www.example.com"}response = requests.post(\'https://api.spider.cloud/crawl\',  headers=headers,  json=json_data)print(response.json())```Example ResponseUnmatched Speed----------### 5secs  ###To crawl 200 pages### 21x  ###Faster than FireCrawl### 150x  ###Faster than Apify Benchmarks displaying performance between Spider Cloud, Firecrawl, and Apify.[See framework benchmarks ](https://github.com/spider-rs/spider/blob/main/benches/BENCHMARKS.md)Foundations for Crawling Effectively----------### Leading in performance ###Spider is written in Rust and runs in full concurrency to achieve crawling dozens of pages in secs.### Optimal response format ###Get clean and formatted markdown, HTML, or text content for fine-tuning or training AI models.### Caching ###Further boost speed by caching repeated web page crawls.### Smart Mode ###Spider dynamically switches to Headless Chrome when it needs to.Beta### Scrape with AI ###Do custom browser scripting and data extraction using the latest AI models.### Best crawler for LLMs ###Don\'t let crawling and scraping be the highest latency in your LLM & AI agent stack.### Scrape with no headaches ###* Proxy rotations* Agent headers* Avoid anti-bot detections* Headless chrome* Markdown LLM Responses### The Fastest Web Crawler ###* Powered by [spider-rs](https://github.com/spider-rs/spider)* Do 20,000 pages in seconds* Full concurrency* Powerful and simple API* 5,000 requests per minute### Do more with AI ###* Custom browser scripting* Advanced data extraction* Data pipelines* Perfect for LLM and AI Agents* Accurate website labeling[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='91b98a80-7112-4837-8389-cb78221b254c', embedding=None, metadata={'description': 'Get contact information from any website in real time with AI. The only way to accurately get dynamic information from websites.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 25891, 'keywords': None, 'pathname': '/guides/pipelines-extract-contacts', 'resource_type': 'html', 'title': 'Guides - Extract Contacts', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/guides*_*pipelines-extract-contacts.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Guides - Extract Contacts[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)Extract Contacts==========Contents----------* [Seamless extracting any contact any website](#seamless-extracting-any-contact-any-website)* [UI (Extracting Contacts)](#ui-extracting-contacts)* [API Extracting Usage](#api-extracting-usage)  * [API Extracting Example](#api-extracting-example)  * [Pipelines Combo](#pipelines-combo)Seamless extracting any contact any website----------Extracting contacts from a website used to be a very difficult challenge involving many steps that would change often. The challenges typically faced involve being able to get the data from a website without being blocked and setting up query selectors for the information you need using javascript. This would often break in two folds - the data extracting with a correct stealth technique or the css selector breaking as they update the website HTML code. Now we toss those two hard challenges away - one of them spider takes care of and the other the advancement in AI to process and extract information.UI (Extracting Contacts)----------You can use the UI on the dashboard to extract contacts after you crawled a page. Go to the page youwant to extract and click on the horizontal dropdown menu to display an option to extract the contact.The crawl will get the data first to see if anything new has changed. Afterwards if a contact was found usually within 10-60 seconds you will get a notification that the extraction is complete with the data.![Extracting contacts with the spider app](/img/app/extract-contacts.png)After extraction if the page has contact related data you can view it with a grid in the app.![The menu displaying the found contacts after extracting with the spider app](/img/app/extract-contacts-found.png)The grid will display the name, email, phone, title, and host(website found) of the contact(s).![Grid display of all the contact information found for the web page](/img/app/extract-contacts-grid.png)API Extracting Usage----------The endpoint `/pipeline/extract-contacts` provides the ability to extract all contacts from a website concurrently.### API Extracting Example ###To extract contacts from a website you can follow the example below. All params are optional except `url`. Use the `prompt` param to adjust the way the AI handles the extracting. If you use the param `store_data` or if the website already exist in the dashboard the contact data will be saved with the page.```import requests, os, jsonheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}json_data = {"limit":1,"url":"http://www.example.com/contacts", "model": "gpt-4-1106-preview", "prompt": "A custom prompt to tailor the extracting."}response = requests.post(\'https://api.spider.cloud/crawl/pipeline/extract-contacts\',  headers=headers,  json=json_data,  stream=True)for line in response.iter_lines():  if line:      print(json.loads(line))```### Pipelines Combo ###Piplines bring a whole new entry to workflows for data curation, if you combine the API endpoints to only use the extraction on pages you know may have contacts can save credits on the system. One way would be to perform gathering all the links first with the `/links` endpoint. After getting the links for the pages use `/pipeline/filter-links` with a custom prompt that can use AI to reduce the noise of the links to process before `/pipline/extract-contacts`.Loading graph...Written on:  2/1/2024[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='5e7ade0d-0a50-46de-8116-72ee5dca0b20', embedding=None, metadata={'description': 'How to use the Spider API to curate data from any source blazing fast. The most advanced crawler that handles all workloads of all sizes.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 24752, 'keywords': None, 'pathname': '/guides/spider-api', 'resource_type': 'html', 'title': 'Guides - Spider API', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/guides*_*spider-api.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Guides - Spider API[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)Getting started Spider API==========Contents----------* [API built to scale](#api-built-to-scale)* [API Usage](#api-usage)* [Crawling One Page](#crawling-one-page)* [Crawling Multiple Pages](#crawling-multiple-pages)  * [Planet Scale Crawling](#planet-scale-crawling)    * [Automatic Configuration](#automatic-configuration)API built to scale----------Welcome to our cutting-edge web crawler SaaS, renowned for its unparalleled speed.Our platform is designed to effortlessly manage thousands of requests per second, thanks to our elastically scalable system architecture and the Open-Source [spider](https://github.com/spider-rs/spider) project. We deliver consistent latency times ensuring swift processing for all responses.For an in-depth understanding of the request parameters supported, we invite you to explore our comprehensive API documentation. At present, we do not provide client-side libraries, as our API has been crafted with simplicity in mind for straightforward usage. However, we are open to expanding our offerings in the future to enhance user convenience.Dive into our [documentation]((/docs/api)) to get started and unleash the full potential of our web crawler today.API Usage----------Getting started with the API is simple and straight forward. After you get your [secret key](/api-keys)you can access our instance directly. We have one main endpoint `/crawl` that handles all things relatedto data curation. The crawler is highly configurable through the params to fit all needs.Crawling One Page----------Most cases you probally just want to crawl one page. Even if you only need one page, our system performs fast enough to lead the race.The most straight forward way to make sure you only crawl a single page is to set the [budget limit](./account/settings) with a wild card value or `*` to 1.You can also pass in the param `limit` in the JSON body with the limit of pages.Crawling Multiple Pages----------When you crawl multiple pages, the concurrency horsepower of the spider kicks in. You might wonder why and how one request may take (x)ms to come back, and 100 requests take about the same time! That’s because the built-in isolated concurrency allows for crawling thousands to millions of pages in no time. It’s the only current solution that can handle large websites with over 100k pages within a minute or two (sometimes even in a blink or two). By default, we do not add any limits to crawls unless specified.### Planet Scale Crawling ###If you plan on processing crawls that have over 200 pages, we recommend streaming the request from the client instead of parsing the entire payload once finished. We have an example of this with Python on the API docs page, also shown below.```import requests, os, jsonheaders = {    \'Authorization\': os.environ["SPIDER_API_KEY"],    \'Content-Type\': \'application/json\',}json_data = {"limit":250,"url":"http://www.example.com"}response = requests.post(\'https://api.spider.cloud/crawl/crawl\',  headers=headers,  json=json_data,  stream=True)for line in response.iter_lines():  if line:      print(json.loads(line))```#### Automatic Configuration ####Spider handles automatic concurrency handling and ip rotation to make it simple to curate data.The more credits you have or usage available allows for a higher concurrency limit.Written on:  1/3/2024[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='08e5f1d6-4ae7-4b68-ab96-4b6a3768e88c', embedding=None, metadata={'description': 'The programmable time machine that can store pages and all assets for easy website archiving.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 18970, 'keywords': None, 'pathname': '/guides/website-archiving', 'resource_type': 'html', 'title': 'Guides - Website Archiving', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/guides*_*website-archiving.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Guides - Website Archiving[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)Website Archiving==========With Spider you can easily backup or capture a website at any point in time.Enable Full Resource storing in the settings or website configuration to get a 1:1 copy of any websitelocally.Time Machine----------Time machine is storing data at a certain point of a time. Spider brings this to you with one simple configuration.After running the crawls you can simply download the data. This can help store assets incase the code is lost orversion control is removed.Written on:  2/7/2024[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='024cb27e-21d2-49a5-8a1a-963e72038421', embedding=None, metadata={'description': 'How to use the platform to collect data from the internet fast, affordable, and unblockable.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 24666, 'keywords': None, 'pathname': '/guides/spider', 'resource_type': 'html', 'title': 'Guides - Spider Platform', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/guides*_*spider.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Guides - Spider Platform[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)Getting started collecting data with Spider==========Contents----------* [Data Curation](#data-curation)  * [Crawling (Website)](#crawling-website)  * [Crawling (API)](#crawling-api)* [Crawl Configuration](#crawl-configuration)  * [Proxies](#proxies)  * [Headless Browser](#headless-browser)  * [Crawl Budget Limits](#crawl-budget-limits)* [Crawling and Scraping Websites](#crawling-and-scraping-websites)  * [Transforming Data](#transforming-data)    * [Leveraging Open Source](#leveraging-open-source)* [Subscription and Spider Credits](#subscription-and-spider-credits)Data Curation----------Collecting data with Spider can be fast and rewarding if done with some simple preliminary steps.Use the dashboard to collect data seamlessly across the internet with scheduled updates.You have two main ways of collecting data using Spider. The first and simplest is to use the UI available for scraping.The alternative is to use the API to programmatically access the system and perform actions.### Crawling (Website) ###1. Register or login to your account using email or Github.2. Purchase [credits](/credits/new) to kickstart crawls with `pay-as-you-go` go after credits deplete.3. Configure crawl [settings](/account/settings) to fit workflows that you need.4. Navigate to the [dashboard](/) and enter a website url or ask a question to get a url that should be crawled.5. Crawl the website and export/download the data as needed.### Crawling (API) ###1. Register or login to your account using email or Github.2. Purchase [credits](/credits/new) to kickstart crawls with `pay-as-you-go` after credits deplete.3. Configure crawl [settings](/account/settings) to fit workflows that you need.4. Navigate to [API keys](/api-keys) and create a new secret key.5. Go to the [API docs](/docs/api) page to see how the API works and perform crawls with code examples.Crawl Configuration----------Configuration your account for how you would like to crawl can help save costs or effectiveness of the content. Some of the configurations include setting Premium Proxies, Headless Browser Rendering, Webhooks, and Budgeting.### Proxies ###Using proxies with our system is straight forward. Simple check the toggle on if you want all request to use a proxy to increase the success of not being blocked.![Proxies example app screenshot.](/img/app/proxy-setting.png)### Headless Browser ###If you want pages that require JavaScript to be executed the headless browser config is for you. Enabling will run all request through a real Chrome Browser for JavaScript required rendering pages.![Headless browser example app screenshot.](/img/app/headless-browser.png)### Crawl Budget Limits ###One of the key things you may need to do before getting into the crawl is setting up crawl-budgets.Crawl budgets allows you to determine how many pages you are going to crawl for a website.Determining the budget will save you costs when dealing with large websites that you only want certain data points from. The example below shows adding a asterisk (\\*) to determine all routes with a limit of 50 pages maximum. The settings can be overwritten by the website configuration or parameters if using the API.![Crawl budget example screenshot](/img/app/edit-budget.png)Crawling and Scraping Websites----------Collecting data can be done in many ways and for many reasons. Leveraging our state-of-the-art technology allows you to create fast workloads that can process content from multiple locations. At the time of writing, we have started to focus on our data processing API instead of the dashboard. The API has much more flexibility than the UI for performing advanced workloads like batching, formatting, and so on.![Dashboard UI for Spider displaying data collecting from www.napster.com, jeffmendez.com, rsseau.rs, and www.drake.com](/img/app/ui-crawl.png)### Transforming Data ###The API has more features for gathering the content in different formats and transforming the HTML as needed. You can transform the content from HTML to Markdown and feed it to a LLM for better handling the learning aspect. The API is the first class citizen for the application. The UI will have the features provided by the API eventually as the need arises.#### Leveraging Open Source ####One of the reasons Spider is the ultimate data-curation service for scraping is from the power of Open-Source. The core of the engine is completly available on [Github](https://github.com/spider-rs/spider) under [MIT](https://opensource.org/license/mit/) to show what is in store. We are constantly working on the crawler features including performance with plans to maintain the project for the long run.Subscription and Spider Credits----------The platform allows purchasing credits that gives you the ability to crawl at any time.When you purchase credits a crawl subscription is created that allows you to continue to usethe platform when your credits deplete. The limits provided coralate with the amount of creditspurchased, an example would be if you bought $5 in credits you would have about $40 in spending limit - $10 in credit gives $80 and so on.The highest purchase of credits directly determines how much is allowed on the platform. You can view your usage and credits on the [usage limits page](/account/usage).Written on:  1/2/2024[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='44bff527-c7f3-4346-a2f8-1454c52e1b01', embedding=None, metadata={'description': 'Generate API keys that allow access to the system programmatically anywhere. Full management access for your Spider API journey.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 28770, 'keywords': None, 'pathname': '/api-keys', 'resource_type': 'html', 'title': 'API Keys Spider', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/api-keys.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text="API Keys Spider[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider) API Keys==========Generate API keys that allow access to the system programmatically anywhere. Full management access for your Spider API journey. Key Management----------Your secret API keys are listed below. Please note that we do not display your secret API keys again after you generate them.Do not share your API key with others, or expose it in the browser or other client-side code. In order to protect the security of your account, Spider may also automatically disable any API key that we've found has leaked publicly.Filter Name...Columns|   Name    |Key|Created|Last Used|   ||-----------|---|-------|---------|---||No results.|   |       |         |   |0 of 0 row(s) selected.PreviousNext[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='e577c57a-2376-452f-8c39-04d1e284595c', embedding=None, metadata={'description': 'Explore your usage and set limits that work with your budget.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 21195, 'keywords': None, 'pathname': '/account/usage', 'resource_type': 'html', 'title': 'Usage - Spider', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/account*_*usage.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text="Usage - Spider[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider) Usage limit==========Below you'll find a summary of usage for your account. The data may be delayed up to 5 minutes.Credits----------###  Pay as you go  ######  Approved usage limit  ### The maximum usage Spider allows for your organization each month. Ask for increase.###  Set a monthly budget  ###When your organization reaches this usage threshold each month, subsequent requests will be rejected. Data may be deleted if payments are rejected.[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), Document(id_='e3eb1e3c-5080-4590-94e8-fd2ef4f6d3c6', embedding=None, metadata={'description': 'Adjust your spider settings to adjust your crawl settings.', 'domain': 'spider.cloud', 'extracted_data': None, 'file_size': 18322, 'keywords': None, 'pathname': '/account/settings', 'resource_type': 'html', 'title': 'Settings - Spider', 'url': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48/spider.cloud/account*_*settings.html', 'user_id': '48f1bc3c-3fbb-408a-865b-c191a1bb1f48'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Settings - Spider[Spider v1 Logo Spider ](/) [Credits](/credits/new)[GitHubGithub637](https://github.com/spider-rs/spider)[API](/docs/api) [Pricing](/credits/new) [Guides](/guides) [About](/about) [Docs](https://docs.rs/spider/latest/spider/) [Privacy](/privacy) [Terms](/eula)© 2024 Spider from A11yWatchTheme Light Dark Toggle Theme [GitHubGithub](https://github.com/spider-rs/spider)', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n')]

```

For guides and documentation, visit [Spider](https://spider.cloud/docs/api)
# Using Browserbase Reader 🅱️
[Section titled “Using Browserbase Reader 🅱️”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-browserbase-reader-%F0%9F%85%B1%EF%B8%8F)
[Browserbase](https://browserbase.com) is a serverless platform for running headless browsers, it offers advanced debugging, session recordings, stealth mode, integrated proxies and captcha solving.
## Installation and Setup
[Section titled “Installation and Setup”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#installation-and-setup)
  * Get an API key and Project ID from [browserbase.com](https://browserbase.com) and set it in environment variables (`BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID`).
  * Install the [Browserbase SDK](http://github.com/browserbase/python-sdk):



```


%pip install browserbase


```


```


from llama_index.readers.web import BrowserbaseWebReader


```


```


reader = BrowserbaseWebReader()




docs = reader.load_data(




urls=[




"https://example.com",





# Text mode




text_content=False,



```

### Using FireCrawl Reader 🔥
[Section titled “Using FireCrawl Reader 🔥”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-firecrawl-reader)
Firecrawl is an api that turns entire websites into clean, LLM accessible markdown.
Using Firecrawl to gather an entire website

```


%pip install firecrawl-py


```


```


from llama_index.readers.web import FireCrawlWebReader


```


```

# using firecrawl to crawl a website



firecrawl_reader = FireCrawlWebReader(




api_key="<your_api_key>"# Replace with your actual API key from https://www.firecrawl.dev/




mode="scrape"# Choose between "crawl" and "scrape" for single page scraping




params={"additional": "parameters"},  # Optional additional parameters





# Load documents from a single page URL



documents = firecrawl_reader.load_data(url="http://paulgraham.com/")


```


```


index = SummaryIndex.from_documents(documents)


```


```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")


```


```


display(Markdown(f"<b>{response}</b>"))


```

Using firecrawl for a single page

```

# Initialize the FireCrawlWebReader with your API key and desired mode



from llama_index.readers.web.firecrawl_web.base import FireCrawlWebReader





firecrawl_reader = FireCrawlWebReader(




api_key="<your_api_key>"# Replace with your actual API key from https://www.firecrawl.dev/




mode="scrape"# Choose between "crawl" and "scrape" for single page scraping




params={"additional": "parameters"},  # Optional additional parameters





# Load documents from a single page URL



documents = firecrawl_reader.load_data(url="http://paulgraham.com/worked.html")


```


```

Running cells with '/opt/homebrew/bin/python3' requires the ipykernel package.




Run the following command to install 'ipykernel' into the Python environment.




Command: '/opt/homebrew/bin/python3 -m pip install ipykernel -U --user --force-reinstall'

```


```


index = SummaryIndex.from_documents(documents)


```


```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")


```


```


display(Markdown(f"<b>{response}</b>"))


```

Using FireCrawl’s extract mode to extract structured data from URLs

```

# Initialize the FireCrawlWebReader with your API key and extract mode



from llama_index.readers.web.firecrawl_web.base import FireCrawlWebReader





firecrawl_reader = FireCrawlWebReader(




api_key="<your_api_key>"# Replace with your actual API key from https://www.firecrawl.dev/




mode="extract"# Use extract mode to extract structured data




params={




"prompt": "Extract the title, author, and main points from this essay",




# Required prompt parameter for extract mode






# Load documents by providing a list of URLs to extract data from



documents = firecrawl_reader.load_data(




urls=[




"https://www.paulgraham.com",




"https://www.paulgraham.com/worked.html",




```


```


index = SummaryIndex.from_documents(documents)


```


```

# Query the extracted structured data



query_engine = index.as_query_engine()




response = query_engine.query("What are the main points from these essays?")





display(Markdown(f"<b>{response}</b>"))


```

# Using Hyperbrowser Reader ⚡
[Section titled “Using Hyperbrowser Reader ⚡”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-hyperbrowser-reader)
[Hyperbrowser](https://hyperbrowser.ai) is a platform for running and scaling headless browsers. It lets you launch and manage browser sessions at scale and provides easy to use solutions for any webscraping needs, such as scraping a single page or crawling an entire site.
Key Features:
  * Instant Scalability - Spin up hundreds of browser sessions in seconds without infrastructure headaches
  * Simple Integration - Works seamlessly with popular tools like Puppeteer and Playwright
  * Powerful APIs - Easy to use APIs for scraping/crawling any site, and much more
  * Bypass Anti-Bot Measures - Built-in stealth mode, ad blocking, automatic CAPTCHA solving, and rotating proxies


For more information about Hyperbrowser, please visit the [Hyperbrowser website](https://hyperbrowser.ai) or if you want to check out the docs, you can visit the [Hyperbrowser docs](https://docs.hyperbrowser.ai).
## Installation and Setup
[Section titled “Installation and Setup”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#installation-and-setup-1)
  * Head to [Hyperbrowser](https://app.hyperbrowser.ai/) to sign up and generate an API key. Once you’ve done this set the `HYPERBROWSER_API_KEY` environment variable or you can pass it to the `HyperbrowserWebReader` constructor.
  * Install the [Hyperbrowser SDK](https://github.com/hyperbrowserai/python-sdk):



```


%pip install hyperbrowser


```


```


from llama_index.readers.web import HyperbrowserWebReader





reader = HyperbrowserWebReader(api_key="your_api_key_here")




docs = reader.load_data(




urls=["https://example.com"],




operation="scrape",




docs

```

#### Using TrafilaturaWebReader
[Section titled “Using TrafilaturaWebReader”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-trafilaturawebreader)

```


from llama_index.readers.web import TrafilaturaWebReader


```


```

---------------------------------------------------------------------------



ModuleNotFoundError                       Traceback (most recent call last)



Cell In[7], line 1


----> 1 from llama_index.readers.web import TrafilaturaWebReader




ModuleNotFoundError: No module named 'llama_index.readers.web'

```


```


documents = TrafilaturaWebReader().load_data(




["http://paulgraham.com/worked.html"]



```


```


index = SummaryIndex.from_documents(documents)


```


```

# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("What did the author do growing up?")


```


```


display(Markdown(f"<b>{response}</b>"))


```

### Using RssReader
[Section titled “Using RssReader”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-rssreader)

```


from llama_index.core import SummaryIndex




from llama_index.readers.web import RssReader





documents = RssReader().load_data(




["https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"]






index = SummaryIndex.from_documents(documents)




# set Logging to DEBUG for more detailed outputs



query_engine = index.as_query_engine()




response = query_engine.query("What happened in the news today?")


```

## Using ScrapFly
[Section titled “Using ScrapFly”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-scrapfly)
ScrapFly is a web scraping API with headless browser capabilities, proxies, and anti-bot bypass. It allows for extracting web page data into accessible LLM markdown or text. Install ScrapFly Python SDK using pip:
Terminal window
```


pipinstallscrapfly-sdk


```

Here is a basic usage of ScrapflyReader

```


from llama_index.readers.web import ScrapflyReader




# Initiate ScrapflyReader with your ScrapFly API key



scrapfly_reader = ScrapflyReader(




api_key="Your ScrapFly API key"# Get your API key from https://www.scrapfly.io/




ignore_scrape_failures=True# Ignore unprocessable web pages and log their exceptions





# Load documents from URLs as markdown



documents = scrapfly_reader.load_data(




urls=["https://web-scraping.dev/products"]



```

The ScrapflyReader also allows passigng ScrapeConfig object for customizing the scrape request. See the documentation for the full feature details and their API params: <https://scrapfly.io/docs/scrape-api/getting-started>

```


from llama_index.readers.web import ScrapflyReader




# Initiate ScrapflyReader with your ScrapFly API key



scrapfly_reader = ScrapflyReader(




api_key="Your ScrapFly API key"# Get your API key from https://www.scrapfly.io/




ignore_scrape_failures=True# Ignore unprocessable web pages and log their exceptions






scrapfly_scrape_config = {




"asp": True# Bypass scraping blocking and antibot solutions, like Cloudflare




"render_js": True# Enable JavaScript rendering with a cloud headless browser




"proxy_pool": "public_residential_pool"# Select a proxy pool (datacenter or residnetial)




"country": "us"# Select a proxy location




"auto_scroll": True# Auto scroll the page




"js": ""# Execute custom JavaScript code by the headless browser





# Load documents from URLs as markdown



documents = scrapfly_reader.load_data(




urls=["https://web-scraping.dev/products"],




scrape_config=scrapfly_scrape_config,  # Pass the scrape config




scrape_format="markdown"# The scrape result format, either `markdown`(default) or `text`



```

# Using ZyteWebReader
[Section titled “Using ZyteWebReader”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-zytewebreader)
ZyteWebReader allows a user to access the content of webpage in different modes (“article”, “html-text”, “html”). It enables user to change setting such as browser rendering and JS as the content of many sites would require setting these options to access relevant content. All supported options can be found here: <https://docs.zyte.com/zyte-api/usage/reference.html>
To install dependencies:
Terminal window
```


pipinstallzyte-api


```

To get access to your ZYTE API key please visit: <https://docs.zyte.com/zyte-api/get-started.html>

```


from llama_index.readers.web import ZyteWebReader




# Required to run it in notebook


# import nest_asyncio


# nest_asyncio.apply()




# Initiate ZyteWebReader with your Zyte API key



zyte_reader = ZyteWebReader(




api_key="your ZYTE API key here",




mode="article"# or "html-text" or "html"






urls = [




"https://www.zyte.com/blog/web-scraping-apis/",




"https://www.zyte.com/blog/system-integrators-extract-big-data/",






documents = zyte_reader.load_data(




urls=urls,






print(len(documents[0].text))


```

Browser rendering and javascript can be enabled by passing setting corresponding parameters during initialization.

```


zyte_dw_params = {




"browserHtml": True# Enable browser rendering




"javascript": True# Enable JavaScript





# Initiate ZyteWebReader with your Zyte API key and use default "article" mode



zyte_reader = ZyteWebReader(




api_key="your ZYTE API key here",




download_kwargs=zyte_dw_params,





# Load documents from URLs



documents = zyte_reader.load_data(




urls=urls,



```


```


len(documents[0].text)


```

Set “continue_on_failure” to False if you’d like to stop when any request fails.

```


zyte_reader = ZyteWebReader(




api_key="your ZYTE API key here",




mode="html-text",




download_kwargs=zyte_dw_params,




continue_on_failure=False,





# Load documents from URLs



documents = zyte_reader.load_data(




urls=urls,



```


```


len(documents[0].text)


```


```

17488

```

In default mode (“article”) only the article text is extracted while in the “html-text” full text is extracted from the webpage, there the length of the text is significantly longer.
# Using AgentQLWebReader 🐠
[Section titled “Using AgentQLWebReader 🐠”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-agentqlwebreader)
Use AgentQL to scrape structured data from a website.

```


from llama_index.readers.web import AgentQLWebReader




from llama_index.core import VectorStoreIndex




from IPython.display import Markdown, display


```


```

# Using AgentQL to crawl a website



agentql_reader = AgentQLWebReader(




api_key="YOUR_API_KEY"# Replace with your actual API key from https://dev.agentql.com




params={




"is_scroll_to_bottom_enabled": True




},  # Optional additional parameters





# Load documents from a single page URL



document = agentql_reader.load_data(




url="https://www.ycombinator.com/companies?batch=W25",




query="{ company[] { name location description industry_category link(a link to the company's detail on Ycombinator)} }",



```


```


index = VectorStoreIndex.from_documents(document)




query_engine = index.as_query_engine()




response = query_engine.query(




"Find companies that are working on web agent, list their names, locations and link"






display(Markdown(f"<b>{response}</b>"))


```

# Using OxylabsWebReader
[Section titled “Using OxylabsWebReader”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-oxylabswebreader)
OxylabsWebReader allows a user to scrape any website with different parameters while bypassing most of the anti-bot tools. Check out the [Oxylabs documentation](https://developers.oxylabs.io/scraper-apis/web-scraper-api/other-websites) to get the full list of parameters.
Claim free API credentials by creating an Oxylabs account [here](https://oxylabs.io/).

```


from llama_index.readers.web import OxylabsWebReader






reader = OxylabsWebReader(




username="OXYLABS_USERNAME", password="OXYLABS_PASSWORD"






documents = reader.load_data(





"https://sandbox.oxylabs.io/products/1",




"https://sandbox.oxylabs.io/products/2",







print(documents[0].text)


```


```

The Legend of Zelda: Ocarina of Time | Oxylabs Scraping Sandbox



[![]()![logo](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)](/)



Game platforms:



* **All**



* [Nintendo platform](/products/category/nintendo)



+ wii


+ wii-u


+ nintendo-64


+ switch


+ gamecube


+ game-boy-advance


+ 3ds


+ ds



* [Xbox platform](/products/category/xbox-platform)



* **Dreamcast**



* [Playstation platform](/products/category/playstation-platform)



* **Pc**



* **Stadia**



Go Back



Note!This is a sandbox website used for web scraping. Information listed in this website does not have any real meaning and should not be associated with the actual products.



![The Legend of Zelda: Ocarina of Time](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)



The Legend of Zelda: Ocarina of Time


------------------------------------



**Developer:** Nintendo**Platform:****Type:** singleplayer



As a young boy, Link is tricked by Ganondorf, the King of the Gerudo Thieves. The evil human uses Link to gain access to the Sacred Realm, where he places his tainted hands on Triforce and transforms the beautiful Hyrulean landscape into a barren wasteland. Link is determined to fix the problems he helped to create, so with the help of Rauru he travels through time gathering the powers of the Seven Sages.



91,99 €



In stock



Add to Basket



[![The_Legend_of_Zelda:_Majora's_Mask](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)



#### The Legend of Zelda: Majora's Mask](/products/20)



Action Adventure Fantasy



Thrown into a parallel world by the mischievous actions of a possessed Skull Kid, Link finds a land in grave danger. The dark power of a relic called Majora's Mask has wreaked havoc on the citizens of Termina, but their most urgent problem is a suicidal moon crashing toward the world. Link has only 72 hours to find a way to stop its descent.



91,99 €



Add to Basket



[![Indiana_Jones_and_the_Infernal_Machine](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)



#### Indiana Jones and the Infernal Machine](/products/1836)



Action Adventure Historic



1947. The nazis have been crushed, the Cold War has begun and Soviet agents are sniffing around an ancient ruin. Grab your whip and fedora and join Indy in a globespanning race to unearth the mysterious "Infernal Machine". Survive the challenges of unusual beasts, half the Red Army and more (including - oh no - snakes!) . Puzzle your way through 17 chapters of an action-packed story. Travel the world to exotic locales, from the ruins of Babylon to Egyptian deserts. All the weapons you'll need, including firearms, explosives-and of course Indy's trusty whip and revolver.



80,99 €



Add to Basket

```

Another example with parameters for selecting the geolocation, user agent type, JavaScript rendering, headers, and cookies.

```


documents = reader.load_data(





"https://sandbox.oxylabs.io/products/3",






"geo_location": "Berlin, Germany",




"render": "html",




"user_agent_type": "mobile",




"context": [




{"key": "force_headers", "value": True},




{"key": "force_cookies", "value": True},





"key": "headers",




"value": {




"Content-Type": "text/html",




"Custom-Header-Name": "custom header content",







"key": "cookies",




"value": [




{"key": "NID", "value": "1234567890"},




{"key": "1P JAR", "value": "0987654321"},






{"key": "http_method", "value": "get"},




{"key": "follow_redirects", "value": True},




{"key": "successful_status_codes", "value": [808, 909]},





```

# Using ZenRows Web Reader 🌐
[Section titled “Using ZenRows Web Reader 🌐”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-zenrows-web-reader)
[ZenRows](https://www.zenrows.com/) is a powerful web scraping API that provides advanced features for bypassing anti-bot measures and extracting data from modern websites.
Key Features:
  * **JavaScript Rendering** : Handle SPAs and dynamic content with headless browser rendering
  * **Premium Proxies** : Bypass anti-bot protection with 55M+ residential IPs from 190+ countries
  * **Session Management** : Maintain the same IP across multiple requests
  * **Advanced Data Extraction** : Use CSS selectors or automatic parsing to extract specific data
  * **Multiple Output Formats** : Get results in HTML, Markdown, Text, or PDF format
  * **Geolocation Support** : Use proxies from specific countries for geo-restricted content


**Prerequisites:** You need to have a ZenRows API key to use this reader. You can get one at [zenrows.com](https://app.zenrows.com/register).

```

# Basic web scraping with ZenRows



from llama_index.readers.web import ZenRowsWebReader





zenrows_reader = ZenRowsWebReader(




api_key="YOUR_API_KEY"# Get one at https://app.zenrows.com/register




response_type="markdown",





# Scrape a single URL



documents = zenrows_reader.load_data(["https://httpbin.io/html"])




print(documents[0].text[:500])  # Print first 500 characters


```


```

# Advanced scraping with anti-bot bypass



zenrows_advanced = ZenRowsWebReader(




api_key="YOUR_API_KEY",




js_render=True# Enable JavaScript rendering




premium_proxy=True# Use residential proxies




proxy_country="us"# Optional: specify country






documents = zenrows_advanced.load_data(




["https://www.scrapingcourse.com/antibot-challenge"]





print(f"Scraped {len(documents[0].text)} characters with advanced features")


```


```

# Integration with LlamaIndex - scraping multiple pages



zenrows_reader = ZenRowsWebReader(




api_key="YOUR_API_KEY", js_render=True, response_type="markdown"





# Scrape multiple URLs



urls = ["https://example.com/", "https://httpbin.io/html"]





documents = zenrows_reader.load_data(urls)




# Create index and query



index = SummaryIndex.from_documents(documents)




query_engine = index.as_query_engine()




response = query_engine.query("What content was found on these pages?")





display(Markdown(f"<b>{response}</b>"))


```

For more advanced features like custom headers, CSS data extraction, screenshot capabilities, and detailed configuration options, visit the [ZenRows documentation](https://docs.zenrows.com/universal-scraper-api/api-reference).
# Using Olostep Web Reader 🧢
[Section titled “Using Olostep Web Reader 🧢”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-olostep-web-reader)
[Olostep](https://www.olostep.com/) is reliable and **cost-effective web scraping API built for scale.** It bypasses bot detection, delivers results in seconds, and can process millions of requests.
The API returns clean data from any website in various formats, including Markdown, HTML, and structured JSON.
Sign up [here](https://www.olostep.com/auth) and get 1000 credits for free.

```

# Scraping content in Markdown




from llama_index.readers.web import OlostepWebReader




from llama_index.core import SummaryIndex




# Initialize the reader in scrape mode



reader = OlostepWebReader(api_key="YOUR_OLOSTEP_API_KEY", mode="scrape")




# Load data from a URL



documents = reader.load_data(url="https://www.olostep.com/")




# Create index and query



index = SummaryIndex.from_documents(documents)




query_engine = index.as_query_engine()




response = query_engine.query("Summarize in 100 words")





print(response)


```


```

Olostep offers a Web Scraping API that provides clean data for AI applications from any website in just 1-5 seconds. The API can handle up to 100K requests in minutes, making it efficient and cost-effective. Users can sign up for free with an invite code and access various features like structured data extraction, parsers for common websites, and batch executions for scaling up to 100K URLs in 5-7 minutes. Olostep emphasizes reliability, scalability, and affordability, catering to startups, AI developers, and businesses needing web data extraction services. Additionally, the API supports JS execution, residential IPs, and various output formats like Markdown, HTML, PDF, and structured JSON.

```


```

# Running Google Searches




from llama_index.readers.web import OlostepWebReader




from llama_index.core import SummaryIndex




# Initialize the reader in search mode



reader = OlostepWebReader(api_key="YOUR_OLOSTEP_API_KEY", mode="search")




# Load data using a search query



documents = reader.load_data(query="What are the latest advancements in AI?")




# You can also pass additional parameters, for example, to specify the country for the search



documents_with_params = reader.load_data(




query="What are the latest advancements in AI?", params={"country": "US"}





# Create index and query



index = SummaryIndex.from_documents(documents)




query_engine = index.as_query_engine()




response = query_engine.query("List me the headlines")





print(response)


```


```

The Latest AI News and AI Breakthroughs that Matter Most


Advancements in AI and Machine Learning


Top 11 New Technologies in AI: Exploring the Latest Trends


AI News | Latest AI News, Analysis & Events


Year in review: Google's biggest AI advancements of 2024


Clarifying The Latest AI Advancements


5 examples of the most advanced AI | Achieve better ROI now


6 AI trends you'll see more of in 2025


The future of AI: trends shaping the next 10 years


5 AI Trends Shaping Innovation and ROI in 2025

```

# Using Scrapy Web Reader 🕸️
[Section titled “Using Scrapy Web Reader 🕸️”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#using-scrapy-web-reader-%EF%B8%8F)
Scrapy is a popular web crawling framework for Python. The ScrapyWebReader allows you to leverage Scrapy’s powerful crawling capabilities to extract data from websites. It can be used in 2 ways
  1. By providing an Scrapy spider class.
  2. By providing the path to a Scrapy project.


### 1. Using with Scrapy Spider Class
[Section titled “1. Using with Scrapy Spider Class”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#1-using-with-scrapy-spider-class)

```


from scrapy.spiders import Spider




from llama_index.readers.web import ScrapyWebReader






classSampleSpider(Spider):




name ="sample_spider"




start_urls = ["http://quotes.toscrape.com"]





defparse(self, response):







reader = ScrapyWebReader()




docs = reader.load_data(SampleSpider)


```

### 2. Using with Scrapy Project Path
[Section titled “2. Using with Scrapy Project Path”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#2-using-with-scrapy-project-path)
Downloading a Sample Scrapy Project

```


%git clone https://github.com/scrapy/quotesbot.git


```

Using the scrapy project with spider named “toscrape-css”

```


from llama_index.readers.web import ScrapyWebReader





reader = ScrapyWebReader(project_path="./quotesbot")




docs = reader.load_data("toscrape-css")


```

### Metadata
[Section titled “Metadata”](https://developers.llamaindex.ai/python/examples/data_connectors/webpagedemo/#metadata)
Some keys from the scraped items can be stored as metadata in the Document object. You can specify which keys to include as metadata using the `metadata_keys` parameter. If you want to keep the keys in both the content and as metadata, you can set the `keep_keys` parameter to `True`.

```


reader = ScrapyWebReader(




project_path="./quotesbot",




metadata_keys=["author", "tags"],




keep_keys=True,





docs = reader.load_data("toscrape-css")


```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


