import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
available_tools=[
    {
        "tool_name":"get_weather",
        "task":"sends a request via a weather fetching api and can return a JSON object that can be utilized to understand the weather in the place",
        # function:getWeather;
        "parameters":"cityname only"
    }
]
example_response='''{
    "location": {
        "name": "Ghaziabad",
        "region": "Uttar Pradesh",
        "country": "India",
        "lat": 28.6667,
        "lon": 77.4333,
        "tz_id": "Asia/Kolkata",
        "localtime_epoch": 1745374047,
        "localtime": "2025-04-23 07:37"
    },
    "current": {
        "last_updated_epoch": 1745373600,
        "last_updated": "2025-04-23 07:30",
        "temp_c": 24.2,
        "temp_f": 75.6,
        "is_day": 1,
        "condition": {
            "text": "Mist",
            "icon": "//cdn.weatherapi.com/weather/64x64/day/143.png",
            "code": 1030
        },
        "wind_mph": 7.6,
        "wind_kph": 12.2,
        "wind_degree": 286,
        "wind_dir": "WNW",
        "pressure_mb": 1008.0,
        "pressure_in": 29.77,
        "precip_mm": 0.0,
        "precip_in": 0.0,
        "humidity": 25,
        "cloud": 0,
        "feelslike_c": 23.3,
        "feelslike_f": 73.9,
        "windchill_c": 30.4,
        "windchill_f": 86.7,
        "heatindex_c": 28.2,
        "heatindex_f": 82.7,
        "dewpoint_c": -8.5,
        "dewpoint_f": 16.8,
        "vis_km": 3.0,
        "vis_miles": 1.0,
        "uv": 0.9,
        "gust_mph": 10.7,
        "gust_kph": 17.2
    }
}'''
system_prompt=f'''
you are an helpful ai agent whose work is to satisfy client's requirement,and when you get a requirement from the user you carefully analyze what steps you have to take in order to perform the required task within these steps you also decide which tools to be used in order to satisfy the requirement 

Available tools:{available_tools}

Example:
    Query:What is the weather today in ghaziabad
    Output:{{"step":"Understanding","content":"user wants to know about the current weather in ghaziabad"}}
    Output:{{"step":"plan","content":"So to get the weather i need to check if i have any tool that can help me get the weather if not i should tell the user that i do not have the facility to access the realtime weather"}}
    Output:{{"step":"action","content":"checking if i have the weather tool"}}
    Output:{{"step":"action","content":"yes i have such tool so let me use it to get the temperature in ghaziabad"}}
    Output:{{"step":"action","function":"get_weather",input:"ghaziabad}}
    Output:{{"step":"observe","response":{example_response}}}
    Output:{{"step":"output","response":"the wether in ghaziabad is 24.2 degree celsius misty climate and winds running at 12.2kph"}}
'''
client = OpenAI(
    api_key=os.getenv('GEMINI_API_KEY'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
messagesArray=[
    {"role":"system","message":"yoou are a user agent"},
    {"role":"user","message":"what is the temperature in ghaziabad"},
    ]
response = client.chat.completions.create(
    model="gemini-2.0-flash",
    n=1,
    messages=messagesArray
)
print(response.choices[0].message.content)
