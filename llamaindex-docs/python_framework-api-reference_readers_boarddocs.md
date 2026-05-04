# Boarddocs
##  BoardDocsReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/boarddocs/#llama_index.readers.boarddocs.BoardDocsReader "Permanent link")
Bases: 
BoardDocs doc reader.
Read public agendas included on a BoardDocs site.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `site`  |  The BoardDocs site you'd like to index, e.g. "ca/redwood"  |  _required_  |  
|  `committee_id`  |  The committee on the site you want to index  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-boarddocs/llama_index/readers/boarddocs/base.py`  
| 
```
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
```
 | 
```
classBoardDocsReader(BaseReader):
"""
    BoardDocs doc reader.

    Read public agendas included on a BoardDocs site.

    Args:
        site (str): The BoardDocs site you'd like to index, e.g. "ca/redwood"
        committee_id (str): The committee on the site you want to index

    """

    def__init__(
        self,
        site: str,
        committee_id: str,
    ) -> None:
"""Initialize with parameters."""
        self.site = site
        self.committee_id = committee_id
        self.base_url = "https://go.boarddocs.com/" + site + "/Board.nsf"

        # set up the headers required for the server to answer
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": (
                '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"'
            ),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
        }
        super().__init__()

    defget_meeting_list(self) -> List[dict]:
"""
        Returns a list of meetings for the committee.

        Args:
            None
        Returns:
            List[dict]: A list of meetings, each with a meetingID, date, and unid

        """
        meeting_list_url = self.base_url + "/BD-GetMeetingsList?open"

        data = "current_committee_id=" + self.committee_id
        response = requests.post(meeting_list_url, headers=self.headers, data=data)
        meetingsData = json.loads(response.text)

        return [
            {
                "meetingID": meeting.get("unique", None),
                "date": meeting.get("numberdate", None),
                "unid": meeting.get("unid", None),
            }
            for meeting in meetingsData
        ]

    defprocess_meeting(
        self, meeting_id: str, index_pdfs: bool = True
    ) -> List[Document]:
"""
        Returns documents from the given meeting.
        """
        agenda_url = self.base_url + "/PRINT-AgendaDetailed"

        # set the meetingID & committee
        data = "id=" + meeting_id + "&" + "current_committee_id=" + self.committee_id

        # POST the request!
        response = requests.post(agenda_url, headers=self.headers, data=data)

        # parse the returned HTML
        soup = BeautifulSoup(response.content, "html.parser")
        agenda_date = soup.find("div", {"class": "print-meeting-date"}).string
        agenda_title = soup.find("div", {"class": "print-meeting-name"}).string
        [fd.a.get("href") for fd in soup.find_all("div", {"class": "public-file"})]
        agenda_data = html2text.html2text(response.text)

        # TODO: index the linked PDFs in agenda_files!

        docs = []
        agenda_doc = Document(
            text=agenda_data,
            doc_id=meeting_id,
            extra_info={
                "committee": self.committee_id,
                "title": agenda_title,
                "date": agenda_date,
                "url": agenda_url,
            },
        )
        docs.append(agenda_doc)
        return docs

    defload_data(
        self, meeting_ids: Optional[List[str]] = None, **load_kwargs: Any
    ) -> List[Document]:
"""
        Load all meetings of the committee.

        Args:
            meeting_ids (List[str]): A list of meeting IDs to load. If None, load all meetings.

        """
        # if a list of meetings wasn't provided, enumerate them all
        if not meeting_ids:
            meeting_ids = [
                meeting.get("meetingID") for meeting in self.get_meeting_list()
            ]

        # process all relevant meetings & return the documents
        docs = []
        for meeting_id in meeting_ids:
            docs.extend(self.process_meeting(meeting_id))
        return docs

```
 |  
| --- | --- |  
###  get_meeting_list [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/boarddocs/#llama_index.readers.boarddocs.BoardDocsReader.get_meeting_list "Permanent link")

```
get_meeting_list() -> []

```

Returns a list of meetings for the committee.
Returns: List[dict]: A list of meetings, each with a meetingID, date, and unid
Source code in `llama-index-integrations/readers/llama-index-readers-boarddocs/llama_index/readers/boarddocs/base.py`  
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
```
 | 
```
defget_meeting_list(self) -> List[dict]:
"""
    Returns a list of meetings for the committee.

    Args:
        None
    Returns:
        List[dict]: A list of meetings, each with a meetingID, date, and unid

    """
    meeting_list_url = self.base_url + "/BD-GetMeetingsList?open"

    data = "current_committee_id=" + self.committee_id
    response = requests.post(meeting_list_url, headers=self.headers, data=data)
    meetingsData = json.loads(response.text)

    return [
        {
            "meetingID": meeting.get("unique", None),
            "date": meeting.get("numberdate", None),
            "unid": meeting.get("unid", None),
        }
        for meeting in meetingsData
    ]

```
 |  
| --- | --- |  
###  process_meeting [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/boarddocs/#llama_index.readers.boarddocs.BoardDocsReader.process_meeting "Permanent link")

```
process_meeting(
    meeting_id: , index_pdfs:  = True
) -> []

```

Returns documents from the given meeting.
Source code in `llama-index-integrations/readers/llama-index-readers-boarddocs/llama_index/readers/boarddocs/base.py`  
| 
```
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
```
 | 
```
defprocess_meeting(
    self, meeting_id: str, index_pdfs: bool = True
) -> List[Document]:
"""
    Returns documents from the given meeting.
    """
    agenda_url = self.base_url + "/PRINT-AgendaDetailed"

    # set the meetingID & committee
    data = "id=" + meeting_id + "&" + "current_committee_id=" + self.committee_id

    # POST the request!
    response = requests.post(agenda_url, headers=self.headers, data=data)

    # parse the returned HTML
    soup = BeautifulSoup(response.content, "html.parser")
    agenda_date = soup.find("div", {"class": "print-meeting-date"}).string
    agenda_title = soup.find("div", {"class": "print-meeting-name"}).string
    [fd.a.get("href") for fd in soup.find_all("div", {"class": "public-file"})]
    agenda_data = html2text.html2text(response.text)

    # TODO: index the linked PDFs in agenda_files!

    docs = []
    agenda_doc = Document(
        text=agenda_data,
        doc_id=meeting_id,
        extra_info={
            "committee": self.committee_id,
            "title": agenda_title,
            "date": agenda_date,
            "url": agenda_url,
        },
    )
    docs.append(agenda_doc)
    return docs

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/boarddocs/#llama_index.readers.boarddocs.BoardDocsReader.load_data "Permanent link")

```
load_data(
    meeting_ids: Optional[[]] = None,
    **load_kwargs: 
) -> []

```

Load all meetings of the committee.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `meeting_ids`  |  `List[str]`  |  A list of meeting IDs to load. If None, load all meetings.  |  `None`  |  
Source code in `llama-index-integrations/readers/llama-index-readers-boarddocs/llama_index/readers/boarddocs/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, meeting_ids: Optional[List[str]] = None, **load_kwargs: Any
) -> List[Document]:
"""
    Load all meetings of the committee.

    Args:
        meeting_ids (List[str]): A list of meeting IDs to load. If None, load all meetings.

    """
    # if a list of meetings wasn't provided, enumerate them all
    if not meeting_ids:
        meeting_ids = [
            meeting.get("meetingID") for meeting in self.get_meeting_list()
        ]

    # process all relevant meetings & return the documents
    docs = []
    for meeting_id in meeting_ids:
        docs.extend(self.process_meeting(meeting_id))
    return docs

```
 |  
| --- | --- |  
options: members: - BoardDocsReader
