# Json
##  JSONReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/json/#llama_index.readers.json.JSONReader "Permanent link")
Bases: 
JSON reader.
Reads JSON documents with options to help us out relationships between nodes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `levels_back`  |  the number of levels to go back in the JSON tree, 0 if you want all levels. If levels_back is None, then we just format the JSON and make each line an embedding  |  `None`  |  
|  `collapse_length`  |  the maximum number of characters a JSON fragment would be collapsed in the output (levels_back needs to be not None) ex: if collapse_length = 10, and input is {a: [1, 2, 3], b: {"hello": "world", "foo": "bar"}} then a would be collapsed into one line, while b would not. Recommend starting around 100 and then adjusting from there.  |  `None`  |  
|  `is_jsonl`  |  `Optional[bool]`  |  If True, indicates that the file is in JSONL format.  |  `False`  |  
|  `clean_json`  |  `Optional[bool]`  |  If True, lines containing only JSON structure are removed.  |  `True`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-json/llama_index/readers/json/base.py`  
| 
```
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
```
 | 
```
classJSONReader(BaseReader):
"""
    JSON reader.

    Reads JSON documents with options to help us out relationships between nodes.

    Args:
        levels_back (int): the number of levels to go back in the JSON tree, 0
          if you want all levels. If levels_back is None, then we just format the
          JSON and make each line an embedding

        collapse_length (int): the maximum number of characters a JSON fragment
          would be collapsed in the output (levels_back needs to be not None)
          ex: if collapse_length = 10, and
          input is {a: [1, 2, 3], b: {"hello": "world", "foo": "bar"}}
          then a would be collapsed into one line, while b would not.
          Recommend starting around 100 and then adjusting from there.

        is_jsonl (Optional[bool]): If True, indicates that the file is in JSONL format.
        Defaults to False.

        clean_json (Optional[bool]): If True, lines containing only JSON structure are removed.
        This removes lines that are not as useful. If False, no lines are removed and the document maintains a valid JSON object structure.
        If levels_back is set the json is not cleaned and this option is ignored.
        Defaults to True.

    """

    def__init__(
        self,
        levels_back: Optional[int] = None,
        collapse_length: Optional[int] = None,
        ensure_ascii: bool = False,
        is_jsonl: Optional[bool] = False,
        clean_json: Optional[bool] = True,
    ) -> None:
"""Initialize with arguments."""
        super().__init__()
        self.levels_back = levels_back
        self.collapse_length = collapse_length
        self.ensure_ascii = ensure_ascii
        self.is_jsonl = is_jsonl
        self.clean_json = clean_json

    defload_data(
        self, input_file: str, extra_info: Optional[Dict] = {}
    ) -> List[Document]:
"""Load data from the input file."""
        with open(input_file, encoding="utf-8") as f:
            load_data = []
            if self.is_jsonl:
                for line in f:
                    load_data.append(json.loads(line.strip()))
            else:
                load_data = [json.load(f)]

            documents = []
            for data in load_data:
                if self.levels_back is None and self.clean_json is True:
                    # If levels_back isn't set and clean json is set,
                    # remove lines containing only formatting, we just format and make each
                    # line an embedding
                    json_output = json.dumps(
                        data, indent=0, ensure_ascii=self.ensure_ascii
                    )
                    lines = json_output.split("\n")
                    useful_lines = [
                        line for line in lines if not re.match(r"^[{}\[\],]*$", line)
                    ]
                    documents.append(
                        Document(text="\n".join(useful_lines), metadata=extra_info)
                    )

                elif self.levels_back is None and self.clean_json is False:
                    # If levels_back isn't set  and clean json is False, create documents without cleaning
                    json_output = json.dumps(data, ensure_ascii=self.ensure_ascii)
                    documents.append(Document(text=json_output, metadata=extra_info))

                elif self.levels_back is not None:
                    # If levels_back is set, we make the embeddings contain the labels
                    # from further up the JSON tree
                    lines = [
                        *_depth_first_yield(
                            data,
                            self.levels_back,
                            self.collapse_length,
                            [],
                            self.ensure_ascii,
                        )
                    ]
                    documents.append(
                        Document(text="\n".join(lines), metadata=extra_info)
                    )
            return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/json/#llama_index.readers.json.JSONReader.load_data "Permanent link")

```
load_data(
    input_file: , extra_info: Optional[] = {}
) -> []

```

Load data from the input file.
Source code in `llama-index-integrations/readers/llama-index-readers-json/llama_index/readers/json/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, input_file: str, extra_info: Optional[Dict] = {}
) -> List[Document]:
"""Load data from the input file."""
    with open(input_file, encoding="utf-8") as f:
        load_data = []
        if self.is_jsonl:
            for line in f:
                load_data.append(json.loads(line.strip()))
        else:
            load_data = [json.load(f)]

        documents = []
        for data in load_data:
            if self.levels_back is None and self.clean_json is True:
                # If levels_back isn't set and clean json is set,
                # remove lines containing only formatting, we just format and make each
                # line an embedding
                json_output = json.dumps(
                    data, indent=0, ensure_ascii=self.ensure_ascii
                )
                lines = json_output.split("\n")
                useful_lines = [
                    line for line in lines if not re.match(r"^[{}\[\],]*$", line)
                ]
                documents.append(
                    Document(text="\n".join(useful_lines), metadata=extra_info)
                )

            elif self.levels_back is None and self.clean_json is False:
                # If levels_back isn't set  and clean json is False, create documents without cleaning
                json_output = json.dumps(data, ensure_ascii=self.ensure_ascii)
                documents.append(Document(text=json_output, metadata=extra_info))

            elif self.levels_back is not None:
                # If levels_back is set, we make the embeddings contain the labels
                # from further up the JSON tree
                lines = [
                    *_depth_first_yield(
                        data,
                        self.levels_back,
                        self.collapse_length,
                        [],
                        self.ensure_ascii,
                    )
                ]
                documents.append(
                    Document(text="\n".join(lines), metadata=extra_info)
                )
        return documents

```
 |  
| --- | --- |  
options: members: - JSONReader
