# Ionic shopping
##  IonicShoppingToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/ionic_shopping/#llama_index.tools.ionic_shopping.IonicShoppingToolSpec "Permanent link")
Bases: 
Ionic Shopping tool spec.
This tool can be used to build e-commerce experiences with LLMs.
Source code in `llama-index-integrations/tools/llama-index-tools-ionic-shopping/llama_index/tools/ionic_shopping/base.py`  
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
```
 | 
```
classIonicShoppingToolSpec(BaseToolSpec):
"""
    Ionic Shopping tool spec.

    This tool can be used to build e-commerce experiences with LLMs.
    """

    spec_functions = ["query"]

    def__init__(self, api_key: Optional[str] = None) -> None:
"""
        Ionic API Key.

        Learn more about attribution with Ionic API Keys
        https://docs.ioniccommerce.com/guides/attribution
        """
        fromionicimport Ionic as IonicSDK

        if api_key:
            self.client = IonicSDK(api_key_header=api_key)
        else:
            self.client = IonicSDK()

    defquery(
        self,
        query: str,
        num_results: Optional[int] = 5,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
    ) -> list[Product]:
"""
        Use this function to search for products and to get product recommendations.

        Args:
            query (str): A precise query of a product name or product category
            num_results (Optional[int]): Defaults to 5. The number of product results to return.
            min_price (Option[int]): The minimum price in cents the requester is willing to pay
            max_price (Option[int]): The maximum price in cents the requester is willing to pay

        """
        request = QueryAPIRequest(
            query=SDKQuery(
                query=query,
                num_results=num_results,
                min_price=min_price,
                max_price=max_price,
            )
        )
        response: QueryResponse = self.client.query(
            request=request,
            security=QuerySecurity(),
        )

        return [
            product
            for result in response.query_api_response.results
            for product in result.products
        ]

```
 |  
| --- | --- |  
###  query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/ionic_shopping/#llama_index.tools.ionic_shopping.IonicShoppingToolSpec.query "Permanent link")

```
query(
    query: ,
    num_results: Optional[] = 5,
    min_price: Optional[] = None,
    max_price: Optional[] = None,
) -> [Product]

```

Use this function to search for products and to get product recommendations.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  A precise query of a product name or product category  |  _required_  |  
|  `num_results`  |  `Optional[int]`  |  Defaults to 5. The number of product results to return.  |  
|  `min_price`  |  `Option[int]`  |  The minimum price in cents the requester is willing to pay  |  `None`  |  
|  `max_price`  |  `Option[int]`  |  The maximum price in cents the requester is willing to pay  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-ionic-shopping/llama_index/tools/ionic_shopping/base.py`  
| 
```
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
```
 | 
```
defquery(
    self,
    query: str,
    num_results: Optional[int] = 5,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
) -> list[Product]:
"""
    Use this function to search for products and to get product recommendations.

    Args:
        query (str): A precise query of a product name or product category
        num_results (Optional[int]): Defaults to 5. The number of product results to return.
        min_price (Option[int]): The minimum price in cents the requester is willing to pay
        max_price (Option[int]): The maximum price in cents the requester is willing to pay

    """
    request = QueryAPIRequest(
        query=SDKQuery(
            query=query,
            num_results=num_results,
            min_price=min_price,
            max_price=max_price,
        )
    )
    response: QueryResponse = self.client.query(
        request=request,
        security=QuerySecurity(),
    )

    return [
        product
        for result in response.query_api_response.results
        for product in result.products
    ]

```
 |  
| --- | --- |  
options: members: - IonicShoppingToolSpec
