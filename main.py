import os, argparse
from dotenv import load_dotenv
from openai import OpenAI

def get_consumed_tokens(response: object) -> tuple[int, int]:
    if not response.usage:
        raise Exception("no usage property in response")
    return response.usage.prompt_tokens, response.usage.completion_tokens

def print_consumed_tokens(response: object) -> None:
    prompt_tokens, completion_tokens = get_consumed_tokens(response)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")
    return


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
    args = parser.parse_args()

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": args.user_prompt
            }
        ],
    )
    print_consumed_tokens(response)
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
