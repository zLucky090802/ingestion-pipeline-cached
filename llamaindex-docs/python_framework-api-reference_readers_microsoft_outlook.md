# Microsoft outlook
##  OutlookLocalCalendarReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/microsoft_outlook/#llama_index.readers.microsoft_outlook.OutlookLocalCalendarReader "Permanent link")
Bases: 
Outlook local calendar reader for Windows. Reads events from local copy of Outlook calendar.
Source code in `llama-index-integrations/readers/llama-index-readers-microsoft-outlook/llama_index/readers/microsoft_outlook/base.py`  
| 
```
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
```
 | 
```
classOutlookLocalCalendarReader(BaseReader):
"""
    Outlook local calendar reader for Windows.
    Reads events from local copy of Outlook calendar.
    """

    defload_data(
        self,
        number_of_results: Optional[int] = 100,
        start_date: Optional[Union[str, datetime.date]] = None,
        end_date: Optional[Union[str, datetime.date]] = None,
        more_attributes: Optional[List[str]] = None,
    ) -> List[Document]:
"""
        Load data from user's local calendar.

        Args:
            number_of_results (Optional[int]): the number of events to return. Defaults to 100.
            start_date (Optional[Union[str, datetime.date]]): the start date to return events from. Defaults to today.
            end_date (Optional[Union[str, datetime.date]]): the last date (inclusive) to return events from. Defaults to 2199-01-01.
            more_attributes (Optional[ List[str]]): additional attributes to be retrieved from calendar entries. Non-existnat attributes are ignored.

        Returns a list of documents sutitable for indexing by llam_index. Always returns Start, End, Subject, Location, and Organizer
        attributes and optionally returns additional attributes specified in the more_attributes parameter.

        """
        if platform.system().lower() != "windows":
            return []
        attributes = [
            "Start",
            "End",
            "Subject",
            "Location",
            "Organizer",
        ]  # base attributes to return
        if more_attributes is not None:  # if the user has specified more attributes
            attributes += more_attributes
        if start_date is None:
            start_date = datetime.date.today()
        elif isinstance(start_date, str):
            start_date = datetime.date.fromisoformat(start_date)

        # Initialize the Outlook application
        winstuff = importlib.import_module("win32com.client")
        outlook = winstuff.Dispatch("Outlook.Application").GetNamespace("MAPI")

        # Get the Calendar folder
        calendar_folder = outlook.GetDefaultFolder(9)

        # Retrieve calendar items
        events = calendar_folder.Items

        if not events:
            return []
        events.Sort("[Start]")  # Sort items by start time
        numberReturned = 0
        results = []
        for event in events:
            converted_date = datetime.date(
                event.Start.year, event.Start.month, event.Start.day
            )
            if converted_date  start_date:  # if past start date
                numberReturned += 1
                eventstring = ""
                for attribute in attributes:
                    if hasattr(event, attribute):
                        eventstring += f"{attribute}: {getattr(event,attribute)}, "
                results.append(Document(text=eventstring))
            if numberReturned >= number_of_results:
                break

        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/microsoft_outlook/#llama_index.readers.microsoft_outlook.OutlookLocalCalendarReader.load_data "Permanent link")

```
load_data(
    number_of_results: Optional[] = 100,
    start_date: Optional[Union[, ]] = None,
    end_date: Optional[Union[, ]] = None,
    more_attributes: Optional[[]] = None,
) -> []

```

Load data from user's local calendar.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `number_of_results`  |  `Optional[int]`  |  the number of events to return. Defaults to 100.  |  `100`  |  
|  `start_date`  |  `Optional[Union[str, date]]`  |  the start date to return events from. Defaults to today.  |  `None`  |  
|  `end_date`  |  `Optional[Union[str, date]]`  |  the last date (inclusive) to return events from. Defaults to 2199-01-01.  |  `None`  |  
|  `more_attributes`  |  `Optional[List[str]]`  |  additional attributes to be retrieved from calendar entries. Non-existnat attributes are ignored.  |  `None`  |  
Returns a list of documents sutitable for indexing by llam_index. Always returns Start, End, Subject, Location, and Organizer attributes and optionally returns additional attributes specified in the more_attributes parameter.
Source code in `llama-index-integrations/readers/llama-index-readers-microsoft-outlook/llama_index/readers/microsoft_outlook/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    number_of_results: Optional[int] = 100,
    start_date: Optional[Union[str, datetime.date]] = None,
    end_date: Optional[Union[str, datetime.date]] = None,
    more_attributes: Optional[List[str]] = None,
) -> List[Document]:
"""
    Load data from user's local calendar.

    Args:
        number_of_results (Optional[int]): the number of events to return. Defaults to 100.
        start_date (Optional[Union[str, datetime.date]]): the start date to return events from. Defaults to today.
        end_date (Optional[Union[str, datetime.date]]): the last date (inclusive) to return events from. Defaults to 2199-01-01.
        more_attributes (Optional[ List[str]]): additional attributes to be retrieved from calendar entries. Non-existnat attributes are ignored.

    Returns a list of documents sutitable for indexing by llam_index. Always returns Start, End, Subject, Location, and Organizer
    attributes and optionally returns additional attributes specified in the more_attributes parameter.

    """
    if platform.system().lower() != "windows":
        return []
    attributes = [
        "Start",
        "End",
        "Subject",
        "Location",
        "Organizer",
    ]  # base attributes to return
    if more_attributes is not None:  # if the user has specified more attributes
        attributes += more_attributes
    if start_date is None:
        start_date = datetime.date.today()
    elif isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)

    # Initialize the Outlook application
    winstuff = importlib.import_module("win32com.client")
    outlook = winstuff.Dispatch("Outlook.Application").GetNamespace("MAPI")

    # Get the Calendar folder
    calendar_folder = outlook.GetDefaultFolder(9)

    # Retrieve calendar items
    events = calendar_folder.Items

    if not events:
        return []
    events.Sort("[Start]")  # Sort items by start time
    numberReturned = 0
    results = []
    for event in events:
        converted_date = datetime.date(
            event.Start.year, event.Start.month, event.Start.day
        )
        if converted_date  start_date:  # if past start date
            numberReturned += 1
            eventstring = ""
            for attribute in attributes:
                if hasattr(event, attribute):
                    eventstring += f"{attribute}: {getattr(event,attribute)}, "
            results.append(Document(text=eventstring))
        if numberReturned >= number_of_results:
            break

    return results

```
 |  
| --- | --- |  
options: members: - OutlookLocalCalendarReader
