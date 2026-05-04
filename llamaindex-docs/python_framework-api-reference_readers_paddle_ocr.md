# Paddle ocr
##  PDFPaddleOCRReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/paddle_ocr/#llama_index.readers.paddle_ocr.PDFPaddleOCRReader "Permanent link")
Bases: 
Source code in `llama-index-integrations/readers/llama-index-readers-paddle-ocr/llama_index/readers/paddle_ocr/base.py`  
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
```
 | 
```
classPDFPaddleOCRReader(BaseReader):
    def__init__(self, use_angle_cls: bool = True, lang: str = "en"):
"""Initialize PaddleOCR with given parameters"""
        self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)

    defextract_text_from_image(self, image_data):
"""
        Extract text from image data using PaddleOCR
        """
        try:
            # Convert image data to PIL Image
            image = Image.open(io.BytesIO(image_data))

            # Save temporary image file for PaddleOCR
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                image.save(temp_file.name)
                temp_file_path = temp_file.name

            # Use PaddleOCR to recognize text in the image
            result = self.ocr.predict(temp_file_path)

            # Clean up temporary file
            Path(temp_file_path).unlink()

            # Extract text from recognition results
            extracted_text = ""
            for line in result:
                for text in line["rec_texts"]:
                    extracted_text += text + " "

            return extracted_text.strip()

        except Exception as e:
            logging.error(f"Error in image OCR recognition: {e!s}")
            return ""

    defis_text_meaningful(self, text):
"""
        Check if the extracted text is meaningful
        """
        if not text or len(text.strip())  5:
            return False

        # Filter out cases that are likely just page numbers
        if re.match(r"^\d{1,3}$", text.strip()):
            return False

        # Filter out cases that are likely just headers or footers
        common_footers = ["page", "of", "total", "copyright", "all rights reserved"]
        if any(footer in text.lower() for footer in common_footers):
            return len(text.strip())  10

        return True

    defextract_page_elements(self, pdf_path, page_num):
"""
        Extract all elements (text and images) from a PDF page, maintaining original order
        """
        elements = []

        try:
            # Use pdfplumber to extract text and position information
            with pdfplumber.open(pdf_path) as pdf:
                if page_num  len(pdf.pages):
                    page = pdf.pages[page_num]

                    # Extract text and their positions
                    words = page.extract_words(keep_blank_chars=True)
                    for word in words:
                        elements.append(("text", word["text"], word["top"]))

            # Use PyMuPDF to extract images and their positions
            doc = fitz.open(pdf_path)
            pdf_page = doc.load_page(page_num)

            # Get all images in the page
            image_list = pdf_page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                # Extract image
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Get image position
                image_rects = pdf_page.get_image_rects(xref)
                if image_rects:
                    position = image_rects[0].y0
                else:
                    position = 0

                elements.append(("image", image_bytes, position))

            doc.close()

            # Sort elements by position (top to bottom)
            elements.sort(key=lambda x: x[2])

        except Exception as e:
            logging.error(f"Error occurred while extracting page elements: {e!s}")

        return elements

    defload_data(
        self, file_path: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
"""Load data from PDF using PaddleOCR for image content"""
        documents = []
        file_path = Path(file_path)

        try:
            # Use PyMuPDF to get the total number of pages
            doc = fitz.open(file_path)
            total_pages = len(doc)
            doc.close()

            # Process each page
            for page_num in range(total_pages):
                logging.info(f"Processing page {page_num+1}/{total_pages}...")

                # Extract all elements from the page (sorted by position)
                elements = self.extract_page_elements(file_path, page_num)

                page_text = ""
                for element_type, content, position in elements:
                    if element_type == "text":
                        # Directly add text
                        if self.is_text_meaningful(content):
                            page_text += f"[Text Content]: {content} "
                    elif element_type == "image":
                        # Perform OCR on the image
                        ocr_text = self.extract_text_from_image(content)
                        if ocr_text and self.is_text_meaningful(ocr_text):
                            page_text += f"[Image Content]: {ocr_text} "

                # Create Document object and add page number as metadata
                if page_text.strip():
                    metadata = {"page": page_num + 1, "source": str(file_path)}
                    if extra_info:
                        metadata.update(extra_info)

                    document = Document(text=page_text.strip(), metadata=metadata)
                    documents.append(document)

        except Exception as e:
            logging.error(f"Error occurred while reading PDF: {e!s}")
            # Return a Document containing error information
            error_doc = Document(
                text=f"Error occurred while reading PDF: {e!s}",
                metadata={"source": str(file_path), "error": True},
            )
            return [error_doc]

        return documents

```
 |  
| --- | --- |  
###  extract_text_from_image [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/paddle_ocr/#llama_index.readers.paddle_ocr.PDFPaddleOCRReader.extract_text_from_image "Permanent link")

```
extract_text_from_image(image_data)

```

Extract text from image data using PaddleOCR
Source code in `llama-index-integrations/readers/llama-index-readers-paddle-ocr/llama_index/readers/paddle_ocr/base.py`  
| 
```
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
```
 | 
```
defextract_text_from_image(self, image_data):
"""
    Extract text from image data using PaddleOCR
    """
    try:
        # Convert image data to PIL Image
        image = Image.open(io.BytesIO(image_data))

        # Save temporary image file for PaddleOCR
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            image.save(temp_file.name)
            temp_file_path = temp_file.name

        # Use PaddleOCR to recognize text in the image
        result = self.ocr.predict(temp_file_path)

        # Clean up temporary file
        Path(temp_file_path).unlink()

        # Extract text from recognition results
        extracted_text = ""
        for line in result:
            for text in line["rec_texts"]:
                extracted_text += text + " "

        return extracted_text.strip()

    except Exception as e:
        logging.error(f"Error in image OCR recognition: {e!s}")
        return ""

```
 |  
| --- | --- |  
###  is_text_meaningful [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/paddle_ocr/#llama_index.readers.paddle_ocr.PDFPaddleOCRReader.is_text_meaningful "Permanent link")

```
is_text_meaningful(text)

```

Check if the extracted text is meaningful
Source code in `llama-index-integrations/readers/llama-index-readers-paddle-ocr/llama_index/readers/paddle_ocr/base.py`  
| 
```
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
```
 | 
```
defis_text_meaningful(self, text):
"""
    Check if the extracted text is meaningful
    """
    if not text or len(text.strip())  5:
        return False

    # Filter out cases that are likely just page numbers
    if re.match(r"^\d{1,3}$", text.strip()):
        return False

    # Filter out cases that are likely just headers or footers
    common_footers = ["page", "of", "total", "copyright", "all rights reserved"]
    if any(footer in text.lower() for footer in common_footers):
        return len(text.strip())  10

    return True

```
 |  
| --- | --- |  
###  extract_page_elements [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/paddle_ocr/#llama_index.readers.paddle_ocr.PDFPaddleOCRReader.extract_page_elements "Permanent link")

```
extract_page_elements(pdf_path, page_num)

```

Extract all elements (text and images) from a PDF page, maintaining original order
Source code in `llama-index-integrations/readers/llama-index-readers-paddle-ocr/llama_index/readers/paddle_ocr/base.py`  
| 
```
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
```
 | 
```
defextract_page_elements(self, pdf_path, page_num):
"""
    Extract all elements (text and images) from a PDF page, maintaining original order
    """
    elements = []

    try:
        # Use pdfplumber to extract text and position information
        with pdfplumber.open(pdf_path) as pdf:
            if page_num  len(pdf.pages):
                page = pdf.pages[page_num]

                # Extract text and their positions
                words = page.extract_words(keep_blank_chars=True)
                for word in words:
                    elements.append(("text", word["text"], word["top"]))

        # Use PyMuPDF to extract images and their positions
        doc = fitz.open(pdf_path)
        pdf_page = doc.load_page(page_num)

        # Get all images in the page
        image_list = pdf_page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            # Extract image
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Get image position
            image_rects = pdf_page.get_image_rects(xref)
            if image_rects:
                position = image_rects[0].y0
            else:
                position = 0

            elements.append(("image", image_bytes, position))

        doc.close()

        # Sort elements by position (top to bottom)
        elements.sort(key=lambda x: x[2])

    except Exception as e:
        logging.error(f"Error occurred while extracting page elements: {e!s}")

    return elements

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/paddle_ocr/#llama_index.readers.paddle_ocr.PDFPaddleOCRReader.load_data "Permanent link")

```
load_data(
    file_path: , extra_info: Optional[] = None
) -> []

```

Load data from PDF using PaddleOCR for image content
Source code in `llama-index-integrations/readers/llama-index-readers-paddle-ocr/llama_index/readers/paddle_ocr/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self, file_path: Path, extra_info: Optional[Dict] = None
) -> List[Document]:
"""Load data from PDF using PaddleOCR for image content"""
    documents = []
    file_path = Path(file_path)

    try:
        # Use PyMuPDF to get the total number of pages
        doc = fitz.open(file_path)
        total_pages = len(doc)
        doc.close()

        # Process each page
        for page_num in range(total_pages):
            logging.info(f"Processing page {page_num+1}/{total_pages}...")

            # Extract all elements from the page (sorted by position)
            elements = self.extract_page_elements(file_path, page_num)

            page_text = ""
            for element_type, content, position in elements:
                if element_type == "text":
                    # Directly add text
                    if self.is_text_meaningful(content):
                        page_text += f"[Text Content]: {content} "
                elif element_type == "image":
                    # Perform OCR on the image
                    ocr_text = self.extract_text_from_image(content)
                    if ocr_text and self.is_text_meaningful(ocr_text):
                        page_text += f"[Image Content]: {ocr_text} "

            # Create Document object and add page number as metadata
            if page_text.strip():
                metadata = {"page": page_num + 1, "source": str(file_path)}
                if extra_info:
                    metadata.update(extra_info)

                document = Document(text=page_text.strip(), metadata=metadata)
                documents.append(document)

    except Exception as e:
        logging.error(f"Error occurred while reading PDF: {e!s}")
        # Return a Document containing error information
        error_doc = Document(
            text=f"Error occurred while reading PDF: {e!s}",
            metadata={"source": str(file_path), "error": True},
        )
        return [error_doc]

    return documents

```
 |  
| --- | --- |  
options: members: - PDFPaddleOcrReader
