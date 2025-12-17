# CUGA Demo Application - Architecture Flowchart

This document provides a visual representation of the application's logic flow using Mermaid diagrams.

## Overall Application Flow

```mermaid
flowchart TD
    Start([User Starts Application]) --> CheckEnv{Check Environment}
    CheckEnv -->|.env exists| LoadEnv[Load Environment Variables]
    CheckEnv -->|.env missing| CreateEnv[Copy .env.example to .env]
    CreateEnv --> LoadEnv
    
    LoadEnv --> DetectProvider{Detect LLM Provider}
    DetectProvider -->|Ollama| CheckOllama[Check Ollama Service]
    DetectProvider -->|Cloud| CheckAPIKey[Verify API Key]
    
    CheckOllama -->|Running| InitLogger[Initialize Output Logger]
    CheckOllama -->|Not Running| ShowError[Show Error: Start Ollama]
    CheckAPIKey -->|Valid| InitLogger
    CheckAPIKey -->|Invalid| ShowError
    
    ShowError --> End([Exit])
    
    InitLogger --> LoadConfig[Load Configuration Files]
    LoadConfig --> LoadSettings[Load settings.toml]
    LoadSettings --> LoadMode[Load Mode Config<br/>fast/balanced/accurate]
    LoadMode --> SelectCommand{Select CLI Command}
    
    SelectCommand -->|check-setup| CheckSetup[Run Setup Check]
    SelectCommand -->|examples| ShowExamples[Display Example Tasks]
    SelectCommand -->|run| RunTask[Execute Single Task]
    SelectCommand -->|interactive| InteractiveMode[Start Interactive Mode]
    
    CheckSetup --> LogOutput[Log to Markdown File]
    ShowExamples --> LogOutput
    RunTask --> ExecuteTask[Execute Task Logic]
    InteractiveMode --> WaitInput[Wait for User Input]
    
    WaitInput -->|Task| ExecuteTask
    WaitInput -->|config| ShowConfig[Display Configuration]
    WaitInput -->|help| ShowHelp[Show Help]
    WaitInput -->|exit/quit| LogOutput
    
    ShowConfig --> WaitInput
    ShowHelp --> WaitInput
    
    ExecuteTask --> InitAgent[Initialize CUGA Agent]
    InitAgent --> LoadTools[Load Custom Tools]
    LoadTools --> ProcessTask[Process Task]
    ProcessTask --> ReturnResult[Return Result]
    ReturnResult --> LogOutput
    
    LogOutput --> SaveFile[Save to ./output/<br/>script_timestamp.md]
    SaveFile --> End
```

## Task Execution Flow

```mermaid
flowchart TD
    TaskStart([Task Received]) --> ParseTask[Parse Natural Language Task]
    ParseTask --> DetermineMode{Task Mode?}
    
    DetermineMode -->|API| APIMode[API Mode Execution]
    DetermineMode -->|Web| WebMode[Web Mode Execution]
    DetermineMode -->|Hybrid| HybridMode[Hybrid Mode Execution]
    
    APIMode --> LoadAPITools[Load OpenAPI Tools]
    LoadAPITools --> PlanAPI[Plan API Calls]
    PlanAPI --> ExecuteAPI[Execute API Requests]
    ExecuteAPI --> ProcessAPIData[Process Response Data]
    ProcessAPIData --> FormatResult[Format Result]
    
    WebMode --> LoadWebTools[Load Web Tools]
    LoadWebTools --> PlanWeb[Plan Web Actions]
    PlanWeb --> ExecuteWeb[Execute Browser Actions]
    ExecuteWeb --> ExtractData[Extract Web Data]
    ExtractData --> FormatResult
    
    HybridMode --> LoadAllTools[Load API + Web Tools]
    LoadAllTools --> PlanHybrid[Plan Hybrid Workflow]
    PlanHybrid --> ExecuteHybrid[Execute Mixed Actions]
    ExecuteHybrid --> AggregateData[Aggregate Results]
    AggregateData --> FormatResult
    
    FormatResult --> LogResult[Log to Output File]
    LogResult --> ReturnToUser[Return to User]
    ReturnToUser --> TaskEnd([Task Complete])
```

## Configuration Loading Flow

```mermaid
flowchart TD
    ConfigStart([Load Configuration]) --> LoadEnvVars[Load .env Variables]
    LoadEnvVars --> CheckProvider{Provider Type?}
    
    CheckProvider -->|Ollama| SetOllama[Set Ollama Config<br/>API Key: ollama<br/>Base URL: localhost:11434]
    CheckProvider -->|OpenAI| SetOpenAI[Set OpenAI Config<br/>API Key from env<br/>Model: gpt-4o]
    CheckProvider -->|watsonx| SetWatsonx[Set watsonx Config<br/>API Key + Project ID]
    CheckProvider -->|Azure| SetAzure[Set Azure Config<br/>Endpoint + API Key]
    CheckProvider -->|OpenRouter| SetOpenRouter[Set OpenRouter Config<br/>API Key + Base URL]
    
    SetOllama --> LoadMainConfig[Load settings.toml]
    SetOpenAI --> LoadMainConfig
    SetWatsonx --> LoadMainConfig
    SetAzure --> LoadMainConfig
    SetOpenRouter --> LoadMainConfig
    
    LoadMainConfig --> ParseFeatures[Parse Features Section]
    ParseFeatures --> GetMode[Get CUGA Mode<br/>fast/balanced/accurate]
    GetMode --> LoadModeConfig[Load Mode-Specific Config<br/>modes/{mode}.toml]
    
    LoadModeConfig --> MergeConfigs[Merge Configurations]
    MergeConfigs --> LoadToolRegistry[Load Tool Registry<br/>tools/mcp_servers.yaml]
    LoadToolRegistry --> ConfigReady[Configuration Ready]
    ConfigReady --> ConfigEnd([Return Config Object])
```

## Output Logger Flow

```mermaid
flowchart TD
    LogStart([Script Execution Starts]) --> CreateLogger[Create Output Logger<br/>script_name + timestamp]
    CreateLogger --> CreateDir{./output exists?}
    CreateDir -->|No| MakeDir[Create ./output directory]
    CreateDir -->|Yes| InitFile[Initialize Markdown File]
    MakeDir --> InitFile
    
    InitFile --> WriteHeader[Write File Header<br/>Title + Timestamp]
    WriteHeader --> ScriptRuns[Script Executes]
    
    ScriptRuns --> LogSection[Log Section]
    LogSection --> LogContent{Content Type?}
    
    LogContent -->|Text| WriteText[Write Plain Text]
    LogContent -->|Code| WriteCode[Write Code Block<br/>with syntax highlighting]
    LogContent -->|Data| WriteJSON[Write JSON Block]
    LogContent -->|Table| WriteTable[Write Markdown Table]
    LogContent -->|Result| WriteResult[Write Result with Status<br/>✅ Success / ❌ Error]
    
    WriteText --> MoreLogs{More to Log?}
    WriteCode --> MoreLogs
    WriteJSON --> MoreLogs
    WriteTable --> MoreLogs
    WriteResult --> MoreLogs
    
    MoreLogs -->|Yes| LogSection
    MoreLogs -->|No| Finalize[Finalize Log File<br/>Add Footer + Timestamp]
    
    Finalize --> DisplayPath[Display File Path to User]
    DisplayPath --> LogEnd([Log Complete])
```

## Agent Initialization Flow

```mermaid
flowchart TD
    AgentStart([Initialize Agent]) --> LoadAgentConfig[Load Agent Configuration]
    LoadAgentConfig --> SetMode{Reasoning Mode?}
    
    SetMode -->|Fast| FastConfig[Fast Mode Config<br/>Max Iterations: 10<br/>Timeout: 120s<br/>Reflection: Off]
    SetMode -->|Balanced| BalancedConfig[Balanced Mode Config<br/>Max Iterations: 20<br/>Timeout: 300s<br/>Reflection: On]
    SetMode -->|Accurate| AccurateConfig[Accurate Mode Config<br/>Max Iterations: 30<br/>Timeout: 600s<br/>Reflection: On<br/>Deep Planning: On]
    
    FastConfig --> InitPlanner[Initialize Planner]
    BalancedConfig --> InitPlanner
    AccurateConfig --> InitPlanner
    
    InitPlanner --> InitExecutor[Initialize Executor]
    InitExecutor --> LoadCustomTools[Load Custom Tools]
    
    LoadCustomTools --> LoadCalculator[Load Calculator Tool]
    LoadCalculator --> LoadSentiment[Load Sentiment Analyzer]
    LoadSentiment --> LoadDataProcessor[Load Data Processor]
    LoadDataProcessor --> LoadOpenAPI[Load OpenAPI Tools<br/>from specs/]
    
    LoadOpenAPI --> RegisterTools[Register All Tools<br/>in Tool Registry]
    RegisterTools --> EnableMemory{Memory Enabled?}
    
    EnableMemory -->|Yes| InitMemory[Initialize Memory Backend]
    EnableMemory -->|No| AgentReady[Agent Ready]
    InitMemory --> AgentReady
    
    AgentReady --> AgentEnd([Return Agent Instance])
```

## Error Handling Flow

```mermaid
flowchart TD
    ErrorStart([Error Occurs]) --> CatchError[Catch Exception]
    CatchError --> IdentifyType{Error Type?}
    
    IdentifyType -->|Connection| ConnError[Connection Error<br/>Check Ollama/API]
    IdentifyType -->|Authentication| AuthError[Auth Error<br/>Check API Key]
    IdentifyType -->|Validation| ValError[Validation Error<br/>Check Input]
    IdentifyType -->|Timeout| TimeError[Timeout Error<br/>Increase Timeout]
    IdentifyType -->|Other| GenError[General Error<br/>Log Details]
    
    ConnError --> LogError[Log Error to Output File]
    AuthError --> LogError
    ValError --> LogError
    TimeError --> LogError
    GenError --> LogError
    
    LogError --> RetryEnabled{Retry Enabled?}
    RetryEnabled -->|Yes| CheckRetries{Retries Left?}
    RetryEnabled -->|No| ShowError[Display Error Message]
    
    CheckRetries -->|Yes| WaitDelay[Wait Retry Delay]
    CheckRetries -->|No| ShowError
    
    WaitDelay --> RetryOperation[Retry Operation]
    RetryOperation --> Success{Success?}
    
    Success -->|Yes| ErrorEnd([Continue Execution])
    Success -->|No| CatchError
    
    ShowError --> ProvideHelp[Provide Troubleshooting Help]
    ProvideHelp --> ErrorEnd
```

## Interactive Mode Flow

```mermaid
flowchart TD
    InterStart([Start Interactive Mode]) --> ShowWelcome[Display Welcome Message<br/>Show Available Commands]
    ShowWelcome --> InitSession[Initialize Session<br/>Load Configuration]
    InitSession --> DisplayPrompt[Display CUGA> Prompt]
    
    DisplayPrompt --> WaitInput[Wait for User Input]
    WaitInput --> ParseInput{Parse Command}
    
    ParseInput -->|Task| ExecuteTask[Execute Task]
    ParseInput -->|config| ShowConfig[Display Current Config]
    ParseInput -->|help| ShowHelp[Show Help Message]
    ParseInput -->|exit/quit| Cleanup[Cleanup & Save Logs]
    ParseInput -->|Empty| DisplayPrompt
    
    ExecuteTask --> LogTask[Log Task to Output]
    LogTask --> RunAgent[Run CUGA Agent]
    RunAgent --> ShowResult[Display Result]
    ShowResult --> LogResult[Log Result to Output]
    LogResult --> DisplayPrompt
    
    ShowConfig --> DisplayPrompt
    ShowHelp --> DisplayPrompt
    
    Cleanup --> FinalizeLog[Finalize Log File]
    FinalizeLog --> ShowGoodbye[Display Goodbye Message]
    ShowGoodbye --> InterEnd([Exit Interactive Mode])
```

## Tool Execution Flow

```mermaid
flowchart TD
    ToolStart([Tool Called]) --> ValidateInput[Validate Tool Input]
    ValidateInput --> InputValid{Input Valid?}
    
    InputValid -->|No| ReturnError[Return Validation Error]
    InputValid -->|Yes| IdentifyTool{Tool Type?}
    
    IdentifyTool -->|Calculator| ExecCalc[Execute Calculator<br/>Evaluate Expression]
    IdentifyTool -->|Sentiment| ExecSentiment[Execute Sentiment Analyzer<br/>Analyze Text]
    IdentifyTool -->|DataProcessor| ExecData[Execute Data Processor<br/>Transform Data]
    IdentifyTool -->|OpenAPI| ExecAPI[Execute API Call<br/>Make HTTP Request]
    IdentifyTool -->|Custom| ExecCustom[Execute Custom Tool<br/>Run Custom Logic]
    
    ExecCalc --> ProcessResult[Process Tool Result]
    ExecSentiment --> ProcessResult
    ExecData --> ProcessResult
    ExecAPI --> ProcessResult
    ExecCustom --> ProcessResult
    
    ProcessResult --> LogToolUse[Log Tool Usage]
    LogToolUse --> ReturnResult[Return Tool Result]
    ReturnError --> ToolEnd([Tool Execution Complete])
    ReturnResult --> ToolEnd
```

---

## Legend

- **Rectangles**: Process/Action steps
- **Diamonds**: Decision points
- **Rounded Rectangles**: Start/End points
- **Parallelograms**: Input/Output operations

## Notes

1. All flows include automatic output logging to `./output/` directory
2. Error handling is integrated at every major step
3. Configuration is loaded once at startup and cached
4. Tools are registered dynamically based on configuration
5. Interactive mode maintains session state throughout execution

---

*Generated for CUGA Demo Application*  
*Last Updated: December 17, 2024*