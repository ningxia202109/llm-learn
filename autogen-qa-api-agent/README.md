# AI QA API Agent

This is an AI empowered solution to automate generate test code for testing RestFul API endpoints.

This solution is based Autogen multiple AI agent architecture.

## Process Flow
### Create test code for RestFul API

```mermaid
flowchart TB
    %% Define styles
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef highlight fill:#e1f5fe,stroke:#01579b,stroke-width:3px;
    classDef llm fill:#fff8e1,stroke:#ff6f00,stroke-width:2px;
    classDef output fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;

    %% Main Swagger-QA-Agent subgraph
    subgraph Swagger-QA-Agent["Swagger QA Agent"]
        direction TB
        SwaggerReader("🔍 Swagger Reader")
        QAAgent("🤖 AI QA Agent")
        CodeWriter("✍️ Code Writer")
        CoderReviewer("👀 Code Reviewer")
        TestExecuter("🧪 Test Executer")

        QAAgent -- "1 Ask API" --> SwaggerReader
        SwaggerReader -- "3 API Spec" --> QAAgent
        QAAgent -- "4 Test Task" --> CodeWriter
        CodeWriter -- "5 Code" --> CoderReviewer
        CoderReviewer -- "6 Feedback" --> CodeWriter
        CodeWriter -- "7 Code" --> TestExecuter
        TestExecuter -- "11 Test Result" --> QAAgent
    end

    %% Other subgraphs
    subgraph SandBox["🏖️ Sandbox"]
        TestEngine("⚙️ Test Engine")
    end

    subgraph API-Server["🖥️ API Server"]
        APIServer("🔌 API Endpoint")
        SwaggerServer("📚 Swagger Server")
    end

    subgraph LLM["🧠 Language Model"]
        gpt4omini("GPT-4 or Mini")
    end

    subgraph output["📊 Results"]
        pr("🔀 PR")
        slack("💬 Slack")
    end

    %% Cross-graph links
    SwaggerServer <-- "2 Get API Info" -->  SwaggerReader
    TestExecuter -- "8 Execute Test" --> TestEngine
    TestEngine -- "10 Test Result" --> TestExecuter
    TestEngine <-- "9 API Test" --> APIServer
    QAAgent -.-> gpt4omini
    CodeWriter -.-> gpt4omini
    CoderReviewer -.-> gpt4omini
    SwaggerReader -.-> gpt4omini
    TestExecuter -.-> gpt4omini
    QAAgent --> output

    %% Apply styles
    class SwaggerReader,QAAgent,CodeWriter,CoderReviewer,TestExecuter highlight;
    class gpt4omini llm;
    class pr,slack output;

```

## Structure

## References:
- [AutoGen dev version](https://microsoft.github.io/autogen/dev/)
- [AI-Data-Analysis-MultiAgent](https://github.com/starpig1129/AI-Data-Analysis-MultiAgent)
