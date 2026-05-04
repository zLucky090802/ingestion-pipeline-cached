# Hwp
##  HWPReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/hwp/#llama_index.readers.hwp.HWPReader "Permanent link")
Bases: 
Hwp Reader. Reads contents from Hwp file. Args: None.
Source code in `llama-index-integrations/readers/llama-index-readers-hwp/llama_index/readers/hwp/base.py`  
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
```
 | 
```
classHWPReader(BaseReader):
"""
    Hwp Reader. Reads contents from Hwp file.
    Args: None.
    """

    def__init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.FILE_HEADER_SECTION = "FileHeader"
        self.HWP_SUMMARY_SECTION = "\x05HwpSummaryInformation"
        self.SECTION_NAME_LENGTH = len("Section")
        self.BODYTEXT_SECTION = "BodyText"
        self.HWP_TEXT_TAGS = [67]

    defload_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
"""
        Load data and extract table from Hwp file.

        Args:
            file (Path): Path for the Hwp file.


        Returns:
            List[Document].

        """
        importolefile

        load_file = olefile.OleFileIO(file)
        file_dir = load_file.listdir()

        if self.is_valid(file_dir) is False:
            raise Exception("Not Valid HwpFile")

        result_text = self._get_text(load_file, file_dir)
        result = self._text_to_document(text=result_text, extra_info=extra_info)
        return [result]

    defis_valid(self, dirs):
        if [self.FILE_HEADER_SECTION] not in dirs:
            return False

        return [self.HWP_SUMMARY_SECTION] in dirs

    defget_body_sections(self, dirs):
        m = []
        for d in dirs:
            if d[0] == self.BODYTEXT_SECTION:
                m.append(int(d[1][self.SECTION_NAME_LENGTH :]))

        return ["BodyText/Section" + str(x) for x in sorted(m)]

    def_text_to_document(
        self, text: str, extra_info: Optional[Dict] = None
    ) -> Document:
        return Document(text=text, extra_info=extra_info or {})

    defget_text(self):
        return self.text

        # 전체 text 추출

    def_get_text(self, load_file, file_dir):
        sections = self.get_body_sections(file_dir)
        text = ""
        for section in sections:
            text += self.get_text_from_section(load_file, section)
            text += "\n"

        self.text = text
        return self.text

    defis_compressed(self, load_file):
        header = load_file.openstream("FileHeader")
        header_data = header.read()
        return (header_data[36]  1) == 1

    defget_text_from_section(self, load_file, section):
        bodytext = load_file.openstream(section)
        data = bodytext.read()

        unpacked_data = (
            zlib.decompress(data, -15) if self.is_compressed(load_file) else data
        )
        size = len(unpacked_data)

        i = 0

        text = ""
        while i  size:
            header = struct.unpack_from("<I", unpacked_data, i)[0]
            rec_type = header  0x3FF
            (header  10)  0x3FF
            rec_len = (header  20)  0xFFF

            if rec_type in self.HWP_TEXT_TAGS:
                rec_data = unpacked_data[i + 4 : i + 4 + rec_len]
                text += rec_data.decode("utf-16")
                text += "\n"

            i += 4 + rec_len

        return text

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/hwp/#llama_index.readers.hwp.HWPReader.load_data "Permanent link")

```
load_data(
    file: , extra_info: Optional[] = None
) -> []

```

Load data and extract table from Hwp file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file`  |  `Path`  |  Path for the Hwp file.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document].  |  
Source code in `llama-index-integrations/readers/llama-index-readers-hwp/llama_index/readers/hwp/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, file: Path, extra_info: Optional[Dict] = None
) -> List[Document]:
"""
    Load data and extract table from Hwp file.

    Args:
        file (Path): Path for the Hwp file.


    Returns:
        List[Document].

    """
    importolefile

    load_file = olefile.OleFileIO(file)
    file_dir = load_file.listdir()

    if self.is_valid(file_dir) is False:
        raise Exception("Not Valid HwpFile")

    result_text = self._get_text(load_file, file_dir)
    result = self._text_to_document(text=result_text, extra_info=extra_info)
    return [result]

```
 |  
| --- | --- |  
options: members: - HWPReader
