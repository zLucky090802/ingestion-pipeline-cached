# Bedrock agentcore
##  AgentCoreMemory [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/bedrock_agentcore/#llama_index.memory.bedrock_agentcore.AgentCoreMemory "Permanent link")
Bases: `BaseAgentCoreMemory`
Source code in `llama-index-integrations/memory/llama-index-memory-bedrock-agentcore/llama_index/memory/bedrock_agentcore/base.py`  
| 
```
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
```
 | 
```
classAgentCoreMemory(BaseAgentCoreMemory):
    search_msg_limit: int = Field(
        default=5,
        description="Limit of chat history messages to use for context in search API",
    )
    insert_method: InsertMethod = Field(
        default=InsertMethod.SYSTEM,
        description="Whether to inject memory blocks into a system message or into the latest user message.",
    )

    _context: AgentCoreMemoryContext = PrivateAttr()

    def__init__(
        self,
        context: AgentCoreMemoryContext,
        # TODO: add support for InsertMethod.USER. for now default to InsertMethod.SYSTEM
        # insert_method: InsertMethod = InsertMethod.SYSTEM,
        profile_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        region_name: Optional[str] = None,
        api_version: Optional[str] = None,
        use_ssl: bool = True,
        verify: Optional[Union[bool, str]] = None,
        endpoint_url: Optional[str] = None,
        botocore_session: Optional[Any] = None,
        client: Optional[Any] = None,
        timeout: Optional[float] = 60.0,
        max_retries: Optional[int] = 10,
        botocore_config: Optional[Any] = None,
    ) -> None:
        boto3_user_agent_identifier = "x-client-framework:llama_index"

        session_kwargs = {
            "profile_name": profile_name,
            "region_name": region_name,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token,
            "botocore_session": botocore_session,
        }
        self._config = (
            Config(
                retries={"max_attempts": max_retries, "mode": "standard"},
                connect_timeout=timeout,
                read_timeout=timeout,
                user_agent_extra=boto3_user_agent_identifier,
            )
            if botocore_config is None
            else botocore_config
        )

        self._boto_client_kwargs = {
            "api_version": api_version,
            "use_ssl": use_ssl,
            "verify": verify,
            "endpoint_url": endpoint_url,
        }

        try:
            self._config = (
                Config(
                    retries={"max_attempts": max_retries, "mode": "standard"},
                    connect_timeout=timeout,
                    read_timeout=timeout,
                    user_agent_extra=boto3_user_agent_identifier,
                )
                if botocore_config is None
                else botocore_config
            )
            session = boto3.Session(**session_kwargs)
        except ImportError:
            raise ImportError(
                "boto3  package not found, install with pip install boto3"
            )
        session = boto3.Session(**session_kwargs)

        if client is not None:
            self._client = client
        else:
            self._client = session.client(
                "bedrock-agentcore",
                config=self._config,
                **self._boto_client_kwargs,
            )
        self._client._serializer._serializer._serialize_type_timestamp = (
            self._serialize_timestamp_with_microseconds
        )
        super().__init__(self._client)

        self._context = context

    @model_serializer
    defserialize_memory(self) -> Dict[str, Any]:
        # leaving out the two keys since they are causing serialization/deserialization problems
        return {
            "search_msg_limit": self.search_msg_limit,
        }

    @classmethod
    defclass_name(cls) -> str:
"""Class name."""
        return "AgentCoreMemory"

    @classmethod
    deffrom_defaults(cls, **kwargs: Any) -> "AgentCoreMemory":
        raise NotImplementedError("Use either from_client or from_config")

    def_serialize_timestamp_with_microseconds(self, serialized, value, shape, name):
        original_serialize_timestamp = (
            self._client._serializer._serializer._serialize_type_timestamp
        )
        if isinstance(value, datetime):
            serialized[name] = value.timestamp()  # Float with microseconds
        else:
            original_serialize_timestamp(serialized, value, shape, name)

    def_add_msgs_to_client_memory(self, messages: List[ChatMessage]) -> None:
"""Add new user and assistant messages to client memory."""
        self.create_event(
            messages=messages,
            memory_id=self._context.memory_id,
            actor_id=self._context.actor_id,
            session_id=self._context.session_id,
        )

    async defaget(self, input: Optional[str] = None) -> List[ChatMessage]:
        # Get list of events to represent as the chat history. Use this as the query for the memory records. If an input is provided, then also append it to the list of events
        messages = self.list_events(
            memory_id=self._context.memory_id,
            session_id=self._context.session_id,
            actor_id=self._context.actor_id,
        )
        input = convert_messages_to_string(messages, input)

        search_criteria = {"searchQuery": input[:10000]}
        if self._context.memory_strategy_id is not None:
            search_criteria["memoryStrategyId"] = self._context.memory_strategy_id

        memory_records = self.retrieve_memories(
            memory_id=self._context.memory_id,
            namespace=self._context.namespace,
            search_criteria=search_criteria,
        )

        if self.insert_method == InsertMethod.SYSTEM:
            system_message = convert_memory_to_system_message(memory_records)
            # If system message is present
            if len(messages)  0 and messages[0].role == MessageRole.SYSTEM:
                assert messages[0].content is not None
                system_message = convert_memory_to_system_message(
                    response=memory_records,
                    existing_system_message=messages[0],
                )
            messages.insert(0, system_message)
        elif self.insert_method == InsertMethod.USER:
            # Find the latest user message
            session_idx = next(
                (
                    i
                    for i, msg in enumerate(reversed(messages))
                    if msg.role == MessageRole.USER
                ),
                None,
            )

            memory_content = convert_memory_to_user_message(memory_records)

            if session_idx is not None:
                # Get actual index (since we enumerated in reverse)
                actual_idx = len(messages) - 1 - session_idx
                # Update existing user message since many LLMs have issues with consecutive user msgs
                final_user_content = (
                    memory_content.content + messages[actual_idx].content
                )
                messages[actual_idx] = ChatMessage(
                    content=final_user_content, role=MessageRole.USER
                )
                messages[actual_idx].blocks = [
                    *memory_content.blocks,
                    *messages[actual_idx].blocks,
                ]
            else:
                messages.append(
                    ChatMessage(content=memory_content, role=MessageRole.USER)
                )

        return messages

    async defaget_all(self) -> List[ChatMessage]:
        return self.list_events(
            memory_id=self._context.memory_id,
            session_id=self._context.session_id,
            actor_id=self._context.actor_id,
        )

    async defaput(self, message: ChatMessage) -> None:
"""Add a message to the chat store and process waterfall logic if needed."""
        # Add the message to the chat store
        self._add_msgs_to_client_memory([message])

    async defaput_messages(self, messages: List[ChatMessage]) -> None:
"""Add a list of messages to the chat store and process waterfall logic if needed."""
        # Add the messages to the chat store
        self._add_msgs_to_client_memory(messages)

    async defaset(self, messages: List[ChatMessage]) -> None:
        initial_chat_len = len(self.get_all())
        # Insert only new chat messages
        self._add_msgs_to_client_memory(messages[initial_chat_len:])

    # ---- Sync method wrappers ----
    defget(self, input: Optional[str] = None) -> List[ChatMessage]:
"""Get chat history."""
        return asyncio_run(self.aget(input=input))

    defget_all(self) -> List[ChatMessage]:
"""Returns all chat history."""
        return asyncio_run(self.aget_all())

    defput(self, message: ChatMessage) -> None:
"""Add message to chat history and client memory."""
        return asyncio_run(self.aput(message))

    defput_messages(self, messages: List[ChatMessage]) -> None:
        return asyncio_run(self.aput_messages(messages))

    defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history and add new messages to client memory."""
        return asyncio_run(self.aset(messages))

    defreset(self) -> None:
"""Only reset chat history."""
        # Our guidance has been to not delete memory resources in AgentCore on behalf of the customer. If this changes in the future, then we can implement this method.

    defget_context(self) -> AgentCoreMemoryContext:
        return self._context.get_context()

```
 |  
| --- | --- |  
###  class_name `classmethod` [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/bedrock_agentcore/#llama_index.memory.bedrock_agentcore.AgentCoreMemory.class_name "Permanent link")

```
class_name() -> 

```

Class name.
Source code in `llama-index-integrations/memory/llama-index-memory-bedrock-agentcore/llama_index/memory/bedrock_agentcore/base.py`  
| 
```
596
597
598
599
```
 | 
```
@classmethod
defclass_name(cls) -> str:
"""Class name."""
    return "AgentCoreMemory"

```
 |  
| --- | --- |  
###  aput [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/bedrock_agentcore/#llama_index.memory.bedrock_agentcore.AgentCoreMemory.aput "Permanent link")

```
aput(message: ) -> None

```

Add a message to the chat store and process waterfall logic if needed.
Source code in `llama-index-integrations/memory/llama-index-memory-bedrock-agentcore/llama_index/memory/bedrock_agentcore/base.py`  
| 
```
693
694
695
696
```
 | 
```
async defaput(self, message: ChatMessage) -> None:
"""Add a message to the chat store and process waterfall logic if needed."""
    # Add the message to the chat store
    self._add_msgs_to_client_memory([message])

```
 |  
| --- | --- |  
###  aput_messages [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/bedrock_agentcore/#llama_index.memory.bedrock_agentcore.AgentCoreMemory.aput_messages "Permanent link")

```
aput_messages(messages: []) -> None

```

Add a list of messages to the chat store and process waterfall logic if needed.
Source code in `llama-index-integrations/memory/llama-index-memory-bedrock-agentcore/llama_index/memory/bedrock_agentcore/base.py`  
| 
```
698
699
700
701
```
 | 
```
async defaput_messages(self, messages: List[ChatMessage]) -> None:
"""Add a list of messages to the chat store and process waterfall logic if needed."""
    # Add the messages to the chat store
    self._add_msgs_to_client_memory(messages)

```
 |  
| --- | --- |  
###  get [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/bedrock_agentcore/#llama_index.memory.bedrock_agentcore.AgentCoreMemory.get "Permanent link")

```
get(input: Optional[] = None) -> []

```

Get chat history.
Source code in `llama-index-integrations/memory/llama-index-memory-bedrock-agentcore/llama_index/memory/bedrock_agentcore/base.py`  
| 
```
709
710
711
```
 | 
```
defget(self, input: Optional[str] = None) -> List[ChatMessage]:
"""Get chat history."""
    return asyncio_run(self.aget(input=input))

```
 |  
| --- | --- |  
###  get_all [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/bedrock_agentcore/#llama_index.memory.bedrock_agentcore.AgentCoreMemory.get_all "Permanent link")

```
get_all() -> []

```

Returns all chat history.
Source code in `llama-index-integrations/memory/llama-index-memory-bedrock-agentcore/llama_index/memory/bedrock_agentcore/base.py`  
| 
```
713
714
715
```
 | 
```
defget_all(self) -> List[ChatMessage]:
"""Returns all chat history."""
    return asyncio_run(self.aget_all())

```
 |  
| --- | --- |  
###  put [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/bedrock_agentcore/#llama_index.memory.bedrock_agentcore.AgentCoreMemory.put "Permanent link")

```
put(message: ) -> None

```

Add message to chat history and client memory.
Source code in `llama-index-integrations/memory/llama-index-memory-bedrock-agentcore/llama_index/memory/bedrock_agentcore/base.py`  
| 
```
717
718
719
```
 | 
```
defput(self, message: ChatMessage) -> None:
"""Add message to chat history and client memory."""
    return asyncio_run(self.aput(message))

```
 |  
| --- | --- |  
###  set [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/bedrock_agentcore/#llama_index.memory.bedrock_agentcore.AgentCoreMemory.set "Permanent link")

```
set(messages: []) -> None

```

Set chat history and add new messages to client memory.
Source code in `llama-index-integrations/memory/llama-index-memory-bedrock-agentcore/llama_index/memory/bedrock_agentcore/base.py`  
| 
```
724
725
726
```
 | 
```
defset(self, messages: List[ChatMessage]) -> None:
"""Set chat history and add new messages to client memory."""
    return asyncio_run(self.aset(messages))

```
 |  
| --- | --- |  
###  reset [#](https://developers.llamaindex.ai/python/framework-api-reference/memory/bedrock_agentcore/#llama_index.memory.bedrock_agentcore.AgentCoreMemory.reset "Permanent link")

```
reset() -> None

```

Only reset chat history.
Source code in `llama-index-integrations/memory/llama-index-memory-bedrock-agentcore/llama_index/memory/bedrock_agentcore/base.py`  
| 
```
728
729
```
 | 
```
defreset(self) -> None:
"""Only reset chat history."""

```
 |  
| --- | --- |  
options: members: - AgentCoreMemory
