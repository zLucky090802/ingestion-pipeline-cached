# Adapter
##  AdapterEmbeddingModel [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/adapter/#llama_index.embeddings.adapter.AdapterEmbeddingModel "Permanent link")
Bases: 
Adapter for any embedding model.
This is a wrapper around any embedding model that adds an adapter layer on top of it. This is useful for finetuning an embedding model on a downstream task. The embedding model can be any model - it does not need to expose gradients.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `base_embed_model`  |   |  Base embedding model.  |  _required_  |  
|  `adapter_path`  |  Path to adapter.  |  _required_  |  
|  `adapter_cls`  |  `Optional[Type[Any]]`  |  Adapter class. Defaults to None, in which case a linear adapter is used.  |  `None`  |  
|  `transform_query`  |  `bool`  |  Whether to transform query embeddings. Defaults to True.  |  `True`  |  
|  `device`  |  `Optional[str]`  |  Device to use. Defaults to None.  |  `None`  |  
|  `embed_batch_size`  |  Batch size for embedding. Defaults to 10.  |  `DEFAULT_EMBED_BATCH_SIZE`  |  
|  `callback_manager`  |  `Optional[CallbackManager[](https://developers.llamaindex.ai/python/framework-api-reference/callbacks/#llama_index.core.callbacks.base.CallbackManager "CallbackManager \(llama_index.core.callbacks.CallbackManager\)")]`  |  Callback manager. Defaults to None.  |  `None`  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-adapter/llama_index/embeddings/adapter/base.py`  
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
```
 | 
```
classAdapterEmbeddingModel(BaseEmbedding):
"""
    Adapter for any embedding model.

    This is a wrapper around any embedding model that adds an adapter layer \
        on top of it.
    This is useful for finetuning an embedding model on a downstream task.
    The embedding model can be any model - it does not need to expose gradients.

    Args:
        base_embed_model (BaseEmbedding): Base embedding model.
        adapter_path (str): Path to adapter.
        adapter_cls (Optional[Type[Any]]): Adapter class. Defaults to None, in which \
            case a linear adapter is used.
        transform_query (bool): Whether to transform query embeddings. Defaults to True.
        device (Optional[str]): Device to use. Defaults to None.
        embed_batch_size (int): Batch size for embedding. Defaults to 10.
        callback_manager (Optional[CallbackManager]): Callback manager. \
            Defaults to None.

    """

    _base_embed_model: BaseEmbedding = PrivateAttr()
    _adapter: Any = PrivateAttr()
    _transform_query: bool = PrivateAttr()
    _device: Optional[str] = PrivateAttr()
    _target_device: Any = PrivateAttr()

    def__init__(
        self,
        base_embed_model: BaseEmbedding,
        adapter_path: str,
        adapter_cls: Optional[Type[Any]] = None,
        transform_query: bool = True,
        device: Optional[str] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
"""Init params."""
        importtorch
        fromllama_index.embeddings.adapter.utilsimport BaseAdapter, LinearLayer

        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            model_name=f"Adapter for {base_embed_model.model_name}",
        )

        if device is None:
            device = infer_torch_device()
            logger.info(f"Use pytorch device: {device}")
        self._target_device = torch.device(device)

        self._base_embed_model = base_embed_model

        if adapter_cls is None:
            adapter_cls = LinearLayer
        else:
            adapter_cls = cast(Type[BaseAdapter], adapter_cls)

        adapter = adapter_cls.load(adapter_path)
        self._adapter = cast(BaseAdapter, adapter)
        self._adapter.to(self._target_device)

        self._transform_query = transform_query

    @classmethod
    defclass_name(cls) -> str:
        return "AdapterEmbeddingModel"

    def_get_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        importtorch

        query_embedding = self._base_embed_model._get_query_embedding(query)
        if self._transform_query:
            query_embedding_t = torch.tensor(query_embedding).to(self._target_device)
            query_embedding_t = self._adapter.forward(query_embedding_t)
            query_embedding = query_embedding_t.tolist()

        return query_embedding

    async def_aget_query_embedding(self, query: str) -> List[float]:
"""Get query embedding."""
        importtorch

        query_embedding = await self._base_embed_model._aget_query_embedding(query)
        if self._transform_query:
            query_embedding_t = torch.tensor(query_embedding).to(self._target_device)
            query_embedding_t = self._adapter.forward(query_embedding_t)
            query_embedding = query_embedding_t.tolist()

        return query_embedding

    def_get_text_embedding(self, text: str) -> List[float]:
        return self._base_embed_model._get_text_embedding(text)

    async def_aget_text_embedding(self, text: str) -> List[float]:
        return await self._base_embed_model._aget_text_embedding(text)

```
 |  
| --- | --- |  
##  BaseAdapter [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/adapter/#llama_index.embeddings.adapter.BaseAdapter "Permanent link")
Bases: `Module`
Base adapter.
Can be subclassed to implement custom adapters. To implement a custom adapter, subclass this class and implement the following methods: - get_config_dict - forward
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-adapter/llama_index/embeddings/adapter/utils.py`  
| 
```
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
classBaseAdapter(nn.Module):
"""
    Base adapter.

    Can be subclassed to implement custom adapters.
    To implement a custom adapter, subclass this class and implement the
    following methods:
        - get_config_dict
        - forward

    """

    @abstractmethod
    defget_config_dict(self) -> Dict:
"""Get config dict."""

    @abstractmethod
    defforward(self, embed: Tensor) -> Tensor:
"""Forward pass."""

    defsave(self, output_path: str) -> None:
"""Save model."""
        os.makedirs(output_path, exist_ok=True)
        with open(os.path.join(output_path, "config.json"), "w") as fOut:
            json.dump(self.get_config_dict(), fOut)
        torch.save(self.state_dict(), os.path.join(output_path, "pytorch_model.bin"))

    @classmethod
    defload(cls, input_path: str) -> "BaseAdapter":
"""Load model."""
        with open(os.path.join(input_path, "config.json")) as fIn:
            config = json.load(fIn)
        model = cls(**config)
        model.load_state_dict(
            torch.load(
                os.path.join(input_path, "pytorch_model.bin"),
                map_location=torch.device("cpu"),
            )
        )
        return model

```
 |  
| --- | --- |  
###  get_config_dict `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/adapter/#llama_index.embeddings.adapter.BaseAdapter.get_config_dict "Permanent link")

```
get_config_dict() -> 

```

Get config dict.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-adapter/llama_index/embeddings/adapter/utils.py`  
| 
```
28
29
30
```
 | 
```
@abstractmethod
defget_config_dict(self) -> Dict:
"""Get config dict."""

```
 |  
| --- | --- |  
###  forward `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/adapter/#llama_index.embeddings.adapter.BaseAdapter.forward "Permanent link")

```
forward(embed: Tensor) -> Tensor

```

Forward pass.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-adapter/llama_index/embeddings/adapter/utils.py`  
| 
```
32
33
34
```
 | 
```
@abstractmethod
defforward(self, embed: Tensor) -> Tensor:
"""Forward pass."""

```
 |  
| --- | --- |  
###  save [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/adapter/#llama_index.embeddings.adapter.BaseAdapter.save "Permanent link")

```
save(output_path: ) -> None

```

Save model.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-adapter/llama_index/embeddings/adapter/utils.py`  
| 
```
36
37
38
39
40
41
```
 | 
```
defsave(self, output_path: str) -> None:
"""Save model."""
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, "config.json"), "w") as fOut:
        json.dump(self.get_config_dict(), fOut)
    torch.save(self.state_dict(), os.path.join(output_path, "pytorch_model.bin"))

```
 |  
| --- | --- |  
###  load `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/adapter/#llama_index.embeddings.adapter.BaseAdapter.load "Permanent link")

```
load(input_path: ) -> 

```

Load model.
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-adapter/llama_index/embeddings/adapter/utils.py`  
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
```
 | 
```
@classmethod
defload(cls, input_path: str) -> "BaseAdapter":
"""Load model."""
    with open(os.path.join(input_path, "config.json")) as fIn:
        config = json.load(fIn)
    model = cls(**config)
    model.load_state_dict(
        torch.load(
            os.path.join(input_path, "pytorch_model.bin"),
            map_location=torch.device("cpu"),
        )
    )
    return model

```
 |  
| --- | --- |  
##  LinearLayer [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/adapter/#llama_index.embeddings.adapter.LinearLayer "Permanent link")
Bases: 
Linear transformation.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `in_features`  |  Input dimension.  |  _required_  |  
|  `out_features`  |  Output dimension.  |  _required_  |  
|  `bias`  |  `bool`  |  Whether to use bias. Defaults to False.  |  `False`  |  
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-adapter/llama_index/embeddings/adapter/utils.py`  
| 
```
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
```
 | 
```
classLinearLayer(BaseAdapter):
"""
    Linear transformation.

    Args:
        in_features (int): Input dimension.
        out_features (int): Output dimension.
        bias (bool): Whether to use bias. Defaults to False.

    """

    def__init__(self, in_features: int, out_features: int, bias: bool = False) -> None:
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.bias = bias
        self.linear = nn.Linear(in_features, out_features, bias=bias)
        # seed with identity matrix and 0 bias
        # only works for square matrices
        self.linear.weight.data.copy_(torch.eye(in_features, out_features))
        if bias:
            self.linear.bias.data.copy_(torch.zeros(out_features))

    defforward(self, embed: Tensor) -> Tensor:
"""Forward pass (Wv)."""
        return self.linear(embed)

    defget_config_dict(self) -> Dict:
        return {
            "in_features": self.in_features,
            "out_features": self.out_features,
            "bias": self.bias,
        }

```
 |  
| --- | --- |  
###  forward [#](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/adapter/#llama_index.embeddings.adapter.LinearLayer.forward "Permanent link")

```
forward(embed: Tensor) -> Tensor

```

Forward pass (Wv).
Source code in `llama-index-integrations/embeddings/llama-index-embeddings-adapter/llama_index/embeddings/adapter/utils.py`  
| 
```
81
82
83
```
 | 
```
defforward(self, embed: Tensor) -> Tensor:
"""Forward pass (Wv)."""
    return self.linear(embed)

```
 |  
| --- | --- |  
options: members: - AdapterEmbeddingModel - LinearAdapterEmbeddingModel
