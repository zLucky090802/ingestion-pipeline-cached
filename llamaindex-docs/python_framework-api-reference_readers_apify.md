# Apify
##  ApifyActor [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/apify/#llama_index.readers.apify.ApifyActor "Permanent link")
Bases: 
Apify Actor reader. Calls an Actor on the Apify platform and reads its resulting dataset when it finishes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `apify_api_token`  |  Apify API token.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-apify/llama_index/readers/apify/actor/base.py`  
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
```
 | 
```
classApifyActor(BaseReader):
"""
    Apify Actor reader.
    Calls an Actor on the Apify platform and reads its resulting dataset when it finishes.

    Args:
        apify_api_token (str): Apify API token.

    """

    def__init__(self, apify_api_token: str) -> None:
"""Initialize the Apify Actor reader."""
        fromapify_clientimport ApifyClient

        self.apify_api_token = apify_api_token

        client = ApifyClient(apify_api_token)
        if hasattr(client.http_client, "httpx_client"):
            client.http_client.httpx_client.headers["user-agent"] += (
                "; Origin/llama_index"
            )
        self.apify_client = client

    defload_data(
        self,
        actor_id: str,
        run_input: Dict,
        dataset_mapping_function: Callable[[Dict], Document],
        *,
        build: Optional[str] = None,
        memory_mbytes: Optional[int] = None,
        timeout_secs: Optional[int] = None,
    ) -> List[Document]:
"""
        Call an Actor on the Apify platform, wait for it to finish, and return its resulting dataset.

        Args:
            actor_id (str): The ID or name of the Actor.
            run_input (Dict): The input object of the Actor that you're trying to run.
            dataset_mapping_function (Callable): A function that takes a single dictionary (an Apify dataset item) and converts it to an instance of the Document class.
            build (str, optional): Optionally specifies the Actor build to run. It can be either a build tag or build number.
            memory_mbytes (int, optional): Optional memory limit for the run, in megabytes.
            timeout_secs (int, optional): Optional timeout for the run, in seconds.


        Returns:
            List[Document]: List of documents.

        """
        actor_call = self.apify_client.actor(actor_id).call(
            run_input=run_input,
            build=build,
            memory_mbytes=memory_mbytes,
            timeout_secs=timeout_secs,
        )

        reader = ApifyDataset(self.apify_api_token)
        return reader.load_data(
            dataset_id=actor_call.get("defaultDatasetId"),
            dataset_mapping_function=dataset_mapping_function,
        )

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/apify/#llama_index.readers.apify.ApifyActor.load_data "Permanent link")

```
load_data(
    actor_id: ,
    run_input: ,
    dataset_mapping_function: Callable[[], ],
    *,
    build: Optional[] = None,
    memory_mbytes: Optional[] = None,
    timeout_secs: Optional[] = None
) -> []

```

Call an Actor on the Apify platform, wait for it to finish, and return its resulting dataset.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `actor_id`  |  The ID or name of the Actor.  |  _required_  |  
|  `run_input`  |  `Dict`  |  The input object of the Actor that you're trying to run.  |  _required_  |  
|  `dataset_mapping_function`  |  `Callable`  |  A function that takes a single dictionary (an Apify dataset item) and converts it to an instance of the Document class.  |  _required_  |  
|  `build`  |  Optionally specifies the Actor build to run. It can be either a build tag or build number.  |  `None`  |  
|  `memory_mbytes`  |  Optional memory limit for the run, in megabytes.  |  `None`  |  
|  `timeout_secs`  |  Optional timeout for the run, in seconds.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-apify/llama_index/readers/apify/actor/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    actor_id: str,
    run_input: Dict,
    dataset_mapping_function: Callable[[Dict], Document],
    *,
    build: Optional[str] = None,
    memory_mbytes: Optional[int] = None,
    timeout_secs: Optional[int] = None,
) -> List[Document]:
"""
    Call an Actor on the Apify platform, wait for it to finish, and return its resulting dataset.

    Args:
        actor_id (str): The ID or name of the Actor.
        run_input (Dict): The input object of the Actor that you're trying to run.
        dataset_mapping_function (Callable): A function that takes a single dictionary (an Apify dataset item) and converts it to an instance of the Document class.
        build (str, optional): Optionally specifies the Actor build to run. It can be either a build tag or build number.
        memory_mbytes (int, optional): Optional memory limit for the run, in megabytes.
        timeout_secs (int, optional): Optional timeout for the run, in seconds.


    Returns:
        List[Document]: List of documents.

    """
    actor_call = self.apify_client.actor(actor_id).call(
        run_input=run_input,
        build=build,
        memory_mbytes=memory_mbytes,
        timeout_secs=timeout_secs,
    )

    reader = ApifyDataset(self.apify_api_token)
    return reader.load_data(
        dataset_id=actor_call.get("defaultDatasetId"),
        dataset_mapping_function=dataset_mapping_function,
    )

```
 |  
| --- | --- |  
##  ApifyDataset [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/apify/#llama_index.readers.apify.ApifyDataset "Permanent link")
Bases: 
Apify Dataset reader. Reads a dataset on the Apify platform.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `apify_api_token`  |  Apify API token.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-apify/llama_index/readers/apify/dataset/base.py`  
| 
```
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
classApifyDataset(BaseReader):
"""
    Apify Dataset reader.
    Reads a dataset on the Apify platform.

    Args:
        apify_api_token (str): Apify API token.

    """

    def__init__(self, apify_api_token: str) -> None:
"""Initialize Apify dataset reader."""
        fromapify_clientimport ApifyClient

        client = ApifyClient(apify_api_token)
        if hasattr(client.http_client, "httpx_client"):
            client.http_client.httpx_client.headers["user-agent"] += (
                "; Origin/llama_index"
            )

        self.apify_client = client

    defload_data(
        self, dataset_id: str, dataset_mapping_function: Callable[[Dict], Document]
    ) -> List[Document]:
"""
        Load data from the Apify dataset.

        Args:
            dataset_id (str): Dataset ID.
            dataset_mapping_function (Callable[[Dict], Document]): Function to map dataset items to Document.


        Returns:
            List[Document]: List of documents.

        """
        items_list = self.apify_client.dataset(dataset_id).list_items(clean=True)

        document_list = []
        for item in items_list.items:
            document = dataset_mapping_function(item)
            if not isinstance(document, Document):
                raise ValueError("Dataset_mapping_function must return a Document")
            document_list.append(document)

        return document_list

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/apify/#llama_index.readers.apify.ApifyDataset.load_data "Permanent link")

```
load_data(
    dataset_id: ,
    dataset_mapping_function: Callable[[], ],
) -> []

```

Load data from the Apify dataset.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `dataset_id`  |  Dataset ID.  |  _required_  |  
|  `dataset_mapping_function`  |  `Callable[[Dict], Document[](https://developers.llamaindex.ai/python/framework-api-reference/schema/#llama_index.core.schema.Document "Document \(llama_index.core.schema.Document\)")]`  |  Function to map dataset items to Document.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-apify/llama_index/readers/apify/dataset/base.py`  
| 
```
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
defload_data(
    self, dataset_id: str, dataset_mapping_function: Callable[[Dict], Document]
) -> List[Document]:
"""
    Load data from the Apify dataset.

    Args:
        dataset_id (str): Dataset ID.
        dataset_mapping_function (Callable[[Dict], Document]): Function to map dataset items to Document.


    Returns:
        List[Document]: List of documents.

    """
    items_list = self.apify_client.dataset(dataset_id).list_items(clean=True)

    document_list = []
    for item in items_list.items:
        document = dataset_mapping_function(item)
        if not isinstance(document, Document):
            raise ValueError("Dataset_mapping_function must return a Document")
        document_list.append(document)

    return document_list

```
 |  
| --- | --- |  
options: members: - ApifyActor - ApifyDataset
