# Bedrock
##  AmazonKnowledgeBasesRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/bedrock/#llama_index.retrievers.bedrock.AmazonKnowledgeBasesRetriever "Permanent link")
Bases: 
`Amazon Bedrock Knowledge Bases` retrieval.
See https://aws.amazon.com/bedrock/knowledge-bases for more info.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `knowledge_base_id`  |  Knowledge Base ID.  |  _required_  |  
|  `retrieval_config`  |  `Optional[Dict[str, Any]]`  |  Configuration for retrieval.  |  `None`  |  
|  `profile_name`  |  `Optional[str]`  |  The name of the profile in the ~/.aws/credentials or ~/.aws/config files, which has either access keys or role information specified. If not specified, the default credential profile or, if on an EC2 instance, credentials from IMDS will be used.  |  `None`  |  
|  `region_name`  |  `Optional[str]`  |  The aws region e.g., `us-west-2`. Fallback to AWS_DEFAULT_REGION env variable or region specified in ~/.aws/config.  |  `None`  |  
|  `aws_access_key_id`  |  `Optional[str]`  |  The aws access key id.  |  `None`  |  
|  `aws_secret_access_key`  |  `Optional[str]`  |  The aws secret access key.  |  `None`  |  
|  `aws_session_token`  |  `Optional[str]`  |  AWS temporary session token.  |  `None`  |  
Example
.. code-block:: python

```
from llama_index.retrievers.bedrock import AmazonKnowledgeBasesRetriever

retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="<knowledge-base-id>",
    retrieval_config={
        "vectorSearchConfiguration": {
            "numberOfResults": 4,
            "overrideSearchType": "SEMANTIC",
            "filter": {
                "equals": {
                    "key": "tag",
                    "value": "space"
                }
            }
        }
    },
)

```
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-bedrock/llama_index/retrievers/bedrock/base.py`  
| 
```
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
```
 | 
```
classAmazonKnowledgeBasesRetriever(BaseRetriever):
"""
    `Amazon Bedrock Knowledge Bases` retrieval.

    See https://aws.amazon.com/bedrock/knowledge-bases for more info.

    Args:
        knowledge_base_id: Knowledge Base ID.
        retrieval_config: Configuration for retrieval.
        profile_name: The name of the profile in the ~/.aws/credentials
            or ~/.aws/config files, which has either access keys or role information
            specified. If not specified, the default credential profile or, if on an
            EC2 instance, credentials from IMDS will be used.
        region_name: The aws region e.g., `us-west-2`.
            Fallback to AWS_DEFAULT_REGION env variable or region specified in
            ~/.aws/config.
        aws_access_key_id: The aws access key id.
        aws_secret_access_key: The aws secret access key.
        aws_session_token: AWS temporary session token.

    Example:
        .. code-block:: python

            from llama_index.retrievers.bedrock import AmazonKnowledgeBasesRetriever

            retriever = AmazonKnowledgeBasesRetriever(
                knowledge_base_id="<knowledge-base-id>",
                retrieval_config={
                    "vectorSearchConfiguration": {
                        "numberOfResults": 4,
                        "overrideSearchType": "SEMANTIC",
                        "filter": {
                            "equals": {
                                "key": "tag",
                                "value": "space"






    """

    def__init__(
        self,
        knowledge_base_id: str,
        retrieval_config: Optional[Dict[str, Any]] = None,
        profile_name: Optional[str] = None,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
    ):
        # Keep existing sync client for backward compatibility
        self._client = get_aws_service_client(
            service_name="bedrock-agent-runtime",
            profile_name=profile_name,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )

        # Create async session with the same credentials
        self._async_session = aioboto3.Session(
            profile_name=profile_name,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )

        self.knowledge_base_id = knowledge_base_id
        self.retrieval_config = retrieval_config
        super().__init__(callback_manager)

    def_parse_response(self, response: Dict[str, Any]) -> List[NodeWithScore]:
"""Parse Knowledge Base response into NodeWithScore objects."""
        results = response["retrievalResults"]
        node_with_score = []

        for result in results:
            metadata = {}
            if "location" in result:
                metadata["location"] = result["location"]
            if "metadata" in result:
                metadata["sourceMetadata"] = result["metadata"]

            node_with_score.append(
                NodeWithScore(
                    node=TextNode(
                        text=result["content"]["text"],
                        metadata=metadata,
                    ),
                    score=result["score"] if "score" in result else 0,
                )
            )

        return node_with_score

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Synchronous retrieve method."""
        query = query_bundle.query_str

        response = self._client.retrieve(
            retrievalQuery={"text": query.strip()},
            knowledgeBaseId=self.knowledge_base_id,
            retrievalConfiguration=self.retrieval_config,
        )

        return self._parse_response(response)

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Asynchronous retrieve method."""
        query = query_bundle.query_str

        async with self._async_session.client("bedrock-agent-runtime") as client:
            response = await client.retrieve(
                retrievalQuery={"text": query.strip()},
                knowledgeBaseId=self.knowledge_base_id,
                retrievalConfiguration=self.retrieval_config,
            )

            return self._parse_response(response)

```
 |  
| --- | --- |  
options: members: - AmazonKnowledgeBasesRetriever
