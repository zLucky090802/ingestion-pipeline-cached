# Imdb review
##  IMDBReviews [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/imdb_review/#llama_index.readers.imdb_review.IMDBReviews "Permanent link")
Bases: 
Source code in `llama-index-integrations/readers/llama-index-readers-imdb-review/llama_index/readers/imdb_review/base.py`  
| 
```
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
```
 | 
```
classIMDBReviews(BaseReader):
    def__init__(
        self,
        movie_name_year: str,
        webdriver_engine: str = "google",
        generate_csv: bool = False,
        multithreading: bool = False,
        max_workers: int = 0,
        reviews_folder: str = "movie_reviews",
    ):
"""
        Get the IMDB reviews of a movie.

        Args:
            movie_name_year (str): movie name alongwith year
            webdriver_engine (str, optional): webdriver engine to use. Defaults to "google".
            generate_csv (bool, optional): whether to generate csv. Defaults to False.
            multithreading (bool, optional): whether to use multithreading. Defaults to False.
            max_workers (int, optional): number of workers if you are using multithreading. Defaults to 0.

        """
        assert webdriver_engine in [
            "google",
            "edge",
            "firefox",
        ], "The webdriver should be in ['google','edge','firefox']"
        self.movie_name_year = movie_name_year
        self.webdriver_engine = webdriver_engine
        self.generate_csv = generate_csv
        self.multithreading = multithreading
        self.max_workers = max_workers
        self.reviews_folder = reviews_folder

    defload_data(self) -> List[Document]:
"""
        Scrapes the data from the IMDB website movie reviews.

        Returns:
            List[Document]: document object in llama index with date and rating as extra information

        """
        (
            reviews_date,
            reviews_title,
            reviews_comment,
            reviews_rating,
            reviews_link,
            review_helpful,
            review_total_votes,
            review_if_spoiler,
        ) = main_scraper(
            self.movie_name_year,
            self.webdriver_engine,
            self.generate_csv,
            self.multithreading,
            self.max_workers,
            self.reviews_folder,
        )

        all_docs = []
        for i in range(len(reviews_date)):
            all_docs.append(
                Document(
                    text=reviews_title[i] + " " + reviews_comment[i],
                    extra_info={
                        "date": reviews_date[i],
                        "rating": reviews_rating[i],
                        "link": reviews_link[i],
                        "found_helpful_votes": review_helpful[i],
                        "total_votes": review_total_votes[i],
                        "spolier": review_if_spoiler[i],
                    },
                )
            )
        return all_docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/imdb_review/#llama_index.readers.imdb_review.IMDBReviews.load_data "Permanent link")

```
load_data() -> []

```

Scrapes the data from the IMDB website movie reviews.
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: document object in llama index with date and rating as extra information  |  
Source code in `llama-index-integrations/readers/llama-index-readers-imdb-review/llama_index/readers/imdb_review/base.py`  
| 
```
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
```
 | 
```
defload_data(self) -> List[Document]:
"""
    Scrapes the data from the IMDB website movie reviews.

    Returns:
        List[Document]: document object in llama index with date and rating as extra information

    """
    (
        reviews_date,
        reviews_title,
        reviews_comment,
        reviews_rating,
        reviews_link,
        review_helpful,
        review_total_votes,
        review_if_spoiler,
    ) = main_scraper(
        self.movie_name_year,
        self.webdriver_engine,
        self.generate_csv,
        self.multithreading,
        self.max_workers,
        self.reviews_folder,
    )

    all_docs = []
    for i in range(len(reviews_date)):
        all_docs.append(
            Document(
                text=reviews_title[i] + " " + reviews_comment[i],
                extra_info={
                    "date": reviews_date[i],
                    "rating": reviews_rating[i],
                    "link": reviews_link[i],
                    "found_helpful_votes": review_helpful[i],
                    "total_votes": review_total_votes[i],
                    "spolier": review_if_spoiler[i],
                },
            )
        )
    return all_docs

```
 |  
| --- | --- |  
options: members: - IMDBReviews
