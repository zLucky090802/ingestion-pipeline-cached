# Shopify
##  ShopifyToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/shopify/#llama_index.tools.shopify.ShopifyToolSpec "Permanent link")
Bases: 
Shopify tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-shopify/llama_index/tools/shopify/base.py`  
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
```
 | 
```
classShopifyToolSpec(BaseToolSpec):
"""Shopify tool spec."""

    spec_functions = ["run_graphql_query"]

    def__init__(self, shop_url: str, api_version: str, admin_api_key: str):
        # Currently only supports Admin API auth
        # https://shopify.dev/docs/apps/auth/admin-app-access-tokens
        fromshopifyimport Session, ShopifyResource

        session = Session(shop_url, api_version, admin_api_key)
        ShopifyResource.activate_session(session)

    defrun_graphql_query(self, graphql_query: str):
"""
        Run a GraphQL query against the Shopify Admin API.

        Example graphql_query: {
              products (first: 3) {
                edges {
                  node {

                    title
                    handle





        providing this query would return the id, title and handle of the first 3 products
        """
        fromshopifyimport GraphQL

        return GraphQL().execute(graphql_query)

```
 |  
| --- | --- |  
###  run_graphql_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/shopify/#llama_index.tools.shopify.ShopifyToolSpec.run_graphql_query "Permanent link")

```
run_graphql_query(graphql_query: )

```

Run a GraphQL query against the Shopify Admin API.
{
products (first: 3) { edges { node { id title handle } } }
providing this query would return the id, title and handle of the first 3 products
Source code in `llama-index-integrations/tools/llama-index-tools-shopify/llama_index/tools/shopify/base.py`  
| 
```
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
```
 | 
```
defrun_graphql_query(self, graphql_query: str):
"""
    Run a GraphQL query against the Shopify Admin API.

    Example graphql_query: {
          products (first: 3) {
            edges {
              node {

                title
                handle





    providing this query would return the id, title and handle of the first 3 products
    """
    fromshopifyimport GraphQL

    return GraphQL().execute(graphql_query)

```
 |  
| --- | --- |  
options: members: - ShopifyToolSpec
