[Skip to content](https://developers.llamaindex.ai/python/llamaagents/workflows/retry_steps/#_top)
LlamaAgents
Agent Workflows
[Retry steps execution](https://developers.llamaindex.ai/python/llamaagents/workflows/retry_steps/)
Copy Markdown
Open in **Claude**
Open in **ChatGPT**
Open in **Cursor**
**Copy Markdown**
**View as Markdown**
# Retry steps execution
A step that fails its execution might result in the failure of the entire workflow, but oftentimes errors are expected and the execution can be safely retried. Think of a HTTP request that times out because of a transient congestion of the network, or an external API call that hits a rate limiter.
For all those situations where you want the step to try again, you can use a **retry policy**. A retry policy instructs the workflow to execute a step multiple times, controlling how long to wait before each new attempt, which errors are retryable, and when to give up.
The retry module is built from three families of composable building blocks:
  * **Retry conditions** decide whether an exception is retryable.
  * **Wait strategies** decide how long to sleep before the next attempt.
  * **Stop conditions** decide when the workflow should give up.


Compose them into a policy with `retry_policy(retry=..., wait=..., stop=...)` and pass the result to the `@step` decorator. Retry conditions support `|` and , wait strategies support `+`, and stop conditions support `|` and .
## Basic usage
[Section titled “Basic usage”](https://developers.llamaindex.ai/python/llamaagents/workflows/retry_steps/#basic-usage)

```


from workflows import Workflow, Context, step




from workflows.events import StartEvent, StopEvent




from workflows.retry_policy import (




retry_policy,




stop_after_attempt,




wait_fixed,







classMyWorkflow(Workflow):




@step(




retry_policy=retry_policy(




wait=wait_fixed(5),




stop=stop_after_attempt(10),






asyncdefflaky_step(self, ctx: Context, ev: StartEvent) -> StopEvent:




result = flaky_call()  # this might raise




return StopEvent(result=result)


```

With no arguments, `retry_policy()` retries all exceptions up to 3 attempts with a 5-second fixed delay between each. Pass `retry=`, `wait=`, or `stop=` to customize any component.
## Filtering exceptions
[Section titled “Filtering exceptions”](https://developers.llamaindex.ai/python/llamaagents/workflows/retry_steps/#filtering-exceptions)
Use retry conditions to control which exceptions are retried:

```


from workflows import Workflow, step




from workflows.events import StartEvent, StopEvent




from workflows.retry_policy import (




retry_policy,




retry_if_exception_message,




retry_if_exception_type,




stop_after_attempt,




stop_before_delay,




wait_fixed,




wait_random,







classMyWorkflow(Workflow):




@step(




retry_policy=retry_policy(




retry=retry_if_exception_type((TimeoutError, ConnectionError))




| retry_if_exception_message(match="rate limit|temporarily unavailable"),




wait=wait_fixed(1) + wait_random(0, 1),




stop=stop_after_attempt(5) | stop_before_delay(30),






asyncdefcall_provider(self, ev: StartEvent) -> StopEvent:




result =await flaky_call()




return StopEvent(result=result)


```

The named combinators are equivalent if you prefer a more explicit style:

```


from workflows.retry_policy import (




retry_policy,




retry_any,




retry_if_exception_message,




retry_if_exception_type,




stop_any,




stop_after_attempt,




stop_before_delay,




wait_combine,




wait_fixed,




wait_random,






policy = retry_policy(




retry=retry_any(




retry_if_exception_type((TimeoutError, ConnectionError)),




retry_if_exception_message(match="rate limit|temporarily unavailable"),





wait=wait_combine(wait_fixed(1), wait_random(0, 1)),




stop=stop_any(stop_after_attempt(5), stop_before_delay(30)),



```

## Exponential backoff
[Section titled “Exponential backoff”](https://developers.llamaindex.ai/python/llamaagents/workflows/retry_steps/#exponential-backoff)
For steps that call LLM providers or rate-limited APIs, exponential backoff avoids thundering-herd effects:

```


from workflows import Workflow, Context, step




from workflows.events import StartEvent, StopEvent




from workflows.retry_policy import (




retry_policy,




stop_after_attempt,




wait_exponential_jitter,







classMyWorkflow(Workflow):




@step(




retry_policy=retry_policy(




wait=wait_exponential_jitter(initial=1, exp_base=2, max=30, jitter=1),




stop=stop_after_attempt(5),






asyncdefcall_llm(self, ctx: Context, ev: StartEvent) -> StopEvent:




result =await llm_call()  # this might raise on rate-limit




return StopEvent(result=result)


```

## Full API reference
[Section titled “Full API reference”](https://developers.llamaindex.ai/python/llamaagents/workflows/retry_steps/#full-api-reference)
The module exposes many more retry conditions, wait strategies, and stop conditions than shown here. See the [API reference](https://developers.llamaindex.ai/python/workflows-api-reference/retry_policy/) for the complete list of building blocks and their parameters.
## Custom retry policies
[Section titled “Custom retry policies”](https://developers.llamaindex.ai/python/llamaagents/workflows/retry_steps/#custom-retry-policies)
If the composable API doesn’t cover your use case, you can write a custom policy. The only requirement is a class with a `next` method matching the `RetryPolicy` protocol:

```


defnext(




self, elapsed_time: float, attempts: int, error: Exception




) -> Optional[float]:



```

Return the number of seconds to wait before retrying, or `None` to stop.
For example, this policy only retries on Fridays:

```


from datetime import datetime




from typing import Optional






classRetryOnFridayPolicy:




defnext(




self, elapsed_time: float, attempts: int, error: Exception




) -> Optional[float]:




if datetime.today().strftime("%A") =="Friday":




return5# retry in 5 seconds




returnNone# don't retry


```

## Deprecated convenience constructors
[Section titled “Deprecated convenience constructors”](https://developers.llamaindex.ai/python/llamaagents/workflows/retry_steps/#deprecated-convenience-constructors)

```


from workflows.retry_policy import ConstantDelayRetryPolicy




# Deprecated — equivalent to:


#   retry_policy(wait=wait_fixed(5), stop=stop_after_attempt(10))



policy = ConstantDelayRetryPolicy(delay=5, maximum_attempts=10)


```


```


from workflows.retry_policy import ExponentialBackoffRetryPolicy




# Deprecated — equivalent to:


#   retry_policy(wait=wait_random_exponential(multiplier=1, exp_base=2, max=30),


#                stop=stop_after_attempt(5))



policy = ExponentialBackoffRetryPolicy(




initial_delay=1, multiplier=2, max_delay=30, maximum_attempts=5,



```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


