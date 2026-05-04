# Weather
##  WeatherReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/weather/#llama_index.readers.weather.WeatherReader "Permanent link")
Bases: 
Weather Reader.
Reads the forecast & current weather of any location using OpenWeatherMap's free API.
Check 'https://openweathermap.org/appid' on how to generate a free OpenWeatherMap API, It's free.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `token`  |  bearer_token that you get from OWM API.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-weather/llama_index/readers/weather/base.py`  
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
classWeatherReader(BaseReader):
"""
    Weather Reader.

    Reads the forecast & current weather of any location using OpenWeatherMap's free API.

    Check 'https://openweathermap.org/appid' \
        on how to generate a free OpenWeatherMap API, It's free.

    Args:
        token (str): bearer_token that you get from OWM API.

    """

    def__init__(
        self,
        token: str,
    ) -> None:
"""Initialize with parameters."""
        super().__init__()
        self.token = token

    defload_data(
        self,
        places: List[str],
    ) -> List[Document]:
"""
        Load weather data for the given locations.
        OWM's One Call API provides the following weather data for any geographical coordinate:
        - Current weather
        - Hourly forecast for 48 hours
        - Daily forecast for 7 days.

        Args:
            places (List[str]) - places you want the weather data for.

        """
        try:
            importpyowm
        except ImportError:
            raise ImportError("install pyowm using `pip install pyowm`")

        owm = pyowm.OWM(api_key=self.token)
        mgr = owm.weather_manager()

        reg = owm.city_id_registry()

        results = []
        for place in places:
            info_dict = {}
            extra_info = {}
            list_of_locations = reg.locations_for(city_name=place)

            try:
                city = list_of_locations[0]
            except ValueError:
                raise ValueError(
                    f"Unable to find {place}, try checking the spelling and try again"
                )
            lat = city.lat
            lon = city.lon

            res = mgr.one_call(lat=lat, lon=lon)

            extra_info["latitude"] = lat
            extra_info["longitude"] = lon
            extra_info["timezone"] = res.timezone
            info_dict["location"] = place
            info_dict["current weather"] = res.current.to_dict()
            if res.forecast_daily:
                info_dict["daily forecast"] = [i.to_dict() for i in res.forecast_daily]
            if res.forecast_hourly:
                info_dict["hourly forecast"] = [
                    i.to_dict() for i in res.forecast_hourly
                ]
            if res.forecast_minutely:
                info_dict["minutely forecast"] = [
                    i.to_dict() for i in res.forecast_minutely
                ]
            if res.national_weather_alerts:
                info_dict["national weather alerts"] = [
                    i.to_dict() for i in res.national_weather_alerts
                ]

            results.append(Document(text=str(info_dict), extra_info=extra_info))

        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/weather/#llama_index.readers.weather.WeatherReader.load_data "Permanent link")

```
load_data(places: []) -> []

```

Load weather data for the given locations. OWM's One Call API provides the following weather data for any geographical coordinate: - Current weather - Hourly forecast for 48 hours - Daily forecast for 7 days.
Source code in `llama-index-integrations/readers/llama-index-readers-weather/llama_index/readers/weather/base.py`  
| 
```
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
defload_data(
    self,
    places: List[str],
) -> List[Document]:
"""
    Load weather data for the given locations.
    OWM's One Call API provides the following weather data for any geographical coordinate:
    - Current weather
    - Hourly forecast for 48 hours
    - Daily forecast for 7 days.

    Args:
        places (List[str]) - places you want the weather data for.

    """
    try:
        importpyowm
    except ImportError:
        raise ImportError("install pyowm using `pip install pyowm`")

    owm = pyowm.OWM(api_key=self.token)
    mgr = owm.weather_manager()

    reg = owm.city_id_registry()

    results = []
    for place in places:
        info_dict = {}
        extra_info = {}
        list_of_locations = reg.locations_for(city_name=place)

        try:
            city = list_of_locations[0]
        except ValueError:
            raise ValueError(
                f"Unable to find {place}, try checking the spelling and try again"
            )
        lat = city.lat
        lon = city.lon

        res = mgr.one_call(lat=lat, lon=lon)

        extra_info["latitude"] = lat
        extra_info["longitude"] = lon
        extra_info["timezone"] = res.timezone
        info_dict["location"] = place
        info_dict["current weather"] = res.current.to_dict()
        if res.forecast_daily:
            info_dict["daily forecast"] = [i.to_dict() for i in res.forecast_daily]
        if res.forecast_hourly:
            info_dict["hourly forecast"] = [
                i.to_dict() for i in res.forecast_hourly
            ]
        if res.forecast_minutely:
            info_dict["minutely forecast"] = [
                i.to_dict() for i in res.forecast_minutely
            ]
        if res.national_weather_alerts:
            info_dict["national weather alerts"] = [
                i.to_dict() for i in res.national_weather_alerts
            ]

        results.append(Document(text=str(info_dict), extra_info=extra_info))

    return results

```
 |  
| --- | --- |  
options: members: - WeatherReader
