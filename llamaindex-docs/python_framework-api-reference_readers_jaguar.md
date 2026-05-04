# Jaguar
##  JaguarReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/jaguar/#llama_index.readers.jaguar.JaguarReader "Permanent link")
Bases: 
Jaguar reader. Retrieve documents from existing persisted Jaguar store.
Source code in `llama-index-integrations/readers/llama-index-readers-jaguar/llama_index/readers/jaguar/base.py`  
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
252
253
254
255
256
```
 | 
```
classJaguarReader(BaseReader):
"""
    Jaguar reader.
    Retrieve documents from existing persisted Jaguar store.
    """

    def__init__(
        self,
        pod: str,
        store: str,
        vector_index: str,
        vector_type: str,
        vector_dimension: int,
        url: str,
    ):
"""
        Constructor of JaguarReader.

        Args:
            pod: name of the pod (database)
            store: name of vector store in the pod
            vector_index: name of vector index of the store
            vector_type: type of the vector index
            vector_dimension: dimension of the vector index
            url: end point URL of jaguar http server

        """
        self._pod = pod
        self._store = store
        self._vector_index = vector_index
        self._vector_type = vector_type
        self._vector_dimension = vector_dimension
        self._jag = JaguarHttpClient(url)
        self._token = ""

    deflogin(
        self,
        jaguar_api_key: Optional[str] = "",
    ) -> bool:
"""
        Login to jaguar server with a jaguar_api_key or let self._jag find a key.

        Args:
            optional jaguar_api_key (str): API key of user to jaguardb server.
            If not provided, jaguar api key is read from environment variable
            JAGUAR_API_KEY or from file $HOME/.jagrc
        Returns:
            True if successful; False if not successful

        """
        if jaguar_api_key == "":
            jaguar_api_key = self._jag.getApiKey()
        self._jaguar_api_key = jaguar_api_key
        self._token = self._jag.login(jaguar_api_key)
        return self._token != ""

    deflogout(self) -> None:
"""
        Logout from jaguar server to cleanup resources.

        Args: no args
        Returns: None
        """
        self._jag.logout(self._token)

    defload_data(
        self,
        embedding: Optional[List[float]] = None,
        k: int = 10,
        metadata_fields: Optional[List[str]] = None,
        where: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Document]:
"""
        Load data from the jaguar vector store.

        Args:
            embedding: list of float number for vector. If this
                       is given, it returns topk similar documents.
            k: Number of results to return.
            where: "a = '100' or ( b > 100 and c < 200 )"
                   If embedding is not given, it finds values
                   of columns in metadata_fields, and the text value.
            metadata_fields: Optional[List[str]] a list of metadata fields to load
                       in addition to the text document

        Returns:
            List of documents

        """
        if embedding is not None:
            return self._load_similar_data(
                embedding=embedding,
                k=k,
                metadata_fields=metadata_fields,
                where=where,
                **kwargs,
            )
        else:
            return self._load_store_data(
                k=k, metadata_fields=metadata_fields, where=where, **kwargs
            )

    def_load_similar_data(
        self,
        embedding: List[float],
        k: int = 10,
        metadata_fields: Optional[List[str]] = None,
        where: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Document]:
"""Load data by similarity search from the jaguar store."""
        ### args is additional search conditions, such as time decay
        args = kwargs.get("args")
        fetch_k = kwargs.get("fetch_k", -1)

        vcol = self._vector_index
        vtype = self._vector_type
        str_embeddings = [str(f) for f in embedding]
        qv_comma = ",".join(str_embeddings)
        podstore = self._pod + "." + self._store
        q = (
            "select similarity("
            + vcol
            + ",'"
            + qv_comma
            + "','topk="
            + str(k)
            + ",fetch_k="
            + str(fetch_k)
            + ",type="
            + vtype
        )
        q += ",with_score,with_text"
        if args is not None:
            q += "," + args

        if metadata_fields is not None:
            x = "&".join(metadata_fields)
            q += ",metadata=" + x

        q += "') from " + podstore

        if where is not None:
            q += " where " + where

        jarr = self.run(q)
        if jarr is None:
            return []

        docs = []
        for js in jarr:
            score = js["score"]
            text = js["text"]
            zid = js["zid"]

            md = {}
            md["zid"] = zid
            md["score"] = score
            if metadata_fields is not None:
                for m in metadata_fields:
                    md[m] = js[m]

            doc = Document(
                id_=zid,
                text=text,
                metadata=md,
            )
            docs.append(doc)

        return docs

    def_load_store_data(
        self,
        k: int = 10,
        metadata_fields: Optional[List[str]] = None,
        where: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Document]:
"""Load a number of document from the jaguar store."""
        vcol = self._vector_index
        podstore = self._pod + "." + self._store
        txtcol = vcol + ":text"

        sel_str = "zid," + txtcol
        if metadata_fields is not None:
            sel_str += "," + ",".join(metadata_fields)

        q = "select " + sel_str
        q += " from " + podstore

        if where is not None:
            q += " where " + where
        q += " limit " + str(k)

        jarr = self.run(q)
        if jarr is None:
            return []

        docs = []
        for ds in jarr:
            js = json.loads(ds)
            text = js[txtcol]
            zid = js["zid"]

            md = {}
            md["zid"] = zid
            if metadata_fields is not None:
                for m in metadata_fields:
                    md[m] = js[m]

            doc = Document(
                id_=zid,
                text=text,
                metadata=md,
            )
            docs.append(doc)

        return docs

    defrun(self, query: str) -> dict:
"""
        Run any query statement in jaguardb.

        Args:
            query (str): query statement to jaguardb
        Returns:
            None for invalid token, or
            json result string

        """
        if self._token == "":
            return {}

        resp = self._jag.post(query, self._token, False)
        txt = resp.text
        try:
            return json.loads(txt)
        except Exception:
            return {}

    defprt(self, msg: str) -> None:
        nows = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/tmp/debugjaguarrdr.log", "a") as file:
            print(f"{nows} msg={msg}", file=file, flush=True)

```
 |  
| --- | --- |  
###  login [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/jaguar/#llama_index.readers.jaguar.JaguarReader.login "Permanent link")

```
login(jaguar_api_key: Optional[] = '') -> 

```

Login to jaguar server with a jaguar_api_key or let self._jag find a key.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `optional jaguar_api_key`  |  API key of user to jaguardb server.  |  _required_  |  
Returns: True if successful; False if not successful
Source code in `llama-index-integrations/readers/llama-index-readers-jaguar/llama_index/readers/jaguar/base.py`  
| 
```
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
```
 | 
```
deflogin(
    self,
    jaguar_api_key: Optional[str] = "",
) -> bool:
"""
    Login to jaguar server with a jaguar_api_key or let self._jag find a key.

    Args:
        optional jaguar_api_key (str): API key of user to jaguardb server.
        If not provided, jaguar api key is read from environment variable
        JAGUAR_API_KEY or from file $HOME/.jagrc
    Returns:
        True if successful; False if not successful

    """
    if jaguar_api_key == "":
        jaguar_api_key = self._jag.getApiKey()
    self._jaguar_api_key = jaguar_api_key
    self._token = self._jag.login(jaguar_api_key)
    return self._token != ""

```
 |  
| --- | --- |  
###  logout [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/jaguar/#llama_index.readers.jaguar.JaguarReader.logout "Permanent link")

```
logout() -> None

```

Logout from jaguar server to cleanup resources.
Args: no args Returns: None
Source code in `llama-index-integrations/readers/llama-index-readers-jaguar/llama_index/readers/jaguar/base.py`  
| 
```
68
69
70
71
72
73
74
75
```
 | 
```
deflogout(self) -> None:
"""
    Logout from jaguar server to cleanup resources.

    Args: no args
    Returns: None
    """
    self._jag.logout(self._token)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/jaguar/#llama_index.readers.jaguar.JaguarReader.load_data "Permanent link")

```
load_data(
    embedding: Optional[[float]] = None,
    k:  = 10,
    metadata_fields: Optional[[]] = None,
    where: Optional[] = None,
    **kwargs: 
) -> []

```

Load data from the jaguar vector store.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `embedding`  |  `Optional[List[float]]`  |  list of float number for vector. If this is given, it returns topk similar documents.  |  `None`  |  
|  Number of results to return.  |  
|  `where`  |  `Optional[str]`  |  "a = '100' or ( b > 100 and c < 200 )" If embedding is not given, it finds values of columns in metadata_fields, and the text value.  |  `None`  |  
|  `metadata_fields`  |  `Optional[List[str]]`  |  Optional[List[str]] a list of metadata fields to load in addition to the text document  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List of documents  |  
Source code in `llama-index-integrations/readers/llama-index-readers-jaguar/llama_index/readers/jaguar/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    embedding: Optional[List[float]] = None,
    k: int = 10,
    metadata_fields: Optional[List[str]] = None,
    where: Optional[str] = None,
    **kwargs: Any,
) -> List[Document]:
"""
    Load data from the jaguar vector store.

    Args:
        embedding: list of float number for vector. If this
                   is given, it returns topk similar documents.
        k: Number of results to return.
        where: "a = '100' or ( b > 100 and c < 200 )"
               If embedding is not given, it finds values
               of columns in metadata_fields, and the text value.
        metadata_fields: Optional[List[str]] a list of metadata fields to load
                   in addition to the text document

    Returns:
        List of documents

    """
    if embedding is not None:
        return self._load_similar_data(
            embedding=embedding,
            k=k,
            metadata_fields=metadata_fields,
            where=where,
            **kwargs,
        )
    else:
        return self._load_store_data(
            k=k, metadata_fields=metadata_fields, where=where, **kwargs
        )

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/jaguar/#llama_index.readers.jaguar.JaguarReader.run "Permanent link")

```
run(query: ) -> 

```

Run any query statement in jaguardb.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  query statement to jaguardb  |  _required_  |  
Returns: None for invalid token, or json result string
Source code in `llama-index-integrations/readers/llama-index-readers-jaguar/llama_index/readers/jaguar/base.py`  
| 
```
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
defrun(self, query: str) -> dict:
"""
    Run any query statement in jaguardb.

    Args:
        query (str): query statement to jaguardb
    Returns:
        None for invalid token, or
        json result string

    """
    if self._token == "":
        return {}

    resp = self._jag.post(query, self._token, False)
    txt = resp.text
    try:
        return json.loads(txt)
    except Exception:
        return {}

```
 |  
| --- | --- |  
options: members: - JaguarReader
