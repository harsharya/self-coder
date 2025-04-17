from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel

import os
import json
load_dotenv()

client =  genai.Client(api_key='')

def run_command(command):
    result=os.system(command=command)
    return result

def language_project(language):
    result =run_command()
    return result
    
def folder_create(path: str):
    newpath = f'{path}' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
def file_create(file_data: list):
    try:
        filename, content = file_data  # unpacking the list
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return filename
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")



available_tools={
    "run_command":{
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output"
    },
    "folder_create":{
        "fn": folder_create,
        "description": "This methond will help to create the folder"
    },
    "file_create":{
        "fn": file_create,
        "description": "This methond will help to create the folder in the new structure"
    },
}

system_prompt="""

You are an AI assitant which help user to create the boiler plate structure of a language selected by user. 
Use the run_command tool to create the boilder plate folder structure.
In the index or main file write to fuction to two numbers and write a function a test the output in the test folder
The steps are you get a user input, you analyse, you think, you again think for serveral times and then take action and then return the output with explanation
The files written should not be enclosed in BOS and end EOS.

Rules:
    1. Always perform one step at a time and wait for next input
    2. Always Create project Folder first and create file inside the created project folder.
    3. Analyze the user query and find in which language user wants to create project 
    4. Strictly follow the boiler plate structure of that language
    5. Always create test cases for the functions 
    
Output Format:
{{
"step":"string", 
"content":"string",
"function": "The name of function  if the step is action",
"input": "The input parameter for the function",
}}
Avialble Tools:
- run_command: This tool will take command to execute on system and retun output
- file_create: This tool will help to write file 

Example 1:
User Query: Please create the boiler plate project
output:{{"step": "analyze", "content": "The user wants wants to create the boiler plate project"}}
output:{{"step": "analyze", "content": "Analyze the user query if the user requested to write some code"}}
output:{{"step": "plan", "content": "User is interested in to create the boiler plate structure"}}
output:{{"step": "plan", "content": "Use the available tools to create the project files"}}
output:{{"step": "action", "function": "run_command", "input": "my-project, "}}
output:{{"step": "observe", "content": "Strucure created"}}
output:{{"step": "output", "content": "Boiler plate structure is created"}}

How To Use Tool How to file_write_content 

you action step should be like 
Output: {{"step": "action", "function": "file_write_content", "input": ["filename.txt","Here Send Content as String"]}}


"""
message=[
    types.Content(
    role='assistant',
    parts=[types.Part.from_text(text=system_prompt)]
    )
]
print("I am an AI assistant. I will help you to generate the boiler plate structure")

while True:
    query= input("> ")
    message.append(types.Content(
    role='user',
    parts=[types.Part.from_text(text=query)]
    ))
    response = client.models.generate_content(
            #model='gemini-2.0-flash',
            model='gemini-2.0-flash-lite',
            contents=message,
            config={
                'response_mime_type': 'application/json',               
            },
        )
    #print(f"response text", response.text)
    #print(f"response text type", type(response.text))
    loadresult=json.loads(response.text)
    #print(f"loadresult", loadresult)
    #print(f"type", type(loadresult))
    print(f"length", len(loadresult))
    if isinstance(loadresult, list):
        for item in loadresult:  
            #result=json.dumps(key["step"])
            #print(f"testing {json.dumps(parsed_output[step])}")
            if (item["step"]== "analyze"):
                print(f"test", {item["step"]})
                print(f"🧠: {item["content"]}")
                continue
            if (item["step"]== "plan"):
                print(f"test", {item["step"]})
                print(f"🧠: {item["content"]}")
                continue

            if(item["step"]=="action"):
                tool_name=item["function"]
                tool_input=item["input"]

                if available_tools.get(tool_name, False) !=False:
                    output=available_tools[tool_name].get("fn")(tool_input)
                    print(f"Created")
                    #message.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                    continue

            if item["step"]=='output':
                print(f"🤖: {item["content"]}")
                break
    elif isinstance(loadresult, dict):
        #print("Its is a dict")
        while True:
            for key, value in loadresult.items():
                #print(f"step {value}, ")
                if (key == "content"):
                    message.append(types.Content(
                        role='model',
                        parts=[types.Part.from_text(text=value)]
                        ))
                    #print(f"test", key)
                    print(f"🧠:", value)
                if (value == "output"):
                    #print(f"test", key)
                    print(f"🧠:", value)
                    break
                response = client.models.generate_content(
                model='gemini-2.0-flash-lite',
                contents=message,
                config={
                    'response_mime_type': 'application/json',               
                },
                )
                loadresult=json.loads(response.text)        



