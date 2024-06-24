from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a developer with great sense of humor.",
        },
        {
            "role": "user",
            "content": "Make a joke of the python language",
        },
    ],
)

print(completion.choices[0].message)
