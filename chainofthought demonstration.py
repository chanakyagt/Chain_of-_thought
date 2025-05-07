from openai import OpenAI
from dotenv import load_dotenv
import json
import os
load_dotenv()
client=OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)
systemPrompt='''
you are an helpful agent who only solves maths queries and you follow four step approach that is think,analyze,execute,return
Carefully analyze the query and breakdown the tasks
Remember that you only return one step at a time and generate the next step once you get the previous step as input 
Output should be strictly in JSON format

Output Format:
{"step":"string","content":"string"}

Example:
Query:What is 5*3+10
Output:{step:"think",content:"So the user has given me a mathematical instruction containing + and *}
Output:{step:"analyze",content:"Since the mathematic expression contains * and + symbol * (Multiply will take preference and hence resolved first followed by the + operator)}
Output:{step:"execute",content:"So since 5*3=15 and 15+10=25"}
Output:{step:"return",content:"the answer for the expression is 25"}
'''
message_array=[
    {"role":"system","content":systemPrompt}
]
userQuery=input(">")
message_array.append({"role":"user","content":userQuery})

while True:

    response=client.chat.completions.create(
        model='gpt-4.1-mini',
        response_format={"type":"json_object"},
        messages=message_array
    )
    print(response.choices[0].message.content)
    message_array.append({"role":"assistant","content":response.choices[0].message.content})
    if(json.loads(response.choices[0].message.content).get("step")=="return"):
        break