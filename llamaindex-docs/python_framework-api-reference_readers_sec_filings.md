# Sec filings
##  SECFilingsLoader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/sec_filings/#llama_index.readers.sec_filings.SECFilingsLoader "Permanent link")
Bases: 
SEC Filings loader Get the SEC filings of multiple tickers.
Source code in `llama-index-integrations/readers/llama-index-readers-sec-filings/llama_index/readers/sec_filings/base.py`  
| 
```
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
```
 | 
```
classSECFilingsLoader(BaseReader):
"""
    SEC Filings loader
    Get the SEC filings of multiple tickers.
    """

    def__init__(
        self,
        tickers: List[str],
        amount: int,
        filing_type: str = "10-K",
        num_workers: int = 2,
        include_amends: bool = False,
    ):
        assert filing_type in [
            "10-K",
            "10-Q",
        ], "The supported document types are 10-K and 10-Q"

        self.tickers = tickers
        self.amount = amount
        self.filing_type = filing_type
        self.num_workers = num_workers
        self.include_amends = include_amends

        self.se = SECExtractor(
            tickers, amount, filing_type, include_amends=include_amends
        )

        os.makedirs("data", exist_ok=True)

    defmultiprocess_run(self, tic):
        # print(f"Started for {tic}")
        tic_dict = self.se.get_accession_numbers(tic)
        text_dict = defaultdict(list)
        for tic, fields in tic_dict.items():
            os.makedirs(f"data/{tic}", exist_ok=True)
            print(f"Started for {tic}")

            field_urls = [field["url"] for field in fields]
            years = [field["year"] for field in fields]
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=self.num_workers
            ) as executor:
                results = executor.map(self.se.get_text_from_url, field_urls)
            for idx, res in enumerate(results):
                all_text, filing_type = res
                text_dict[tic].append(
                    {
                        "year": years[idx],
                        "ticker": tic,
                        "all_texts": all_text,
                        "filing_type": filing_type,
                    }
                )
        return text_dict

    defload_data(self):
        start = time.time()
        thread_workers = min(len(self.tickers), self.num_workers)
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=thread_workers
        ) as executor:
            results = executor.map(self.multiprocess_run, self.tickers)

        for res in results:
            curr_tic = next(iter(res.keys()))
            for data in res[curr_tic]:
                curr_year = data["year"]
                curr_filing_type = data["filing_type"]
                if curr_filing_type in ["10-K/A", "10-Q/A"]:
                    curr_filing_type = curr_filing_type.replace("/", "")
                if curr_filing_type in ["10-K", "10-KA"]:
                    os.makedirs(f"data/{curr_tic}/{curr_year}", exist_ok=True)
                    with open(
                        f"data/{curr_tic}/{curr_year}/{curr_filing_type}.json", "w"
                    ) as f:
                        json.dump(data, f, indent=4)
                elif curr_filing_type in ["10-Q", "10-QA"]:
                    os.makedirs(f"data/{curr_tic}/{curr_year[:-2]}", exist_ok=True)
                    with open(
                        f"data/{curr_tic}/{curr_year[:-2]}/{curr_filing_type}_{curr_year[-2:]}.json",
                        "w",
                    ) as f:
                        json.dump(data, f, indent=4)
                print(
                    f"Done for {curr_tic} for document {curr_filing_type} and year"
                    f" {curr_year}"
                )

        print(f"It took {round(time.time()-start,2)} seconds")

```
 |  
| --- | --- |  
options: members: - SECFilingsLoader
