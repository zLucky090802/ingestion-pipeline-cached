# Simple directory reader
Simple reader that reads files of different formats from a directory.
##  FileSystemReaderMixin [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.FileSystemReaderMixin "Permanent link")
Bases: 
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
classFileSystemReaderMixin(ABC):
    @abstractmethod
    defread_file_content(self, input_file: Path, **kwargs: Any) -> bytes:
"""
        Read the bytes content of a file.

        Args:
            input_file (Path): Path to the file.

        Returns:
            bytes: File content.

        """

    async defaread_file_content(
        self, input_file: Path, **kwargs: Any
    ) -> bytes:  # pragma: no cover
"""
        A thin wrapper around read_file_content.

        Args:
            input_file (Path): Path to the file.

        Returns:
            bytes: File content.

        """
        return self.read_file_content(input_file, **kwargs)

```
 |  
| --- | --- |  
###  read_file_content `abstractmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.FileSystemReaderMixin.read_file_content "Permanent link")

```
read_file_content(input_file: , **kwargs: ) -> bytes

```

Read the bytes content of a file.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_file`  |  `Path`  |  Path to the file.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `bytes`  |  `bytes`  |  File content.  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
```
 | 
```
@abstractmethod
defread_file_content(self, input_file: Path, **kwargs: Any) -> bytes:
"""
    Read the bytes content of a file.

    Args:
        input_file (Path): Path to the file.

    Returns:
        bytes: File content.

    """

```
 |  
| --- | --- |  
###  aread_file_content [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.FileSystemReaderMixin.aread_file_content "Permanent link")

```
aread_file_content(
    input_file: , **kwargs: 
) -> bytes

```

A thin wrapper around read_file_content.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_file`  |  `Path`  |  Path to the file.  |  _required_  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `bytes`  |  `bytes`  |  File content.  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
async defaread_file_content(
    self, input_file: Path, **kwargs: Any
) -> bytes:  # pragma: no cover
"""
    A thin wrapper around read_file_content.

    Args:
        input_file (Path): Path to the file.

    Returns:
        bytes: File content.

    """
    return self.read_file_content(input_file, **kwargs)

```
 |  
| --- | --- |  
##  SimpleDirectoryReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.SimpleDirectoryReader "Permanent link")
Bases: , , 
Simple directory reader.
Load files from file directory. Automatically select the best file reader given file extensions.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_dir`  |  `Union[Path, str]`  |  Path to the directory.  |  `None`  |  
|  `input_files`  |  `List`  |  List of file paths to read (Optional; overrides input_dir, exclude)  |  `None`  |  
|  `exclude`  |  `List`  |  glob of python file paths to exclude (Optional)  |  `None`  |  
|  `exclude_hidden`  |  `bool`  |  Whether to exclude hidden files (dotfiles).  |  `True`  |  
|  `exclude_empty`  |  `bool`  |  Whether to exclude empty files (Optional).  |  `False`  |  
|  `encoding`  |  Encoding of the files. Default is utf-8.  |  `'utf-8'`  |  
|  `errors`  |  how encoding and decoding errors are to be handled, see https://docs.python.org/3/library/functions.html#open  |  `'ignore'`  |  
|  `recursive`  |  `bool`  |  Whether to recursively search in subdirectories. False by default.  |  `False`  |  
|  `filename_as_id`  |  `bool`  |  Whether to use the filename as the document id. False by default.  |  `False`  |  
|  `required_exts`  |  `Optional[List[str]]`  |  List of required extensions. Default is None.  |  `None`  |  
|  `file_extractor`  |  `Optional[Dict[str, BaseReader[](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader "BaseReader \(llama_index.core.readers.base.BaseReader\)")]]`  |  A mapping of file extension to a BaseReader class that specifies how to convert that file to text. If not specified, use default from DEFAULT_FILE_READER_CLS.  |  `None`  |  
|  `num_files_limit`  |  `Optional[int]`  |  Maximum number of files to read. Default is None.  |  `None`  |  
|  `file_metadata`  |  `Optional[Callable[[str], Dict]]`  |  A function that takes in a filename and returns a Dict of metadata for the Document. Default is None.  |  `None`  |  
|  `raise_on_error`  |  `bool`  |  Whether to raise an error if a file cannot be read.  |  `False`  |  
|  `Optional[AbstractFileSystem]`  |  File system to use. Defaults  |  `None`  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
```
 | 
```
classSimpleDirectoryReader(BaseReader, ResourcesReaderMixin, FileSystemReaderMixin):
"""
    Simple directory reader.

    Load files from file directory.
    Automatically select the best file reader given file extensions.

    Args:
        input_dir (Union[Path, str]): Path to the directory.
        input_files (List): List of file paths to read
            (Optional; overrides input_dir, exclude)
        exclude (List): glob of python file paths to exclude (Optional)
        exclude_hidden (bool): Whether to exclude hidden files (dotfiles).
        exclude_empty (bool): Whether to exclude empty files (Optional).
        encoding (str): Encoding of the files.
            Default is utf-8.
        errors (str): how encoding and decoding errors are to be handled,
              see https://docs.python.org/3/library/functions.html#open
        recursive (bool): Whether to recursively search in subdirectories.
            False by default.
        filename_as_id (bool): Whether to use the filename as the document id.
            False by default.
        required_exts (Optional[List[str]]): List of required extensions.
            Default is None.
        file_extractor (Optional[Dict[str, BaseReader]]): A mapping of file
            extension to a BaseReader class that specifies how to convert that file
            to text. If not specified, use default from DEFAULT_FILE_READER_CLS.
        num_files_limit (Optional[int]): Maximum number of files to read.
            Default is None.
        file_metadata (Optional[Callable[[str], Dict]]): A function that takes
            in a filename and returns a Dict of metadata for the Document.
            Default is None.
        raise_on_error (bool): Whether to raise an error if a file cannot be read.
        fs (Optional[fsspec.AbstractFileSystem]): File system to use. Defaults
        to using the local file system. Can be changed to use any remote file system
        exposed via the fsspec interface.

    """

    supported_suffix_fn: Callable = _try_loading_included_file_formats

    def__init__(
        self,
        input_dir: Optional[Union[Path, str]] = None,
        input_files: Optional[list] = None,
        exclude: Optional[list] = None,
        exclude_hidden: bool = True,
        exclude_empty: bool = False,
        errors: str = "ignore",
        recursive: bool = False,
        encoding: str = "utf-8",
        filename_as_id: bool = False,
        required_exts: Optional[list[str]] = None,
        file_extractor: Optional[dict[str, BaseReader]] = None,
        num_files_limit: Optional[int] = None,
        file_metadata: Optional[Callable[[str], dict]] = None,
        raise_on_error: bool = False,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> None:
"""Initialize with parameters."""
        super().__init__()

        if not input_dir and not input_files:
            raise ValueError("Must provide either `input_dir` or `input_files`.")

        self.fs = fs or get_default_fs()
        self.errors = errors
        self.encoding = encoding

        self.exclude = exclude
        self.recursive = recursive
        self.exclude_hidden = exclude_hidden
        self.exclude_empty = exclude_empty
        self.required_exts = required_exts
        self.num_files_limit = num_files_limit
        self.raise_on_error = raise_on_error
        _Path = Path if is_default_fs(self.fs) else PurePosixPath

        if input_files:
            self.input_files = []
            for path in input_files:
                if not self.fs.isfile(path):
                    raise ValueError(f"File {path} does not exist.")
                input_file = _Path(path)
                self.input_files.append(input_file)
        elif input_dir:
            if not self.fs.isdir(input_dir):
                raise ValueError(f"Directory {input_dir} does not exist.")
            self.input_dir = _Path(input_dir)
            self.exclude = exclude
            self.input_files = self._add_files(self.input_dir)

        self.file_extractor = file_extractor or {}
        self.file_metadata = file_metadata or _DefaultFileMetadataFunc(self.fs)
        self.filename_as_id = filename_as_id

    defis_hidden(self, path: Path | PurePosixPath) -> bool:
        return any(
            part.startswith(".") and part not in [".", ".."] for part in path.parts
        )

    defis_empty_file(self, path: Path | PurePosixPath) -> bool:
        return self.fs.isfile(str(path)) and self.fs.info(str(path)).get("size", 0) == 0

    def_is_directory(self, path: Path | PurePosixPath) -> bool:
"""
        Check if a path is a directory, with special handling for S3 filesystems.

        For S3 filesystems, directories are often represented as 0-byte objects
        ending with '/'. This method provides more reliable directory detection
        than fs.isdir() alone.
        """
        try:
            # First try the standard isdir check
            if self.fs.isdir(path):
                return True

            # For non-default filesystems (like S3), also check for directory placeholders
            if not is_default_fs(self.fs):
                try:
                    info = self.fs.info(str(path))
                    # Check if it's a 0-byte object ending with '/'
                    # This is how S3 typically represents directory placeholders
                    if (
                        info.get("size", 0) == 0
                        and str(path).endswith("/")
                        and info.get("type") != "file"
                    ):
                        return True
                except Exception:
                    # If we can't get info, fall back to the original isdir check
                    pass

            return False
        except Exception:
            # If anything fails, assume it's not a directory to be safe
            return False

    def_add_files(self, input_dir: Path | PurePosixPath) -> list[Path | PurePosixPath]:
"""Add files."""
        all_files: set[Path | PurePosixPath] = set()
        rejected_files: set[Path | PurePosixPath] = set()
        rejected_dirs: set[Path | PurePosixPath] = set()
        # Default to POSIX paths for non-default file systems (e.g. S3)
        _Path = Path if is_default_fs(self.fs) else PurePosixPath

        if self.exclude is not None:
            for excluded_pattern in self.exclude:
                if self.recursive:
                    # Recursive glob
                    excluded_glob = _Path(input_dir) / _Path("**") / excluded_pattern
                else:
                    # Non-recursive glob
                    excluded_glob = _Path(input_dir) / excluded_pattern
                for file in self.fs.glob(str(excluded_glob)):
                    if self.fs.isdir(file):
                        rejected_dirs.add(_Path(str(file)))
                    else:
                        rejected_files.add(_Path(str(file)))

        file_refs: list[Union[Path, PurePosixPath]] = []
        limit = (
            self.num_files_limit
            if self.num_files_limit is not None and self.num_files_limit  0
            else None
        )
        c = 0
        depth = 1000 if self.recursive else 1
        for root, _, files in self.fs.walk(
            str(input_dir), topdown=True, maxdepth=depth
        ):
            for file in files:
                c += 1
                if limit and c  limit:
                    break
                file_refs.append(_Path(root, file))

        for ref in file_refs:
            # Manually check if file is hidden or directory instead of
            # in glob for backwards compatibility.
            is_dir = self._is_directory(ref)
            skip_because_hidden = self.exclude_hidden and self.is_hidden(ref)
            skip_because_empty = self.exclude_empty and self.is_empty_file(ref)
            skip_because_bad_ext = (
                self.required_exts is not None and ref.suffix not in self.required_exts
            )
            skip_because_excluded = ref in rejected_files
            if not skip_because_excluded:
                if is_dir:
                    ref_parent_dir = ref
                else:
                    ref_parent_dir = self.fs._parent(ref)
                for rejected_dir in rejected_dirs:
                    if str(ref_parent_dir).startswith(str(rejected_dir)):
                        skip_because_excluded = True
                        logger.debug(
                            "Skipping %s because it in parent dir %s which is in %s",
                            ref,
                            ref_parent_dir,
                            rejected_dir,
                        )
                        break

            if (
                is_dir
                or skip_because_hidden
                or skip_because_bad_ext
                or skip_because_excluded
                or skip_because_empty
            ):
                continue
            else:
                all_files.add(ref)

        new_input_files = sorted(all_files)

        if len(new_input_files) == 0:
            raise ValueError(f"No files found in {input_dir}.")

        # print total number of files added
        logger.debug(
            f"> [SimpleDirectoryReader] Total files added: {len(new_input_files)}"
        )

        return new_input_files

    def_exclude_metadata(self, documents: list[Document]) -> list[Document]:
"""
        Exclude metadata from documents.

        Args:
            documents (List[Document]): List of documents.

        """
        for doc in documents:
            # Keep only metadata['file_path'] in both embedding and llm content
            # str, which contain extreme important context that about the chunks.
            # Dates is provided for convenience of postprocessor such as
            # TimeWeightedPostprocessor, but excluded for embedding and LLMprompts
            doc.excluded_embed_metadata_keys.extend(
                [
                    "file_name",
                    "file_type",
                    "file_size",
                    "creation_date",
                    "last_modified_date",
                    "last_accessed_date",
                ]
            )
            doc.excluded_llm_metadata_keys.extend(
                [
                    "file_name",
                    "file_type",
                    "file_size",
                    "creation_date",
                    "last_modified_date",
                    "last_accessed_date",
                ]
            )

        return documents

    deflist_resources(self, *args: Any, **kwargs: Any) -> list[str]:
"""List files in the given filesystem."""
        return [str(x) for x in self.input_files]

    defget_resource_info(self, resource_id: str, *args: Any, **kwargs: Any) -> dict:
        info_result = self.fs.info(resource_id)

        creation_date = _format_file_timestamp(
            info_result.get("created"), include_time=True
        )
        last_modified_date = _format_file_timestamp(
            info_result.get("mtime"), include_time=True
        )

        info_dict = {
            "file_path": resource_id,
            "file_size": info_result.get("size"),
            "creation_date": creation_date,
            "last_modified_date": last_modified_date,
        }

        # Ignore None values
        return {
            meta_key: meta_value
            for meta_key, meta_value in info_dict.items()
            if meta_value is not None
        }

    defload_resource(
        self, resource_id: str, *args: Any, **kwargs: Any
    ) -> list[Document]:
        file_metadata = kwargs.get("file_metadata", self.file_metadata)
        file_extractor = kwargs.get("file_extractor", self.file_extractor)
        filename_as_id = kwargs.get("filename_as_id", self.filename_as_id)
        encoding = kwargs.get("encoding", self.encoding)
        errors = kwargs.get("errors", self.errors)
        raise_on_error = kwargs.get("raise_on_error", self.raise_on_error)
        fs = kwargs.get("fs", self.fs)

        _Path = Path if is_default_fs(fs) else PurePosixPath

        return SimpleDirectoryReader.load_file(
            input_file=_Path(resource_id),
            file_metadata=file_metadata,
            file_extractor=file_extractor,
            filename_as_id=filename_as_id,
            encoding=encoding,
            errors=errors,
            raise_on_error=raise_on_error,
            fs=fs,
            **kwargs,
        )

    async defaload_resource(
        self, resource_id: str, *args: Any, **kwargs: Any
    ) -> list[Document]:
        file_metadata = kwargs.get("file_metadata", self.file_metadata)
        file_extractor = kwargs.get("file_extractor", self.file_extractor)
        filename_as_id = kwargs.get("filename_as_id", self.filename_as_id)
        encoding = kwargs.get("encoding", self.encoding)
        errors = kwargs.get("errors", self.errors)
        raise_on_error = kwargs.get("raise_on_error", self.raise_on_error)
        fs = kwargs.get("fs", self.fs)
        _Path = Path if is_default_fs(fs) else PurePosixPath

        return await SimpleDirectoryReader.aload_file(
            input_file=_Path(resource_id),
            file_metadata=file_metadata,
            file_extractor=file_extractor,
            filename_as_id=filename_as_id,
            encoding=encoding,
            errors=errors,
            raise_on_error=raise_on_error,
            fs=fs,
            **kwargs,
        )

    defread_file_content(self, input_file: Path, **kwargs: Any) -> bytes:
"""Read file content."""
        fs: fsspec.AbstractFileSystem = kwargs.get("fs", self.fs)
        with fs.open(input_file, errors=self.errors, encoding=self.encoding) as f:
            # default mode is 'rb', we can cast the return value of f.read()
            return cast(bytes, f.read())

    @staticmethod
    defload_file(
        input_file: Path | PurePosixPath,
        file_metadata: Callable[[str], dict],
        file_extractor: dict[str, BaseReader],
        filename_as_id: bool = False,
        encoding: str = "utf-8",
        errors: str = "ignore",
        raise_on_error: bool = False,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> list[Document]:
"""
        Static method for loading file.

        NOTE: necessarily as a static method for parallel processing.

        Args:
            input_file (Path): File path to read
            file_metadata ([Callable[[str], Dict]]): A function that takes
                in a filename and returns a Dict of metadata for the Document.
            file_extractor (Dict[str, BaseReader]): A mapping of file
                extension to a BaseReader class that specifies how to convert that file
                to text.
            filename_as_id (bool): Whether to use the filename as the document id.
            encoding (str): Encoding of the files.
                Default is utf-8.
            errors (str): how encoding and decoding errors are to be handled,
                see https://docs.python.org/3/library/functions.html#open
            raise_on_error (bool): Whether to raise an error if a file cannot be read.
            fs (Optional[fsspec.AbstractFileSystem]): File system to use. Defaults
                to using the local file system. Can be changed to use any remote file system

        Returns:
            List[Document]: loaded documents

        """
        # TODO: make this less redundant
        default_file_reader_cls = SimpleDirectoryReader.supported_suffix_fn()
        default_file_reader_suffix = list(default_file_reader_cls.keys())
        metadata: dict | None = None
        documents: list[Document] = []

        if file_metadata is not None:
            metadata = file_metadata(str(input_file))

        file_suffix = input_file.suffix.lower()
        if file_suffix in default_file_reader_suffix or file_suffix in file_extractor:
            # use file readers
            if file_suffix not in file_extractor:
                # instantiate file reader if not already
                reader_cls = default_file_reader_cls[file_suffix]
                file_extractor[file_suffix] = reader_cls()
            reader = file_extractor[file_suffix]

            # load data -- catch all errors except for ImportError
            try:
                kwargs: dict[str, Any] = {"extra_info": metadata}
                if fs and not is_default_fs(fs):
                    kwargs["fs"] = fs
                docs = reader.load_data(input_file, **kwargs)
            except ImportError as e:
                # ensure that ImportError is raised so user knows
                # about missing dependencies
                raise ImportError(str(e))
            except Exception as e:
                if raise_on_error:
                    raise Exception("Error loading file") frome
                # otherwise, just skip the file and report the error
                print(
                    f"Failed to load file {input_file} with error: {e}. Skipping...",
                    flush=True,
                )
                return []

            # iterate over docs if needed
            if filename_as_id:
                for i, doc in enumerate(docs):
                    doc.id_ = f"{input_file!s}_part_{i}"

            documents.extend(docs)
        else:
            # do standard read
            fs = fs or get_default_fs()
            with fs.open(input_file, errors=errors, encoding=encoding) as f:
                data = cast(bytes, f.read()).decode(encoding, errors=errors)

            doc = Document(text=data, metadata=metadata or {})  # type: ignore
            if filename_as_id:
                doc.id_ = str(input_file)

            documents.append(doc)

        return documents

    @staticmethod
    async defaload_file(
        input_file: Path | PurePosixPath,
        file_metadata: Callable[[str], dict],
        file_extractor: dict[str, BaseReader],
        filename_as_id: bool = False,
        encoding: str = "utf-8",
        errors: str = "ignore",
        raise_on_error: bool = False,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> list[Document]:
"""Load file asynchronously."""
        # TODO: make this less redundant
        default_file_reader_cls = SimpleDirectoryReader.supported_suffix_fn()
        default_file_reader_suffix = list(default_file_reader_cls.keys())
        metadata: dict | None = None
        documents: list[Document] = []

        if file_metadata is not None:
            metadata = file_metadata(str(input_file))

        file_suffix = input_file.suffix.lower()
        if file_suffix in default_file_reader_suffix or file_suffix in file_extractor:
            # use file readers
            if file_suffix not in file_extractor:
                # instantiate file reader if not already
                reader_cls = default_file_reader_cls[file_suffix]
                file_extractor[file_suffix] = reader_cls()
            reader = file_extractor[file_suffix]

            # load data -- catch all errors except for ImportError
            try:
                kwargs: dict[str, Any] = {"extra_info": metadata}
                if fs and not is_default_fs(fs):
                    kwargs["fs"] = fs
                docs = await reader.aload_data(input_file, **kwargs)
            except ImportError as e:
                # ensure that ImportError is raised so user knows
                # about missing dependencies
                raise ImportError(str(e))
            except Exception as e:
                if raise_on_error:
                    raise
                # otherwise, just skip the file and report the error
                print(
                    f"Failed to load file {input_file} with error: {e}. Skipping...",
                    flush=True,
                )
                return []

            # iterate over docs if needed
            if filename_as_id:
                for i, doc in enumerate(docs):
                    doc.id_ = f"{input_file!s}_part_{i}"

            documents.extend(docs)
        else:
            # do standard read
            fs = fs or get_default_fs()
            with fs.open(input_file, errors=errors, encoding=encoding) as f:
                data = cast(bytes, f.read()).decode(encoding, errors=errors)

            doc = Document(text=data, metadata=metadata or {})  # type: ignore
            if filename_as_id:
                doc.id_ = str(input_file)

            documents.append(doc)

        return documents

    defload_data(
        self,
        show_progress: bool = False,
        num_workers: int | None = None,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> list[Document]:
"""
        Load data from the input directory.

        Args:
            show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
            num_workers  (Optional[int]): Number of workers to parallelize data-loading over.
            fs (Optional[fsspec.AbstractFileSystem]): File system to use. If fs was specified
                in the constructor, it will override the fs parameter here.

        Returns:
            List[Document]: A list of documents.

        """
        documents = []

        fs = fs or self.fs
        load_file_with_args = partial(
            SimpleDirectoryReader.load_file,
            file_metadata=self.file_metadata,
            file_extractor=self.file_extractor,
            filename_as_id=self.filename_as_id,
            encoding=self.encoding,
            errors=self.errors,
            raise_on_error=self.raise_on_error,
            fs=fs,
        )

        if num_workers and num_workers  1:
            num_cpus = multiprocessing.cpu_count()
            if num_workers  num_cpus:
                warnings.warn(
                    "Specified num_workers exceed number of CPUs in the system. "
                    "Setting `num_workers` down to the maximum CPU count.",
                    stacklevel=2,
                )
                num_workers = num_cpus

            with multiprocessing.get_context("spawn").Pool(num_workers) as pool:
                map_iterator = cast(
                    Iterable[list[Document]],
                    get_tqdm_iterable(
                        pool.imap(load_file_with_args, self.input_files),
                        show_progress=show_progress,
                        desc="Loading files",
                        total=len(self.input_files),
                    ),
                )
                for result in map_iterator:
                    documents.extend(result)

        else:
            files_to_process = cast(
                list[Union[Path, PurePosixPath]],
                get_tqdm_iterable(
                    self.input_files,
                    show_progress=show_progress,
                    desc="Loading files",
                ),
            )
            for input_file in files_to_process:
                documents.extend(load_file_with_args(input_file))

        return self._exclude_metadata(documents)

    async defaload_data(
        self,
        show_progress: bool = False,
        num_workers: int | None = None,
        fs: fsspec.AbstractFileSystem | None = None,
    ) -> list[Document]:
"""
        Load data from the input directory.

        Args:
            show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
            num_workers  (Optional[int]): Number of workers to parallelize data-loading over.
            fs (Optional[fsspec.AbstractFileSystem]): File system to use. If fs was specified
                in the constructor, it will override the fs parameter here.

        Returns:
            List[Document]: A list of documents.

        """
        files_to_process = self.input_files
        fs = fs or self.fs

        coroutines = [
            SimpleDirectoryReader.aload_file(
                input_file,
                self.file_metadata,
                self.file_extractor,
                self.filename_as_id,
                self.encoding,
                self.errors,
                self.raise_on_error,
                fs,
            )
            for input_file in files_to_process
        ]

        if num_workers:
            document_lists = await run_jobs(
                coroutines, show_progress=show_progress, workers=num_workers
            )
        elif show_progress:
            _asyncio = get_asyncio_module(show_progress=show_progress)
            document_lists = await _asyncio.gather(*coroutines)
        else:
            document_lists = await asyncio.gather(*coroutines)
        documents = [doc for doc_list in document_lists for doc in doc_list]

        return self._exclude_metadata(documents)

    defiter_data(
        self, show_progress: bool = False
    ) -> Generator[list[Document], Any, Any]:
"""
        Load data iteratively from the input directory.

        Args:
            show_progress (bool): Whether to show tqdm progress bars. Defaults to False.

        Returns:
            Generator[List[Document]]: A list of documents.

        """
        files_to_process = cast(
            list[Union[Path, PurePosixPath]],
            get_tqdm_iterable(
                self.input_files,
                show_progress=show_progress,
                desc="Loading files",
            ),
        )
        for input_file in files_to_process:
            documents = SimpleDirectoryReader.load_file(
                input_file=input_file,
                file_metadata=self.file_metadata,
                file_extractor=self.file_extractor,
                filename_as_id=self.filename_as_id,
                encoding=self.encoding,
                errors=self.errors,
                raise_on_error=self.raise_on_error,
                fs=self.fs,
            )

            documents = self._exclude_metadata(documents)

            if len(documents)  0:
                yield documents

```
 |  
| --- | --- |  
###  list_resources [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.SimpleDirectoryReader.list_resources "Permanent link")

```
list_resources(*args: , **kwargs: ) -> []

```

List files in the given filesystem.
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
470
471
472
```
 | 
```
deflist_resources(self, *args: Any, **kwargs: Any) -> list[str]:
"""List files in the given filesystem."""
    return [str(x) for x in self.input_files]

```
 |  
| --- | --- |  
###  read_file_content [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.SimpleDirectoryReader.read_file_content "Permanent link")

```
read_file_content(input_file: , **kwargs: ) -> bytes

```

Read file content.
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
547
548
549
550
551
552
```
 | 
```
defread_file_content(self, input_file: Path, **kwargs: Any) -> bytes:
"""Read file content."""
    fs: fsspec.AbstractFileSystem = kwargs.get("fs", self.fs)
    with fs.open(input_file, errors=self.errors, encoding=self.encoding) as f:
        # default mode is 'rb', we can cast the return value of f.read()
        return cast(bytes, f.read())

```
 |  
| --- | --- |  
###  load_file `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.SimpleDirectoryReader.load_file "Permanent link")

```
load_file(
    input_file:  | PurePosixPath,
    file_metadata: Callable[[], ],
    file_extractor: [, ],
    filename_as_id:  = False,
    encoding:  = "utf-8",
    errors:  = "ignore",
    raise_on_error:  = False,
    fs: AbstractFileSystem | None = None,
) -> []

```

Static method for loading file.
NOTE: necessarily as a static method for parallel processing.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `input_file`  |  `Path`  |  File path to read  |  _required_  |  
|  `file_metadata`  |  `[Callable[[str], Dict]]`  |  A function that takes in a filename and returns a Dict of metadata for the Document.  |  _required_  |  
|  `file_extractor`  |  `Dict[str, BaseReader[](https://developers.llamaindex.ai/python/framework-api-reference/readers/#llama_index.core.readers.base.BaseReader "BaseReader \(llama_index.core.readers.base.BaseReader\)")]`  |  A mapping of file extension to a BaseReader class that specifies how to convert that file to text.  |  _required_  |  
|  `filename_as_id`  |  `bool`  |  Whether to use the filename as the document id.  |  `False`  |  
|  `encoding`  |  Encoding of the files. Default is utf-8.  |  `'utf-8'`  |  
|  `errors`  |  how encoding and decoding errors are to be handled, see https://docs.python.org/3/library/functions.html#open  |  `'ignore'`  |  
|  `raise_on_error`  |  `bool`  |  Whether to raise an error if a file cannot be read.  |  `False`  |  
|  `Optional[AbstractFileSystem]`  |  File system to use. Defaults to using the local file system. Can be changed to use any remote file system  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: loaded documents  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
```
 | 
```
@staticmethod
defload_file(
    input_file: Path | PurePosixPath,
    file_metadata: Callable[[str], dict],
    file_extractor: dict[str, BaseReader],
    filename_as_id: bool = False,
    encoding: str = "utf-8",
    errors: str = "ignore",
    raise_on_error: bool = False,
    fs: fsspec.AbstractFileSystem | None = None,
) -> list[Document]:
"""
    Static method for loading file.

    NOTE: necessarily as a static method for parallel processing.

    Args:
        input_file (Path): File path to read
        file_metadata ([Callable[[str], Dict]]): A function that takes
            in a filename and returns a Dict of metadata for the Document.
        file_extractor (Dict[str, BaseReader]): A mapping of file
            extension to a BaseReader class that specifies how to convert that file
            to text.
        filename_as_id (bool): Whether to use the filename as the document id.
        encoding (str): Encoding of the files.
            Default is utf-8.
        errors (str): how encoding and decoding errors are to be handled,
            see https://docs.python.org/3/library/functions.html#open
        raise_on_error (bool): Whether to raise an error if a file cannot be read.
        fs (Optional[fsspec.AbstractFileSystem]): File system to use. Defaults
            to using the local file system. Can be changed to use any remote file system

    Returns:
        List[Document]: loaded documents

    """
    # TODO: make this less redundant
    default_file_reader_cls = SimpleDirectoryReader.supported_suffix_fn()
    default_file_reader_suffix = list(default_file_reader_cls.keys())
    metadata: dict | None = None
    documents: list[Document] = []

    if file_metadata is not None:
        metadata = file_metadata(str(input_file))

    file_suffix = input_file.suffix.lower()
    if file_suffix in default_file_reader_suffix or file_suffix in file_extractor:
        # use file readers
        if file_suffix not in file_extractor:
            # instantiate file reader if not already
            reader_cls = default_file_reader_cls[file_suffix]
            file_extractor[file_suffix] = reader_cls()
        reader = file_extractor[file_suffix]

        # load data -- catch all errors except for ImportError
        try:
            kwargs: dict[str, Any] = {"extra_info": metadata}
            if fs and not is_default_fs(fs):
                kwargs["fs"] = fs
            docs = reader.load_data(input_file, **kwargs)
        except ImportError as e:
            # ensure that ImportError is raised so user knows
            # about missing dependencies
            raise ImportError(str(e))
        except Exception as e:
            if raise_on_error:
                raise Exception("Error loading file") frome
            # otherwise, just skip the file and report the error
            print(
                f"Failed to load file {input_file} with error: {e}. Skipping...",
                flush=True,
            )
            return []

        # iterate over docs if needed
        if filename_as_id:
            for i, doc in enumerate(docs):
                doc.id_ = f"{input_file!s}_part_{i}"

        documents.extend(docs)
    else:
        # do standard read
        fs = fs or get_default_fs()
        with fs.open(input_file, errors=errors, encoding=encoding) as f:
            data = cast(bytes, f.read()).decode(encoding, errors=errors)

        doc = Document(text=data, metadata=metadata or {})  # type: ignore
        if filename_as_id:
            doc.id_ = str(input_file)

        documents.append(doc)

    return documents

```
 |  
| --- | --- |  
###  aload_file `async` `staticmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.SimpleDirectoryReader.aload_file "Permanent link")

```
aload_file(
    input_file:  | PurePosixPath,
    file_metadata: Callable[[], ],
    file_extractor: [, ],
    filename_as_id:  = False,
    encoding:  = "utf-8",
    errors:  = "ignore",
    raise_on_error:  = False,
    fs: AbstractFileSystem | None = None,
) -> []

```

Load file asynchronously.
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
```
 | 
```
@staticmethod
async defaload_file(
    input_file: Path | PurePosixPath,
    file_metadata: Callable[[str], dict],
    file_extractor: dict[str, BaseReader],
    filename_as_id: bool = False,
    encoding: str = "utf-8",
    errors: str = "ignore",
    raise_on_error: bool = False,
    fs: fsspec.AbstractFileSystem | None = None,
) -> list[Document]:
"""Load file asynchronously."""
    # TODO: make this less redundant
    default_file_reader_cls = SimpleDirectoryReader.supported_suffix_fn()
    default_file_reader_suffix = list(default_file_reader_cls.keys())
    metadata: dict | None = None
    documents: list[Document] = []

    if file_metadata is not None:
        metadata = file_metadata(str(input_file))

    file_suffix = input_file.suffix.lower()
    if file_suffix in default_file_reader_suffix or file_suffix in file_extractor:
        # use file readers
        if file_suffix not in file_extractor:
            # instantiate file reader if not already
            reader_cls = default_file_reader_cls[file_suffix]
            file_extractor[file_suffix] = reader_cls()
        reader = file_extractor[file_suffix]

        # load data -- catch all errors except for ImportError
        try:
            kwargs: dict[str, Any] = {"extra_info": metadata}
            if fs and not is_default_fs(fs):
                kwargs["fs"] = fs
            docs = await reader.aload_data(input_file, **kwargs)
        except ImportError as e:
            # ensure that ImportError is raised so user knows
            # about missing dependencies
            raise ImportError(str(e))
        except Exception as e:
            if raise_on_error:
                raise
            # otherwise, just skip the file and report the error
            print(
                f"Failed to load file {input_file} with error: {e}. Skipping...",
                flush=True,
            )
            return []

        # iterate over docs if needed
        if filename_as_id:
            for i, doc in enumerate(docs):
                doc.id_ = f"{input_file!s}_part_{i}"

        documents.extend(docs)
    else:
        # do standard read
        fs = fs or get_default_fs()
        with fs.open(input_file, errors=errors, encoding=encoding) as f:
            data = cast(bytes, f.read()).decode(encoding, errors=errors)

        doc = Document(text=data, metadata=metadata or {})  # type: ignore
        if filename_as_id:
            doc.id_ = str(input_file)

        documents.append(doc)

    return documents

```
 |  
| --- | --- |  
###  load_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.SimpleDirectoryReader.load_data "Permanent link")

```
load_data(
    show_progress:  = False,
    num_workers:  | None = None,
    fs: AbstractFileSystem | None = None,
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `num_workers`  |  `Optional[int]`  |  Number of workers to parallelize data-loading over.  |  `None`  |  
|  `Optional[AbstractFileSystem]`  |  File system to use. If fs was specified in the constructor, it will override the fs parameter here.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
```
 | 
```
defload_data(
    self,
    show_progress: bool = False,
    num_workers: int | None = None,
    fs: fsspec.AbstractFileSystem | None = None,
) -> list[Document]:
"""
    Load data from the input directory.

    Args:
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
        num_workers  (Optional[int]): Number of workers to parallelize data-loading over.
        fs (Optional[fsspec.AbstractFileSystem]): File system to use. If fs was specified
            in the constructor, it will override the fs parameter here.

    Returns:
        List[Document]: A list of documents.

    """
    documents = []

    fs = fs or self.fs
    load_file_with_args = partial(
        SimpleDirectoryReader.load_file,
        file_metadata=self.file_metadata,
        file_extractor=self.file_extractor,
        filename_as_id=self.filename_as_id,
        encoding=self.encoding,
        errors=self.errors,
        raise_on_error=self.raise_on_error,
        fs=fs,
    )

    if num_workers and num_workers  1:
        num_cpus = multiprocessing.cpu_count()
        if num_workers  num_cpus:
            warnings.warn(
                "Specified num_workers exceed number of CPUs in the system. "
                "Setting `num_workers` down to the maximum CPU count.",
                stacklevel=2,
            )
            num_workers = num_cpus

        with multiprocessing.get_context("spawn").Pool(num_workers) as pool:
            map_iterator = cast(
                Iterable[list[Document]],
                get_tqdm_iterable(
                    pool.imap(load_file_with_args, self.input_files),
                    show_progress=show_progress,
                    desc="Loading files",
                    total=len(self.input_files),
                ),
            )
            for result in map_iterator:
                documents.extend(result)

    else:
        files_to_process = cast(
            list[Union[Path, PurePosixPath]],
            get_tqdm_iterable(
                self.input_files,
                show_progress=show_progress,
                desc="Loading files",
            ),
        )
        for input_file in files_to_process:
            documents.extend(load_file_with_args(input_file))

    return self._exclude_metadata(documents)

```
 |  
| --- | --- |  
###  aload_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.SimpleDirectoryReader.aload_data "Permanent link")

```
aload_data(
    show_progress:  = False,
    num_workers:  | None = None,
    fs: AbstractFileSystem | None = None,
) -> []

```

Load data from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
|  `num_workers`  |  `Optional[int]`  |  Number of workers to parallelize data-loading over.  |  `None`  |  
|  `Optional[AbstractFileSystem]`  |  File system to use. If fs was specified in the constructor, it will override the fs parameter here.  |  `None`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|   |  List[Document]: A list of documents.  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
```
 | 
```
async defaload_data(
    self,
    show_progress: bool = False,
    num_workers: int | None = None,
    fs: fsspec.AbstractFileSystem | None = None,
) -> list[Document]:
"""
    Load data from the input directory.

    Args:
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.
        num_workers  (Optional[int]): Number of workers to parallelize data-loading over.
        fs (Optional[fsspec.AbstractFileSystem]): File system to use. If fs was specified
            in the constructor, it will override the fs parameter here.

    Returns:
        List[Document]: A list of documents.

    """
    files_to_process = self.input_files
    fs = fs or self.fs

    coroutines = [
        SimpleDirectoryReader.aload_file(
            input_file,
            self.file_metadata,
            self.file_extractor,
            self.filename_as_id,
            self.encoding,
            self.errors,
            self.raise_on_error,
            fs,
        )
        for input_file in files_to_process
    ]

    if num_workers:
        document_lists = await run_jobs(
            coroutines, show_progress=show_progress, workers=num_workers
        )
    elif show_progress:
        _asyncio = get_asyncio_module(show_progress=show_progress)
        document_lists = await _asyncio.gather(*coroutines)
    else:
        document_lists = await asyncio.gather(*coroutines)
    documents = [doc for doc_list in document_lists for doc in doc_list]

    return self._exclude_metadata(documents)

```
 |  
| --- | --- |  
###  iter_data [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.SimpleDirectoryReader.iter_data "Permanent link")

```
iter_data(
    show_progress:  = False,
) -> Generator[[], , ]

```

Load data iteratively from the input directory.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `show_progress`  |  `bool`  |  Whether to show tqdm progress bars. Defaults to False.  |  `False`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  Generator[List[Document]]: A list of documents.  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
```
 | 
```
defiter_data(
    self, show_progress: bool = False
) -> Generator[list[Document], Any, Any]:
"""
    Load data iteratively from the input directory.

    Args:
        show_progress (bool): Whether to show tqdm progress bars. Defaults to False.

    Returns:
        Generator[List[Document]]: A list of documents.

    """
    files_to_process = cast(
        list[Union[Path, PurePosixPath]],
        get_tqdm_iterable(
            self.input_files,
            show_progress=show_progress,
            desc="Loading files",
        ),
    )
    for input_file in files_to_process:
        documents = SimpleDirectoryReader.load_file(
            input_file=input_file,
            file_metadata=self.file_metadata,
            file_extractor=self.file_extractor,
            filename_as_id=self.filename_as_id,
            encoding=self.encoding,
            errors=self.errors,
            raise_on_error=self.raise_on_error,
            fs=self.fs,
        )

        documents = self._exclude_metadata(documents)

        if len(documents)  0:
            yield documents

```
 |  
| --- | --- |  
##  default_file_metadata_func [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/simple_directory_reader/#llama_index.core.readers.file.base.default_file_metadata_func "Permanent link")

```
default_file_metadata_func(
    file_path: , fs: AbstractFileSystem | None = None
) -> 

```

Get some handy metadata from filesystem.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `file_path`  |  str: file path in str  |  _required_  |  
Source code in `llama-index-core/llama_index/core/readers/file/base.py`  
| 
```
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
```
 | 
```
defdefault_file_metadata_func(
    file_path: str, fs: fsspec.AbstractFileSystem | None = None
) -> dict:
"""
    Get some handy metadata from filesystem.

    Args:
        file_path: str: file path in str

    """
    fs = fs or get_default_fs()
    stat_result = fs.stat(file_path)

    try:
        file_name = os.path.basename(str(stat_result["name"]))
    except Exception as e:
        file_name = os.path.basename(file_path)

    creation_date = _format_file_timestamp(stat_result.get("created"))
    last_modified_date = _format_file_timestamp(stat_result.get("mtime"))
    last_accessed_date = _format_file_timestamp(stat_result.get("atime"))
    default_meta = {
        "file_path": file_path,
        "file_name": file_name,
        "file_type": mimetypes.guess_type(file_path)[0],
        "file_size": stat_result.get("size"),
        "creation_date": creation_date,
        "last_modified_date": last_modified_date,
        "last_accessed_date": last_accessed_date,
    }

    # Return not null value
    return {
        meta_key: meta_value
        for meta_key, meta_value in default_meta.items()
        if meta_value is not None
    }

```
 |  
| --- | --- |  
options: members: - SimpleDirectoryReader
