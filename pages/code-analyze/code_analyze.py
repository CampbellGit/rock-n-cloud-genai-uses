import os
import boto3
from langchain.llms.bedrock import Bedrock
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


HTTP_ACCEPT= 'application/json'
MODEL_ID='anthropic.claude-v2'
AWS_REGION='us-east-1'
AWS_SERVICE_BEDROCK_RUNTIME='bedrock-runtime'


def send_code_to_claude(code_file: str):

    bedrock_runtime = boto3.client(
        service_name=AWS_SERVICE_BEDROCK_RUNTIME, 
        region_name=AWS_REGION
    )

    model = Bedrock(
        model_id=MODEL_ID,
        client=bedrock_runtime,
        model_kwargs={"max_tokens_to_sample": 1000, "temperature": 0.9},
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    #memory = ConversationBufferWindowMemory(k=7)

   

    #memory.load_memory_variables({'history': []})



    prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system", """Write everything in French.
         You are a code analysis tool. Only answer in French. You are provided raw code files, write the documentation for those files. 
         Print you answer in the markdown format
         DO NOT SAY: "Here is the Markdown documentation for the provided code".
         ONLY answer with the analysis"""),
        ("human", "{code_file}"),
    ])
    parser = StrOutputParser()
    chain = prompt2 | model | parser

    response = chain.invoke({"code_file": code_file})
    print(response)
    return response

def find_files_print_structure_and_create_docs(root_dir, extensions=('.js', '.java', '.swt')):
    found_files = []  # List to store paths of files matching the extensions
    all_paths = []  # List to store all paths (files and directories)
    
    # Ensure the docs directory exists
    docs_dir = os.path.join(root_dir, 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(root_dir):
        all_paths.append(root)  # Store the directory path
        for file in files:
            file_path = os.path.join(root, file)
            all_paths.append(file_path)  # Store the file path
            if file.endswith(extensions):
                found_files.append(file_path)  # Store path if it matches the extensions
    
    # Process found files
    for file_path in found_files:
        print("file found: {}".format(file_path))
        try:
            with open(file_path, 'r') as file:
                current_file = file.read()
                analysis = send_code_to_claude(current_file)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue  # Skip to the next file if there's an error

        # Creating the markdown file in the docs folder
        md_filename = os.path.basename(file_path)
        md_file_path = os.path.join(docs_dir, md_filename + '.md')
        md_content = f"analysed {md_filename}"
        
        with open(md_file_path, 'w') as md_file:
            md_file.write(analysis)
        
        # Now, if you need to remove the first line
        with open(md_file_path, 'r') as md_file:
            lines = md_file.readlines()
        
        with open(md_file_path, 'w') as md_file:
            md_file.writelines(lines[1:])  # This skips the first line

        print("-" * 80)  # Print a separator line for readability
        
    print("\nComplete file structure:")
    # Print the entire file structure
    for path in all_paths:
        print(path)

if __name__ == "__main__":
    entry_point = os.getcwd()  # Use the current working directory as the entry point
    find_files_print_structure_and_create_docs(entry_point)


