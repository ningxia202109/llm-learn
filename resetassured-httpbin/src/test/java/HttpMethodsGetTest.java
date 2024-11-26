import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class HttpMethodsGetTest extends BaseTest {

    @BeforeAll
    public static void setup() {
        RestAssured.reset();
        RestAssured.baseURI = "https://httpbin.org";  // Set the correct base URI
    }

    @Test
    public void testGet() {

        System.out.println("Starting test");
        System.out.println("Base URI: " + RestAssured.baseURI);
        System.out.println("Base Path: " + RestAssured.basePath);

        Response response = given()
                .accept(ContentType.JSON)
                .when()
                .get("/get");

        System.out.println("Response received: " + response.asString());
        // Log the response body with class and method name
        String className = this.getClass().getSimpleName();
        String methodName = new Object() {
        }.getClass().getEnclosingMethod().getName();
        System.out.println("Response Body for " + className + "." + methodName + ":");
        System.out.println(response.getBody().asPrettyString());

        // Perform assertions
        response.then()
                .statusCode(200)
                .contentType(ContentType.JSON)
                .body("url", equalTo("https://httpbin.org/get"))
                .body("$", hasKey("args"))
                // .body("headers.Accept", equalTo("application/json"))
                // .body("headers.Host", equalTo("httpbin.org"))
                .body("origin", not(emptyOrNullString()))
                .header("Access-Control-Allow-Credentials", "true")
                .header("Access-Control-Allow-Origin", "*")
                .header("Content-Type", "application/json")
                .header("Server", "gunicorn/19.9.0");
    }
}
