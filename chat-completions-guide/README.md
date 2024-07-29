# Chat Completions
* https://platform.openai.com/docs/guides/chat-completions

# Overview

The Chat Completions API supports text and image inputs, and can output text content (including code and JSON).

It accepts inputs via the `messages` parameter, which is an array of message objects.

# Message roles

Each message object has a role (either `system`, `user`, or `assistant`) and content.

* The `system` message is optional and can be used to set the behavior of the assistant. By default, the system message is "You are a helpful assistant". You can define instructions in the user message, but the instructions set in the system message are more effective. You can only set one system message per conversation.
* The `user` messages provide requests or comments for the assistant to respond to
* Assistant messages store previous assistant responses, but can also be written by you to give examples of desired behavior ([few-shot examples](https://platform.openai.com/docs/guides/prompt-engineering/tactic-provide-examples))

# Getting started

Chat models take a list of messages as input and return a model-generated message as output. Although the chat format is designed to make multi-turn conversations easy, it’s just as useful for single-turn tasks without any conversation.

```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)
```

Including conversation history is important when user instructions refer to prior messages. In the example above, the user's final question of "Where was it played?" only makes sense in the context of the prior messages about the World Series of 2020. Because the models have no memory of past requests, all relevant information must be supplied as part of the conversation history in each request. If a conversation cannot fit within the model’s token limit, it will need to be shortened in some way.


# Chat Completions response format
```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
        "role": "assistant"
      },
      "logprobs": null
    }
  ],
  "created": 1677664795,
  "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
  "model": "gpt-4o-mini",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 17,
    "prompt_tokens": 57,
    "total_tokens": 74
  }
}
```

Every response will include a `finish_reason`. The possible values for `finish_reason` are:

* `stop`: API returned complete message, or a message terminated by one of the stop sequences provided via the stop parameter
* `length`: Incomplete model output due to max_tokens parameter or token limit
* `function_call`: The model decided to call a function
* `content_filter`: Omitted content due to a flag from our content filters
* `null`: API response still in progress or incomplete


The assistant's reply can be extracted with:
```python
message = completion.choices[0].message.content
```

