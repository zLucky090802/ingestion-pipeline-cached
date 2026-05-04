# Cogniswitch
##  CogniswitchToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/cogniswitch/#llama_index.tools.cogniswitch.CogniswitchToolSpec "Permanent link")
Bases: 
Cogniswitch Tool Spec. A toolspec to have store_data and query_knowledge as tools to store the data from a file or a url and answer questions from the knowledge stored respectively.
Source code in `llama-index-integrations/tools/llama-index-tools-cogniswitch/llama_index/tools/cogniswitch/base.py`  
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
```
 | 
```
classCogniswitchToolSpec(BaseToolSpec):
"""
    Cogniswitch Tool Spec.
    A toolspec to have store_data and query_knowledge as tools to store the data from a file or a url
    and answer questions from the knowledge stored respectively.
    """

    spec_functions = ["store_data", "query_knowledge", "knowledge_status"]

    def__init__(
        self,
        cs_token: str,
        apiKey: str,
        OAI_token: Optional[str] = None,
    ) -> None:
"""
        Args:
            cs_token (str): Cogniswitch token.
            OAI_token (str): OpenAI token.
            apiKey (str): Oauth token.

        """
        self.cs_token = cs_token
        if OAI_token:
            self.OAI_token = OAI_token
        elif os.environ["OPENAI_API_KEY"]:
            self.OAI_token = os.environ["OPENAI_API_KEY"]
        else:
            raise ValueError("Please provide the OpenAI token")
        self.apiKey = apiKey
        self.source_URL_endpoint = (
            "https://api.cogniswitch.ai:8243/cs-api/0.0.1/cs/knowledgeSource/url"
        )
        self.source_file_endpoint = (
            "https://api.cogniswitch.ai:8243/cs-api/0.0.1/cs/knowledgeSource/file"
        )
        self.knowledge_request_endpoint = (
            "https://api.cogniswitch.ai:8243/cs-api/0.0.1/cs/knowledgeRequest"
        )
        self.knowledge_status_endpoint = (
            "https://api.cogniswitch.ai:8243/cs-api/0.0.1/cs/knowledgeSource/status"
        )
        self.headers = {
            "apiKey": self.apiKey,
            "platformToken": self.cs_token,
            "openAIToken": self.OAI_token,
        }

    defstore_data(
        self,
        url: Optional[str] = None,
        file: Optional[str] = None,
        document_name: Optional[str] = None,
        document_description: Optional[str] = None,
    ) -> dict:
"""
        Store data using the Cogniswitch service.

        Args:
            url (Optional[str]): URL link.
            file (Optional[str]): file path of your file.
            the current files supported by the files are
            .txt, .pdf, .docx, .doc, .html
            document_name (Optional[str]): Name of the document you are uploading.
            document_description (Optional[str]): Description of the document.



        Returns:
            dict: Response JSON from the Cogniswitch service.

        """
        if not file and not url:
            return {
                "message": "No input provided",
            }
        elif file and url:
            return {
                "message": "Too many inputs, please provide either file or url",
            }
        elif url:
            api_url = self.source_URL_endpoint
            headers = self.headers
            files = None
            data = {
                "url": url,
                "documentName": document_name,
                "documentDescription": document_description,
            }
            response = requests.post(api_url, headers=headers, data=data, files=files)

        elif file:
            api_url = self.source_file_endpoint

            headers = self.headers
            if file is not None:
                files = {"file": open(file, "rb")}
            else:
                files = None
            data = {
                "url": url,
                "documentName": document_name,
                "documentDescription": document_description,
            }
            response = requests.post(api_url, headers=headers, data=data, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            # error_message = response.json()["message"]
            return {
                "message": "Bad Request",
            }

    defquery_knowledge(self, query: str) -> dict:
"""
        Send a query to the Cogniswitch service and retrieve the response.

        Args:
            query (str): Query to be answered.

        Returns:
            dict: Response JSON from the Cogniswitch service.

        """
        api_url = self.knowledge_request_endpoint

        headers = self.headers

        data = {"query": query}
        response = requests.post(api_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            # error_message = response.json()["message"]
            return {
                "message": "Bad Request",
            }

    defknowledge_status(self, document_name: str) -> dict:
"""
        Use this function to know the status of the document or the URL uploaded
        Args:
            document_name (str): The document name or the url that is uploaded.

        Returns:
            dict: Response JSON from the Cogniswitch service.

        """
        params = {"docName": document_name, "platformToken": self.cs_token}
        response = requests.get(
            self.knowledge_status_endpoint,
            headers=self.headers,
            params=params,
        )
        if response.status_code == 200:
            source_info = response.json()
            return source_info[-1]
        else:
            # error_message = response.json()["message"]
            return {
                "message": "Bad Request",
            }

```
 |  
| --- | --- |  
###  store_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/cogniswitch/#llama_index.tools.cogniswitch.CogniswitchToolSpec.store_data "Permanent link")

```
store_data(
    url: Optional[] = None,
    file: Optional[] = None,
    document_name: Optional[] = None,
    document_description: Optional[] = None,
) -> 

```

Store data using the Cogniswitch service.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  `Optional[str]`  |  URL link.  |  `None`  |  
|  `file`  |  `Optional[str]`  |  file path of your file.  |  `None`  |  
|  `document_name`  |  `Optional[str]`  |  Name of the document you are uploading.  |  `None`  |  
|  `document_description`  |  `Optional[str]`  |  Description of the document.  |  `None`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `dict`  |  `dict`  |  Response JSON from the Cogniswitch service.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-cogniswitch/llama_index/tools/cogniswitch/base.py`  
| 
```
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
```
 | 
```
defstore_data(
    self,
    url: Optional[str] = None,
    file: Optional[str] = None,
    document_name: Optional[str] = None,
    document_description: Optional[str] = None,
) -> dict:
"""
    Store data using the Cogniswitch service.

    Args:
        url (Optional[str]): URL link.
        file (Optional[str]): file path of your file.
        the current files supported by the files are
        .txt, .pdf, .docx, .doc, .html
        document_name (Optional[str]): Name of the document you are uploading.
        document_description (Optional[str]): Description of the document.



    Returns:
        dict: Response JSON from the Cogniswitch service.

    """
    if not file and not url:
        return {
            "message": "No input provided",
        }
    elif file and url:
        return {
            "message": "Too many inputs, please provide either file or url",
        }
    elif url:
        api_url = self.source_URL_endpoint
        headers = self.headers
        files = None
        data = {
            "url": url,
            "documentName": document_name,
            "documentDescription": document_description,
        }
        response = requests.post(api_url, headers=headers, data=data, files=files)

    elif file:
        api_url = self.source_file_endpoint

        headers = self.headers
        if file is not None:
            files = {"file": open(file, "rb")}
        else:
            files = None
        data = {
            "url": url,
            "documentName": document_name,
            "documentDescription": document_description,
        }
        response = requests.post(api_url, headers=headers, data=data, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        # error_message = response.json()["message"]
        return {
            "message": "Bad Request",
        }

```
 |  
| --- | --- |  
###  query_knowledge [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/cogniswitch/#llama_index.tools.cogniswitch.CogniswitchToolSpec.query_knowledge "Permanent link")

```
query_knowledge(query: ) -> 

```

Send a query to the Cogniswitch service and retrieve the response.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  Query to be answered.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `dict`  |  `dict`  |  Response JSON from the Cogniswitch service.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-cogniswitch/llama_index/tools/cogniswitch/base.py`  
| 
```
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
```
 | 
```
defquery_knowledge(self, query: str) -> dict:
"""
    Send a query to the Cogniswitch service and retrieve the response.

    Args:
        query (str): Query to be answered.

    Returns:
        dict: Response JSON from the Cogniswitch service.

    """
    api_url = self.knowledge_request_endpoint

    headers = self.headers

    data = {"query": query}
    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        # error_message = response.json()["message"]
        return {
            "message": "Bad Request",
        }

```
 |  
| --- | --- |  
###  knowledge_status [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/cogniswitch/#llama_index.tools.cogniswitch.CogniswitchToolSpec.knowledge_status "Permanent link")

```
knowledge_status(document_name: ) -> 

```

Use this function to know the status of the document or the URL uploaded Args: document_name (str): The document name or the url that is uploaded.
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `dict`  |  `dict`  |  Response JSON from the Cogniswitch service.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-cogniswitch/llama_index/tools/cogniswitch/base.py`  
| 
```
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
```
 | 
```
defknowledge_status(self, document_name: str) -> dict:
"""
    Use this function to know the status of the document or the URL uploaded
    Args:
        document_name (str): The document name or the url that is uploaded.

    Returns:
        dict: Response JSON from the Cogniswitch service.

    """
    params = {"docName": document_name, "platformToken": self.cs_token}
    response = requests.get(
        self.knowledge_status_endpoint,
        headers=self.headers,
        params=params,
    )
    if response.status_code == 200:
        source_info = response.json()
        return source_info[-1]
    else:
        # error_message = response.json()["message"]
        return {
            "message": "Bad Request",
        }

```
 |  
| --- | --- |  
options: members: - CogniswitchToolSpec
