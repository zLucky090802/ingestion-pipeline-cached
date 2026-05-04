# Galaxia
##  GalaxiaRetriever [#](https://developers.llamaindex.ai/python/framework-api-reference/retrievers/galaxia/#llama_index.retrievers.galaxia.GalaxiaRetriever "Permanent link")
Bases: 
Galaxia knowledge retriever.
before using the API create your knowledge base here: beta.cloud.smabbler.com/
learn more here: https://smabbler.gitbook.io/smabbler/api-rag/smabblers-api-rag
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_url `  |  url of galaxia API, e.g. "https://beta.api.smabbler.com"  |  _required_  |  
|  `api_key `  |  API key  |  _required_  |  
|  `knowledge_base_id `  |  ID of the knowledge base (galaxia model)  |  _required_  |  
Example
.. code-block:: python

```
from llama_index.retrievers.galaxia import GalaxiaRetriever
from llama_index.core.schema import QueryBundle

retriever = GalaxiaRetriever(
    api_url="beta.api.smabbler.com",
    api_key="<key>",
    knowledge_base_id="<knowledge_base_id>",
)

result = retriever._retrieve(QueryBundle(
    "<test question>"
))

print(result)

```
Source code in `llama-index-integrations/retrievers/llama-index-retrievers-galaxia/llama_index/retrievers/galaxia/base.py`  
| 
```
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
```
 | 
```
classGalaxiaRetriever(BaseRetriever):
"""
    Galaxia knowledge retriever.

    before using the API create your knowledge base here:
    beta.cloud.smabbler.com/

    learn more here:
    https://smabbler.gitbook.io/smabbler/api-rag/smabblers-api-rag

    Args:
        api_url : url of galaxia API, e.g. "https://beta.api.smabbler.com"
        api_key : API key
        knowledge_base_id : ID of the knowledge base (galaxia model)

    Example:
        .. code-block:: python

            from llama_index.retrievers.galaxia import GalaxiaRetriever
            from llama_index.core.schema import QueryBundle

            retriever = GalaxiaRetriever(
                api_url="beta.api.smabbler.com",
                api_key="<key>",
                knowledge_base_id="<knowledge_base_id>",


            result = retriever._retrieve(QueryBundle(
                "<test question>"


            print(result)

    """

    def__init__(
        self,
        api_url: str,
        api_key: str,
        knowledge_base_id: str,
        n_retries: int = 20,
        wait_time: int = 2,
        callback_manager: Optional[CallbackManager] = None,
    ):
        self._client = GalaxiaClient(
            api_url, api_key, knowledge_base_id, n_retries, wait_time
        )

        super().__init__(callback_manager)

    def_retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        query = query_bundle.query_str
        response = self._client.retrieve(query)

        if response is None:
            return []

        node_with_score = []

        for res in response:
            node_with_score.append(
                NodeWithScore(
                    node=TextNode(
                        text=res["category"],
                        metadata={
                            "model": res["model"],
                            "file": res["group"],
                        },
                    ),
                    score=res["rank"],
                )
            )

        return node_with_score

```
 |  
| --- | --- |  
options: members: - GalaxiaRetriever
