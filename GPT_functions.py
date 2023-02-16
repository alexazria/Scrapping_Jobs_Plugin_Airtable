import os
import openai
openai.api_key = ""
# openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_format(texte):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt="Put the following paragraph in a nice and readable format: {}".format(texte),
      temperature=0,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.0,
    #   stop=["\n"]
    )

    generated_text = response["choices"][0]["text"]
    return generated_text