# Langchain
##  LangchainOutputParser [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/langchain/#llama_index.output_parsers.langchain.LangchainOutputParser "Permanent link")
Bases: 
Langchain output parser.
Source code in `llama-index-integrations/output_parsers/llama-index-output-parsers-langchain/llama_index/output_parsers/langchain/base.py`  
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
```
 | 
```
classLangchainOutputParser(BaseOutputParser):
"""Langchain output parser."""

    def__init__(
        self, output_parser: "LCOutputParser", format_key: Optional[str] = None
    ) -> None:
"""Init params."""
        self._output_parser = output_parser
        self._format_key = format_key

    defparse(self, output: str) -> Any:
"""Parse, validate, and correct errors programmatically."""
        # TODO: this object may be stringified by our upstream llmpredictor,
        # figure out better
        # ways to "convert" the object to a proper string format.
        return self._output_parser.parse(output)

    defformat(self, query: str) -> str:
"""Format a query with structured output formatting instructions."""
        format_instructions = self._output_parser.get_format_instructions()

        # TODO: this is a temporary hack. if there's curly brackets in the format
        # instructions (and query is a string template), we need to
        # escape the curly brackets in the format instructions to preserve the
        # overall template.
        query_tmpl_vars = {
            v for _, v, _, _ in Formatter().parse(query) if v is not None
        }
        if len(query_tmpl_vars)  0:
            format_instructions = format_instructions.replace("{", "{{")
            format_instructions = format_instructions.replace("}", "}}")

        if self._format_key is not None:
            fmt_query = query.format(**{self._format_key: format_instructions})
        else:
            fmt_query = query + "\n\n" + format_instructions

        return fmt_query

```
 |  
| --- | --- |  
###  parse [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/langchain/#llama_index.output_parsers.langchain.LangchainOutputParser.parse "Permanent link")

```
parse(output: ) -> 

```

Parse, validate, and correct errors programmatically.
Source code in `llama-index-integrations/output_parsers/llama-index-output-parsers-langchain/llama_index/output_parsers/langchain/base.py`  
| 
```
22
23
24
25
26
27
```
 | 
```
defparse(self, output: str) -> Any:
"""Parse, validate, and correct errors programmatically."""
    # TODO: this object may be stringified by our upstream llmpredictor,
    # figure out better
    # ways to "convert" the object to a proper string format.
    return self._output_parser.parse(output)

```
 |  
| --- | --- |  
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/langchain/#llama_index.output_parsers.langchain.LangchainOutputParser.format "Permanent link")

```
format(query: ) -> 

```

Format a query with structured output formatting instructions.
Source code in `llama-index-integrations/output_parsers/llama-index-output-parsers-langchain/llama_index/output_parsers/langchain/base.py`  
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
```
 | 
```
defformat(self, query: str) -> str:
"""Format a query with structured output formatting instructions."""
    format_instructions = self._output_parser.get_format_instructions()

    # TODO: this is a temporary hack. if there's curly brackets in the format
    # instructions (and query is a string template), we need to
    # escape the curly brackets in the format instructions to preserve the
    # overall template.
    query_tmpl_vars = {
        v for _, v, _, _ in Formatter().parse(query) if v is not None
    }
    if len(query_tmpl_vars)  0:
        format_instructions = format_instructions.replace("{", "{{")
        format_instructions = format_instructions.replace("}", "}}")

    if self._format_key is not None:
        fmt_query = query.format(**{self._format_key: format_instructions})
    else:
        fmt_query = query + "\n\n" + format_instructions

    return fmt_query

```
 |  
| --- | --- |  
options: members: - LangchainOutputParser
