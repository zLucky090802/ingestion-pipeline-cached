# Elasticsearch
##  ElasticsearchEmbedding [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/elasticsearch/#llama_index.embeddings.elasticsearch.ElasticsearchEmbedding "Permanent link")
Bases: 
Elasticsearch embedding models.
This class provides an interface to generate embeddings using a model deployed in an Elasticsearch cluster. It requires an Elasticsearch connection object and the model_id of the model deployed in the cluster.
In Elasticsearch you need to have an embedding model loaded and deployed. - https://www.elastic.co /guide/en/elasticsearch/reference/current/infer-trained-model.html - https://www.elastic.co /guide/en/machine-learning/current/ml-nlp-deploy-models.html
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-elasticsearch/llama_index/embeddings/elasticsearch/base.py`  
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
```
 | 
```
classElasticsearchEmbedding(BaseEmbedding):
"""
    Elasticsearch embedding models.

    This class provides an interface to generate embeddings using a model deployed
    in an Elasticsearch cluster. It requires an Elasticsearch connection object
    and the model_id of the model deployed in the cluster.

    In Elasticsearch you need to have an embedding model loaded and deployed.
    - https://www.elastic.co
        /guide/en/elasticsearch/reference/current/infer-trained-model.html
    - https://www.elastic.co
        /guide/en/machine-learning/current/ml-nlp-deploy-models.html
    """  #

    _client: Any = PrivateAttr()
    model_id: str
    input_field: str

    defclass_name(self) -> str:
        return "ElasticsearchEmbedding"

    def__init__(
        self,
        client: Any,
        model_id: str,
        input_field: str = "text_field",
        **kwargs: Any,
    ):
        super().__init__(model_id=model_id, input_field=input_field, **kwargs)
        self._client = client

    @classmethod
    deffrom_es_connection(
        cls,
        model_id: str,
        es_connection: Any,
        input_field: str = "text_field",
    ) -> BaseEmbedding:
"""
        Instantiate embeddings from an existing Elasticsearch connection.

        This method provides a way to create an instance of the ElasticsearchEmbedding
        class using an existing Elasticsearch connection. The connection object is used
        to create an MlClient, which is then used to initialize the
        ElasticsearchEmbedding instance.

        Args:
        model_id (str): The model_id of the model deployed in the Elasticsearch cluster.
        es_connection (elasticsearch.Elasticsearch): An existing Elasticsearch
            connection object.
        input_field (str, optional): The name of the key for the input text field
            in the document. Defaults to 'text_field'.

        Returns:
        ElasticsearchEmbedding: An instance of the ElasticsearchEmbedding class.

        Example:
            .. code-block:: python

                from elasticsearch import Elasticsearch

                from llama_index.embeddings.elasticsearch import ElasticsearchEmbedding

                # Define the model ID and input field name (if different from default)
                model_id = "your_model_id"
                # Optional, only if different from 'text_field'
                input_field = "your_input_field"

                # Create Elasticsearch connection
                es_connection = Elasticsearch(hosts=["localhost:9200"], basic_auth=("user", "password"))

                # Instantiate ElasticsearchEmbedding using the existing connection
                embeddings = ElasticsearchEmbedding.from_es_connection(
                    model_id,
                    es_connection,
                    input_field=input_field,


        """
        client = MlClient(es_connection)
        return cls(client, model_id, input_field=input_field)

    @classmethod
    deffrom_credentials(
        cls,
        model_id: str,
        es_url: str,
        es_username: str,
        es_password: str,
        input_field: str = "text_field",
    ) -> BaseEmbedding:
"""
        Instantiate embeddings from Elasticsearch credentials.

        Args:
            model_id (str): The model_id of the model deployed in the Elasticsearch
                cluster.
            input_field (str): The name of the key for the input text field in the
                document. Defaults to 'text_field'.
            es_url: (str): The Elasticsearch url to connect to.
            es_username: (str): Elasticsearch username.
            es_password: (str): Elasticsearch password.

        Example:
            .. code-block:: python

                from llama_index.embeddings.bedrock import ElasticsearchEmbedding

                # Define the model ID and input field name (if different from default)
                model_id = "your_model_id"
                # Optional, only if different from 'text_field'
                input_field = "your_input_field"

                embeddings = ElasticsearchEmbedding.from_credentials(
                    model_id,
                    input_field=input_field,
                    es_url="foo",
                    es_username="bar",
                    es_password="baz",


        """
        es_connection = Elasticsearch(
            hosts=[es_url],
            basic_auth=(es_username, es_password),
        )

        client = MlClient(es_connection)
        return cls(client, model_id, input_field=input_field)

    def_get_embedding(self, text: str) -> List[float]:
"""
        Generate an embedding for a single query text.

        Args:
            text (str): The query text to generate an embedding for.

        Returns:
            List[float]: The embedding for the input query text.

        """
        response = self._client.infer_trained_model(
            model_id=self.model_id,
            docs=[{self.input_field: text}],
        )

        return response["inference_results"][0]["predicted_value"]

    def_get_text_embedding(self, text: str) -> List[float]:
        return self._get_embedding(text)

    def_get_query_embedding(self, query: str) -> List[float]:
        return self._get_embedding(query)

    async def_aget_text_embedding(self, text: str) -> List[float]:
        return await asyncio.to_thread(self._get_text_embedding, text)

    async def_aget_query_embedding(self, query: str) -> List[float]:
        return await asyncio.to_thread(self._get_query_embedding, query)

```
 |  
| --- | --- |  
###  from_es_connection `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/elasticsearch/#llama_index.embeddings.elasticsearch.ElasticsearchEmbedding.from_es_connection "Permanent link")

```
from_es_connection(
    model_id: ,
    es_connection: ,
    input_field:  = "text_field",
) -> 

```

Instantiate embeddings from an existing Elasticsearch connection.
This method provides a way to create an instance of the ElasticsearchEmbedding class using an existing Elasticsearch connection. The connection object is used to create an MlClient, which is then used to initialize the ElasticsearchEmbedding instance.
Args: model_id (str): The model_id of the model deployed in the Elasticsearch cluster. es_connection (elasticsearch.Elasticsearch): An existing Elasticsearch connection object. input_field (str, optional): The name of the key for the input text field in the document. Defaults to 'text_field'.
Returns: ElasticsearchEmbedding: An instance of the ElasticsearchEmbedding class.
Example
.. code-block:: python

```
from elasticsearch import Elasticsearch

from llama_index.embeddings.elasticsearch import ElasticsearchEmbedding

# Define the model ID and input field name (if different from default)
model_id = "your_model_id"
# Optional, only if different from 'text_field'
input_field = "your_input_field"

# Create Elasticsearch connection
es_connection = Elasticsearch(hosts=["localhost:9200"], basic_auth=("user", "password"))

# Instantiate ElasticsearchEmbedding using the existing connection
embeddings = ElasticsearchEmbedding.from_es_connection(
    model_id,
    es_connection,
    input_field=input_field,
)

```
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-elasticsearch/llama_index/embeddings/elasticsearch/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_es_connection(
    cls,
    model_id: str,
    es_connection: Any,
    input_field: str = "text_field",
) -> BaseEmbedding:
"""
    Instantiate embeddings from an existing Elasticsearch connection.

    This method provides a way to create an instance of the ElasticsearchEmbedding
    class using an existing Elasticsearch connection. The connection object is used
    to create an MlClient, which is then used to initialize the
    ElasticsearchEmbedding instance.

    Args:
    model_id (str): The model_id of the model deployed in the Elasticsearch cluster.
    es_connection (elasticsearch.Elasticsearch): An existing Elasticsearch
        connection object.
    input_field (str, optional): The name of the key for the input text field
        in the document. Defaults to 'text_field'.

    Returns:
    ElasticsearchEmbedding: An instance of the ElasticsearchEmbedding class.

    Example:
        .. code-block:: python

            from elasticsearch import Elasticsearch

            from llama_index.embeddings.elasticsearch import ElasticsearchEmbedding

            # Define the model ID and input field name (if different from default)
            model_id = "your_model_id"
            # Optional, only if different from 'text_field'
            input_field = "your_input_field"

            # Create Elasticsearch connection
            es_connection = Elasticsearch(hosts=["localhost:9200"], basic_auth=("user", "password"))

            # Instantiate ElasticsearchEmbedding using the existing connection
            embeddings = ElasticsearchEmbedding.from_es_connection(
                model_id,
                es_connection,
                input_field=input_field,


    """
    client = MlClient(es_connection)
    return cls(client, model_id, input_field=input_field)

```
 |  
| --- | --- |  
###  from_credentials `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/elasticsearch/#llama_index.embeddings.elasticsearch.ElasticsearchEmbedding.from_credentials "Permanent link")

```
from_credentials(
    model_id: ,
    es_url: ,
    es_username: ,
    es_password: ,
    input_field:  = "text_field",
) -> 

```

Instantiate embeddings from Elasticsearch credentials.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `model_id`  |  The model_id of the model deployed in the Elasticsearch cluster.  |  _required_  |  
|  `input_field`  |  The name of the key for the input text field in the document. Defaults to 'text_field'.  |  `'text_field'`  |  
|  `es_url`  |  (str): The Elasticsearch url to connect to.  |  _required_  |  
|  `es_username`  |  (str): Elasticsearch username.  |  _required_  |  
|  `es_password`  |  (str): Elasticsearch password.  |  _required_  |  
Example
.. code-block:: python

```
from llama_index.embeddings.bedrock import ElasticsearchEmbedding

# Define the model ID and input field name (if different from default)
model_id = "your_model_id"
# Optional, only if different from 'text_field'
input_field = "your_input_field"

embeddings = ElasticsearchEmbedding.from_credentials(
    model_id,
    input_field=input_field,
    es_url="foo",
    es_username="bar",
    es_password="baz",
)

```
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-elasticsearch/llama_index/embeddings/elasticsearch/base.py`  
| 
```
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
```
 | 
```
@classmethod
deffrom_credentials(
    cls,
    model_id: str,
    es_url: str,
    es_username: str,
    es_password: str,
    input_field: str = "text_field",
) -> BaseEmbedding:
"""
    Instantiate embeddings from Elasticsearch credentials.

    Args:
        model_id (str): The model_id of the model deployed in the Elasticsearch
            cluster.
        input_field (str): The name of the key for the input text field in the
            document. Defaults to 'text_field'.
        es_url: (str): The Elasticsearch url to connect to.
        es_username: (str): Elasticsearch username.
        es_password: (str): Elasticsearch password.

    Example:
        .. code-block:: python

            from llama_index.embeddings.bedrock import ElasticsearchEmbedding

            # Define the model ID and input field name (if different from default)
            model_id = "your_model_id"
            # Optional, only if different from 'text_field'
            input_field = "your_input_field"

            embeddings = ElasticsearchEmbedding.from_credentials(
                model_id,
                input_field=input_field,
                es_url="foo",
                es_username="bar",
                es_password="baz",


    """
    es_connection = Elasticsearch(
        hosts=[es_url],
        basic_auth=(es_username, es_password),
    )

    client = MlClient(es_connection)
    return cls(client, model_id, input_field=input_field)

```
 |  
| --- | --- |  
options: members: - ElasticsearchEmbedding
