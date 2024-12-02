from tools import SwaggerAPIReader
import json


def main():
    api_url = "https://httpbin.org/spec.json"
    reader = SwaggerAPIReader(api_url)

    selected_api = "/bytes/{n}"
    selected_apiSpec = reader.get_endpoint(selected_api)

    if selected_apiSpec:
        print(f"\nDetails for {selected_api} endpoint:")
        print(f"Methods: {selected_apiSpec.get_all_methods()}")
        print("Full specification in JSON format:")
        print(selected_apiSpec.full_spec_in_json())


if __name__ == "__main__":
    main()
