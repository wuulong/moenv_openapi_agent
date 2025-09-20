import yaml
from pathlib import Path

def remove_hardcoded_api_key(file_path: Path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if 'components' in data and 'securitySchemes' in data['components']:
        security_schemes = data['components']['securitySchemes']
        for scheme_name, scheme_details in security_schemes.items():
            if scheme_details.get('type') == 'apiKey' and 'name' in scheme_details:
                # Assuming the API key is defined as a parameter in paths
                # This part might need adjustment based on the exact structure
                # of how the default is set.
                # For now, let's focus on parameters within paths.
                pass # We will handle this in the paths section

    if 'paths' in data:
        for path, methods in data['paths'].items():
            for method, details in methods.items():
                if 'parameters' in details:
                    for param in details['parameters']:
                        if param.get('name') == 'api_key' and 'default' in param:
                            print(f"Removing hardcoded default API key from: {path} -> {method} -> {param.get('name')}")
                            del param['default']
                if 'requestBody' in details and 'content' in details['requestBody']:
                    for content_type, content_details in details['requestBody']['content'].items():
                        if 'schema' in content_details and 'properties' in content_details['schema']:
                            properties = content_details['schema']['properties']
                            if 'api_key' in properties and 'default' in properties['api_key']:
                                print(f"Removing hardcoded default API key from requestBody: {path} -> {method} -> api_key")
                                del properties['api_key']['default']

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    openapi_file = Path(__file__).parent / 'moenv_openapi.yaml'
    if openapi_file.exists():
        remove_hardcoded_api_key(openapi_file)
        print(f"Processed {openapi_file.name}: Removed hardcoded default API keys.")
    else:
        print(f"Error: {openapi_file.name} not found.")
