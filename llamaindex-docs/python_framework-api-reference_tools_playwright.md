# Playwright
##  PlaywrightToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec "Permanent link")
Bases: 
Playwright tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
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
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
```
 | 
```
classPlaywrightToolSpec(BaseToolSpec):
"""
    Playwright tool spec.
    """

    spec_functions = [
        "click",
        "fill",
        "get_current_page",
        "extract_hyperlinks",
        "extract_text",
        "get_elements",
        "navigate_to",
        "navigate_back",
    ]

    def__init__(
        self,
        async_browser: Optional[AsyncBrowser] = None,
        visible_only: bool = False,
        playwright_strict: bool = False,
        playwright_timeout: float = 1_000,
        absolute_url: bool = False,
        html_parser: str = "html.parser",
    ) -> None:
"""
        Initialize PlaywrightToolSpec.

        Args:
            async_browser: Optional[AsyncBrowser] = None. A browser instance to use for automation.
            visible_only: bool = True. Whether to only click on visible elements.
            playwright_strict: bool = False. Whether to use strict mode for playwright.
            playwright_timeout: float = 1_000. Timeout for playwright operations.
            absolute_url: bool = False. Whether to return absolute urls.
            html_parser: str = "html.parser". The html parser to use with BeautifulSoup

        """
        self.async_browser = async_browser

        # for click tool
        self.visible_only = visible_only
        self.playwright_strict = playwright_strict
        self.playwright_timeout = playwright_timeout

        # for extractHyperlinks tool
        self.absolute_url = absolute_url
        self.html_parser = html_parser

    @classmethod
    deffrom_async_browser(cls, async_browser: AsyncBrowser) -> "PlaywrightToolSpec":
"""
        Initialize PlaywrightToolSpec from an async browser instance.
        """
        return cls(async_browser=async_browser)

    #################
    # Utils Methods #
    #################
    def_selector_effective(self, selector: str) -> str:
"""
        Get the effective selector.
        """
        if not self.visible_only:
            return selector
        return f"{selector} >> visible=1"

    @staticmethod
    async defcreate_async_playwright_browser(
        headless: bool = True, args: Optional[List[str]] = None
    ) -> AsyncBrowser:
"""
        Create an async playwright browser.

        Args:
            headless: Whether to run the browser in headless mode. Defaults to True.
            args: arguments to pass to browser.chromium.launch

        Returns:
            AsyncBrowser: The playwright browser.

        """
        fromplaywright.async_apiimport async_playwright

        browser = await async_playwright().start()
        return await browser.chromium.launch(headless=headless, args=args)

    async def_aget_current_page(self, browser: AsyncBrowser) -> AsyncPage:
"""
        Get the current page of the async browser.

        Args:
            browser: The browser to get the current page from.

        Returns:
            AsyncPage: The current page.

        """
        if not browser.contexts:
            context = await browser.new_context()
            return await context.new_page()
        context = browser.contexts[
            0
        ]  # Assuming you're using the default browser context
        if not context.pages:
            return await context.new_page()
        # Assuming the last page in the list is the active one
        return context.pages[-1]

    #################
    # Click #
    #################
    async defclick(
        self,
        selector: str,
    ) -> str:
"""
        Click on a web element based on a CSS selector.

        Args:
            selector: The CSS selector for the web element to click on.

        """
        if self.async_browser is None:
            raise ValueError("Async browser is not initialized")

        page = await self._aget_current_page(self.async_browser)
        # Navigate to the desired webpage before using this tool
        selector_effective = self._selector_effective(selector=selector)
        fromplaywright.async_apiimport TimeoutError as PlaywrightTimeoutError

        try:
            await page.click(
                selector_effective,
                strict=self.playwright_strict,
                timeout=self.playwright_timeout,
            )
        except PlaywrightTimeoutError:
            return f"Unable to click on element '{selector}'"
        return f"Clicked element '{selector}'"

    #################
    # Fill #
    #################
    async deffill(
        self,
        selector: str,
        value: str,
    ) -> str:
"""
        Fill an web input field specified by the given CSS selector with the given value.

        Args:
            selector: The CSS selector for the web input field to fill.
            value: The value to fill in.

        """
        if self.async_browser is None:
            raise ValueError("Async browser is not initialized")

        page = await self._aget_current_page(self.async_browser)
        # Navigate to the desired webpage before using this tool
        selector_effective = self._selector_effective(selector=selector)
        fromplaywright.async_apiimport TimeoutError as PlaywrightTimeoutError

        try:
            await page.fill(
                selector_effective,
                value,
                strict=self.playwright_strict,
                timeout=self.playwright_timeout,
            )
        except PlaywrightTimeoutError:
            return f"Unable to fill element '{selector}'"
        return f"Filled element '{selector}'"

    #################
    # Get Current Page #
    #################
    async defget_current_page(self) -> str:
"""
        Get the url of the current web page.
        """
        if self.async_browser is None:
            raise ValueError("Async browser is not initialized")
        page = await self._aget_current_page(self.async_browser)
        return page.url

    #################
    # Extract Hyperlinks #
    #################
    defscrape_page(self, page: Any, html_content: str, absolute_urls: bool) -> str:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, self.html_parser)

        # Find all the anchor elements and extract their href attributes
        anchors = soup.find_all("a")
        if absolute_urls:
            base_url = page.url
            links = [urljoin(base_url, anchor.get("href", "")) for anchor in anchors]
        else:
            links = [anchor.get("href", "") for anchor in anchors]
        # Return the list of links as a JSON string. Duplicated link
        # only appears once in the list
        return json.dumps(list(set(links)))

    async defextract_hyperlinks(self) -> str:
"""
        Extract all hyperlinks from the current web page.
        """
        if self.async_browser is None:
            raise ValueError("Async browser is not initialized")

        page = await self._aget_current_page(self.async_browser)
        html_content = await page.content()
        return self.scrape_page(page, html_content, self.absolute_url)

    #################
    # Extract Text #
    #################
    async defextract_text(self) -> str:
"""
        Extract all text from the current web page.
        """
        if self.async_browser is None:
            raise ValueError("Async browser is not initialized")

        page = await self._aget_current_page(self.async_browser)
        html_content = await page.content()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, self.html_parser)

        return " ".join(text for text in soup.stripped_strings)

    #################
    # Get Elements #
    #################
    async def_aget_elements(
        self, page: AsyncPage, selector: str, attributes: Sequence[str]
    ) -> List[dict]:
"""Get elements matching the given CSS selector."""
        elements = await page.query_selector_all(selector)
        results = []
        for element in elements:
            result = {}
            for attribute in attributes:
                if attribute == "innerText":
                    val: Optional[str] = await element.inner_text()
                else:
                    val = await element.get_attribute(attribute)
                if val is not None and val.strip() != "":
                    result[attribute] = val
            if result:
                results.append(result)
        return results

    async defget_elements(
        self, selector: str, attributes: List[str] = ["innerText"]
    ) -> str:
"""
        Retrieve elements in the current web page matching the given CSS selector.

        Args:
            selector: CSS selector, such as '*', 'div', 'p', 'a', #id, .classname
            attribute: Set of attributes to retrieve for each element

        """
        if self.async_browser is None:
            raise ValueError("Async browser is not initialized")

        page = await self._aget_current_page(self.async_browser)
        results = await self._aget_elements(page, selector, attributes)
        return json.dumps(results, ensure_ascii=False)

    #################
    # Navigate #
    #################
    defvalidate_url(self, url: str):
"""
        Validate the given url.
        """
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ("http", "https"):
            raise ValueError("URL scheme must be 'http' or 'https'")

    async defnavigate_to(
        self,
        url: str,
    ) -> str:
"""
        Navigate to the given url.

        Args:
            url: The url to navigate to.

        """
        if self.async_browser is None:
            raise ValueError("Async browser is not initialized")
        self.validate_url(url)

        page = await self._aget_current_page(self.async_browser)
        response = await page.goto(url)
        status = response.status if response else "unknown"
        return f"Navigating to {url} returned status code {status}"

    #################
    # Navigate Back #
    #################
    async defnavigate_back(self) -> str:
"""
        Navigate back to the previous web page.
        """
        if self.async_browser is None:
            raise ValueError("Async browser is not initialized")
        page = await self._aget_current_page(self.async_browser)
        response = await page.go_back()

        if response:
            return (
                f"Navigated back to the previous page with URL '{response.url}'."
                f" Status code {response.status}"
            )
        else:
            return "Unable to navigate back; no previous page in the history"

```
 |  
| --- | --- |  
###  from_async_browser `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.from_async_browser "Permanent link")

```
from_async_browser(
    async_browser: Browser,
) -> 

```

Initialize PlaywrightToolSpec from an async browser instance.
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
60
61
62
63
64
65
```
 | 
```
@classmethod
deffrom_async_browser(cls, async_browser: AsyncBrowser) -> "PlaywrightToolSpec":
"""
    Initialize PlaywrightToolSpec from an async browser instance.
    """
    return cls(async_browser=async_browser)

```
 |  
| --- | --- |  
###  create_async_playwright_browser `async` `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.create_async_playwright_browser "Permanent link")

```
create_async_playwright_browser(
    headless:  = True, args: Optional[[]] = None
) -> Browser

```

Create an async playwright browser.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `headless`  |  `bool`  |  Whether to run the browser in headless mode. Defaults to True.  |  `True`  |  
|  `args`  |  `Optional[List[str]]`  |  arguments to pass to browser.chromium.launch  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `AsyncBrowser`  |  `Browser`  |  The playwright browser.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
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
```
 | 
```
@staticmethod
async defcreate_async_playwright_browser(
    headless: bool = True, args: Optional[List[str]] = None
) -> AsyncBrowser:
"""
    Create an async playwright browser.

    Args:
        headless: Whether to run the browser in headless mode. Defaults to True.
        args: arguments to pass to browser.chromium.launch

    Returns:
        AsyncBrowser: The playwright browser.

    """
    fromplaywright.async_apiimport async_playwright

    browser = await async_playwright().start()
    return await browser.chromium.launch(headless=headless, args=args)

```
 |  
| --- | --- |  
###  click [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.click "Permanent link")

```
click(selector: ) -> 

```

Click on a web element based on a CSS selector.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  The CSS selector for the web element to click on.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
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
140
141
142
143
144
145
146
147
148
149
150
```
 | 
```
async defclick(
    self,
    selector: str,
) -> str:
"""
    Click on a web element based on a CSS selector.

    Args:
        selector: The CSS selector for the web element to click on.

    """
    if self.async_browser is None:
        raise ValueError("Async browser is not initialized")

    page = await self._aget_current_page(self.async_browser)
    # Navigate to the desired webpage before using this tool
    selector_effective = self._selector_effective(selector=selector)
    fromplaywright.async_apiimport TimeoutError as PlaywrightTimeoutError

    try:
        await page.click(
            selector_effective,
            strict=self.playwright_strict,
            timeout=self.playwright_timeout,
        )
    except PlaywrightTimeoutError:
        return f"Unable to click on element '{selector}'"
    return f"Clicked element '{selector}'"

```
 |  
| --- | --- |  
###  fill [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.fill "Permanent link")

```
fill(selector: , value: ) -> 

```

Fill an web input field specified by the given CSS selector with the given value.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  The CSS selector for the web input field to fill.  |  _required_  |  
|  `value`  |  The value to fill in.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
```
 | 
```
async deffill(
    self,
    selector: str,
    value: str,
) -> str:
"""
    Fill an web input field specified by the given CSS selector with the given value.

    Args:
        selector: The CSS selector for the web input field to fill.
        value: The value to fill in.

    """
    if self.async_browser is None:
        raise ValueError("Async browser is not initialized")

    page = await self._aget_current_page(self.async_browser)
    # Navigate to the desired webpage before using this tool
    selector_effective = self._selector_effective(selector=selector)
    fromplaywright.async_apiimport TimeoutError as PlaywrightTimeoutError

    try:
        await page.fill(
            selector_effective,
            value,
            strict=self.playwright_strict,
            timeout=self.playwright_timeout,
        )
    except PlaywrightTimeoutError:
        return f"Unable to fill element '{selector}'"
    return f"Filled element '{selector}'"

```
 |  
| --- | --- |  
###  get_current_page [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.get_current_page "Permanent link")

```
get_current_page() -> 

```

Get the url of the current web page.
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
190
191
192
193
194
195
196
197
```
 | 
```
async defget_current_page(self) -> str:
"""
    Get the url of the current web page.
    """
    if self.async_browser is None:
        raise ValueError("Async browser is not initialized")
    page = await self._aget_current_page(self.async_browser)
    return page.url

```
 |  
| --- | --- |  
###  extract_hyperlinks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.extract_hyperlinks "Permanent link")

```
extract_hyperlinks() -> 

```

Extract all hyperlinks from the current web page.
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
217
218
219
220
221
222
223
224
225
226
```
 | 
```
async defextract_hyperlinks(self) -> str:
"""
    Extract all hyperlinks from the current web page.
    """
    if self.async_browser is None:
        raise ValueError("Async browser is not initialized")

    page = await self._aget_current_page(self.async_browser)
    html_content = await page.content()
    return self.scrape_page(page, html_content, self.absolute_url)

```
 |  
| --- | --- |  
###  extract_text [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.extract_text "Permanent link")

```
extract_text() -> 

```

Extract all text from the current web page.
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
231
232
233
234
235
236
237
238
239
240
241
242
243
244
```
 | 
```
async defextract_text(self) -> str:
"""
    Extract all text from the current web page.
    """
    if self.async_browser is None:
        raise ValueError("Async browser is not initialized")

    page = await self._aget_current_page(self.async_browser)
    html_content = await page.content()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, self.html_parser)

    return " ".join(text for text in soup.stripped_strings)

```
 |  
| --- | --- |  
###  get_elements [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.get_elements "Permanent link")

```
get_elements(
    selector: , attributes: [] = ["innerText"]
) -> 

```

Retrieve elements in the current web page matching the given CSS selector.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  CSS selector, such as '*', 'div', 'p', 'a', #id, .classname  |  _required_  |  
|  `attribute`  |  Set of attributes to retrieve for each element  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
```
 | 
```
async defget_elements(
    self, selector: str, attributes: List[str] = ["innerText"]
) -> str:
"""
    Retrieve elements in the current web page matching the given CSS selector.

    Args:
        selector: CSS selector, such as '*', 'div', 'p', 'a', #id, .classname
        attribute: Set of attributes to retrieve for each element

    """
    if self.async_browser is None:
        raise ValueError("Async browser is not initialized")

    page = await self._aget_current_page(self.async_browser)
    results = await self._aget_elements(page, selector, attributes)
    return json.dumps(results, ensure_ascii=False)

```
 |  
| --- | --- |  
###  validate_url [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.validate_url "Permanent link")

```
validate_url(url: )

```

Validate the given url.
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
289
290
291
292
293
294
295
```
 | 
```
defvalidate_url(self, url: str):
"""
    Validate the given url.
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be 'http' or 'https'")

```
 |  
| --- | --- |  
###  navigate_to [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.navigate_to "Permanent link")

```
navigate_to(url: ) -> 

```

Navigate to the given url.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  The url to navigate to.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
```
 | 
```
async defnavigate_to(
    self,
    url: str,
) -> str:
"""
    Navigate to the given url.

    Args:
        url: The url to navigate to.

    """
    if self.async_browser is None:
        raise ValueError("Async browser is not initialized")
    self.validate_url(url)

    page = await self._aget_current_page(self.async_browser)
    response = await page.goto(url)
    status = response.status if response else "unknown"
    return f"Navigating to {url} returned status code {status}"

```
 |  
| --- | --- |  
###  navigate_back [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/playwright/#llama_index.tools.playwright.PlaywrightToolSpec.navigate_back "Permanent link")

```
navigate_back() -> 

```

Navigate back to the previous web page.
Source code in `llama-index-integrations/tools/llama-index-tools-playwright/llama_index/tools/playwright/base.py`  
| 
```
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
```
 | 
```
async defnavigate_back(self) -> str:
"""
    Navigate back to the previous web page.
    """
    if self.async_browser is None:
        raise ValueError("Async browser is not initialized")
    page = await self._aget_current_page(self.async_browser)
    response = await page.go_back()

    if response:
        return (
            f"Navigated back to the previous page with URL '{response.url}'."
            f" Status code {response.status}"
        )
    else:
        return "Unable to navigate back; no previous page in the history"

```
 |  
| --- | --- |  
options: members: - PlaywrightToolSpec
