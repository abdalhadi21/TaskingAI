from typing import List, Optional
from pydantic import BaseModel, Field, Literal


class OpenaiChoiceDeltaFunctionCall(BaseModel):
    arguments: Optional[str] = Field(
        None,
        description="The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.",
    )

    name: Optional[str] = Field(None, description="The name of the function to call.")


class OpenaiChoiceDeltaToolCallFunction(BaseModel):
    arguments: Optional[str] = Field(
        None,
        description="The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.",
    )

    name: Optional[str] = Field(None, description="The name of the function to call.")


class OpenaiChoiceDeltaToolCall(BaseModel):
    index: int = Field(...)

    id: Optional[str] = Field(None, description="The ID of the tool call.")

    function: Optional[OpenaiChoiceDeltaToolCallFunction] = Field(default=None)

    type: Optional[Literal["function"]] = Field(
        None, description="The type of the tool. Currently, only function is supported."
    )


class OpenaiChoiceDelta(BaseModel):
    content: Optional[str] = Field(None, description="The contents of the chunk message.")

    function_call: Optional[OpenaiChoiceDeltaFunctionCall] = Field(
        None,
        description="Deprecated and replaced by tool_calls. The name and arguments of a function that should be called, as generated by the model.",
    )

    role: Optional[Literal["system", "user", "assistant", "tool"]] = Field(
        None, description="The role of the author of this message."
    )

    tool_calls: Optional[List[OpenaiChoiceDeltaToolCall]] = Field(default=None)


class OpenaiChoice(BaseModel):
    delta: OpenaiChoiceDelta = Field(..., description="A chat completion delta generated by streamed model responses.")

    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = Field(
        None,
        description="The reason the model stopped generating tokens. This will be stop if the model hit a natural stop point or a provided stop sequence, length if the maximum number of tokens specified in the request was reached, content_filter if content was omitted due to a flag from our content filters, tool_calls if the model called a tool, or function_call if the model called a function.",
    )

    index: int = Field(..., description="The index of the choice in the list of choices.")

    logprobs: None


class OpenaiChatCompletionChunk(BaseModel):
    id: str = Field(..., description="A unique identifier for the chat completion. Each chunk has the same ID.")

    choices: List[OpenaiChoice] = Field(
        ...,
        description="A list of chat completion choices. Can be more than one if n is greater than 1.",
    )

    created: int = Field(
        ...,
        description="The Unix timestamp (in seconds) of when the chat completion was created. Each chunk has the same timestamp.",
    )

    model: str = Field(..., description="The model to generate the completion.")

    object: Literal["chat.completion.chunk"] = Field(
        "chat.completion.chunk", description="The object type, which is always chat.completion.chunk."
    )

    system_fingerprint: Optional[str] = Field(
        None,
        description="This fingerprint represents the backend configuration that the model runs with. Can be used in conjunction with the seed request parameter to understand when backend changes have been made that might impact determinism.",
    )
