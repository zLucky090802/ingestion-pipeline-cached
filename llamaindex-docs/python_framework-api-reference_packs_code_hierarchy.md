# Code hierarchy
##  CodeHierarchyAgentPack [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyAgentPack "Permanent link")
Bases: 
Code hierarchy agent pack.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/base.py`  
| 
```
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
```
 | 
```
classCodeHierarchyAgentPack(BaseLlamaPack):
"""Code hierarchy agent pack."""

    def__init__(self, split_nodes: List[BaseNode], llm: OpenAI, verbose: bool = True):
"""Initialize the code hierarchy agent pack."""
        fromllama_index.packs.code_hierarchyimport CodeHierarchyKeywordQueryEngine

        self.query_engine = CodeHierarchyKeywordQueryEngine(
            nodes=split_nodes,
        )

        self.tool = QueryEngineTool.from_defaults(
            query_engine=self.query_engine,
            name="code_search",
            description="Search the code hierarchy for a specific code element, using keywords or IDs.",
        )

        self.agent = FunctionAgent(
            tools=[self.tool],
            llm=llm,
            system_prompt=self.query_engine.get_tool_instructions(),
            verbose=verbose,
        )

    defget_modules(self) -> Dict[str, Any]:
        return {
            "query_engine": self.query_engine,
            "tool": self.tool,
            "agent": self.agent,
        }

    defrun(self, user_message: str) -> str:
"""Run the agent on the user message."""
        return asyncio_run(self.arun(user_message))

    async defarun(self, user_message: str) -> str:
"""Run the agent on the user message."""
        return str(await self.agent.run(user_message))

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyAgentPack.run "Permanent link")

```
run(user_message: ) -> 

```

Run the agent on the user message.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/base.py`  
| 
```
42
43
44
```
 | 
```
defrun(self, user_message: str) -> str:
"""Run the agent on the user message."""
    return asyncio_run(self.arun(user_message))

```
 |  
| --- | --- |  
###  arun [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyAgentPack.arun "Permanent link")

```
arun(user_message: ) -> 

```

Run the agent on the user message.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/base.py`  
| 
```
46
47
48
```
 | 
```
async defarun(self, user_message: str) -> str:
"""Run the agent on the user message."""
    return str(await self.agent.run(user_message))

```
 |  
| --- | --- |  
##  CodeHierarchyNodeParser [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyNodeParser "Permanent link")
Bases: 
Split code using a AST parser.
Add metadata about the scope of the code block and relationships between code blocks.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/code_hierarchy.py`  
| 
```
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
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
```
 | 
```
classCodeHierarchyNodeParser(NodeParser):
"""
    Split code using a AST parser.

    Add metadata about the scope of the code block and relationships between
    code blocks.
    """

    @classmethod
    defclass_name(cls) -> str:
"""Get class name."""
        return "CodeHierarchyNodeParser"

    language: str = Field(
        description="The programming language of the code being split."
    )
    signature_identifiers: Dict[str, _SignatureCaptureOptions] = Field(
        description=(
            "A dictionary mapping the type of a split mapped to the first and last type"
            " of itschildren which identify its signature."
        )
    )
    min_characters: int = Field(
        default=80,
        description=(
            "Minimum number of characters per chunk.Defaults to 80 because that's about"
            " how long a replacement comment is in skeleton mode."
        ),
    )
    code_splitter: Optional[CodeSplitter] = Field(
        description="The text splitter to use when splitting documents."
    )
    metadata_extractor: Optional[BaseExtractor] = Field(
        default=None, description="Metadata extraction pipeline to apply to nodes."
    )
    callback_manager: CallbackManager = Field(
        default_factory=CallbackManager, exclude=True
    )
    skeleton: bool = Field(
        True,
        description=(
            "Parent nodes have the text of their child nodes replaced with a signature"
            " and a comment instructing the language model to visit the child node for"
            " the full text of the scope."
        ),
    )

    def__init__(
        self,
        language: str,
        skeleton: bool = True,
        signature_identifiers: Optional[Dict[str, _SignatureCaptureOptions]] = None,
        code_splitter: Optional[CodeSplitter] = None,
        callback_manager: Optional[CallbackManager] = None,
        metadata_extractor: Optional[BaseExtractor] = None,
        chunk_min_characters: int = 80,
    ):
        callback_manager = callback_manager or CallbackManager([])

        if signature_identifiers is None and language in _DEFAULT_SIGNATURE_IDENTIFIERS:
            signature_identifiers = _DEFAULT_SIGNATURE_IDENTIFIERS[language]

        super().__init__(
            include_prev_next_rel=False,
            language=language,
            callback_manager=callback_manager,
            metadata_extractor=metadata_extractor,
            code_splitter=code_splitter,
            signature_identifiers=signature_identifiers,
            min_characters=chunk_min_characters,
            skeleton=skeleton,
        )

    def_get_node_name(self, node: Node) -> str:
"""Get the name of a node."""
        signature_identifier = self.signature_identifiers[node.type]

        defrecur(node: Node) -> str:
            for child in node.children:
                if child.type == signature_identifier.name_identifier:
                    return child.text.decode()
                if child.children:
                    out = recur(child)
                    if out:
                        return out
            return ""

        return recur(node).strip()

    def_get_node_signature(self, text: str, node: Node) -> str:
"""Get the signature of a node."""
        signature_identifier = self.signature_identifiers[node.type]

        deffind_start(node: Node) -> Optional[int]:
            if not signature_identifier.start_signature_types:
                signature_identifier.start_signature_types = []

            for st in signature_identifier.start_signature_types:
                if node.type == st.type:
                    if st.inclusive:
                        return node.start_byte
                    return node.end_byte

            for child in node.children:
                out = find_start(child)
                if out is not None:
                    return out

            return None

        deffind_end(node: Node) -> Optional[int]:
            if not signature_identifier.end_signature_types:
                signature_identifier.end_signature_types = []

            for st in signature_identifier.end_signature_types:
                if node.type == st.type:
                    if st.inclusive:
                        return node.end_byte
                    return node.start_byte

            for child in node.children:
                out = find_end(child)
                if out is not None:
                    return out

            return None

        start_byte, end_byte = find_start(node), find_end(node)
        if start_byte is None:
            start_byte = node.start_byte
        if end_byte is None:
            end_byte = node.end_byte
        return bytes(text, "utf-8")[start_byte:end_byte].decode().strip()

    def_chunk_node(
        self,
        parent: Node,
        text: str,
        _context_list: Optional[List[_ScopeItem]] = None,
        _root: bool = True,
    ) -> _ChunkNodeOutput:
"""
        This is really the "main" method of this class. It is recursive and recursively
        chunks the text by the options identified in self.signature_identifiers.

        It is ran by get_nodes_from_documents.

        Args:
            parent (Node): The parent node to chunk
            text (str): The text of the entire document
            _context_list (Optional[List[_ScopeItem]]): The scope context of the
                                                        parent node
            _root (bool): Whether or not this is the root node

        """
        if _context_list is None:
            _context_list = []

        upstream_children_documents: List[TextNode] = []
        all_documents: List[TextNode] = []

        # Capture any whitespace before parent.start_byte
        # Very important for space sensitive languages like python
        start_byte = parent.start_byte
        text_bytes = bytes(text, "utf-8")
        while start_byte  0 and text_bytes[start_byte - 1 : start_byte] in (
            b" ",
            b"\t",
        ):
            start_byte -= 1

        # Create this node
        current_chunk = text_bytes[start_byte : parent.end_byte].decode()

        # Return early if the chunk is too small
        if len(current_chunk)  self.min_characters and not _root:
            return _ChunkNodeOutput(
                this_document=None, all_documents=[], upstream_children_documents=[]
            )

        # TIP: This is a wonderful place to put a debug breakpoint when
        #      Trying to integrate a new language. Pay attention to parent.type to learn
        #      all the available node types and their hierarchy.
        if parent.type in self.signature_identifiers or _root:
            # Get the new context
            if not _root:
                new_context = _ScopeItem(
                    name=self._get_node_name(parent),
                    type=parent.type,
                    signature=self._get_node_signature(text=text, node=parent),
                )
                _context_list.append(new_context)
            this_document = TextNode(
                text=current_chunk,
                metadata={
                    "inclusive_scopes": [cl.dict() for cl in _context_list],
                    "start_byte": start_byte,
                    "end_byte": parent.end_byte,
                },
                relationships={
                    NodeRelationship.CHILD: [],
                },
            )
            all_documents.append(this_document)
        else:
            this_document = None

        # Iterate over children
        for child in parent.children:
            if child.children:
                # Recurse on the child
                next_chunks = self._chunk_node(
                    child, text, _context_list=_context_list.copy(), _root=False
                )

                # If there is a this_document, then we need
                # to add the children to this_document
                # and flush upstream_children_documents
                if this_document is not None:
                    # If we have been given a document, that means it's children
                    # are already set, so it needs to become a child of this node
                    if next_chunks.this_document is not None:
                        assert not next_chunks.upstream_children_documents, (
                            "next_chunks.this_document and"
                            " next_chunks.upstream_children_documents are exclusive."
                        )
                        this_document.relationships[NodeRelationship.CHILD].append(  # type: ignore
                            next_chunks.this_document.as_related_node_info()
                        )
                        next_chunks.this_document.relationships[
                            NodeRelationship.PARENT
                        ] = this_document.as_related_node_info()
                    # Otherwise, we have been given a list of
                    # upstream_children_documents. We need to make
                    # them a child of this node
                    else:
                        for d in next_chunks.upstream_children_documents:
                            this_document.relationships[NodeRelationship.CHILD].append(  # type: ignore
                                d.as_related_node_info()
                            )
                            d.relationships[NodeRelationship.PARENT] = (
                                this_document.as_related_node_info()
                            )
                # Otherwise we pass the children upstream
                else:
                    # If we have been given a document, that means it's
                    # children are already set, so it needs to become a
                    # child of the next node
                    if next_chunks.this_document is not None:
                        assert not next_chunks.upstream_children_documents, (
                            "next_chunks.this_document and"
                            " next_chunks.upstream_children_documents are exclusive."
                        )
                        upstream_children_documents.append(next_chunks.this_document)
                    # Otherwise, we have leftover children, they need
                    # to become children of the next node
                    else:
                        upstream_children_documents.extend(
                            next_chunks.upstream_children_documents
                        )

                # Lastly we need to maintain all documents
                all_documents.extend(next_chunks.all_documents)

        return _ChunkNodeOutput(
            this_document=this_document,
            upstream_children_documents=upstream_children_documents,
            all_documents=all_documents,
        )

    @staticmethod
    defget_code_hierarchy_from_nodes(
        nodes: Sequence[BaseNode],
        max_depth: int = -1,
    ) -> Tuple[Dict[str, Any], str]:
"""
        Creates a code hierarchy appropriate to put into a tool description or context
        to make it easier to search for code.

        Call after `get_nodes_from_documents` and pass that output to this function.
        """
        out: Dict[str, Any] = defaultdict(dict)

        defget_subdict(keys: List[str]) -> Dict[str, Any]:
            # Get the dictionary we are operating on
            this_dict = out
            for key in keys:
                if key not in this_dict:
                    this_dict[key] = defaultdict(dict)
                this_dict = this_dict[key]
            return this_dict

        defrecur_inclusive_scope(node: BaseNode, i: int, keys: List[str]) -> None:
            if "inclusive_scopes" not in node.metadata:
                raise KeyError("inclusive_scopes not in node.metadata")
            if i >= len(node.metadata["inclusive_scopes"]):
                return
            scope = node.metadata["inclusive_scopes"][i]

            this_dict = get_subdict(keys)

            if scope["name"] not in this_dict:
                this_dict[scope["name"]] = defaultdict(dict)

            if i  max_depth or max_depth == -1:
                recur_inclusive_scope(node, i + 1, [*keys, scope["name"]])

        defdict_to_markdown(d: Dict[str, Any], depth: int = 0) -> str:
            markdown = ""
            indent = "  " * depth  # Two spaces per depth level

            for key, value in d.items():
                if isinstance(value, dict):  # Check if value is a dict
                    # Add the key with a bullet point and increase depth for nested dicts
                    markdown += f"{indent}- {key}\n{dict_to_markdown(value,depth+1)}"
                else:
                    # Handle non-dict items if necessary
                    markdown += f"{indent}- {key}: {value}\n"

            return markdown

        for node in nodes:
            filepath = node.metadata["filepath"].split("/")
            filepath[-1] = filepath[-1].split(".")[0]
            recur_inclusive_scope(node, 0, filepath)

        return out, dict_to_markdown(out)

    def_parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
"""
        The main public method of this class.

        Parse documents into nodes.
        """
        out: List[BaseNode] = []

        try:
            importtree_sitter_language_pack
        except ImportError:
            raise ImportError(
                "Please install tree_sitter_language_pack to use CodeSplitter."
            )

        try:
            parser = tree_sitter_language_pack.get_parser(self.language)
            language = tree_sitter_language_pack.get_language(self.language)

            # Construct the path to the SCM file
            scm_fname = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "pytree-sitter-queries",
                f"tree-sitter-{self.language}-tags.scm",
            )
        except Exception as e:
            print(
                f"Could not get parser for language {self.language}. Check "
                "https://github.com/Goldziher/tree-sitter-language-pack?tab=readme-ov-file#available-languages "
                "for a list of valid languages."
            )
            raise e  # noqa: TRY201

        query = None
        if self.signature_identifiers is None:
            assert os.path.exists(scm_fname), f"Could not find {scm_fname}"
            fp = open(scm_fname)
            query_scm = fp.read()
            query = language.query(query_scm)

        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Parsing documents into nodes"
        )

        for node in nodes_with_progress:
            text = node.text
            tree = parser.parse(bytes(text, "utf-8"))

            if self.signature_identifiers is None:
                assert query is not None
                self.signature_identifiers = {}
                tag_to_type = {}
                captures = query.captures(tree.root_node)
                for _node, _tag in captures:
                    tag_to_type[_tag] = _node.type
                    if _tag.startswith("name.definition"):
                        # ignore name.
                        parent_tag = _tag[5:]
                        assert parent_tag in tag_to_type
                        parent_type = tag_to_type[parent_tag]
                        if parent_type not in self.signature_identifiers:
                            self.signature_identifiers[parent_type] = (
                                _SignatureCaptureOptions(name_identifier=_node.type)
                            )

            if (
                not tree.root_node.children
                or tree.root_node.children[0].type != "ERROR"
            ):
                # Chunk the code
                _chunks = self._chunk_node(tree.root_node, node.text)
                assert _chunks.this_document is not None, "Root node must be a chunk"
                chunks = _chunks.all_documents

                # Add your metadata to the chunks here
                for chunk in chunks:
                    chunk.metadata = {
                        "language": self.language,
                        **chunk.metadata,
                        **node.metadata,
                    }
                    chunk.relationships[NodeRelationship.SOURCE] = (
                        node.as_related_node_info()
                    )

                if self.skeleton:
                    self._skeletonize_list(chunks)

                # Now further split the code by lines and characters
                # TODO: Test this and the relationships it creates
                if self.code_splitter:
                    new_nodes = []
                    for original_node in chunks:
                        new_split_nodes = self.code_splitter.get_nodes_from_documents(
                            [original_node], show_progress=show_progress, **kwargs
                        )

                        if not new_split_nodes:
                            continue

                        # Force the first new_split_node to have the
                        # same id as the original_node
                        new_split_nodes[0].id_ = original_node.id_

                        # Add the UUID of the next node to the end of all nodes
                        for i, new_split_node in enumerate(new_split_nodes[:-1]):
                            new_split_node.text = (
                                new_split_node.text
                                + "\n"
                                + self._create_comment_line(new_split_nodes[i + 1], 0)
                            ).strip()

                        # Add the UUID of the previous node to the beginning of all nodes
                        for i, new_split_node in enumerate(new_split_nodes[1:]):
                            new_split_node.text = (
                                self._create_comment_line(new_split_nodes[i])
                                + new_split_node.text
                            ).strip()

                        # Add the parent child info to all the new_nodes_
                        # derived from node
                        for new_split_node in new_split_nodes:
                            new_split_node.relationships[NodeRelationship.CHILD] = (
                                original_node.child_nodes
                            )  # type: ignore
                            new_split_node.relationships[NodeRelationship.PARENT] = (
                                original_node.parent_node
                            )  # type: ignore

                        # Go through chunks and replace all
                        # instances of node.node_id in relationships
                        # with new_nodes_[0].node_id
                        for old_node in chunks:
                            # Handle child nodes, which are a list
                            new_children = []
                            for old_nodes_child in old_node.child_nodes or []:
                                if old_nodes_child.node_id == original_node.node_id:
                                    new_children.append(
                                        new_split_nodes[0].as_related_node_info()
                                    )
                                new_children.append(old_nodes_child)
                            old_node.relationships[NodeRelationship.CHILD] = (
                                new_children
                            )

                            # Handle parent node
                            if (
                                old_node.parent_node
                                and old_node.parent_node.node_id
                                == original_node.node_id
                            ):
                                old_node.relationships[NodeRelationship.PARENT] = (
                                    new_split_nodes[0].as_related_node_info()
                                )

                        # Now save new_nodes_
                        new_nodes += new_split_nodes

                    chunks = new_nodes

                # Or just extract metadata
                if self.metadata_extractor:
                    chunks = self.metadata_extractor.process_nodes(  # type: ignore
                        chunks
                    )

                out += chunks
            else:
                raise ValueError(f"Could not parse code with language {self.language}.")

        return out

    @staticmethod
    def_get_indentation(text: str) -> Tuple[str, int, int]:
        indent_char = None
        minimum_chain = None

        # Check that text is at least 1 line long
        text_split = text.splitlines()
        if len(text_split) == 0:
            raise ValueError("Text should be at least one line long.")

        for line in text_split:
            stripped_line = line.lstrip()

            if stripped_line:
                # Get whether it's tabs or spaces
                spaces_count = line.count(" ", 0, len(line) - len(stripped_line))
                tabs_count = line.count("\t", 0, len(line) - len(stripped_line))

                if not indent_char:
                    if spaces_count:
                        indent_char = " "
                    if tabs_count:
                        indent_char = "\t"

                # Detect mixed indentation.
                if spaces_count  0 and tabs_count  0:
                    raise ValueError("Mixed indentation found.")
                if indent_char == " " and tabs_count  0:
                    raise ValueError("Mixed indentation found.")
                if indent_char == "\t" and spaces_count  0:
                    raise ValueError("Mixed indentation found.")

                # Get the minimum chain of indent_char
                if indent_char:
                    char_count = line.count(
                        indent_char, 0, len(line) - len(stripped_line)
                    )
                    if minimum_chain is not None:
                        if char_count  0:
                            minimum_chain = min(char_count, minimum_chain)
                    else:
                        if char_count  0:
                            minimum_chain = char_count

        # Handle edge case
        if indent_char is None:
            indent_char = " "
        if minimum_chain is None:
            minimum_chain = 4

        # Get the first indent count
        first_line = text_split[0]
        first_indent_count = 0
        for char in first_line:
            if char == indent_char:
                first_indent_count += 1
            else:
                break

        # Return the default indent level if only one indentation level was found.
        return indent_char, minimum_chain, first_indent_count // minimum_chain

    @staticmethod
    def_get_comment_text(node: TextNode) -> str:
"""Gets just the natural language text for a skeletonize comment."""
        return f"Code replaced for brevity. See node_id {node.node_id}"

    @classmethod
    def_create_comment_line(cls, node: TextNode, indention_lvl: int = -1) -> str:
"""
        Creates a comment line for a node.

        Sometimes we don't use this in a loop because it requires recalculating
        a lot of the same information. But it is handy.
        """
        # Create the text to replace the child_node.text with
        language = node.metadata["language"]
        if language not in _COMMENT_OPTIONS:
            # TODO: Create a contribution message
            raise KeyError("Language not yet supported. Please contribute!")
        comment_options = _COMMENT_OPTIONS[language]
        (
            indentation_char,
            indentation_count_per_lvl,
            first_indentation_lvl,
        ) = cls._get_indentation(node.text)
        if indention_lvl != -1:
            first_indentation_lvl = indention_lvl
        else:
            first_indentation_lvl += 1
        return (
            indentation_char * indentation_count_per_lvl * first_indentation_lvl
            + comment_options.comment_template.format(cls._get_comment_text(node))
            + "\n"
        )

    @classmethod
    def_get_replacement_text(cls, child_node: TextNode) -> str:
"""
        Manufactures a the replacement text to use to skeletonize a given child node.
        """
        signature = child_node.metadata["inclusive_scopes"][-1]["signature"]
        language = child_node.metadata["language"]
        if language not in _COMMENT_OPTIONS:
            # TODO: Create a contribution message
            raise KeyError("Language not yet supported. Please contribute!")
        comment_options = _COMMENT_OPTIONS[language]

        # Create the text to replace the child_node.text with
        (
            indentation_char,
            indentation_count_per_lvl,
            first_indentation_lvl,
        ) = cls._get_indentation(child_node.text)

        # Start with a properly indented signature
        replacement_txt = (
            indentation_char * indentation_count_per_lvl * first_indentation_lvl
            + signature
        )

        # Add brackets if necessary. Expandable in the
        # future to other methods of scoping.
        if comment_options.scope_method == _ScopeMethod.BRACKETS:
            replacement_txt += " {\n"
            replacement_txt += (
                indentation_char
                * indentation_count_per_lvl
                * (first_indentation_lvl + 1)
                + comment_options.comment_template.format(
                    cls._get_comment_text(child_node)
                )
                + "\n"
            )
            replacement_txt += (
                indentation_char * indentation_count_per_lvl * first_indentation_lvl
                + "}"
            )

        elif comment_options.scope_method == _ScopeMethod.INDENTATION:
            replacement_txt += "\n"
            replacement_txt += indentation_char * indentation_count_per_lvl * (
                first_indentation_lvl + 1
            ) + comment_options.comment_template.format(
                cls._get_comment_text(child_node)
            )

        elif comment_options.scope_method == _ScopeMethod.HTML_END_TAGS:
            tag_name = child_node.metadata["inclusive_scopes"][-1]["name"]
            end_tag = f"</{tag_name}>"
            replacement_txt += "\n"
            replacement_txt += (
                indentation_char
                * indentation_count_per_lvl
                * (first_indentation_lvl + 1)
                + comment_options.comment_template.format(
                    cls._get_comment_text(child_node)
                )
                + "\n"
            )
            replacement_txt += (
                indentation_char * indentation_count_per_lvl * first_indentation_lvl
                + end_tag
            )

        else:
            raise KeyError(f"Unrecognized enum value {comment_options.scope_method}")

        return replacement_txt

    @classmethod
    def_skeletonize(cls, parent_node: TextNode, child_node: TextNode) -> None:
"""WARNING: In Place Operation."""
        # Simple protection clauses
        if child_node.text not in parent_node.text:
            raise ValueError("The child text is not contained inside the parent text.")
        if child_node.node_id not in (c.node_id for c in parent_node.child_nodes or []):
            raise ValueError("The child node is not a child of the parent node.")

        # Now do the replacement
        replacement_text = cls._get_replacement_text(child_node=child_node)

        index = parent_node.text.find(child_node.text)
        # If the text is found, replace only the first occurrence
        if index != -1:
            parent_node.text = (
                parent_node.text[:index]
                + replacement_text
                + parent_node.text[index + len(child_node.text) :]
            )

    @classmethod
    def_skeletonize_list(cls, nodes: List[TextNode]) -> None:
        # Create a convenient map for mapping node id's to nodes
        node_id_map = {n.node_id: n for n in nodes}

        defrecur(node: TextNode) -> None:
            # If any children exist, skeletonize ourselves, starting at the root DFS
            for child in node.child_nodes or []:
                child_node = node_id_map[child.node_id]
                cls._skeletonize(parent_node=node, child_node=child_node)
                recur(child_node)

        # Iterate over root nodes and recur
        for n in nodes:
            if n.parent_node is None:
                recur(n)

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyNodeParser.class_name "Permanent link")

```
class_name() -> 

```

Get class name.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/code_hierarchy.py`  
| 
```
202
203
204
205
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Get class name."""
    return "CodeHierarchyNodeParser"

```
 |  
| --- | --- |  
###  get_code_hierarchy_from_nodes `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyNodeParser.get_code_hierarchy_from_nodes "Permanent link")

```
get_code_hierarchy_from_nodes(
    nodes: Sequence[], max_depth:  = -1
) -> Tuple[[, ], ]

```

Creates a code hierarchy appropriate to put into a tool description or context to make it easier to search for code.
Call after `get_nodes_from_documents` and pass that output to this function.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/code_hierarchy.py`  
| 
```
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
```
 | 
```
@staticmethod
defget_code_hierarchy_from_nodes(
    nodes: Sequence[BaseNode],
    max_depth: int = -1,
) -> Tuple[Dict[str, Any], str]:
"""
    Creates a code hierarchy appropriate to put into a tool description or context
    to make it easier to search for code.

    Call after `get_nodes_from_documents` and pass that output to this function.
    """
    out: Dict[str, Any] = defaultdict(dict)

    defget_subdict(keys: List[str]) -> Dict[str, Any]:
        # Get the dictionary we are operating on
        this_dict = out
        for key in keys:
            if key not in this_dict:
                this_dict[key] = defaultdict(dict)
            this_dict = this_dict[key]
        return this_dict

    defrecur_inclusive_scope(node: BaseNode, i: int, keys: List[str]) -> None:
        if "inclusive_scopes" not in node.metadata:
            raise KeyError("inclusive_scopes not in node.metadata")
        if i >= len(node.metadata["inclusive_scopes"]):
            return
        scope = node.metadata["inclusive_scopes"][i]

        this_dict = get_subdict(keys)

        if scope["name"] not in this_dict:
            this_dict[scope["name"]] = defaultdict(dict)

        if i  max_depth or max_depth == -1:
            recur_inclusive_scope(node, i + 1, [*keys, scope["name"]])

    defdict_to_markdown(d: Dict[str, Any], depth: int = 0) -> str:
        markdown = ""
        indent = "  " * depth  # Two spaces per depth level

        for key, value in d.items():
            if isinstance(value, dict):  # Check if value is a dict
                # Add the key with a bullet point and increase depth for nested dicts
                markdown += f"{indent}- {key}\n{dict_to_markdown(value,depth+1)}"
            else:
                # Handle non-dict items if necessary
                markdown += f"{indent}- {key}: {value}\n"

        return markdown

    for node in nodes:
        filepath = node.metadata["filepath"].split("/")
        filepath[-1] = filepath[-1].split(".")[0]
        recur_inclusive_scope(node, 0, filepath)

    return out, dict_to_markdown(out)

```
 |  
| --- | --- |  
##  CodeHierarchyKeywordQueryEngine [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyKeywordQueryEngine "Permanent link")
Bases: 
A keyword table made specifically to work with the code hierarchy node parser.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/query_engine.py`  
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
```
 | 
```
classCodeHierarchyKeywordQueryEngine(CustomQueryEngine):
"""A keyword table made specifically to work with the code hierarchy node parser."""

    nodes: Sequence[BaseNode]
    node_dict: Optional[Dict[str, Tuple[int, BaseNode]]] = None
    repo_map_depth: int = -1
    include_repo_map: bool = True
    repo_map: Optional[Tuple[Dict[str, Any], str]] = None
    tool_instructions: str = DEFAULT_TOOL_INSTRUCTIONS

    def_setup_node_dict(self) -> None:
"""Initialize the index."""
        self.node_dict = {}
        for node in self.nodes:
            keys = self._extract_keywords_from_node(node)
            for key in keys:
                self.node_dict[key] = (node.metadata["start_byte"], node.text)
        self.repo_map = CodeHierarchyNodeParser.get_code_hierarchy_from_nodes(
            self.nodes, max_depth=self.repo_map_depth
        )

    def_extract_keywords_from_node(self, node: BaseNode) -> Set[str]:
"""Determine the keywords associated with the node in the index."""
        keywords = self._extract_uuid_from_node(node)
        keywords |= self._extract_module_from_node(node)
        keywords |= self._extract_name_from_node(node)
        return keywords

    def_extract_uuid_from_node(self, node: BaseNode) -> Set[str]:
"""Extract the uuid from the node."""
        return {node.id_}

    def_extract_module_from_node(self, node: BaseNode) -> Set[str]:
"""Extract the module name from the node."""
        keywords = set()
        if not node.metadata["inclusive_scopes"]:
            path = Path(node.metadata["filepath"])
            name = path.name
            name = re.sub(r"\..*$", "", name)
            if name in self.node_dict:
                its_start_byte, _ = self.node_dict[name]
                if node.metadata["start_byte"]  its_start_byte:
                    keywords.add(name)
            else:
                keywords.add(name)
        return keywords

    def_extract_name_from_node(self, node: BaseNode) -> Set[str]:
"""Extract the name and signature from the node."""
        keywords = set()
        if node.metadata["inclusive_scopes"]:
            name = node.metadata["inclusive_scopes"][-1]["name"]
            start_byte = node.metadata["start_byte"]
            if name in self.node_dict:
                its_start_byte, _ = self.node_dict[name]
                if start_byte  its_start_byte:
                    keywords.add(name)
            else:
                keywords.add(name)
        return keywords

    defcustom_query(self, query: str) -> str:
"""
        Query the index. Only use exact matches.
        If there is no exact match, but there is one for a parent, returns the parent.
        """
        if self.node_dict is None or self.repo_map is None:
            self._setup_node_dict()

        defget_all_dict_recursive(inp: Dict[str, Any]) -> Set[str]:
"""Get all keys and values from a dictionary of dictionaries recursively."""
            kvs = set()
            for key, value in inp.items():
                kvs.add(key)
                if isinstance(value, dict):
                    kvs |= get_all_dict_recursive(value)
                else:
                    kvs.add(value)
            return kvs

        defget_parent_dict_recursive(inp: Dict[str, Any], query: str) -> str:
"""Get the parent of a key in a dictionary of dictionaries recursively."""
            for key, value in inp.items():
                if isinstance(value, dict):
                    if query in value:
                        return key
                    else:
                        parent = get_parent_dict_recursive(value, query)
                        if parent is not None:
                            return parent
            return None

        if query in self.node_dict:
            return self.node_dict[query][1]

        kvs = get_all_dict_recursive(self.repo_map[0])
        if query not in kvs:
            return None
        parent_query = query
        while parent_query not in self.node_dict:
            parent_query = get_parent_dict_recursive(self.repo_map[0], parent_query)
            if parent_query is None:
                return "None"

        # After finding the parent_query, ensure it's in self.node_dict before accessing
        if parent_query in self.node_dict:
            return self.node_dict[parent_query][1]
        else:
            return "None"

    defget_tool_instructions(self) -> str:
"""Get the tool instructions."""
        if self.node_dict is None or self.repo_map is None:
            self._setup_node_dict()
        return self.tool_instructions.format(
            repo_map=self.repo_map[1] if self.include_repo_map else ""
        )

    defas_langchain_tool(
        self,
        **tool_kwargs: Any,
    ) -> "LlamaIndexTool":
"""
        Return the index as a langchain tool.
        Set a repo map depth of -1 to include all nodes.
        otherwise set the depth to the desired max depth.
        """
        fromllama_index.core.langchain_helpers.agentsimport LlamaIndexTool

        if self.node_dict is None or self.repo_map is None:
            self._setup_node_dict()
        return LlamaIndexTool(
            name="Code Search",
            description=self.get_tool_instructions(),
            query_engine=self,
            **tool_kwargs,
        )

```
 |  
| --- | --- |  
###  custom_query [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyKeywordQueryEngine.custom_query "Permanent link")

```
custom_query(query: ) -> 

```

Query the index. Only use exact matches. If there is no exact match, but there is one for a parent, returns the parent.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/query_engine.py`  
| 
```
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
```
 | 
```
defcustom_query(self, query: str) -> str:
"""
    Query the index. Only use exact matches.
    If there is no exact match, but there is one for a parent, returns the parent.
    """
    if self.node_dict is None or self.repo_map is None:
        self._setup_node_dict()

    defget_all_dict_recursive(inp: Dict[str, Any]) -> Set[str]:
"""Get all keys and values from a dictionary of dictionaries recursively."""
        kvs = set()
        for key, value in inp.items():
            kvs.add(key)
            if isinstance(value, dict):
                kvs |= get_all_dict_recursive(value)
            else:
                kvs.add(value)
        return kvs

    defget_parent_dict_recursive(inp: Dict[str, Any], query: str) -> str:
"""Get the parent of a key in a dictionary of dictionaries recursively."""
        for key, value in inp.items():
            if isinstance(value, dict):
                if query in value:
                    return key
                else:
                    parent = get_parent_dict_recursive(value, query)
                    if parent is not None:
                        return parent
        return None

    if query in self.node_dict:
        return self.node_dict[query][1]

    kvs = get_all_dict_recursive(self.repo_map[0])
    if query not in kvs:
        return None
    parent_query = query
    while parent_query not in self.node_dict:
        parent_query = get_parent_dict_recursive(self.repo_map[0], parent_query)
        if parent_query is None:
            return "None"

    # After finding the parent_query, ensure it's in self.node_dict before accessing
    if parent_query in self.node_dict:
        return self.node_dict[parent_query][1]
    else:
        return "None"

```
 |  
| --- | --- |  
###  get_tool_instructions [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyKeywordQueryEngine.get_tool_instructions "Permanent link")

```
get_tool_instructions() -> 

```

Get the tool instructions.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/query_engine.py`  
| 
```
132
133
134
135
136
137
138
```
 | 
```
defget_tool_instructions(self) -> str:
"""Get the tool instructions."""
    if self.node_dict is None or self.repo_map is None:
        self._setup_node_dict()
    return self.tool_instructions.format(
        repo_map=self.repo_map[1] if self.include_repo_map else ""
    )

```
 |  
| --- | --- |  
###  as_langchain_tool [#](https://developers.llamaindex.ai/python/framework-api-reference/packs/code_hierarchy/#llama_index.packs.code_hierarchy.CodeHierarchyKeywordQueryEngine.as_langchain_tool "Permanent link")

```
as_langchain_tool(**tool_kwargs: ) -> LlamaIndexTool

```

Return the index as a langchain tool. Set a repo map depth of -1 to include all nodes. otherwise set the depth to the desired max depth.
Source code in `llama-index-packs/llama-index-packs-code-hierarchy/llama_index/packs/code_hierarchy/query_engine.py`  
| 
```
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
```
 | 
```
defas_langchain_tool(
    self,
    **tool_kwargs: Any,
) -> "LlamaIndexTool":
"""
    Return the index as a langchain tool.
    Set a repo map depth of -1 to include all nodes.
    otherwise set the depth to the desired max depth.
    """
    fromllama_index.core.langchain_helpers.agentsimport LlamaIndexTool

    if self.node_dict is None or self.repo_map is None:
        self._setup_node_dict()
    return LlamaIndexTool(
        name="Code Search",
        description=self.get_tool_instructions(),
        query_engine=self,
        **tool_kwargs,
    )

```
 |  
| --- | --- |  
options: members: - CodeHierarchyAgentPack
