import json
from typing import List, Dict, Any, Optional
from .http_method import HttpMethod


class ApiSpec:
    def __init__(self, path: str, spec_data: Dict[str, Dict[str, Any]]):
        self.path = path
        self.methods: Dict[str, HttpMethod] = {}
        for method, method_data in spec_data.items():
            self.methods[method] = HttpMethod(method_data)

    def get_method(self, method: str) -> Optional[HttpMethod]:
        return self.methods.get(method.lower())

    def get_all_methods(self) -> List[str]:
        return list(self.methods.keys())

    def get_content_types(self, method: str) -> List[str]:
        http_method = self.get_method(method)
        return http_method.produces if http_method else []

    def get_response(self, method: str, status_code: str) -> Dict[str, str]:
        http_method = self.get_method(method)
        return http_method.responses.get(status_code, {}) if http_method else {}

    def get_parameters(self, method: str) -> List[Dict[str, Any]]:
        http_method = self.get_method(method)
        return http_method.parameters if http_method else []

    def __str__(self) -> str:
        methods = ", ".join(self.get_all_methods())
        return f"ApiSpec(path='{self.path}', methods=[{methods}])"

    def full_spec(self) -> Dict[str, Any]:
        return {
            self.path: {
                method: {
                    "produces": http_method.produces,
                    "responses": http_method.responses,
                    "summary": http_method.summary,
                    "tags": http_method.tags,
                    "parameters": http_method.parameters,
                }
                for method, http_method in self.methods.items()
            }
        }

    def full_spec_in_json(self) -> str:
        return json.dumps(self.full_spec(), indent=2)


# Example usage
if __name__ == "__main__":
    spec_data = {
        "delete": {
            "produces": ["application/json"],
            "responses": {"200": {"description": "Anything passed in request"}},
            "summary": "Returns anything passed in request data.",
            "tags": ["Anything"],
        },
        "get": {
            "parameters": [
                {"in": "header", "name": "Authorization", "schema": {"type": "string"}}
            ],
            "produces": ["application/json"],
            "responses": {"200": {"description": "Anything passed in request"}},
            "summary": "Returns anything passed in request data.",
            "tags": ["Anything"],
        },
    }

    api_spec = ApiSpec("/anything", spec_data)

    print(api_spec)
    print(f"All methods: {api_spec.get_all_methods()}")
    print(f"GET method details: {api_spec.get_method('get')}")
    print(f"GET content types: {api_spec.get_content_types('get')}")
    print(f"DELETE 200 response: {api_spec.get_response('delete', '200')}")
    print(f"GET parameters: {api_spec.get_parameters('get')}")
    print("Full spec:")
    print(api_spec.full_spec())
