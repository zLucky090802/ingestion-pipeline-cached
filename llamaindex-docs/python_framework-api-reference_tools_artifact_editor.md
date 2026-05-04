# Artifact editor
##  ArtifactMemoryBlock [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/artifact_editor/#llama_index.tools.artifact_editor.ArtifactMemoryBlock "Permanent link")
Bases: `BaseMemoryBlock[](https://developers.llamaindex.ai/python/framework-api-reference/memory/memory/#llama_index.core.memory.BaseMemoryBlock "BaseMemoryBlock \(llama_index.core.memory.BaseMemoryBlock\)")[str]`
Custom memory block to maintain the artifact in-memory.
Source code in `llama-index-integrations/tools/llama-index-tools-artifact-editor/llama_index/tools/artifact_editor/memory_block.py`  
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
```
 | 
```
classArtifactMemoryBlock(BaseMemoryBlock[str]):
"""Custom memory block to maintain the artifact in-memory."""

    name: str = Field(
        default="current_artifact", description="The name of the artifact block"
    )
    artifact_spec: Optional[ArtifactEditorToolSpec] = Field(
        default=None, description="The artifact spec for the artifact block"
    )

    async def_aget(
        self, messages: Optional[List[ChatMessage]] = None, **kwargs: Any
    ) -> str:
        if self.artifact_spec.get_current_artifact() is None:
            return "No artifact created yet"
        return str(self.artifact_spec.get_current_artifact())

    async def_aput(self, messages: List[ChatMessage]) -> None:
        pass

```
 |  
| --- | --- |  
##  ArtifactEditorToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/artifact_editor/#llama_index.tools.artifact_editor.ArtifactEditorToolSpec "Permanent link")
Bases: 
A tool spec that allows you to edit an artifact in-memory.
Using JSON patch operations, an LLM/Agent can be prompted to create, modify, and iterate on an artifact like a report, code, or anything that can be represented as a Pydantic model.
Attributes:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `pydantic_cls`  |  The Pydantic model class to edit  |  
| `current_artifact`  |  `Optional[T]`  |  The current artifact instance  |  
Methods:  
| Name  | Description  |  
| --- | --- |  
| `to_tool_list`  |  Returns a list of tools that can be used to edit the artifact  |  
|   |  Creates an initial artifact instance  |  
|   |  Gets the current artifact instance  |  
|   |  Applies a JSON patch to the current artifact instance  |  
Source code in `llama-index-integrations/tools/llama-index-tools-artifact-editor/llama_index/tools/artifact_editor/base.py`  
| 
```
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
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
```
 | 
```
classArtifactEditorToolSpec(BaseToolSpec):
"""
    A tool spec that allows you to edit an artifact in-memory.

    Using JSON patch operations, an LLM/Agent can be prompted to create, modify, and iterate on an artifact like a report, code, or anything that can be represented as a Pydantic model.

    Attributes:
        pydantic_cls: The Pydantic model class to edit
        current_artifact: The current artifact instance

    Methods:
        to_tool_list: Returns a list of tools that can be used to edit the artifact
        create_artifact: Creates an initial artifact instance
        get_current_artifact: Gets the current artifact instance
        apply_patch: Applies a JSON patch to the current artifact instance

    """

    # The `create_artifact` function is excluded as it is manually injected into the tool spec
    spec_functions = [
        "apply_patch",
        "get_current_artifact",
    ]

    def__init__(
        self,
        pydantic_cls: Type[T],
        current_artifact: Optional[T] = None,
    ) -> None:
"""
        Initialize the artifact editor tool spec.

        Args:
            pydantic_cls (BaseModel): The Pydantic model class to edit
            current_artifact (Optional[BaseModel]): The initial artifact instance to use

        """
        self.pydantic_cls = pydantic_cls
        self.current_artifact: Optional[T] = current_artifact

    defto_tool_list(self) -> List[BaseTool]:
        tools = super().to_tool_list()
        tools.append(
            FunctionTool.from_defaults(
                self.create_artifact,
                description=self.pydantic_cls.__doc__
                or "Create an initial artifact instance.",
                fn_schema=self.pydantic_cls,
            )
        )
        return tools

    defcreate_artifact(self, **kwargs: Any) -> dict:
"""Create an initial artifact instance."""
        self.current_artifact = self.pydantic_cls.model_validate(kwargs)
        return self.current_artifact.model_dump()

    defget_current_artifact(self) -> Optional[dict]:
"""Get the current artifact instance."""
        return self.current_artifact.model_dump() if self.current_artifact else None

    defapply_patch(self, patch: JsonPatch) -> dict:
"""
        Apply a JSON patch to the current Pydantic model instance.

        Args:
            patch: JsonPatch containing operations to apply

        Returns:
            New instance of the same model type with patches applied.
            Also overwrites and saves the new instance as the current artifact.

        Raises:
            ValueError: If patch operation is invalid
            IndexError: If array index is out of range
            ValidationError: If patch results in invalid model

        """
        # Validate patch object
        if isinstance(patch, dict):
            patch = JsonPatch.model_validate(patch)
        elif isinstance(patch, str):
            patch = JsonPatch.model_validate_json(patch)

        # Convert to dict for easier manipulation
        model_dict = self.current_artifact.model_dump()
        model_class = self.pydantic_cls

        for operation in patch.operations:
            try:
                self._apply_single_operation(model_dict, operation)
            except Exception as e:
                raise ValueError(
                    f"Failed to apply operation {operation.op} at {operation.path}: {e!s}"
                )

        # Convert back to original model type and validate
        try:
            self.current_artifact = model_class.model_validate(model_dict)
            return self.current_artifact.model_dump()
        except ValidationError as e:
            raise ValueError(
                f"Patch resulted in invalid {model_class.__name__} structure: {e!s}"
            )

    def_apply_single_operation(
        self, data: Dict[str, Any], operation: PatchOperation
    ) -> None:
"""Apply a single patch operation to the data dictionary."""
        path_parts = self._parse_path(operation.path)

        # Validate path before applying operation
        if operation.op in ["add", "replace"]:
            self._validate_path_against_schema(path_parts, self.pydantic_cls)

        if operation.op == "replace":
            self._set_value_at_path(data, path_parts, operation.value)

        elif operation.op == "add":
            self._add_value_at_path(data, path_parts, operation.value)

        elif operation.op == "remove":
            self._remove_value_at_path(data, path_parts)

        elif operation.op == "move":
            if not operation.from_path:
                raise ValueError("'move' operation requires 'from_path'")
            from_parts = self._parse_path(operation.from_path)
            to_parts = path_parts
            # Validate both paths
            self._validate_path_against_schema(to_parts, self.pydantic_cls)
            value = self._get_value_at_path(data, from_parts)
            self._remove_value_at_path(data, from_parts)
            self._set_value_at_path(data, to_parts, value)

        elif operation.op == "copy":
            if not operation.from_path:
                raise ValueError("'copy' operation requires 'from_path'")
            from_parts = self._parse_path(operation.from_path)
            to_parts = path_parts
            # Validate target path
            self._validate_path_against_schema(to_parts, self.pydantic_cls)
            value = self._get_value_at_path(data, from_parts)
            self._set_value_at_path(data, to_parts, value)

        else:
            raise ValueError(f"Unknown operation: {operation.op}")

    def_validate_path_against_schema(
        self, path_parts: List[Union[str, int]], model_class: Type[BaseModel]
    ) -> None:
"""
        Validate that a path corresponds to valid fields in the Pydantic model schema.

        Args:
            path_parts: Parsed path components
            model_class: The Pydantic model class to validate against

        Raises:
            ValueError: If the path contains invalid fields

        """
        if not path_parts:
            return

        current_model = model_class
        current_path = ""

        for i, part in enumerate(path_parts):
            current_path += f"/{part}" if current_path else f"{part}"

            # If part is an integer or '-' (array append), we're dealing with an array index
            if isinstance(part, int) or part == "-":
                continue

            # Check if this field exists in the current model
            if hasattr(current_model, "model_fields"):
                fields = current_model.model_fields
            else:
                # Fallback for older Pydantic versions
                fields = getattr(current_model, "__fields__", {})

            if part not in fields:
                raise ValueError(
                    f"Invalid field '{part}' at path '/{current_path}'. Valid fields are: {list(fields.keys())}"
                )

            # Get the field type for nested validation
            field_info = fields[part]

            # Handle nested models
            if hasattr(field_info, "annotation"):
                field_type = field_info.annotation
            else:
                # Fallback for older Pydantic versions
                field_type = getattr(field_info, "type_", None)

            if field_type:
                # Handle Optional types
                if hasattr(field_type, "__origin__") and field_type.__origin__ is Union:
                    # Extract non-None type from Optional
                    args = getattr(field_type, "__args__", ())
                    field_type = next(
                        (arg for arg in args if arg is not type(None)), field_type
                    )

                # Handle List types
                if hasattr(field_type, "__origin__") and field_type.__origin__ in (
                    list,
                    List,
                ):
                    # For list types, the next part should be an index or '-'
                    if i + 1  len(path_parts) and (
                        isinstance(path_parts[i + 1], int) or path_parts[i + 1] == "-"
                    ):
                        continue
                    # If we're at the end of the path and it's a list, that's valid too
                    elif i + 1 == len(path_parts):
                        continue

                # If it's a BaseModel subclass, use it for next iteration
                if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                    current_model = field_type
                else:
                    # If we have more path parts but current field is not a model or list, check validity
                    if (
                        i + 1  len(path_parts)
                        and not isinstance(path_parts[i + 1], int)
                        and path_parts[i + 1] != "-"
                    ):
                        raise ValueError(
                            f"Cannot access nested field '{path_parts[i+1]}' on non-object field '{part}' of type {field_type}"
                        )

    def_parse_path(self, path: str) -> List[Union[str, int]]:
"""Parse a JSON pointer path into components."""
        if not path.startswith("/"):
            raise ValueError("Path must start with '/'")

        if path == "/":
            return []

        parts = []
        for part in path[1:].split("/"):
            # Unescape JSON pointer characters
            part = part.replace("~1", "/").replace("~0", "~")

            # Try to convert to int if it looks like an array index
            if part.isdigit():
                parts.append(int(part))
            else:
                parts.append(part)

        return parts

    def_get_value_at_path(
        self, data: Dict[str, Any], path_parts: List[Union[str, int]]
    ) -> Any:
"""Get value at the specified path."""
        current = data

        for part in path_parts:
            if isinstance(current, dict):
                if part not in current:
                    raise KeyError(f"Key '{part}' not found")
                current = current[part]
            elif isinstance(current, list):
                if not isinstance(part, int):
                    raise ValueError(f"Array index must be integer, got {part}")
                if part >= len(current) or part  -len(current):
                    raise IndexError(f"Array index {part} out of range")
                current = current[part]
            else:
                raise ValueError(
                    f"Cannot index into {type(current).__name__} with {part}"
                )

        return current

    def_set_value_at_path(
        self, data: Dict[str, Any], path_parts: List[Union[str, int]], value: Any
    ) -> None:
"""Set value at the specified path."""
        if not path_parts:
            raise ValueError("Cannot replace root")

        current = data
        for part in path_parts[:-1]:
            if isinstance(current, dict):
                if part not in current:
                    raise KeyError(f"Key '{part}' not found")
                current = current[part]
            elif isinstance(current, list):
                if not isinstance(part, int):
                    raise ValueError(f"Array index must be integer, got {part}")
                if part >= len(current) or part  -len(current):
                    raise IndexError(f"Array index {part} out of range")
                current = current[part]
            else:
                raise ValueError(
                    f"Cannot index into {type(current).__name__} with {part}"
                )

        last_part = path_parts[-1]
        if isinstance(current, dict):
            current[last_part] = value
        elif isinstance(current, list):
            if not isinstance(last_part, int):
                raise ValueError(f"Array index must be integer, got {last_part}")
            if last_part >= len(current) or last_part  -len(current):
                raise IndexError(f"Array index {last_part} out of range")
            current[last_part] = value
        else:
            raise ValueError(f"Cannot set value in {type(current).__name__}")

    def_add_value_at_path(
        self, data: Dict[str, Any], path_parts: List[Union[str, int]], value: Any
    ) -> None:
"""Add value at the specified path."""
        if not path_parts:
            raise ValueError("Cannot add to root")

        current = data
        for part in path_parts[:-1]:
            if isinstance(current, dict):
                if part not in current:
                    raise KeyError(f"Key '{part}' not found")
                current = current[part]
            elif isinstance(current, list):
                if not isinstance(part, int):
                    raise ValueError(f"Array index must be integer, got {part}")
                if part >= len(current) or part  -len(current):
                    raise IndexError(f"Array index {part} out of range")
                current = current[part]
            else:
                raise ValueError(
                    f"Cannot index into {type(current).__name__} with {part}"
                )

        last_part = path_parts[-1]
        if isinstance(current, dict):
            current[last_part] = value
        elif isinstance(current, list):
            if isinstance(last_part, int):
                if last_part  len(current) or last_part  -len(current) - 1:
                    raise IndexError(
                        f"Array index {last_part} out of range for insertion"
                    )
                current.insert(last_part, value)
            elif last_part == "-":  # Special case for appending to array
                current.append(value)
            else:
                raise ValueError(f"Invalid array index for add operation: {last_part}")
        else:
            raise ValueError(f"Cannot add value to {type(current).__name__}")

    def_remove_value_at_path(
        self, data: Dict[str, Any], path_parts: List[Union[str, int]]
    ) -> None:
"""Remove value at the specified path."""
        if not path_parts:
            raise ValueError("Cannot remove root")

        current = data
        for part in path_parts[:-1]:
            if isinstance(current, dict):
                if part not in current:
                    raise KeyError(f"Key '{part}' not found")
                current = current[part]
            elif isinstance(current, list):
                if not isinstance(part, int):
                    raise ValueError(f"Array index must be integer, got {part}")
                if part >= len(current) or part  -len(current):
                    raise IndexError(f"Array index {part} out of range")
                current = current[part]
            else:
                raise ValueError(
                    f"Cannot index into {type(current).__name__} with {part}"
                )

        last_part = path_parts[-1]
        if isinstance(current, dict):
            if last_part not in current:
                raise KeyError(f"Key '{last_part}' not found")
            del current[last_part]
        elif isinstance(current, list):
            if not isinstance(last_part, int):
                raise ValueError(f"Array index must be integer, got {last_part}")
            if last_part >= len(current) or last_part  -len(current):
                raise IndexError(f"Array index {last_part} out of range")
            del current[last_part]
        else:
            raise ValueError(f"Cannot remove value from {type(current).__name__}")

```
 |  
| --- | --- |  
###  create_artifact [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/artifact_editor/#llama_index.tools.artifact_editor.ArtifactEditorToolSpec.create_artifact "Permanent link")

```
create_artifact(**kwargs: ) -> 

```

Create an initial artifact instance.
Source code in `llama-index-integrations/tools/llama-index-tools-artifact-editor/llama_index/tools/artifact_editor/base.py`  
| 
```
86
87
88
89
```
 | 
```
defcreate_artifact(self, **kwargs: Any) -> dict:
"""Create an initial artifact instance."""
    self.current_artifact = self.pydantic_cls.model_validate(kwargs)
    return self.current_artifact.model_dump()

```
 |  
| --- | --- |  
###  get_current_artifact [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/artifact_editor/#llama_index.tools.artifact_editor.ArtifactEditorToolSpec.get_current_artifact "Permanent link")

```
get_current_artifact() -> Optional[]

```

Get the current artifact instance.
Source code in `llama-index-integrations/tools/llama-index-tools-artifact-editor/llama_index/tools/artifact_editor/base.py`  
| 
```
91
92
93
```
 | 
```
defget_current_artifact(self) -> Optional[dict]:
"""Get the current artifact instance."""
    return self.current_artifact.model_dump() if self.current_artifact else None

```
 |  
| --- | --- |  
###  apply_patch [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/artifact_editor/#llama_index.tools.artifact_editor.ArtifactEditorToolSpec.apply_patch "Permanent link")

```
apply_patch(patch: JsonPatch) -> 

```

Apply a JSON patch to the current Pydantic model instance.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `patch`  |  `JsonPatch`  |  JsonPatch containing operations to apply  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `dict`  |  New instance of the same model type with patches applied.  |  
|  `dict`  |  Also overwrites and saves the new instance as the current artifact.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If patch operation is invalid  |  
|  `IndexError`  |  If array index is out of range  |  
|  `ValidationError`  |  If patch results in invalid model  |  
Source code in `llama-index-integrations/tools/llama-index-tools-artifact-editor/llama_index/tools/artifact_editor/base.py`  
| 
```
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
```
 | 
```
defapply_patch(self, patch: JsonPatch) -> dict:
"""
    Apply a JSON patch to the current Pydantic model instance.

    Args:
        patch: JsonPatch containing operations to apply

    Returns:
        New instance of the same model type with patches applied.
        Also overwrites and saves the new instance as the current artifact.

    Raises:
        ValueError: If patch operation is invalid
        IndexError: If array index is out of range
        ValidationError: If patch results in invalid model

    """
    # Validate patch object
    if isinstance(patch, dict):
        patch = JsonPatch.model_validate(patch)
    elif isinstance(patch, str):
        patch = JsonPatch.model_validate_json(patch)

    # Convert to dict for easier manipulation
    model_dict = self.current_artifact.model_dump()
    model_class = self.pydantic_cls

    for operation in patch.operations:
        try:
            self._apply_single_operation(model_dict, operation)
        except Exception as e:
            raise ValueError(
                f"Failed to apply operation {operation.op} at {operation.path}: {e!s}"
            )

    # Convert back to original model type and validate
    try:
        self.current_artifact = model_class.model_validate(model_dict)
        return self.current_artifact.model_dump()
    except ValidationError as e:
        raise ValueError(
            f"Patch resulted in invalid {model_class.__name__} structure: {e!s}"
        )

```
 |  
| --- | --- |  
options: members: - ArtifactEditorToolSpec
