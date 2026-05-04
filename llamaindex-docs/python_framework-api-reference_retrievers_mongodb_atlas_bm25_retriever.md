# Mongodb atlas bm25 retriever
##  MongoDBAtlasBM25Retriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/mongodb_atlas_bm25_retriever/#llama_index.retrievers.mongodb_atlas_bm25_retriever.MongoDBAtlasBM25Retriever "Permanent link")
Bases: 
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-mongodb-atlas-bm25-retriever/llama_index/retrievers/mongodb_atlas_bm25_retriever/base.py`  
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
```
 | 
```
classMongoDBAtlasBM25Retriever(BaseRetriever):
    def__init__(
        self,
        mongodb_client: Optional[Any] = None,
        db_name: str = "default_db",
        collection_name: str = "default_collection",
        index_name: str = "default",
        text_key: str = "text",
        metadata_key: str = "metadata",
        similarity_top_k: int = DEFAULT_SIMILARITY_TOP_K,
    ) -> None:
"""
        Initialize the vector store.

        Args:
            mongodb_client: A MongoDB client.
            db_name: A MongoDB database name.
            collection_name: A MongoDB collection name.
            index_name: A MongoDB Atlas Vector Search index name.
            text_key: A MongoDB field that will contain the text for each document.
            metadata_key: A MongoDB field that will contain

        """
        import_err_msg = "`pymongo` package not found, please run `pip install pymongo`"
        try:
            fromimportlib.metadataimport version
            frompymongoimport MongoClient
            frompymongo.driver_infoimport DriverInfo
        except ImportError:
            raise ImportError(import_err_msg)

        if mongodb_client is not None:
            self._mongodb_client = cast(MongoClient, mongodb_client)
        else:
            if "MONGO_URI" not in os.environ:
                raise ValueError(
                    "Must specify MONGO_URI via env variable "
                    "if not directly passing in client."
                )
            self._mongodb_client = MongoClient(
                os.environ["MONGO_URI"],
                driver=DriverInfo(name="llama-index", version=version("llama-index")),
            )
        self._db = self._mongodb_client[db_name]
        self._collection = self._db[collection_name]
        self._index_name = index_name
        self._text_key = text_key
        self._metadata_key = metadata_key
        self._similarity_top_k = similarity_top_k

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Retrieve nodes given query."""
        query = query_bundle.query_str

        pipeline = [
            {
                "$search": {
                    "index": self._index_name,
                    "text": {"query": query, "path": self._text_key},
                }
            },
            {"$addFields": {"score": {"$meta": "searchScore"}}},
            {"$sort": {"score": -1}},
            {"$limit": self._similarity_top_k},
        ]

        results = list(self._collection.aggregate(pipeline))

        retrieve_nodes = []
        for result in results[: self._similarity_top_k]:
            doc = self._collection.find_one({"_id": result["_id"]})
            node = doc[self._text_key]
            node_content = json.loads(
                doc.get("metadata", {}).get("_node_content", "{}")
            )
            metadata_dict = doc.pop(self._metadata_key)
            node = None

            try:
                node = metadata_dict_to_node(metadata_dict)
                node.set_content(doc["text"])
            except Exception:
                node = TextNode(
                    text=doc["text"],
                    id_=doc["id"],
                    metadata=doc.get("metadata", {}),
                    start_char_idx=node_content.get("start_char_idx", None),
                    end_char_idx=node_content.get("end_char_idx", None),
                    relationships=node_content.get("relationships", None),
                )

            node_with_score = NodeWithScore(node=node, score=result["score"])
            retrieve_nodes.append(node_with_score)
        return retrieve_nodes

```
 |  
| --- | --- |  
options: members: - MongoDBAtlasBM25Retriever
