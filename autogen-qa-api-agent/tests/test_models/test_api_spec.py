import unittest
from src.models import ApiSpec, HttpMethod
class TestApiSpec(unittest.TestCase):

    def setUp(self):
        self.sample_methods = {
            "get": {
                "summary": "Get pet",
                "description": "Returns a single pet",
                "parameters": [
                    {
                        "name": "petId",
                        "in": "path",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation"
                    }
                }
            },
            "post": {
                "summary": "Add pet",
                "description": "Add a new pet to the store",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/Pet"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Created"
                    }
                }
            }
        }
        self.api_spec = ApiSpec("/pet/{petId}", self.sample_methods)

    def test_init(self):
        self.assertEqual(self.api_spec.path, "/pet/{petId}")
        self.assertIsInstance(self.api_spec.methods, dict)
        self.assertEqual(len(self.api_spec.methods), 2)

    def test_get_all_methods(self):
        methods = self.api_spec.get_all_methods()
        self.assertListEqual(sorted(methods), ["get", "post"])

    def test_get_method(self):
        get_method = self.api_spec.get_method("get")
        self.assertIsInstance(get_method, HttpMethod)
        self.assertEqual(get_method.summary, "Get pet")

        # Test case insensitivity
        post_method = self.api_spec.get_method("POST")
        self.assertIsInstance(post_method, HttpMethod)

        # Test non-existent method
        self.assertIsNone(self.api_spec.get_method("put"))

    def test_get_parameters(self):
        get_params = self.api_spec.get_parameters("get")
        self.assertEqual(len(get_params), 1)
        self.assertEqual(get_params[0]["name"], "petId")

        post_params = self.api_spec.get_parameters("post")
        self.assertEqual(len(post_params), 1)
        self.assertEqual(post_params[0]["name"], "body")

        # Test non-existent method
        self.assertEqual(self.api_spec.get_parameters("put"), [])

    def test_full_spec(self):
        full_spec = self.api_spec.full_spec()
        self.assertIsInstance(full_spec, dict)

if __name__ == '__main__':
    unittest.main()
