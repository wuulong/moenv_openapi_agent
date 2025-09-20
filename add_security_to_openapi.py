import yaml
import os

def add_security_to_openapi(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    paths = data.get('paths', {})
    for path_key, methods in paths.items():
        for method_key, method_details in methods.items():
            if method_key == 'get': # Only modify GET operations
                # Add security section
                method_details['security'] = [{'ApiKeyAuth': []}]

                # Remove api_key from parameters
                parameters = method_details.get('parameters', [])
                new_parameters = []
                for param in parameters:
                    if param.get('name') != 'api_key':
                        new_parameters.append(param)
                method_details['parameters'] = new_parameters

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    openapi_file_path = os.path.join(script_dir, 'moenv_openapi.yaml')
    
    if os.path.exists(openapi_file_path):
        add_security_to_openapi(openapi_file_path)
        print(f"Successfully added security definitions and removed api_key parameters from {openapi_file_path}")
    else:
        print(f"Error: {openapi_file_path} not found.")
