import openai

def query_openai_api(question):
    client = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": question,
            },
        ],
    )
    return client.choices[0].message.content