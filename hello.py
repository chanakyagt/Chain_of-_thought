import streamlit as st
import os
import json
from openai import OpenAI,BaseModel
from dotenv import load_dotenv
load_dotenv()
                           
client=OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)
# userQuery=input(">")
system_Prompt='''
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
response=client.chat.completions.create(
     model="gpt-4.1-mini",
     response_format={"type":"json_object"},
     messages=[
    {"role": "system", "content": system_Prompt},
    {"role": "user", "content": "what is 6/2-1+35/7"},
    {"role":"assistant","content":json.dumps({"step":"think","content":"The user wants to evaluate the mathematical expression 6/2 - 1 + 35/7."})},
    {"role":"assistant","content":json.dumps({"step": "analyze", "content": "The expression contains division (/), subtraction (-), and addition (+). According to order of operations, division operations should be performed before subtraction and addition, which are performed from left to right."})},
    {"role":"assistant","content":json.dumps({"step": "execute", "content": "First, evaluate the divisions: 6/2 = 3 and 35/7 = 5. Now, the expression becomes 3 - 1 + 5. Next, perform the subtraction and addition from left to right: (3 - 1) + 5 = 2 + 5 = 7."})},
]
)
print(json.loads(response.choices[0].message.content))
print(type(json.loads(response.choices[0].message.content)))