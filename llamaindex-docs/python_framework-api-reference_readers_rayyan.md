# Rayyan
##  RayyanReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/rayyan/#llama_index.readers.rayyan.RayyanReader "Permanent link")
Bases: 
Rayyan reader. Reads articles from a Rayyan review.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `credentials_path`  |  Rayyan credentials path.  |  _required_  |  
|  `rayyan_url`  |  Rayyan URL. Defaults to https://rayyan.ai. Set to an alternative URL if you are using a non-production Rayyan instance.  |  `'https://rayyan.ai'`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-rayyan/llama_index/readers/rayyan/base.py`  
| 
```
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
```
 | 
```
classRayyanReader(BaseReader):
"""
    Rayyan reader. Reads articles from a Rayyan review.

    Args:
        credentials_path (str): Rayyan credentials path.
        rayyan_url (str, optional): Rayyan URL. Defaults to https://rayyan.ai.
            Set to an alternative URL if you are using a non-production Rayyan instance.

    """

    def__init__(
        self, credentials_path: str, rayyan_url: str = "https://rayyan.ai"
    ) -> None:
"""Initialize Rayyan reader."""
        fromrayyanimport Rayyan
        fromrayyan.userimport User

        logging.debug("Initializing Rayyan reader...")
        self.rayyan = Rayyan(credentials_path, url=rayyan_url)
        user = User(self.rayyan).get_info()
        logging.info(f"Signed in successfully to Rayyan as: {user['displayName']}!")

    defload_data(self, review_id: str, filters: dict = {}) -> List[Document]:
"""
        Load articles from a review.

        Args:
            review_id (int): Rayyan review ID.
            filters (dict, optional): Filters to apply to the review. Defaults to None. Passed to
                the Rayyan review results method as is.


        Returns:
            List[Document]: List of documents.

        """
        fromtenacityimport (
            retry,
            stop_after_attempt,
            stop_after_delay,
            stop_all,
            wait_random_exponential,
        )
        fromtqdmimport tqdm

        fromrayyan.reviewimport Review

        rayyan_review = Review(self.rayyan)
        my_review = rayyan_review.get(review_id)
        logging.info(
            f"Working on review: '{my_review['title']}' with {my_review['total_articles']} total articles."
        )

        result_params = {"start": 0, "length": 100}
        result_params.update(filters)

        @retry(
            wait=wait_random_exponential(min=1, max=10),
            stop=stop_all(stop_after_attempt(3), stop_after_delay(30)),
        )
        deffetch_results_with_retry():
            logging.debug("Fetch parameters: %s", result_params)
            return rayyan_review.results(review_id, result_params)

        articles = []
        logging.info("Fetching articles from Rayyan...")
        total = my_review["total_articles"]
        with tqdm(total=total) as pbar:
            while len(articles)  total:
                # retrieve articles in batches
                review_results = fetch_results_with_retry()
                fetched_articles = review_results["data"]
                articles.extend(fetched_articles)
                # update total in case filters are applied
                if total != review_results["recordsFiltered"]:
                    total = review_results["recordsFiltered"]
                    pbar.total = total
                result_params["start"] += len(fetched_articles)
                pbar.update(len(fetched_articles))

        results = []
        for article in articles:
            # iterate over all abstracts
            abstracts = ""
            if article["abstracts"] is not None:
                abstracts_arr = [
                    abstract["content"] for abstract in article["abstracts"]
                ]
                if len(abstracts_arr)  0:
                    # map array into a string
                    abstracts = "\n".join(abstracts_arr)[0:1024].strip()
            title = article["title"]
            if title is not None:
                title = title.strip()
            body = f"{title}\n{abstracts}"
            if body.strip() == "":
                continue
            extra_info = {"id": article["id"], "title": title}

            results.append(
                Document(
                    text=body,
                    extra_info=extra_info,
                )
            )

        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/rayyan/#llama_index.readers.rayyan.RayyanReader.load_data "Permanent link")

```
load_data(
    review_id: , filters:  = {}
) -> []

```

Load articles from a review.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `review_id`  |  Rayyan review ID.  |  _required_  |  
|  `filters`  |  `dict`  |  Filters to apply to the review. Defaults to None. Passed to the Rayyan review results method as is.  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: List of documents.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-rayyan/llama_index/readers/rayyan/base.py`  
| 
```
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
```
 | 
```
defload_data(self, review_id: str, filters: dict = {}) -> List[Document]:
"""
    Load articles from a review.

    Args:
        review_id (int): Rayyan review ID.
        filters (dict, optional): Filters to apply to the review. Defaults to None. Passed to
            the Rayyan review results method as is.


    Returns:
        List[Document]: List of documents.

    """
    fromtenacityimport (
        retry,
        stop_after_attempt,
        stop_after_delay,
        stop_all,
        wait_random_exponential,
    )
    fromtqdmimport tqdm

    fromrayyan.reviewimport Review

    rayyan_review = Review(self.rayyan)
    my_review = rayyan_review.get(review_id)
    logging.info(
        f"Working on review: '{my_review['title']}' with {my_review['total_articles']} total articles."
    )

    result_params = {"start": 0, "length": 100}
    result_params.update(filters)

    @retry(
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_all(stop_after_attempt(3), stop_after_delay(30)),
    )
    deffetch_results_with_retry():
        logging.debug("Fetch parameters: %s", result_params)
        return rayyan_review.results(review_id, result_params)

    articles = []
    logging.info("Fetching articles from Rayyan...")
    total = my_review["total_articles"]
    with tqdm(total=total) as pbar:
        while len(articles)  total:
            # retrieve articles in batches
            review_results = fetch_results_with_retry()
            fetched_articles = review_results["data"]
            articles.extend(fetched_articles)
            # update total in case filters are applied
            if total != review_results["recordsFiltered"]:
                total = review_results["recordsFiltered"]
                pbar.total = total
            result_params["start"] += len(fetched_articles)
            pbar.update(len(fetched_articles))

    results = []
    for article in articles:
        # iterate over all abstracts
        abstracts = ""
        if article["abstracts"] is not None:
            abstracts_arr = [
                abstract["content"] for abstract in article["abstracts"]
            ]
            if len(abstracts_arr)  0:
                # map array into a string
                abstracts = "\n".join(abstracts_arr)[0:1024].strip()
        title = article["title"]
        if title is not None:
            title = title.strip()
        body = f"{title}\n{abstracts}"
        if body.strip() == "":
            continue
        extra_info = {"id": article["id"], "title": title}

        results.append(
            Document(
                text=body,
                extra_info=extra_info,
            )
        )

    return results

```
 |  
| --- | --- |  
options: members: - RayyanReader
