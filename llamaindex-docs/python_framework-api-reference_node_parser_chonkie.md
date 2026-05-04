# Chonkie
LlamaIndex Chonkie integration for text chunking.
##  Chunker [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/chonkie/#llama_index.node_parser.chonkie.Chunker "Permanent link")
Bases: 
Wrapper for Chonkie's chunkers.
This class integrates Chonkie's chunking functionality with LlamaIndex's MetadataAwareTextSplitter interface.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-chonkie/llama_index/node_parser/chonkie/chunkers.py`  
| 
```
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
```
 | 
```
classChunker(MetadataAwareTextSplitter):
"""
    Wrapper for Chonkie's chunkers.

    This class integrates Chonkie's chunking functionality with LlamaIndex's
    MetadataAwareTextSplitter interface.
    """

    # this is related to the metadata schema in the super, or pydantic will fail
    #  attributes need to be defined as pydantic fields
    chunker: Optional[BaseChunker] = Field(default=None, exclude=True)

    valid_chunker_aliases: List[str] = Field(
        default_factory=lambda: CHUNKERS, exclude=True
    )
    _logged_warning_for_incompatible_chunker: bool = False

    def__init__(
        self,
        chunker: Union[str, BaseChunker] = "recursive",
        callback_manager: Optional[CallbackManager] = None,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        id_func: Optional[Callable] = None,
        **kwargs: Any,
    ):
"""
        Initialize with a Chonkie chunker instance or create one if not provided.

        Args:
            chunker (Union[str, BaseChunker]): The chunker to use. Must be one of {CHUNKERS}
                or a chonkie chunker instance.
            callback_manager (Optional[CallbackManager]): Callback manager for handling callbacks.
            include_metadata (bool): Whether to include metadata in the nodes.
            include_prev_next_rel (bool): Whether to include previous/next relationships.
            id_func (Optional[Callable]): Function to generate node IDs.
            **kwargs: Additional keyword arguments for the underlying Chonkie chunker.

        """
        id_func = id_func or default_id_func
        callback_manager = callback_manager or CallbackManager([])
        super().__init__(
            callback_manager=callback_manager,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            id_func=id_func,
        )

        if isinstance(chunker, str) and chunker not in self.valid_chunker_aliases:
            raise ValueError(
                f"Invalid chunker '{chunker}'. Must be one of: {self.valid_chunker_aliases}"
            )

        if isinstance(chunker, str):
            # flexible approach to pull chunker classes based on their alias
            ChunkingClass = ComponentRegistry.get_chunker(chunker).component_class
            self.chunker = ChunkingClass(**kwargs)
        else:
            self.chunker = chunker

    @classmethod
    deffrom_defaults(
        cls,
        callback_manager: Optional[CallbackManager] = None,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
    ) -> "Chunker":
"""Initialize with parameters."""
        callback_manager = callback_manager or CallbackManager([])
        return cls(
            callback_manager=callback_manager,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
        )

    @classmethod
    defclass_name(cls) -> str:
        return "Chunker"

    defsplit_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]:
"""Split text with metadata awareness."""
        # only apply metadata-aware chunking if the chunker is compatible (counter-example fast)
        if (
            hasattr(self.chunker, "_tokenizer")
            and (self.chunker._tokenizer is not None)
            and hasattr(self.chunker, "chunk_size")
            and self.chunker.chunk_size is not None
        ):
            # count tokens and update chunk_size
            num_tokens = self.chunker._tokenizer.count_tokens(metadata_str)
            original_chunk_size = self.chunker.chunk_size
            effective_chunk_size = original_chunk_size - num_tokens
            self.chunker.chunk_size = effective_chunk_size
            if effective_chunk_size <= 0:
                raise ValueError(
                    f"Metadata length ({num_tokens} tokens) is longer than or equal to "
                    f"chunk size ({original_chunk_size}). Consider increasing the chunk size or "
                    "decreasing the size of your metadata to avoid this."
                )
            splits = self.split_text(text)
            # reset chunk_size to original value after splitting
            self.chunker.chunk_size = original_chunk_size
            return splits
        # fallback mechanism for incompatible chunkers (only logs a warning once per instance)
        if not self._logged_warning_for_incompatible_chunker:
            logger.warning(
                "current chunker type does not support metadata awareness. Proceeding with regular chunking."
                " This warning will only be logged once per instance."
            )
            self._logged_warning_for_incompatible_chunker = True
        return self.split_text(text)

    defsplit_text(self, text: str) -> List[str]:
"""Split incoming text and return chunks using Chonkie chunker."""
        if text == "":
            return [text]

        if self.chunker is None:
            raise ValueError("Chunker not initialized")
        chunks = self.chunker.chunk(text)

        # extract attributes from chonkie Chunk dataclass
        # see https://github.com/chonkie-inc/chonkie/blob/cd8bd643bd7045686f0a8b73a64f1c9296c0dae2/src/chonkie/types/base.py#L32-L38
        if isinstance(chunks, list):
            return [
                chunk.text if hasattr(chunk, "text") else str(chunk) for chunk in chunks
            ]
        else:
            return [chunks.text if hasattr(chunks, "text") else str(chunks)]

```
 |  
| --- | --- |  
###  from_defaults `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/chonkie/#llama_index.node_parser.chonkie.Chunker.from_defaults "Permanent link")

```
from_defaults(
    callback_manager: Optional[] = None,
    include_metadata:  = True,
    include_prev_next_rel:  = True,
) -> 

```

Initialize with parameters.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-chonkie/llama_index/node_parser/chonkie/chunkers.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_defaults(
    cls,
    callback_manager: Optional[CallbackManager] = None,
    include_metadata: bool = True,
    include_prev_next_rel: bool = True,
) -> "Chunker":
"""Initialize with parameters."""
    callback_manager = callback_manager or CallbackManager([])
    return cls(
        callback_manager=callback_manager,
        include_metadata=include_metadata,
        include_prev_next_rel=include_prev_next_rel,
    )

```
 |  
| --- | --- |  
###  split_text_metadata_aware [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/chonkie/#llama_index.node_parser.chonkie.Chunker.split_text_metadata_aware "Permanent link")

```
split_text_metadata_aware(
    text: , metadata_str: 
) -> []

```

Split text with metadata awareness.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-chonkie/llama_index/node_parser/chonkie/chunkers.py`  
| 
```
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
```
 | 
```
defsplit_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]:
"""Split text with metadata awareness."""
    # only apply metadata-aware chunking if the chunker is compatible (counter-example fast)
    if (
        hasattr(self.chunker, "_tokenizer")
        and (self.chunker._tokenizer is not None)
        and hasattr(self.chunker, "chunk_size")
        and self.chunker.chunk_size is not None
    ):
        # count tokens and update chunk_size
        num_tokens = self.chunker._tokenizer.count_tokens(metadata_str)
        original_chunk_size = self.chunker.chunk_size
        effective_chunk_size = original_chunk_size - num_tokens
        self.chunker.chunk_size = effective_chunk_size
        if effective_chunk_size <= 0:
            raise ValueError(
                f"Metadata length ({num_tokens} tokens) is longer than or equal to "
                f"chunk size ({original_chunk_size}). Consider increasing the chunk size or "
                "decreasing the size of your metadata to avoid this."
            )
        splits = self.split_text(text)
        # reset chunk_size to original value after splitting
        self.chunker.chunk_size = original_chunk_size
        return splits
    # fallback mechanism for incompatible chunkers (only logs a warning once per instance)
    if not self._logged_warning_for_incompatible_chunker:
        logger.warning(
            "current chunker type does not support metadata awareness. Proceeding with regular chunking."
            " This warning will only be logged once per instance."
        )
        self._logged_warning_for_incompatible_chunker = True
    return self.split_text(text)

```
 |  
| --- | --- |  
###  split_text [#](https://developers.llamaindex.ai/python/framework-api-reference/node_parser/chonkie/#llama_index.node_parser.chonkie.Chunker.split_text "Permanent link")

```
split_text(text: ) -> []

```

Split incoming text and return chunks using Chonkie chunker.
Source code in `llama-index-integrations/node_parser/llama-index-node-parser-chonkie/llama_index/node_parser/chonkie/chunkers.py`  
| 
```
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
```
 | 
```
defsplit_text(self, text: str) -> List[str]:
"""Split incoming text and return chunks using Chonkie chunker."""
    if text == "":
        return [text]

    if self.chunker is None:
        raise ValueError("Chunker not initialized")
    chunks = self.chunker.chunk(text)

    # extract attributes from chonkie Chunk dataclass
    # see https://github.com/chonkie-inc/chonkie/blob/cd8bd643bd7045686f0a8b73a64f1c9296c0dae2/src/chonkie/types/base.py#L32-L38
    if isinstance(chunks, list):
        return [
            chunk.text if hasattr(chunk, "text") else str(chunk) for chunk in chunks
        ]
    else:
        return [chunks.text if hasattr(chunks, "text") else str(chunks)]

```
 |  
| --- | --- |  
options: members: - Chunker
