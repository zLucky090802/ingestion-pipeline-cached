# Aws bedrock agentcore
AWS Bedrock AgentCore tools and runtime.
##  AgentCoreBrowserToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec "Permanent link")
Bases: 
AWS Bedrock AgentCore Browser Tool Spec.
This toolkit provides a set of tools for working with a remote browser environment:
  * navigate_browser - Navigate to a URL
  * click_element - Click on an element using CSS selectors
  * extract_text - Extract all text from the current webpage
  * extract_hyperlinks - Extract all hyperlinks from the current webpage
  * get_elements - Get elements matching a CSS selector
  * navigate_back - Navigate to the previous page
  * current_webpage - Get information about the current webpage


The toolkit supports multiple threads by maintaining separate browser sessions for each thread ID.
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
 906
 907
 908
 909
 910
 911
 912
 913
 914
 915
 916
 917
 918
 919
 920
 921
 922
 923
 924
 925
 926
 927
 928
 929
 930
 931
 932
 933
 934
 935
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
```
 | 
```
classAgentCoreBrowserToolSpec(BaseToolSpec):
"""
    AWS Bedrock AgentCore Browser Tool Spec.

    This toolkit provides a set of tools for working with a remote browser environment:

    * navigate_browser - Navigate to a URL
    * click_element - Click on an element using CSS selectors
    * extract_text - Extract all text from the current webpage
    * extract_hyperlinks - Extract all hyperlinks from the current webpage
    * get_elements - Get elements matching a CSS selector
    * navigate_back - Navigate to the previous page
    * current_webpage - Get information about the current webpage

    The toolkit supports multiple threads by maintaining separate browser sessions for each thread ID.
    """

    spec_functions = [
        ("navigate_browser", "anavigate_browser"),
        ("click_element", "aclick_element"),
        ("extract_text", "aextract_text"),
        ("extract_hyperlinks", "aextract_hyperlinks"),
        ("get_elements", "aget_elements"),
        ("navigate_back", "anavigate_back"),
        ("current_webpage", "acurrent_webpage"),
        ("generate_live_view_url", "agenerate_live_view_url"),
        ("take_control", "atake_control"),
        ("release_control", "arelease_control"),
    ]

    def__init__(
        self,
        region: Optional[str] = None,
        identifier: Optional[str] = None,
    ) -> None:
"""
        Initialize the AWS Bedrock AgentCore Browser Tool Spec.

        Args:
            region (Optional[str]): AWS region to use for Bedrock AgentCore services.
                If not provided, will try to get it from environment variables.
            identifier (Optional[str]): Custom browser identifier for VPC-enabled
                resources. If not provided, uses the default identifier.

        """
        self.region = region if region is not None else get_aws_region()
        self._identifier = identifier
        self._browser_clients: Dict[str, BrowserClient] = {}
        self._cp_browser_client: Optional[BrowserClient] = None
        self._session_manager = BrowserSessionManager(
            region=self.region, identifier=self._identifier
        )

    def_get_or_create_browser_client(
        self, thread_id: str = "default"
    ) -> BrowserClient:
"""
        Get or create a browser client for the specified thread.

        Args:
            thread_id: Thread ID for the browser session

        Returns:
            BrowserClient instance

        """
        if thread_id in self._browser_clients:
            return self._browser_clients[thread_id]

        # Create a new browser client for this thread
        browser_client = BrowserClient(self.region, integration_source="llamaindex")
        self._browser_clients[thread_id] = browser_client
        return browser_client

    def_get_control_plane_client(self) -> BrowserClient:
"""
        Get or create a browser client for control-plane operations only.

        This client is used for account-level operations (list, create, delete, get)
        that do not require a browser session.
        """
        if self._cp_browser_client is None:
            self._cp_browser_client = BrowserClient(
                self.region, integration_source="llamaindex"
            )
        return self._cp_browser_client

    defnavigate_browser(
        self,
        url: str,
        thread_id: str = "default",
    ) -> str:
"""
        Navigate to a URL (synchronous version).

        Args:
            url (str): URL to navigate to.
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Confirmation message.

        """
        try:
            # Validate URL scheme
            parsed_url = urlparse(url)
            if parsed_url.scheme not in ("http", "https"):
                return f"URL scheme must be 'http' or 'https', got: {parsed_url.scheme}"

            # Get browser and navigate to URL
            browser = self._session_manager.get_sync_browser(thread_id)
            try:
                page = get_current_page(browser)
                response = page.goto(url)
                status = response.status if response else "unknown"
                return f"Navigated to {url} with status code {status}"
            finally:
                self._session_manager.release_sync_browser(thread_id)
        except Exception as e:
            return f"Error navigating to URL: {e!s}"

    async defanavigate_browser(
        self,
        url: str,
        thread_id: str = "default",
    ) -> str:
"""
        Navigate to a URL (asynchronous version).

        Args:
            url (str): URL to navigate to.
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Confirmation message.

        """
        try:
            # Validate URL scheme
            parsed_url = urlparse(url)
            if parsed_url.scheme not in ("http", "https"):
                return f"URL scheme must be 'http' or 'https', got: {parsed_url.scheme}"

            # Get browser and navigate to URL
            browser = await self._session_manager.get_async_browser(thread_id)
            page = await aget_current_page(browser)
            response = await page.goto(url)
            status = response.status if response else "unknown"

            # Release the browser
            await self._session_manager.release_async_browser(thread_id)

            return f"Navigated to {url} with status code {status}"
        except Exception as e:
            return f"Error navigating to URL: {e!s}"

    defclick_element(
        self,
        selector: str,
        thread_id: str = "default",
    ) -> str:
"""
        Click on an element with the given CSS selector (synchronous version).

        Args:
            selector (str): CSS selector for the element to click on.
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Confirmation message.

        """
        try:
            # Get browser and click on element
            browser = self._session_manager.get_sync_browser(thread_id)
            try:
                page = get_current_page(browser)

                try:
                    page.click(selector, timeout=5000)
                    return f"Clicked on element with selector '{selector}'"
                except Exception as click_error:
                    return f"Unable to click on element with selector '{selector}': {click_error!s}"
            finally:
                self._session_manager.release_sync_browser(thread_id)
        except Exception as e:
            return f"Error clicking on element: {e!s}"

    async defaclick_element(
        self,
        selector: str,
        thread_id: str = "default",
    ) -> str:
"""
        Click on an element with the given CSS selector (asynchronous version).

        Args:
            selector (str): CSS selector for the element to click on.
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Confirmation message.

        """
        try:
            # Get browser and click on element
            browser = await self._session_manager.get_async_browser(thread_id)
            page = await aget_current_page(browser)

            try:
                await page.click(selector, timeout=5000)
                result = f"Clicked on element with selector '{selector}'"
            except Exception as click_error:
                result = f"Unable to click on element with selector '{selector}': {click_error!s}"

            # Release the browser
            await self._session_manager.release_async_browser(thread_id)

            return result
        except Exception as e:
            return f"Error clicking on element: {e!s}"

    defextract_text(
        self,
        selector: Optional[str] = None,
        thread_id: str = "default",
    ) -> str:
"""
        Extract text from the current page (synchronous version).

        Args:
            selector (Optional[str]): CSS selector for the element to extract text from. If not provided, extracts text from the entire page.
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: The extracted text.

        """
        try:
            # Get browser and extract text
            browser = self._session_manager.get_sync_browser(thread_id)
            try:
                page = get_current_page(browser)

                if selector:
                    try:
                        element = page.query_selector(selector)
                        if element:
                            text = element.text_content()
                            result = (
                                text if text else "Element found but contains no text"
                            )
                        else:
                            result = f"No element found with selector '{selector}'"
                    except Exception as selector_error:
                        result = f"Error extracting text from selector '{selector}': {selector_error!s}"
                else:
                    # Extract text from the entire page
                    result = page.content()

                return result
            finally:
                self._session_manager.release_sync_browser(thread_id)
        except Exception as e:
            return f"Error extracting text: {e!s}"

    async defaextract_text(
        self,
        selector: Optional[str] = None,
        thread_id: str = "default",
    ) -> str:
"""
        Extract text from the current page (asynchronous version).

        Args:
            selector (Optional[str]): CSS selector for the element to extract text from. If not provided, extracts text from the entire page.
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: The extracted text.

        """
        try:
            # Get browser and extract text
            browser = await self._session_manager.get_async_browser(thread_id)
            page = await aget_current_page(browser)

            if selector:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.text_content()
                        result = text if text else "Element found but contains no text"
                    else:
                        result = f"No element found with selector '{selector}'"
                except Exception as selector_error:
                    result = f"Error extracting text from selector '{selector}': {selector_error!s}"
            else:
                # Extract text from the entire page
                result = await page.content()

            # Release the browser
            await self._session_manager.release_async_browser(thread_id)

            return result
        except Exception as e:
            return f"Error extracting text: {e!s}"

    defextract_hyperlinks(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Extract hyperlinks from the current page (synchronous version).

        Args:
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: The extracted hyperlinks.

        """
        try:
            # Get browser and extract hyperlinks
            browser = self._session_manager.get_sync_browser(thread_id)
            try:
                page = get_current_page(browser)

                # Extract all hyperlinks from the page
                links = page.eval_on_selector_all(
                    "a[href]",
"""
                    (elements) => {
                        return elements.map(el => {
                            return {
                                text: el.innerText || el.textContent,
                                href: el.href



,
                )

                # Format the links
                formatted_links = []
                for i, link in enumerate(links):
                    formatted_links.append(
                        f"{i+1}. {link.get('text','No text')}: {link.get('href','No href')}"
                    )

                return (
                    "\n".join(formatted_links)
                    if formatted_links
                    else "No hyperlinks found on the page"
                )
            finally:
                self._session_manager.release_sync_browser(thread_id)
        except Exception as e:
            return f"Error extracting hyperlinks: {e!s}"

    async defaextract_hyperlinks(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Extract hyperlinks from the current page (asynchronous version).

        Args:
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: The extracted hyperlinks.

        """
        try:
            # Get browser and extract hyperlinks
            browser = await self._session_manager.get_async_browser(thread_id)
            page = await aget_current_page(browser)

            # Extract all hyperlinks from the page
            links = await page.eval_on_selector_all(
                "a[href]",
"""
                (elements) => {
                    return elements.map(el => {
                        return {
                            text: el.innerText || el.textContent,
                            href: el.href



,
            )

            # Format the links
            formatted_links = []
            for i, link in enumerate(links):
                formatted_links.append(
                    f"{i+1}. {link.get('text','No text')}: {link.get('href','No href')}"
                )

            result = (
                "\n".join(formatted_links)
                if formatted_links
                else "No hyperlinks found on the page"
            )

            # Release the browser
            await self._session_manager.release_async_browser(thread_id)

            return result
        except Exception as e:
            return f"Error extracting hyperlinks: {e!s}"

    defget_elements(
        self,
        selector: str,
        thread_id: str = "default",
    ) -> str:
"""
        Get elements matching a CSS selector (synchronous version).

        Args:
            selector (str): CSS selector for the elements to get.
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Information about the matching elements.

        """
        try:
            # Get browser and find elements
            browser = self._session_manager.get_sync_browser(thread_id)
            try:
                page = get_current_page(browser)

                # Find elements matching the selector
                elements = page.query_selector_all(selector)

                if not elements:
                    result = f"No elements found matching selector '{selector}'"
                else:
                    # Extract information about the elements
                    elements_info = []
                    for i, element in enumerate(elements):
                        tag_name = element.evaluate("el => el.tagName.toLowerCase()")
                        text = element.text_content() or ""
                        attributes = element.evaluate(
"""
                            (el) => {
                                const attrs = {};
                                for (const attr of el.attributes) {
                                    attrs[attr.name] = attr.value;

                                return attrs;


                        )

                        # Format element info
                        attr_str = ", ".join(
                            [f'{k}="{v}"' for k, v in attributes.items()]
                        )
                        elements_info.append(
                            f"{i+1}. <{tag_name}{attr_str}{text}</{tag_name}>"
                        )

                    result = (
                        f"Found {len(elements)} element(s) matching selector '{selector}':\n"
                        + "\n".join(elements_info)
                    )

                return result
            finally:
                self._session_manager.release_sync_browser(thread_id)
        except Exception as e:
            return f"Error getting elements: {e!s}"

    async defaget_elements(
        self,
        selector: str,
        thread_id: str = "default",
    ) -> str:
"""
        Get elements matching a CSS selector (asynchronous version).

        Args:
            selector (str): CSS selector for the elements to get.
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Information about the matching elements.

        """
        try:
            # Get browser and find elements
            browser = await self._session_manager.get_async_browser(thread_id)
            page = await aget_current_page(browser)

            # Find elements matching the selector
            elements = await page.query_selector_all(selector)

            if not elements:
                result = f"No elements found matching selector '{selector}'"
            else:
                # Extract information about the elements
                elements_info = []
                for i, element in enumerate(elements):
                    tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
                    text = await element.text_content() or ""
                    attributes = await element.evaluate(
"""
                        (el) => {
                            const attrs = {};
                            for (const attr of el.attributes) {
                                attrs[attr.name] = attr.value;

                            return attrs;


                    )

                    # Format element info
                    attr_str = ", ".join([f'{k}="{v}"' for k, v in attributes.items()])
                    elements_info.append(
                        f"{i+1}. <{tag_name}{attr_str}{text}</{tag_name}>"
                    )

                result = (
                    f"Found {len(elements)} element(s) matching selector '{selector}':\n"
                    + "\n".join(elements_info)
                )

            # Release the browser
            await self._session_manager.release_async_browser(thread_id)

            return result
        except Exception as e:
            return f"Error getting elements: {e!s}"

    defnavigate_back(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Navigate to the previous page (synchronous version).

        Args:
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Confirmation message.

        """
        try:
            # Get browser and navigate back
            browser = self._session_manager.get_sync_browser(thread_id)
            try:
                page = get_current_page(browser)

                # Navigate back
                response = page.go_back()

                # Get the current URL after navigating back
                current_url = page.url if response else "unknown"

                if response:
                    return f"Navigated back to {current_url}"
                else:
                    return "Could not navigate back (no previous page in history)"
            finally:
                self._session_manager.release_sync_browser(thread_id)
        except Exception as e:
            return f"Error navigating back: {e!s}"

    async defanavigate_back(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Navigate to the previous page (asynchronous version).

        Args:
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Confirmation message.

        """
        try:
            # Get browser and navigate back
            browser = await self._session_manager.get_async_browser(thread_id)
            page = await aget_current_page(browser)

            # Navigate back
            response = await page.go_back()

            # Get the current URL after navigating back
            current_url = page.url if response else "unknown"

            # Release the browser
            await self._session_manager.release_async_browser(thread_id)

            if response:
                return f"Navigated back to {current_url}"
            else:
                return "Could not navigate back (no previous page in history)"
        except Exception as e:
            return f"Error navigating back: {e!s}"

    defcurrent_webpage(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Get information about the current webpage (synchronous version).

        Args:
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Information about the current webpage.

        """
        try:
            # Get browser and get current webpage info
            browser = self._session_manager.get_sync_browser(thread_id)
            try:
                page = get_current_page(browser)

                # Get the current URL
                url = page.url

                # Get the page title
                title = page.title()

                # Get basic page metrics
                metrics = page.evaluate(
"""
                    () => {
                        return {
                            width: document.documentElement.clientWidth,
                            height: document.documentElement.clientHeight,
                            links: document.querySelectorAll('a').length,
                            images: document.querySelectorAll('img').length,
                            forms: document.querySelectorAll('form').length



                )

                # Format the result
                result = f"Current webpage information:\n"
                result += f"URL: {url}\n"
                result += f"Title: {title}\n"
                result += f"Viewport size: {metrics['width']}x{metrics['height']}\n"
                result += f"Links: {metrics['links']}\n"
                result += f"Images: {metrics['images']}\n"
                result += f"Forms: {metrics['forms']}"

                return result
            finally:
                self._session_manager.release_sync_browser(thread_id)
        except Exception as e:
            return f"Error getting current webpage information: {e!s}"

    async defacurrent_webpage(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Get information about the current webpage (asynchronous version).

        Args:
            thread_id (str): Thread ID for the browser session.

        Returns:
            str: Information about the current webpage.

        """
        try:
            # Get browser and get current webpage info
            browser = await self._session_manager.get_async_browser(thread_id)
            page = await aget_current_page(browser)

            # Get the current URL
            url = page.url

            # Get the page title
            title = await page.title()

            # Get basic page metrics
            metrics = await page.evaluate(
"""
                () => {
                    return {
                        width: document.documentElement.clientWidth,
                        height: document.documentElement.clientHeight,
                        links: document.querySelectorAll('a').length,
                        images: document.querySelectorAll('img').length,
                        forms: document.querySelectorAll('form').length



            )

            # Format the result
            result = f"Current webpage information:\n"
            result += f"URL: {url}\n"
            result += f"Title: {title}\n"
            result += f"Viewport size: {metrics['width']}x{metrics['height']}\n"
            result += f"Links: {metrics['links']}\n"
            result += f"Images: {metrics['images']}\n"
            result += f"Forms: {metrics['forms']}"

            # Release the browser
            await self._session_manager.release_async_browser(thread_id)

            return result
        except Exception as e:
            return f"Error getting current webpage information: {e!s}"

    defgenerate_live_view_url(
        self,
        expires: int = DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT,
        thread_id: str = "default",
    ) -> str:
"""
        Generate a presigned URL for live viewing a browser session (synchronous version).

        This URL allows a human to observe the browser session in real-time for oversight.
        A browser session must already exist for the given thread_id (e.g., by navigating
        to a URL first).

        Args:
            expires (int): Seconds until the URL expires. Maximum 300. Default is 300.
            thread_id (str): Thread ID for the browser session. Default is "default".

        Returns:
            str: The presigned URL for viewing the browser session.

        """
        try:
            browser_client = self._session_manager.get_browser_client(thread_id)
            if browser_client is None:
                return (
                    f"No browser session found for thread '{thread_id}'. "
                    "Navigate to a URL first to start a session."
                )
            return browser_client.generate_live_view_url(expires=expires)
        except Exception as e:
            return f"Error generating live view URL: {e!s}"

    async defagenerate_live_view_url(
        self,
        expires: int = DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT,
        thread_id: str = "default",
    ) -> str:
"""
        Generate a presigned URL for live viewing a browser session (asynchronous version).

        This URL allows a human to observe the browser session in real-time for oversight.
        A browser session must already exist for the given thread_id (e.g., by navigating
        to a URL first).

        Args:
            expires (int): Seconds until the URL expires. Maximum 300. Default is 300.
            thread_id (str): Thread ID for the browser session. Default is "default".

        Returns:
            str: The presigned URL for viewing the browser session.

        """
        return await asyncio.to_thread(
            self.generate_live_view_url, expires=expires, thread_id=thread_id
        )

    deflist_browsers(
        self,
        browser_type: Optional[str] = None,
        max_results: int = 10,
        thread_id: str = "default",
    ) -> str:
"""
        List all browsers in the account (synchronous version).

        Args:
            browser_type (Optional[str]): Filter by type: "SYSTEM" or "CUSTOM".
            max_results (int): Maximum results to return (1-100). Default is 10.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: JSON-formatted list of browser summaries.

        """
        try:
            browser_client = self._get_control_plane_client()
            response = browser_client.list_browsers(
                browser_type=browser_type, max_results=max_results
            )
            summaries = response.get("browserSummaries", [])
            if not summaries:
                return "No browsers found."
            lines = []
            for b in summaries:
                lines.append(
                    f"- {b.get('name','N/A')} (ID: {b.get('browserId','N/A')}, "
                    f"Status: {b.get('status','N/A')}, Type: {b.get('type','N/A')})"
                )
            return f"Found {len(summaries)} browser(s):\n" + "\n".join(lines)
        except Exception as e:
            return f"Error listing browsers: {e!s}"

    async defalist_browsers(
        self,
        browser_type: Optional[str] = None,
        max_results: int = 10,
        thread_id: str = "default",
    ) -> str:
"""
        List all browsers in the account (asynchronous version).

        Args:
            browser_type (Optional[str]): Filter by type: "SYSTEM" or "CUSTOM".
            max_results (int): Maximum results to return (1-100). Default is 10.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: JSON-formatted list of browser summaries.

        """
        return await asyncio.to_thread(
            self.list_browsers,
            browser_type=browser_type,
            max_results=max_results,
            thread_id=thread_id,
        )

    defcreate_browser(
        self,
        name: str,
        execution_role_arn: str,
        network_mode: str = "PUBLIC",
        description: str = "",
        subnet_ids: Optional[List[str]] = None,
        security_group_ids: Optional[List[str]] = None,
        thread_id: str = "default",
    ) -> str:
"""
        Create a custom browser with specific configuration (synchronous version).

        Args:
            name (str): Name for the browser. Must match pattern [a-zA-Z][a-zA-Z0-9_]{0,47}.
            execution_role_arn (str): IAM role ARN with permissions for browser operations.
            network_mode (str): Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".
            description (str): Description of the browser. Default is "".
            subnet_ids (Optional[List[str]]): Subnet IDs for VPC mode.
            security_group_ids (Optional[List[str]]): Security group IDs for VPC mode.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Confirmation with browser ID and status.

        """
        try:
            browser_client = self._get_control_plane_client()
            network_config: Dict[str, Any] = {"networkMode": network_mode}
            if subnet_ids or security_group_ids:
                vpc_config: Dict[str, Any] = {}
                if subnet_ids:
                    vpc_config["subnets"] = subnet_ids
                if security_group_ids:
                    vpc_config["securityGroups"] = security_group_ids
                network_config["vpcConfig"] = vpc_config
            kwargs: Dict[str, Any] = {
                "name": name,
                "execution_role_arn": execution_role_arn,
                "network_configuration": network_config,
            }
            if description:
                kwargs["description"] = description
            response = browser_client.create_browser(**kwargs)
            browser_id = response.get("browserId", "unknown")
            status = response.get("status", "unknown")
            return f"Browser created (ID: {browser_id}, Status: {status})"
        except Exception as e:
            return f"Error creating browser: {e!s}"

    async defacreate_browser(
        self,
        name: str,
        execution_role_arn: str,
        network_mode: str = "PUBLIC",
        description: str = "",
        subnet_ids: Optional[List[str]] = None,
        security_group_ids: Optional[List[str]] = None,
        thread_id: str = "default",
    ) -> str:
"""
        Create a custom browser with specific configuration (asynchronous version).

        Args:
            name (str): Name for the browser. Must match pattern [a-zA-Z][a-zA-Z0-9_]{0,47}.
            execution_role_arn (str): IAM role ARN with permissions for browser operations.
            network_mode (str): Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".
            description (str): Description of the browser. Default is "".
            subnet_ids (Optional[List[str]]): Subnet IDs for VPC mode.
            security_group_ids (Optional[List[str]]): Security group IDs for VPC mode.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Confirmation with browser ID and status.

        """
        return await asyncio.to_thread(
            self.create_browser,
            name=name,
            execution_role_arn=execution_role_arn,
            network_mode=network_mode,
            description=description,
            subnet_ids=subnet_ids,
            security_group_ids=security_group_ids,
            thread_id=thread_id,
        )

    defdelete_browser(
        self,
        browser_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Delete a custom browser (synchronous version).

        Args:
            browser_id (str): The browser identifier to delete.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Confirmation of deletion.

        """
        try:
            browser_client = self._get_control_plane_client()
            response = browser_client.delete_browser(browser_id=browser_id)
            status = response.get("status", "unknown")
            return f"Browser '{browser_id}' deleted (Status: {status})"
        except Exception as e:
            return f"Error deleting browser: {e!s}"

    async defadelete_browser(
        self,
        browser_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Delete a custom browser (asynchronous version).

        Args:
            browser_id (str): The browser identifier to delete.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Confirmation of deletion.

        """
        return await asyncio.to_thread(
            self.delete_browser, browser_id=browser_id, thread_id=thread_id
        )

    defget_browser(
        self,
        browser_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Get detailed information about a browser (synchronous version).

        Args:
            browser_id (str): The browser identifier.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Browser details including name, status, and configuration.

        """
        try:
            browser_client = self._get_control_plane_client()
            response = browser_client.get_browser(browser_id=browser_id)
            name = response.get("name", "N/A")
            status = response.get("status", "N/A")
            desc = response.get("description", "")
            result = f"Browser '{browser_id}':\n"
            result += f"  Name: {name}\n"
            result += f"  Status: {status}\n"
            if desc:
                result += f"  Description: {desc}\n"
            network = response.get("networkConfiguration", {})
            if network:
                result += f"  Network mode: {network.get('networkMode','N/A')}"
            return result
        except Exception as e:
            return f"Error getting browser: {e!s}"

    async defaget_browser(
        self,
        browser_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Get detailed information about a browser (asynchronous version).

        Args:
            browser_id (str): The browser identifier.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Browser details including name, status, and configuration.

        """
        return await asyncio.to_thread(
            self.get_browser, browser_id=browser_id, thread_id=thread_id
        )

    deftake_control(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Take manual control of a browser session by disabling the automation stream (synchronous version).

        This allows a human to interact with the browser via the live view URL while
        preventing the automation agent from making changes.

        Args:
            thread_id (str): Thread ID for the browser session. Default is "default".

        Returns:
            str: Confirmation message.

        """
        try:
            browser_client = self._session_manager.get_browser_client(thread_id)
            if browser_client is None:
                return (
                    f"No browser session found for thread '{thread_id}'. "
                    "Navigate to a URL first to start a session."
                )
            browser_client.take_control()
            return "Took manual control of the browser session. Automation stream disabled."
        except Exception as e:
            return f"Error taking control: {e!s}"

    async defatake_control(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Take manual control of a browser session by disabling the automation stream (asynchronous version).

        Args:
            thread_id (str): Thread ID for the browser session. Default is "default".

        Returns:
            str: Confirmation message.

        """
        return await asyncio.to_thread(self.take_control, thread_id=thread_id)

    defrelease_control(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Release manual control and re-enable the automation stream (synchronous version).

        This returns control to the automation agent after manual interaction.

        Args:
            thread_id (str): Thread ID for the browser session. Default is "default".

        Returns:
            str: Confirmation message.

        """
        try:
            browser_client = self._session_manager.get_browser_client(thread_id)
            if browser_client is None:
                return (
                    f"No browser session found for thread '{thread_id}'. "
                    "Navigate to a URL first to start a session."
                )
            browser_client.release_control()
            return "Released manual control. Automation stream re-enabled."
        except Exception as e:
            return f"Error releasing control: {e!s}"

    async defarelease_control(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Release manual control and re-enable the automation stream (asynchronous version).

        Args:
            thread_id (str): Thread ID for the browser session. Default is "default".

        Returns:
            str: Confirmation message.

        """
        return await asyncio.to_thread(self.release_control, thread_id=thread_id)

    async defcleanup(self, thread_id: Optional[str] = None) -> None:
"""
        Clean up resources

        Args:
            thread_id: Optional thread ID to clean up. If None, cleans up all sessions.

        """
        if thread_id:
            # Clean up a specific thread's session
            if thread_id in self._browser_clients:
                try:
                    self._browser_clients[thread_id].stop()
                    del self._browser_clients[thread_id]
                    logger.info(f"Browser session for thread {thread_id} cleaned up")
                except Exception as e:
                    logger.warning(
                        f"Error stopping browser for thread {thread_id}: {e}"
                    )
        else:
            # Clean up all sessions
            thread_ids = list(self._browser_clients.keys())
            for tid in thread_ids:
                try:
                    self._browser_clients[tid].stop()
                except Exception as e:
                    logger.warning(f"Error stopping browser for thread {tid}: {e}")

            self._browser_clients = {}
            logger.info("All browser sessions cleaned up")

```
 |  
| --- | --- |  
###  navigate_browser [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.navigate_browser "Permanent link")

```
navigate_browser(
    url: , thread_id:  = "default"
) -> 

```

Navigate to a URL (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  URL to navigate to.  |  _required_  |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
defnavigate_browser(
    self,
    url: str,
    thread_id: str = "default",
) -> str:
"""
    Navigate to a URL (synchronous version).

    Args:
        url (str): URL to navigate to.
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Confirmation message.

    """
    try:
        # Validate URL scheme
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ("http", "https"):
            return f"URL scheme must be 'http' or 'https', got: {parsed_url.scheme}"

        # Get browser and navigate to URL
        browser = self._session_manager.get_sync_browser(thread_id)
        try:
            page = get_current_page(browser)
            response = page.goto(url)
            status = response.status if response else "unknown"
            return f"Navigated to {url} with status code {status}"
        finally:
            self._session_manager.release_sync_browser(thread_id)
    except Exception as e:
        return f"Error navigating to URL: {e!s}"

```
 |  
| --- | --- |  
###  anavigate_browser [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.anavigate_browser "Permanent link")

```
anavigate_browser(
    url: , thread_id:  = "default"
) -> 

```

Navigate to a URL (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `url`  |  URL to navigate to.  |  _required_  |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
async defanavigate_browser(
    self,
    url: str,
    thread_id: str = "default",
) -> str:
"""
    Navigate to a URL (asynchronous version).

    Args:
        url (str): URL to navigate to.
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Confirmation message.

    """
    try:
        # Validate URL scheme
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ("http", "https"):
            return f"URL scheme must be 'http' or 'https', got: {parsed_url.scheme}"

        # Get browser and navigate to URL
        browser = await self._session_manager.get_async_browser(thread_id)
        page = await aget_current_page(browser)
        response = await page.goto(url)
        status = response.status if response else "unknown"

        # Release the browser
        await self._session_manager.release_async_browser(thread_id)

        return f"Navigated to {url} with status code {status}"
    except Exception as e:
        return f"Error navigating to URL: {e!s}"

```
 |  
| --- | --- |  
###  click_element [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.click_element "Permanent link")

```
click_element(
    selector: , thread_id:  = "default"
) -> 

```

Click on an element with the given CSS selector (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  CSS selector for the element to click on.  |  _required_  |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
defclick_element(
    self,
    selector: str,
    thread_id: str = "default",
) -> str:
"""
    Click on an element with the given CSS selector (synchronous version).

    Args:
        selector (str): CSS selector for the element to click on.
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Confirmation message.

    """
    try:
        # Get browser and click on element
        browser = self._session_manager.get_sync_browser(thread_id)
        try:
            page = get_current_page(browser)

            try:
                page.click(selector, timeout=5000)
                return f"Clicked on element with selector '{selector}'"
            except Exception as click_error:
                return f"Unable to click on element with selector '{selector}': {click_error!s}"
        finally:
            self._session_manager.release_sync_browser(thread_id)
    except Exception as e:
        return f"Error clicking on element: {e!s}"

```
 |  
| --- | --- |  
###  aclick_element [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.aclick_element "Permanent link")

```
aclick_element(
    selector: , thread_id:  = "default"
) -> 

```

Click on an element with the given CSS selector (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  CSS selector for the element to click on.  |  _required_  |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
async defaclick_element(
    self,
    selector: str,
    thread_id: str = "default",
) -> str:
"""
    Click on an element with the given CSS selector (asynchronous version).

    Args:
        selector (str): CSS selector for the element to click on.
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Confirmation message.

    """
    try:
        # Get browser and click on element
        browser = await self._session_manager.get_async_browser(thread_id)
        page = await aget_current_page(browser)

        try:
            await page.click(selector, timeout=5000)
            result = f"Clicked on element with selector '{selector}'"
        except Exception as click_error:
            result = f"Unable to click on element with selector '{selector}': {click_error!s}"

        # Release the browser
        await self._session_manager.release_async_browser(thread_id)

        return result
    except Exception as e:
        return f"Error clicking on element: {e!s}"

```
 |  
| --- | --- |  
###  extract_text [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.extract_text "Permanent link")

```
extract_text(
    selector: Optional[] = None,
    thread_id:  = "default",
) -> 

```

Extract text from the current page (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  `Optional[str]`  |  CSS selector for the element to extract text from. If not provided, extracts text from the entire page.  |  `None`  |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The extracted text.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
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
```
 | 
```
defextract_text(
    self,
    selector: Optional[str] = None,
    thread_id: str = "default",
) -> str:
"""
    Extract text from the current page (synchronous version).

    Args:
        selector (Optional[str]): CSS selector for the element to extract text from. If not provided, extracts text from the entire page.
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: The extracted text.

    """
    try:
        # Get browser and extract text
        browser = self._session_manager.get_sync_browser(thread_id)
        try:
            page = get_current_page(browser)

            if selector:
                try:
                    element = page.query_selector(selector)
                    if element:
                        text = element.text_content()
                        result = (
                            text if text else "Element found but contains no text"
                        )
                    else:
                        result = f"No element found with selector '{selector}'"
                except Exception as selector_error:
                    result = f"Error extracting text from selector '{selector}': {selector_error!s}"
            else:
                # Extract text from the entire page
                result = page.content()

            return result
        finally:
            self._session_manager.release_sync_browser(thread_id)
    except Exception as e:
        return f"Error extracting text: {e!s}"

```
 |  
| --- | --- |  
###  aextract_text [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.aextract_text "Permanent link")

```
aextract_text(
    selector: Optional[] = None,
    thread_id:  = "default",
) -> 

```

Extract text from the current page (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  `Optional[str]`  |  CSS selector for the element to extract text from. If not provided, extracts text from the entire page.  |  `None`  |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The extracted text.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
async defaextract_text(
    self,
    selector: Optional[str] = None,
    thread_id: str = "default",
) -> str:
"""
    Extract text from the current page (asynchronous version).

    Args:
        selector (Optional[str]): CSS selector for the element to extract text from. If not provided, extracts text from the entire page.
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: The extracted text.

    """
    try:
        # Get browser and extract text
        browser = await self._session_manager.get_async_browser(thread_id)
        page = await aget_current_page(browser)

        if selector:
            try:
                element = await page.query_selector(selector)
                if element:
                    text = await element.text_content()
                    result = text if text else "Element found but contains no text"
                else:
                    result = f"No element found with selector '{selector}'"
            except Exception as selector_error:
                result = f"Error extracting text from selector '{selector}': {selector_error!s}"
        else:
            # Extract text from the entire page
            result = await page.content()

        # Release the browser
        await self._session_manager.release_async_browser(thread_id)

        return result
    except Exception as e:
        return f"Error extracting text: {e!s}"

```
 |  
| --- | --- |  
###  extract_hyperlinks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.extract_hyperlinks "Permanent link")

```
extract_hyperlinks(thread_id:  = 'default') -> 

```

Extract hyperlinks from the current page (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The extracted hyperlinks.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
defextract_hyperlinks(
    self,
    thread_id: str = "default",
) -> str:
"""
    Extract hyperlinks from the current page (synchronous version).

    Args:
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: The extracted hyperlinks.

    """
    try:
        # Get browser and extract hyperlinks
        browser = self._session_manager.get_sync_browser(thread_id)
        try:
            page = get_current_page(browser)

            # Extract all hyperlinks from the page
            links = page.eval_on_selector_all(
                "a[href]",
"""
                (elements) => {
                    return elements.map(el => {
                        return {
                            text: el.innerText || el.textContent,
                            href: el.href



,
            )

            # Format the links
            formatted_links = []
            for i, link in enumerate(links):
                formatted_links.append(
                    f"{i+1}. {link.get('text','No text')}: {link.get('href','No href')}"
                )

            return (
                "\n".join(formatted_links)
                if formatted_links
                else "No hyperlinks found on the page"
            )
        finally:
            self._session_manager.release_sync_browser(thread_id)
    except Exception as e:
        return f"Error extracting hyperlinks: {e!s}"

```
 |  
| --- | --- |  
###  aextract_hyperlinks [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.aextract_hyperlinks "Permanent link")

```
aextract_hyperlinks(thread_id:  = 'default') -> 

```

Extract hyperlinks from the current page (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The extracted hyperlinks.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
async defaextract_hyperlinks(
    self,
    thread_id: str = "default",
) -> str:
"""
    Extract hyperlinks from the current page (asynchronous version).

    Args:
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: The extracted hyperlinks.

    """
    try:
        # Get browser and extract hyperlinks
        browser = await self._session_manager.get_async_browser(thread_id)
        page = await aget_current_page(browser)

        # Extract all hyperlinks from the page
        links = await page.eval_on_selector_all(
            "a[href]",
"""
            (elements) => {
                return elements.map(el => {
                    return {
                        text: el.innerText || el.textContent,
                        href: el.href



        """,
        )

        # Format the links
        formatted_links = []
        for i, link in enumerate(links):
            formatted_links.append(
                f"{i+1}. {link.get('text','No text')}: {link.get('href','No href')}"
            )

        result = (
            "\n".join(formatted_links)
            if formatted_links
            else "No hyperlinks found on the page"
        )

        # Release the browser
        await self._session_manager.release_async_browser(thread_id)

        return result
    except Exception as e:
        return f"Error extracting hyperlinks: {e!s}"

```
 |  
| --- | --- |  
###  get_elements [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.get_elements "Permanent link")

```
get_elements(
    selector: , thread_id:  = "default"
) -> 

```

Get elements matching a CSS selector (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  CSS selector for the elements to get.  |  _required_  |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Information about the matching elements.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
defget_elements(
    self,
    selector: str,
    thread_id: str = "default",
) -> str:
"""
    Get elements matching a CSS selector (synchronous version).

    Args:
        selector (str): CSS selector for the elements to get.
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Information about the matching elements.

    """
    try:
        # Get browser and find elements
        browser = self._session_manager.get_sync_browser(thread_id)
        try:
            page = get_current_page(browser)

            # Find elements matching the selector
            elements = page.query_selector_all(selector)

            if not elements:
                result = f"No elements found matching selector '{selector}'"
            else:
                # Extract information about the elements
                elements_info = []
                for i, element in enumerate(elements):
                    tag_name = element.evaluate("el => el.tagName.toLowerCase()")
                    text = element.text_content() or ""
                    attributes = element.evaluate(
"""
                        (el) => {
                            const attrs = {};
                            for (const attr of el.attributes) {
                                attrs[attr.name] = attr.value;

                            return attrs;


                    )

                    # Format element info
                    attr_str = ", ".join(
                        [f'{k}="{v}"' for k, v in attributes.items()]
                    )
                    elements_info.append(
                        f"{i+1}. <{tag_name}{attr_str}{text}</{tag_name}>"
                    )

                result = (
                    f"Found {len(elements)} element(s) matching selector '{selector}':\n"
                    + "\n".join(elements_info)
                )

            return result
        finally:
            self._session_manager.release_sync_browser(thread_id)
    except Exception as e:
        return f"Error getting elements: {e!s}"

```
 |  
| --- | --- |  
###  aget_elements [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.aget_elements "Permanent link")

```
aget_elements(
    selector: , thread_id:  = "default"
) -> 

```

Get elements matching a CSS selector (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `selector`  |  CSS selector for the elements to get.  |  _required_  |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Information about the matching elements.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
async defaget_elements(
    self,
    selector: str,
    thread_id: str = "default",
) -> str:
"""
    Get elements matching a CSS selector (asynchronous version).

    Args:
        selector (str): CSS selector for the elements to get.
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Information about the matching elements.

    """
    try:
        # Get browser and find elements
        browser = await self._session_manager.get_async_browser(thread_id)
        page = await aget_current_page(browser)

        # Find elements matching the selector
        elements = await page.query_selector_all(selector)

        if not elements:
            result = f"No elements found matching selector '{selector}'"
        else:
            # Extract information about the elements
            elements_info = []
            for i, element in enumerate(elements):
                tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
                text = await element.text_content() or ""
                attributes = await element.evaluate(
"""
                    (el) => {
                        const attrs = {};
                        for (const attr of el.attributes) {
                            attrs[attr.name] = attr.value;

                        return attrs;


                )

                # Format element info
                attr_str = ", ".join([f'{k}="{v}"' for k, v in attributes.items()])
                elements_info.append(
                    f"{i+1}. <{tag_name}{attr_str}{text}</{tag_name}>"
                )

            result = (
                f"Found {len(elements)} element(s) matching selector '{selector}':\n"
                + "\n".join(elements_info)
            )

        # Release the browser
        await self._session_manager.release_async_browser(thread_id)

        return result
    except Exception as e:
        return f"Error getting elements: {e!s}"

```
 |  
| --- | --- |  
###  navigate_back [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.navigate_back "Permanent link")

```
navigate_back(thread_id:  = 'default') -> 

```

Navigate to the previous page (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
defnavigate_back(
    self,
    thread_id: str = "default",
) -> str:
"""
    Navigate to the previous page (synchronous version).

    Args:
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Confirmation message.

    """
    try:
        # Get browser and navigate back
        browser = self._session_manager.get_sync_browser(thread_id)
        try:
            page = get_current_page(browser)

            # Navigate back
            response = page.go_back()

            # Get the current URL after navigating back
            current_url = page.url if response else "unknown"

            if response:
                return f"Navigated back to {current_url}"
            else:
                return "Could not navigate back (no previous page in history)"
        finally:
            self._session_manager.release_sync_browser(thread_id)
    except Exception as e:
        return f"Error navigating back: {e!s}"

```
 |  
| --- | --- |  
###  anavigate_back [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.anavigate_back "Permanent link")

```
anavigate_back(thread_id:  = 'default') -> 

```

Navigate to the previous page (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
async defanavigate_back(
    self,
    thread_id: str = "default",
) -> str:
"""
    Navigate to the previous page (asynchronous version).

    Args:
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Confirmation message.

    """
    try:
        # Get browser and navigate back
        browser = await self._session_manager.get_async_browser(thread_id)
        page = await aget_current_page(browser)

        # Navigate back
        response = await page.go_back()

        # Get the current URL after navigating back
        current_url = page.url if response else "unknown"

        # Release the browser
        await self._session_manager.release_async_browser(thread_id)

        if response:
            return f"Navigated back to {current_url}"
        else:
            return "Could not navigate back (no previous page in history)"
    except Exception as e:
        return f"Error navigating back: {e!s}"

```
 |  
| --- | --- |  
###  current_webpage [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.current_webpage "Permanent link")

```
current_webpage(thread_id:  = 'default') -> 

```

Get information about the current webpage (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Information about the current webpage.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
defcurrent_webpage(
    self,
    thread_id: str = "default",
) -> str:
"""
    Get information about the current webpage (synchronous version).

    Args:
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Information about the current webpage.

    """
    try:
        # Get browser and get current webpage info
        browser = self._session_manager.get_sync_browser(thread_id)
        try:
            page = get_current_page(browser)

            # Get the current URL
            url = page.url

            # Get the page title
            title = page.title()

            # Get basic page metrics
            metrics = page.evaluate(
"""
                () => {
                    return {
                        width: document.documentElement.clientWidth,
                        height: document.documentElement.clientHeight,
                        links: document.querySelectorAll('a').length,
                        images: document.querySelectorAll('img').length,
                        forms: document.querySelectorAll('form').length



            )

            # Format the result
            result = f"Current webpage information:\n"
            result += f"URL: {url}\n"
            result += f"Title: {title}\n"
            result += f"Viewport size: {metrics['width']}x{metrics['height']}\n"
            result += f"Links: {metrics['links']}\n"
            result += f"Images: {metrics['images']}\n"
            result += f"Forms: {metrics['forms']}"

            return result
        finally:
            self._session_manager.release_sync_browser(thread_id)
    except Exception as e:
        return f"Error getting current webpage information: {e!s}"

```
 |  
| --- | --- |  
###  acurrent_webpage [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.acurrent_webpage "Permanent link")

```
acurrent_webpage(thread_id:  = 'default') -> 

```

Get information about the current webpage (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Information about the current webpage.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
async defacurrent_webpage(
    self,
    thread_id: str = "default",
) -> str:
"""
    Get information about the current webpage (asynchronous version).

    Args:
        thread_id (str): Thread ID for the browser session.

    Returns:
        str: Information about the current webpage.

    """
    try:
        # Get browser and get current webpage info
        browser = await self._session_manager.get_async_browser(thread_id)
        page = await aget_current_page(browser)

        # Get the current URL
        url = page.url

        # Get the page title
        title = await page.title()

        # Get basic page metrics
        metrics = await page.evaluate(
"""
            () => {
                return {
                    width: document.documentElement.clientWidth,
                    height: document.documentElement.clientHeight,
                    links: document.querySelectorAll('a').length,
                    images: document.querySelectorAll('img').length,
                    forms: document.querySelectorAll('form').length


        """
        )

        # Format the result
        result = f"Current webpage information:\n"
        result += f"URL: {url}\n"
        result += f"Title: {title}\n"
        result += f"Viewport size: {metrics['width']}x{metrics['height']}\n"
        result += f"Links: {metrics['links']}\n"
        result += f"Images: {metrics['images']}\n"
        result += f"Forms: {metrics['forms']}"

        # Release the browser
        await self._session_manager.release_async_browser(thread_id)

        return result
    except Exception as e:
        return f"Error getting current webpage information: {e!s}"

```
 |  
| --- | --- |  
###  generate_live_view_url [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.generate_live_view_url "Permanent link")

```
generate_live_view_url(
    expires:  = DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT,
    thread_id:  = "default",
) -> 

```

Generate a presigned URL for live viewing a browser session (synchronous version).
This URL allows a human to observe the browser session in real-time for oversight. A browser session must already exist for the given thread_id (e.g., by navigating to a URL first).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `expires`  |  Seconds until the URL expires. Maximum 300. Default is 300.  |  `DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT`  |  
|  `thread_id`  |  Thread ID for the browser session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The presigned URL for viewing the browser session.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
defgenerate_live_view_url(
    self,
    expires: int = DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT,
    thread_id: str = "default",
) -> str:
"""
    Generate a presigned URL for live viewing a browser session (synchronous version).

    This URL allows a human to observe the browser session in real-time for oversight.
    A browser session must already exist for the given thread_id (e.g., by navigating
    to a URL first).

    Args:
        expires (int): Seconds until the URL expires. Maximum 300. Default is 300.
        thread_id (str): Thread ID for the browser session. Default is "default".

    Returns:
        str: The presigned URL for viewing the browser session.

    """
    try:
        browser_client = self._session_manager.get_browser_client(thread_id)
        if browser_client is None:
            return (
                f"No browser session found for thread '{thread_id}'. "
                "Navigate to a URL first to start a session."
            )
        return browser_client.generate_live_view_url(expires=expires)
    except Exception as e:
        return f"Error generating live view URL: {e!s}"

```
 |  
| --- | --- |  
###  agenerate_live_view_url [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.agenerate_live_view_url "Permanent link")

```
agenerate_live_view_url(
    expires:  = DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT,
    thread_id:  = "default",
) -> 

```

Generate a presigned URL for live viewing a browser session (asynchronous version).
This URL allows a human to observe the browser session in real-time for oversight. A browser session must already exist for the given thread_id (e.g., by navigating to a URL first).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `expires`  |  Seconds until the URL expires. Maximum 300. Default is 300.  |  `DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT`  |  
|  `thread_id`  |  Thread ID for the browser session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The presigned URL for viewing the browser session.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
async defagenerate_live_view_url(
    self,
    expires: int = DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT,
    thread_id: str = "default",
) -> str:
"""
    Generate a presigned URL for live viewing a browser session (asynchronous version).

    This URL allows a human to observe the browser session in real-time for oversight.
    A browser session must already exist for the given thread_id (e.g., by navigating
    to a URL first).

    Args:
        expires (int): Seconds until the URL expires. Maximum 300. Default is 300.
        thread_id (str): Thread ID for the browser session. Default is "default".

    Returns:
        str: The presigned URL for viewing the browser session.

    """
    return await asyncio.to_thread(
        self.generate_live_view_url, expires=expires, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  list_browsers [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.list_browsers "Permanent link")

```
list_browsers(
    browser_type: Optional[] = None,
    max_results:  = 10,
    thread_id:  = "default",
) -> 

```

List all browsers in the account (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `browser_type`  |  `Optional[str]`  |  Filter by type: "SYSTEM" or "CUSTOM".  |  `None`  |  
|  `max_results`  |  Maximum results to return (1-100). Default is 10.  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  JSON-formatted list of browser summaries.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
deflist_browsers(
    self,
    browser_type: Optional[str] = None,
    max_results: int = 10,
    thread_id: str = "default",
) -> str:
"""
    List all browsers in the account (synchronous version).

    Args:
        browser_type (Optional[str]): Filter by type: "SYSTEM" or "CUSTOM".
        max_results (int): Maximum results to return (1-100). Default is 10.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: JSON-formatted list of browser summaries.

    """
    try:
        browser_client = self._get_control_plane_client()
        response = browser_client.list_browsers(
            browser_type=browser_type, max_results=max_results
        )
        summaries = response.get("browserSummaries", [])
        if not summaries:
            return "No browsers found."
        lines = []
        for b in summaries:
            lines.append(
                f"- {b.get('name','N/A')} (ID: {b.get('browserId','N/A')}, "
                f"Status: {b.get('status','N/A')}, Type: {b.get('type','N/A')})"
            )
        return f"Found {len(summaries)} browser(s):\n" + "\n".join(lines)
    except Exception as e:
        return f"Error listing browsers: {e!s}"

```
 |  
| --- | --- |  
###  alist_browsers [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.alist_browsers "Permanent link")

```
alist_browsers(
    browser_type: Optional[] = None,
    max_results:  = 10,
    thread_id:  = "default",
) -> 

```

List all browsers in the account (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `browser_type`  |  `Optional[str]`  |  Filter by type: "SYSTEM" or "CUSTOM".  |  `None`  |  
|  `max_results`  |  Maximum results to return (1-100). Default is 10.  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  JSON-formatted list of browser summaries.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
```
 | 
```
async defalist_browsers(
    self,
    browser_type: Optional[str] = None,
    max_results: int = 10,
    thread_id: str = "default",
) -> str:
"""
    List all browsers in the account (asynchronous version).

    Args:
        browser_type (Optional[str]): Filter by type: "SYSTEM" or "CUSTOM".
        max_results (int): Maximum results to return (1-100). Default is 10.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: JSON-formatted list of browser summaries.

    """
    return await asyncio.to_thread(
        self.list_browsers,
        browser_type=browser_type,
        max_results=max_results,
        thread_id=thread_id,
    )

```
 |  
| --- | --- |  
###  create_browser [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.create_browser "Permanent link")

```
create_browser(
    name: ,
    execution_role_arn: ,
    network_mode:  = "PUBLIC",
    description:  = "",
    subnet_ids: Optional[[]] = None,
    security_group_ids: Optional[[]] = None,
    thread_id:  = "default",
) -> 

```

Create a custom browser with specific configuration (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  Name for the browser. Must match pattern [a-zA-Z][a-zA-Z0-9_].  |  _required_  |  
|  `execution_role_arn`  |  IAM role ARN with permissions for browser operations.  |  _required_  |  
|  `network_mode`  |  Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".  |  `'PUBLIC'`  |  
|  `description`  |  Description of the browser. Default is "".  |  
|  `subnet_ids`  |  `Optional[List[str]]`  |  Subnet IDs for VPC mode.  |  `None`  |  
|  `security_group_ids`  |  `Optional[List[str]]`  |  Security group IDs for VPC mode.  |  `None`  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation with browser ID and status.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
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
906
907
```
 | 
```
defcreate_browser(
    self,
    name: str,
    execution_role_arn: str,
    network_mode: str = "PUBLIC",
    description: str = "",
    subnet_ids: Optional[List[str]] = None,
    security_group_ids: Optional[List[str]] = None,
    thread_id: str = "default",
) -> str:
"""
    Create a custom browser with specific configuration (synchronous version).

    Args:
        name (str): Name for the browser. Must match pattern [a-zA-Z][a-zA-Z0-9_]{0,47}.
        execution_role_arn (str): IAM role ARN with permissions for browser operations.
        network_mode (str): Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".
        description (str): Description of the browser. Default is "".
        subnet_ids (Optional[List[str]]): Subnet IDs for VPC mode.
        security_group_ids (Optional[List[str]]): Security group IDs for VPC mode.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Confirmation with browser ID and status.

    """
    try:
        browser_client = self._get_control_plane_client()
        network_config: Dict[str, Any] = {"networkMode": network_mode}
        if subnet_ids or security_group_ids:
            vpc_config: Dict[str, Any] = {}
            if subnet_ids:
                vpc_config["subnets"] = subnet_ids
            if security_group_ids:
                vpc_config["securityGroups"] = security_group_ids
            network_config["vpcConfig"] = vpc_config
        kwargs: Dict[str, Any] = {
            "name": name,
            "execution_role_arn": execution_role_arn,
            "network_configuration": network_config,
        }
        if description:
            kwargs["description"] = description
        response = browser_client.create_browser(**kwargs)
        browser_id = response.get("browserId", "unknown")
        status = response.get("status", "unknown")
        return f"Browser created (ID: {browser_id}, Status: {status})"
    except Exception as e:
        return f"Error creating browser: {e!s}"

```
 |  
| --- | --- |  
###  acreate_browser [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.acreate_browser "Permanent link")

```
acreate_browser(
    name: ,
    execution_role_arn: ,
    network_mode:  = "PUBLIC",
    description:  = "",
    subnet_ids: Optional[[]] = None,
    security_group_ids: Optional[[]] = None,
    thread_id:  = "default",
) -> 

```

Create a custom browser with specific configuration (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  Name for the browser. Must match pattern [a-zA-Z][a-zA-Z0-9_].  |  _required_  |  
|  `execution_role_arn`  |  IAM role ARN with permissions for browser operations.  |  _required_  |  
|  `network_mode`  |  Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".  |  `'PUBLIC'`  |  
|  `description`  |  Description of the browser. Default is "".  |  
|  `subnet_ids`  |  `Optional[List[str]]`  |  Subnet IDs for VPC mode.  |  `None`  |  
|  `security_group_ids`  |  `Optional[List[str]]`  |  Security group IDs for VPC mode.  |  `None`  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation with browser ID and status.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
938
939
940
941
942
943
944
```
 | 
```
async defacreate_browser(
    self,
    name: str,
    execution_role_arn: str,
    network_mode: str = "PUBLIC",
    description: str = "",
    subnet_ids: Optional[List[str]] = None,
    security_group_ids: Optional[List[str]] = None,
    thread_id: str = "default",
) -> str:
"""
    Create a custom browser with specific configuration (asynchronous version).

    Args:
        name (str): Name for the browser. Must match pattern [a-zA-Z][a-zA-Z0-9_]{0,47}.
        execution_role_arn (str): IAM role ARN with permissions for browser operations.
        network_mode (str): Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".
        description (str): Description of the browser. Default is "".
        subnet_ids (Optional[List[str]]): Subnet IDs for VPC mode.
        security_group_ids (Optional[List[str]]): Security group IDs for VPC mode.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Confirmation with browser ID and status.

    """
    return await asyncio.to_thread(
        self.create_browser,
        name=name,
        execution_role_arn=execution_role_arn,
        network_mode=network_mode,
        description=description,
        subnet_ids=subnet_ids,
        security_group_ids=security_group_ids,
        thread_id=thread_id,
    )

```
 |  
| --- | --- |  
###  delete_browser [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.delete_browser "Permanent link")

```
delete_browser(
    browser_id: , thread_id:  = "default"
) -> 

```

Delete a custom browser (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `browser_id`  |  The browser identifier to delete.  |  _required_  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation of deletion.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
946
947
948
949
950
951
952
953
954
955
956
957
958
959
960
961
962
963
964
965
966
967
968
```
 | 
```
defdelete_browser(
    self,
    browser_id: str,
    thread_id: str = "default",
) -> str:
"""
    Delete a custom browser (synchronous version).

    Args:
        browser_id (str): The browser identifier to delete.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Confirmation of deletion.

    """
    try:
        browser_client = self._get_control_plane_client()
        response = browser_client.delete_browser(browser_id=browser_id)
        status = response.get("status", "unknown")
        return f"Browser '{browser_id}' deleted (Status: {status})"
    except Exception as e:
        return f"Error deleting browser: {e!s}"

```
 |  
| --- | --- |  
###  adelete_browser [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.adelete_browser "Permanent link")

```
adelete_browser(
    browser_id: , thread_id:  = "default"
) -> 

```

Delete a custom browser (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `browser_id`  |  The browser identifier to delete.  |  _required_  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation of deletion.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
970
971
972
973
974
975
976
977
978
979
980
981
982
983
984
985
986
987
988
```
 | 
```
async defadelete_browser(
    self,
    browser_id: str,
    thread_id: str = "default",
) -> str:
"""
    Delete a custom browser (asynchronous version).

    Args:
        browser_id (str): The browser identifier to delete.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Confirmation of deletion.

    """
    return await asyncio.to_thread(
        self.delete_browser, browser_id=browser_id, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  get_browser [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.get_browser "Permanent link")

```
get_browser(
    browser_id: , thread_id:  = "default"
) -> 

```

Get detailed information about a browser (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `browser_id`  |  The browser identifier.  |  _required_  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Browser details including name, status, and configuration.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
```
 | 
```
defget_browser(
    self,
    browser_id: str,
    thread_id: str = "default",
) -> str:
"""
    Get detailed information about a browser (synchronous version).

    Args:
        browser_id (str): The browser identifier.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Browser details including name, status, and configuration.

    """
    try:
        browser_client = self._get_control_plane_client()
        response = browser_client.get_browser(browser_id=browser_id)
        name = response.get("name", "N/A")
        status = response.get("status", "N/A")
        desc = response.get("description", "")
        result = f"Browser '{browser_id}':\n"
        result += f"  Name: {name}\n"
        result += f"  Status: {status}\n"
        if desc:
            result += f"  Description: {desc}\n"
        network = response.get("networkConfiguration", {})
        if network:
            result += f"  Network mode: {network.get('networkMode','N/A')}"
        return result
    except Exception as e:
        return f"Error getting browser: {e!s}"

```
 |  
| --- | --- |  
###  aget_browser [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.aget_browser "Permanent link")

```
aget_browser(
    browser_id: , thread_id:  = "default"
) -> 

```

Get detailed information about a browser (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `browser_id`  |  The browser identifier.  |  _required_  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Browser details including name, status, and configuration.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
```
 | 
```
async defaget_browser(
    self,
    browser_id: str,
    thread_id: str = "default",
) -> str:
"""
    Get detailed information about a browser (asynchronous version).

    Args:
        browser_id (str): The browser identifier.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Browser details including name, status, and configuration.

    """
    return await asyncio.to_thread(
        self.get_browser, browser_id=browser_id, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  take_control [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.take_control "Permanent link")

```
take_control(thread_id:  = 'default') -> 

```

Take manual control of a browser session by disabling the automation stream (synchronous version).
This allows a human to interact with the browser via the live view URL while preventing the automation agent from making changes.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
```
 | 
```
deftake_control(
    self,
    thread_id: str = "default",
) -> str:
"""
    Take manual control of a browser session by disabling the automation stream (synchronous version).

    This allows a human to interact with the browser via the live view URL while
    preventing the automation agent from making changes.

    Args:
        thread_id (str): Thread ID for the browser session. Default is "default".

    Returns:
        str: Confirmation message.

    """
    try:
        browser_client = self._session_manager.get_browser_client(thread_id)
        if browser_client is None:
            return (
                f"No browser session found for thread '{thread_id}'. "
                "Navigate to a URL first to start a session."
            )
        browser_client.take_control()
        return "Took manual control of the browser session. Automation stream disabled."
    except Exception as e:
        return f"Error taking control: {e!s}"

```
 |  
| --- | --- |  
###  atake_control [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.atake_control "Permanent link")

```
atake_control(thread_id:  = 'default') -> 

```

Take manual control of a browser session by disabling the automation stream (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
```
 | 
```
async defatake_control(
    self,
    thread_id: str = "default",
) -> str:
"""
    Take manual control of a browser session by disabling the automation stream (asynchronous version).

    Args:
        thread_id (str): Thread ID for the browser session. Default is "default".

    Returns:
        str: Confirmation message.

    """
    return await asyncio.to_thread(self.take_control, thread_id=thread_id)

```
 |  
| --- | --- |  
###  release_control [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.release_control "Permanent link")

```
release_control(thread_id:  = 'default') -> 

```

Release manual control and re-enable the automation stream (synchronous version).
This returns control to the automation agent after manual interaction.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
```
 | 
```
defrelease_control(
    self,
    thread_id: str = "default",
) -> str:
"""
    Release manual control and re-enable the automation stream (synchronous version).

    This returns control to the automation agent after manual interaction.

    Args:
        thread_id (str): Thread ID for the browser session. Default is "default".

    Returns:
        str: Confirmation message.

    """
    try:
        browser_client = self._session_manager.get_browser_client(thread_id)
        if browser_client is None:
            return (
                f"No browser session found for thread '{thread_id}'. "
                "Navigate to a URL first to start a session."
            )
        browser_client.release_control()
        return "Released manual control. Automation stream re-enabled."
    except Exception as e:
        return f"Error releasing control: {e!s}"

```
 |  
| --- | --- |  
###  arelease_control [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.arelease_control "Permanent link")

```
arelease_control(thread_id:  = 'default') -> 

```

Release manual control and re-enable the automation stream (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the browser session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
```
 | 
```
async defarelease_control(
    self,
    thread_id: str = "default",
) -> str:
"""
    Release manual control and re-enable the automation stream (asynchronous version).

    Args:
        thread_id (str): Thread ID for the browser session. Default is "default".

    Returns:
        str: Confirmation message.

    """
    return await asyncio.to_thread(self.release_control, thread_id=thread_id)

```
 |  
| --- | --- |  
###  cleanup [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreBrowserToolSpec.cleanup "Permanent link")

```
cleanup(thread_id: Optional[] = None) -> None

```

Clean up resources
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  `Optional[str]`  |  Optional thread ID to clean up. If None, cleans up all sessions.  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/browser/base.py`  
| 
```
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
```
 | 
```
async defcleanup(self, thread_id: Optional[str] = None) -> None:
"""
    Clean up resources

    Args:
        thread_id: Optional thread ID to clean up. If None, cleans up all sessions.

    """
    if thread_id:
        # Clean up a specific thread's session
        if thread_id in self._browser_clients:
            try:
                self._browser_clients[thread_id].stop()
                del self._browser_clients[thread_id]
                logger.info(f"Browser session for thread {thread_id} cleaned up")
            except Exception as e:
                logger.warning(
                    f"Error stopping browser for thread {thread_id}: {e}"
                )
    else:
        # Clean up all sessions
        thread_ids = list(self._browser_clients.keys())
        for tid in thread_ids:
            try:
                self._browser_clients[tid].stop()
            except Exception as e:
                logger.warning(f"Error stopping browser for thread {tid}: {e}")

        self._browser_clients = {}
        logger.info("All browser sessions cleaned up")

```
 |  
| --- | --- |  
##  AgentCoreCodeInterpreterToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec "Permanent link")
Bases: 
AWS Bedrock AgentCore Code Interpreter Tool Spec.
This toolkit provides a set of tools for working with a remote code interpreter environment:
  * execute_code - Run code in various languages (primarily Python)
  * execute_command - Run shell commands
  * read_files - Read content of files in the environment
  * list_files - List files in directories
  * delete_files - Remove files from the environment
  * write_files - Create or update files
  * start_command - Start long-running commands asynchronously
  * get_task - Check status of async tasks
  * stop_task - Stop running tasks


The toolkit lazily initializes the code interpreter session on first use. It supports multiple threads by maintaining separate code interpreter sessions for each thread ID.
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
 906
 907
 908
 909
 910
 911
 912
 913
 914
 915
 916
 917
 918
 919
 920
 921
 922
 923
 924
 925
 926
 927
 928
 929
 930
 931
 932
 933
 934
 935
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
```
 | 
```
classAgentCoreCodeInterpreterToolSpec(BaseToolSpec):
"""
    AWS Bedrock AgentCore Code Interpreter Tool Spec.

    This toolkit provides a set of tools for working with a remote code interpreter environment:

    * execute_code - Run code in various languages (primarily Python)
    * execute_command - Run shell commands
    * read_files - Read content of files in the environment
    * list_files - List files in directories
    * delete_files - Remove files from the environment
    * write_files - Create or update files
    * start_command - Start long-running commands asynchronously
    * get_task - Check status of async tasks
    * stop_task - Stop running tasks

    The toolkit lazily initializes the code interpreter session on first use.
    It supports multiple threads by maintaining separate code interpreter sessions for each thread ID.
    """

    spec_functions = [
        ("execute_code", "aexecute_code"),
        ("execute_command", "aexecute_command"),
        ("read_files", "aread_files"),
        ("list_files", "alist_files"),
        ("delete_files", "adelete_files"),
        ("write_files", "awrite_files"),
        ("start_command", "astart_command"),
        ("get_task", "aget_task"),
        ("stop_task", "astop_task"),
        ("upload_file", "aupload_file"),
        ("upload_files", "aupload_files"),
        ("install_packages", "ainstall_packages"),
        ("download_file", "adownload_file"),
        ("download_files", "adownload_files"),
        ("clear_context", "aclear_context"),
    ]

    def__init__(
        self,
        region: Optional[str] = None,
        identifier: Optional[str] = None,
    ) -> None:
"""
        Initialize the AWS Bedrock AgentCore Code Interpreter Tool Spec.

        Args:
            region (Optional[str]): AWS region to use for Bedrock AgentCore services.
                If not provided, will try to get it from environment variables.
            identifier (Optional[str]): Custom code interpreter identifier for
                VPC-enabled resources. If not provided, uses the default identifier.

        """
        self.region = region if region is not None else get_aws_region()
        self._identifier = identifier
        self._code_interpreters: Dict[str, CodeInterpreter] = {}
        self._cp_ci_client: Optional[CodeInterpreter] = None

    def_get_or_create_interpreter(self, thread_id: str = "default") -> CodeInterpreter:
"""
        Get or create a code interpreter for the specified thread.

        Args:
            thread_id: Thread ID for the code interpreter session

        Returns:
            CodeInterpreter instance

        """
        if thread_id in self._code_interpreters:
            return self._code_interpreters[thread_id]

        # Create a new code interpreter for this thread
        code_interpreter = CodeInterpreter(
            region=self.region, integration_source="llamaindex"
        )
        start_kwargs = {}
        if self._identifier is not None:
            start_kwargs["identifier"] = self._identifier
        code_interpreter.start(**start_kwargs)
        logger.info(
            f"Started code interpreter with session_id:{code_interpreter.session_id} for thread:{thread_id}"
        )

        # Store the interpreter
        self._code_interpreters[thread_id] = code_interpreter
        return code_interpreter

    def_get_control_plane_client(self) -> CodeInterpreter:
"""
        Get or create a code interpreter client for control-plane operations only.

        This client is used for account-level operations (list, create, delete, get)
        that do not require starting a session.
        """
        if self._cp_ci_client is None:
            self._cp_ci_client = CodeInterpreter(
                region=self.region, integration_source="llamaindex"
            )
        return self._cp_ci_client

    defexecute_code(
        self,
        code: str,
        language: str = "python",
        clear_context: bool = False,
        thread_id: str = "default",
    ) -> str:
"""
        Execute code in the code interpreter sandbox (synchronous version).

        Args:
            code (str): The code to execute.
            language (str): The programming language of the code. Default is "python".
            clear_context (bool): Whether to clear execution context. Default is False.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the code execution.

        """
        try:
            # Get or create code interpreter
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

            # Execute code
            response = code_interpreter.invoke(
                method="executeCode",
                params={
                    "code": code,
                    "language": language,
                    "clearContext": clear_context,
                },
            )

            return extract_output_from_stream(response)
        except Exception as e:
            return f"Error executing code: {e!s}"

    async defaexecute_code(
        self,
        code: str,
        language: str = "python",
        clear_context: bool = False,
        thread_id: str = "default",
    ) -> str:
"""
        Execute code in the code interpreter sandbox (asynchronous version).

        Args:
            code (str): The code to execute.
            language (str): The programming language of the code. Default is "python".
            clear_context (bool): Whether to clear execution context. Default is False.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the code execution.

        """
        return await asyncio.to_thread(
            self.execute_code,
            code=code,
            language=language,
            clear_context=clear_context,
            thread_id=thread_id,
        )

    defexecute_command(
        self,
        command: str,
        thread_id: str = "default",
    ) -> str:
"""
        Execute a shell command in the code interpreter sandbox (synchronous version).

        Args:
            command (str): The command to execute.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the command execution.

        """
        try:
            # Get or create code interpreter
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

            # Execute command
            response = code_interpreter.invoke(
                method="executeCommand", params={"command": command}
            )

            return extract_output_from_stream(response)
        except Exception as e:
            return f"Error executing command: {e!s}"

    async defaexecute_command(
        self,
        command: str,
        thread_id: str = "default",
    ) -> str:
"""
        Execute a shell command in the code interpreter sandbox (asynchronous version).

        Args:
            command (str): The command to execute.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the command execution.

        """
        return await asyncio.to_thread(
            self.execute_command, command=command, thread_id=thread_id
        )

    defread_files(
        self,
        paths: List[str],
        thread_id: str = "default",
    ) -> str:
"""
        Read content of files in the environment (synchronous version).

        Args:
            paths (List[str]): List of file paths to read.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The content of the files.

        """
        try:
            # Get or create code interpreter
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

            # Read files
            response = code_interpreter.invoke(
                method="readFiles", params={"paths": paths}
            )

            return extract_output_from_stream(response)
        except Exception as e:
            return f"Error reading files: {e!s}"

    async defaread_files(
        self,
        paths: List[str],
        thread_id: str = "default",
    ) -> str:
"""
        Read content of files in the environment (asynchronous version).

        Args:
            paths (List[str]): List of file paths to read.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The content of the files.

        """
        return await asyncio.to_thread(
            self.read_files, paths=paths, thread_id=thread_id
        )

    deflist_files(
        self,
        directory_path: str = "",
        thread_id: str = "default",
    ) -> str:
"""
        List files in directories in the environment (synchronous version).

        Args:
            directory_path (str): Path to the directory to list. Default is current directory.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The list of files.

        """
        try:
            # Get or create code interpreter
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

            # List files
            response = code_interpreter.invoke(
                method="listFiles", params={"directoryPath": directory_path}
            )

            return extract_output_from_stream(response)
        except Exception as e:
            return f"Error listing files: {e!s}"

    async defalist_files(
        self,
        directory_path: str = "",
        thread_id: str = "default",
    ) -> str:
"""
        List files in directories in the environment (asynchronous version).

        Args:
            directory_path (str): Path to the directory to list. Default is current directory.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The list of files.

        """
        return await asyncio.to_thread(
            self.list_files, directory_path=directory_path, thread_id=thread_id
        )

    defdelete_files(
        self,
        paths: List[str],
        thread_id: str = "default",
    ) -> str:
"""
        Remove files from the environment (synchronous version).

        Args:
            paths (List[str]): List of file paths to delete.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the delete operation.

        """
        try:
            # Get or create code interpreter
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

            # Remove files
            response = code_interpreter.invoke(
                method="removeFiles", params={"paths": paths}
            )

            return extract_output_from_stream(response)
        except Exception as e:
            return f"Error deleting files: {e!s}"

    async defadelete_files(
        self,
        paths: List[str],
        thread_id: str = "default",
    ) -> str:
"""
        Remove files from the environment (asynchronous version).

        Args:
            paths (List[str]): List of file paths to delete.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the delete operation.

        """
        return await asyncio.to_thread(
            self.delete_files, paths=paths, thread_id=thread_id
        )

    defwrite_files(
        self,
        files: List[Dict[str, str]],
        thread_id: str = "default",
    ) -> str:
"""
        Create or update files in the environment (synchronous version).

        Args:
            files (List[Dict[str, str]]): List of dictionaries with path and text fields.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the write operation.

        """
        try:
            # Get or create code interpreter
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

            # Write files
            response = code_interpreter.invoke(
                method="writeFiles", params={"content": files}
            )

            return extract_output_from_stream(response)
        except Exception as e:
            return f"Error writing files: {e!s}"

    async defawrite_files(
        self,
        files: List[Dict[str, str]],
        thread_id: str = "default",
    ) -> str:
"""
        Create or update files in the environment (asynchronous version).

        Args:
            files (List[Dict[str, str]]): List of dictionaries with path and text fields.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the write operation.

        """
        return await asyncio.to_thread(
            self.write_files, files=files, thread_id=thread_id
        )

    defstart_command(
        self,
        command: str,
        thread_id: str = "default",
    ) -> str:
"""
        Start a long-running command asynchronously (synchronous version).

        Args:
            command (str): The command to execute asynchronously.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The task ID and status.

        """
        try:
            # Get or create code interpreter
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

            # Start command execution
            response = code_interpreter.invoke(
                method="startCommandExecution", params={"command": command}
            )

            return extract_output_from_stream(response)
        except Exception as e:
            return f"Error starting command: {e!s}"

    async defastart_command(
        self,
        command: str,
        thread_id: str = "default",
    ) -> str:
"""
        Start a long-running command asynchronously (asynchronous version).

        Args:
            command (str): The command to execute asynchronously.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The task ID and status.

        """
        return await asyncio.to_thread(
            self.start_command, command=command, thread_id=thread_id
        )

    defget_task(
        self,
        task_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Check status of an async task (synchronous version).

        Args:
            task_id (str): The ID of the task to check.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The task status.

        """
        try:
            # Get or create code interpreter
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

            # Get task status
            response = code_interpreter.invoke(
                method="getTask", params={"taskId": task_id}
            )

            return extract_output_from_stream(response)
        except Exception as e:
            return f"Error getting task status: {e!s}"

    async defaget_task(
        self,
        task_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Check status of an async task (asynchronous version).

        Args:
            task_id (str): The ID of the task to check.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The task status.

        """
        return await asyncio.to_thread(
            self.get_task, task_id=task_id, thread_id=thread_id
        )

    defstop_task(
        self,
        task_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Stop a running task (synchronous version).

        Args:
            task_id (str): The ID of the task to stop.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the stop operation.

        """
        try:
            # Get or create code interpreter
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

            # Stop task
            response = code_interpreter.invoke(
                method="stopTask", params={"taskId": task_id}
            )

            return extract_output_from_stream(response)
        except Exception as e:
            return f"Error stopping task: {e!s}"

    async defastop_task(
        self,
        task_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Stop a running task (asynchronous version).

        Args:
            task_id (str): The ID of the task to stop.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The result of the stop operation.

        """
        return await asyncio.to_thread(
            self.stop_task, task_id=task_id, thread_id=thread_id
        )

    defupload_file(
        self,
        path: str,
        content: str,
        description: str = "",
        thread_id: str = "default",
    ) -> str:
"""
        Upload a file to the code interpreter sandbox (synchronous version).

        Args:
            path (str): Relative file path in the sandbox.
            content (str): File content as a string.
            description (str): Semantic description of the file. Default is "".
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: Confirmation message with the uploaded file path.

        """
        try:
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
            code_interpreter.upload_file(
                path=path, content=content, description=description
            )
            return f"Uploaded file to {path}"
        except Exception as e:
            return f"Error uploading file: {e!s}"

    async defaupload_file(
        self,
        path: str,
        content: str,
        description: str = "",
        thread_id: str = "default",
    ) -> str:
"""
        Upload a file to the code interpreter sandbox (asynchronous version).

        Args:
            path (str): Relative file path in the sandbox.
            content (str): File content as a string.
            description (str): Semantic description of the file. Default is "".
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: Confirmation message with the uploaded file path.

        """
        return await asyncio.to_thread(
            self.upload_file,
            path=path,
            content=content,
            description=description,
            thread_id=thread_id,
        )

    defupload_files(
        self,
        files: List[Dict[str, str]],
        thread_id: str = "default",
    ) -> str:
"""
        Upload multiple files to the code interpreter sandbox (synchronous version).

        Args:
            files (List[Dict[str, str]]): List of file specifications, each with
                'path', 'content', and optional 'description' keys.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: Confirmation message with the number of files uploaded.

        """
        try:
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
            code_interpreter.upload_files(files=files)
            return f"Uploaded {len(files)} file(s)"
        except Exception as e:
            return f"Error uploading files: {e!s}"

    async defaupload_files(
        self,
        files: List[Dict[str, str]],
        thread_id: str = "default",
    ) -> str:
"""
        Upload multiple files to the code interpreter sandbox (asynchronous version).

        Args:
            files (List[Dict[str, str]]): List of file specifications, each with
                'path', 'content', and optional 'description' keys.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: Confirmation message with the number of files uploaded.

        """
        return await asyncio.to_thread(
            self.upload_files, files=files, thread_id=thread_id
        )

    definstall_packages(
        self,
        packages: List[str],
        upgrade: bool = False,
        thread_id: str = "default",
    ) -> str:
"""
        Install Python packages in the code interpreter sandbox (synchronous version).

        Args:
            packages (List[str]): List of package names to install. Can include version
                specifiers (e.g., 'pandas>=2.0').
            upgrade (bool): Whether to upgrade existing packages. Default is False.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The pip install output (stdout/stderr).

        """
        try:
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
            result = code_interpreter.install_packages(
                packages=packages, upgrade=upgrade
            )
            return str(result)
        except Exception as e:
            return f"Error installing packages: {e!s}"

    async defainstall_packages(
        self,
        packages: List[str],
        upgrade: bool = False,
        thread_id: str = "default",
    ) -> str:
"""
        Install Python packages in the code interpreter sandbox (asynchronous version).

        Args:
            packages (List[str]): List of package names to install. Can include version
                specifiers (e.g., 'pandas>=2.0').
            upgrade (bool): Whether to upgrade existing packages. Default is False.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The pip install output (stdout/stderr).

        """
        return await asyncio.to_thread(
            self.install_packages,
            packages=packages,
            upgrade=upgrade,
            thread_id=thread_id,
        )

    defdownload_file(
        self,
        path: str,
        thread_id: str = "default",
    ) -> str:
"""
        Download a file from the code interpreter sandbox (synchronous version).

        Args:
            path (str): Path to the file in the sandbox.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The file content as text, or base64-encoded string for binary files.

        """
        try:
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
            content = code_interpreter.download_file(path=path)
            if isinstance(content, bytes):
                encoded = base64.b64encode(content).decode("utf-8")
                return f"[base64 encoded binary file: {path}]\n{encoded}"
            return content
        except Exception as e:
            return f"Error downloading file: {e!s}"

    async defadownload_file(
        self,
        path: str,
        thread_id: str = "default",
    ) -> str:
"""
        Download a file from the code interpreter sandbox (asynchronous version).

        Args:
            path (str): Path to the file in the sandbox.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: The file content as text, or base64-encoded string for binary files.

        """
        return await asyncio.to_thread(
            self.download_file, path=path, thread_id=thread_id
        )

    defdownload_files(
        self,
        paths: List[str],
        thread_id: str = "default",
    ) -> str:
"""
        Download multiple files from the code interpreter sandbox (synchronous version).

        Args:
            paths (List[str]): List of file paths in the sandbox.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: Formatted output with each file's content.

        """
        try:
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
            results = code_interpreter.download_files(paths=paths)
            output = []
            for file_path, content in results.items():
                if isinstance(content, bytes):
                    encoded = base64.b64encode(content).decode("utf-8")
                    output.append(
                        f"==== File: {file_path} (binary, base64) ====\n{encoded}"
                    )
                else:
                    output.append(f"==== File: {file_path} ====\n{content}")
            return "\n\n".join(output)
        except Exception as e:
            return f"Error downloading files: {e!s}"

    async defadownload_files(
        self,
        paths: List[str],
        thread_id: str = "default",
    ) -> str:
"""
        Download multiple files from the code interpreter sandbox (asynchronous version).

        Args:
            paths (List[str]): List of file paths in the sandbox.
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: Formatted output with each file's content.

        """
        return await asyncio.to_thread(
            self.download_files, paths=paths, thread_id=thread_id
        )

    deflist_code_interpreters(
        self,
        interpreter_type: Optional[str] = None,
        max_results: int = 10,
        thread_id: str = "default",
    ) -> str:
"""
        List all code interpreters in the account (synchronous version).

        Args:
            interpreter_type (Optional[str]): Filter by type: "SYSTEM" or "CUSTOM".
            max_results (int): Maximum results to return (1-100). Default is 10.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Formatted list of code interpreter summaries.

        """
        try:
            code_interpreter = self._get_control_plane_client()
            response = code_interpreter.list_code_interpreters(
                interpreter_type=interpreter_type, max_results=max_results
            )
            summaries = response.get("codeInterpreterSummaries", [])
            if not summaries:
                return "No code interpreters found."
            lines = []
            for ci in summaries:
                lines.append(
                    f"- {ci.get('name','N/A')} (ID: {ci.get('codeInterpreterId','N/A')}, "
                    f"Status: {ci.get('status','N/A')}, Type: {ci.get('type','N/A')})"
                )
            return f"Found {len(summaries)} code interpreter(s):\n" + "\n".join(lines)
        except Exception as e:
            return f"Error listing code interpreters: {e!s}"

    async defalist_code_interpreters(
        self,
        interpreter_type: Optional[str] = None,
        max_results: int = 10,
        thread_id: str = "default",
    ) -> str:
"""
        List all code interpreters in the account (asynchronous version).

        Args:
            interpreter_type (Optional[str]): Filter by type: "SYSTEM" or "CUSTOM".
            max_results (int): Maximum results to return (1-100). Default is 10.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Formatted list of code interpreter summaries.

        """
        return await asyncio.to_thread(
            self.list_code_interpreters,
            interpreter_type=interpreter_type,
            max_results=max_results,
            thread_id=thread_id,
        )

    defcreate_code_interpreter(
        self,
        name: str,
        execution_role_arn: str,
        network_mode: str = "PUBLIC",
        description: str = "",
        subnet_ids: Optional[List[str]] = None,
        security_group_ids: Optional[List[str]] = None,
        thread_id: str = "default",
    ) -> str:
"""
        Create a custom code interpreter with specific configuration (synchronous version).

        Args:
            name (str): Name for the interpreter. Must match pattern [a-zA-Z][a-zA-Z0-9_]{0,47}.
            execution_role_arn (str): IAM role ARN with permissions for interpreter operations.
            network_mode (str): Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".
            description (str): Description of the interpreter. Default is "".
            subnet_ids (Optional[List[str]]): Subnet IDs for VPC mode.
            security_group_ids (Optional[List[str]]): Security group IDs for VPC mode.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Confirmation with interpreter ID and status.

        """
        try:
            code_interpreter = self._get_control_plane_client()
            network_config: Dict[str, Any] = {"networkMode": network_mode}
            if subnet_ids or security_group_ids:
                vpc_config: Dict[str, Any] = {}
                if subnet_ids:
                    vpc_config["subnets"] = subnet_ids
                if security_group_ids:
                    vpc_config["securityGroups"] = security_group_ids
                network_config["vpcConfig"] = vpc_config
            kwargs: Dict[str, Any] = {
                "name": name,
                "execution_role_arn": execution_role_arn,
                "network_configuration": network_config,
            }
            if description:
                kwargs["description"] = description
            response = code_interpreter.create_code_interpreter(**kwargs)
            interpreter_id = response.get("codeInterpreterId", "unknown")
            status = response.get("status", "unknown")
            return f"Code interpreter created (ID: {interpreter_id}, Status: {status})"
        except Exception as e:
            return f"Error creating code interpreter: {e!s}"

    async defacreate_code_interpreter(
        self,
        name: str,
        execution_role_arn: str,
        network_mode: str = "PUBLIC",
        description: str = "",
        subnet_ids: Optional[List[str]] = None,
        security_group_ids: Optional[List[str]] = None,
        thread_id: str = "default",
    ) -> str:
"""
        Create a custom code interpreter with specific configuration (asynchronous version).

        Args:
            name (str): Name for the interpreter. Must match pattern [a-zA-Z][a-zA-Z0-9_]{0,47}.
            execution_role_arn (str): IAM role ARN with permissions for interpreter operations.
            network_mode (str): Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".
            description (str): Description of the interpreter. Default is "".
            subnet_ids (Optional[List[str]]): Subnet IDs for VPC mode.
            security_group_ids (Optional[List[str]]): Security group IDs for VPC mode.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Confirmation with interpreter ID and status.

        """
        return await asyncio.to_thread(
            self.create_code_interpreter,
            name=name,
            execution_role_arn=execution_role_arn,
            network_mode=network_mode,
            description=description,
            subnet_ids=subnet_ids,
            security_group_ids=security_group_ids,
            thread_id=thread_id,
        )

    defdelete_code_interpreter(
        self,
        interpreter_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Delete a custom code interpreter (synchronous version).

        Args:
            interpreter_id (str): The code interpreter identifier to delete.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Confirmation of deletion.

        """
        try:
            code_interpreter = self._get_control_plane_client()
            response = code_interpreter.delete_code_interpreter(
                interpreter_id=interpreter_id
            )
            status = response.get("status", "unknown")
            return f"Code interpreter '{interpreter_id}' deleted (Status: {status})"
        except Exception as e:
            return f"Error deleting code interpreter: {e!s}"

    async defadelete_code_interpreter(
        self,
        interpreter_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Delete a custom code interpreter (asynchronous version).

        Args:
            interpreter_id (str): The code interpreter identifier to delete.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Confirmation of deletion.

        """
        return await asyncio.to_thread(
            self.delete_code_interpreter,
            interpreter_id=interpreter_id,
            thread_id=thread_id,
        )

    defget_code_interpreter(
        self,
        interpreter_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Get detailed information about a code interpreter (synchronous version).

        Args:
            interpreter_id (str): The code interpreter identifier.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Interpreter details including name, status, and configuration.

        """
        try:
            code_interpreter = self._get_control_plane_client()
            response = code_interpreter.get_code_interpreter(
                interpreter_id=interpreter_id
            )
            name = response.get("name", "N/A")
            status = response.get("status", "N/A")
            desc = response.get("description", "")
            result = f"Code interpreter '{interpreter_id}':\n"
            result += f"  Name: {name}\n"
            result += f"  Status: {status}\n"
            if desc:
                result += f"  Description: {desc}\n"
            network = response.get("networkConfiguration", {})
            if network:
                result += f"  Network mode: {network.get('networkMode','N/A')}"
            return result
        except Exception as e:
            return f"Error getting code interpreter: {e!s}"

    async defaget_code_interpreter(
        self,
        interpreter_id: str,
        thread_id: str = "default",
    ) -> str:
"""
        Get detailed information about a code interpreter (asynchronous version).

        Args:
            interpreter_id (str): The code interpreter identifier.
            thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

        Returns:
            str: Interpreter details including name, status, and configuration.

        """
        return await asyncio.to_thread(
            self.get_code_interpreter,
            interpreter_id=interpreter_id,
            thread_id=thread_id,
        )

    defclear_context(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Clear all variable state in the Python execution context (synchronous version).

        This resets the interpreter to a fresh state, removing all previously defined
        variables, imports, and function definitions.

        Args:
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: Confirmation that the context was cleared.

        """
        try:
            code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
            code_interpreter.clear_context()
            return "Python execution context cleared successfully."
        except Exception as e:
            return f"Error clearing context: {e!s}"

    async defaclear_context(
        self,
        thread_id: str = "default",
    ) -> str:
"""
        Clear all variable state in the Python execution context (asynchronous version).

        Args:
            thread_id (str): Thread ID for the code interpreter session. Default is "default".

        Returns:
            str: Confirmation that the context was cleared.

        """
        return await asyncio.to_thread(self.clear_context, thread_id=thread_id)

    async defcleanup(self, thread_id: Optional[str] = None) -> None:
"""
        Clean up resources

        Args:
            thread_id: Optional thread ID to clean up. If None, cleans up all sessions.

        """
        if thread_id:
            # Clean up a specific thread's session
            if thread_id in self._code_interpreters:
                try:
                    self._code_interpreters[thread_id].stop()
                    del self._code_interpreters[thread_id]
                    logger.info(
                        f"Code interpreter session for thread {thread_id} cleaned up"
                    )
                except Exception as e:
                    logger.warning(
                        f"Error stopping code interpreter for thread {thread_id}: {e}"
                    )
        else:
            # Clean up all sessions
            thread_ids = list(self._code_interpreters.keys())
            for tid in thread_ids:
                try:
                    self._code_interpreters[tid].stop()
                except Exception as e:
                    logger.warning(
                        f"Error stopping code interpreter for thread {tid}: {e}"
                    )

            self._code_interpreters = {}
            logger.info("All code interpreter sessions cleaned up")

```
 |  
| --- | --- |  
###  execute_code [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.execute_code "Permanent link")

```
execute_code(
    code: ,
    language:  = "python",
    clear_context:  = False,
    thread_id:  = "default",
) -> 

```

Execute code in the code interpreter sandbox (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `code`  |  The code to execute.  |  _required_  |  
|  `language`  |  The programming language of the code. Default is "python".  |  `'python'`  |  
|  `clear_context`  |  `bool`  |  Whether to clear execution context. Default is False.  |  `False`  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the code execution.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defexecute_code(
    self,
    code: str,
    language: str = "python",
    clear_context: bool = False,
    thread_id: str = "default",
) -> str:
"""
    Execute code in the code interpreter sandbox (synchronous version).

    Args:
        code (str): The code to execute.
        language (str): The programming language of the code. Default is "python".
        clear_context (bool): Whether to clear execution context. Default is False.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the code execution.

    """
    try:
        # Get or create code interpreter
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

        # Execute code
        response = code_interpreter.invoke(
            method="executeCode",
            params={
                "code": code,
                "language": language,
                "clearContext": clear_context,
            },
        )

        return extract_output_from_stream(response)
    except Exception as e:
        return f"Error executing code: {e!s}"

```
 |  
| --- | --- |  
###  aexecute_code [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.aexecute_code "Permanent link")

```
aexecute_code(
    code: ,
    language:  = "python",
    clear_context:  = False,
    thread_id:  = "default",
) -> 

```

Execute code in the code interpreter sandbox (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `code`  |  The code to execute.  |  _required_  |  
|  `language`  |  The programming language of the code. Default is "python".  |  `'python'`  |  
|  `clear_context`  |  `bool`  |  Whether to clear execution context. Default is False.  |  `False`  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the code execution.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defaexecute_code(
    self,
    code: str,
    language: str = "python",
    clear_context: bool = False,
    thread_id: str = "default",
) -> str:
"""
    Execute code in the code interpreter sandbox (asynchronous version).

    Args:
        code (str): The code to execute.
        language (str): The programming language of the code. Default is "python".
        clear_context (bool): Whether to clear execution context. Default is False.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the code execution.

    """
    return await asyncio.to_thread(
        self.execute_code,
        code=code,
        language=language,
        clear_context=clear_context,
        thread_id=thread_id,
    )

```
 |  
| --- | --- |  
###  execute_command [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.execute_command "Permanent link")

```
execute_command(
    command: , thread_id:  = "default"
) -> 

```

Execute a shell command in the code interpreter sandbox (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `command`  |  The command to execute.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the command execution.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defexecute_command(
    self,
    command: str,
    thread_id: str = "default",
) -> str:
"""
    Execute a shell command in the code interpreter sandbox (synchronous version).

    Args:
        command (str): The command to execute.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the command execution.

    """
    try:
        # Get or create code interpreter
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

        # Execute command
        response = code_interpreter.invoke(
            method="executeCommand", params={"command": command}
        )

        return extract_output_from_stream(response)
    except Exception as e:
        return f"Error executing command: {e!s}"

```
 |  
| --- | --- |  
###  aexecute_command [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.aexecute_command "Permanent link")

```
aexecute_command(
    command: , thread_id:  = "default"
) -> 

```

Execute a shell command in the code interpreter sandbox (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `command`  |  The command to execute.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the command execution.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
async defaexecute_command(
    self,
    command: str,
    thread_id: str = "default",
) -> str:
"""
    Execute a shell command in the code interpreter sandbox (asynchronous version).

    Args:
        command (str): The command to execute.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the command execution.

    """
    return await asyncio.to_thread(
        self.execute_command, command=command, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  read_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.read_files "Permanent link")

```
read_files(
    paths: [], thread_id:  = "default"
) -> 

```

Read content of files in the environment (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `paths`  |  `List[str]`  |  List of file paths to read.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The content of the files.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defread_files(
    self,
    paths: List[str],
    thread_id: str = "default",
) -> str:
"""
    Read content of files in the environment (synchronous version).

    Args:
        paths (List[str]): List of file paths to read.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The content of the files.

    """
    try:
        # Get or create code interpreter
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

        # Read files
        response = code_interpreter.invoke(
            method="readFiles", params={"paths": paths}
        )

        return extract_output_from_stream(response)
    except Exception as e:
        return f"Error reading files: {e!s}"

```
 |  
| --- | --- |  
###  aread_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.aread_files "Permanent link")

```
aread_files(
    paths: [], thread_id:  = "default"
) -> 

```

Read content of files in the environment (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `paths`  |  `List[str]`  |  List of file paths to read.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The content of the files.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defaread_files(
    self,
    paths: List[str],
    thread_id: str = "default",
) -> str:
"""
    Read content of files in the environment (asynchronous version).

    Args:
        paths (List[str]): List of file paths to read.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The content of the files.

    """
    return await asyncio.to_thread(
        self.read_files, paths=paths, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  list_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.list_files "Permanent link")

```
list_files(
    directory_path:  = "", thread_id:  = "default"
) -> 

```

List files in directories in the environment (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `directory_path`  |  Path to the directory to list. Default is current directory.  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The list of files.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
deflist_files(
    self,
    directory_path: str = "",
    thread_id: str = "default",
) -> str:
"""
    List files in directories in the environment (synchronous version).

    Args:
        directory_path (str): Path to the directory to list. Default is current directory.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The list of files.

    """
    try:
        # Get or create code interpreter
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

        # List files
        response = code_interpreter.invoke(
            method="listFiles", params={"directoryPath": directory_path}
        )

        return extract_output_from_stream(response)
    except Exception as e:
        return f"Error listing files: {e!s}"

```
 |  
| --- | --- |  
###  alist_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.alist_files "Permanent link")

```
alist_files(
    directory_path:  = "", thread_id:  = "default"
) -> 

```

List files in directories in the environment (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `directory_path`  |  Path to the directory to list. Default is current directory.  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The list of files.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defalist_files(
    self,
    directory_path: str = "",
    thread_id: str = "default",
) -> str:
"""
    List files in directories in the environment (asynchronous version).

    Args:
        directory_path (str): Path to the directory to list. Default is current directory.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The list of files.

    """
    return await asyncio.to_thread(
        self.list_files, directory_path=directory_path, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  delete_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.delete_files "Permanent link")

```
delete_files(
    paths: [], thread_id:  = "default"
) -> 

```

Remove files from the environment (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `paths`  |  `List[str]`  |  List of file paths to delete.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the delete operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defdelete_files(
    self,
    paths: List[str],
    thread_id: str = "default",
) -> str:
"""
    Remove files from the environment (synchronous version).

    Args:
        paths (List[str]): List of file paths to delete.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the delete operation.

    """
    try:
        # Get or create code interpreter
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

        # Remove files
        response = code_interpreter.invoke(
            method="removeFiles", params={"paths": paths}
        )

        return extract_output_from_stream(response)
    except Exception as e:
        return f"Error deleting files: {e!s}"

```
 |  
| --- | --- |  
###  adelete_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.adelete_files "Permanent link")

```
adelete_files(
    paths: [], thread_id:  = "default"
) -> 

```

Remove files from the environment (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `paths`  |  `List[str]`  |  List of file paths to delete.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the delete operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defadelete_files(
    self,
    paths: List[str],
    thread_id: str = "default",
) -> str:
"""
    Remove files from the environment (asynchronous version).

    Args:
        paths (List[str]): List of file paths to delete.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the delete operation.

    """
    return await asyncio.to_thread(
        self.delete_files, paths=paths, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  write_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.write_files "Permanent link")

```
write_files(
    files: [[, ]], thread_id:  = "default"
) -> 

```

Create or update files in the environment (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `files`  |  `List[Dict[str, str]]`  |  List of dictionaries with path and text fields.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the write operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defwrite_files(
    self,
    files: List[Dict[str, str]],
    thread_id: str = "default",
) -> str:
"""
    Create or update files in the environment (synchronous version).

    Args:
        files (List[Dict[str, str]]): List of dictionaries with path and text fields.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the write operation.

    """
    try:
        # Get or create code interpreter
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

        # Write files
        response = code_interpreter.invoke(
            method="writeFiles", params={"content": files}
        )

        return extract_output_from_stream(response)
    except Exception as e:
        return f"Error writing files: {e!s}"

```
 |  
| --- | --- |  
###  awrite_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.awrite_files "Permanent link")

```
awrite_files(
    files: [[, ]], thread_id:  = "default"
) -> 

```

Create or update files in the environment (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `files`  |  `List[Dict[str, str]]`  |  List of dictionaries with path and text fields.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the write operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defawrite_files(
    self,
    files: List[Dict[str, str]],
    thread_id: str = "default",
) -> str:
"""
    Create or update files in the environment (asynchronous version).

    Args:
        files (List[Dict[str, str]]): List of dictionaries with path and text fields.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the write operation.

    """
    return await asyncio.to_thread(
        self.write_files, files=files, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  start_command [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.start_command "Permanent link")

```
start_command(
    command: , thread_id:  = "default"
) -> 

```

Start a long-running command asynchronously (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `command`  |  The command to execute asynchronously.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The task ID and status.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defstart_command(
    self,
    command: str,
    thread_id: str = "default",
) -> str:
"""
    Start a long-running command asynchronously (synchronous version).

    Args:
        command (str): The command to execute asynchronously.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The task ID and status.

    """
    try:
        # Get or create code interpreter
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

        # Start command execution
        response = code_interpreter.invoke(
            method="startCommandExecution", params={"command": command}
        )

        return extract_output_from_stream(response)
    except Exception as e:
        return f"Error starting command: {e!s}"

```
 |  
| --- | --- |  
###  astart_command [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.astart_command "Permanent link")

```
astart_command(
    command: , thread_id:  = "default"
) -> 

```

Start a long-running command asynchronously (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `command`  |  The command to execute asynchronously.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The task ID and status.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defastart_command(
    self,
    command: str,
    thread_id: str = "default",
) -> str:
"""
    Start a long-running command asynchronously (asynchronous version).

    Args:
        command (str): The command to execute asynchronously.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The task ID and status.

    """
    return await asyncio.to_thread(
        self.start_command, command=command, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  get_task [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.get_task "Permanent link")

```
get_task(task_id: , thread_id:  = 'default') -> 

```

Check status of an async task (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `task_id`  |  The ID of the task to check.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The task status.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defget_task(
    self,
    task_id: str,
    thread_id: str = "default",
) -> str:
"""
    Check status of an async task (synchronous version).

    Args:
        task_id (str): The ID of the task to check.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The task status.

    """
    try:
        # Get or create code interpreter
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

        # Get task status
        response = code_interpreter.invoke(
            method="getTask", params={"taskId": task_id}
        )

        return extract_output_from_stream(response)
    except Exception as e:
        return f"Error getting task status: {e!s}"

```
 |  
| --- | --- |  
###  aget_task [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.aget_task "Permanent link")

```
aget_task(task_id: , thread_id:  = 'default') -> 

```

Check status of an async task (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `task_id`  |  The ID of the task to check.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The task status.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defaget_task(
    self,
    task_id: str,
    thread_id: str = "default",
) -> str:
"""
    Check status of an async task (asynchronous version).

    Args:
        task_id (str): The ID of the task to check.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The task status.

    """
    return await asyncio.to_thread(
        self.get_task, task_id=task_id, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  stop_task [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.stop_task "Permanent link")

```
stop_task(task_id: , thread_id:  = 'default') -> 

```

Stop a running task (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `task_id`  |  The ID of the task to stop.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the stop operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defstop_task(
    self,
    task_id: str,
    thread_id: str = "default",
) -> str:
"""
    Stop a running task (synchronous version).

    Args:
        task_id (str): The ID of the task to stop.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the stop operation.

    """
    try:
        # Get or create code interpreter
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)

        # Stop task
        response = code_interpreter.invoke(
            method="stopTask", params={"taskId": task_id}
        )

        return extract_output_from_stream(response)
    except Exception as e:
        return f"Error stopping task: {e!s}"

```
 |  
| --- | --- |  
###  astop_task [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.astop_task "Permanent link")

```
astop_task(task_id: , thread_id:  = 'default') -> 

```

Stop a running task (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `task_id`  |  The ID of the task to stop.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The result of the stop operation.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defastop_task(
    self,
    task_id: str,
    thread_id: str = "default",
) -> str:
"""
    Stop a running task (asynchronous version).

    Args:
        task_id (str): The ID of the task to stop.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The result of the stop operation.

    """
    return await asyncio.to_thread(
        self.stop_task, task_id=task_id, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  upload_file [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.upload_file "Permanent link")

```
upload_file(
    path: ,
    content: ,
    description:  = "",
    thread_id:  = "default",
) -> 

```

Upload a file to the code interpreter sandbox (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `path`  |  Relative file path in the sandbox.  |  _required_  |  
|  `content`  |  File content as a string.  |  _required_  |  
|  `description`  |  Semantic description of the file. Default is "".  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message with the uploaded file path.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defupload_file(
    self,
    path: str,
    content: str,
    description: str = "",
    thread_id: str = "default",
) -> str:
"""
    Upload a file to the code interpreter sandbox (synchronous version).

    Args:
        path (str): Relative file path in the sandbox.
        content (str): File content as a string.
        description (str): Semantic description of the file. Default is "".
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: Confirmation message with the uploaded file path.

    """
    try:
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
        code_interpreter.upload_file(
            path=path, content=content, description=description
        )
        return f"Uploaded file to {path}"
    except Exception as e:
        return f"Error uploading file: {e!s}"

```
 |  
| --- | --- |  
###  aupload_file [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.aupload_file "Permanent link")

```
aupload_file(
    path: ,
    content: ,
    description:  = "",
    thread_id:  = "default",
) -> 

```

Upload a file to the code interpreter sandbox (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `path`  |  Relative file path in the sandbox.  |  _required_  |  
|  `content`  |  File content as a string.  |  _required_  |  
|  `description`  |  Semantic description of the file. Default is "".  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message with the uploaded file path.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defaupload_file(
    self,
    path: str,
    content: str,
    description: str = "",
    thread_id: str = "default",
) -> str:
"""
    Upload a file to the code interpreter sandbox (asynchronous version).

    Args:
        path (str): Relative file path in the sandbox.
        content (str): File content as a string.
        description (str): Semantic description of the file. Default is "".
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: Confirmation message with the uploaded file path.

    """
    return await asyncio.to_thread(
        self.upload_file,
        path=path,
        content=content,
        description=description,
        thread_id=thread_id,
    )

```
 |  
| --- | --- |  
###  upload_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.upload_files "Permanent link")

```
upload_files(
    files: [[, ]], thread_id:  = "default"
) -> 

```

Upload multiple files to the code interpreter sandbox (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `files`  |  `List[Dict[str, str]]`  |  List of file specifications, each with 'path', 'content', and optional 'description' keys.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message with the number of files uploaded.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defupload_files(
    self,
    files: List[Dict[str, str]],
    thread_id: str = "default",
) -> str:
"""
    Upload multiple files to the code interpreter sandbox (synchronous version).

    Args:
        files (List[Dict[str, str]]): List of file specifications, each with
            'path', 'content', and optional 'description' keys.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: Confirmation message with the number of files uploaded.

    """
    try:
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
        code_interpreter.upload_files(files=files)
        return f"Uploaded {len(files)} file(s)"
    except Exception as e:
        return f"Error uploading files: {e!s}"

```
 |  
| --- | --- |  
###  aupload_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.aupload_files "Permanent link")

```
aupload_files(
    files: [[, ]], thread_id:  = "default"
) -> 

```

Upload multiple files to the code interpreter sandbox (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `files`  |  `List[Dict[str, str]]`  |  List of file specifications, each with 'path', 'content', and optional 'description' keys.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation message with the number of files uploaded.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defaupload_files(
    self,
    files: List[Dict[str, str]],
    thread_id: str = "default",
) -> str:
"""
    Upload multiple files to the code interpreter sandbox (asynchronous version).

    Args:
        files (List[Dict[str, str]]): List of file specifications, each with
            'path', 'content', and optional 'description' keys.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: Confirmation message with the number of files uploaded.

    """
    return await asyncio.to_thread(
        self.upload_files, files=files, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  install_packages [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.install_packages "Permanent link")

```
install_packages(
    packages: [],
    upgrade:  = False,
    thread_id:  = "default",
) -> 

```

Install Python packages in the code interpreter sandbox (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `packages`  |  `List[str]`  |  List of package names to install. Can include version specifiers (e.g., 'pandas>=2.0').  |  _required_  |  
|  `upgrade`  |  `bool`  |  Whether to upgrade existing packages. Default is False.  |  `False`  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The pip install output (stdout/stderr).  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
definstall_packages(
    self,
    packages: List[str],
    upgrade: bool = False,
    thread_id: str = "default",
) -> str:
"""
    Install Python packages in the code interpreter sandbox (synchronous version).

    Args:
        packages (List[str]): List of package names to install. Can include version
            specifiers (e.g., 'pandas>=2.0').
        upgrade (bool): Whether to upgrade existing packages. Default is False.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The pip install output (stdout/stderr).

    """
    try:
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
        result = code_interpreter.install_packages(
            packages=packages, upgrade=upgrade
        )
        return str(result)
    except Exception as e:
        return f"Error installing packages: {e!s}"

```
 |  
| --- | --- |  
###  ainstall_packages [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.ainstall_packages "Permanent link")

```
ainstall_packages(
    packages: [],
    upgrade:  = False,
    thread_id:  = "default",
) -> 

```

Install Python packages in the code interpreter sandbox (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `packages`  |  `List[str]`  |  List of package names to install. Can include version specifiers (e.g., 'pandas>=2.0').  |  _required_  |  
|  `upgrade`  |  `bool`  |  Whether to upgrade existing packages. Default is False.  |  `False`  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The pip install output (stdout/stderr).  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defainstall_packages(
    self,
    packages: List[str],
    upgrade: bool = False,
    thread_id: str = "default",
) -> str:
"""
    Install Python packages in the code interpreter sandbox (asynchronous version).

    Args:
        packages (List[str]): List of package names to install. Can include version
            specifiers (e.g., 'pandas>=2.0').
        upgrade (bool): Whether to upgrade existing packages. Default is False.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The pip install output (stdout/stderr).

    """
    return await asyncio.to_thread(
        self.install_packages,
        packages=packages,
        upgrade=upgrade,
        thread_id=thread_id,
    )

```
 |  
| --- | --- |  
###  download_file [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.download_file "Permanent link")

```
download_file(path: , thread_id:  = 'default') -> 

```

Download a file from the code interpreter sandbox (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `path`  |  Path to the file in the sandbox.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The file content as text, or base64-encoded string for binary files.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defdownload_file(
    self,
    path: str,
    thread_id: str = "default",
) -> str:
"""
    Download a file from the code interpreter sandbox (synchronous version).

    Args:
        path (str): Path to the file in the sandbox.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The file content as text, or base64-encoded string for binary files.

    """
    try:
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
        content = code_interpreter.download_file(path=path)
        if isinstance(content, bytes):
            encoded = base64.b64encode(content).decode("utf-8")
            return f"[base64 encoded binary file: {path}]\n{encoded}"
        return content
    except Exception as e:
        return f"Error downloading file: {e!s}"

```
 |  
| --- | --- |  
###  adownload_file [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.adownload_file "Permanent link")

```
adownload_file(
    path: , thread_id:  = "default"
) -> 

```

Download a file from the code interpreter sandbox (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `path`  |  Path to the file in the sandbox.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  The file content as text, or base64-encoded string for binary files.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defadownload_file(
    self,
    path: str,
    thread_id: str = "default",
) -> str:
"""
    Download a file from the code interpreter sandbox (asynchronous version).

    Args:
        path (str): Path to the file in the sandbox.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: The file content as text, or base64-encoded string for binary files.

    """
    return await asyncio.to_thread(
        self.download_file, path=path, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  download_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.download_files "Permanent link")

```
download_files(
    paths: [], thread_id:  = "default"
) -> 

```

Download multiple files from the code interpreter sandbox (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `paths`  |  `List[str]`  |  List of file paths in the sandbox.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Formatted output with each file's content.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
defdownload_files(
    self,
    paths: List[str],
    thread_id: str = "default",
) -> str:
"""
    Download multiple files from the code interpreter sandbox (synchronous version).

    Args:
        paths (List[str]): List of file paths in the sandbox.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: Formatted output with each file's content.

    """
    try:
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
        results = code_interpreter.download_files(paths=paths)
        output = []
        for file_path, content in results.items():
            if isinstance(content, bytes):
                encoded = base64.b64encode(content).decode("utf-8")
                output.append(
                    f"==== File: {file_path} (binary, base64) ====\n{encoded}"
                )
            else:
                output.append(f"==== File: {file_path} ====\n{content}")
        return "\n\n".join(output)
    except Exception as e:
        return f"Error downloading files: {e!s}"

```
 |  
| --- | --- |  
###  adownload_files [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.adownload_files "Permanent link")

```
adownload_files(
    paths: [], thread_id:  = "default"
) -> 

```

Download multiple files from the code interpreter sandbox (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `paths`  |  `List[str]`  |  List of file paths in the sandbox.  |  _required_  |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Formatted output with each file's content.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
async defadownload_files(
    self,
    paths: List[str],
    thread_id: str = "default",
) -> str:
"""
    Download multiple files from the code interpreter sandbox (asynchronous version).

    Args:
        paths (List[str]): List of file paths in the sandbox.
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: Formatted output with each file's content.

    """
    return await asyncio.to_thread(
        self.download_files, paths=paths, thread_id=thread_id
    )

```
 |  
| --- | --- |  
###  list_code_interpreters [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.list_code_interpreters "Permanent link")

```
list_code_interpreters(
    interpreter_type: Optional[] = None,
    max_results:  = 10,
    thread_id:  = "default",
) -> 

```

List all code interpreters in the account (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `interpreter_type`  |  `Optional[str]`  |  Filter by type: "SYSTEM" or "CUSTOM".  |  `None`  |  
|  `max_results`  |  Maximum results to return (1-100). Default is 10.  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Formatted list of code interpreter summaries.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
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
```
 | 
```
deflist_code_interpreters(
    self,
    interpreter_type: Optional[str] = None,
    max_results: int = 10,
    thread_id: str = "default",
) -> str:
"""
    List all code interpreters in the account (synchronous version).

    Args:
        interpreter_type (Optional[str]): Filter by type: "SYSTEM" or "CUSTOM".
        max_results (int): Maximum results to return (1-100). Default is 10.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Formatted list of code interpreter summaries.

    """
    try:
        code_interpreter = self._get_control_plane_client()
        response = code_interpreter.list_code_interpreters(
            interpreter_type=interpreter_type, max_results=max_results
        )
        summaries = response.get("codeInterpreterSummaries", [])
        if not summaries:
            return "No code interpreters found."
        lines = []
        for ci in summaries:
            lines.append(
                f"- {ci.get('name','N/A')} (ID: {ci.get('codeInterpreterId','N/A')}, "
                f"Status: {ci.get('status','N/A')}, Type: {ci.get('type','N/A')})"
            )
        return f"Found {len(summaries)} code interpreter(s):\n" + "\n".join(lines)
    except Exception as e:
        return f"Error listing code interpreters: {e!s}"

```
 |  
| --- | --- |  
###  alist_code_interpreters [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.alist_code_interpreters "Permanent link")

```
alist_code_interpreters(
    interpreter_type: Optional[] = None,
    max_results:  = 10,
    thread_id:  = "default",
) -> 

```

List all code interpreters in the account (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `interpreter_type`  |  `Optional[str]`  |  Filter by type: "SYSTEM" or "CUSTOM".  |  `None`  |  
|  `max_results`  |  Maximum results to return (1-100). Default is 10.  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Formatted list of code interpreter summaries.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
```
 | 
```
async defalist_code_interpreters(
    self,
    interpreter_type: Optional[str] = None,
    max_results: int = 10,
    thread_id: str = "default",
) -> str:
"""
    List all code interpreters in the account (asynchronous version).

    Args:
        interpreter_type (Optional[str]): Filter by type: "SYSTEM" or "CUSTOM".
        max_results (int): Maximum results to return (1-100). Default is 10.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Formatted list of code interpreter summaries.

    """
    return await asyncio.to_thread(
        self.list_code_interpreters,
        interpreter_type=interpreter_type,
        max_results=max_results,
        thread_id=thread_id,
    )

```
 |  
| --- | --- |  
###  create_code_interpreter [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.create_code_interpreter "Permanent link")

```
create_code_interpreter(
    name: ,
    execution_role_arn: ,
    network_mode:  = "PUBLIC",
    description:  = "",
    subnet_ids: Optional[[]] = None,
    security_group_ids: Optional[[]] = None,
    thread_id:  = "default",
) -> 

```

Create a custom code interpreter with specific configuration (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  Name for the interpreter. Must match pattern [a-zA-Z][a-zA-Z0-9_].  |  _required_  |  
|  `execution_role_arn`  |  IAM role ARN with permissions for interpreter operations.  |  _required_  |  
|  `network_mode`  |  Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".  |  `'PUBLIC'`  |  
|  `description`  |  Description of the interpreter. Default is "".  |  
|  `subnet_ids`  |  `Optional[List[str]]`  |  Subnet IDs for VPC mode.  |  `None`  |  
|  `security_group_ids`  |  `Optional[List[str]]`  |  Security group IDs for VPC mode.  |  `None`  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation with interpreter ID and status.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
938
939
940
941
942
943
944
945
946
947
948
949
950
951
952
953
954
955
956
957
958
959
960
961
962
963
964
965
966
967
968
969
970
```
 | 
```
defcreate_code_interpreter(
    self,
    name: str,
    execution_role_arn: str,
    network_mode: str = "PUBLIC",
    description: str = "",
    subnet_ids: Optional[List[str]] = None,
    security_group_ids: Optional[List[str]] = None,
    thread_id: str = "default",
) -> str:
"""
    Create a custom code interpreter with specific configuration (synchronous version).

    Args:
        name (str): Name for the interpreter. Must match pattern [a-zA-Z][a-zA-Z0-9_]{0,47}.
        execution_role_arn (str): IAM role ARN with permissions for interpreter operations.
        network_mode (str): Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".
        description (str): Description of the interpreter. Default is "".
        subnet_ids (Optional[List[str]]): Subnet IDs for VPC mode.
        security_group_ids (Optional[List[str]]): Security group IDs for VPC mode.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Confirmation with interpreter ID and status.

    """
    try:
        code_interpreter = self._get_control_plane_client()
        network_config: Dict[str, Any] = {"networkMode": network_mode}
        if subnet_ids or security_group_ids:
            vpc_config: Dict[str, Any] = {}
            if subnet_ids:
                vpc_config["subnets"] = subnet_ids
            if security_group_ids:
                vpc_config["securityGroups"] = security_group_ids
            network_config["vpcConfig"] = vpc_config
        kwargs: Dict[str, Any] = {
            "name": name,
            "execution_role_arn": execution_role_arn,
            "network_configuration": network_config,
        }
        if description:
            kwargs["description"] = description
        response = code_interpreter.create_code_interpreter(**kwargs)
        interpreter_id = response.get("codeInterpreterId", "unknown")
        status = response.get("status", "unknown")
        return f"Code interpreter created (ID: {interpreter_id}, Status: {status})"
    except Exception as e:
        return f"Error creating code interpreter: {e!s}"

```
 |  
| --- | --- |  
###  acreate_code_interpreter [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.acreate_code_interpreter "Permanent link")

```
acreate_code_interpreter(
    name: ,
    execution_role_arn: ,
    network_mode:  = "PUBLIC",
    description:  = "",
    subnet_ids: Optional[[]] = None,
    security_group_ids: Optional[[]] = None,
    thread_id:  = "default",
) -> 

```

Create a custom code interpreter with specific configuration (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `name`  |  Name for the interpreter. Must match pattern [a-zA-Z][a-zA-Z0-9_].  |  _required_  |  
|  `execution_role_arn`  |  IAM role ARN with permissions for interpreter operations.  |  _required_  |  
|  `network_mode`  |  Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".  |  `'PUBLIC'`  |  
|  `description`  |  Description of the interpreter. Default is "".  |  
|  `subnet_ids`  |  `Optional[List[str]]`  |  Subnet IDs for VPC mode.  |  `None`  |  
|  `security_group_ids`  |  `Optional[List[str]]`  |  Security group IDs for VPC mode.  |  `None`  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation with interpreter ID and status.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
```
 | 
```
async defacreate_code_interpreter(
    self,
    name: str,
    execution_role_arn: str,
    network_mode: str = "PUBLIC",
    description: str = "",
    subnet_ids: Optional[List[str]] = None,
    security_group_ids: Optional[List[str]] = None,
    thread_id: str = "default",
) -> str:
"""
    Create a custom code interpreter with specific configuration (asynchronous version).

    Args:
        name (str): Name for the interpreter. Must match pattern [a-zA-Z][a-zA-Z0-9_]{0,47}.
        execution_role_arn (str): IAM role ARN with permissions for interpreter operations.
        network_mode (str): Network mode: "PUBLIC" or "VPC". Default is "PUBLIC".
        description (str): Description of the interpreter. Default is "".
        subnet_ids (Optional[List[str]]): Subnet IDs for VPC mode.
        security_group_ids (Optional[List[str]]): Security group IDs for VPC mode.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Confirmation with interpreter ID and status.

    """
    return await asyncio.to_thread(
        self.create_code_interpreter,
        name=name,
        execution_role_arn=execution_role_arn,
        network_mode=network_mode,
        description=description,
        subnet_ids=subnet_ids,
        security_group_ids=security_group_ids,
        thread_id=thread_id,
    )

```
 |  
| --- | --- |  
###  delete_code_interpreter [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.delete_code_interpreter "Permanent link")

```
delete_code_interpreter(
    interpreter_id: , thread_id:  = "default"
) -> 

```

Delete a custom code interpreter (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `interpreter_id`  |  The code interpreter identifier to delete.  |  _required_  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation of deletion.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
```
 | 
```
defdelete_code_interpreter(
    self,
    interpreter_id: str,
    thread_id: str = "default",
) -> str:
"""
    Delete a custom code interpreter (synchronous version).

    Args:
        interpreter_id (str): The code interpreter identifier to delete.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Confirmation of deletion.

    """
    try:
        code_interpreter = self._get_control_plane_client()
        response = code_interpreter.delete_code_interpreter(
            interpreter_id=interpreter_id
        )
        status = response.get("status", "unknown")
        return f"Code interpreter '{interpreter_id}' deleted (Status: {status})"
    except Exception as e:
        return f"Error deleting code interpreter: {e!s}"

```
 |  
| --- | --- |  
###  adelete_code_interpreter [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.adelete_code_interpreter "Permanent link")

```
adelete_code_interpreter(
    interpreter_id: , thread_id:  = "default"
) -> 

```

Delete a custom code interpreter (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `interpreter_id`  |  The code interpreter identifier to delete.  |  _required_  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation of deletion.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
```
 | 
```
async defadelete_code_interpreter(
    self,
    interpreter_id: str,
    thread_id: str = "default",
) -> str:
"""
    Delete a custom code interpreter (asynchronous version).

    Args:
        interpreter_id (str): The code interpreter identifier to delete.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Confirmation of deletion.

    """
    return await asyncio.to_thread(
        self.delete_code_interpreter,
        interpreter_id=interpreter_id,
        thread_id=thread_id,
    )

```
 |  
| --- | --- |  
###  get_code_interpreter [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.get_code_interpreter "Permanent link")

```
get_code_interpreter(
    interpreter_id: , thread_id:  = "default"
) -> 

```

Get detailed information about a code interpreter (synchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `interpreter_id`  |  The code interpreter identifier.  |  _required_  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Interpreter details including name, status, and configuration.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
```
 | 
```
defget_code_interpreter(
    self,
    interpreter_id: str,
    thread_id: str = "default",
) -> str:
"""
    Get detailed information about a code interpreter (synchronous version).

    Args:
        interpreter_id (str): The code interpreter identifier.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Interpreter details including name, status, and configuration.

    """
    try:
        code_interpreter = self._get_control_plane_client()
        response = code_interpreter.get_code_interpreter(
            interpreter_id=interpreter_id
        )
        name = response.get("name", "N/A")
        status = response.get("status", "N/A")
        desc = response.get("description", "")
        result = f"Code interpreter '{interpreter_id}':\n"
        result += f"  Name: {name}\n"
        result += f"  Status: {status}\n"
        if desc:
            result += f"  Description: {desc}\n"
        network = response.get("networkConfiguration", {})
        if network:
            result += f"  Network mode: {network.get('networkMode','N/A')}"
        return result
    except Exception as e:
        return f"Error getting code interpreter: {e!s}"

```
 |  
| --- | --- |  
###  aget_code_interpreter [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.aget_code_interpreter "Permanent link")

```
aget_code_interpreter(
    interpreter_id: , thread_id:  = "default"
) -> 

```

Get detailed information about a code interpreter (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `interpreter_id`  |  The code interpreter identifier.  |  _required_  |  
|  `thread_id`  |  Deprecated. Ignored. Kept for backward compatibility.  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Interpreter details including name, status, and configuration.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
```
 | 
```
async defaget_code_interpreter(
    self,
    interpreter_id: str,
    thread_id: str = "default",
) -> str:
"""
    Get detailed information about a code interpreter (asynchronous version).

    Args:
        interpreter_id (str): The code interpreter identifier.
        thread_id (str): Deprecated. Ignored. Kept for backward compatibility.

    Returns:
        str: Interpreter details including name, status, and configuration.

    """
    return await asyncio.to_thread(
        self.get_code_interpreter,
        interpreter_id=interpreter_id,
        thread_id=thread_id,
    )

```
 |  
| --- | --- |  
###  clear_context [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.clear_context "Permanent link")

```
clear_context(thread_id:  = 'default') -> 

```

Clear all variable state in the Python execution context (synchronous version).
This resets the interpreter to a fresh state, removing all previously defined variables, imports, and function definitions.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation that the context was cleared.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
```
 | 
```
defclear_context(
    self,
    thread_id: str = "default",
) -> str:
"""
    Clear all variable state in the Python execution context (synchronous version).

    This resets the interpreter to a fresh state, removing all previously defined
    variables, imports, and function definitions.

    Args:
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: Confirmation that the context was cleared.

    """
    try:
        code_interpreter = self._get_or_create_interpreter(thread_id=thread_id)
        code_interpreter.clear_context()
        return "Python execution context cleared successfully."
    except Exception as e:
        return f"Error clearing context: {e!s}"

```
 |  
| --- | --- |  
###  aclear_context [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.aclear_context "Permanent link")

```
aclear_context(thread_id:  = 'default') -> 

```

Clear all variable state in the Python execution context (asynchronous version).
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  Thread ID for the code interpreter session. Default is "default".  |  `'default'`  |  
Returns:  
| Name  | Type  | Description  |  
| --- | --- | --- |  
| `str`  |  Confirmation that the context was cleared.  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
```
 | 
```
async defaclear_context(
    self,
    thread_id: str = "default",
) -> str:
"""
    Clear all variable state in the Python execution context (asynchronous version).

    Args:
        thread_id (str): Thread ID for the code interpreter session. Default is "default".

    Returns:
        str: Confirmation that the context was cleared.

    """
    return await asyncio.to_thread(self.clear_context, thread_id=thread_id)

```
 |  
| --- | --- |  
###  cleanup [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreCodeInterpreterToolSpec.cleanup "Permanent link")

```
cleanup(thread_id: Optional[] = None) -> None

```

Clean up resources
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `thread_id`  |  `Optional[str]`  |  Optional thread ID to clean up. If None, cleans up all sessions.  |  `None`  |  
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/code_interpreter/base.py`  
| 
```
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
```
 | 
```
async defcleanup(self, thread_id: Optional[str] = None) -> None:
"""
    Clean up resources

    Args:
        thread_id: Optional thread ID to clean up. If None, cleans up all sessions.

    """
    if thread_id:
        # Clean up a specific thread's session
        if thread_id in self._code_interpreters:
            try:
                self._code_interpreters[thread_id].stop()
                del self._code_interpreters[thread_id]
                logger.info(
                    f"Code interpreter session for thread {thread_id} cleaned up"
                )
            except Exception as e:
                logger.warning(
                    f"Error stopping code interpreter for thread {thread_id}: {e}"
                )
    else:
        # Clean up all sessions
        thread_ids = list(self._code_interpreters.keys())
        for tid in thread_ids:
            try:
                self._code_interpreters[tid].stop()
            except Exception as e:
                logger.warning(
                    f"Error stopping code interpreter for thread {tid}: {e}"
                )

        self._code_interpreters = {}
        logger.info("All code interpreter sessions cleaned up")

```
 |  
| --- | --- |  
##  AgentCoreRuntime [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreRuntime "Permanent link")
Serves a LlamaIndex agent via BedrockAgentCoreApp (POST /invocations, GET /ping).
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/runtime/base.py`  
| 
```
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
```
 | 
```
classAgentCoreRuntime:
"""Serves a LlamaIndex agent via BedrockAgentCoreApp (POST /invocations, GET /ping)."""

    def__init__(
        self,
        agent: Any,
        stream: bool = True,
        port: int = 8080,
        host: Optional[str] = None,
        debug: bool = False,
        memory: Optional[Any] = None,
        lifespan: Optional[Lifespan] = None,
        middleware: Optional[Sequence[Middleware]] = None,
    ):
        self._agent = agent
        self._stream = stream
        self._port = port
        self._host = host
        self._memory = memory
        self._app = BedrockAgentCoreApp(
            debug=debug, lifespan=lifespan, middleware=middleware
        )

        # Register entrypoint using closure wrappers (not bound methods).
        # entrypoint() sets func.run attr which fails on bound methods.
        # Closures also preserve isasyncgenfunction() detection for streaming.
        runtime = self
        if stream:

            async defstreaming_entrypoint(
                payload: dict, context: RequestContext
            ) -> AsyncGenerator[dict, None]:
                # Validate eagerly (before the first yield) so that
                # HTTPException propagates before streaming begins.
                prompt = runtime._extract_prompt(payload)
                memory = runtime._get_memory(context)
                async for chunk in runtime._stream_events(prompt, memory):
                    yield chunk

            self._app.entrypoint(streaming_entrypoint)
        else:

            async defnon_streaming_entrypoint(
                payload: dict, context: RequestContext
            ) -> dict:
                return await runtime._non_streaming_handler(payload, context)

            self._app.entrypoint(non_streaming_entrypoint)

    @classmethod
    defserve(cls, agent: Any, **kwargs: Any) -> None:
"""Create runtime and start server in one call."""
        runtime = cls(agent=agent, **kwargs)
        runtime.run()

    defrun(self, **kwargs: Any) -> None:
"""Start uvicorn server."""
        self._app.run(port=self._port, host=self._host, **kwargs)

    @property
    defapp(self) -> BedrockAgentCoreApp:
"""Expose for ASGI mounting or testing."""
        return self._app

    @staticmethod
    def_extract_prompt(payload: dict) -> str:
"""Normalize payload to user message string."""
        prompt = payload.get("prompt") or payload.get("message") or payload.get("input")
        if isinstance(prompt, dict):
            prompt = prompt.get("prompt")
        if isinstance(prompt, str):
            prompt = prompt.strip()
        if not prompt or not isinstance(prompt, (str, int, float)):
            raise HTTPException(
                status_code=400,
                detail="Request must include 'prompt', 'message', or 'input' field"
                " with a string value",
            )
        return str(prompt)

    def_get_memory(self, context: Optional[RequestContext] = None) -> Optional[Any]:
"""Return per-request memory copy with session_id from AgentCore context."""
        if self._memory is None:
            return None
        if context and context.session_id and hasattr(self._memory, "_context"):
            if hasattr(self._memory._context, "session_id"):
                memory = copy.copy(self._memory)
                memory._context = copy.copy(self._memory._context)
                memory._context.session_id = context.session_id
                return memory
        return self._memory

    async def_non_streaming_handler(
        self, payload: dict, context: RequestContext
    ) -> dict:
"""Handle non-streaming invocation. Returns JSON response."""
        prompt = self._extract_prompt(payload)
        memory = self._get_memory(context)
        handler = self._agent.run(user_msg=prompt, memory=memory)
        result = await handler
        return {"response": str(result)}

    async def_stream_events(
        self, prompt: str, memory: Optional[Any]
    ) -> AsyncGenerator[dict, None]:
"""
        Yield SSE event dicts for a validated prompt.

        Callers should validate the prompt (via _extract_prompt) before
        calling this method so that validation errors are raised eagerly.
        """
        handler = self._agent.run(user_msg=prompt, memory=memory)

        try:
            async for event in handler.stream_events():
                if isinstance(event, AgentStream):
                    ev: Dict[str, Any] = {
                        "event": "agent_stream",
                        "delta": event.delta,
                        "response": event.response,
                    }
                    if event.thinking_delta:
                        ev["thinking_delta"] = event.thinking_delta
                    yield ev
                elif isinstance(event, ToolCall):
                    yield {
                        "event": "tool_call",
                        "tool_name": event.tool_name,
                        "tool_kwargs": event.tool_kwargs,
                    }
                elif isinstance(event, ToolCallResult):
                    yield {
                        "event": "tool_result",
                        "tool_name": event.tool_name,
                        "tool_output": str(event.tool_output),
                    }
                elif isinstance(event, AgentOutput):
                    yield {"event": "done", "response": str(event.response)}
                else:
                    logger.debug(
                        "Ignoring unknown event type: %s", type(event).__name__
                    )
        except Exception as e:
            logger.exception("Error during streaming")
            yield {"event": "error", "message": str(e)}
            return

        # Await handler to ensure background tasks complete (memory flush, etc.)
        try:
            await handler
        except Exception:
            logger.exception("Error awaiting handler completion")

```
 |  
| --- | --- |  
###  app `property` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreRuntime.app "Permanent link")

```
app: BedrockAgentCoreApp

```

Expose for ASGI mounting or testing.
###  serve `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreRuntime.serve "Permanent link")

```
serve(agent: , **kwargs: ) -> None

```

Create runtime and start server in one call.
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/runtime/base.py`  
| 
```
70
71
72
73
74
```
 | 
```
@classmethod
defserve(cls, agent: Any, **kwargs: Any) -> None:
"""Create runtime and start server in one call."""
    runtime = cls(agent=agent, **kwargs)
    runtime.run()

```
 |  
| --- | --- |  
###  run [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/aws_bedrock_agentcore/#llama_index.tools.aws_bedrock_agentcore.AgentCoreRuntime.run "Permanent link")

```
run(**kwargs: ) -> None

```

Start uvicorn server.
Source code in `llama-index-integrations/tools/llama-index-tools-aws-bedrock-agentcore/llama_index/tools/aws_bedrock_agentcore/runtime/base.py`  
| 
```
76
77
78
```
 | 
```
defrun(self, **kwargs: Any) -> None:
"""Start uvicorn server."""
    self._app.run(port=self._port, host=self._host, **kwargs)

```
 |  
| --- | --- |  
options: members: - AgentCoreBrowserToolSpec - AgentCoreCodeInterpreterToolSpec - AgentCoreRuntime
