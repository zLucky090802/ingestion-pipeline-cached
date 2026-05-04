# Salesforce
##  SalesforceToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/salesforce/#llama_index.tools.salesforce.SalesforceToolSpec "Permanent link")
Bases: 
Salesforce tool spec.
Gives the agent the ability to interact with Salesforce using simple_salesforce
Source code in `llama-index-integrations/tools/llama-index-tools-salesforce/llama_index/tools/salesforce/base.py`  
| 
```
 4
 5
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
```
 | 
```
classSalesforceToolSpec(BaseToolSpec):
"""
    Salesforce tool spec.

    Gives the agent the ability to interact with Salesforce using simple_salesforce

    """

    spec_functions = ["execute_sosl", "execute_soql"]

    def__init__(self, **kargs) -> None:
"""Initialize with parameters for Salesforce connection."""
        fromsimple_salesforceimport Salesforce

        self.sf = Salesforce(**kargs)

    defexecute_sosl(self, search: str) -> str:
"""
        Returns the result of a Salesforce search as a dict decoded from
        the Salesforce response JSON payload.

        Arguments:
        * search -- the fully formatted SOSL search string, e.g.
                    `FIND {Waldo}`.

        """
        fromsimple_salesforceimport SalesforceError

        try:
            res = self.sf.search(search)
        except SalesforceError as err:
            return f"Error running SOSL query: {err}"
        return res

    defexecute_soql(self, query: str) -> str:
"""
        Returns the full set of results for the `query`. This is a
        convenience wrapper around `query(...)` and `query_more(...)`.
        The returned dict is the decoded JSON payload from the final call to
        Salesforce, but with the `totalSize` field representing the full
        number of results retrieved and the `records` list representing the
        full list of records retrieved.

        Arguments:
        * query -- the SOQL query to send to Salesforce, e.g.
                   SELECT Id FROM Lead WHERE Email = "waldo@somewhere.com".

        """
        fromsimple_salesforceimport SalesforceError

        try:
            res = self.sf.query_all(query)
        except SalesforceError as err:
            return f"Error running SOQL query: {err}"
        return res

```
 |  
| --- | --- |  
###  execute_sosl [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/salesforce/#llama_index.tools.salesforce.SalesforceToolSpec.execute_sosl "Permanent link")

```
execute_sosl(search: ) -> 

```

Returns the result of a Salesforce search as a dict decoded from the Salesforce response JSON payload.
  * search -- the fully formatted SOSL search string, e.g. `FIND {Waldo}`.

Source code in `llama-index-integrations/tools/llama-index-tools-salesforce/llama_index/tools/salesforce/base.py`  
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
```
 | 
```
defexecute_sosl(self, search: str) -> str:
"""
    Returns the result of a Salesforce search as a dict decoded from
    the Salesforce response JSON payload.

    Arguments:
    * search -- the fully formatted SOSL search string, e.g.
                `FIND {Waldo}`.

    """
    fromsimple_salesforceimport SalesforceError

    try:
        res = self.sf.search(search)
    except SalesforceError as err:
        return f"Error running SOSL query: {err}"
    return res

```
 |  
| --- | --- |  
###  execute_soql [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/salesforce/#llama_index.tools.salesforce.SalesforceToolSpec.execute_soql "Permanent link")

```
execute_soql(query: ) -> 

```

Returns the full set of results for the `query`. This is a convenience wrapper around `query(...)` and `query_more(...)`. The returned dict is the decoded JSON payload from the final call to Salesforce, but with the `totalSize` field representing the full number of results retrieved and the `records` list representing the full list of records retrieved.
  * query -- the SOQL query to send to Salesforce, e.g. SELECT Id FROM Lead WHERE Email = "waldo@somewhere.com".

Source code in `llama-index-integrations/tools/llama-index-tools-salesforce/llama_index/tools/salesforce/base.py`  
| 
```
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
```
 | 
```
defexecute_soql(self, query: str) -> str:
"""
    Returns the full set of results for the `query`. This is a
    convenience wrapper around `query(...)` and `query_more(...)`.
    The returned dict is the decoded JSON payload from the final call to
    Salesforce, but with the `totalSize` field representing the full
    number of results retrieved and the `records` list representing the
    full list of records retrieved.

    Arguments:
    * query -- the SOQL query to send to Salesforce, e.g.
               SELECT Id FROM Lead WHERE Email = "waldo@somewhere.com".

    """
    fromsimple_salesforceimport SalesforceError

    try:
        res = self.sf.query_all(query)
    except SalesforceError as err:
        return f"Error running SOQL query: {err}"
    return res

```
 |  
| --- | --- |  
options: members: - SalesforceToolSpec
