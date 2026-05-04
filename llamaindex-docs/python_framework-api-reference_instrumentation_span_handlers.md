# Span handlers
Bases: `BaseModel`, `Generic[T]`
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `open_spans`  |  `Dict[str, T]`  |  Dictionary of open spans.  |  `<class 'dict'>`  |  
|  `completed_spans`  |  `List[T]`  |  List of completed spans.  |  `<dynamic>`  |  
|  `dropped_spans`  |  `List[T]`  |  List of completed spans.  |  `<dynamic>`  |  
|  `current_span_ids`  |  `Dict[Any, str | None]`  |  Id of current spans in a given thread.  |  
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/base.py`  
| 
```
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
```
 | 
```
classBaseSpanHandler(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    open_spans: Dict[str, T] = Field(
        default_factory=dict, description="Dictionary of open spans."
    )
    completed_spans: List[T] = Field(
        default_factory=list, description="List of completed spans."
    )
    dropped_spans: List[T] = Field(
        default_factory=list, description="List of completed spans."
    )
    current_span_ids: Dict[Any, Optional[str]] = Field(
        default={}, description="Id of current spans in a given thread."
    )
    _lock: Optional[threading.Lock] = PrivateAttr()

    def__init__(
        self,
        open_spans: Dict[str, T] = {},
        completed_spans: List[T] = [],
        dropped_spans: List[T] = [],
        current_span_ids: Dict[Any, str] = {},
    ):
        super().__init__(
            open_spans=open_spans,
            completed_spans=completed_spans,
            dropped_spans=dropped_spans,
            current_span_ids=current_span_ids,
        )
        self._lock = None

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "BaseSpanHandler"

    @property
    deflock(self) -> threading.Lock:
        if self._lock is None:
            self._lock = threading.Lock()
        return self._lock

    defspan_enter(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        parent_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
"""Logic for entering a span."""
        if id_ in self.open_spans:
            pass  # should probably raise an error here
        else:
            span = self.new_span(
                id_=id_,
                bound_args=bound_args,
                instance=instance,
                parent_span_id=parent_id,
                tags=tags,
            )
            if span:
                with self.lock:
                    self.open_spans[id_] = span

    defspan_exit(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        result: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
"""Logic for exiting a span."""
        span = self.prepare_to_exit_span(
            id_=id_, bound_args=bound_args, instance=instance, result=result
        )
        if span:
            with self.lock:
                del self.open_spans[id_]

    defspan_drop(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        err: Optional[BaseException] = None,
        **kwargs: Any,
    ) -> None:
"""Logic for dropping a span i.e. early exit."""
        span = self.prepare_to_drop_span(
            id_=id_, bound_args=bound_args, instance=instance, err=err
        )
        if span:
            with self.lock:
                del self.open_spans[id_]

    @abstractmethod
    defnew_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        parent_span_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[T]:
"""
        Create a span.

        Subclasses of BaseSpanHandler should create the respective span type T
        and return it. Only NullSpanHandler should return a None here.
        """
        ...

    @abstractmethod
    defprepare_to_exit_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        result: Optional[Any] = None,
        **kwargs: Any,
    ) -> Optional[T]:
"""
        Logic for preparing to exit a span.

        Subclasses of BaseSpanHandler should return back the specific span T
        that is to be exited. If None is returned, then the span won't actually
        be exited.
        """
        ...

    @abstractmethod
    defprepare_to_drop_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        err: Optional[BaseException] = None,
        **kwargs: Any,
    ) -> Optional[T]:
"""
        Logic for preparing to drop a span.

        Subclasses of BaseSpanHandler should return back the specific span T
        that is to be dropped. If None is returned, then the span won't actually
        be dropped.
        """
        ...

```
 |  
| --- | --- |  
##  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.base.BaseSpanHandler.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/base.py`  
| 
```
77
78
79
80
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "BaseSpanHandler"

```
 |  
| --- | --- |  
##  span_enter [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.base.BaseSpanHandler.span_enter "Permanent link")

```
span_enter(
    id_: ,
    bound_args: BoundArguments,
    instance: Optional[] = None,
    parent_id: Optional[] = None,
    tags: Optional[[, ]] = None,
    **kwargs: 
) -> None

```

Logic for entering a span.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/base.py`  
| 
```
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
```
 | 
```
defspan_enter(
    self,
    id_: str,
    bound_args: inspect.BoundArguments,
    instance: Optional[Any] = None,
    parent_id: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> None:
"""Logic for entering a span."""
    if id_ in self.open_spans:
        pass  # should probably raise an error here
    else:
        span = self.new_span(
            id_=id_,
            bound_args=bound_args,
            instance=instance,
            parent_span_id=parent_id,
            tags=tags,
        )
        if span:
            with self.lock:
                self.open_spans[id_] = span

```
 |  
| --- | --- |  
##  span_exit [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.base.BaseSpanHandler.span_exit "Permanent link")

```
span_exit(
    id_: ,
    bound_args: BoundArguments,
    instance: Optional[] = None,
    result: Optional[] = None,
    **kwargs: 
) -> None

```

Logic for exiting a span.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/base.py`  
| 
```
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
```
 | 
```
defspan_exit(
    self,
    id_: str,
    bound_args: inspect.BoundArguments,
    instance: Optional[Any] = None,
    result: Optional[Any] = None,
    **kwargs: Any,
) -> None:
"""Logic for exiting a span."""
    span = self.prepare_to_exit_span(
        id_=id_, bound_args=bound_args, instance=instance, result=result
    )
    if span:
        with self.lock:
            del self.open_spans[id_]

```
 |  
| --- | --- |  
##  span_drop [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.base.BaseSpanHandler.span_drop "Permanent link")

```
span_drop(
    id_: ,
    bound_args: BoundArguments,
    instance: Optional[] = None,
    err: Optional[BaseException] = None,
    **kwargs: 
) -> None

```

Logic for dropping a span i.e. early exit.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/base.py`  
| 
```
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
```
 | 
```
defspan_drop(
    self,
    id_: str,
    bound_args: inspect.BoundArguments,
    instance: Optional[Any] = None,
    err: Optional[BaseException] = None,
    **kwargs: Any,
) -> None:
"""Logic for dropping a span i.e. early exit."""
    span = self.prepare_to_drop_span(
        id_=id_, bound_args=bound_args, instance=instance, err=err
    )
    if span:
        with self.lock:
            del self.open_spans[id_]

```
 |  
| --- | --- |  
##  new_span `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.base.BaseSpanHandler.new_span "Permanent link")

```
new_span(
    id_: ,
    bound_args: BoundArguments,
    instance: Optional[] = None,
    parent_span_id: Optional[] = None,
    tags: Optional[[, ]] = None,
    **kwargs: 
) -> Optional[]

```

Create a span.
Subclasses of BaseSpanHandler should create the respective span type T and return it. Only NullSpanHandler should return a None here.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/base.py`  
| 
```
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
```
 | 
```
@abstractmethod
defnew_span(
    self,
    id_: str,
    bound_args: inspect.BoundArguments,
    instance: Optional[Any] = None,
    parent_span_id: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Optional[T]:
"""
    Create a span.

    Subclasses of BaseSpanHandler should create the respective span type T
    and return it. Only NullSpanHandler should return a None here.
    """
    ...

```
 |  
| --- | --- |  
##  prepare_to_exit_span `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.base.BaseSpanHandler.prepare_to_exit_span "Permanent link")

```
prepare_to_exit_span(
    id_: ,
    bound_args: BoundArguments,
    instance: Optional[] = None,
    result: Optional[] = None,
    **kwargs: 
) -> Optional[]

```

Logic for preparing to exit a span.
Subclasses of BaseSpanHandler should return back the specific span T that is to be exited. If None is returned, then the span won't actually be exited.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/base.py`  
| 
```
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
```
 | 
```
@abstractmethod
defprepare_to_exit_span(
    self,
    id_: str,
    bound_args: inspect.BoundArguments,
    instance: Optional[Any] = None,
    result: Optional[Any] = None,
    **kwargs: Any,
) -> Optional[T]:
"""
    Logic for preparing to exit a span.

    Subclasses of BaseSpanHandler should return back the specific span T
    that is to be exited. If None is returned, then the span won't actually
    be exited.
    """
    ...

```
 |  
| --- | --- |  
##  prepare_to_drop_span `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.base.BaseSpanHandler.prepare_to_drop_span "Permanent link")

```
prepare_to_drop_span(
    id_: ,
    bound_args: BoundArguments,
    instance: Optional[] = None,
    err: Optional[BaseException] = None,
    **kwargs: 
) -> Optional[]

```

Logic for preparing to drop a span.
Subclasses of BaseSpanHandler should return back the specific span T that is to be dropped. If None is returned, then the span won't actually be dropped.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/base.py`  
| 
```
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
```
 | 
```
@abstractmethod
defprepare_to_drop_span(
    self,
    id_: str,
    bound_args: inspect.BoundArguments,
    instance: Optional[Any] = None,
    err: Optional[BaseException] = None,
    **kwargs: Any,
) -> Optional[T]:
"""
    Logic for preparing to drop a span.

    Subclasses of BaseSpanHandler should return back the specific span T
    that is to be dropped. If None is returned, then the span won't actually
    be dropped.
    """
    ...

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
Bases: `BaseSpanHandler[SimpleSpan]`
Span Handler that manages SimpleSpan's.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/simple.py`  
| 
```
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
```
 | 
```
classSimpleSpanHandler(BaseSpanHandler[SimpleSpan]):
"""Span Handler that manages SimpleSpan's."""

    defclass_name(cls) -> str:
"""Class name."""
        return "SimpleSpanHandler"

    defnew_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        parent_span_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> SimpleSpan:
"""Create a span."""
        return SimpleSpan(id_=id_, parent_id=parent_span_id, tags=tags or {})

    defprepare_to_exit_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        result: Optional[Any] = None,
        **kwargs: Any,
    ) -> SimpleSpan:
"""Logic for preparing to drop a span."""
        span = self.open_spans[id_]
        span = cast(SimpleSpan, span)
        span.end_time = datetime.now()
        span.duration = (span.end_time - span.start_time).total_seconds()
        with self.lock:
            self.completed_spans += [span]
        return span

    defprepare_to_drop_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        err: Optional[BaseException] = None,
        **kwargs: Any,
    ) -> Optional[SimpleSpan]:
"""Logic for droppping a span."""
        if id_ in self.open_spans:
            with self.lock:
                span = self.open_spans[id_]
                span.metadata = {"error": str(err)}
                self.dropped_spans += [span]
            return span

        return None

    def_get_parents(self) -> List[SimpleSpan]:
"""Helper method to get all parent/root spans."""
        all_spans = self.completed_spans + self.dropped_spans
        return [s for s in all_spans if s.parent_id is None]

    def_build_tree_by_parent(
        self, parent: SimpleSpan, acc: List[SimpleSpan], spans: List[SimpleSpan]
    ) -> List[SimpleSpan]:
"""Builds the tree by parent root."""
        if not spans:
            return acc

        children = [s for s in spans if s.parent_id == parent.id_]
        if not children:
            return acc
        updated_spans = [s for s in spans if s not in children]

        children_trees = [
            self._build_tree_by_parent(
                parent=c, acc=[c], spans=[s for s in updated_spans if c != s]
            )
            for c in children
        ]

        return acc + reduce(lambda x, y: x + y, children_trees)

    def_get_trace_trees(self) -> List["Tree"]:
"""Method for getting trace trees."""
        try:
            fromtreelibimport Tree
        except ImportError as e:
            raise ImportError(
                "`treelib` package is missing. Please install it by using "
                "`pip install treelib`."
            )

        all_spans = self.completed_spans + self.dropped_spans
        for s in all_spans:
            if s.parent_id is None:
                continue
            if not any(ns.id_ == s.parent_id for ns in all_spans):
                warnings.warn(f"Parent with id {s.parent_id} missing from spans")
                s.parent_id += "-MISSING"
                all_spans.append(SimpleSpan(id_=s.parent_id, parent_id=None))

        parents = self._get_parents()
        span_groups = []
        for p in parents:
            this_span_group = self._build_tree_by_parent(
                parent=p, acc=[p], spans=[s for s in all_spans if s != p]
            )
            sorted_span_group = sorted(this_span_group, key=lambda x: x.start_time)
            span_groups.append(sorted_span_group)

        trees = []
        tree = Tree()
        for grp in span_groups:
            for span in grp:
                if span.parent_id is None:
                    # complete old tree unless its empty (i.e., start of loop)
                    if tree.all_nodes():
                        trees.append(tree)
                        # start new tree
                        tree = Tree()

                tree.create_node(
                    tag=f"{span.id_} ({span.duration})",
                    identifier=span.id_,
                    parent=span.parent_id,
                    data=span.start_time,
                )

        trees.append(tree)
        return trees

    defprint_trace_trees(self) -> None:
"""Method for viewing trace trees."""
        trees = self._get_trace_trees()
        for tree in trees:
            print(tree.show(stdout=False, sorting=True, key=lambda node: node.data))
            print("")

```
 |  
| --- | --- |  
##  class_name [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.simple.SimpleSpanHandler.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/simple.py`  
| 
```
18
19
20
```
 | 
```
defclass_name(cls) -> str:
"""Class name."""
    return "SimpleSpanHandler"

```
 |  
| --- | --- |  
##  new_span [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.simple.SimpleSpanHandler.new_span "Permanent link")

```
new_span(
    id_: ,
    bound_args: BoundArguments,
    instance: Optional[] = None,
    parent_span_id: Optional[] = None,
    tags: Optional[[, ]] = None,
    **kwargs: 
) -> SimpleSpan

```

Create a span.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/simple.py`  
| 
```
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
```
 | 
```
defnew_span(
    self,
    id_: str,
    bound_args: inspect.BoundArguments,
    instance: Optional[Any] = None,
    parent_span_id: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> SimpleSpan:
"""Create a span."""
    return SimpleSpan(id_=id_, parent_id=parent_span_id, tags=tags or {})

```
 |  
| --- | --- |  
##  prepare_to_exit_span [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.simple.SimpleSpanHandler.prepare_to_exit_span "Permanent link")

```
prepare_to_exit_span(
    id_: ,
    bound_args: BoundArguments,
    instance: Optional[] = None,
    result: Optional[] = None,
    **kwargs: 
) -> SimpleSpan

```

Logic for preparing to drop a span.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/simple.py`  
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
```
 | 
```
defprepare_to_exit_span(
    self,
    id_: str,
    bound_args: inspect.BoundArguments,
    instance: Optional[Any] = None,
    result: Optional[Any] = None,
    **kwargs: Any,
) -> SimpleSpan:
"""Logic for preparing to drop a span."""
    span = self.open_spans[id_]
    span = cast(SimpleSpan, span)
    span.end_time = datetime.now()
    span.duration = (span.end_time - span.start_time).total_seconds()
    with self.lock:
        self.completed_spans += [span]
    return span

```
 |  
| --- | --- |  
##  prepare_to_drop_span [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.simple.SimpleSpanHandler.prepare_to_drop_span "Permanent link")

```
prepare_to_drop_span(
    id_: ,
    bound_args: BoundArguments,
    instance: Optional[] = None,
    err: Optional[BaseException] = None,
    **kwargs: 
) -> Optional[SimpleSpan]

```

Logic for droppping a span.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/simple.py`  
| 
```
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
```
 | 
```
defprepare_to_drop_span(
    self,
    id_: str,
    bound_args: inspect.BoundArguments,
    instance: Optional[Any] = None,
    err: Optional[BaseException] = None,
    **kwargs: Any,
) -> Optional[SimpleSpan]:
"""Logic for droppping a span."""
    if id_ in self.open_spans:
        with self.lock:
            span = self.open_spans[id_]
            span.metadata = {"error": str(err)}
            self.dropped_spans += [span]
        return span

    return None

```
 |  
| --- | --- |  
##  print_trace_trees [#](https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/#llama_index_instrumentation.span_handlers.simple.SimpleSpanHandler.print_trace_trees "Permanent link")

```
print_trace_trees() -> None

```

Method for viewing trace trees.
Source code in `.venv/lib/python3.14/site-packages/llama_index_instrumentation/span_handlers/simple.py`  
| 
```
144
145
146
147
148
149
```
 | 
```
defprint_trace_trees(self) -> None:
"""Method for viewing trace trees."""
    trees = self._get_trace_trees()
    for tree in trees:
        print(tree.show(stdout=False, sorting=True, key=lambda node: node.data))
        print("")

```
 |  
| --- | --- |  
options: show_root_heading: true show_root_full_path: false
