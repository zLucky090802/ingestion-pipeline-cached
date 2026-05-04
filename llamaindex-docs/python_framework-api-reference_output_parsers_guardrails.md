# Guardrails
##  GuardrailsOutputParser [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/guardrails/#llama_index.output_parsers.guardrails.GuardrailsOutputParser "Permanent link")
Bases: 
Guardrails output parser.
Source code in `llama-index-integrations/output_parsers/llama-index-output-parsers-guardrails/llama_index/output_parsers/guardrails/base.py`  
| 
```
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
```
 | 
```
classGuardrailsOutputParser(BaseOutputParser):
"""Guardrails output parser."""

    def__init__(
        self,
        guard: Guard,
        format_key: Optional[str] = None,
    ):
"""Initialize a Guardrails output parser."""
        self.guard: Guard = guard
        self.format_key = format_key

    @classmethod
    @deprecated(version="0.8.46")
    deffrom_rail(cls, rail: str) -> "GuardrailsOutputParser":
"""From rail."""
        if Guard is None:
            raise ImportError(
                "Guardrails is not installed. Run `pip install guardrails-ai`. "
            )

        return cls(Guard.from_rail(rail))

    @classmethod
    @deprecated(version="0.8.46")
    deffrom_rail_string(cls, rail_string: str) -> "GuardrailsOutputParser":
"""From rail string."""
        if Guard is None:
            raise ImportError(
                "Guardrails is not installed. Run `pip install guardrails-ai`. "
            )

        return cls(Guard.from_rail_string(rail_string))

    defparse(self, output: str, *args: Any, **kwargs: Any) -> Any:
"""Parse, validate, and correct errors programmatically."""
        return self.guard.parse(output, *args, **kwargs).validated_output

    defformat(self, query: str) -> str:
"""Format a query with structured output formatting instructions."""
        output_schema_text = deepcopy(self.guard.rail.prompt)

        # Add format instructions here.
        format_instructions_tmpl = self.guard.raw_prompt.format_instructions
        # NOTE: output_schema is fixed
        format_instructions = format_instructions_tmpl.format(
            output_schema=output_schema_text
        )

        if self.format_key is not None:
            fmt_query = query.format(**{self.format_key: format_instructions})
        else:
            fmt_query = query + "\n\n" + format_instructions

        return fmt_query

```
 |  
| --- | --- |  
###  from_rail `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/guardrails/#llama_index.output_parsers.guardrails.GuardrailsOutputParser.from_rail "Permanent link")

```
from_rail(rail: ) -> 

```

From rail.
Source code in `llama-index-integrations/output_parsers/llama-index-output-parsers-guardrails/llama_index/output_parsers/guardrails/base.py`  
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
```
 | 
```
@classmethod
@deprecated(version="0.8.46")
deffrom_rail(cls, rail: str) -> "GuardrailsOutputParser":
"""From rail."""
    if Guard is None:
        raise ImportError(
            "Guardrails is not installed. Run `pip install guardrails-ai`. "
        )

    return cls(Guard.from_rail(rail))

```
 |  
| --- | --- |  
###  from_rail_string `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/guardrails/#llama_index.output_parsers.guardrails.GuardrailsOutputParser.from_rail_string "Permanent link")

```
from_rail_string(
    rail_string: ,
) -> 

```

From rail string.
Source code in `llama-index-integrations/output_parsers/llama-index-output-parsers-guardrails/llama_index/output_parsers/guardrails/base.py`  
| 
```
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
@classmethod
@deprecated(version="0.8.46")
deffrom_rail_string(cls, rail_string: str) -> "GuardrailsOutputParser":
"""From rail string."""
    if Guard is None:
        raise ImportError(
            "Guardrails is not installed. Run `pip install guardrails-ai`. "
        )

    return cls(Guard.from_rail_string(rail_string))

```
 |  
| --- | --- |  
###  parse [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/guardrails/#llama_index.output_parsers.guardrails.GuardrailsOutputParser.parse "Permanent link")

```
parse(output: , *args: , **kwargs: ) -> 

```

Parse, validate, and correct errors programmatically.
Source code in `llama-index-integrations/output_parsers/llama-index-output-parsers-guardrails/llama_index/output_parsers/guardrails/base.py`  
| 
```
51
52
53
```
 | 
```
defparse(self, output: str, *args: Any, **kwargs: Any) -> Any:
"""Parse, validate, and correct errors programmatically."""
    return self.guard.parse(output, *args, **kwargs).validated_output

```
 |  
| --- | --- |  
###  format [#](https://developers.llamaindex.ai/python/framework-api-reference/output_parsers/guardrails/#llama_index.output_parsers.guardrails.GuardrailsOutputParser.format "Permanent link")

```
format(query: ) -> 

```

Format a query with structured output formatting instructions.
Source code in `llama-index-integrations/output_parsers/llama-index-output-parsers-guardrails/llama_index/output_parsers/guardrails/base.py`  
| 
```
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
```
 | 
```
defformat(self, query: str) -> str:
"""Format a query with structured output formatting instructions."""
    output_schema_text = deepcopy(self.guard.rail.prompt)

    # Add format instructions here.
    format_instructions_tmpl = self.guard.raw_prompt.format_instructions
    # NOTE: output_schema is fixed
    format_instructions = format_instructions_tmpl.format(
        output_schema=output_schema_text
    )

    if self.format_key is not None:
        fmt_query = query.format(**{self.format_key: format_instructions})
    else:
        fmt_query = query + "\n\n" + format_instructions

    return fmt_query

```
 |  
| --- | --- |  
options: members: - GuardrailsOutputParser
