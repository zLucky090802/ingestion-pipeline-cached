# Earnings call transcript
##  EarningsCallTranscript [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/earnings_call_transcript/#llama_index.readers.earnings_call_transcript.EarningsCallTranscript "Permanent link")
Bases: 
Source code in `llama-index-integrations/readers/llama-index-readers-earnings-call-transcript/llama_index/readers/earnings_call_transcript/base.py`  
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
```
 | 
```
classEarningsCallTranscript(BaseReader):
    def__init__(self, year: int, ticker: str, quarter: str):
"""
        Get the earning call transcripts for a given company, in a given year and quarter.

        Args:
            year (int): Year of the transcript
            ticker (str): ticker symbol of the stock
            quarter (str): quarter

        """
        curr_year = datetime.now().year
        assert year <= curr_year, "The year should be less than current year"

        assert quarter in [
            "Q1",
            "Q2",
            "Q3",
            "Q4",
        ], 'The quarter should from the list ["Q1","Q2","Q3","Q4"]'
        self.year = year
        self.ticker = ticker
        self.quarter = quarter

    defload_data(self) -> List[Document]:
        resp_dict, speakers_list = get_earnings_transcript(
            self.quarter, self.ticker, self.year
        )
        return Document(
            text=resp_dict["content"],
            extra_info={
                "ticker": resp_dict["symbol"],
                "quarter": "Q" + str(resp_dict["quarter"]),
                "date_time": resp_dict["date"],
                "speakers_list": speakers_list,
            },
        )

```
 |  
| --- | --- |  
options: members: - EarningsCallTranscript
