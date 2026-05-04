# Pandas ai
##  PandasAIReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pandas_ai/#llama_index.readers.pandas_ai.PandasAIReader "Permanent link")
Bases: 
Pandas AI reader.
Light wrapper around https://github.com/gventuri/pandas-ai.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `llm`  |  `Optional[llm]`  |  LLM to use. Defaults to None.  |  _required_  |  
|  `concat_rows`  |  `bool`  |  whether to concatenate all rows into one document. If set to False, a Document will be created for each row. True by default.  |  `True`  |  
|  `col_joiner`  |  Separator to use for joining cols per row. Set to ", " by default.  |  `', '`  |  
|  `row_joiner`  |  Separator to use for joining each row. Only used when `concat_rows=True`. Set to "\n" by default.  |  `'\n'`  |  
|  `pandas_config`  |  `dict`  |  Options for the `pandas.read_csv` function call. Refer to https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html for more information. Set to empty dict by default, this means pandas will try to figure out the separators, table head, etc. on its own.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pandas-ai/llama_index/readers/pandas_ai/base.py`  
| 
```
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
```
 | 
```
classPandasAIReader(BaseReader):
r"""
    Pandas AI reader.

    Light wrapper around https://github.com/gventuri/pandas-ai.

    Args:
        llm (Optional[pandas.llm]): LLM to use. Defaults to None.
        concat_rows (bool): whether to concatenate all rows into one document.
            If set to False, a Document will be created for each row.
            True by default.

        col_joiner (str): Separator to use for joining cols per row.
            Set to ", " by default.

        row_joiner (str): Separator to use for joining each row.
            Only used when `concat_rows=True`.
            Set to "\n" by default.

        pandas_config (dict): Options for the `pandas.read_csv` function call.
            Refer to https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
            for more information.
            Set to empty dict by default, this means pandas will try to figure
            out the separators, table head, etc. on its own.

    """

    def__init__(
        self,
        pandas_llm: Optional[PandasLLM] = None,
        concat_rows: bool = True,
        col_joiner: str = ", ",
        row_joiner: str = "\n",
        pandas_config: dict = {},
    ) -> None:
"""Init params."""
        self._llm = pandas_llm or OpenAI()
        self._pandasai_config = {"llm": self._llm}

        self._concat_rows = concat_rows
        self._col_joiner = col_joiner
        self._row_joiner = row_joiner
        self._pandas_config = pandas_config

    defrun_pandas_ai(
        self,
        initial_df: pd.DataFrame,
        query: str,
        is_conversational_answer: bool = False,
    ) -> Any:
"""Load dataframe."""
        smart_df = SmartDataframe(initial_df, config=self._pandasai_config)
        return smart_df.chat(query=query)

    defload_data(
        self,
        initial_df: pd.DataFrame,
        query: str,
        is_conversational_answer: bool = False,
    ) -> List[Document]:
"""Parse file."""
        result = self.run_pandas_ai(
            initial_df, query, is_conversational_answer=is_conversational_answer
        )
        if is_conversational_answer:
            return [Document(text=result)]
        else:
            if isinstance(result, (np.generic)):
                result = pd.Series(result)
            elif isinstance(result, (pd.Series, pd.DataFrame)):
                pass
            else:
                raise ValueError(f"Unexpected type for result: {type(result)}")
            # if not conversational answer, use Pandas CSV Reader
            reader = PandasCSVReader(
                concat_rows=self._concat_rows,
                col_joiner=self._col_joiner,
                row_joiner=self._row_joiner,
                pandas_config=self._pandas_config,
            )

            with TemporaryDirectory() as tmpdir:
                outpath = Path(tmpdir) / "out.csv"
                with outpath.open("w") as f:
                    # TODO: add option to specify index=False
                    result.to_csv(f, index=False)

                return reader.load_data(outpath)

```
 |  
| --- | --- |  
###  run_pandas_ai [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pandas_ai/#llama_index.readers.pandas_ai.PandasAIReader.run_pandas_ai "Permanent link")

```
run_pandas_ai(
    initial_df: DataFrame,
    query: ,
    is_conversational_answer:  = False,
) -> 

```

Load dataframe.
Source code in `llama-index-integrations/readers/llama-index-readers-pandas-ai/llama_index/readers/pandas_ai/base.py`  
| 
```
62
63
64
65
66
67
68
69
70
```
 | 
```
defrun_pandas_ai(
    self,
    initial_df: pd.DataFrame,
    query: str,
    is_conversational_answer: bool = False,
) -> Any:
"""Load dataframe."""
    smart_df = SmartDataframe(initial_df, config=self._pandasai_config)
    return smart_df.chat(query=query)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pandas_ai/#llama_index.readers.pandas_ai.PandasAIReader.load_data "Permanent link")

```
load_data(
    initial_df: DataFrame,
    query: ,
    is_conversational_answer:  = False,
) -> []

```

Parse file.
Source code in `llama-index-integrations/readers/llama-index-readers-pandas-ai/llama_index/readers/pandas_ai/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    initial_df: pd.DataFrame,
    query: str,
    is_conversational_answer: bool = False,
) -> List[Document]:
"""Parse file."""
    result = self.run_pandas_ai(
        initial_df, query, is_conversational_answer=is_conversational_answer
    )
    if is_conversational_answer:
        return [Document(text=result)]
    else:
        if isinstance(result, (np.generic)):
            result = pd.Series(result)
        elif isinstance(result, (pd.Series, pd.DataFrame)):
            pass
        else:
            raise ValueError(f"Unexpected type for result: {type(result)}")
        # if not conversational answer, use Pandas CSV Reader
        reader = PandasCSVReader(
            concat_rows=self._concat_rows,
            col_joiner=self._col_joiner,
            row_joiner=self._row_joiner,
            pandas_config=self._pandas_config,
        )

        with TemporaryDirectory() as tmpdir:
            outpath = Path(tmpdir) / "out.csv"
            with outpath.open("w") as f:
                # TODO: add option to specify index=False
                result.to_csv(f, index=False)

            return reader.load_data(outpath)

```
 |  
| --- | --- |  
options: members: - PandasAIReader
