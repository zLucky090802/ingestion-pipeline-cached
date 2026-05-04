# Compact accumulate
##  CompactAndAccumulate [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/compact_accumulate/#llama_index.core.response_synthesizers.compact_and_accumulate.CompactAndAccumulate "Permanent link")
Bases: 
Accumulate responses across compact text chunks.
Source code in `llama-index-core/llama_index/core/response_synthesizers/compact_and_accumulate.py`  
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
```
 | 
```
classCompactAndAccumulate(Accumulate):
"""Accumulate responses across compact text chunks."""

    async defaget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        separator: str = "\n---------------------\n",
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Get compact response."""
        # use prompt helper to fix compact text_chunks under the prompt limitation
        text_qa_template = self._text_qa_template.partial_format(query_str=query_str)

        with temp_set_attrs(self._prompt_helper):
            new_texts = self._prompt_helper.repack(
                text_qa_template, text_chunks, llm=self._llm
            )

            return await super().aget_response(
                query_str=query_str,
                text_chunks=new_texts,
                separator=separator,
                **response_kwargs,
            )

    defget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        separator: str = "\n---------------------\n",
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
"""Get compact response."""
        # use prompt helper to fix compact text_chunks under the prompt limitation
        text_qa_template = self._text_qa_template.partial_format(query_str=query_str)

        with temp_set_attrs(self._prompt_helper):
            new_texts = self._prompt_helper.repack(
                text_qa_template, text_chunks, llm=self._llm
            )

            return super().get_response(
                query_str=query_str,
                text_chunks=new_texts,
                separator=separator,
                **response_kwargs,
            )

```
 |  
| --- | --- |  
###  aget_response [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/compact_accumulate/#llama_index.core.response_synthesizers.compact_and_accumulate.CompactAndAccumulate.aget_response "Permanent link")

```
aget_response(
    query_str: ,
    text_chunks: Sequence[],
    separator:  = "\n---------------------\n",
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Get compact response.
Source code in `llama-index-core/llama_index/core/response_synthesizers/compact_and_accumulate.py`  
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
```
 | 
```
async defaget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    separator: str = "\n---------------------\n",
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Get compact response."""
    # use prompt helper to fix compact text_chunks under the prompt limitation
    text_qa_template = self._text_qa_template.partial_format(query_str=query_str)

    with temp_set_attrs(self._prompt_helper):
        new_texts = self._prompt_helper.repack(
            text_qa_template, text_chunks, llm=self._llm
        )

        return await super().aget_response(
            query_str=query_str,
            text_chunks=new_texts,
            separator=separator,
            **response_kwargs,
        )

```
 |  
| --- | --- |  
###  get_response [#](https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/compact_accumulate/#llama_index.core.response_synthesizers.compact_and_accumulate.CompactAndAccumulate.get_response "Permanent link")

```
get_response(
    query_str: ,
    text_chunks: Sequence[],
    separator:  = "\n---------------------\n",
    **response_kwargs: 
) -> RESPONSE_TEXT_TYPE

```

Get compact response.
Source code in `llama-index-core/llama_index/core/response_synthesizers/compact_and_accumulate.py`  
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
```
 | 
```
defget_response(
    self,
    query_str: str,
    text_chunks: Sequence[str],
    separator: str = "\n---------------------\n",
    **response_kwargs: Any,
) -> RESPONSE_TEXT_TYPE:
"""Get compact response."""
    # use prompt helper to fix compact text_chunks under the prompt limitation
    text_qa_template = self._text_qa_template.partial_format(query_str=query_str)

    with temp_set_attrs(self._prompt_helper):
        new_texts = self._prompt_helper.repack(
            text_qa_template, text_chunks, llm=self._llm
        )

        return super().get_response(
            query_str=query_str,
            text_chunks=new_texts,
            separator=separator,
            **response_kwargs,
        )

```
 |  
| --- | --- |  
options: members: - CompactAndAccumulate
