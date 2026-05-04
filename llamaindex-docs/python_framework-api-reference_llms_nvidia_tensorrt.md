# Nvidia tensorrt
##  LocalTensorRTLLM [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/nvidia_tensorrt/#llama_index.llms.nvidia_tensorrt.LocalTensorRTLLM "Permanent link")
Bases: `CustomLLM`
Local TensorRT LLM.
[TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) provides users with an easy-to-use Python API to define Large Language Models (LLMs) and build TensorRT engines that contain state-of-the-art optimizations to perform inference efficiently on NVIDIA GPUs.
Since TensorRT-LLM is a SDK for interacting with local models in process there are a few environment steps that must be followed to ensure that the TensorRT-LLM setup can be used.
  1. Nvidia Cuda 12.2 or higher is currently required to run TensorRT-LLM
  2. Install `tensorrt_llm` via pip with `pip3 install tensorrt_llm -U --extra-index-url https://pypi.nvidia.com`
  3. For this example we will use Llama2. The Llama2 model files need to be created via scripts following the instructions (https://github.com/NVIDIA/trt-llm-rag-windows/blob/release/1.0/README.md#building-trt-engine)
     * The following files will be created from following the stop above
     * `Llama_float16_tp1_rank0.engine`: The main output of the build script, containing the executable graph of operations with the model weights embedded.
     * `config.json`: Includes detailed information about the model, like its general structure and precision, as well as information about which plug-ins were incorporated into the engine.
     * `model.cache`: Caches some of the timing and optimization information from model compilation, making successive builds quicker.
  4. `mkdir model`
  5. Move all of the files mentioned above to the model directory.


Examples:
`pip install llama-index-llms-nvidia-tensorrt`

```
fromllama_index.llms.nvidia_tensorrtimport LocalTensorRTLLM


defcompletion_to_prompt(completion):
    return f"<s> [INST] {completion} [/INST] "

defmessages_to_prompt(messages):
    content = ""
    for message in messages:
        content += str(message) + "\n"
    return f"<s> [INST] {content} [/INST] "

llm = LocalTensorRTLLM(
    model_path="./model",
    engine_name="llama_float16_tp1_rank0.engine",
    tokenizer_dir="meta-llama/Llama-2-13b-chat",
    completion_to_prompt=completion_to_prompt,
    messages_to_prompt=messages_to_prompt,
)

resp = llm.complete("Who is Paul Graham?")
print(str(resp))

```

Source code in `llama-index-integrations/llms/llama-index-llms-nvidia-tensorrt/llama_index/llms/nvidia_tensorrt/base.py`  
| 
```
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
```
 | 
```
classLocalTensorRTLLM(CustomLLM):
r"""
    Local TensorRT LLM.

    [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) provides users with an easy-to-use Python API to define Large Language Models (LLMs) and build TensorRT engines that contain state-of-the-art optimizations to perform inference
    efficiently on NVIDIA GPUs.

    Since TensorRT-LLM is a SDK for interacting with local models in process there are a few environment steps that must be followed to ensure that the TensorRT-LLM setup can be used.

    1. Nvidia Cuda 12.2 or higher is currently required to run TensorRT-LLM
    2. Install `tensorrt_llm` via pip with `pip3 install tensorrt_llm -U --extra-index-url https://pypi.nvidia.com`
    3. For this example we will use Llama2. The Llama2 model files need to be created via scripts following the instructions
    (https://github.com/NVIDIA/trt-llm-rag-windows/blob/release/1.0/README.md#building-trt-engine)
        * The following files will be created from following the stop above
        * `Llama_float16_tp1_rank0.engine`: The main output of the build script, containing the executable graph of operations with the model weights embedded.
        * `config.json`: Includes detailed information about the model, like its general structure and precision, as well as information about which plug-ins were incorporated into the engine.
        * `model.cache`: Caches some of the timing and optimization information from model compilation, making successive builds quicker.
    4. `mkdir model`
    5. Move all of the files mentioned above to the model directory.

    Examples:
        `pip install llama-index-llms-nvidia-tensorrt`

        ```python
        from llama_index.llms.nvidia_tensorrt import LocalTensorRTLLM


        def completion_to_prompt(completion):
            return f"<s> [INST] {completion} [/INST] "

        def messages_to_prompt(messages):
            content = ""
            for message in messages:
                content += str(message) + "\n"
            return f"<s> [INST] {content} [/INST] "

        llm = LocalTensorRTLLM(
            model_path="./model",
            engine_name="llama_float16_tp1_rank0.engine",
            tokenizer_dir="meta-llama/Llama-2-13b-chat",
            completion_to_prompt=completion_to_prompt,
            messages_to_prompt=messages_to_prompt,


        resp = llm.complete("Who is Paul Graham?")
        print(str(resp))
        ```

    """

    model_path: Optional[str] = Field(description="The path to the trt engine.")
    temperature: float = Field(description="The temperature to use for sampling.")
    max_new_tokens: int = Field(description="The maximum number of tokens to generate.")
    context_window: int = Field(
        description="The maximum number of context tokens for the model."
    )
    messages_to_prompt: Callable = Field(
        description="The function to convert messages to a prompt.", exclude=True
    )
    completion_to_prompt: Callable = Field(
        description="The function to convert a completion to a prompt.", exclude=True
    )
    generate_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Kwargs used for generation."
    )
    model_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Kwargs used for model initialization."
    )
    verbose: bool = Field(description="Whether to print verbose output.")

    _model: Any = PrivateAttr()
    _model_config: Any = PrivateAttr()
    _tokenizer: Any = PrivateAttr()
    _max_new_tokens = PrivateAttr()
    _sampling_config = PrivateAttr()
    _verbose = PrivateAttr()

    def__init__(
        self,
        model_path: Optional[str] = None,
        engine_name: Optional[str] = None,
        tokenizer_dir: Optional[str] = None,
        temperature: float = 0.1,
        max_new_tokens: int = DEFAULT_NUM_OUTPUTS,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        messages_to_prompt: Optional[Callable] = None,
        completion_to_prompt: Optional[Callable] = None,
        callback_manager: Optional[CallbackManager] = None,
        generate_kwargs: Optional[Dict[str, Any]] = None,
        model_kwargs: Optional[Dict[str, Any]] = None,
        verbose: bool = False,
    ) -> None:
        try:
            importtensorrt_llm
            fromtensorrt_llm.runtimeimport ModelConfig, SamplingConfig
        except ImportError:
            print(
                "Unable to import `tensorrt_llm` module. Please ensure you have\
                  `tensorrt_llm` installed in your environment. You can run\
                  `pip3 install tensorrt_llm -U --extra-index-url https://pypi.nvidia.com` to install."
            )

        model_kwargs = model_kwargs or {}
        model_kwargs.update({"n_ctx": context_window, "verbose": verbose})
        max_new_tokens = max_new_tokens
        verbose = verbose
        # check if model is cached
        if model_path is not None:
            if not os.path.exists(model_path):
                raise ValueError(
                    "Provided model path does not exist. "
                    "Please check the path or provide a model_url to download."
                )
            else:
                engine_dir = model_path
                engine_dir_path = Path(engine_dir)
                config_path = engine_dir_path / "config.json"

                # config function
                with open(config_path) as f:
                    config = json.load(f)
                use_gpt_attention_plugin = config["plugin_config"][
                    "gpt_attention_plugin"
                ]
                remove_input_padding = config["plugin_config"]["remove_input_padding"]
                tp_size = config["builder_config"]["tensor_parallel"]
                pp_size = 1
                if "pipeline_parallel" in config["builder_config"]:
                    pp_size = config["builder_config"]["pipeline_parallel"]
                world_size = tp_size * pp_size
                assert world_size == tensorrt_llm.mpi_world_size(), (
                    f"Engine world size ({world_size}) != Runtime world size ({tensorrt_llm.mpi_world_size()})"
                )
                num_heads = config["builder_config"]["num_heads"] // tp_size
                hidden_size = config["builder_config"]["hidden_size"] // tp_size
                vocab_size = config["builder_config"]["vocab_size"]
                num_layers = config["builder_config"]["num_layers"]
                num_kv_heads = config["builder_config"].get("num_kv_heads", num_heads)
                paged_kv_cache = config["plugin_config"]["paged_kv_cache"]
                if config["builder_config"].get("multi_query_mode", False):
                    tensorrt_llm.logger.warning(
                        "`multi_query_mode` config is deprecated. Please rebuild the engine."
                    )
                    num_kv_heads = 1
                num_kv_heads = (num_kv_heads + tp_size - 1) // tp_size

                model_config = ModelConfig(
                    num_heads=num_heads,
                    num_kv_heads=num_kv_heads,
                    hidden_size=hidden_size,
                    vocab_size=vocab_size,
                    num_layers=num_layers,
                    gpt_attention_plugin=use_gpt_attention_plugin,
                    paged_kv_cache=paged_kv_cache,
                    remove_input_padding=remove_input_padding,
                    max_batch_size=config["builder_config"]["max_batch_size"],
                )

                assert pp_size == 1, (
                    "Python runtime does not support pipeline parallelism"
                )
                world_size = tp_size * pp_size

                runtime_rank = tensorrt_llm.mpi_rank()
                runtime_mapping = tensorrt_llm.Mapping(
                    world_size, runtime_rank, tp_size=tp_size, pp_size=pp_size
                )

                # TensorRT-LLM must run on a GPU.
                assert torch.cuda.is_available(), (
                    "LocalTensorRTLLM requires a Nvidia CUDA enabled GPU to operate"
                )
                torch.cuda.set_device(runtime_rank % runtime_mapping.gpus_per_node)
                tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir, legacy=False)
                sampling_config = SamplingConfig(
                    end_id=EOS_TOKEN,
                    pad_id=PAD_TOKEN,
                    num_beams=1,
                    temperature=temperature,
                )

                serialize_path = engine_dir_path / (engine_name if engine_name else "")
                with open(serialize_path, "rb") as f:
                    engine_buffer = f.read()
                decoder = tensorrt_llm.runtime.GenerationSession(
                    model_config, engine_buffer, runtime_mapping, debug_mode=False
                )
                model = decoder

        generate_kwargs = generate_kwargs or {}
        generate_kwargs.update(
            {"temperature": temperature, "max_tokens": max_new_tokens}
        )

        super().__init__(
            model_path=model_path,
            temperature=temperature,
            context_window=context_window,
            max_new_tokens=max_new_tokens,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            callback_manager=callback_manager,
            generate_kwargs=generate_kwargs,
            model_kwargs=model_kwargs,
            verbose=verbose,
        )
        self._model = model
        self._model_config = model_config
        self._tokenizer = tokenizer
        self._sampling_config = sampling_config
        self._max_new_tokens = max_new_tokens
        self._verbose = verbose

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "LocalTensorRTLLM"

    @property
    defmetadata(self) -> LLMMetadata:
"""LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_new_tokens,
            model_name=self.model_path,
        )

    @llm_chat_callback()
    defchat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.complete(prompt, formatted=True, **kwargs)
        return completion_response_to_chat_response(completion_response)

    @llm_completion_callback()
    defcomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        try:
            importtorch
        except ImportError:
            raise ImportError("nvidia_tensorrt requires `pip install torch`.")

        self.generate_kwargs.update({"stream": False})

        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        input_text = prompt
        input_ids, input_lengths = parse_input(
            input_text, self._tokenizer, EOS_TOKEN, self._model_config
        )

        max_input_length = torch.max(input_lengths).item()
        self._model.setup(
            input_lengths.size(0), max_input_length, self._max_new_tokens, 1
        )  # beam size is set to 1
        if self._verbose:
            start_time = time.time()

        output_ids = self._model.decode(input_ids, input_lengths, self._sampling_config)
        torch.cuda.synchronize()

        elapsed_time = -1.0
        if self._verbose:
            end_time = time.time()
            elapsed_time = end_time - start_time

        output_txt, output_token_ids = get_output(
            output_ids, input_lengths, self._max_new_tokens, self._tokenizer
        )

        if self._verbose:
            print(f"Input context length  : {input_ids.shape[1]}")
            print(f"Inference time        : {elapsed_time:.2f} seconds")
            print(f"Output context length : {len(output_token_ids)} ")
            print(
                f"Inference token/sec   : {(len(output_token_ids)/elapsed_time):2f}"
            )

        # call garbage collected after inference
        torch.cuda.empty_cache()
        gc.collect()

        return CompletionResponse(
            text=output_txt,
            raw=generate_completion_dict(output_txt, self._model, self.model_path),
        )

    @llm_completion_callback()
    defstream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        raise NotImplementedError(
            "Nvidia TensorRT-LLM does not currently support streaming completion."
        )

```
 |  
| --- | --- |  
###  metadata `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/nvidia_tensorrt/#llama_index.llms.nvidia_tensorrt.LocalTensorRTLLM.metadata "Permanent link")

```
metadata: 

```

LLM metadata.
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/nvidia_tensorrt/#llama_index.llms.nvidia_tensorrt.LocalTensorRTLLM.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-nvidia-tensorrt/llama_index/llms/nvidia_tensorrt/base.py`  
| 
```
276
277
278
279
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "LocalTensorRTLLM"

```
 |  
| --- | --- |  
options: members: - LocalTensorRTLLM
