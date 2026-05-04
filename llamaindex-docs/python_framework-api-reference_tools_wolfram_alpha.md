# Wolfram alpha
##  WolframAlphaToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/wolfram_alpha/#llama_index.tools.wolfram_alpha.WolframAlphaToolSpec "Permanent link")
Bases: 
Wolfram Alpha tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-wolfram-alpha/llama_index/tools/wolfram_alpha/base.py`  
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
```
 | 
```
classWolframAlphaToolSpec(BaseToolSpec):
"""Wolfram Alpha tool spec."""

    spec_functions = ["wolfram_alpha_query"]

    def__init__(
        self,
        app_id: Optional[str] = None,
        api_params: Optional[dict] = None,
    ) -> None:
"""Initialize with parameters."""
        self.token = app_id
        self._api_params = api_params or {}

    defwolfram_alpha_query(self, query: str) -> str:
r"""
        Query Wolfram|Alpha for computational knowledge.

        WolframAlpha understands natural language queries about entities in
        chemistry, physics, geography, history, art, astronomy, and more.
        WolframAlpha performs mathematical calculations, date and unit
        conversions, formula solving, etc.

        QUERY FORMAT:
        - Convert inputs to simplified keyword queries whenever possible
          (e.g., "how many people live in France" -> "France population")
        - Send queries in English only; translate non-English queries before
          sending, then respond in the original language
        - Query must be a single-line string

        MATH AND UNITS:
        - ALWAYS use this exponent notation: 6*10^14, NEVER 6e14
        - Use ONLY single-letter variable names, with or without integer
          subscript (e.g., n, n1, n_1)
        - Use named physical constants (e.g., "speed of light") without
          numerical substitution
        - Include a space between compound units (e.g., "Ω m" for "ohm*meter")
        - To solve for a variable in an equation with units, consider solving
          a corresponding equation without units; exclude counting units
          (e.g., books), include genuine units (e.g., kg)

        MULTIPLE PROPERTIES:
        - If data for multiple properties is needed, make separate calls for
          each property

        HANDLING RESULTS:
        - Display image URLs with Markdown syntax: ![URL]
        - Use proper Markdown formatting for all math, scientific, and chemical
          formulas, symbols, etc.: '$$\n[expression]\n$$' for standalone
          cases and '\( [expression] \)' when inline
        - Never mention your knowledge cutoff date; Wolfram may return more
          recent data
        - If a WolframAlpha result is not relevant to the query:
          - If Wolfram provides multiple 'Assumptions' for a query, choose the
            more relevant one(s) without explaining the initial result
          - Re-send the exact same 'input' with NO modifications, and add the
            'assumption' parameter with the relevant values
          - ONLY simplify or rephrase the initial query if a more relevant
            'Assumption' or other input suggestions are not provided
          - Do not explain each step unless user input is needed; proceed
            directly to making a better API call based on available assumptions

        Args:
            query (str): The query to be passed to wolfram alpha.

        """
        params = {"input": query, **self._api_params}
        url = f"{QUERY_URL_TMPL}?{urllib.parse.urlencode(params)}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

```
 |  
| --- | --- |  
###  wolfram_alpha_query [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/wolfram_alpha/#llama_index.tools.wolfram_alpha.WolframAlphaToolSpec.wolfram_alpha_query "Permanent link")

```
wolfram_alpha_query(query: ) -> 

```

Query Wolfram|Alpha for computational knowledge.
WolframAlpha understands natural language queries about entities in chemistry, physics, geography, history, art, astronomy, and more. WolframAlpha performs mathematical calculations, date and unit conversions, formula solving, etc.
QUERY FORMAT: - Convert inputs to simplified keyword queries whenever possible (e.g., "how many people live in France" -> "France population") - Send queries in English only; translate non-English queries before sending, then respond in the original language - Query must be a single-line string
MATH AND UNITS: - ALWAYS use this exponent notation: 6 _10^14, NEVER 6e14 - Use ONLY single-letter variable names, with or without integer subscript (e.g., n, n1, n_1) - Use named physical constants (e.g., "speed of light") without numerical substitution - Include a space between compound units (e.g., "Ω m" for "ohm_ meter") - To solve for a variable in an equation with units, consider solving a corresponding equation without units; exclude counting units (e.g., books), include genuine units (e.g., kg)
MULTIPLE PROPERTIES: - If data for multiple properties is needed, make separate calls for each property
HANDLING RESULTS: - Display image URLs with Markdown syntax: ![URL] - Use proper Markdown formatting for all math, scientific, and chemical formulas, symbols, etc.: '$$\n[expression]\n$$' for standalone cases and '( [expression] )' when inline - Never mention your knowledge cutoff date; Wolfram may return more recent data - If a WolframAlpha result is not relevant to the query: - If Wolfram provides multiple 'Assumptions' for a query, choose the more relevant one(s) without explaining the initial result - Re-send the exact same 'input' with NO modifications, and add the 'assumption' parameter with the relevant values - ONLY simplify or rephrase the initial query if a more relevant 'Assumption' or other input suggestions are not provided - Do not explain each step unless user input is needed; proceed directly to making a better API call based on available assumptions
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to wolfram alpha.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-wolfram-alpha/llama_index/tools/wolfram_alpha/base.py`  
| 
```
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
```
 | 
```
defwolfram_alpha_query(self, query: str) -> str:
r"""
    Query Wolfram|Alpha for computational knowledge.

    WolframAlpha understands natural language queries about entities in
    chemistry, physics, geography, history, art, astronomy, and more.
    WolframAlpha performs mathematical calculations, date and unit
    conversions, formula solving, etc.

    QUERY FORMAT:
    - Convert inputs to simplified keyword queries whenever possible
      (e.g., "how many people live in France" -> "France population")
    - Send queries in English only; translate non-English queries before
      sending, then respond in the original language
    - Query must be a single-line string

    MATH AND UNITS:
    - ALWAYS use this exponent notation: 6*10^14, NEVER 6e14
    - Use ONLY single-letter variable names, with or without integer
      subscript (e.g., n, n1, n_1)
    - Use named physical constants (e.g., "speed of light") without
      numerical substitution
    - Include a space between compound units (e.g., "Ω m" for "ohm*meter")
    - To solve for a variable in an equation with units, consider solving
      a corresponding equation without units; exclude counting units
      (e.g., books), include genuine units (e.g., kg)

    MULTIPLE PROPERTIES:
    - If data for multiple properties is needed, make separate calls for
      each property

    HANDLING RESULTS:
    - Display image URLs with Markdown syntax: ![URL]
    - Use proper Markdown formatting for all math, scientific, and chemical
      formulas, symbols, etc.: '$$\n[expression]\n$$' for standalone
      cases and '\( [expression] \)' when inline
    - Never mention your knowledge cutoff date; Wolfram may return more
      recent data
    - If a WolframAlpha result is not relevant to the query:
      - If Wolfram provides multiple 'Assumptions' for a query, choose the
        more relevant one(s) without explaining the initial result
      - Re-send the exact same 'input' with NO modifications, and add the
        'assumption' parameter with the relevant values
      - ONLY simplify or rephrase the initial query if a more relevant
        'Assumption' or other input suggestions are not provided
      - Do not explain each step unless user input is needed; proceed
        directly to making a better API call based on available assumptions

    Args:
        query (str): The query to be passed to wolfram alpha.

    """
    params = {"input": query, **self._api_params}
    url = f"{QUERY_URL_TMPL}?{urllib.parse.urlencode(params)}"
    headers = {"Authorization": f"Bearer {self.token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

```
 |  
| --- | --- |  
options: members: - WolframAlphaToolSpec
