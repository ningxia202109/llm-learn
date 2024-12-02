from typing import Dict, Any


class HttpMethod:
    def __init__(self, method_data: Dict[str, Any]):
        self.produces = method_data.get("produces", [])
        self.responses = method_data.get("responses", {})
        self.summary = method_data.get("summary", "")
        self.tags = method_data.get("tags", [])
        self.parameters = method_data.get("parameters", [])

    def full_spec(self) -> Dict:
        return {
            "method": self.method,
            "summary": self.summary,
            "description": self.description,
            "parameters": self.parameters,
            "responses": self.responses,
        }

    def __str__(self) -> str:
        return f"HttpMethod(summary='{self.summary}', tags={self.tags})"
