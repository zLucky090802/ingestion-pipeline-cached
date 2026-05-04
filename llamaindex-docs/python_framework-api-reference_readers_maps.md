# Maps
##  OpenMap [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/maps/#llama_index.readers.maps.OpenMap "Permanent link")
Bases: 
OpenMap Reader.
Get the map Features from the overpass api(osm) for the given location/area
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `if you not sure about the search_tag and tag_values visit https`  |  //taginfo.openstreetmap.org/tags  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-maps/llama_index/readers/maps/base.py`  
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
```
 | 
```
classOpenMap(BaseReader):
"""
    OpenMap Reader.

    Get the map Features from the overpass api(osm) for the given location/area


    Args:
        localarea(str) -  Area or location you are searching for
        tag_values(str) -  filter for the give area
        search_tag(str)  - Tag that you are looking for

        if you not sure about the search_tag and tag_values visit https://taginfo.openstreetmap.org/tags

        remove_keys(list) - list of keys that need to be removed from the response
                            by default  following keys will be removed ['nodes','geometry','members']

    """

    def__init__(self) -> None:
"""Initialize with parameters."""
        super().__init__()

    @staticmethod
    def_get_user() -> str:
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(10))

    @staticmethod
    def_get_latlon(locarea: str, user_agent: str) -> tuple:
        try:
            fromgeopy.geocodersimport Nominatim
        except ImportError:
            raise ImportError("install geopy using `pip3 install geopy`")

        geolocator = Nominatim(user_agent=user_agent)
        location = geolocator.geocode(locarea)
        return (location.latitude, location.longitude) if location else (None, None)

    defload_data(
        self,
        localarea: str,
        search_tag: Optional[str] = "amenity",
        remove_keys: Optional[List] = ["nodes", "geometry", "members"],
        tag_only: Optional[bool] = True,
        tag_values: Optional[List] = [""],
        local_area_buffer: Optional[int] = 2000,
    ) -> List[Document]:
"""
        This loader will bring you the all the node values from the open street maps for the given location.

        Args:
        localarea(str) -  Area or location you are searching for
        search_tag(str)  - Tag that you are looking for
        if you not sure about the search_tag and tag_values visit https://taginfo.openstreetmap.org/tags

        remove_keys(list) - list of keys that need to be removed from the response
                            by default it those keys will be removed ['nodes','geometry','members']

        tag_only(bool) - if True it  return the nodes which has tags if False returns all the nodes
        tag_values(str) -  filter for the give area
        local_area_buffer(int) - range that you wish to cover (Default 2000(2km))

        """
        try:
            fromosmxtractimport location, overpass
            fromosmxtract.errorsimport OverpassBadRequest
        except ImportError:
            raise ImportError("install osmxtract using `pip3 install osmxtract`")

        null_list = ["", "null", "none", None]
        extra_info = {}
        local_area = localarea

        if local_area.lower().strip() in null_list:
            raise Exception("The Area should not be null")

        user = self._get_user()
        lat, lon = self._get_latlon(local_area, user)
        try:
            bounds = location.from_buffer(lat, lon, buffer_size=int(local_area_buffer))
        except TypeError:
            raise TypeError("Please give valid location name or check for spelling")

        # overpass query generation and execution
        tag_values = [str(i).lower().strip() for i in tag_values]
        query = overpass.ql_query(
            bounds, tag=search_tag.lower(), values=tag_values, timeout=500
        )

        extra_info["overpass_query"] = query
        try:
            response = overpass.request(query)

        except OverpassBadRequest:
            raise TypeError(
                f"Error while executing the Query {query} please check the Args"
            )

        res = response["elements"]

        _meta = response.copy()
        del _meta["elements"]
        extra_info["overpass_meta"] = str(_meta)
        extra_info["lat"] = lat
        extra_info["lon"] = lon
        # filtering for only the tag values
        filtered = [i for i in res if "tags" in i] if tag_only else res

        for key in remove_keys:
            [i.pop(key, None) for i in filtered]
        if filtered:
            return Document(text=str(filtered), extra_info=extra_info)
        else:
            return Document(text=str(res), extra_info=extra_info)

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/maps/#llama_index.readers.maps.OpenMap.load_data "Permanent link")

```
load_data(
    localarea: ,
    search_tag: Optional[] = "amenity",
    remove_keys: Optional[] = [
        "nodes",
        "geometry",
        "members",
    ],
    tag_only: Optional[] = True,
    tag_values: Optional[] = [""],
    local_area_buffer: Optional[] = 2000,
) -> []

```

This loader will bring you the all the node values from the open street maps for the given location.
Args: localarea(str) - Area or location you are searching for search_tag(str) - Tag that you are looking for if you not sure about the search_tag and tag_values visit https://taginfo.openstreetmap.org/tags
remove_keys(list) - list of keys that need to be removed from the response by default it those keys will be removed ['nodes','geometry','members']
tag_only(bool) - if True it return the nodes which has tags if False returns all the nodes tag_values(str) - filter for the give area local_area_buffer(int) - range that you wish to cover (Default 2000(2km))
Source code in `llama-index-integrations/readers/llama-index-readers-maps/llama_index/readers/maps/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    localarea: str,
    search_tag: Optional[str] = "amenity",
    remove_keys: Optional[List] = ["nodes", "geometry", "members"],
    tag_only: Optional[bool] = True,
    tag_values: Optional[List] = [""],
    local_area_buffer: Optional[int] = 2000,
) -> List[Document]:
"""
    This loader will bring you the all the node values from the open street maps for the given location.

    Args:
    localarea(str) -  Area or location you are searching for
    search_tag(str)  - Tag that you are looking for
    if you not sure about the search_tag and tag_values visit https://taginfo.openstreetmap.org/tags

    remove_keys(list) - list of keys that need to be removed from the response
                        by default it those keys will be removed ['nodes','geometry','members']

    tag_only(bool) - if True it  return the nodes which has tags if False returns all the nodes
    tag_values(str) -  filter for the give area
    local_area_buffer(int) - range that you wish to cover (Default 2000(2km))

    """
    try:
        fromosmxtractimport location, overpass
        fromosmxtract.errorsimport OverpassBadRequest
    except ImportError:
        raise ImportError("install osmxtract using `pip3 install osmxtract`")

    null_list = ["", "null", "none", None]
    extra_info = {}
    local_area = localarea

    if local_area.lower().strip() in null_list:
        raise Exception("The Area should not be null")

    user = self._get_user()
    lat, lon = self._get_latlon(local_area, user)
    try:
        bounds = location.from_buffer(lat, lon, buffer_size=int(local_area_buffer))
    except TypeError:
        raise TypeError("Please give valid location name or check for spelling")

    # overpass query generation and execution
    tag_values = [str(i).lower().strip() for i in tag_values]
    query = overpass.ql_query(
        bounds, tag=search_tag.lower(), values=tag_values, timeout=500
    )

    extra_info["overpass_query"] = query
    try:
        response = overpass.request(query)

    except OverpassBadRequest:
        raise TypeError(
            f"Error while executing the Query {query} please check the Args"
        )

    res = response["elements"]

    _meta = response.copy()
    del _meta["elements"]
    extra_info["overpass_meta"] = str(_meta)
    extra_info["lat"] = lat
    extra_info["lon"] = lon
    # filtering for only the tag values
    filtered = [i for i in res if "tags" in i] if tag_only else res

    for key in remove_keys:
        [i.pop(key, None) for i in filtered]
    if filtered:
        return Document(text=str(filtered), extra_info=extra_info)
    else:
        return Document(text=str(res), extra_info=extra_info)

```
 |  
| --- | --- |  
options: members: - OpenMap
