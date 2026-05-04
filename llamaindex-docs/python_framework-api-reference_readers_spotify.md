# Spotify
##  SpotifyReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/spotify/#llama_index.readers.spotify.SpotifyReader "Permanent link")
Bases: 
Spotify Reader.
Read a user's saved albums, tracks, or playlists from Spotify.
Source code in `llama-index-integrations/readers/llama-index-readers-spotify/llama_index/readers/spotify/base.py`  
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
```
 | 
```
classSpotifyReader(BaseReader):
"""
    Spotify Reader.

    Read a user's saved albums, tracks, or playlists from Spotify.

    """

    defload_data(self, collection: Optional[str] = "albums") -> List[Document]:
"""
        Load data from a user's Spotify account.

        Args:
            collections (Optional[str]): "albums", "tracks", or "playlists"

        """
        importspotipy
        fromspotipy.oauth2import SpotifyOAuth

        scope = "user-library-read"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        results = []

        if collection == "albums":
            response = sp.current_user_saved_albums()
            items = response["items"]
            for item in items:
                album = item["album"]
                album_name = album["name"]
                artist_name = album["artists"][0]["name"]
                album_string = f"Album {album_name} by Artist {artist_name}\n"
                results.append(Document(text=album_string))
        elif collection == "tracks":
            response = sp.current_user_saved_tracks()
            items = response["items"]
            for item in items:
                track = item["track"]
                track_name = track["name"]
                artist_name = track["artists"][0]["name"]
                artist_string = f"Track {track_name} by Artist {artist_name}\n"
                results.append(Document(text=artist_string))
        elif collection == "playlists":
            response = sp.current_user_playlists()
            items = response["items"]
            for item in items:
                playlist_name = item["name"]
                owner_name = item["owner"]["display_name"]
                playlist_string = f"Playlist {playlist_name} created by {owner_name}\n"
                results.append(Document(text=playlist_string))
        else:
            raise ValueError(
                "Invalid collection parameter value. Allowed values are 'albums',"
                " 'tracks', or 'playlists'."
            )

        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/spotify/#llama_index.readers.spotify.SpotifyReader.load_data "Permanent link")

```
load_data(
    collection: Optional[] = "albums",
) -> []

```

Load data from a user's Spotify account.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `collections`  |  `Optional[str]`  |  "albums", "tracks", or "playlists"  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-spotify/llama_index/readers/spotify/base.py`  
| 
```
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
```
 | 
```
defload_data(self, collection: Optional[str] = "albums") -> List[Document]:
"""
    Load data from a user's Spotify account.

    Args:
        collections (Optional[str]): "albums", "tracks", or "playlists"

    """
    importspotipy
    fromspotipy.oauth2import SpotifyOAuth

    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = []

    if collection == "albums":
        response = sp.current_user_saved_albums()
        items = response["items"]
        for item in items:
            album = item["album"]
            album_name = album["name"]
            artist_name = album["artists"][0]["name"]
            album_string = f"Album {album_name} by Artist {artist_name}\n"
            results.append(Document(text=album_string))
    elif collection == "tracks":
        response = sp.current_user_saved_tracks()
        items = response["items"]
        for item in items:
            track = item["track"]
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            artist_string = f"Track {track_name} by Artist {artist_name}\n"
            results.append(Document(text=artist_string))
    elif collection == "playlists":
        response = sp.current_user_playlists()
        items = response["items"]
        for item in items:
            playlist_name = item["name"]
            owner_name = item["owner"]["display_name"]
            playlist_string = f"Playlist {playlist_name} created by {owner_name}\n"
            results.append(Document(text=playlist_string))
    else:
        raise ValueError(
            "Invalid collection parameter value. Allowed values are 'albums',"
            " 'tracks', or 'playlists'."
        )

    return results

```
 |  
| --- | --- |  
options: members: - SpotifyReader
