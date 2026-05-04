# Microsoft outlook emails
##  OutlookEmailReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/microsoft_outlook_emails/#llama_index.readers.microsoft_outlook_emails.OutlookEmailReader "Permanent link")
Bases: 
Outlook Emails Reader using Microsoft Graph API.
Reads emails from a given Outlook mailbox and indexes the subject and body.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `client_id`  |  The Application ID for the app registered in Microsoft Azure.  |  _required_  |  
|  `client_secret`  |  The application secret for the app registered in Azure.  |  _required_  |  
|  `tenant_id`  |  Unique identifier of the Azure Active Directory Instance.  |  _required_  |  
|  `user_email`  |  Email address of the user whose emails need to be fetched.  |  _required_  |  
|  `folder`  |  `Optional[str]`  |  The email folder to fetch emails from. Defaults to "Inbox".  |  `'Inbox'`  |  
|  `num_mails`  |  Number of emails to retrieve. Defaults to 10.  |  
Source code in `llama-index-integrations/readers/llama-index-readers-microsoft-outlook-emails/llama_index/readers/microsoft_outlook_emails/base.py`  
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
```
 | 
```
classOutlookEmailReader(BasePydanticReader):
"""
    Outlook Emails Reader using Microsoft Graph API.

    Reads emails from a given Outlook mailbox and indexes the subject and body.

    Args:
        client_id (str): The Application ID for the app registered in Microsoft Azure.
        client_secret (str): The application secret for the app registered in Azure.
        tenant_id (str): Unique identifier of the Azure Active Directory Instance.
        user_email (str): Email address of the user whose emails need to be fetched.
        folder (Optional[str]): The email folder to fetch emails from. Defaults to "Inbox".
        num_mails (int): Number of emails to retrieve. Defaults to 10.

    """

    client_id: str
    client_secret: str
    tenant_id: str
    user_email: str
    folder: Optional[str] = "Inbox"
    num_mails: int = 10

    _authorization_headers: Optional[dict] = PrivateAttr(default=None)

    def__init__(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        user_email: str,
        folder: Optional[str] = "Inbox",
        num_mails: int = 10,
    ):
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
            user_email=user_email,
            folder=folder,
            num_mails=num_mails,
        )

    def_ensure_token(self):
"""Ensures we have a valid access token."""
        if self._authorization_headers is None:
            token = self._get_access_token()
            self._authorization_headers = {"Authorization": f"Bearer {token}"}

    def_get_access_token(self) -> str:
"""Fetches the OAuth token from Microsoft."""
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "resource": "https://graph.microsoft.com/",
        }
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")

    def_fetch_emails(self) -> List[dict]:
"""Fetches emails from the specified folder."""
        self._ensure_token()
        url = f"https://graph.microsoft.com/v1.0/users/{self.user_email}/mailFolders/{self.folder}/messages?$top={self.num_mails}"
        response = requests.get(url, headers=self._authorization_headers)
        response.raise_for_status()
        return response.json().get("value", [])

    defload_data(self) -> List[str]:
"""Loads emails as texts containing subject and body."""
        emails = self._fetch_emails()
        email_texts = []
        for email in emails:
            subject = email.get("subject", "No Subject")
            body = email.get("body", {}).get("content", "No Content")
            email_texts.append(f"Subject: {subject}\n\n{body}")
        return email_texts

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/microsoft_outlook_emails/#llama_index.readers.microsoft_outlook_emails.OutlookEmailReader.load_data "Permanent link")

```
load_data() -> []

```

Loads emails as texts containing subject and body.
Source code in `llama-index-integrations/readers/llama-index-readers-microsoft-outlook-emails/llama_index/readers/microsoft_outlook_emails/base.py`  
| 
```
80
81
82
83
84
85
86
87
88
```
 | 
```
defload_data(self) -> List[str]:
"""Loads emails as texts containing subject and body."""
    emails = self._fetch_emails()
    email_texts = []
    for email in emails:
        subject = email.get("subject", "No Subject")
        body = email.get("body", {}).get("content", "No Content")
        email_texts.append(f"Subject: {subject}\n\n{body}")
    return email_texts

```
 |  
| --- | --- |  
options: members: - OutlookEmailReader
