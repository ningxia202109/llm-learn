
// BaseTest.java
import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeAll;

public class BaseTest {
    protected static String baseUrl;

    @BeforeAll
    public static void setup() {
        // Default to httpbin.org if no environment is specified
        String env = System.getProperty("test.environment", "production");
        System.out.println("Test env is: " + env);
        switch (env) {
            case "local":
                baseUrl = "http://localhost:8585";
                break;
            case "production":
            default:
                baseUrl = "https://httpbin.org";
                break;
        }

        RestAssured.baseURI = baseUrl;
        System.out.println("Using base URL: " + baseUrl);
    }
}
