# Rest API testing with AI assisted
A sample RestAPI test by RestAssured test framework, and the testing generetats Junit Test report, the error log will be analyisted by LLM.

The AI agent uses AutoGen framework.

## Process Flow
```mermaid
graph TB
    A[report-reader] --read-junit-report--> B
    B[find-failed-testcase] --get-error-message--> C
    C[ai-qa-agent] --error-message--> D
    D[gpt-4o-mini] --analyse-error-message--> C
    C --add-ai-qa-agent-response--> B
```

## Architecture
```mermaid
architecture-beta
    group github(cloud)[GITHUB]

    service server(server)[Server] in github

```
