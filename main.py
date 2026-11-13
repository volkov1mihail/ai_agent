import os, argparse, json
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from prompts import system_prompt
from config import AGENT_TEMPERATURE
from call_function import available_functions, call_function

def generate_content(client: OpenAI, messages: dict[str, str]) -> ChatCompletion:
    return client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=AGENT_TEMPERATURE,
        tools=available_functions,
    )

def get_consumed_tokens(response: ChatCompletion) -> tuple[int, int]:
    if not response.usage:
        raise Exception("no usage property in response")
    return response.usage.prompt_tokens, response.usage.completion_tokens

def consumed_tokens_string(response: ChatCompletion) -> str:
    prompt_tokens, completion_tokens = get_consumed_tokens(response)
    return f"Prompt tokens: {prompt_tokens}" + "\n" + f"Response tokens: {completion_tokens}" 

def generate_output(response: ChatCompletion, args) -> str:
    result = ""
    if args.verbose:
        result += f"User prompt: {args.user_prompt}" + "\n"
        result += consumed_tokens_string(response) + "\n"
    result += "Response:\n"

    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            return_message = call_function(tool_call, args.verbose)
            if not return_message["content"]:
                raise Exception("Error: Tool call returned with empty content")
            result += return_message["content"]
    else:
        result += message.content
    return result


def main():
    global system_prompt
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("couldn't load the API key")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = generate_content(client, messages)
    response_text = generate_output(response, args)
    print(response_text)


if __name__ == "__main__":
    main()
