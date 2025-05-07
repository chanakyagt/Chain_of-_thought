import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import json

# Page configuration
st.set_page_config(page_title="Chain of Thought Mimicer", page_icon="🤔")
st.header("Chain of Thought Mimicer")

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def fetchWeatherDetails(city: str):
    requestURL = f'http://api.weatherapi.com/v1/current.json?key={os.getenv("WEATHER_API")}&q={city}&aqi=yes'
    fetchedWeather = requests.get(requestURL)
    return fetchedWeather.text

def executeShellCommand(command: str):
    os.system(command)
    return f"Command executed: {command}"

# Define available tools
availableTools = {
    "fetchWeatherDetails": {
        "function": fetchWeatherDetails,
        "description": "it is an api based call that sends the city as the only arguement and recieves the weather details that contains temperasture in celcius and fareinheit,current atmospheric condition,windspeed,humidity,pressure,precipitation etc.",
        "Parameters": "single City name only"
    },
    "executeShellCommand": {
        "function": executeShellCommand,
        "description": "it is a function that takes the command as the only arguement and passes it to os.system() method to do the required task via the cms so we just have to pass the proper cmd instruction as per the user requirement NOTE:the commands must and should be windows based cmd commands",
        "Parameters": "single command only"
    }
}

def toolCaller(tool: str, parameter: str):
    func = availableTools.get(tool).get("function")
    return func(parameter)

# System prompt
system_Prompt_initial = '''
you are an wise helpful agent who solves the issues of the user , in case you face any limitation or the task given by the user is out of your scope or if you have to have access to some external item in order to complete the task or if you want something as intermidiary to take care of the task you can call the tools from the list of available tools if it matches the current requirement of the user if you dont find any tool that matches the user requirement you return "NO_TOOL_FOUND"

always try to check if the given task can be performed using tool if yes use tool

only use the execute step if and only if you have a tool that needs to be executed elso do not use this step

the system you are working on is windows

But first you Carefully analyze the query and breakdown the tasks 

Remember that you only return one step at a time and generate the next step once you get the previous step as input 

Output should be strictly in JSON format

Dont take assumptions for real time values and real tasks always care fully analyze if you have to use a tool using the execute step

also remember only once the step should be execute and it must mandatorily contain the the functionToCall,content and parameter 

Output Format:
{"step":"string","content":"string"}

Example:
Query:What is 5*3+10
Output:{"step":"think","content":"So the user has given me a mathematical instruction containing + and *}
Output:{"step":"analyze","content":"Since the user is saying to solve the mathematical expression i have the capability to do so  no need for any tool calling)}
Output:{"step":"analyze","content":"Since the mathematic expression contains * and + symbol * (Multiply will take preference and hence resolved first followed by the + operator)}
Output:{"step":"execute","content":"So since 5*3=15 and 15+10=25"}
Output:{"step":"return","content":"the answer for the expression is 25"}

Example:
Query:What is the Weather in Bhopal
Output:{"step":"think","content":"So the user wants to know the current Weather in bhopal}
Output:{"step":"analyze","content":"Since the weather changes in real time it is out of my scope to get the current weather   )}
Output:{"step":"analyze","content":"So I have to search if any of the available tools can be used this time to resolve usee requirements" )}
Output:{"step":"finding","content":"the tool named fetchWeatherDetails can fulfil the requirement"}
Output:{"step":"execute","content":"True","functionToCall":"fetchWeatherDetails","parameter":"Bhopal"}
Output:{"step":"recieve","content":{"location":{"name":"Lucknow","region":"Uttar Pradesh","country":"India","lat":26.85,"lon":80.917,"tz_id":"Asia/Kolkata","localtime_epoch":1745506607,"localtime":"2025-04-24 20:26"},"current":{"last_updated_epoch":1745505900,"last_updated":"2025-04-24 20:15","temp_c":30.2,"temp_f":86.4,"is_day":0,"condition":{"text":"Mist","icon":"//cdn.weatherapi.com/weather/64x64/night/143.png","code":1030},"wind_mph":6.9,"wind_kph":11.2,"wind_degree":285,"wind_dir":"WNW","pressure_mb":1003.0,"pressure_in":29.62,"precip_mm":0.0,"precip_in":0.0,"humidity":24,"cloud":0,"feelslike_c":28.0,"feelslike_f":82.4,"windchill_c":33.9,"windchill_f":93.1,"heatindex_c":31.9,"heatindex_f":89.4,"dewpoint_c":-11.7,"dewpoint_f":10.9,"vis_km":4.0,"vis_miles":2.0,"uv":0.0,"gust_mph":14.6,"gust_kph":23.4,"air_quality":{"co":379.25,"no2":2.96,"o3":161.0,"so2":8.51,"pm2_5":46.62,"pm10":312.65,"us-epa-index":3,"gb-defra-index":5}}}}
Output:{"step":"return","content":"The temperature in lucknow is 30.2 degree celcius" }

Example:
Query:Tell me yesterday's news
Output:{"step":"think","content":"So the user wants to know the yesterday's news}
Output:{"step":"analyze","content":"Since the news changes in real time it is out of my scope to get the news)}
Output:{"step":"analyze","content":"So I have to search if any of the available tools can be used this time to resolve usee requirements" )}
Output:{"step":"finding","content":"No Tool fulfils the requirement"}
Output:{"step":"execute","content":"False" ,"functionToCall":"None"}
Output:{"step":"return","content":"Sorry I do not have the capability to find news as it changes at realtime" }
'''

finalSystemPrompt = '''AvailableTools:{}

Task:{}
'''.format(availableTools, system_Prompt_initial)

# UI components
st.markdown("This tool demonstrates how AI breaks down problems and thinks step-by-step")
st.write("Enter your query below and watch the AI's thought process unfold")

# Create a container for the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.thinking_steps = []

# Function to display the thinking steps with appropriate styling
def display_thinking_steps():
    for i, step in enumerate(st.session_state.thinking_steps):
        step_type = step["step"]
        content = step["content"]
        
        # Different styling based on step type
        if step_type == "think":
            with st.container(border=True):
                st.markdown(f"**🤔 Thinking:** {content}")
        elif step_type == "analyze":
            with st.container(border=True):
                st.markdown(f"**🔍 Analysis:** {content}")
        elif step_type == "finding":
            with st.container(border=True):
                st.markdown(f"**🔎 Finding:** {content}")
        elif step_type == "execute":
            with st.container(border=True):
                if "functionToCall" in step:
                    st.markdown(f"**⚙️ Executing:** Calling function `{step['functionToCall']}` with parameter `{step['parameter']}`")
                else:
                    st.markdown(f"**⚙️ Executing:** {content}")
        elif step_type == "recieve":
            with st.container(border=True):
                st.markdown(f"**📥 Received Data:**")
                # Try to parse and format JSON data
                try:
                    parsed_content = json.loads(content)
                    st.json(parsed_content)
                except:
                    st.text(content)
        elif step_type == "return":
            with st.container(border=True):
                st.markdown(f"**✅ Final Answer:** {content}")

# User input
userQuery = st.chat_input("Ask me anything...")

if userQuery:
    # Clear previous thinking steps when a new query is entered
    st.session_state.thinking_steps = []
    
    # Show user message
    st.chat_message("user").write(userQuery)
    
    # Initialize message array for the conversation
    messageArray = [
        {"role": "system", "content": finalSystemPrompt}
    ]
    messageArray.append({"role": "user", "content": userQuery})
    
    # Progress indicator
    with st.status("Thinking...", expanded=True) as status:
        while True:
            response = client.chat.completions.create(
                model='gpt-4.1-mini',
                messages=messageArray
            )
            
            response_content = response.choices[0].message.content
            messageArray.append({"role": "assistant", "content": response_content})
            
            # Parse and store the thinking step
            try:
                step_data = json.loads(response_content)
                st.session_state.thinking_steps.append(step_data)
                status.update(label=f"Step: {step_data['step'].capitalize()}")
            except json.JSONDecodeError:
                st.error("Error parsing response")
                break
            
            # Check if we've reached the return step
            if step_data.get("step") == "return":
                status.update(label="Done!", state="complete")
                break
            # Handle execute step and tool calling
            elif step_data.get("step") == "execute" and "functionToCall" in step_data and step_data.get("functionToCall") != "None":
                try:
                    toolResponse = toolCaller(
                        step_data.get("functionToCall"),
                        step_data.get("parameter")
                    )
                    receive_step = {"step": "recieve", "content": json.dumps(toolResponse)}
                    st.session_state.thinking_steps.append(receive_step)
                    messageArray.append({"role": "assistant", "content": json.dumps(receive_step)})
                except Exception as e:
                    st.error(f"Error calling tool: {e}")
                    break
    
    # Display all thinking steps
    display_thinking_steps()
