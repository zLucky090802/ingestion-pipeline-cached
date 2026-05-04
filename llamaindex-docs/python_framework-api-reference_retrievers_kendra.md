# Kendra
##  AmazonKendraRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/kendra/#llama_index.retrievers.kendra.AmazonKendraRetriever "Permanent link")
Bases: 
AWS Kendra retriever for LlamaIndex.
See https://aws.amazon.com/kendra/ for more info.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `index_id`  |  Kendra Index ID.  |  _required_  |  
|  `query_config`  |  `Optional[Dict[str, Any]]`  |  Configuration for querying Kendra.  |  `None`  |  
|  `profile_name`  |  `Optional[str]`  |  The name of the profile in the ~/.aws/credentials or ~/.aws/config files, which has either access keys or role information specified. If not specified, the default credential profile or, if on an EC2 instance, credentials from IMDS will be used.  |  `None`  |  
|  `region_name`  |  `Optional[str]`  |  The aws region e.g., `us-west-2`. Fallback to AWS_DEFAULT_REGION env variable or region specified in ~/.aws/config.  |  `None`  |  
|  `aws_access_key_id`  |  `Optional[str]`  |  The aws access key id.  |  `None`  |  
|  `aws_secret_access_key`  |  `Optional[str]`  |  The aws secret access key.  |  `None`  |  
|  `aws_session_token`  |  `Optional[str]`  |  AWS temporary session token.  |  `None`  |  
Example
.. code-block:: python

```
from llama_index.retrievers.kendra import AmazonKendraRetriever

retriever = AmazonKendraRetriever(
    index_id="<kendra-index-id>",
    query_config={
        "PageSize": 4,
        "AttributeFilter": {
            "EqualsTo": {
                "Key": "tag",
                "Value": {"StringValue": "space"}
            }
        }
    },
)

```
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-kendra/llama_index/retrievers/kendra/base.py`  
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
```
 | 
```
classAmazonKendraRetriever(BaseRetriever):
"""
    AWS Kendra retriever for LlamaIndex.

    See https://aws.amazon.com/kendra/ for more info.

    Args:
        index_id: Kendra Index ID.
        query_config: Configuration for querying Kendra.
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

            from llama_index.retrievers.kendra import AmazonKendraRetriever

            retriever = AmazonKendraRetriever(
                index_id="<kendra-index-id>",
                query_config={
                    "PageSize": 4,
                    "AttributeFilter": {
                        "EqualsTo": {
                            "Key": "tag",
                            "Value": {"StringValue": "space"}





    """

    # Mapping of Kendra confidence levels to float scores
    CONFIDENCE_SCORES = {
        "VERY_HIGH": 1.0,
        "HIGH": 0.8,
        "MEDIUM": 0.6,
        "LOW": 0.4,
        "NOT_AVAILABLE": 0.0,
    }

    def__init__(
        self,
        index_id: str,
        query_config: Optional[Dict[str, Any]] = None,
        profile_name: Optional[str] = None,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
    ):
        self._client = get_aws_service_client(
            service_name="kendra",
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
        self.index_id = index_id
        self.query_config = query_config or {}
        super().__init__(callback_manager)

    def_parse_response(self, response: Dict[str, Any]) -> List[NodeWithScore]:
"""Parse Kendra response into NodeWithScore objects."""
        node_with_score = []
        result_items = response.get("ResultItems", [])

        for result in result_items:
            text = ""
            metadata = {}

            # Extract text based on result type
            if result.get("Type") == "ANSWER":
                text = (
                    result.get("AdditionalAttributes", [{}])[0]
                    .get("Value", {})
                    .get("TextWithHighlightsValue", {})
                    .get("Text", "")
                )
            elif result.get("Type") == "DOCUMENT":
                text = result.get("DocumentExcerpt", {}).get("Text", "")

            # Extract metadata
            if "DocumentId" in result:
                metadata["document_id"] = result["DocumentId"]
            if "DocumentTitle" in result:
                metadata["title"] = result.get("DocumentTitle", {}).get("Text", "")
            if "DocumentURI" in result:
                metadata["source"] = result["DocumentURI"]

            # Only create nodes for results with actual content
            if text:
                # Convert Kendra's confidence score to float
                confidence = result.get("ScoreAttributes", {}).get(
                    "ScoreConfidence", "NOT_AVAILABLE"
                )
                score = self.CONFIDENCE_SCORES.get(confidence, 0.0)

                node_with_score.append(
                    NodeWithScore(
                        node=TextNode(
                            text=text,
                            metadata=metadata,
                        ),
                        score=score,
                    )
                )

        return node_with_score

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Synchronous retrieve method."""
        query = query_bundle.query_str

        query_params = {
            "IndexId": self.index_id,
            "QueryText": query.strip(),
            **self.query_config,
        }

        response = self._client.query(**query_params)
        return self._parse_response(response)

    async def_aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
"""Asynchronous retrieve method."""
        query = query_bundle.query_str

        query_params = {
            "IndexId": self.index_id,
            "QueryText": query.strip(),
            **self.query_config,
        }

        async with self._async_session.client("kendra") as client:
            response = await client.query(**query_params)
            return self._parse_response(response)

```
 |  
| --- | --- |  
options: members: - AmazonKendraRetriever
