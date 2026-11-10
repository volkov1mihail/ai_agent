import os, argparse
from dotenv import load_dotenv
from openai import OpenAI

def generate_content(client: OpenAI, messages: dict[str, str]) -> object:
    return client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

def get_consumed_tokens(response: object) -> tuple[int, int]:
    if not response.usage:
        raise Exception("no usage property in response")
    return response.usage.prompt_tokens, response.usage.completion_tokens

def consumed_tokens_string(response: object) -> str:
    prompt_tokens, completion_tokens = get_consumed_tokens(response)
    return f"Prompt tokens: {prompt_tokens}" + "\n" + f"Response tokens: {completion_tokens}" 

def generate_output(response: object, args) -> str:
    result = ""
    if args.verbose:
        result += f"User prompt: {args.user_prompt}" + "\n"
        result += consumed_tokens_string(response) + "\n"
    
    return result + "Response:\n" + response.choices[0].message.content


def main():
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
        {"role": "user", "content": args.user_prompt},
    ]

    response = generate_content(client, messages)
    response_text = generate_output(response, args)
    print(response_text)


if __name__ == "__main__":
    main()
