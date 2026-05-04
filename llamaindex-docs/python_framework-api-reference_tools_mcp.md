# Mcp
##  McpToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.McpToolSpec "Permanent link")
Bases: , `TypeResolutionMixin`, `TypeCreationMixin`, `FieldExtractionMixin`
MCPToolSpec will get the tools from MCP Client (only need to implement ClientSession) and convert them to LlamaIndex's FunctionTool objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `client`  |  `ClientSession`  |  An MCP client instance implementing ClientSession, and it should support the following methods in ClientSession: - list_tools: List all tools. - call_tool: Call a tool. - list_resources: List all resources. - read_resource: Read a resource.  |  _required_  |  
|  `allowed_tools`  |  `Optional[List[str]]`  |  If set, only return tools with the specified names.  |  `None`  |  
|  `global_partial_params`  |  `Optional[Dict[str, Any]]`  |  A dict of params to apply to all tools globally.  |  `None`  |  
|  `partial_params_by_tool`  |  `Optional[Dict[str, Dict[str, Any]]]`  |  A dict mapping tool names to param overrides. Values override global_partial_params. Use None as a value to remove a global param for a specific tool.  |  `None`  |  
|  `include_resources`  |  `bool`  |  Whether to include resources in the tool list.  |  `False`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/base.py`  
| 
```
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
257
258
259
```
 | 
```
classMcpToolSpec(
    BaseToolSpec, TypeResolutionMixin, TypeCreationMixin, FieldExtractionMixin
):
"""
    MCPToolSpec will get the tools from MCP Client (only need to implement ClientSession) and convert them to LlamaIndex's FunctionTool objects.

    Args:
        client: An MCP client instance implementing ClientSession, and it should support the following methods in ClientSession:
            - list_tools: List all tools.
            - call_tool: Call a tool.
            - list_resources: List all resources.
            - read_resource: Read a resource.
        allowed_tools: If set, only return tools with the specified names.
        global_partial_params: A dict of params to apply to all tools globally.
        partial_params_by_tool: A dict mapping tool names to param overrides. Values override global_partial_params. Use None as a value to remove a global param for a specific tool.
        include_resources: Whether to include resources in the tool list.

    """

    def__init__(
        self,
        client: ClientSession,
        allowed_tools: Optional[List[str]] = None,
        global_partial_params: Optional[Dict[str, Any]] = None,
        partial_params_by_tool: Optional[Dict[str, Dict[str, Any]]] = None,
        include_resources: bool = False,
    ) -> None:
        self.client = client
        self.allowed_tools = allowed_tools
        self.global_partial_params = global_partial_params
        self.partial_params_by_tool = partial_params_by_tool
        self.include_resources = include_resources
        self.properties_cache = {}

    async deffetch_tools(self) -> List[Any]:
"""
        An asynchronous method to get the tools list from MCP Client. If allowed_tools is set, it will filter the tools.

        Returns:
            A list of tools, each tool object needs to contain name, description, inputSchema properties.

        """
        response = await self.client.list_tools()
        tools = response.tools if hasattr(response, "tools") else []

        if self.allowed_tools is None:
            # get all tools by default
            return tools

        if any(self.allowed_tools):
            return [tool for tool in tools if tool.name in self.allowed_tools]

        logging.warning(
            "Returning an empty tool list due to the empty `allowed_tools` list. Please ensure `allowed_tools` is set appropriately."
        )
        return []

    async deffetch_resources(self) -> List[Resource]:
"""
        An asynchronous method to get the resources list from MCP Client.
        """
        static_response = await self.client.list_resources()
        dynamic_response = await self.client.list_resource_templates()
        static_resources = (
            static_response.resources if hasattr(static_response, "resources") else []
        )
        dynamic_resources = (
            dynamic_response.resourceTemplates
            if hasattr(dynamic_response, "resourceTemplates")
            else []
        )
        resources = static_resources + dynamic_resources
        if self.allowed_tools is None:
            return resources

        if any(self.allowed_tools):
            return [
                resource
                for resource in resources
                if resource.name in self.allowed_tools
            ]

        logging.warning(
            "Returning an empty resource list due to the empty `allowed_tools` list. Please ensure `allowed_tools` is set appropriately."
        )
        return []

    def_create_tool_fn(self, tool_name: str) -> Callable:
"""
        Create a tool call function for a specified MCP tool name. The function internally wraps the call_tool call to the MCP Client.
        """

        async defasync_tool_fn(**kwargs):
            return await self.client.call_tool(tool_name, kwargs)

        return async_tool_fn

    def_create_resource_fn(self, resource_uri: str) -> Callable:
"""
        Create a resource call function for a specified MCP resource name. The function internally wraps the read_resource call to the MCP Client.
        """

        async defasync_resource_fn():
            return await self.client.read_resource(resource_uri)

        return async_resource_fn

    async defto_tool_list_async(self) -> List[FunctionTool]:
"""
        Asynchronous method to convert MCP tools to FunctionTool objects.

        Returns:
            A list of FunctionTool objects.

        """
        tools_list = await self.fetch_tools()
        function_tool_list: List[FunctionTool] = []
        for tool in tools_list:
            fn = self._create_tool_fn(tool.name)
            # Create a Pydantic model based on the tool inputSchema
            model_schema = self.create_model_from_json_schema(
                tool.inputSchema, model_name=f"{tool.name}_Schema"
            )
            # Set up global partial params as default
            tool_partial_params = dict(self.global_partial_params or {})
            # Override with tool-specific partial params
            if self.partial_params_by_tool and tool.name in self.partial_params_by_tool:
                tool_overrides = self.partial_params_by_tool[tool.name]
                for key, value in tool_overrides.items():
                    if value is None:
                        # Remove the param if set to None
                        tool_partial_params.pop(key, None)
                    else:
                        # Override or add the param
                        tool_partial_params[key] = value

            # Remove fields that are set as partial params
            if tool_partial_params:
                model_schema = self.remove_model_fields(
                    model_schema,
                    fields_to_remove=set(tool_partial_params),
                    model_name=f"{tool.name}_Schema",
                )

            metadata = ToolMetadata(
                name=tool.name,
                description=tool.description,
                fn_schema=model_schema,
            )
            function_tool = FunctionTool.from_defaults(
                async_fn=fn, tool_metadata=metadata, partial_params=tool_partial_params
            )
            function_tool_list.append(function_tool)

        if self.include_resources:
            resources_list = await self.fetch_resources()
            for resource in resources_list:
                if hasattr(resource, "uri"):
                    uri = resource.uri
                elif hasattr(resource, "template"):
                    uri = resource.template
                fn = self._create_resource_fn(uri)
                function_tool_list.append(
                    FunctionTool.from_defaults(
                        async_fn=fn,
                        name=resource.name.replace("/", "_"),
                        description=resource.description,
                    )
                )

        return function_tool_list

    defto_tool_list(self) -> List[FunctionTool]:
"""
        Synchronous interface: Convert MCP Client tools to FunctionTool objects.
        Note: This method should not be called in an asynchronous environment, otherwise an exception will be thrown. Use to_tool_list_async instead.

        Returns:
            A list of FunctionTool objects.

        """
        return patch_sync(self.to_tool_list_async)()

    defcreate_model_from_json_schema(
        self,
        schema: dict[str, Any],
        model_name: str = "DynamicModel",
    ) -> type[BaseModel]:
"""
        To create a Pydantic model from the JSON Schema of MCP tools.

        Args:
            schema: A JSON Schema dictionary containing properties and required fields.
            model_name: The name of the model.

        Returns:
            A Pydantic model class.

        """
        defs = schema.get("$defs", {})

        # Process all type definitions
        for cls_name, cls_schema in defs.items():
            self.properties_cache[cls_name] = self._create_model(
                cls_schema,
                cls_name,
                defs,
            )

        return self._create_model(schema, model_name)

    def_create_model(
        self,
        schema: dict,
        model_name: str,
        defs: dict = {},
    ) -> type[BaseModel]:
"""Create a Pydantic model from a schema."""
        if model_name in self.properties_cache:
            return self.properties_cache[model_name]

        fields = self._extract_fields(schema, defs)
        model = create_model(model_name, **fields)
        self.properties_cache[model_name] = model
        return model

    defremove_model_fields(
        self,
        model: type[BaseModel],
        fields_to_remove: Set[str],
        model_name: str,
    ) -> type[BaseModel]:
        fields = {
            name: (
                field.annotation,
                field.default if field.is_required() else field.default,
            )
            for name, field in model.model_fields.items()
            if name not in fields_to_remove
        }
        return create_model(model_name, **fields)

```
 |  
| --- | --- |  
###  fetch_tools [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.McpToolSpec.fetch_tools "Permanent link")

```
fetch_tools() -> []

```

An asynchronous method to get the tools list from MCP Client. If allowed_tools is set, it will filter the tools.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[Any]`  |  A list of tools, each tool object needs to contain name, description, inputSchema properties.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/base.py`  
| 
```
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
```
 | 
```
async deffetch_tools(self) -> List[Any]:
"""
    An asynchronous method to get the tools list from MCP Client. If allowed_tools is set, it will filter the tools.

    Returns:
        A list of tools, each tool object needs to contain name, description, inputSchema properties.

    """
    response = await self.client.list_tools()
    tools = response.tools if hasattr(response, "tools") else []

    if self.allowed_tools is None:
        # get all tools by default
        return tools

    if any(self.allowed_tools):
        return [tool for tool in tools if tool.name in self.allowed_tools]

    logging.warning(
        "Returning an empty tool list due to the empty `allowed_tools` list. Please ensure `allowed_tools` is set appropriately."
    )
    return []

```
 |  
| --- | --- |  
###  fetch_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.McpToolSpec.fetch_resources "Permanent link")

```
fetch_resources() -> [Resource]

```

An asynchronous method to get the resources list from MCP Client.
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/base.py`  
| 
```
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
```
 | 
```
async deffetch_resources(self) -> List[Resource]:
"""
    An asynchronous method to get the resources list from MCP Client.
    """
    static_response = await self.client.list_resources()
    dynamic_response = await self.client.list_resource_templates()
    static_resources = (
        static_response.resources if hasattr(static_response, "resources") else []
    )
    dynamic_resources = (
        dynamic_response.resourceTemplates
        if hasattr(dynamic_response, "resourceTemplates")
        else []
    )
    resources = static_resources + dynamic_resources
    if self.allowed_tools is None:
        return resources

    if any(self.allowed_tools):
        return [
            resource
            for resource in resources
            if resource.name in self.allowed_tools
        ]

    logging.warning(
        "Returning an empty resource list due to the empty `allowed_tools` list. Please ensure `allowed_tools` is set appropriately."
    )
    return []

```
 |  
| --- | --- |  
###  to_tool_list_async [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.McpToolSpec.to_tool_list_async "Permanent link")

```
to_tool_list_async() -> []

```

Asynchronous method to convert MCP tools to FunctionTool objects.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[FunctionTool[](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool "FunctionTool \(llama_index.core.tools.function_tool.FunctionTool\)")]`  |  A list of FunctionTool objects.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/base.py`  
| 
```
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
```
 | 
```
async defto_tool_list_async(self) -> List[FunctionTool]:
"""
    Asynchronous method to convert MCP tools to FunctionTool objects.

    Returns:
        A list of FunctionTool objects.

    """
    tools_list = await self.fetch_tools()
    function_tool_list: List[FunctionTool] = []
    for tool in tools_list:
        fn = self._create_tool_fn(tool.name)
        # Create a Pydantic model based on the tool inputSchema
        model_schema = self.create_model_from_json_schema(
            tool.inputSchema, model_name=f"{tool.name}_Schema"
        )
        # Set up global partial params as default
        tool_partial_params = dict(self.global_partial_params or {})
        # Override with tool-specific partial params
        if self.partial_params_by_tool and tool.name in self.partial_params_by_tool:
            tool_overrides = self.partial_params_by_tool[tool.name]
            for key, value in tool_overrides.items():
                if value is None:
                    # Remove the param if set to None
                    tool_partial_params.pop(key, None)
                else:
                    # Override or add the param
                    tool_partial_params[key] = value

        # Remove fields that are set as partial params
        if tool_partial_params:
            model_schema = self.remove_model_fields(
                model_schema,
                fields_to_remove=set(tool_partial_params),
                model_name=f"{tool.name}_Schema",
            )

        metadata = ToolMetadata(
            name=tool.name,
            description=tool.description,
            fn_schema=model_schema,
        )
        function_tool = FunctionTool.from_defaults(
            async_fn=fn, tool_metadata=metadata, partial_params=tool_partial_params
        )
        function_tool_list.append(function_tool)

    if self.include_resources:
        resources_list = await self.fetch_resources()
        for resource in resources_list:
            if hasattr(resource, "uri"):
                uri = resource.uri
            elif hasattr(resource, "template"):
                uri = resource.template
            fn = self._create_resource_fn(uri)
            function_tool_list.append(
                FunctionTool.from_defaults(
                    async_fn=fn,
                    name=resource.name.replace("/", "_"),
                    description=resource.description,
                )
            )

    return function_tool_list

```
 |  
| --- | --- |  
###  to_tool_list [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.McpToolSpec.to_tool_list "Permanent link")

```
to_tool_list() -> []

```

Synchronous interface: Convert MCP Client tools to FunctionTool objects. Note: This method should not be called in an asynchronous environment, otherwise an exception will be thrown. Use to_tool_list_async instead.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[FunctionTool[](https://developers.llamaindex.ai/python/framework-api-reference/tools/function/#llama_index.core.tools.function_tool.FunctionTool "FunctionTool \(llama_index.core.tools.function_tool.FunctionTool\)")]`  |  A list of FunctionTool objects.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/base.py`  
| 
```
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
```
 | 
```
defto_tool_list(self) -> List[FunctionTool]:
"""
    Synchronous interface: Convert MCP Client tools to FunctionTool objects.
    Note: This method should not be called in an asynchronous environment, otherwise an exception will be thrown. Use to_tool_list_async instead.

    Returns:
        A list of FunctionTool objects.

    """
    return patch_sync(self.to_tool_list_async)()

```
 |  
| --- | --- |  
###  create_model_from_json_schema [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.McpToolSpec.create_model_from_json_schema "Permanent link")

```
create_model_from_json_schema(
    schema: [, ], model_name:  = "DynamicModel"
) -> [BaseModel]

```

To create a Pydantic model from the JSON Schema of MCP tools.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `schema`  |  `dict[str, Any]`  |  A JSON Schema dictionary containing properties and required fields.  |  _required_  |  
|  `model_name`  |  The name of the model.  |  `'DynamicModel'`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `type[BaseModel]`  |  A Pydantic model class.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/base.py`  
| 
```
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
```
 | 
```
defcreate_model_from_json_schema(
    self,
    schema: dict[str, Any],
    model_name: str = "DynamicModel",
) -> type[BaseModel]:
"""
    To create a Pydantic model from the JSON Schema of MCP tools.

    Args:
        schema: A JSON Schema dictionary containing properties and required fields.
        model_name: The name of the model.

    Returns:
        A Pydantic model class.

    """
    defs = schema.get("$defs", {})

    # Process all type definitions
    for cls_name, cls_schema in defs.items():
        self.properties_cache[cls_name] = self._create_model(
            cls_schema,
            cls_name,
            defs,
        )

    return self._create_model(schema, model_name)

```
 |  
| --- | --- |  
##  BasicMCPClient [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.BasicMCPClient "Permanent link")
Bases: `ClientSession`
Basic MCP client that can be used to connect to an MCP server.
This is useful for connecting to any MCP server.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `command_or_url`  |  The command to run or the URL to connect to.  |  _required_  |  
|  `args`  |  `Optional[List[str]]`  |  The arguments to pass to StdioServerParameters.  |  `None`  |  
|  `env`  |  `Optional[Dict[str, str]]`  |  The environment variables to set for StdioServerParameters.  |  `None`  |  
|  `timeout`  |  The timeout for HTTP operations in seconds. Default is 30.  |  
|  `sse_read_timeout`  |  The timeout for SSE read operations in seconds. Default is 300 (5 minutes).  |  `300`  |  
|  `auth`  |  `Optional[OAuthClientProvider]`  |  Optional OAuth client provider for authentication.  |  `None`  |  
|  `sampling_callback`  |  `Optional[Callable[[CreateMessageRequestParams], Awaitable[CreateMessageResult]]]`  |  Optional callback for handling sampling messages.  |  `None`  |  
|  `headers`  |  `Optional[Dict[str, Any]]`  |  Optional headers to pass by sse client or streamable http client  |  `None`  |  
|  `tool_call_logs_callback`  |  `Optional[Callable[[List[str]], Awaitable[Any]]]`  |  Async function to store the logs deriving from an MCP tool call: logs are provided as a list of strings, representing log messages. Defaults to None.  |  `None`  |  
|  `http_client`  |  `Optional[AsyncClient]`  |  Optional httpx AsyncClient to use for Streamable transport. Will ignore timeout and headers parameters if provided.  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/client.py`  
| 
```
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
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
```
 | 
```
classBasicMCPClient(ClientSession):
"""
    Basic MCP client that can be used to connect to an MCP server.

    This is useful for connecting to any MCP server.

    Args:
        command_or_url: The command to run or the URL to connect to.
        args: The arguments to pass to StdioServerParameters.
        env: The environment variables to set for StdioServerParameters.
        timeout: The timeout for HTTP operations in seconds. Default is 30.
        sse_read_timeout: The timeout for SSE read operations in seconds. Default is 300 (5 minutes).
        auth: Optional OAuth client provider for authentication.
        sampling_callback: Optional callback for handling sampling messages.
        headers: Optional headers to pass by sse client or streamable http client
        tool_call_logs_callback: Async function to store the logs deriving from an MCP tool call: logs are provided as a list of strings, representing log messages. Defaults to None.
        http_client: Optional httpx AsyncClient to use for Streamable transport. Will ignore timeout and headers parameters if provided.

    """

    def__init__(
        self,
        command_or_url: str,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        sse_read_timeout: int = 300,
        auth: Optional[OAuthClientProvider] = None,
        sampling_callback: Optional[
            Callable[
                [types.CreateMessageRequestParams], Awaitable[types.CreateMessageResult]
            ]
        ] = None,
        headers: Optional[Dict[str, Any]] = None,
        tool_call_logs_callback: Optional[Callable[[List[str]], Awaitable[Any]]] = None,
        http_client: Optional[AsyncClient] = None,
    ):
        self.command_or_url = command_or_url
        self.args = args or []
        self.env = env or {}
        self.timeout = timeout
        self.sse_read_timeout = sse_read_timeout
        self.auth = auth
        self.sampling_callback = sampling_callback
        self.headers = headers
        self.tool_call_logs_callback = tool_call_logs_callback
        self.client_provided = http_client is not None
        self.http_client = (
            http_client
            if self.client_provided
            else create_mcp_http_client(
                timeout=Timeout(timeout, read=sse_read_timeout), headers=headers
            )
        )
        if auth is not None:
            self.http_client.auth = auth

    @classmethod
    defwith_oauth(
        cls,
        command_or_url: str,
        client_name: str,
        redirect_uris: List[str],
        redirect_handler: Callable[[str], None],
        callback_handler: Callable[[], Tuple[str, Optional[str]]],
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        sse_read_timeout: int = 300,
        token_storage: Optional[TokenStorage] = None,
        tool_call_logs_callback: Optional[Callable[[List[str]], Awaitable[Any]]] = None,
        http_client: Optional[AsyncClient] = None,
    ) -> "BasicMCPClient":
"""
        Create a client with OAuth authentication.

        Args:
            command_or_url: The command to run or the URL to connect to
            client_name: The name of the OAuth client
            redirect_uris: The redirect URIs for the OAuth flow
            redirect_handler: Function that handles the redirect URL
            callback_handler: Function that returns the auth code and state
            token_storage: Optional token storage for OAuth client. If not provided,
                           a default in-memory storage is used (tokens will be lost on restart).
            args: The arguments to pass to StdioServerParameters.
            env: The environment variables to set for StdioServerParameters.
            timeout: The timeout for HTTP operations in seconds. Default is 30.
            sse_read_timeout: The timeout for SSE read operations in seconds. Default is 300.
            tool_call_logs_callback: Async function to store the logs deriving from an MCP tool call: logs are provided as a list of strings, representing log messages. Defaults to None.
            http_client: Optional httpx AsyncClient to use for Streamable transport. Will ignore timeout and headers parameters if provided.

        Returns:
            An authenticated MCP client

        """
        # Use default in-memory storage if none provided
        if token_storage is None:
            token_storage = DefaultInMemoryTokenStorage()
            warnings.warn(
                "Using default in-memory token storage. Tokens will be lost on restart.",
                UserWarning,
            )

        oauth_auth = OAuthClientProvider(
            server_url=command_or_url if urlparse(command_or_url).scheme else None,
            client_metadata=OAuthClientMetadata(
                client_name=client_name,
                redirect_uris=redirect_uris,
                grant_types=["authorization_code", "refresh_token"],
                response_types=["code"],
            ),
            redirect_handler=redirect_handler,
            callback_handler=callback_handler,
            storage=token_storage,
        )

        return cls(
            command_or_url,
            auth=oauth_auth,
            args=args,
            env=env,
            timeout=timeout,
            sse_read_timeout=sse_read_timeout,
            tool_call_logs_callback=tool_call_logs_callback,
            http_client=http_client,
        )

    @asynccontextmanager
    async def_run_session(self) -> AsyncIterator[ClientSession]:
"""Create and initialize a session with the MCP server."""
        url = urlparse(self.command_or_url)
        scheme = url.scheme

        if scheme in ("http", "https"):
            # Check if this is a streamable HTTP endpoint (default) or SSE
            if enable_sse(self.command_or_url):
                # SSE transport
                async with sse_client(
                    self.command_or_url,
                    auth=self.auth,
                    headers=self.headers,
                    timeout=self.timeout,
                    sse_read_timeout=self.sse_read_timeout,
                ) as streams:
                    async with ClientSession(
                        *streams,
                        read_timeout_seconds=timedelta(seconds=self.timeout),
                        sampling_callback=self.sampling_callback,
                    ) as session:
                        await session.initialize()
                        yield session
            else:
                # Streamable HTTP transport (recommended)
                async with streamable_http_client(
                    url=self.command_or_url,
                    http_client=self.http_client,
                ) as (read, write, _):
                    async with ClientSession(
                        read,
                        write,
                        read_timeout_seconds=timedelta(seconds=self.timeout),
                        sampling_callback=self.sampling_callback,
                    ) as session:
                        await session.initialize()
                        yield session
        else:
            # stdio transport
            server_parameters = StdioServerParameters(
                command=self.command_or_url, args=self.args, env=self.env
            )
            async with stdio_client(server_parameters) as streams:
                async with ClientSession(
                    *streams,
                    read_timeout_seconds=timedelta(seconds=self.timeout),
                    sampling_callback=self.sampling_callback,
                ) as session:
                    await session.initialize()
                    yield session

    def_configure_tool_call_logs_callback(self) -> io.StringIO:
        handler = io.StringIO()
        stream_handler = logging.StreamHandler(handler)

        # Configure logging to capture all events
        logging.basicConfig(
            level=logging.DEBUG,  # Capture all log levels
            format="%(asctime)s%(name)s%(levelname)s%(message)s\n",
            handlers=[
                stream_handler,
            ],
        )
        # Also enable logging for specific FastMCP components
        fastmcp_logger = logging.getLogger("fastmcp")
        fastmcp_logger.setLevel(logging.DEBUG)

        # Enable HTTP transport logging to see network details
        http_logger = logging.getLogger("httpx")
        http_logger.setLevel(logging.DEBUG)

        return handler

    # Tool methods
    async defcall_tool(
        self,
        tool_name: str,
        arguments: Optional[dict] = None,
        progress_callback: Optional[ProgressFnT] = None,
    ) -> types.CallToolResult:
"""Call a tool on the MCP server."""
        if self.tool_call_logs_callback is not None:
            # we use a string stream so that we can recover all logs at the end of the session
            handler = self._configure_tool_call_logs_callback()

            async with self._run_session() as session:
                result = await session.call_tool(
                    tool_name, arguments=arguments, progress_callback=progress_callback
                )

                # get all logs by dividing the string with \n, since the format of the log has an \n at the end of the log message
                extra_values = handler.getvalue().split("\n")

                # pipe the logs list into tool_call_logs_callback
                await self.tool_call_logs_callback(extra_values)

                return result
        else:
            async with self._run_session() as session:
                return await session.call_tool(
                    tool_name, arguments=arguments, progress_callback=progress_callback
                )

    async deflist_tools(self) -> types.ListToolsResult:
"""List all available tools on the MCP server."""
        async with self._run_session() as session:
            return await session.list_tools()

    # Resource methods
    async deflist_resources(self) -> types.ListToolsResult:
"""List all available resources on the MCP server."""
        async with self._run_session() as session:
            return await session.list_resources()

    async deflist_resource_templates(self) -> types.ListToolsResult:
"""List all dynamic available resources on the MCP server."""
        async with self._run_session() as session:
            return await session.list_resource_templates()

    async defread_resource(self, resource_uri: AnyUrl) -> types.ReadResourceResult:
"""
        Read a resource from the MCP server.

        Returns:
            Tuple containing the resource content as bytes and the MIME type

        """
        async with self._run_session() as session:
            return await session.read_resource(resource_uri)

    ## ----- Prompt methods -----

    async deflist_prompts(self) -> List[types.Prompt]:
"""List all available prompts on the MCP server."""
        async with self._run_session() as session:
            return await session.list_prompts()

    async defget_prompt(
        self, prompt_name: str, arguments: Optional[Dict[str, str]] = None
    ) -> List[ChatMessage]:
"""
        Get a prompt from the MCP server.

        Args:
            prompt_name: The name of the prompt to get
            arguments: Optional arguments to pass to the prompt

        Returns:
            The prompt as a list of llama-index ChatMessage objects

        """
        async with self._run_session() as session:
            prompt = await session.get_prompt(prompt_name, arguments)
            llama_messages = []
            for message in prompt.messages:
                if isinstance(message.content, types.TextContent):
                    llama_messages.append(
                        ChatMessage(
                            role=message.role,
                            blocks=[TextBlock(text=message.content.text)],
                        )
                    )
                elif isinstance(message.content, types.ImageContent):
                    llama_messages.append(
                        ChatMessage(
                            role=message.role,
                            blocks=[
                                ImageBlock(
                                    image=message.content.data,
                                    image_mimetype=message.content.mimeType,
                                )
                            ],
                        )
                    )
                elif isinstance(message.content, types.EmbeddedResource):
                    raise NotImplementedError(
                        "Embedded resources are not supported yet"
                    )
                else:
                    raise ValueError(
                        f"Unsupported content type: {type(message.content)}"
                    )

            return llama_messages

```
 |  
| --- | --- |  
###  with_oauth `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.BasicMCPClient.with_oauth "Permanent link")

```
with_oauth(
    command_or_url: ,
    client_name: ,
    redirect_uris: [],
    redirect_handler: Callable[[], None],
    callback_handler: Callable[
        [], Tuple[, Optional[]]
    ],
    args: Optional[[]] = None,
    env: Optional[[, ]] = None,
    timeout:  = 30,
    sse_read_timeout:  = 300,
    token_storage: Optional[TokenStorage] = None,
    tool_call_logs_callback: Optional[
        Callable[[[]], Awaitable[]]
    ] = None,
    http_client: Optional[AsyncClient] = None,
) -> 

```

Create a client with OAuth authentication.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `command_or_url`  |  The command to run or the URL to connect to  |  _required_  |  
|  `client_name`  |  The name of the OAuth client  |  _required_  |  
|  `redirect_uris`  |  `List[str]`  |  The redirect URIs for the OAuth flow  |  _required_  |  
|  `redirect_handler`  |  `Callable[[str], None]`  |  Function that handles the redirect URL  |  _required_  |  
|  `callback_handler`  |  `Callable[[], Tuple[str, Optional[str]]]`  |  Function that returns the auth code and state  |  _required_  |  
|  `token_storage`  |  `Optional[TokenStorage]`  |  Optional token storage for OAuth client. If not provided, a default in-memory storage is used (tokens will be lost on restart).  |  `None`  |  
|  `args`  |  `Optional[List[str]]`  |  The arguments to pass to StdioServerParameters.  |  `None`  |  
|  `env`  |  `Optional[Dict[str, str]]`  |  The environment variables to set for StdioServerParameters.  |  `None`  |  
|  `timeout`  |  The timeout for HTTP operations in seconds. Default is 30.  |  
|  `sse_read_timeout`  |  The timeout for SSE read operations in seconds. Default is 300.  |  `300`  |  
|  `tool_call_logs_callback`  |  `Optional[Callable[[List[str]], Awaitable[Any]]]`  |  Async function to store the logs deriving from an MCP tool call: logs are provided as a list of strings, representing log messages. Defaults to None.  |  `None`  |  
|  `http_client`  |  `Optional[AsyncClient]`  |  Optional httpx AsyncClient to use for Streamable transport. Will ignore timeout and headers parameters if provided.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  An authenticated MCP client  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/client.py`  
| 
```
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
```
 | 
```
@classmethod
defwith_oauth(
    cls,
    command_or_url: str,
    client_name: str,
    redirect_uris: List[str],
    redirect_handler: Callable[[str], None],
    callback_handler: Callable[[], Tuple[str, Optional[str]]],
    args: Optional[List[str]] = None,
    env: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    sse_read_timeout: int = 300,
    token_storage: Optional[TokenStorage] = None,
    tool_call_logs_callback: Optional[Callable[[List[str]], Awaitable[Any]]] = None,
    http_client: Optional[AsyncClient] = None,
) -> "BasicMCPClient":
"""
    Create a client with OAuth authentication.

    Args:
        command_or_url: The command to run or the URL to connect to
        client_name: The name of the OAuth client
        redirect_uris: The redirect URIs for the OAuth flow
        redirect_handler: Function that handles the redirect URL
        callback_handler: Function that returns the auth code and state
        token_storage: Optional token storage for OAuth client. If not provided,
                       a default in-memory storage is used (tokens will be lost on restart).
        args: The arguments to pass to StdioServerParameters.
        env: The environment variables to set for StdioServerParameters.
        timeout: The timeout for HTTP operations in seconds. Default is 30.
        sse_read_timeout: The timeout for SSE read operations in seconds. Default is 300.
        tool_call_logs_callback: Async function to store the logs deriving from an MCP tool call: logs are provided as a list of strings, representing log messages. Defaults to None.
        http_client: Optional httpx AsyncClient to use for Streamable transport. Will ignore timeout and headers parameters if provided.

    Returns:
        An authenticated MCP client

    """
    # Use default in-memory storage if none provided
    if token_storage is None:
        token_storage = DefaultInMemoryTokenStorage()
        warnings.warn(
            "Using default in-memory token storage. Tokens will be lost on restart.",
            UserWarning,
        )

    oauth_auth = OAuthClientProvider(
        server_url=command_or_url if urlparse(command_or_url).scheme else None,
        client_metadata=OAuthClientMetadata(
            client_name=client_name,
            redirect_uris=redirect_uris,
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
        ),
        redirect_handler=redirect_handler,
        callback_handler=callback_handler,
        storage=token_storage,
    )

    return cls(
        command_or_url,
        auth=oauth_auth,
        args=args,
        env=env,
        timeout=timeout,
        sse_read_timeout=sse_read_timeout,
        tool_call_logs_callback=tool_call_logs_callback,
        http_client=http_client,
    )

```
 |  
| --- | --- |  
###  call_tool [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.BasicMCPClient.call_tool "Permanent link")

```
call_tool(
    tool_name: ,
    arguments: Optional[] = None,
    progress_callback: Optional[ProgressFnT] = None,
) -> CallToolResult

```

Call a tool on the MCP server.
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/client.py`  
| 
```
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
```
 | 
```
async defcall_tool(
    self,
    tool_name: str,
    arguments: Optional[dict] = None,
    progress_callback: Optional[ProgressFnT] = None,
) -> types.CallToolResult:
"""Call a tool on the MCP server."""
    if self.tool_call_logs_callback is not None:
        # we use a string stream so that we can recover all logs at the end of the session
        handler = self._configure_tool_call_logs_callback()

        async with self._run_session() as session:
            result = await session.call_tool(
                tool_name, arguments=arguments, progress_callback=progress_callback
            )

            # get all logs by dividing the string with \n, since the format of the log has an \n at the end of the log message
            extra_values = handler.getvalue().split("\n")

            # pipe the logs list into tool_call_logs_callback
            await self.tool_call_logs_callback(extra_values)

            return result
    else:
        async with self._run_session() as session:
            return await session.call_tool(
                tool_name, arguments=arguments, progress_callback=progress_callback
            )

```
 |  
| --- | --- |  
###  list_tools [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.BasicMCPClient.list_tools "Permanent link")

```
list_tools() -> ListToolsResult

```

List all available tools on the MCP server.
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/client.py`  
| 
```
330
331
332
333
```
 | 
```
async deflist_tools(self) -> types.ListToolsResult:
"""List all available tools on the MCP server."""
    async with self._run_session() as session:
        return await session.list_tools()

```
 |  
| --- | --- |  
###  list_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.BasicMCPClient.list_resources "Permanent link")

```
list_resources() -> ListToolsResult

```

List all available resources on the MCP server.
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/client.py`  
| 
```
336
337
338
339
```
 | 
```
async deflist_resources(self) -> types.ListToolsResult:
"""List all available resources on the MCP server."""
    async with self._run_session() as session:
        return await session.list_resources()

```
 |  
| --- | --- |  
###  list_resource_templates [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.BasicMCPClient.list_resource_templates "Permanent link")

```
list_resource_templates() -> ListToolsResult

```

List all dynamic available resources on the MCP server.
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/client.py`  
| 
```
341
342
343
344
```
 | 
```
async deflist_resource_templates(self) -> types.ListToolsResult:
"""List all dynamic available resources on the MCP server."""
    async with self._run_session() as session:
        return await session.list_resource_templates()

```
 |  
| --- | --- |  
###  read_resource [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.BasicMCPClient.read_resource "Permanent link")

```
read_resource(resource_uri: AnyUrl) -> ReadResourceResult

```

Read a resource from the MCP server.
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `ReadResourceResult`  |  Tuple containing the resource content as bytes and the MIME type  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/client.py`  
| 
```
346
347
348
349
350
351
352
353
354
355
```
 | 
```
async defread_resource(self, resource_uri: AnyUrl) -> types.ReadResourceResult:
"""
    Read a resource from the MCP server.

    Returns:
        Tuple containing the resource content as bytes and the MIME type

    """
    async with self._run_session() as session:
        return await session.read_resource(resource_uri)

```
 |  
| --- | --- |  
###  list_prompts [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.BasicMCPClient.list_prompts "Permanent link")

```
list_prompts() -> [Prompt]

```

List all available prompts on the MCP server.
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/client.py`  
| 
```
359
360
361
362
```
 | 
```
async deflist_prompts(self) -> List[types.Prompt]:
"""List all available prompts on the MCP server."""
    async with self._run_session() as session:
        return await session.list_prompts()

```
 |  
| --- | --- |  
###  get_prompt [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.BasicMCPClient.get_prompt "Permanent link")

```
get_prompt(
    prompt_name: ,
    arguments: Optional[[, ]] = None,
) -> []

```

Get a prompt from the MCP server.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `prompt_name`  |  The name of the prompt to get  |  _required_  |  
|  `arguments`  |  `Optional[Dict[str, str]]`  |  Optional arguments to pass to the prompt  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `List[ChatMessage[](https://developers.llamaindex.ai/python/framework-api-reference/llms/#llama_index.core.base.llms.types.ChatMessage "ChatMessage \(llama_index.core.llms.ChatMessage\)")]`  |  The prompt as a list of llama-index ChatMessage objects  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/client.py`  
| 
```
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
```
 | 
```
async defget_prompt(
    self, prompt_name: str, arguments: Optional[Dict[str, str]] = None
) -> List[ChatMessage]:
"""
    Get a prompt from the MCP server.

    Args:
        prompt_name: The name of the prompt to get
        arguments: Optional arguments to pass to the prompt

    Returns:
        The prompt as a list of llama-index ChatMessage objects

    """
    async with self._run_session() as session:
        prompt = await session.get_prompt(prompt_name, arguments)
        llama_messages = []
        for message in prompt.messages:
            if isinstance(message.content, types.TextContent):
                llama_messages.append(
                    ChatMessage(
                        role=message.role,
                        blocks=[TextBlock(text=message.content.text)],
                    )
                )
            elif isinstance(message.content, types.ImageContent):
                llama_messages.append(
                    ChatMessage(
                        role=message.role,
                        blocks=[
                            ImageBlock(
                                image=message.content.data,
                                image_mimetype=message.content.mimeType,
                            )
                        ],
                    )
                )
            elif isinstance(message.content, types.EmbeddedResource):
                raise NotImplementedError(
                    "Embedded resources are not supported yet"
                )
            else:
                raise ValueError(
                    f"Unsupported content type: {type(message.content)}"
                )

        return llama_messages

```
 |  
| --- | --- |  
##  workflow_as_mcp [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.workflow_as_mcp "Permanent link")

```
workflow_as_mcp(
    workflow: Workflow,
    workflow_name: Optional[] = None,
    workflow_description: Optional[] = None,
    start_event_model: Optional[BaseModel] = None,
    **fastmcp_init_kwargs: 
) -> FastMCP

```

Convert a workflow to an MCP app.
This will convert any `Workflow` to an MCP app. It will expose the workflow as a tool within MCP, which will
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `workflow`  |  `Workflow`  |  The workflow to convert.  |  _required_  |  
|  `workflow_name`  |  `optional`  |  The name of the workflow. Defaults to the workflow class name.  |  `None`  |  
|  `workflow_description`  |  `optional`  |  The description of the workflow. Defaults to the workflow docstring.  |  `None`  |  
|  `start_event_model`  |  `optional`  |  The start event model of the workflow. Can be a `BaseModel` or a `StartEvent` class. Defaults to the workflow's custom `StartEvent` class.  |  `None`  |  
|  `**fastmcp_init_kwargs`  |  Additional keyword arguments to pass to the FastMCP constructor.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `FastMCP`  |  The MCP app object.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/utils.py`  
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
```
 | 
```
defworkflow_as_mcp(
    workflow: Workflow,
    workflow_name: Optional[str] = None,
    workflow_description: Optional[str] = None,
    start_event_model: Optional[BaseModel] = None,
    **fastmcp_init_kwargs: Any,
) -> FastMCP:
"""
    Convert a workflow to an MCP app.

    This will convert any `Workflow` to an MCP app. It will expose the workflow as a tool
    within MCP, which will

    Args:
        workflow:
            The workflow to convert.
        workflow_name (optional):
            The name of the workflow. Defaults to the workflow class name.
        workflow_description (optional):
            The description of the workflow. Defaults to the workflow docstring.
        start_event_model (optional):
            The start event model of the workflow. Can be a `BaseModel` or a `StartEvent` class.
            Defaults to the workflow's custom `StartEvent` class.
        **fastmcp_init_kwargs:
            Additional keyword arguments to pass to the FastMCP constructor.

    Returns:
        The MCP app object.

    """
    app = FastMCP(**fastmcp_init_kwargs)

    # Dynamically get the start event class -- this is a bit of a hack
    StartEventCLS = start_event_model or workflow._start_event_class
    if StartEventCLS == StartEvent:
        raise ValueError(
            "Must declare a custom StartEvent class in your workflow or provide a start_event_model."
        )

    # Get the workflow name and description
    workflow_name = workflow_name or workflow.__class__.__name__
    workflow_description = workflow_description or workflow.__doc__

    @app.tool(name=workflow_name, description=workflow_description)
    async def_workflow_tool(run_args: StartEventCLS, context: Context) -> Any:
        # Handle edge cases where the start event is an Event or a BaseModel
        # If the workflow does not have a custom StartEvent class, then we need to handle the event differently

        if isinstance(run_args, Event) and workflow._start_event_class != StartEvent:
            handler = workflow.run(start_event=run_args)
        elif isinstance(run_args, BaseModel):
            handler = workflow.run(**run_args.model_dump())
        elif isinstance(run_args, dict):
            start_event = StartEventCLS.model_validate(run_args)
            handler = workflow.run(start_event=start_event)
        else:
            raise ValueError(f"Invalid start event type: {type(run_args)}")

        async for event in handler.stream_events():
            if not isinstance(event, StopEvent):
                await context.log("info", message=event.model_dump_json())

        return await handler

    return app

```
 |  
| --- | --- |  
##  get_tools_from_mcp_url [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.get_tools_from_mcp_url "Permanent link")

```
get_tools_from_mcp_url(
    command_or_url: ,
    client: Optional[ClientSession] = None,
    allowed_tools: Optional[[]] = None,
    global_partial_params: Optional[[, ]] = None,
    partial_params_by_tool: Optional[
        [, [, ]]
    ] = None,
    include_resources:  = False,
) -> []

```

Get tools from an MCP server or command.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `command_or_url`  |  The command to run or the URL to connect to.  |  _required_  |  
|  `client`  |  `optional`  |  The client to use to connect to the MCP server.  |  `None`  |  
|  `allowed_tools`  |  `optional`  |  The tool names to allow from the MCP server.  |  `None`  |  
|  `global_partial_params`  |  `Optional[Dict[str, Any]]`  |  A dict of params to apply to all tools globally.  |  `None`  |  
|  `partial_params_by_tool`  |  `Optional[Dict[str, Dict[str, Any]]]`  |  A dict mapping tool names to param overrides. Values override global_partial_params. Use None as a value to remove a global param for a specific tool.  |  `None`  |  
|  `include_resources`  |  `optional`  |  Whether to include resources in the tool list.  |  `False`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/utils.py`  
| 
```
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
```
 | 
```
defget_tools_from_mcp_url(
    command_or_url: str,
    client: Optional[ClientSession] = None,
    allowed_tools: Optional[List[str]] = None,
    global_partial_params: Optional[Dict[str, Any]] = None,
    partial_params_by_tool: Optional[Dict[str, Dict[str, Any]]] = None,
    include_resources: bool = False,
) -> List[FunctionTool]:
"""
    Get tools from an MCP server or command.

    Args:
        command_or_url: The command to run or the URL to connect to.
        client (optional): The client to use to connect to the MCP server.
        allowed_tools (optional): The tool names to allow from the MCP server.
        global_partial_params: A dict of params to apply to all tools globally.
        partial_params_by_tool: A dict mapping tool names to param overrides.
                                Values override global_partial_params. Use None as a value to remove a global param for a specific tool.
        include_resources (optional): Whether to include resources in the tool list.

    """
    client = client or BasicMCPClient(command_or_url)
    tool_spec = McpToolSpec(
        client,
        allowed_tools=allowed_tools,
        global_partial_params=global_partial_params,
        partial_params_by_tool=partial_params_by_tool,
        include_resources=include_resources,
    )
    return tool_spec.to_tool_list()

```
 |  
| --- | --- |  
##  aget_tools_from_mcp_url [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/mcp/#llama_index.tools.mcp.aget_tools_from_mcp_url "Permanent link")

```
aget_tools_from_mcp_url(
    command_or_url: ,
    client: Optional[ClientSession] = None,
    allowed_tools: Optional[[]] = None,
    global_partial_params: Optional[[, ]] = None,
    partial_params_by_tool: Optional[
        [, [, ]]
    ] = None,
    include_resources:  = False,
) -> []

```

Get tools from an MCP server or command.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `command_or_url`  |  The command to run or the URL to connect to.  |  _required_  |  
|  `client`  |  `optional`  |  The client to use to connect to the MCP server.  |  `None`  |  
|  `allowed_tools`  |  `optional`  |  The tool names to allow from the MCP server.  |  `None`  |  
|  `global_partial_params`  |  `Optional[Dict[str, Any]]`  |  A dict of params to apply to all tools globally.  |  `None`  |  
|  `partial_params_by_tool`  |  `Optional[Dict[str, Dict[str, Any]]]`  |  A dict mapping tool names to param overrides. Values override global_partial_params. Use None as a value to remove a global param for a specific tool.  |  `None`  |  
|  `include_resources`  |  `optional`  |  Whether to include resources in the tool list.  |  `False`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-mcp/llama_index/tools/mcp/utils.py`  
| 
```
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
```
 | 
```
async defaget_tools_from_mcp_url(
    command_or_url: str,
    client: Optional[ClientSession] = None,
    allowed_tools: Optional[List[str]] = None,
    global_partial_params: Optional[Dict[str, Any]] = None,
    partial_params_by_tool: Optional[Dict[str, Dict[str, Any]]] = None,
    include_resources: bool = False,
) -> List[FunctionTool]:
"""
    Get tools from an MCP server or command.

    Args:
        command_or_url: The command to run or the URL to connect to.
        client (optional): The client to use to connect to the MCP server.
        allowed_tools (optional): The tool names to allow from the MCP server.
        global_partial_params: A dict of params to apply to all tools globally.
        partial_params_by_tool: A dict mapping tool names to param overrides.
                                Values override global_partial_params. Use None as a value to remove a global param for a specific tool.
        include_resources (optional): Whether to include resources in the tool list.

    """
    client = client or BasicMCPClient(command_or_url)
    tool_spec = McpToolSpec(
        client,
        allowed_tools=allowed_tools,
        global_partial_params=global_partial_params,
        partial_params_by_tool=partial_params_by_tool,
        include_resources=include_resources,
    )
    return await tool_spec.to_tool_list_async()

```
 |  
| --- | --- |  
options: members: - McpToolSpec
