# Measurespace
##  MeasureSpaceToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/measurespace/#llama_index.tools.measurespace.MeasureSpaceToolSpec "Permanent link")
Bases: 
Measure Space tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-measurespace/llama_index/tools/measurespace/base.py`  
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
```
 | 
```
classMeasureSpaceToolSpec(BaseToolSpec):
"""Measure Space tool spec."""

    spec_functions = [
        "get_hourly_weather_forecast",
        "get_daily_weather_forecast",
        "get_daily_climate_forecast",
        "get_daily_air_quality_forecast",
        "get_latitude_longitude_from_location",
        "get_location_from_latitude_longitude",
    ]

    def__init__(self, api_keys: Dict[str, str], unit: str = "metric") -> None:
"""Initialize with parameters."""
        try:
            importmeasure_space_apiasmsa
        except ImportError:
            raise ImportError(
                "The Measure Space tool requires the measure-space-api package to be installed. "
                "Please install it using `pip install measure-space-api`."
            )

        self.api_keys = api_keys
        self.unit = unit
        self.msa = msa

    def_get_api_key(self, api_name: str):
"""
        Get API keys.

        Args:
            api_name (str): API service name

        """
        api_key = self.api_keys.get(api_name)
        if not api_key:
            raise ValueError(
                f"API key is required for {api_name} service. Please get your API key from measurespace.io/pricing."
            )

        return api_key

    def_format_output(self, wx: Dict) -> List[str]:
"""
        Format output to a list of string with the following format.

        ['total precipitation: 1 mm, wind speed: 10 m/s', 'total precipitation: 1 mm, wind speed: 10 m/s']

        Args:
            wx (Dict): API output in json format

        """
        wx_list = []
        for i in range(len(wx["time"])):
            tmp_list = []
            for key, value in wx.items():
                if key != "time":
                    a_name, a_unit = self.msa.get_metadata(key, self.unit)
                    tmp_list.append(f"{a_name}: {value[i]}{a_unit}")
            if tmp_list:
                wx_list.append(",".join(tmp_list))

        return wx_list

    defget_hourly_weather_forecast(self, location: str) -> List[Document]:
"""
        Get hourly weather forecast for given location.

        Args:
            location (str): location name

        """
        api_key = self._get_api_key("hourly_weather")
        geocoding_api_key = self._get_api_key("geocoding")
        params = {"variables": "tp, t2m, windSpeed, windDegree, r2"}
        wx = self.msa.get_hourly_weather(
            api_key,
            geocoding_api_key,
            location,
            params,
        )
        # Get variable metadata
        for x in ["latitude", "longitude"]:
            if x in wx:
                del wx[x]
        output = self._format_output(wx)
        documents = []
        for i in range(len(wx["time"])):
            documents.append(
                Document(
                    text=output[i],
                    metadata={
                        "Hourly weather for location": location,
                        "Date and time": wx["time"][i],
                    },
                )
            )

        return documents

    defget_daily_weather_forecast(self, location: str) -> List[Document]:
"""
        Get daily weather forecast for given location.

        Args:
            location (str): location name

        """
        api_key = self._get_api_key("daily_weather")
        geocoding_api_key = self._get_api_key("geocoding")
        params = {"variables": "tp, minT, maxT, meanwindSpeed, meanwindDegree, meanRH"}

        wx = self.msa.get_daily_weather(
            api_key,
            geocoding_api_key,
            location,
            params,
        )
        # Get variable metadata
        for x in ["latitude", "longitude"]:
            if x in wx:
                del wx[x]
        output = self._format_output(wx)
        documents = []

        for i in range(len(wx["time"])):
            documents.append(
                Document(
                    text=output[i],
                    metadata={
                        "Daily weather for location": location,
                        "Date": wx["time"][i],
                    },
                )
            )

        return documents

    defget_daily_climate_forecast(self, location: str) -> List[Document]:
"""
        Get hourly climate forecast for given location.

        Args:
            location (str): location name

        """
        api_key = self._get_api_key("daily_climate")
        geocoding_api_key = self._get_api_key("geocoding")
        params = {"variables": "t2m, tmin, tmax, sh2"}

        wx = self.msa.get_daily_climate(
            api_key,
            geocoding_api_key,
            location,
            params,
        )
        # Get variable metadata
        for x in ["latitude", "longitude"]:
            if x in wx:
                del wx[x]
        output = self._format_output(wx)
        documents = []

        for i in range(len(wx["time"])):
            documents.append(
                Document(
                    text=output[i],
                    metadata={
                        "Daily climate for location": location,
                        "Date": wx["time"][i],
                    },
                )
            )

        return documents

    defget_daily_air_quality_forecast(self, location: str) -> List[Document]:
"""
        Get daily air quality forecast for given location.

        Args:
            location (str): location name

        """
        api_key = self._get_api_key("daily_air_quality")
        geocoding_api_key = self._get_api_key("geocoding")
        params = {"variables": "AQI, maxPM10, maxPM25"}

        wx = self.msa.get_daily_air_quality(
            api_key,
            geocoding_api_key,
            location,
            params,
        )
        # Get variable metadata
        for x in ["latitude", "longitude"]:
            if x in wx:
                del wx[x]
        output = self._format_output(wx)
        documents = []

        for i in range(len(wx["time"])):
            documents.append(
                Document(
                    text=output[i],
                    metadata={
                        "Daily air quality for location": location,
                        "Date": wx["time"][i],
                    },
                )
            )

        return documents

    defget_latitude_longitude_from_location(self, location: str) -> List[Document]:
"""
        Get latitude and longitude from given location.

        Args:
            location (str): location name

        """
        api_key = self._get_api_key("geocoding")
        latitude, longitude = self.msa.get_lat_lon_from_city(
            api_key=api_key, location_name=location
        )

        return [
            Document(
                text=f"latitude: {latitude}, longitude: {longitude}",
                metadata={"Latitude and longitude for location": location},
            )
        ]

    defget_location_from_latitude_longitude(
        self, latitude: float, longitude: float
    ) -> List[Document]:
"""
        Get nearest location name from given latitude and longitude.

        Args:
            latitude (float): latitude
            longitude (float): longitude

        """
        api_key = self._get_api_key("geocoding")
        res = self.msa.get_city_from_lat_lon(api_key, latitude, longitude)

        return [
            Document(
                text=f"Location name: {res}",
                metadata="Nearest location for given longitude and latitude",
            )
        ]

```
 |  
| --- | --- |  
###  get_hourly_weather_forecast [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/measurespace/#llama_index.tools.measurespace.MeasureSpaceToolSpec.get_hourly_weather_forecast "Permanent link")

```
get_hourly_weather_forecast(
    location: ,
) -> []

```

Get hourly weather forecast for given location.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `location`  |  location name  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-measurespace/llama_index/tools/measurespace/base.py`  
| 
```
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
```
 | 
```
defget_hourly_weather_forecast(self, location: str) -> List[Document]:
"""
    Get hourly weather forecast for given location.

    Args:
        location (str): location name

    """
    api_key = self._get_api_key("hourly_weather")
    geocoding_api_key = self._get_api_key("geocoding")
    params = {"variables": "tp, t2m, windSpeed, windDegree, r2"}
    wx = self.msa.get_hourly_weather(
        api_key,
        geocoding_api_key,
        location,
        params,
    )
    # Get variable metadata
    for x in ["latitude", "longitude"]:
        if x in wx:
            del wx[x]
    output = self._format_output(wx)
    documents = []
    for i in range(len(wx["time"])):
        documents.append(
            Document(
                text=output[i],
                metadata={
                    "Hourly weather for location": location,
                    "Date and time": wx["time"][i],
                },
            )
        )

    return documents

```
 |  
| --- | --- |  
###  get_daily_weather_forecast [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/measurespace/#llama_index.tools.measurespace.MeasureSpaceToolSpec.get_daily_weather_forecast "Permanent link")

```
get_daily_weather_forecast(location: ) -> []

```

Get daily weather forecast for given location.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `location`  |  location name  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-measurespace/llama_index/tools/measurespace/base.py`  
| 
```
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
```
 | 
```
defget_daily_weather_forecast(self, location: str) -> List[Document]:
"""
    Get daily weather forecast for given location.

    Args:
        location (str): location name

    """
    api_key = self._get_api_key("daily_weather")
    geocoding_api_key = self._get_api_key("geocoding")
    params = {"variables": "tp, minT, maxT, meanwindSpeed, meanwindDegree, meanRH"}

    wx = self.msa.get_daily_weather(
        api_key,
        geocoding_api_key,
        location,
        params,
    )
    # Get variable metadata
    for x in ["latitude", "longitude"]:
        if x in wx:
            del wx[x]
    output = self._format_output(wx)
    documents = []

    for i in range(len(wx["time"])):
        documents.append(
            Document(
                text=output[i],
                metadata={
                    "Daily weather for location": location,
                    "Date": wx["time"][i],
                },
            )
        )

    return documents

```
 |  
| --- | --- |  
###  get_daily_climate_forecast [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/measurespace/#llama_index.tools.measurespace.MeasureSpaceToolSpec.get_daily_climate_forecast "Permanent link")

```
get_daily_climate_forecast(location: ) -> []

```

Get hourly climate forecast for given location.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `location`  |  location name  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-measurespace/llama_index/tools/measurespace/base.py`  
| 
```
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
```
 | 
```
defget_daily_climate_forecast(self, location: str) -> List[Document]:
"""
    Get hourly climate forecast for given location.

    Args:
        location (str): location name

    """
    api_key = self._get_api_key("daily_climate")
    geocoding_api_key = self._get_api_key("geocoding")
    params = {"variables": "t2m, tmin, tmax, sh2"}

    wx = self.msa.get_daily_climate(
        api_key,
        geocoding_api_key,
        location,
        params,
    )
    # Get variable metadata
    for x in ["latitude", "longitude"]:
        if x in wx:
            del wx[x]
    output = self._format_output(wx)
    documents = []

    for i in range(len(wx["time"])):
        documents.append(
            Document(
                text=output[i],
                metadata={
                    "Daily climate for location": location,
                    "Date": wx["time"][i],
                },
            )
        )

    return documents

```
 |  
| --- | --- |  
###  get_daily_air_quality_forecast [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/measurespace/#llama_index.tools.measurespace.MeasureSpaceToolSpec.get_daily_air_quality_forecast "Permanent link")

```
get_daily_air_quality_forecast(
    location: ,
) -> []

```

Get daily air quality forecast for given location.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `location`  |  location name  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-measurespace/llama_index/tools/measurespace/base.py`  
| 
```
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
```
 | 
```
defget_daily_air_quality_forecast(self, location: str) -> List[Document]:
"""
    Get daily air quality forecast for given location.

    Args:
        location (str): location name

    """
    api_key = self._get_api_key("daily_air_quality")
    geocoding_api_key = self._get_api_key("geocoding")
    params = {"variables": "AQI, maxPM10, maxPM25"}

    wx = self.msa.get_daily_air_quality(
        api_key,
        geocoding_api_key,
        location,
        params,
    )
    # Get variable metadata
    for x in ["latitude", "longitude"]:
        if x in wx:
            del wx[x]
    output = self._format_output(wx)
    documents = []

    for i in range(len(wx["time"])):
        documents.append(
            Document(
                text=output[i],
                metadata={
                    "Daily air quality for location": location,
                    "Date": wx["time"][i],
                },
            )
        )

    return documents

```
 |  
| --- | --- |  
###  get_latitude_longitude_from_location [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/measurespace/#llama_index.tools.measurespace.MeasureSpaceToolSpec.get_latitude_longitude_from_location "Permanent link")

```
get_latitude_longitude_from_location(
    location: ,
) -> []

```

Get latitude and longitude from given location.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `location`  |  location name  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-measurespace/llama_index/tools/measurespace/base.py`  
| 
```
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
```
 | 
```
defget_latitude_longitude_from_location(self, location: str) -> List[Document]:
"""
    Get latitude and longitude from given location.

    Args:
        location (str): location name

    """
    api_key = self._get_api_key("geocoding")
    latitude, longitude = self.msa.get_lat_lon_from_city(
        api_key=api_key, location_name=location
    )

    return [
        Document(
            text=f"latitude: {latitude}, longitude: {longitude}",
            metadata={"Latitude and longitude for location": location},
        )
    ]

```
 |  
| --- | --- |  
###  get_location_from_latitude_longitude [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/measurespace/#llama_index.tools.measurespace.MeasureSpaceToolSpec.get_location_from_latitude_longitude "Permanent link")

```
get_location_from_latitude_longitude(
    latitude: float, longitude: float
) -> []

```

Get nearest location name from given latitude and longitude.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `latitude`  |  `float`  |  latitude  |  _required_  |  
|  `longitude`  |  `float`  |  longitude  |  _required_  |  
Source code in `llama-index-integrations/tools/llama-index-tools-measurespace/llama_index/tools/measurespace/base.py`  
| 
```
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
```
 | 
```
defget_location_from_latitude_longitude(
    self, latitude: float, longitude: float
) -> List[Document]:
"""
    Get nearest location name from given latitude and longitude.

    Args:
        latitude (float): latitude
        longitude (float): longitude

    """
    api_key = self._get_api_key("geocoding")
    res = self.msa.get_city_from_lat_lon(api_key, latitude, longitude)

    return [
        Document(
            text=f"Location name: {res}",
            metadata="Nearest location for given longitude and latitude",
        )
    ]

```
 |  
| --- | --- |  
options: members: - MeasureSpaceToolSpec
