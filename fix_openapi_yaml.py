import re

file_path = "/Volumes/D2024/github/adk-python/my_samples/moenv_openapi_agent/moenv_openapi.yaml"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace '200:' with ''200':' within the 'responses' section
    # This regex looks for 'responses: { ' followed by '200:' and captures the content inside the curly braces
    # It's a bit tricky with YAML's flexible syntax, but based on the provided example,
    # the direct string replacement should work for the specific pattern.
    # A more robust solution might involve a YAML parser, but for this specific fix, string replacement is sufficient.
    old_string = "responses: { 200: { description: OK } }"
    new_string = "responses: { '200': { description: OK } }"
    
    modified_content = content.replace(old_string, new_string)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)

    print(f"Successfully fixed '{file_path}'")

except FileNotFoundError:
    print(f"Error: File not found at '{file_path}'")
except Exception as e:
    print(f"An error occurred: {e}")
