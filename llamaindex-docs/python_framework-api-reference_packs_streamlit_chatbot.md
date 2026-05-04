# Streamlit chatbot
##  StreamlitChatPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/streamlit_chatbot/#llama_index.packs.streamlit_chatbot.StreamlitChatPack "Permanent link")
Bases: 
Streamlit chatbot pack.
Source code in `llama-index-packs/llama-index-packs-streamlit-chatbot/llama_index/packs/streamlit_chatbot/base.py`  
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
```
 | 
```
classStreamlitChatPack(BaseLlamaPack):
"""Streamlit chatbot pack."""

    def__init__(
        self,
        wikipedia_page: str = "Snowflake Inc.",
        run_from_main: bool = False,
        **kwargs: Any,
    ) -> None:
"""Init params."""
        if not run_from_main:
            raise ValueError(
                "Please run this llama-pack directly with "
                "`streamlit run [download_dir]/streamlit_chatbot/base.py`"
            )

        self.wikipedia_page = wikipedia_page

    defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
        return {}

    defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
        importstreamlitasst
        fromstreamlit_pillsimport pills

        st.set_page_config(
            page_title=f"Chat with {self.wikipedia_page}'s Wikipedia page, powered by LlamaIndex",
            page_icon="🦙",
            layout="centered",
            initial_sidebar_state="auto",
            menu_items=None,
        )

        if "messages" not in st.session_state:  # Initialize the chat messages history
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Ask me a question about Snowflake!"}
            ]

        st.title(
            f"Chat with {self.wikipedia_page}'s Wikipedia page, powered by LlamaIndex 💬🦙"
        )
        st.info(
            "This example is powered by the **[Llama Hub Wikipedia Loader](https://llamahub.ai/l/wikipedia)**. Use any of [Llama Hub's many loaders](https://llamahub.ai/) to retrieve and chat with your data via a Streamlit app.",
            icon="ℹ️",
        )

        defadd_to_message_history(role, content):
            message = {"role": role, "content": str(content)}
            st.session_state["messages"].append(
                message
            )  # Add response to message history

        @st.cache_resource
        defload_index_data():
            loader = WikipediaReader()
            docs = loader.load_data(pages=[self.wikipedia_page])
            Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5)

            return VectorStoreIndex.from_documents(docs)

        index = load_index_data()

        selected = pills(
            "Choose a question to get started or write your own below.",
            [
                "What is Snowflake?",
                "What company did Snowflake announce they would acquire in October 2023?",
                "What company did Snowflake acquire in March 2022?",
                "When did Snowflake IPO?",
            ],
            clearable=True,
            index=None,
        )

        if "chat_engine" not in st.session_state:  # Initialize the query engine
            st.session_state["chat_engine"] = index.as_chat_engine(
                chat_mode="context", verbose=True
            )

        for message in st.session_state["messages"]:  # Display the prior chat messages
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # To avoid duplicated display of answered pill questions each rerun
        if selected and selected not in st.session_state.get(
            "displayed_pill_questions", set()
        ):
            st.session_state.setdefault("displayed_pill_questions", set()).add(selected)
            with st.chat_message("user"):
                st.write(selected)
            with st.chat_message("assistant"):
                response = st.session_state["chat_engine"].stream_chat(selected)
                response_str = ""
                response_container = st.empty()
                for token in response.response_gen:
                    response_str += token
                    response_container.write(response_str)
                add_to_message_history("user", selected)
                add_to_message_history("assistant", response)

        if prompt := st.chat_input(
            "Your question"
        ):  # Prompt for user input and save to chat history
            add_to_message_history("user", prompt)

            # Display the new question immediately after it is entered
            with st.chat_message("user"):
                st.write(prompt)

            # If last message is not from assistant, generate a new response
            # if st.session_state["messages"][-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                response = st.session_state["chat_engine"].stream_chat(prompt)
                response_str = ""
                response_container = st.empty()
                for token in response.response_gen:
                    response_str += token
                    response_container.write(response_str)
                # st.write(response.response)
                add_to_message_history("assistant", response.response)

            # Save the state of the generator
            st.session_state["response_gen"] = response.response_gen

```
 |  
| --- | --- |  
###  get_modules [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/streamlit_chatbot/#llama_index.packs.streamlit_chatbot.StreamlitChatPack.get_modules "Permanent link")

```
get_modules() -> [, ]

```

Get modules.
Source code in `llama-index-packs/llama-index-packs-streamlit-chatbot/llama_index/packs/streamlit_chatbot/base.py`  
| 
```
37
38
39
```
 | 
```
defget_modules(self) -> Dict[str, Any]:
"""Get modules."""
    return {}

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/streamlit_chatbot/#llama_index.packs.streamlit_chatbot.StreamlitChatPack.run "Permanent link")

```
run(*args: , **kwargs: ) -> 

```

Run the pipeline.
Source code in `llama-index-packs/llama-index-packs-streamlit-chatbot/llama_index/packs/streamlit_chatbot/base.py`  
| 
```
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
```
 | 
```
defrun(self, *args: Any, **kwargs: Any) -> Any:
"""Run the pipeline."""
    importstreamlitasst
    fromstreamlit_pillsimport pills

    st.set_page_config(
        page_title=f"Chat with {self.wikipedia_page}'s Wikipedia page, powered by LlamaIndex",
        page_icon="🦙",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    if "messages" not in st.session_state:  # Initialize the chat messages history
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Ask me a question about Snowflake!"}
        ]

    st.title(
        f"Chat with {self.wikipedia_page}'s Wikipedia page, powered by LlamaIndex 💬🦙"
    )
    st.info(
        "This example is powered by the **[Llama Hub Wikipedia Loader](https://llamahub.ai/l/wikipedia)**. Use any of [Llama Hub's many loaders](https://llamahub.ai/) to retrieve and chat with your data via a Streamlit app.",
        icon="ℹ️",
    )

    defadd_to_message_history(role, content):
        message = {"role": role, "content": str(content)}
        st.session_state["messages"].append(
            message
        )  # Add response to message history

    @st.cache_resource
    defload_index_data():
        loader = WikipediaReader()
        docs = loader.load_data(pages=[self.wikipedia_page])
        Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5)

        return VectorStoreIndex.from_documents(docs)

    index = load_index_data()

    selected = pills(
        "Choose a question to get started or write your own below.",
        [
            "What is Snowflake?",
            "What company did Snowflake announce they would acquire in October 2023?",
            "What company did Snowflake acquire in March 2022?",
            "When did Snowflake IPO?",
        ],
        clearable=True,
        index=None,
    )

    if "chat_engine" not in st.session_state:  # Initialize the query engine
        st.session_state["chat_engine"] = index.as_chat_engine(
            chat_mode="context", verbose=True
        )

    for message in st.session_state["messages"]:  # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # To avoid duplicated display of answered pill questions each rerun
    if selected and selected not in st.session_state.get(
        "displayed_pill_questions", set()
    ):
        st.session_state.setdefault("displayed_pill_questions", set()).add(selected)
        with st.chat_message("user"):
            st.write(selected)
        with st.chat_message("assistant"):
            response = st.session_state["chat_engine"].stream_chat(selected)
            response_str = ""
            response_container = st.empty()
            for token in response.response_gen:
                response_str += token
                response_container.write(response_str)
            add_to_message_history("user", selected)
            add_to_message_history("assistant", response)

    if prompt := st.chat_input(
        "Your question"
    ):  # Prompt for user input and save to chat history
        add_to_message_history("user", prompt)

        # Display the new question immediately after it is entered
        with st.chat_message("user"):
            st.write(prompt)

        # If last message is not from assistant, generate a new response
        # if st.session_state["messages"][-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            response = st.session_state["chat_engine"].stream_chat(prompt)
            response_str = ""
            response_container = st.empty()
            for token in response.response_gen:
                response_str += token
                response_container.write(response_str)
            # st.write(response.response)
            add_to_message_history("assistant", response.response)

        # Save the state of the generator
        st.session_state["response_gen"] = response.response_gen

```
 |  
| --- | --- |  
options: members: - StreamlitChatPack
