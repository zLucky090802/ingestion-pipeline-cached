# Firestore
##  FirestoreIndexStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/firestore/#llama_index.storage.index_store.firestore.FirestoreIndexStore "Permanent link")
Bases: `KVIndexStore`
Firestore Index store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `firestore_kvstore`  |   |  Firestore key-value store  |  _required_  |  
|  `namespace`  |  namespace for the index store  |  `None`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-firestore/llama_index/storage/index_store/firestore/base.py`  
| 
```
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
```
 | 
```
classFirestoreIndexStore(KVIndexStore):
"""
    Firestore Index store.

    Args:
        firestore_kvstore (FirestoreKVStore): Firestore key-value store
        namespace (str): namespace for the index store

    """

    def__init__(
        self,
        firestore_kvstore: FirestoreKVStore,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> None:
"""Init a FirestoreIndexStore."""
        super().__init__(
            firestore_kvstore, namespace=namespace, collection_suffix=collection_suffix
        )

    @classmethod
    deffrom_database(
        cls,
        project: str,
        database: str,
        namespace: Optional[str] = None,
        collection_suffix: Optional[str] = None,
    ) -> "FirestoreIndexStore":
"""
        Load a FirestoreIndexStore from a Firestore database.

        Args:
            project (str): The project which the client acts on behalf of.
            database (str): The database name that the client targets.
            namespace (str): namespace for the docstore.
            collection_suffix (str): suffix for the collection name

        """
        firestore_kvstore = FirestoreKVStore(project=project, database=database)
        return cls(firestore_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
###  from_database `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/index_store/firestore/#llama_index.storage.index_store.firestore.FirestoreIndexStore.from_database "Permanent link")

```
from_database(
    project: ,
    database: ,
    namespace: Optional[] = None,
    collection_suffix: Optional[] = None,
) -> 

```

Load a FirestoreIndexStore from a Firestore database.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `project`  |  The project which the client acts on behalf of.  |  _required_  |  
|  `database`  |  The database name that the client targets.  |  _required_  |  
|  `namespace`  |  namespace for the docstore.  |  `None`  |  
|  `collection_suffix`  |  suffix for the collection name  |  `None`  |  
Source code in `llama-index-integrations/storage/index_store/llama-index-storage-index-store-firestore/llama_index/storage/index_store/firestore/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_database(
    cls,
    project: str,
    database: str,
    namespace: Optional[str] = None,
    collection_suffix: Optional[str] = None,
) -> "FirestoreIndexStore":
"""
    Load a FirestoreIndexStore from a Firestore database.

    Args:
        project (str): The project which the client acts on behalf of.
        database (str): The database name that the client targets.
        namespace (str): namespace for the docstore.
        collection_suffix (str): suffix for the collection name

    """
    firestore_kvstore = FirestoreKVStore(project=project, database=database)
    return cls(firestore_kvstore, namespace, collection_suffix)

```
 |  
| --- | --- |  
options: members: - FirestoreIndexStore
