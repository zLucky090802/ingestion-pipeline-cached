# Pdb
##  PdbAbstractReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pdb/#llama_index.readers.pdb.PdbAbstractReader "Permanent link")
Bases: 
Protein Data Bank entries' primary citation abstract reader.
Source code in `llama-index-integrations/readers/llama-index-readers-pdb/llama_index/readers/pdb/base.py`  
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
```
 | 
```
classPdbAbstractReader(BaseReader):
"""Protein Data Bank entries' primary citation abstract reader."""

    def__init__(self) -> None:
        super().__init__()

    defload_data(self, pdb_ids: List[str]) -> List[Document]:
"""
        Load data from RCSB or EBI REST API.

        Args:
            pdb_ids (List[str]): List of PDB ids \
                for which primary citation abstract are to be read.

        """
        results = []
        for pdb_id in pdb_ids:
            title, abstracts = get_pdb_abstract(pdb_id)
            primary_citation = abstracts[title]
            abstract = primary_citation["abstract"]
            abstract_text = "\n".join(
                ["\n".join([str(k), str(v)]) for k, v in abstract.items()]
            )
            results.append(
                Document(
                    text=abstract_text,
                    extra_info={"pdb_id": pdb_id, "primary_citation": primary_citation},
                )
            )
        return results

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/pdb/#llama_index.readers.pdb.PdbAbstractReader.load_data "Permanent link")

```
load_data(pdb_ids: []) -> []

```

Load data from RCSB or EBI REST API.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `pdb_ids`  |  `List[str]`  |  List of PDB ids for which primary citation abstract are to be read.  |  _required_  |  
Source code in `llama-index-integrations/readers/llama-index-readers-pdb/llama_index/readers/pdb/base.py`  
| 
```
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
```
 | 
```
defload_data(self, pdb_ids: List[str]) -> List[Document]:
"""
    Load data from RCSB or EBI REST API.

    Args:
        pdb_ids (List[str]): List of PDB ids \
            for which primary citation abstract are to be read.

    """
    results = []
    for pdb_id in pdb_ids:
        title, abstracts = get_pdb_abstract(pdb_id)
        primary_citation = abstracts[title]
        abstract = primary_citation["abstract"]
        abstract_text = "\n".join(
            ["\n".join([str(k), str(v)]) for k, v in abstract.items()]
        )
        results.append(
            Document(
                text=abstract_text,
                extra_info={"pdb_id": pdb_id, "primary_citation": primary_citation},
            )
        )
    return results

```
 |  
| --- | --- |  
options: members: - PdbAbstractReader
