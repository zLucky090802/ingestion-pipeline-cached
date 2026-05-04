# Firestore
##  FirestoreDocumentStore [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/firestore/#llama_index.storage.docstore.firestore.FirestoreDocumentStore "Permanent link")
Bases: `KVDocumentStore`
Firestore Document (Node) store.
A Firestore store for Document and Node objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `firestore_kvstore`  |   |  Firestore key-value store  |  _required_  |  
|  `namespace`  |  namespace for the docstore  |  `None`  |  
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-firestore/llama_index/storage/docstore/firestore/base.py`  
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
```
 | 
```
classFirestoreDocumentStore(KVDocumentStore):
"""
    Firestore Document (Node) store.

    A Firestore store for Document and Node objects.

    Args:
        firestore_kvstore (FirestoreKVStore): Firestore key-value store
        namespace (str): namespace for the docstore

    """

    def__init__(
        self,
        firestore_kvstore: FirestoreKVStore,
        namespace: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
"""Init a FirestoreDocumentStore."""
        super().__init__(firestore_kvstore, namespace=namespace, batch_size=batch_size)

    @classmethod
    deffrom_database(
        cls,
        project: str,
        database: str,
        namespace: Optional[str] = None,
    ) -> "FirestoreDocumentStore":
"""
        Args:
            project (str): The project which the client acts on behalf of.
            database (str): The database name that the client targets.
            namespace (str): namespace for the docstore.

        """
        firestore_kvstore = FirestoreKVStore(project=project, database=database)
        return cls(firestore_kvstore, namespace)

```
 |  
| --- | --- |  
###  from_database `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/storage/docstore/firestore/#llama_index.storage.docstore.firestore.FirestoreDocumentStore.from_database "Permanent link")

```
from_database(
    project: ,
    database: ,
    namespace: Optional[] = None,
) -> 

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `project`  |  The project which the client acts on behalf of.  |  _required_  |  
|  `database`  |  The database name that the client targets.  |  _required_  |  
|  `namespace`  |  namespace for the docstore.  |  `None`  |  
Source code in `llama-index-integrations/storage/docstore/llama-index-storage-docstore-firestore/llama_index/storage/docstore/firestore/base.py`  
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
```
 | 
```
@classmethod
deffrom_database(
    cls,
    project: str,
    database: str,
    namespace: Optional[str] = None,
) -> "FirestoreDocumentStore":
"""
    Args:
        project (str): The project which the client acts on behalf of.
        database (str): The database name that the client targets.
        namespace (str): namespace for the docstore.

    """
    firestore_kvstore = FirestoreKVStore(project=project, database=database)
    return cls(firestore_kvstore, namespace)

```
 |  
| --- | --- |  
options: members: - FirestoreDocumentStore
