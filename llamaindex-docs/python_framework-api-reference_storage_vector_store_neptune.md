# Neptune
##  NeptuneAnalyticsVectorStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/neptune/#llama_index.vector_stores.neptune.NeptuneAnalyticsVectorStore "Permanent link")
Bases: 
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-neptune/llama_index/vector_stores/neptune/base.py`  
| 
```
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
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
```
 | 
```
classNeptuneAnalyticsVectorStore(BasePydanticVectorStore):
    stores_text: bool = True
    flat_metadata: bool = True

    node_label: str
    graph_identifier: str
    embedding_dimension: int
    text_node_property: str
    hybrid_search: bool
    retrieval_query: Optional[str]

    _client: Any = PrivateAttr()

    def__init__(
        self,
        graph_identifier: str,
        embedding_dimension: int,
        client: Any = None,
        credentials_profile_name: Optional[str] = None,
        region_name: Optional[str] = None,
        hybrid_search: bool = False,
        node_label: str = "Chunk",
        text_node_property: str = "text",
        retrieval_query: str = None,
        **kwargs: Any,
    ) -> None:
"""Create a new Neptune Analytics graph wrapper instance."""
        super().__init__(
            graph_identifier=graph_identifier,
            embedding_dimension=embedding_dimension,
            node_label=node_label,
            text_node_property=text_node_property,
            hybrid_search=hybrid_search,
            retrieval_query=retrieval_query,
        )

        try:
            if client is not None:
                self._client = client
            else:
                importboto3

                if credentials_profile_name is not None:
                    session = boto3.Session(profile_name=credentials_profile_name)
                else:
                    # use default credentials
                    session = boto3.Session()

                if region_name:
                    self._client = session.client(
                        "neptune-graph", region_name=region_name
                    )
                else:
                    self._client = session.client("neptune-graph")

        except ImportError:
            raise ModuleNotFoundError(
                "Could not import boto3 python package. "
                "Please install it with `pip install boto3`."
            )
        except Exception as e:
            if type(e).__name__ == "UnknownServiceError":
                raise ModuleNotFoundError(
                    "NeptuneGraph requires a boto3 version 1.34.40 or greater."
                    "Please install it with `pip install -U boto3`."
                ) frome
            else:
                raise ValueError(
                    "Could not load credentials to authenticate with AWS client. "
                    "Please check that credentials in the specified "
                    "profile name are valid."
                ) frome

        # Verify that the analytics graph has a vector search index and that the dimensions match
        self._verify_vectorIndex()

    def_verify_vectorIndex(self) -> None:
"""
        Check if the connected Neptune Analytics graph has VSS enabled and that the dimensions are the same.
        """
        resp = self._client.get_graph(graphIdentifier=self.graph_identifier)

        if "vectorSearchConfiguration" in resp:
            if (
                not resp["vectorSearchConfiguration"]["dimension"]
                == self.embedding_dimension
            ):
                raise ValueError(
                    f"Vector search index dimension for Neptune Analytics graph does not match the provided value."
                )
        else:
            raise ValueError(
                f"Vector search index does not exist for the Neptune Analytics graph."
            )

    @classmethod
    defclass_name(cls) -> str:
        return "NeptuneAnalyticsVectorStore"

    @property
    defclient(self) -> Any:
        return self._client

    defdatabase_query(
        self, query: str, params: Optional[dict] = None
    ) -> List[Dict[str, Any]]:
"""
        This method sends a query to the Neptune Analytics graph
        and returns the results as a list of dictionaries.

        Args:
            query (str): The openCypher query to execute.
            params (dict, optional): Dictionary of query parameters. Defaults to {}.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing the query results.

        """
        try:
            logger.debug(f"query() query: {query} parameters: {json.dumps(params)}")
            resp = self._client.execute_query(
                graphIdentifier=self.graph_identifier,
                queryString=query,
                parameters=params,
                language="OPEN_CYPHER",
            )
            return json.loads(resp["payload"].read().decode("UTF-8"))["results"]
        except Exception as e:
            raise NeptuneVectorQueryException(
                {
                    "message": "An error occurred while executing the query.",
                    "details": str(e),
                }
            )

    defadd(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        ids = [r.node_id for r in nodes]

        for r in nodes:
            import_query = (
                f"MERGE (c:`{self.node_label}` {{`~id`: $id}}) "
                "SET c += $data "
                "WITH c "
                f"CALL neptune.algo.vectors.upsert(c, {r.embedding}) "
                "YIELD node "
                "RETURN id(node) as id"
            )
            resp = self.database_query(
                import_query,
                params=self.__clean_params(r),
            )
        print("Nodes added")
        return ids

    def_get_search_index_query(self, hybrid: bool, k: int = 10) -> str:
        if not hybrid:
            return (
                "WITH $embedding as emb "
                "CALL neptune.algo.vectors.topKByEmbedding(emb, {topK: "
                + str(k)
                + "}) YIELD embedding, node, score "
            )
        else:
            raise NotImplementedError

    defquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        default_retrieval = (
            f"RETURN node.`{self.text_node_property}` AS text, score, "
            "id(node) AS id, "
            f"node AS metadata"
        )

        retrieval_query = self.retrieval_query or default_retrieval
        read_query = (
            self._get_search_index_query(self.hybrid_search, query.similarity_top_k)
            + retrieval_query
        )

        parameters = {
            "embedding": query.query_embedding,
        }

        results = self.database_query(read_query, params=parameters)

        nodes = []
        similarities = []
        ids = []
        for record in results:
            node = metadata_dict_to_node(record["metadata"]["~properties"])
            node.set_content(str(record["text"]))
            nodes.append(node)
            similarities.append(record["score"])
            ids.append(record["id"])

        return VectorStoreQueryResult(nodes=nodes, similarities=similarities, ids=ids)

    defdelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        self.database_query(
            f"MATCH (n:`{self.node_label}`) WHERE n.ref_doc_id = $id DETACH DELETE n",
            params={"id": ref_doc_id},
        )

    def__clean_params(self, record: BaseNode) -> List[Dict[str, Any]]:
"""Convert BaseNode object to a dictionary to be imported into Neo4j."""
        text = record.get_content(metadata_mode=MetadataMode.NONE)
        id = record.node_id
        metadata = node_to_metadata_dict(record, remove_text=True, flat_metadata=False)
        # Remove redundant metadata information
        for k in ["document_id", "doc_id"]:
            del metadata[k]
        return {"id": id, "data": {self.text_node_property: text, "id": id, **metadata}}

```
 |  
| --- | --- |  
###  database_query [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/neptune/#llama_index.vector_stores.neptune.NeptuneAnalyticsVectorStore.database_query "Permanent link")

```
database_query(
    query: , params: Optional[] = None
) -> [[, ]]

```

This method sends a query to the Neptune Analytics graph and returns the results as a list of dictionaries.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The openCypher query to execute.  |  _required_  |  
|  `params`  |  `dict`  |  Dictionary of query parameters. Defaults to {}.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[Dict[str, Any]]`  |  List[Dict[str, Any]]: List of dictionaries containing the query results.  |  
Source code in `llama-index-integrations/vector_stores/llama-index-vector-stores-neptune/llama_index/vector_stores/neptune/base.py`  
| 
```
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
defdatabase_query(
    self, query: str, params: Optional[dict] = None
) -> List[Dict[str, Any]]:
"""
    This method sends a query to the Neptune Analytics graph
    and returns the results as a list of dictionaries.

    Args:
        query (str): The openCypher query to execute.
        params (dict, optional): Dictionary of query parameters. Defaults to {}.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing the query results.

    """
    try:
        logger.debug(f"query() query: {query} parameters: {json.dumps(params)}")
        resp = self._client.execute_query(
            graphIdentifier=self.graph_identifier,
            queryString=query,
            parameters=params,
            language="OPEN_CYPHER",
        )
        return json.loads(resp["payload"].read().decode("UTF-8"))["results"]
    except Exception as e:
        raise NeptuneVectorQueryException(
            {
                "message": "An error occurred while executing the query.",
                "details": str(e),
            }
        )

```
 |  
| --- | --- |  
options: members: - NeptuneAnalyticsVectorStore
