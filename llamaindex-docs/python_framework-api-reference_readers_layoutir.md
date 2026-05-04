# Layoutir
##  LayoutIRReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/layoutir/#llama_index.readers.layoutir.LayoutIRReader "Permanent link")
Bases: 
LayoutIR Reader.
Production-grade document ingestion engine using LayoutIR's compiler-like architecture. Processes PDFs and documents through IR (Intermediate Representation) to preserve complex layouts, tables, and multi-column structures.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `use_gpu`  |  `bool`  |  Whether to use GPU acceleration. Defaults to False.  |  _required_  |  
|  `api_key`  |  `Optional[str]`  |  API key for remote processing. Defaults to None.  |  _required_  |  
|  `model_name`  |  `Optional[str]`  |  Model name to use for processing. Defaults to None.  |  _required_  |  
|  `chunk_strategy`  |  Chunking strategy to use. Options: "semantic", "fixed". Defaults to "semantic".  |  _required_  |  
|  `max_heading_level`  |  Maximum heading level for semantic chunking. Defaults to 2.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-layoutir/llama_index/readers/layoutir/base.py`  
| 
```
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
```
 | 
```
classLayoutIRReader(BasePydanticReader):
"""
    LayoutIR Reader.

    Production-grade document ingestion engine using LayoutIR's compiler-like architecture.
    Processes PDFs and documents through IR (Intermediate Representation) to preserve
    complex layouts, tables, and multi-column structures.

    Args:
        use_gpu (bool, optional): Whether to use GPU acceleration. Defaults to False.
        api_key (Optional[str], optional): API key for remote processing. Defaults to None.
        model_name (Optional[str], optional): Model name to use for processing. Defaults to None.
        chunk_strategy (str, optional): Chunking strategy to use. Options: "semantic", "fixed". Defaults to "semantic".
        max_heading_level (int, optional): Maximum heading level for semantic chunking. Defaults to 2.

    """

    use_gpu: bool = Field(
        default=False,
        description="Whether to use GPU acceleration for document processing.",
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API key for remote LayoutIR processing.",
    )
    model_name: Optional[str] = Field(
        default=None,
        description="Model name to use for document processing.",
    )
    chunk_strategy: str = Field(
        default="semantic",
        description="Chunking strategy: 'semantic' for section-based, 'fixed' for fixed-size chunks.",
    )
    max_heading_level: int = Field(
        default=2,
        description="Maximum heading level for semantic chunking.",
    )
    is_remote: bool = Field(
        default=False,
        description="Whether the data is loaded from a remote API or a local file.",
    )

    deflazy_load_data(
        self,
        file_path: Union[str, Path, List[str], List[Path]],
        extra_info: Optional[Dict[str, Any]] = None,
    ) -> Iterable[Document]:
"""
        Lazily load documents from given file path(s) using LayoutIR.

        Args:
            file_path (Union[str, Path, List[str], List[Path]]): Path to PDF/document file(s).
            extra_info (Optional[Dict[str, Any]], optional): Additional metadata to include. Defaults to None.

        Yields:
            Document: LlamaIndex Document objects with preserved layout structure.

        Raises:
            ImportError: If GPU is requested but PyTorch is not installed.

        """
        # Check GPU requirements if use_gpu is enabled
        if self.use_gpu:
            try:
                importtorch  # noqa: F401
            except ImportError as e:
                raise ImportError(
                    "GPU acceleration requested but PyTorch is not installed. "
                    "Please install PyTorch with CUDA support:\n"
                    "pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu130"
                ) frome

        # Normalize file_path to list
        file_paths = file_path if isinstance(file_path, list) else [file_path]

        # Initialize LayoutIR components
        adapter_kwargs = {"use_gpu": self.use_gpu}
        if self.model_name:
            adapter_kwargs["model_name"] = self.model_name
        if self.api_key:
            adapter_kwargs["api_key"] = self.api_key

        adapter = DoclingAdapter(**adapter_kwargs)

        # Setup chunking strategy
        if self.chunk_strategy == "semantic":
            chunker = SemanticSectionChunker(max_heading_level=self.max_heading_level)
        else:
            chunker = None  # Use default chunking

        pipeline = Pipeline(adapter=adapter, chunk_strategy=chunker)

        # Process each file
        for source in file_paths:
            source_path = Path(source) if isinstance(source, str) else source

            # Use a temp directory for LayoutIR output, cleaned up after processing
            tmp_dir = tempfile.mkdtemp()
            try:
                layoutir_doc = pipeline.process(
                    input_path=source_path,
                    output_dir=Path(tmp_dir),
                )
            finally:
                shutil.rmtree(tmp_dir, ignore_errors=True)

            # Extract blocks/chunks from the IR
            if hasattr(layoutir_doc, "blocks"):
                blocks = layoutir_doc.blocks
            elif hasattr(layoutir_doc, "chunks"):
                blocks = layoutir_doc.chunks
            else:
                # Fallback: treat entire document as single block
                blocks = [{"text": str(layoutir_doc), "type": "document"}]

            # Convert each block to a LlamaIndex Document
            for idx, block in enumerate(blocks):
                # Extract text content from layoutir.schema.Block objects
                if isinstance(block, dict):
                    text = block.get("text", block.get("content", ""))
                    block_type = str(block.get("type", "unknown"))
                    block_id = block.get("id", f"{source_path.stem}_block_{idx}")
                    page_number = block.get("page", block.get("page_number", 0))
                elif hasattr(block, "content"):
                    text = block.content or ""
                    block_type = (
                        str(block.type.value)
                        if hasattr(block.type, "value")
                        else str(block.type)
                    )
                    block_id = getattr(
                        block, "block_id", f"{source_path.stem}_block_{idx}"
                    )
                    page_number = getattr(block, "page_number", 0)
                else:
                    text = str(block)
                    block_type = "block"
                    block_id = f"{source_path.stem}_block_{idx}"
                    page_number = 0

                # Create metadata
                metadata = extra_info.copy() if extra_info else {}
                metadata.update(
                    {
                        "file_path": str(source_path),
                        "file_name": source_path.name,
                        "block_type": block_type,
                        "block_index": idx,
                        "page_number": page_number,
                        "source": "layoutir",
                    }
                )

                # Create and yield Document
                doc = Document(
                    doc_id=block_id,
                    text=text,
                    metadata=metadata,
                )

                yield doc

```
 |  
| --- | --- |  
###  lazy_load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/layoutir/#llama_index.readers.layoutir.LayoutIRReader.lazy_load_data "Permanent link")

```
lazy_load_data(
    file_path: Union[, , [], []],
    extra_info: Optional[[, ]] = None,
) -> Iterable[]

```

Lazily load documents from given file path(s) using LayoutIR.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_path`  |  `Union[str, Path, List[str], List[Path]]`  |  Path to PDF/document file(s).  |  _required_  |  
|  `extra_info`  |  `Optional[Dict[str, Any]]`  |  Additional metadata to include. Defaults to None.  |  `None`  |  
Yields:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `Document`  |  `Iterable[Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  LlamaIndex Document objects with preserved layout structure.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ImportError`  |  If GPU is requested but PyTorch is not installed.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-layoutir/llama_index/readers/layoutir/base.py`  
| 
```
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
```
 | 
```
deflazy_load_data(
    self,
    file_path: Union[str, Path, List[str], List[Path]],
    extra_info: Optional[Dict[str, Any]] = None,
) -> Iterable[Document]:
"""
    Lazily load documents from given file path(s) using LayoutIR.

    Args:
        file_path (Union[str, Path, List[str], List[Path]]): Path to PDF/document file(s).
        extra_info (Optional[Dict[str, Any]], optional): Additional metadata to include. Defaults to None.

    Yields:
        Document: LlamaIndex Document objects with preserved layout structure.

    Raises:
        ImportError: If GPU is requested but PyTorch is not installed.

    """
    # Check GPU requirements if use_gpu is enabled
    if self.use_gpu:
        try:
            importtorch  # noqa: F401
        except ImportError as e:
            raise ImportError(
                "GPU acceleration requested but PyTorch is not installed. "
                "Please install PyTorch with CUDA support:\n"
                "pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu130"
            ) frome

    # Normalize file_path to list
    file_paths = file_path if isinstance(file_path, list) else [file_path]

    # Initialize LayoutIR components
    adapter_kwargs = {"use_gpu": self.use_gpu}
    if self.model_name:
        adapter_kwargs["model_name"] = self.model_name
    if self.api_key:
        adapter_kwargs["api_key"] = self.api_key

    adapter = DoclingAdapter(**adapter_kwargs)

    # Setup chunking strategy
    if self.chunk_strategy == "semantic":
        chunker = SemanticSectionChunker(max_heading_level=self.max_heading_level)
    else:
        chunker = None  # Use default chunking

    pipeline = Pipeline(adapter=adapter, chunk_strategy=chunker)

    # Process each file
    for source in file_paths:
        source_path = Path(source) if isinstance(source, str) else source

        # Use a temp directory for LayoutIR output, cleaned up after processing
        tmp_dir = tempfile.mkdtemp()
        try:
            layoutir_doc = pipeline.process(
                input_path=source_path,
                output_dir=Path(tmp_dir),
            )
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        # Extract blocks/chunks from the IR
        if hasattr(layoutir_doc, "blocks"):
            blocks = layoutir_doc.blocks
        elif hasattr(layoutir_doc, "chunks"):
            blocks = layoutir_doc.chunks
        else:
            # Fallback: treat entire document as single block
            blocks = [{"text": str(layoutir_doc), "type": "document"}]

        # Convert each block to a LlamaIndex Document
        for idx, block in enumerate(blocks):
            # Extract text content from layoutir.schema.Block objects
            if isinstance(block, dict):
                text = block.get("text", block.get("content", ""))
                block_type = str(block.get("type", "unknown"))
                block_id = block.get("id", f"{source_path.stem}_block_{idx}")
                page_number = block.get("page", block.get("page_number", 0))
            elif hasattr(block, "content"):
                text = block.content or ""
                block_type = (
                    str(block.type.value)
                    if hasattr(block.type, "value")
                    else str(block.type)
                )
                block_id = getattr(
                    block, "block_id", f"{source_path.stem}_block_{idx}"
                )
                page_number = getattr(block, "page_number", 0)
            else:
                text = str(block)
                block_type = "block"
                block_id = f"{source_path.stem}_block_{idx}"
                page_number = 0

            # Create metadata
            metadata = extra_info.copy() if extra_info else {}
            metadata.update(
                {
                    "file_path": str(source_path),
                    "file_name": source_path.name,
                    "block_type": block_type,
                    "block_index": idx,
                    "page_number": page_number,
                    "source": "layoutir",
                }
            )

            # Create and yield Document
            doc = Document(
                doc_id=block_id,
                text=text,
                metadata=metadata,
            )

            yield doc

```
 |  
| --- | --- |  
options: members: - LayoutIRReader
