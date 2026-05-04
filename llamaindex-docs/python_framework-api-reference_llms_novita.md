# Novita
##  NovitaAI [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/novita/#llama_index.llms.novita.NovitaAI "Permanent link")
Bases: 
NovitaAI LLM.
Novita AI & LlamaIndex Integration Guide Effortlessly integrate Novita AI with LlamaIndex to build intelligent, data-powered applications.
Designed for optimal indexing and retrieval, LlamaIndex excels in delivering high efficiency for applications requiring precise and fast data access. By combining [Novita AI](https://novita.ai/) with LlamaIndex, you will unlock key benefits such as superior data retrieval accuracy, unmatched scalability, and cost-effective performance. This guide will walk you through how to use LlamaIndex with Novita AI based on the OpenAl APl, offering smarter, scalable, and highly efficient AI solutions that drive innovation and deliver exceptional results for developers.
How to Integrate Novita AI API with LlamaIndex Step 1: Visit [Model Library](https://novita.ai/llm-api) on Novita AI and select a model of interest. 
Navigate to the demo page of the chosen model and click the `Code` button on the right. Copy the model’s name and make a note of it. [Log in ](https://novita.ai/user/login)to the Novita platform. After logging in, go to the platform’s [settings page](https://novita.ai/settings). Create a new [API key](https://novita.ai/settings/key-management) and copy it for service authentication. Install `llama_index` and related Python libraries by running: Write Python code and set the model name and API key as parameters in the NovitaAI class. Run the code to get the output.
For more examples, refer to the documentation: [llama_index/llama-index-integrations/llms/llama-index-llms-novita at main · run-llama/llama_index](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/llms/llama-index-llms-novita).
Source code in `llama-index-integrations/llms/llama-index-llms-novita/llama_index/llms/novita/base.py`  
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
```
 | 
```
classNovitaAI(OpenAILike):
"""
    NovitaAI LLM.

    Novita AI & LlamaIndex Integration Guide
    Effortlessly integrate Novita AI with LlamaIndex to build intelligent, data-powered applications.

    Designed for optimal indexing and retrieval, LlamaIndex excels in delivering high efficiency for applications requiring precise and fast data access. By combining [Novita AI](https://novita.ai/) with LlamaIndex, you will unlock key benefits such as superior data retrieval accuracy, unmatched scalability, and cost-effective performance.
    This guide will walk you through how to use LlamaIndex with Novita AI based on the OpenAl APl, offering smarter, scalable, and highly efficient AI solutions that drive innovation and deliver exceptional results for developers.

    How to Integrate Novita AI API with LlamaIndex
    Step 1: Visit [Model Library](https://novita.ai/llm-api) on Novita AI and select a model of interest.
      ![images/Step1VisitModelLibraryonNovitaAIandselectamodelofinterest.png](https://mintlify.s3.us-west-1.amazonaws.com/novitaai/images/Step1VisitModelLibraryonNovitaAIandselectamodelofinterest.png)

    Step 2: Navigate to the demo page of the chosen model and click the `Code` button on the right.
      ![images/Step2NavigatetothedemopageofthechosenmodelandclicktheCodebuttonontheright.png](https://mintlify.s3.us-west-1.amazonaws.com/novitaai/images/Step2NavigatetothedemopageofthechosenmodelandclicktheCodebuttonontheright.png)

    Step 3: Copy the model’s name and make a note of it.
      ![images/Step3Copythemodel’snameandmakeanoteofit.png](https://mintlify.s3.us-west-1.amazonaws.com/novitaai/images/Step3Copythemodel%E2%80%99snameandmakeanoteofit.png)

    Step 4: [Log in ](https://novita.ai/user/login)to the Novita platform.
      ![images/Step4LogintotheNovitaplatform.png](https://mintlify.s3.us-west-1.amazonaws.com/novitaai/images/Step4LogintotheNovitaplatform.png)

    Step 5: After logging in, go to the platform’s [settings page](https://novita.ai/settings).
      ![images/Step5Afterloggingin,gototheplatform’ssettingspage.png](https://mintlify.s3.us-west-1.amazonaws.com/novitaai/images/Step5Afterloggingin,gototheplatform%E2%80%99ssettingspage.png)

    Step 6: Create a new [API key](https://novita.ai/settings/key-management) and copy it for service authentication.
      ![images/Step6CreateanewAPIkeyandcopyitforserviceauthentication.png](https://mintlify.s3.us-west-1.amazonaws.com/novitaai/images/Step6CreateanewAPIkeyandcopyitforserviceauthentication.png)

    Step 7: Install `llama_index` and related Python libraries by running:
      ![images/Step7Installllama_indexandrelatedPythonlibrariesbyrunning.png](https://mintlify.s3.us-west-1.amazonaws.com/novitaai/images/Step7Installllama_indexandrelatedPythonlibrariesbyrunning.png)

    Step 8: Write Python code and set the model name and API key as parameters in the NovitaAI class.
      ![images/Step8WritePythoncodeandsetthemodelnameandAPIkeyasparametersintheNovitaAIclass.png](https://mintlify.s3.us-west-1.amazonaws.com/novitaai/images/Step8WritePythoncodeandsetthemodelnameandAPIkeyasparametersintheNovitaAIclass.png)

    Step 9: Run the code to get the output.
      ![images/Step9Runthecodetogettheoutput.png](https://mintlify.s3.us-west-1.amazonaws.com/novitaai/images/Step9Runthecodetogettheoutput.png)

    For more examples, refer to the documentation: [llama_index/llama-index-integrations/llms/llama-index-llms-novita at main · run-llama/llama_index](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/llms/llama-index-llms-novita).

    """

    def__init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        temperature: float = 0.95,
        max_tokens: int = 1024,
        is_chat_model: bool = True,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}
        api_base = get_from_param_or_env(
            "api_base", DEFAULT_API_BASE, "NOVITA_API_BASE"
        )
        api_key = get_from_param_or_env("api_key", api_key, "NOVITA_API_KEY")

        super().__init__(
            api_base=api_base,
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            is_chat_model=is_chat_model,
            is_function_calling_model=is_function_calling_model(model),
            additional_kwargs=additional_kwargs,
            **kwargs,
        )

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "NovitaAI"

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/llms/novita/#llama_index.llms.novita.NovitaAI.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-integrations/llms/llama-index-llms-novita/llama_index/llms/novita/base.py`  
| 
```
92
93
94
95
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "NovitaAI"

```
 |  
| --- | --- |  
options: members: - NovitaAI
