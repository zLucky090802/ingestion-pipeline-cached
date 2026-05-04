# Vertexai
##  VertexAIIndex [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vertexai/#llama_index.indices.managed.vertexai.VertexAIIndex "Permanent link")
Bases: `BaseManagedIndex`
Vertex AI Index.
The Vertex AI RAG index implements a managed index that uses Vertex AI as the backend. Vertex AI performs a lot of the functions in traditional indexes in the backend: - breaks down a document into chunks (nodes) - Creates the embedding for each chunk (node) - Performs the search for the top k most similar nodes to a query - Optionally can perform summarization of the top k nodes
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vertexai/llama_index/indices/managed/vertexai/base.py`  
| 
```
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
```
 | 
```
classVertexAIIndex(BaseManagedIndex):
"""
    Vertex AI Index.

    The Vertex AI RAG index implements a managed index that uses Vertex AI as the backend.
    Vertex AI performs a lot of the functions in traditional indexes in the backend:
    - breaks down a document into chunks (nodes)
    - Creates the embedding for each chunk (node)
    - Performs the search for the top k most similar nodes to a query
    - Optionally can perform summarization of the top k nodes

    Args:
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.

    """

    def__init__(
        self,
        project_id: str,
        location: Optional[str] = None,
        corpus_id: Optional[str] = None,
        corpus_display_name: Optional[str] = None,
        corpus_description: Optional[str] = None,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> None:
"""Initialize the Vertex AI API."""
        if corpus_id and (corpus_display_name or corpus_description):
            raise ValueError(
                "Cannot specify both corpus_id and corpus_display_name or corpus_description"
            )

        self.project_id = project_id
        self.location = location
        self.show_progress = show_progress
        self._user_agent = get_user_agent("vertexai-rag")

        vertexai.init(project=self.project_id, location=self.location)

        with telemetry.tool_context_manager(self._user_agent):
            # If a corpus is not specified, create a new one.
            if corpus_id:
                # Make sure corpus exists
                self.corpus_name = rag.get_corpus(name=corpus_id).name
            else:
                self.corpus_name = rag.create_corpus(
                    display_name=corpus_display_name, description=corpus_description
                ).name

    defimport_files(
        self,
        uris: Sequence[str],
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        timeout: Optional[int] = None,
        **kwargs: Any,
    ) -> ImportRagFilesResponse:
"""Import Google Cloud Storage or Google Drive files into the index."""
        # Convert https://storage.googleapis.com URLs to gs:// format
        uris = [
            re.sub(r"^https://storage\.googleapis\.com/", "gs://", uri) for uri in uris
        ]

        with telemetry.tool_context_manager(self._user_agent):
            return rag.import_files(
                self.corpus_name,
                paths=uris,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                timeout=timeout,
                **kwargs,
            )

    definsert_file(
        self,
        file_path: str,
        metadata: Optional[dict] = None,
        **insert_kwargs: Any,
    ) -> Optional[str]:
"""Insert a local file into the index."""
        if metadata:
            display_name = metadata.get("display_name")
            description = metadata.get("description")

        with telemetry.tool_context_manager(self._user_agent):
            rag_file = rag.upload_file(
                corpus_name=self.corpus_name,
                path=file_path,
                display_name=display_name,
                description=description,
                **insert_kwargs,
            )

        return rag_file.name if rag_file else None

    deflist_files(self) -> Sequence[str]:
"""List all files in the index."""
        files = []
        with telemetry.tool_context_manager(self._user_agent):
            for file in rag.list_files(corpus_name=self.corpus_name):
                files.append(file.name)
        return files

    defdelete_file(self, file_name: str) -> None:
"""Delete file from the index."""
        with telemetry.tool_context_manager(self._user_agent):
            rag.delete_file(name=file_name, corpus_name=self.corpus_name)

    defas_query_engine(self, **kwargs: Any) -> BaseQueryEngine:
        fromllama_index.core.query_engine.retriever_query_engineimport (
            RetrieverQueryEngine,
        )

        kwargs["retriever"] = self.as_retriever(**kwargs)
        return RetrieverQueryEngine.from_args(**kwargs)

    defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Return a Retriever for this managed index."""
        fromllama_index.indices.managed.vertexai.retrieverimport (
            VertexAIRetriever,
        )

        similarity_top_k = kwargs.pop("similarity_top_k", None)
        vector_distance_threshold = kwargs.pop("vector_distance_threshold", None)

        return VertexAIRetriever(
            self.corpus_name,
            similarity_top_k,
            vector_distance_threshold,
            self._user_agent,
            **kwargs,
        )

    def_insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
"""Insert a set of documents (each a node)."""
        raise NotImplementedError("Node insertion is not supported.")

    defdelete_ref_doc(
        self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
    ) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
        if delete_from_docstore:
            with telemetry.tool_context_manager(self._user_agent):
                rag.delete_file(
                    name=ref_doc_id,
                    corpus_name=self.corpus_name,
                )

    defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""Update a document and it's corresponding nodes."""
        raise NotImplementedError("Document update is not supported.")

```
 |  
| --- | --- |  
###  import_files [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vertexai/#llama_index.indices.managed.vertexai.VertexAIIndex.import_files "Permanent link")

```
import_files(
    uris: Sequence[],
    chunk_size: Optional[] = None,
    chunk_overlap: Optional[] = None,
    timeout: Optional[] = None,
    **kwargs: 
) -> ImportRagFilesResponse

```

Import Google Cloud Storage or Google Drive files into the index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vertexai/llama_index/indices/managed/vertexai/base.py`  
| 
```
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
```
 | 
```
defimport_files(
    self,
    uris: Sequence[str],
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
    timeout: Optional[int] = None,
    **kwargs: Any,
) -> ImportRagFilesResponse:
"""Import Google Cloud Storage or Google Drive files into the index."""
    # Convert https://storage.googleapis.com URLs to gs:// format
    uris = [
        re.sub(r"^https://storage\.googleapis\.com/", "gs://", uri) for uri in uris
    ]

    with telemetry.tool_context_manager(self._user_agent):
        return rag.import_files(
            self.corpus_name,
            paths=uris,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            timeout=timeout,
            **kwargs,
        )

```
 |  
| --- | --- |  
###  insert_file [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vertexai/#llama_index.indices.managed.vertexai.VertexAIIndex.insert_file "Permanent link")

```
insert_file(
    file_path: ,
    metadata: Optional[] = None,
    **insert_kwargs: 
) -> Optional[]

```

Insert a local file into the index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vertexai/llama_index/indices/managed/vertexai/base.py`  
| 
```
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
```
 | 
```
definsert_file(
    self,
    file_path: str,
    metadata: Optional[dict] = None,
    **insert_kwargs: Any,
) -> Optional[str]:
"""Insert a local file into the index."""
    if metadata:
        display_name = metadata.get("display_name")
        description = metadata.get("description")

    with telemetry.tool_context_manager(self._user_agent):
        rag_file = rag.upload_file(
            corpus_name=self.corpus_name,
            path=file_path,
            display_name=display_name,
            description=description,
            **insert_kwargs,
        )

    return rag_file.name if rag_file else None

```
 |  
| --- | --- |  
###  list_files [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vertexai/#llama_index.indices.managed.vertexai.VertexAIIndex.list_files "Permanent link")

```
list_files() -> Sequence[]

```

List all files in the index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vertexai/llama_index/indices/managed/vertexai/base.py`  
| 
```
142
143
144
145
146
147
148
```
 | 
```
deflist_files(self) -> Sequence[str]:
"""List all files in the index."""
    files = []
    with telemetry.tool_context_manager(self._user_agent):
        for file in rag.list_files(corpus_name=self.corpus_name):
            files.append(file.name)
    return files

```
 |  
| --- | --- |  
###  delete_file [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vertexai/#llama_index.indices.managed.vertexai.VertexAIIndex.delete_file "Permanent link")

```
delete_file(file_name: ) -> None

```

Delete file from the index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vertexai/llama_index/indices/managed/vertexai/base.py`  
| 
```
150
151
152
153
```
 | 
```
defdelete_file(self, file_name: str) -> None:
"""Delete file from the index."""
    with telemetry.tool_context_manager(self._user_agent):
        rag.delete_file(name=file_name, corpus_name=self.corpus_name)

```
 |  
| --- | --- |  
###  as_retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vertexai/#llama_index.indices.managed.vertexai.VertexAIIndex.as_retriever "Permanent link")

```
as_retriever(**kwargs: ) -> 

```

Return a Retriever for this managed index.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vertexai/llama_index/indices/managed/vertexai/base.py`  
| 
```
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
```
 | 
```
defas_retriever(self, **kwargs: Any) -> BaseRetriever:
"""Return a Retriever for this managed index."""
    fromllama_index.indices.managed.vertexai.retrieverimport (
        VertexAIRetriever,
    )

    similarity_top_k = kwargs.pop("similarity_top_k", None)
    vector_distance_threshold = kwargs.pop("vector_distance_threshold", None)

    return VertexAIRetriever(
        self.corpus_name,
        similarity_top_k,
        vector_distance_threshold,
        self._user_agent,
        **kwargs,
    )

```
 |  
| --- | --- |  
###  delete_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vertexai/#llama_index.indices.managed.vertexai.VertexAIIndex.delete_ref_doc "Permanent link")

```
delete_ref_doc(
    ref_doc_id: ,
    delete_from_docstore:  = False,
    **delete_kwargs: 
) -> None

```

Delete a document and it's nodes by using ref_doc_id.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vertexai/llama_index/indices/managed/vertexai/base.py`  
| 
```
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
```
 | 
```
defdelete_ref_doc(
    self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
) -> None:
"""Delete a document and it's nodes by using ref_doc_id."""
    if delete_from_docstore:
        with telemetry.tool_context_manager(self._user_agent):
            rag.delete_file(
                name=ref_doc_id,
                corpus_name=self.corpus_name,
            )

```
 |  
| --- | --- |  
###  update_ref_doc [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vertexai/#llama_index.indices.managed.vertexai.VertexAIIndex.update_ref_doc "Permanent link")

```
update_ref_doc(
    document: , **update_kwargs: 
) -> None

```

Update a document and it's corresponding nodes.
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vertexai/llama_index/indices/managed/vertexai/base.py`  
| 
```
195
196
197
```
 | 
```
defupdate_ref_doc(self, document: Document, **update_kwargs: Any) -> None:
"""Update a document and it's corresponding nodes."""
    raise NotImplementedError("Document update is not supported.")

```
 |  
| --- | --- |  
##  VertexAIRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/indices/vertexai/#llama_index.indices.managed.vertexai.VertexAIRetriever "Permanent link")
Bases: 
Source code in `llama-index-integrations/indices/llama-index-indices-managed-vertexai/llama_index/indices/managed/vertexai/retriever.py`  
| 
```
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
```
 | 
```
classVertexAIRetriever(BaseRetriever):
    def__init__(
        self,
        corpus_name: str,
        similarity_top_k: Optional[int] = None,
        vector_distance_threshold: Optional[float] = 0.3,
        user_agent: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
"""Initialize the Vertex AI Retriever."""
        self.rag_resources = [rag.RagResource(rag_corpus=corpus_name)]
        self._similarity_top_k = similarity_top_k
        self._vector_distance_threshold = vector_distance_threshold
        self._user_agent = user_agent or "llama-index/0.0.0"

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve from the platform."""
        with telemetry.tool_context_manager(self._user_agent):
            response = rag.retrieval_query(
                text=query_bundle.query_str,
                rag_resources=self.rag_resources,
                similarity_top_k=self._similarity_top_k,
                vector_distance_threshold=self._vector_distance_threshold,
            )

        if response.contexts:
            return [
                NodeWithScore(
                    node=TextNode(
                        text=context.text,
                        metadata={
                            "source_uri": context.source_uri,
                            "source_display_name": context.source_display_name,
                        },
                    ),
                    score=context.distance,
                )
                for context in response.contexts.contexts
            ]
        else:
            return []

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Asynchronously retrieve from the platform."""
        return self._retrieve(query_bundle=query_bundle)

```
 |  
| --- | --- |  
options: members: - VertexAIIndex
