[Skip to content](https://developers.llamaindex.ai/python/examples/output_parsing/llm_program/#_top)
# LLM Pydantic Program 
This guide shows you how to generate structured data with our `LLMTextCompletionProgram`. Given an LLM as well as an output Pydantic class, generate a structured Pydantic object.
In terms of the target object, you can choose to directly specify `output_cls`, or specify a `PydanticOutputParser` or any other BaseOutputParser that generates a Pydantic object.
in the examples below, we show you different ways of extracting into the `Album` object (which can contain a list of Song objects)
## Extract into `Album` class
[Section titled “Extract into Album class”](https://developers.llamaindex.ai/python/examples/output_parsing/llm_program/#extract-into-album-class)
This is a simple example of parsing an output into an `Album` schema, which can contain multiple songs.
Just pass `Album` into the `output_cls` property on initialization of the `LLMTextCompletionProgram`.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.

```


!pip install llama-index


```


```


from pydantic import BaseModel




from typing import List





from llama_index.core.program import LLMTextCompletionProgram


```

Define output schema

```


classSong(BaseModel):




"""Data model for a song."""





title: str




length_seconds: int






classAlbum(BaseModel):




"""Data model for an album."""





name: str




artist: str




songs: List[Song]


```

Define LLM pydantic program

```


from llama_index.core.program import LLMTextCompletionProgram


```


```


prompt_template_str ="""\




Generate an example album, with an artist and a list of songs. \




Using the movie {movie_name} as inspiration.\





program = LLMTextCompletionProgram.from_defaults(




output_cls=Album,




prompt_template_str=prompt_template_str,




verbose=True,



```

Run program to get structured output.

```


output = program(movie_name="The Shining")


```

The output is a valid Pydantic object that we can then use to call functions/APIs.

```

output

```


```

Album(name='The Overlook', artist='Jack Torrance', songs=[Song(title='Redrum', length_seconds=240), Song(title="Here's Johnny", length_seconds=180), Song(title='Room 237', length_seconds=300), Song(title='All Work and No Play', length_seconds=210), Song(title='The Maze', length_seconds=270)])

```

### Initialize with Pydantic Output Parser
[Section titled “Initialize with Pydantic Output Parser”](https://developers.llamaindex.ai/python/examples/output_parsing/llm_program/#initialize-with-pydantic-output-parser)
The above is equivalent to defining a Pydantic output parser and passing that in instead of the `output_cls` directly.

```


from llama_index.core.output_parsers import PydanticOutputParser





program = LLMTextCompletionProgram.from_defaults(




output_parser=PydanticOutputParser(output_cls=Album),




prompt_template_str=prompt_template_str,




verbose=True,



```


```


output = program(movie_name="Lord of the Rings")



output

```


```

Album(name='The Fellowship of the Ring', artist='Middle-earth Ensemble', songs=[Song(title='The Shire', length_seconds=240), Song(title='Concerning Hobbits', length_seconds=180), Song(title='The Ring Goes South', length_seconds=300), Song(title='A Knife in the Dark', length_seconds=270), Song(title='Flight to the Ford', length_seconds=210), Song(title='Many Meetings', length_seconds=240), Song(title='The Council of Elrond', length_seconds=330), Song(title='The Great Eye', length_seconds=180), Song(title='The Breaking of the Fellowship', length_seconds=360)])

```

## Define a Custom Output Parser
[Section titled “Define a Custom Output Parser”](https://developers.llamaindex.ai/python/examples/output_parsing/llm_program/#define-a-custom-output-parser)
Sometimes you may want to parse an output your own way into a JSON object.

```


from llama_index.core.output_parsers import BaseOutputParser






classCustomAlbumOutputParser(BaseOutputParser):




"""Custom Album output parser.





Assume first line is name and artist.





Assume each subsequent line is the song.







def__init__(self, verbose: bool=False):




self.verbose = verbose





defparse(self, output: str) -> Album:




"""Parse output."""




ifself.verbose:




print(f"> Raw output: {output}")




lines = output.split("\n")




name, artist = lines[0].split(",")




songs = []




forinrange(1, len(lines)):




title, length_seconds = lines[i].split(",")




songs.append(Song(title=title, length_seconds=length_seconds))





return Album(name=name, artist=artist, songs=songs)


```


```


prompt_template_str ="""\




Generate an example album, with an artist and a list of songs. \




Using the movie {movie_name} as inspiration.\




Return answer in following format.


The first line is:


<album_name>, <album_artist>


Every subsequent line is a song with format:


<song_title>, <song_length_seconds>





program = LLMTextCompletionProgram.from_defaults(




output_parser=CustomAlbumOutputParser(verbose=True),




output_cls=Album,




prompt_template_str=prompt_template_str,




verbose=True,



```


```


output = program(movie_name="The Dark Knight")


```


```

> Raw output: Gotham's Reckoning, The Dark Knight


A Dark Knight Rises, 240


The Joker's Symphony, 180


Harvey Dent's Lament, 210


Gotham's Guardian, 195


The Batmobile Chase, 225


The Dark Knight's Theme, 150


The Joker's Mind Games, 180


Rachel's Tragedy, 210


Gotham's Last Stand, 240


The Dark Knight's Triumph, 180

```


```

output

```


```

Album(name="Gotham's Reckoning", artist=' The Dark Knight', songs=[Song(title='A Dark Knight Rises', length_seconds=240), Song(title="The Joker's Symphony", length_seconds=180), Song(title="Harvey Dent's Lament", length_seconds=210), Song(title="Gotham's Guardian", length_seconds=195), Song(title='The Batmobile Chase', length_seconds=225), Song(title="The Dark Knight's Theme", length_seconds=150), Song(title="The Joker's Mind Games", length_seconds=180), Song(title="Rachel's Tragedy", length_seconds=210), Song(title="Gotham's Last Stand", length_seconds=240), Song(title="The Dark Knight's Triumph", length_seconds=180)])

```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


