from typing import List
from case_study.models import LegalEntities
from openai import OpenAI


def call_llm(instructions: str, user_input: List[str], model="gpt-4o"):
    # openai.api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI()

    rsp = client.responses.parse(
        instructions=instructions,
        input=user_input,
        model=model,
        text_format=LegalEntities,
    )

    for output in rsp.output:
        if output.type != "message":
            raise Exception("Unexpected non message")

        for item in output.content:
            if item.type != "output_text":
                raise Exception("unexpected output type")

            if not item.parsed:
                raise Exception("Could not parse response")

            print(item.parsed)

            print("answer: ", item.parsed.final_answer)

    # or

    message = rsp.output[0]
    assert message.type == "message"

    text = message.content[0]
    assert text.type == "output_text"

    if not text.parsed:
        raise Exception("Could not parse response")

    print(text.parsed)

    print("answer: ", text.parsed.final_answer)
