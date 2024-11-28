# Rest API testing with AI assisted
A sample RestAPI test by RestAssured test framework, and the testing generetats Junit Test report, the error log will be analyisted by LLM.

The AI agent uses AutoGen framework.

## JUnit Report Reader Flow

```mermaid
graph TD
    A[JUnit Test Execution] -->|Generates| B[XML Test Report]
    B -->|Input| C[JUnit Report Reader]
    C -->|Parses| D[Test Results]
    D -->|Extracts| E[Test Statistics]
    D -->|Identifies| F[Failed Tests]
    E --> G[Summary Report]
    F --> G
    G -->|Analyzed by| H[AI/LLM]
    H -->|Generates| I[Insights and Recommendations]
