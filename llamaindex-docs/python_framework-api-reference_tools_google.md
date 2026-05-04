# Google
##  GoogleCalendarToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GoogleCalendarToolSpec "Permanent link")
Bases: 
Google Calendar tool spec.
Currently a simple wrapper around the data loader. TODO: add more methods to the Google Calendar spec.
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/calendar/base.py`  
| 
```
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
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
```
 | 
```
classGoogleCalendarToolSpec(BaseToolSpec):
"""
    Google Calendar tool spec.

    Currently a simple wrapper around the data loader.
    TODO: add more methods to the Google Calendar spec.

    """

    spec_functions = ["load_data", "create_event", "get_date"]

    def__init__(
        self,
        creds: Optional[Any] = None,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
        service_account_key_path: str = "service_account_key.json",
        service_account_key: Optional[dict] = None,
        authorized_user_info: Optional[dict] = None,
        is_cloud: bool = False,
    ):
"""
        Initialize the GoogleCalendarToolSpec.

        Args:
            creds (Optional[Any]): Pre-configured credentials to use for authentication.
                                 If provided, these will be used instead of the OAuth flow.
            credentials_path (str): Path to the OAuth client secrets file.
            token_path (str): Path to the token file for storing user credentials.
            service_account_key_path (str): Path to the service account key JSON file.
            service_account_key (Optional[dict]): Service account key info as a dict.
            authorized_user_info (Optional[dict]): Authorized user info as a dict.
            is_cloud (bool): If True, skip writing token file to disk.

        """
        self.creds = creds
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service_account_key_path = service_account_key_path
        self.service_account_key = service_account_key
        self.authorized_user_info = authorized_user_info
        self.is_cloud = is_cloud
        self.service = None

    def_cache_service(self) -> None:
        if self.service:
            return
        fromgoogleapiclient.discoveryimport build

        credentials = self._get_credentials()
        self.service = build("calendar", "v3", credentials=credentials)

    defload_data(
        self,
        number_of_results: Optional[int] = 100,
        start_date: Optional[Union[str, datetime.date]] = None,
    ) -> List[Document]:
"""
        Load data from user's calendar.

        Args:
            number_of_results (Optional[int]): the number of events to return. Defaults to 100.
            start_date (Optional[Union[str, datetime.date]]): the start date to return events from in date isoformat. Defaults to today.

        """
        self._cache_service()

        if start_date is None:
            start_date = datetime.date.today()
        elif isinstance(start_date, str):
            start_date = datetime.date.fromisoformat(start_date)

        start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
        start_datetime_utc = start_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=start_datetime_utc,
                maxResults=number_of_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            return []

        results = []
        for event in events:
            if "dateTime" in event["start"]:
                start_time = event["start"]["dateTime"]
            else:
                start_time = event["start"]["date"]

            if "dateTime" in event["end"]:
                end_time = event["end"]["dateTime"]
            else:
                end_time = event["end"]["date"]

            event_string = f"Status: {event['status']}, "
            event_string += f"Summary: {event['summary']}, "
            event_string += f"Start time: {start_time}, "
            event_string += f"End time: {end_time}, "

            organizer = event.get("organizer", {})
            display_name = organizer.get("displayName", "N/A")
            email = organizer.get("email", "N/A")
            if display_name != "N/A":
                event_string += f"Organizer: {display_name} ({email})"
            else:
                event_string += f"Organizer: {email}"

            results.append(Document(text=event_string))

        return results

    def_get_credentials(self) -> Any:
"""
        Get valid user credentials from storage.

        Credential resolution order:
        1. Pre-built ``creds`` passed to the constructor.
        2. ``service_account_key`` dict.
        3. ``service_account_key_path`` file.
        4. ``authorized_user_info`` dict.
        5. ``token_path`` file (stored OAuth tokens).
        6. ``InstalledAppFlow`` from ``credentials_path`` (desktop OAuth).

        Returns:
            Credentials, the obtained credential.

        """
        if self.creds is not None:
            return self.creds

        fromgoogle.auth.transport.requestsimport Request
        fromgoogle.oauth2import service_account as sa
        fromgoogle.oauth2.credentialsimport Credentials
        fromgoogle_auth_oauthlib.flowimport InstalledAppFlow

        if self.service_account_key is not None:
            return sa.Credentials.from_service_account_info(
                self.service_account_key, scopes=SCOPES
            )

        if os.path.isfile(self.service_account_key_path):
            with open(self.service_account_key_path, encoding="utf-8") as f:
                sa_key = json.load(f)
            return sa.Credentials.from_service_account_info(sa_key, scopes=SCOPES)

        creds = None
        if self.authorized_user_info is not None:
            creds = Credentials.from_authorized_user_info(
                self.authorized_user_info, SCOPES
            )
        elif os.path.isfile(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            if not self.is_cloud:
                with open(self.token_path, "w") as token:
                    token.write(creds.to_json())

        return creds

    defcreate_event(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        start_datetime: Optional[Union[str, datetime.datetime]] = None,
        end_datetime: Optional[Union[str, datetime.datetime]] = None,
        attendees: Optional[List[str]] = None,
    ) -> str:
"""
            Create an event on the users calendar.

        Args:
            title (Optional[str]): The title for the event
            description (Optional[str]): The description for the event
            location (Optional[str]): The location for the event
            start_datetime Optional[Union[str, datetime.datetime]]: The start datetime for the event
            end_datetime Optional[Union[str, datetime.datetime]]: The end datetime for the event
            attendees Optional[List[str]]: A list of email address to invite to the event

        """
        self._cache_service()

        attendees_list = (
            [{"email": attendee} for attendee in attendees] if attendees else []
        )

        start_time = (
            datetime.datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S%z")
            .astimezone()
            .strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        )
        end_time = (
            datetime.datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S%z")
            .astimezone()
            .strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        )

        event = {
            "summary": title,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
            },
            "end": {
                "dateTime": end_time,
            },
            "attendees": attendees_list,
        }
        event = self.service.events().insert(calendarId="primary", body=event).execute()
        return (
            "Your calendar event has been created successfully! You can move on to the"
            " next step."
        )

    defget_date(self):
"""
        A function to return todays date. Call this before any other functions if you are unaware of the date.
        """
        return datetime.date.today()

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GoogleCalendarToolSpec.load_data "Permanent link")

```
load_data(
    number_of_results: Optional[] = 100,
    start_date: Optional[Union[, ]] = None,
) -> []

```

Load data from user's calendar.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `number_of_results`  |  `Optional[int]`  |  the number of events to return. Defaults to 100.  |  `100`  |  
|  `start_date`  |  `Optional[Union[str, date]]`  |  the start date to return events from in date isoformat. Defaults to today.  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/calendar/base.py`  
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
146
147
```
 | 
```
defload_data(
    self,
    number_of_results: Optional[int] = 100,
    start_date: Optional[Union[str, datetime.date]] = None,
) -> List[Document]:
"""
    Load data from user's calendar.

    Args:
        number_of_results (Optional[int]): the number of events to return. Defaults to 100.
        start_date (Optional[Union[str, datetime.date]]): the start date to return events from in date isoformat. Defaults to today.

    """
    self._cache_service()

    if start_date is None:
        start_date = datetime.date.today()
    elif isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)

    start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
    start_datetime_utc = start_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    events_result = (
        self.service.events()
        .list(
            calendarId="primary",
            timeMin=start_datetime_utc,
            maxResults=number_of_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    if not events:
        return []

    results = []
    for event in events:
        if "dateTime" in event["start"]:
            start_time = event["start"]["dateTime"]
        else:
            start_time = event["start"]["date"]

        if "dateTime" in event["end"]:
            end_time = event["end"]["dateTime"]
        else:
            end_time = event["end"]["date"]

        event_string = f"Status: {event['status']}, "
        event_string += f"Summary: {event['summary']}, "
        event_string += f"Start time: {start_time}, "
        event_string += f"End time: {end_time}, "

        organizer = event.get("organizer", {})
        display_name = organizer.get("displayName", "N/A")
        email = organizer.get("email", "N/A")
        if display_name != "N/A":
            event_string += f"Organizer: {display_name} ({email})"
        else:
            event_string += f"Organizer: {email}"

        results.append(Document(text=event_string))

    return results

```
 |  
| --- | --- |  
###  create_event [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GoogleCalendarToolSpec.create_event "Permanent link")

```
create_event(
    title: Optional[] = None,
    description: Optional[] = None,
    location: Optional[] = None,
    start_datetime: Optional[Union[, datetime]] = None,
    end_datetime: Optional[Union[, datetime]] = None,
    attendees: Optional[[]] = None,
) -> 

```


```
Create an event on the users calendar.

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `title`  |  `Optional[str]`  |  The title for the event  |  `None`  |  
|  `description`  |  `Optional[str]`  |  The description for the event  |  `None`  |  
|  `location`  |  `Optional[str]`  |  The location for the event  |  `None`  |  
|  `start_datetime Optional[Union[str, datetime.datetime]]`  |  The start datetime for the event  |  _required_  |  
|  `end_datetime Optional[Union[str, datetime.datetime]]`  |  The end datetime for the event  |  _required_  |  
|  `attendees Optional[List[str]]`  |  A list of email address to invite to the event  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/calendar/base.py`  
| 
```
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
```
 | 
```
defcreate_event(
    self,
    title: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    start_datetime: Optional[Union[str, datetime.datetime]] = None,
    end_datetime: Optional[Union[str, datetime.datetime]] = None,
    attendees: Optional[List[str]] = None,
) -> str:
"""
        Create an event on the users calendar.

    Args:
        title (Optional[str]): The title for the event
        description (Optional[str]): The description for the event
        location (Optional[str]): The location for the event
        start_datetime Optional[Union[str, datetime.datetime]]: The start datetime for the event
        end_datetime Optional[Union[str, datetime.datetime]]: The end datetime for the event
        attendees Optional[List[str]]: A list of email address to invite to the event

    """
    self._cache_service()

    attendees_list = (
        [{"email": attendee} for attendee in attendees] if attendees else []
    )

    start_time = (
        datetime.datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S%z")
        .astimezone()
        .strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    )
    end_time = (
        datetime.datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S%z")
        .astimezone()
        .strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    )

    event = {
        "summary": title,
        "location": location,
        "description": description,
        "start": {
            "dateTime": start_time,
        },
        "end": {
            "dateTime": end_time,
        },
        "attendees": attendees_list,
    }
    event = self.service.events().insert(calendarId="primary", body=event).execute()
    return (
        "Your calendar event has been created successfully! You can move on to the"
        " next step."
    )

```
 |  
| --- | --- |  
###  get_date [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GoogleCalendarToolSpec.get_date "Permanent link")

```
get_date()

```

A function to return todays date. Call this before any other functions if you are unaware of the date.
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/calendar/base.py`  
| 
```
263
264
265
266
267
```
 | 
```
defget_date(self):
"""
    A function to return todays date. Call this before any other functions if you are unaware of the date.
    """
    return datetime.date.today()

```
 |  
| --- | --- |  
##  GmailToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GmailToolSpec "Permanent link")
Bases: 
GMail tool spec.
Gives the agent the ability to read, draft and send gmail messages
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/gmail/base.py`  
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
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
```
 | 
```
classGmailToolSpec(BaseToolSpec):
"""
    GMail tool spec.

    Gives the agent the ability to read, draft and send gmail messages

    """

    spec_functions = [
        "load_data",
        "search_messages",
        "create_draft",
        "update_draft",
        "get_draft",
        "send_draft",
    ]
    query: str = None
    use_iterative_parser: bool = False
    max_results: int = 10
    service: Any = None

    def__init__(
        self,
        creds: Optional[Any] = None,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
        service_account_key_path: str = "service_account_key.json",
        service_account_key: Optional[dict] = None,
        authorized_user_info: Optional[dict] = None,
        is_cloud: bool = False,
    ):
"""
        Initialize the GmailToolSpec.

        Args:
            creds (Optional[Any]): Pre-configured credentials to use for authentication.
                                 If provided, these will be used instead of the OAuth flow.
            credentials_path (str): Path to the OAuth client secrets file.
            token_path (str): Path to the token file for storing user credentials.
            service_account_key_path (str): Path to the service account key JSON file.
            service_account_key (Optional[dict]): Service account key info as a dict.
            authorized_user_info (Optional[dict]): Authorized user info as a dict.
            is_cloud (bool): If True, skip writing token file to disk.

        """
        self.creds = creds
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service_account_key_path = service_account_key_path
        self.service_account_key = service_account_key
        self.authorized_user_info = authorized_user_info
        self.is_cloud = is_cloud

    def_cache_service(self) -> None:
        if self.service:
            return
        fromgoogleapiclient.discoveryimport build

        credentials = self._get_credentials()
        self.service = build("gmail", "v1", credentials=credentials)

    defload_data(self) -> List[Document]:
"""Load emails from the user's account."""
        self._cache_service()

        return self.search_messages(query="")

    def_get_credentials(self) -> Any:
"""
        Get valid user credentials from storage.

        Credential resolution order:
        1. Pre-built ``creds`` passed to the constructor.
        2. ``service_account_key`` dict.
        3. ``service_account_key_path`` file.
        4. ``authorized_user_info`` dict.
        5. ``token_path`` file (stored OAuth tokens).
        6. ``InstalledAppFlow`` from ``credentials_path`` (desktop OAuth).

        Returns:
            Credentials, the obtained credential.

        """
        if self.creds is not None:
            return self.creds

        fromgoogle.auth.transport.requestsimport Request
        fromgoogle.oauth2import service_account as sa
        fromgoogle.oauth2.credentialsimport Credentials
        fromgoogle_auth_oauthlib.flowimport InstalledAppFlow

        if self.service_account_key is not None:
            return sa.Credentials.from_service_account_info(
                self.service_account_key, scopes=SCOPES
            )

        if os.path.isfile(self.service_account_key_path):
            with open(self.service_account_key_path, encoding="utf-8") as f:
                sa_key = json.load(f)
            return sa.Credentials.from_service_account_info(sa_key, scopes=SCOPES)

        creds = None
        if self.authorized_user_info is not None:
            creds = Credentials.from_authorized_user_info(
                self.authorized_user_info, SCOPES
            )
        elif os.path.isfile(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            if not self.is_cloud:
                with open(self.token_path, "w") as token:
                    token.write(creds.to_json())

        return creds

    defsearch_messages(self, query: str, max_results: Optional[int] = None):
"""
        Searches email messages given a query string and the maximum number
        of results requested by the user
           Returns: List of relevant message objects up to the maximum number of results.

        Args:
            query (str): The user's query
            max_results (Optional[int]): The maximum number of search results
            to return.

        """
        if not max_results:
            max_results = self.max_results

        self._cache_service()

        messages = (
            self.service.users()
            .messages()
            .list(userId="me", q=query or None, maxResults=int(max_results))
            .execute()
            .get("messages", [])
        )

        results = []
        try:
            for message in messages:
                message_data = self.get_message_data(message)
                text = message_data.pop("body")
                metadata = message_data
                results.append(Document(text=text, metadata=metadata))
        except Exception as e:
            raise Exception("Can't get message data" + str(e))

        return results

    defget_message_data(self, message):
        message_id = message["id"]
        message_data = (
            self.service.users()
            .messages()
            .get(format="raw", userId="me", id=message_id)
            .execute()
        )
        if self.use_iterative_parser:
            body = self.extract_message_body_iterative(message_data)
        else:
            body = self.extract_message_body(message_data)

        if not body:
            return None

        return {
            "id": message_data["id"],
            "threadId": message_data["threadId"],
            "snippet": message_data["snippet"],
            "body": body,
        }

    defextract_message_body_iterative(self, message: dict):
        if message["raw"]:
            body = base64.urlsafe_b64decode(message["raw"].encode("utf8"))
            mime_msg = email.message_from_bytes(body)
        else:
            mime_msg = message

        body_text = ""
        if mime_msg.get_content_type() == "text/plain":
            plain_text = mime_msg.get_payload(decode=True)
            charset = mime_msg.get_content_charset("utf-8")
            body_text = plain_text.decode(charset).encode("utf-8").decode("utf-8")

        elif mime_msg.get_content_maintype() == "multipart":
            msg_parts = mime_msg.get_payload()
            for msg_part in msg_parts:
                body_text += self.extract_message_body_iterative(msg_part)

        return body_text

    defextract_message_body(self, message: dict):
        frombs4import BeautifulSoup

        try:
            body = base64.urlsafe_b64decode(message["raw"].encode("utf-8"))
            mime_msg = email.message_from_bytes(body)

            # If the message body contains HTML, parse it with BeautifulSoup
            if "text/html" in mime_msg:
                soup = BeautifulSoup(body, "html.parser")
                body = soup.get_text()
            return body.decode("utf-8")
        except Exception as e:
            raise Exception("Can't parse message body" + str(e))

    def_build_draft(
        self,
        to: Optional[List[str]] = None,
        subject: Optional[str] = None,
        message: Optional[str] = None,
    ) -> str:
        email_message = EmailMessage()

        email_message.set_content(message)

        email_message["To"] = to
        email_message["Subject"] = subject

        encoded_message = base64.urlsafe_b64encode(email_message.as_bytes()).decode()

        return {"message": {"raw": encoded_message}}

    defcreate_draft(
        self,
        to: Optional[List[str]] = None,
        subject: Optional[str] = None,
        message: Optional[str] = None,
    ) -> str:
"""
        Create and insert a draft email.
           Print the returned draft's message and id.
           Returns: Draft object, including draft id and message meta data.

        Args:
            to (Optional[str]): The email addresses to send the message to
            subject (Optional[str]): The subject for the event
            message (Optional[str]): The message for the event

        """
        self._cache_service()
        service = self.service

        return (
            service.users()
            .drafts()
            .create(userId="me", body=self._build_draft(to, subject, message))
            .execute()
        )

    defupdate_draft(
        self,
        to: Optional[List[str]] = None,
        subject: Optional[str] = None,
        message: Optional[str] = None,
        draft_id: str = None,
    ) -> str:
"""
        Update a draft email.
           Print the returned draft's message and id.
           This function is required to be passed a draft_id that is obtained when creating messages
           Returns: Draft object, including draft id and message meta data.

        Args:
            to (Optional[str]): The email addresses to send the message to
            subject (Optional[str]): The subject for the event
            message (Optional[str]): The message for the event
            draft_id (str): the id of the draft to be updated

        """
        self._cache_service()
        service = self.service

        if draft_id is None:
            return (
                "You did not provide a draft id when calling this function. If you"
                " previously created or retrieved the draft, the id is available in"
                " context"
            )

        draft = self.get_draft(draft_id)
        headers = draft["message"]["payload"]["headers"]
        for header in headers:
            if header["name"] == "To" and not to:
                to = header["value"]
            elif header["name"] == "Subject" and not subject:
                subject = header["value"]

        return (
            service.users()
            .drafts()
            .update(
                userId="me", id=draft_id, body=self._build_draft(to, subject, message)
            )
            .execute()
        )

    defget_draft(self, draft_id: str = None) -> str:
"""
        Get a draft email.
           Print the returned draft's message and id.
           Returns: Draft object, including draft id and message meta data.

        Args:
            draft_id (str): the id of the draft to be updated

        """
        self._cache_service()
        service = self.service
        return service.users().drafts().get(userId="me", id=draft_id).execute()

    defsend_draft(self, draft_id: str = None) -> str:
"""
        Sends a draft email.
           Print the returned draft's message and id.
           Returns: Draft object, including draft id and message meta data.

        Args:
            draft_id (str): the id of the draft to be updated

        """
        self._cache_service()
        service = self.service
        return (
            service.users().drafts().send(userId="me", body={"id": draft_id}).execute()
        )

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GmailToolSpec.load_data "Permanent link")

```
load_data() -> []

```

Load emails from the user's account.
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/gmail/base.py`  
| 
```
80
81
82
83
84
```
 | 
```
defload_data(self) -> List[Document]:
"""Load emails from the user's account."""
    self._cache_service()

    return self.search_messages(query="")

```
 |  
| --- | --- |  
###  search_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GmailToolSpec.search_messages "Permanent link")

```
search_messages(
    query: , max_results: Optional[] = None
)

```

Searches email messages given a query string and the maximum number of results requested by the user Returns: List of relevant message objects up to the maximum number of results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The user's query  |  _required_  |  
|  `max_results`  |  `Optional[int]`  |  The maximum number of search results  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/gmail/base.py`  
| 
```
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
```
 | 
```
defsearch_messages(self, query: str, max_results: Optional[int] = None):
"""
    Searches email messages given a query string and the maximum number
    of results requested by the user
       Returns: List of relevant message objects up to the maximum number of results.

    Args:
        query (str): The user's query
        max_results (Optional[int]): The maximum number of search results
        to return.

    """
    if not max_results:
        max_results = self.max_results

    self._cache_service()

    messages = (
        self.service.users()
        .messages()
        .list(userId="me", q=query or None, maxResults=int(max_results))
        .execute()
        .get("messages", [])
    )

    results = []
    try:
        for message in messages:
            message_data = self.get_message_data(message)
            text = message_data.pop("body")
            metadata = message_data
            results.append(Document(text=text, metadata=metadata))
    except Exception as e:
        raise Exception("Can't get message data" + str(e))

    return results

```
 |  
| --- | --- |  
###  create_draft [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GmailToolSpec.create_draft "Permanent link")

```
create_draft(
    to: Optional[[]] = None,
    subject: Optional[] = None,
    message: Optional[] = None,
) -> 

```

Create and insert a draft email. Print the returned draft's message and id. Returns: Draft object, including draft id and message meta data.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `Optional[str]`  |  The email addresses to send the message to  |  `None`  |  
|  `subject`  |  `Optional[str]`  |  The subject for the event  |  `None`  |  
|  `message`  |  `Optional[str]`  |  The message for the event  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/gmail/base.py`  
| 
```
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
```
 | 
```
defcreate_draft(
    self,
    to: Optional[List[str]] = None,
    subject: Optional[str] = None,
    message: Optional[str] = None,
) -> str:
"""
    Create and insert a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

    Args:
        to (Optional[str]): The email addresses to send the message to
        subject (Optional[str]): The subject for the event
        message (Optional[str]): The message for the event

    """
    self._cache_service()
    service = self.service

    return (
        service.users()
        .drafts()
        .create(userId="me", body=self._build_draft(to, subject, message))
        .execute()
    )

```
 |  
| --- | --- |  
###  update_draft [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GmailToolSpec.update_draft "Permanent link")

```
update_draft(
    to: Optional[[]] = None,
    subject: Optional[] = None,
    message: Optional[] = None,
    draft_id:  = None,
) -> 

```

Update a draft email. Print the returned draft's message and id. This function is required to be passed a draft_id that is obtained when creating messages Returns: Draft object, including draft id and message meta data.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `Optional[str]`  |  The email addresses to send the message to  |  `None`  |  
|  `subject`  |  `Optional[str]`  |  The subject for the event  |  `None`  |  
|  `message`  |  `Optional[str]`  |  The message for the event  |  `None`  |  
|  `draft_id`  |  the id of the draft to be updated  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/gmail/base.py`  
| 
```
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
```
 | 
```
defupdate_draft(
    self,
    to: Optional[List[str]] = None,
    subject: Optional[str] = None,
    message: Optional[str] = None,
    draft_id: str = None,
) -> str:
"""
    Update a draft email.
       Print the returned draft's message and id.
       This function is required to be passed a draft_id that is obtained when creating messages
       Returns: Draft object, including draft id and message meta data.

    Args:
        to (Optional[str]): The email addresses to send the message to
        subject (Optional[str]): The subject for the event
        message (Optional[str]): The message for the event
        draft_id (str): the id of the draft to be updated

    """
    self._cache_service()
    service = self.service

    if draft_id is None:
        return (
            "You did not provide a draft id when calling this function. If you"
            " previously created or retrieved the draft, the id is available in"
            " context"
        )

    draft = self.get_draft(draft_id)
    headers = draft["message"]["payload"]["headers"]
    for header in headers:
        if header["name"] == "To" and not to:
            to = header["value"]
        elif header["name"] == "Subject" and not subject:
            subject = header["value"]

    return (
        service.users()
        .drafts()
        .update(
            userId="me", id=draft_id, body=self._build_draft(to, subject, message)
        )
        .execute()
    )

```
 |  
| --- | --- |  
###  get_draft [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GmailToolSpec.get_draft "Permanent link")

```
get_draft(draft_id:  = None) -> 

```

Get a draft email. Print the returned draft's message and id. Returns: Draft object, including draft id and message meta data.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `draft_id`  |  the id of the draft to be updated  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/gmail/base.py`  
| 
```
330
331
332
333
334
335
336
337
338
339
340
341
342
```
 | 
```
defget_draft(self, draft_id: str = None) -> str:
"""
    Get a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

    Args:
        draft_id (str): the id of the draft to be updated

    """
    self._cache_service()
    service = self.service
    return service.users().drafts().get(userId="me", id=draft_id).execute()

```
 |  
| --- | --- |  
###  send_draft [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GmailToolSpec.send_draft "Permanent link")

```
send_draft(draft_id:  = None) -> 

```

Sends a draft email. Print the returned draft's message and id. Returns: Draft object, including draft id and message meta data.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `draft_id`  |  the id of the draft to be updated  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/gmail/base.py`  
| 
```
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
```
 | 
```
defsend_draft(self, draft_id: str = None) -> str:
"""
    Sends a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

    Args:
        draft_id (str): the id of the draft to be updated

    """
    self._cache_service()
    service = self.service
    return (
        service.users().drafts().send(userId="me", body={"id": draft_id}).execute()
    )

```
 |  
| --- | --- |  
##  GoogleSearchToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GoogleSearchToolSpec "Permanent link")
Bases: 
Google Search tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/search/base.py`  
| 
```
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
```
 | 
```
classGoogleSearchToolSpec(BaseToolSpec):
"""Google Search tool spec."""

    spec_functions = [("google_search", "agoogle_search")]

    def__init__(self, key: str, engine: str, num: Optional[int] = None) -> None:
"""Initialize with parameters."""
        self.key = key
        self.engine = engine
        self.num = num

    def_get_url(self, query: str) -> str:
        url = QUERY_URL_TMPL.format(
            key=self.key, engine=self.engine, query=urllib.parse.quote_plus(query)
        )

        if self.num is not None:
            if not 1 <= self.num <= 10:
                raise ValueError("num should be an integer between 1 and 10, inclusive")
            url += f"&num={self.num}"

        return url

    def_parse_results(self, results: List[Dict]) -> Union[List[Dict], str]:
        cleaned_results = []
        if len(results) == 0:
            return "No search results available"

        for result in results:
            if "snippet" in result:
                cleaned_results.append(
                    {
                        "title": result["title"],
                        "link": result["link"],
                        "snippet": result["snippet"],
                    }
                )

        return cleaned_results

    defgoogle_search(self, query: str):
"""
        Make a query to the Google search engine to receive a list of results.

        Args:
            query (str): The query to be passed to Google search.
            num (int, optional): The number of search results to return. Defaults to None.

        Raises:
            ValueError: If the 'num' is not an integer between 1 and 10.

        """
        url = self._get_url(query)

        with httpx.Client() as client:
            response = client.get(url)

        results = json.loads(response.text).get("items", [])

        return self._parse_results(results)

    async defagoogle_search(self, query: str):
"""
        Make a query to the Google search engine to receive a list of results.

        Args:
            query (str): The query to be passed to Google search.
            num (int, optional): The number of search results to return. Defaults to None.

        Raises:
            ValueError: If the 'num' is not an integer between 1 and 10.

        """
        url = self._get_url(query)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        results = json.loads(response.text).get("items", [])

        return self._parse_results(results)

```
 |  
| --- | --- |  
###  google_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GoogleSearchToolSpec.google_search "Permanent link")

```
google_search(query: )

```

Make a query to the Google search engine to receive a list of results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to Google search.  |  _required_  |  
|  `num`  |  The number of search results to return. Defaults to None.  |  _required_  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the 'num' is not an integer between 1 and 10.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/search/base.py`  
| 
```
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
```
 | 
```
defgoogle_search(self, query: str):
"""
    Make a query to the Google search engine to receive a list of results.

    Args:
        query (str): The query to be passed to Google search.
        num (int, optional): The number of search results to return. Defaults to None.

    Raises:
        ValueError: If the 'num' is not an integer between 1 and 10.

    """
    url = self._get_url(query)

    with httpx.Client() as client:
        response = client.get(url)

    results = json.loads(response.text).get("items", [])

    return self._parse_results(results)

```
 |  
| --- | --- |  
###  agoogle_search [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/google/#llama_index.tools.google.GoogleSearchToolSpec.agoogle_search "Permanent link")

```
agoogle_search(query: )

```

Make a query to the Google search engine to receive a list of results.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  The query to be passed to Google search.  |  _required_  |  
|  `num`  |  The number of search results to return. Defaults to None.  |  _required_  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If the 'num' is not an integer between 1 and 10.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-google/llama_index/tools/google/search/base.py`  
| 
```
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
```
 | 
```
async defagoogle_search(self, query: str):
"""
    Make a query to the Google search engine to receive a list of results.

    Args:
        query (str): The query to be passed to Google search.
        num (int, optional): The number of search results to return. Defaults to None.

    Raises:
        ValueError: If the 'num' is not an integer between 1 and 10.

    """
    url = self._get_url(query)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    results = json.loads(response.text).get("items", [])

    return self._parse_results(results)

```
 |  
| --- | --- |  
options: members: - GmailToolSpec - GoogleCalendarToolSpec - GoogleSearchToolSpec
