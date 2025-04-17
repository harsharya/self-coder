from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel

import os
import json
load_dotenv()

client =  genai.Client(api_key='AIzaSyB0UysnEdOkBrdBPzmgliovbNSnICtXwvk')

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
def file_create(path: str, text: str):
        with open(path, 'w') as file:
            file.write(text)



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
Use the current directory to create boiler plate structure. 
    Rules:
    1. Analyze the user query and find in which languaage user wants to create project
    2. Always perform one step at a time
    3. Strictly follow the boiler plate structure of that language
    4. All files should be in a directory
    5. Always create test cases of the functions and test the output
    
Output Format:
{{
"step":"string", 
"content":"string",
"function": "The name of function  if the step is action",
"input": "The input parameter for the function",
}}
Avialble Tools:
- run_command: This tool will take command to execute on system and retun output


Example:
User Query: Please create the boiler plate project
output:{{"step": "analyze", "content": "Analyze the user query in which language user wants to create the boiler plate project"}}
output:{{"step": "analyze", "content": "Analyze the user query if the user requested to write some code"}}
output:{{"step": "plan", "content": "User is interested in to create the boiler plate python project"}}
output:{{"step": "plan", "content": "Plan what the files need to created"}}
output:{{"step": "action", "function": "run_command", "input": "my-project"}}
output:{{"step": "observe", "content": "Strucure created"}}
output:{{"step": "output", "content": "Boiler plate structure is created for python project"}}




"""
message=[
    types.Content(
    role='ASSISTANT',
    parts=[types.Part.from_text(text=system_prompt)]
    )
]
print("I am an AI assistant. I will help you to generate the boiler plate structure")
query=input("> ")
message.append(types.Content(
    role='user',
    parts=[types.Part.from_text(text=query)]
))
while True:
    response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=message,
            config={
                'response_mime_type': 'application/json',               
            },
        )
    loadresult=json.loads(response.text)
    print(f"type", type(loadresult))
    if isinstance(loadresult, list):
        for item in loadresult:  
            #result=json.dumps(key["step"])
            #print(f"testing {json.dumps(parsed_output[step])}")
            print(f"test", item["step"])
            if (item["step"]== "plan"):
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

    query= input("> ")
    message.append(types.Content(
    role='user',
    parts=[types.Part.from_text(text=query)]
    ))


