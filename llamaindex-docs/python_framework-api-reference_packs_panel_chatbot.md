# Panel chatbot
##  PanelChatPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/panel_chatbot/#llama_index.packs.panel_chatbot.PanelChatPack "Permanent link")
Bases: 
Panel chatbot pack.
Source code in `llama-index-packs/llama-index-packs-panel-chatbot/llama_index/packs/panel_chatbot/base.py`  
| 
```
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
```
 | 
```
classPanelChatPack(BaseLlamaPack):
"""Panel chatbot pack."""

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {}

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        for variable in ENVIRONMENT_VARIABLES:
            if variable not in os.environ:
                raise ValueError("%s environment variable is not set", variable)

        importpanelaspn

        if __name__ == "__main__":
            # 'pytest tests' will fail if app is imported elsewhere
            fromappimport create_chat_ui

            pn.serve(create_chat_ui)
        elif __name__.startswith("bokeh"):
            fromappimport create_chat_ui

            create_chat_ui().servable()
        else:
            print(
                "To serve the Panel ChatBot please run this file with 'panel serve' or 'python'"
            )

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/panel_chatbot/#llama_index.packs.panel_chatbot.PanelChatPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-panel-chatbot/llama_index/packs/panel_chatbot/base.py`  
| 
```
17
18
19
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {}

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/panel_chatbot/#llama_index.packs.panel_chatbot.PanelChatPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-panel-chatbot/llama_index/packs/panel_chatbot/base.py`  
| 
```
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
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    for variable in ENVIRONMENT_VARIABLES:
        if variable not in os.environ:
            raise ValueError("%s environment variable is not set", variable)

    importpanelaspn

    if __name__ == "__main__":
        # 'pytest tests' will fail if app is imported elsewhere
        fromappimport create_chat_ui

        pn.serve(create_chat_ui)
    elif __name__.startswith("bokeh"):
        fromappimport create_chat_ui

        create_chat_ui().servable()
    else:
        print(
            "To serve the Panel ChatBot please run this file with 'panel serve' or 'python'"
        )

```
 |  
| --- | --- |  
options: members: - PanelChatPack
