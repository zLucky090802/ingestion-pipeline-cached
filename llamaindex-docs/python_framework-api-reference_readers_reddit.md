# Reddit
##  RedditReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/reddit/#llama_index.readers.reddit.RedditReader "Permanent link")
Bases: 
Subreddit post and top-level comments reader for Reddit.
Source code in `llama-index-integrations/readers/llama-index-readers-reddit/llama_index/readers/reddit/base.py`  
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
```
 | 
```
classRedditReader(BaseReader):
"""
    Subreddit post and top-level comments reader for Reddit.
    """

    defload_data(
        self,
        subreddits: List[str],
        search_keys: List[str],
        post_limit: Optional[int] = [10],
    ) -> List[Document]:
"""
        Load text from relevant posts and top-level comments in subreddit(s), given keyword(s) for search.

        Args:
            subreddits (List[str]): List of subreddits you'd like to read from
            search_keys (List[str]): List of keywords you'd like to use to search from subreddit(s)
            post_limit (Optional[int]): Maximum number of posts per subreddit you'd like to read from, defaults to 10

        """
        importos

        importpraw
        frompraw.modelsimport MoreComments

        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
        )

        posts = []

        for sr in subreddits:
            ml_subreddit = reddit.subreddit(sr)

            for kw in search_keys:
                relevant_posts = ml_subreddit.search(kw, limit=post_limit)

                for post in relevant_posts:
                    posts.append(Document(text=post.selftext))
                    for top_level_comment in post.comments:
                        if isinstance(top_level_comment, MoreComments):
                            continue
                        posts.append(Document(text=top_level_comment.body))

        return posts

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/reddit/#llama_index.readers.reddit.RedditReader.load_data "Permanent link")

```
load_data(
    subreddits: [],
    search_keys: [],
    post_limit: Optional[] = [10],
) -> []

```

Load text from relevant posts and top-level comments in subreddit(s), given keyword(s) for search.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `subreddits`  |  `List[str]`  |  List of subreddits you'd like to read from  |  _required_  |  
|  `search_keys`  |  `List[str]`  |  List of keywords you'd like to use to search from subreddit(s)  |  _required_  |  
|  `post_limit`  |  `Optional[int]`  |  Maximum number of posts per subreddit you'd like to read from, defaults to 10  |  `[10]`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-reddit/llama_index/readers/reddit/base.py`  
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
```
 | 
```
defload_data(
    self,
    subreddits: List[str],
    search_keys: List[str],
    post_limit: Optional[int] = [10],
) -> List[Document]:
"""
    Load text from relevant posts and top-level comments in subreddit(s), given keyword(s) for search.

    Args:
        subreddits (List[str]): List of subreddits you'd like to read from
        search_keys (List[str]): List of keywords you'd like to use to search from subreddit(s)
        post_limit (Optional[int]): Maximum number of posts per subreddit you'd like to read from, defaults to 10

    """
    importos

    importpraw
    frompraw.modelsimport MoreComments

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )

    posts = []

    for sr in subreddits:
        ml_subreddit = reddit.subreddit(sr)

        for kw in search_keys:
            relevant_posts = ml_subreddit.search(kw, limit=post_limit)

            for post in relevant_posts:
                posts.append(Document(text=post.selftext))
                for top_level_comment in post.comments:
                    if isinstance(top_level_comment, MoreComments):
                        continue
                    posts.append(Document(text=top_level_comment.body))

    return posts

```
 |  
| --- | --- |  
options: members: - RedditReader
