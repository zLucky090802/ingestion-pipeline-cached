# Weather
##  OpenWeatherMapToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/weather/#llama_index.tools.weather.OpenWeatherMapToolSpec "Permanent link")
Bases: 
Open Weather tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-weather/llama_index/tools/weather/base.py`  
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
```
 | 
```
classOpenWeatherMapToolSpec(BaseToolSpec):
"""Open Weather tool spec."""

    spec_functions = ["weather_at_location", "forecast_tomorrow_at_location"]

    def__init__(self, key: str, temp_units: str = "celsius") -> None:
"""Initialize with parameters."""
        try:
            frompyowmimport OWM
        except ImportError:
            raise ImportError(
                "The OpenWeatherMap tool requires the pyowm package to be installed. "
                "Please install it using `pip install pyowm`."
            )

        self.key = key
        self.temp_units = temp_units
        self._owm = OWM(self.key)
        self._mgr = self._owm.weather_manager()

    def_format_temp(self, temperature: Any, temp_unit: str) -> str:
        return (
            f"  - Current: {temperature['temp']}{temp_unit}\n"
            f"  - High: {temperature['temp_max']}{temp_unit}\n"
            f"  - Low: {temperature['temp_min']}{temp_unit}\n"
            f"  - Feels like: {temperature['feels_like']}{temp_unit}"
        )

    def_format_weather(
        self, place: str, temp_str: str, w: Any, time_str: str = "now"
    ) -> str:
"""
        Format weather response from OpenWeatherMap.

        Function thanks to
        langchain/utilities/openweathermap.py
        """
        detailed_status = w.detailed_status
        wind = w.wind()
        humidity = w.humidity
        rain = w.rain
        heat_index = w.heat_index
        clouds = w.clouds

        return (
            f"In {place}, the weather for {time_str} is as follows:\n"
            f"Detailed status: {detailed_status}\n"
            f"Wind speed: {wind['speed']} m/s, direction: {wind['deg']}°\n"
            f"Humidity: {humidity}%\n"
            "Temperature: \n"
            f"{temp_str}\n"
            f"Rain: {rain}\n"
            f"Heat index: {heat_index!s}\n"
            f"Cloud cover: {clouds}%"
        )

    defweather_at_location(self, location: str) -> List[Document]:
"""
        Finds the current weather at a location.

        Args:
            place (str):
                The place to find the weather at.
                Should be a city name and country.

        """
        frompyowm.commons.exceptionsimport NotFoundError

        try:
            observation = self._mgr.weather_at_place(location)
        except NotFoundError:
            return [Document(text=f"Unable to find weather at {location}.")]

        w = observation.weather

        temperature = w.temperature(self.temp_units)
        temp_unit = "°C" if self.temp_units == "celsius" else "°F"
        temp_str = self._format_temp(temperature, temp_unit)

        weather_text = self._format_weather(location, temp_str, w)

        return [Document(text=weather_text, metadata={"weather from": location})]

    defforecast_tomorrow_at_location(self, location: str) -> List[Document]:
"""
        Finds the weather forecast for tomorrow at a location.

        Args:
            location (str):
                The location to find the weather tomorrow at.
                Should be a city name and country.

        """
        frompyowm.commons.exceptionsimport NotFoundError
        frompyowm.utilsimport timestamps

        try:
            forecast = self._mgr.forecast_at_place(location, "3h")
        except NotFoundError:
            return [Document(text=f"Unable to find weather at {location}.")]

        tomorrow = timestamps.tomorrow()
        w = forecast.get_weather_at(tomorrow)

        temperature = w.temperature(self.temp_units)
        temp_unit = "°C" if self.temp_units == "celsius" else "°F"
        temp_str = self._format_temp(temperature, temp_unit)

        weather_text = self._format_weather(location, temp_str, w, "tomorrow")

        return [
            Document(
                text=weather_text,
                metadata={
                    "weather from": location,
                    "forecast for": tomorrow.strftime("%Y-%m-%d"),
                },
            )
        ]

```
 |  
| --- | --- |  
###  weather_at_location [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/weather/#llama_index.tools.weather.OpenWeatherMapToolSpec.weather_at_location "Permanent link")

```
weather_at_location(location: ) -> []

```

Finds the current weather at a location.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `place`  |  The place to find the weather at. Should be a city name and country.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-weather/llama_index/tools/weather/base.py`  
| 
```
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
```
 | 
```
defweather_at_location(self, location: str) -> List[Document]:
"""
    Finds the current weather at a location.

    Args:
        place (str):
            The place to find the weather at.
            Should be a city name and country.

    """
    frompyowm.commons.exceptionsimport NotFoundError

    try:
        observation = self._mgr.weather_at_place(location)
    except NotFoundError:
        return [Document(text=f"Unable to find weather at {location}.")]

    w = observation.weather

    temperature = w.temperature(self.temp_units)
    temp_unit = "°C" if self.temp_units == "celsius" else "°F"
    temp_str = self._format_temp(temperature, temp_unit)

    weather_text = self._format_weather(location, temp_str, w)

    return [Document(text=weather_text, metadata={"weather from": location})]

```
 |  
| --- | --- |  
###  forecast_tomorrow_at_location [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/weather/#llama_index.tools.weather.OpenWeatherMapToolSpec.forecast_tomorrow_at_location "Permanent link")

```
forecast_tomorrow_at_location(
    location: ,
) -> []

```

Finds the weather forecast for tomorrow at a location.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `location`  |  The location to find the weather tomorrow at. Should be a city name and country.  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-weather/llama_index/tools/weather/base.py`  
| 
```
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
```
 | 
```
defforecast_tomorrow_at_location(self, location: str) -> List[Document]:
"""
    Finds the weather forecast for tomorrow at a location.

    Args:
        location (str):
            The location to find the weather tomorrow at.
            Should be a city name and country.

    """
    frompyowm.commons.exceptionsimport NotFoundError
    frompyowm.utilsimport timestamps

    try:
        forecast = self._mgr.forecast_at_place(location, "3h")
    except NotFoundError:
        return [Document(text=f"Unable to find weather at {location}.")]

    tomorrow = timestamps.tomorrow()
    w = forecast.get_weather_at(tomorrow)

    temperature = w.temperature(self.temp_units)
    temp_unit = "°C" if self.temp_units == "celsius" else "°F"
    temp_str = self._format_temp(temperature, temp_unit)

    weather_text = self._format_weather(location, temp_str, w, "tomorrow")

    return [
        Document(
            text=weather_text,
            metadata={
                "weather from": location,
                "forecast for": tomorrow.strftime("%Y-%m-%d"),
            },
        )
    ]

```
 |  
| --- | --- |  
options: members: - OpenWeatherMapToolSpec
