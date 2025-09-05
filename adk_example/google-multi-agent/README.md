# Google Multi-Agent Travel Planning System

This project demonstrates a Google ADK (Agent Development Kit) multi-agent system that provides weather information, creates travel itineraries, and books hotel accommodations based on weather conditions.

## Agent Architecture Patterns

This project demonstrates two different Google ADK agent patterns:

### 1. **Single Agent Pattern** (`agent.py`)
```python
root_agent = Agent(
    name="travel_weather_agent",
    model="gemini-2.0-flash",
    tools=[get_weather, create_travel_itinerary, book_hotel],  # Direct functions
)
```

### 2. **Multi-Agent Pattern** (`multi_agent_system.py`)
```python
# Specialized sub-agents
weather_agent = Agent(name="weather_specialist", tools=[get_weather])
itinerary_agent = Agent(name="itinerary_specialist", tools=[create_travel_itinerary])
hotel_agent = Agent(name="hotel_specialist", tools=[book_hotel])

# Coordinating LlmAgent
travel_coordinator = LlmAgent(
    name="travel_coordinator",
    tools=[
        AgentTool(agent=weather_agent),      # Sub-agents as tools
        AgentTool(agent=itinerary_agent),
        AgentTool(agent=hotel_agent),
    ]
)
root_agent = travel_coordinator
```

## Key Differences: Agent vs LlmAgent

| Aspect | Agent | LlmAgent |
|--------|-------|----------|
| **Purpose** | Single-task execution | Multi-agent orchestration |
| **Tools** | Functions/methods | Other agents via `AgentTool()` |
| **Architecture** | Flat, direct | Hierarchical, coordinated |
| **Complexity** | Simple workflows | Complex, multi-step processes |
| **Best For** | Direct tool usage | Agent coordination |
| **Example Use** | Weather checking | Financial analysis with multiple specialists |

## Multi-Agent System Benefits

✅ **Specialization**: Each agent is expert in one domain
✅ **Modularity**: Easy to add/remove specialists
✅ **Scalability**: Can handle complex workflows
✅ **Reusability**: Sub-agents can be used in other systems
✅ **Clarity**: Clear separation of responsibilities

## When to Use Each Pattern

### Choose **Single Agent Pattern** when:
- ✅ Simple, direct workflows
- ✅ Limited number of tools (3-5 functions)
- ✅ Rapid prototyping
- ✅ Learning/educational purposes
- ✅ Single domain expertise

### Choose **Multi-Agent Pattern** when:
- ✅ Complex workflows requiring coordination
- ✅ Multiple specialized domains
- ✅ Enterprise/production systems
- ✅ Scalable architecture needed
- ✅ Team development (different specialists)

## Switching Between Patterns

Edit `agents/travel_weather_agent/__init__.py`:

```python
# For Single Agent Pattern:
from .agent import root_agent

# For Multi-Agent Pattern:
# from .multi_agent_system import root_agent
```

## Architecture Comparison

### Single Agent Flow:
```
User Request → Agent → Function Tools → Response
             ↓
         [get_weather, create_itinerary, book_hotel]
```

### Multi-Agent Flow:
```
User Request → Coordinator → Sub-Agents → Response
             ↓              ↓
         LlmAgent      [weather_agent, 
                       itinerary_agent, 
                       hotel_agent]
```

## Real-World Examples

### Financial Analysis (Multi-Agent)
```python
financial_coordinator = LlmAgent(
    tools=[
        AgentTool(agent=data_analyst_agent),
        AgentTool(agent=trading_analyst_agent),
        AgentTool(agent=risk_analyst_agent),
    ]
)
```

### Customer Service (Single Agent)
```python
support_agent = Agent(
    tools=[get_order_status, process_refund, send_email]
)
```

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Google ADK Travel Planning System                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌───────────────────────────────────────────────────────┐
│   Web Browser   │    │                    ADK Web Server                     │
│ (localhost:8001)│◄───┤                  (FastAPI + UI)                       │
└─────────────────┘    └───────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
                       ┌───────────────────────────────────────────────────────┐
                       │              travel_weather_agent                     │
                       │           (Gemini 2.0 Flash Model)                    │
                       └───────────────────────────────────────────────────────┘
                                                    │
                            ┌───────────────────────┼───────────────────────┐
                            ▼                       ▼                       ▼
                  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
                  │   get_weather   │    │create_travel_   │    │   book_hotel    │
                  │     Tool        │    │itinerary Tool   │    │     Tool        │
                  └─────────────────┘    └─────────────────┘    └─────────────────┘
                            │                       │                       │
                            ▼                       ▼                       ▼
                  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
                  │  Hardcoded      │    │ Activity Logic  │    │ Hotel Database  │
                  │ Weather Data    │    │ Weather-based   │    │ 6 Hotel Types   │
                  │                 │    │ Recommendations │    │ with Amenities  │
                  │ • London        │    │                 │    │                 │
                  │ • Paris         │    │ Sunny →Outdoor  │    │ • Beachfront    │
                  │ • New York      │    │ Rain → Indoor   │    │ • Luxury Spa    │
                  │ • Tokyo         │    │ Overcast→Mixed  │    │ • City Center   │
                  │ • Sydney        │    │                 │    │ • Business      │
                  │ • Default       │    │                 │    │ • Outdoor Pool  │
                  └─────────────────┘    └─────────────────┘    │ • Boutique      │
                                                                └─────────────────┘

                              Data Flow & Tool Interaction
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│  User Request: "Plan a trip to Paris"                                            │
│         │                                                                        │
│         ▼                                                                        │
│  ┌─────────────┐  Weather Report   ┌──────────────────┐  Hotel Type              │
│  │get_weather  │ ─────────────────►│create_travel_    │ ──────────────────┐      │
│  │   (Paris)   │                   │itinerary (Paris) │                   │      │
│  └─────────────┘                   └──────────────────┘                   │      │
│         │                                     │                           │      │
│         │                                     │                           ▼      │
│         │                                     │                  ┌─────────────┐ │
│         │                              Activities &              │ book_hotel  │ │
│         │                              Recommendations           │   (Paris,   │ │
│         │                                     │                  │ hotel_type) │ │
│         │                                     │                  └─────────────┘ │
│         ▼                                     ▼                           │      │
│  ┌──────────────────────────────────────────────────────────────────────────────┐│
│  │                    Unified Response                                          ││
│  │  • Weather: "Sunny, 22.3°C"                                                  ││
│  │  • Activities: ["outdoor sightseeing", "rooftop dining", ...]                ││
│  │  • Hotel: "Beachfront Resort booked - HTL-1234"                              ││
│  │  • Amenities: ["private beach", "outdoor pool", "spa services"]              ││
│  └──────────────────────────────────────────────────────────────────────────────┘│
│                                     │                                            │
│                                     ▼                                            │
│                              User receives comprehensive                         │
│                              travel plan with booking details                    │
└──────────────────────────────────────────────────────────────────────────────────┘

                              Tool Independence
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  Individual Tool Usage:                                                     │
│                                                                             │
│  ┌─────────────┐     ┌──────────────────┐     ┌─────────────┐               │
│  │"Weather in  │     │"Create itinerary │     │"Book luxury │               │
│  │ Tokyo?"     │     │ for London"      │     │ spa hotel"  │               │
│  └─────────────┘     └──────────────────┘     └─────────────┘               │
│         │                      │                     │                      │
│         ▼                      ▼                     ▼                      │
│  ┌─────────────┐     ┌──────────────────┐     ┌─────────────┐               │
│  │Weather Tool │     │ Itinerary Tool   │     │ Hotel Tool  │               │
│  │    Only     │     │     Only         │     │    Only     │               │
│  └─────────────┘     └──────────────────┘     └─────────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Python 3.13 or higher
- pip or uv package manager
- Google ADK package

## Installation & Setup

### 1. Clone/Navigate to Project Directory

```bash
cd "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent"
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Or if using PowerShell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
# Install the project in editable mode (this will install all dependencies)
pip install -e .
```

This will automatically install:
- `google-adk>=1.0.0`
- `google-genai>=1.11.0`
- All other required dependencies

### 4. Verify Installation

Check that the installation was successful:

```bash
pip list | grep google
```

You should see `google-adk` and `google-genai` in the output.

### 5. Verify Agent Structure

Ensure the agent directory exists:

```bash
# Check that the travel_weather_agent directory exists
ls agents/travel_weather_agent/
```

You should see `__init__.py` and `agent.py` files.

## Project Structure

```
google-multi-agent/
├── agents/
│   └── travel_weather_agent/
│       ├── __init__.py
│       ├── agent.py                    # Single Agent Pattern
│       └── multi_agent_system.py       # Multi-Agent Pattern (LlmAgent + sub-agents)
├── main.py                             # Alternative agent entry point
├── pyproject.toml                     # Project configuration
├── README.md                         # This file
└── .venv/                            # Virtual environment
```

## Features

### Single Agent Pattern (`agent.py`)
- **Direct Tool Usage**: Functions called directly by one agent
- **Simple Architecture**: Flat structure, easy to understand
- **Quick Setup**: Minimal configuration required

### Multi-Agent Pattern (`multi_agent_system.py`)
- **Specialist Agents**: Weather specialist, itinerary specialist, hotel specialist
- **Coordinated Workflow**: Master coordinator orchestrates sub-agents
- **Advanced Architecture**: Hierarchical, enterprise-ready structure
- **Scalable Design**: Easy to add new specialist agents

## Running the Agent

The Google ADK provides multiple ways to run and interact with your agent. You can use either pattern:

**Single Agent**: Uses `agent.py` with direct function tools
**Multi-Agent**: Uses `multi_agent_system.py` with specialized sub-agents

### Option 1: Web Interface with UI (Recommended)

**Single Agent Pattern:**
```bash
adk web "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent\agents" --port 8001
# Select "travel_weather_agent" in the UI
```

**Multi-Agent Pattern:**
```bash
# First, update __init__.py to use multi-agent system
# Then run the same command - the coordinator will manage sub-agents automatically
adk web "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent\agents" --port 8001
```

- **Features**: Full web UI, visual interface, easy testing
- **Access**: `http://localhost:8001`
- **Use case**: Development, testing, demos

### Multi-Agent System Usage Examples

**Coordinated Workflow:**
```
User: "Plan a complete trip to Paris"

Coordinator → Weather Specialist: "Get Paris weather"
Weather Specialist → Returns: "Sunny, 22.3°C"

Coordinator → Itinerary Specialist: "Create itinerary for sunny Paris"
Itinerary Specialist → Returns: "Outdoor activities, rooftop dining..."

Coordinator → Hotel Specialist: "Book beachfront resort in Paris"
Hotel Specialist → Returns: "Beachfront Resort booked, HTL-1234"

Coordinator → User: "Complete trip plan with weather, activities, and hotel"
```

**Individual Specialist Access:**
```
User: "What's the weather in Tokyo?"
Coordinator → Weather Specialist → Returns detailed weather info

User: "Book a luxury spa hotel"
Coordinator → Hotel Specialist → Returns booking confirmation
```

### Option 1: Web Interface with UI (Recommended)

**Best for**: Interactive testing, demonstrations, and development

```bash
adk web "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent\agents" --port 8001
```

- **Features**: Full web UI, visual interface, easy testing
- **Access**: `http://localhost:8001`
- **Use case**: Development, testing, demos

### Option 2: API Server (Programmatic Access)

**Best for**: Integration with other applications, API-based interactions

```bash
adk api_server "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent\agents" --port 8002
```

- **Features**: RESTful API endpoints, JSON responses, no UI
- **Access**: `http://localhost:8002` (API endpoints)
- **Use case**: Integration with external systems, automation

#### API Documentation & Endpoints:

**📖 Interactive API Documentation:**
- **Swagger UI**: `http://127.0.0.1:8002/docs` - Interactive API testing interface
- **ReDoc**: `http://127.0.0.1:8002/redoc` - Alternative documentation view
- **OpenAPI Spec**: `http://127.0.0.1:8002/openapi.json` - Raw API specification

**🔧 Available Endpoints:**
```bash
# List all available agents
GET http://127.0.0.1:8002/list-apps
# Returns: ["travel_weather_agent", "weather_themepark_agent"]

# Get agent information
GET http://127.0.0.1:8002/agents/{agent_name}

# Chat with agent (streaming)
POST http://127.0.0.1:8002/chat
Content-Type: application/json
{
  "app_name": "travel_weather_agent",
  "message": "What's the weather in Paris?",
  "session_id": "optional_session_id"
}

# Start new conversation
POST http://127.0.0.1:8002/conversation/start
{
  "app_name": "travel_weather_agent"
}

# Continue conversation
POST http://127.0.0.1:8002/conversation/chat
{
  "conversation_id": "conv_123",
  "message": "Book a hotel in Tokyo"
}
```

**💡 Example API Usage:**
```powershell
# PowerShell example
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8002/list-apps" -Method GET
Write-Output $response

# Chat example
$body = @{
    app_name = "travel_weather_agent"
    message = "Plan a trip to London"
    session_id = "trip_session_1"
} | ConvertTo-Json

$chatResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8002/chat" -Method POST -Body $body -ContentType "application/json"
```

```bash
# Bash/curl examples
# List agents
curl -X GET "http://127.0.0.1:8002/list-apps"

# Chat with agent
curl -X POST "http://127.0.0.1:8002/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "travel_weather_agent",
    "message": "What is the weather in Paris?",
    "session_id": "my_session"
  }'
```

### Option 3: Command Line Interface

**Best for**: Quick testing, scripting, command-line workflows

```bash
adk run "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent\agents\travel_weather_agent"
```

- **Features**: Interactive CLI, session saving, replay functionality
- **Access**: Direct terminal interaction
- **Use case**: Command-line testing, automated scripts

#### CLI Advanced Options:
```bash
# Save session for later review
adk run agents/travel_weather_agent --save_session --session_id "trip_planning_session"

# Resume a previous session
adk run agents/travel_weather_agent --resume session_file.json

# Replay a session automatically
adk run agents/travel_weather_agent --replay test_session.json
```

### Option 4: Create New Projects

**Best for**: Starting new agent projects

```bash
# Create a new agent project
adk create my_new_agent --model "gemini-2.0-flash"

# Create with specific configuration
adk create travel_bot --model "gemini-2.0-flash" --project "my-gcp-project" --region "us-central1"
```

### Option 5: Agent Evaluation

**Best for**: Testing agent performance, quality assurance

```bash
# Run evaluations on your agent
adk eval agents/travel_weather_agent/agent.py eval_set.json

# Run specific evaluations with detailed output
adk eval agents/travel_weather_agent/agent.py eval_set.json:test1,test2,test3 --print_detailed_results
```

### Option 6: Deployment

**Best for**: Production deployment

```bash
# Deploy to Google Cloud Run
adk deploy cloud_run

# Deploy to Agent Engine
adk deploy agent_engine
```

## Command Comparison

| Command | Best For | Features | Access Method | Use Cases |
|---------|----------|----------|---------------|-----------|
| `adk web` | **Development & Demo** | Full web UI, visual interface | Browser (localhost:8001) | Testing, demos, development |
| `adk api_server` | **Integration** | RESTful APIs, JSON responses | HTTP endpoints (localhost:8002) | App integration, automation |
| `adk run` | **CLI Testing** | Interactive CLI, session management | Terminal | Quick testing, scripting |
| `adk create` | **New Projects** | Project templates, scaffolding | File system | Starting new agents |
| `adk eval` | **Quality Assurance** | Performance testing, metrics | Terminal reports | Testing, validation |
| `adk deploy` | **Production** | Cloud deployment, scaling | Cloud platforms | Production hosting |

## Quick Start Examples

### 1. Test Your Agent (Web UI)
```bash
cd "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent"
adk web "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent\agents" --port 8001
# Open http://localhost:8001 in browser
```

### 2. API Integration
```bash
# Start API server
adk api_server "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent\agents" --port 8002

# View API documentation
# Open http://127.0.0.1:8002/docs in browser

# Test with PowerShell
$body = @{
    app_name = "travel_weather_agent"
    message = "Plan a complete trip to Paris"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8002/chat" -Method POST -Body $body -ContentType "application/json"
```

### 3. CLI Testing
```bash
adk run "c:\Workspace\SPR-WS\rntbci_adk_a2a\adk_example\google-multi-agent\agents\travel_weather_agent"
# Interactive chat in terminal
```

## Supported Cities

The agent has hardcoded weather data for the following cities:
- **London**: Partly cloudy, 18.5°C
- **Paris**: Sunny, 22.3°C  
- **New York**: Clear, 25.1°C
- **Tokyo**: Overcast, 19.7°C
- **Sydney**: Light rain, 16.2°C
- **Other cities**: Default to partly cloudy, 20.0°C

## Agent Tools & Capabilities

### 1. Weather Information (`get_weather`)
- Get current weather for any city
- Temperature in both Celsius and Fahrenheit
- Weather conditions description

### 2. Travel Itinerary (`create_travel_itinerary`)
- Weather-based activity recommendations
- Outdoor activities for sunny/clear weather
- Indoor activities for rainy/stormy weather
- Mixed activities for overcast conditions
- Itinerary focus suggestions
- Hotel type recommendations

### 3. Hotel Booking (`book_hotel`)
- Multiple hotel types available:
  - **Beachfront Resort**: Private beach access, outdoor pool, spa services
  - **Luxury Spa Hotel**: Full-service spa, indoor pool, fine dining
  - **City Center Hotel**: Central location, business center, fitness center
  - **Business Hotel**: Meeting rooms, WiFi, airport shuttle
  - **Outdoor Pool Hotel**: Pool, sun deck, poolside service
  - **Boutique Hotel**: Unique design, personalized service, local art
- Detailed amenities and pricing information
- Booking confirmation numbers
- Check-in/check-out details

## Example Interactions

**Getting Weather:**
```
User: "What's the weather like in Paris?"
Agent: "The weather in Paris is Sunny with a temperature of 22.3°C (72.1°F)."
```

**Creating Travel Itinerary:**
```
User: "Create a travel itinerary for London based on the weather"
Agent: "Travel itinerary created for London! Weather: Partly cloudy, 18.5°C. 
        Recommended activities: museum visits, shopping centers, city walking tours, outdoor sightseeing.
        Recommended hotel: city center hotel."
```

**Booking Hotel:**
```
User: "Book a luxury spa hotel in Tokyo"
Agent: "Luxury Spa Hotel successfully booked in Tokyo! 
        Amenities: full-service spa, indoor pool, fine dining, room service.
        Price range: $180-350/night. Booking confirmation: HTL-1234"
```

**Complete Trip Planning:**
```
User: "Plan a complete trip to Paris including weather, itinerary, and hotel"
Agent: [Provides weather → creates sunny weather itinerary → books beachfront resort]
```

## Troubleshooting

### Common Issues

1. **Port 8000 already in use**:
   - Use a different port: `adk web agents --port 8001`

2. **Module not found error**:
   - Ensure you've installed the project: `pip install -e .`
   - Verify virtual environment is activated

3. **Agent not found**:
   - Check the agents directory structure exists
   - Ensure `agent.py` contains the `root_agent` variable

4. **YAML config error**:
   - This project uses Python-based configuration, not YAML
   - Ensure you're using the correct directory structure

### Getting Help

- Check ADK commands: `adk --help`
- Web server options: `adk web --help`
- CLI options: `adk run --help`

## Development

### Adding New Cities

Edit the `hardcoded_weather_data` dictionary in `agents/travel_weather_agent/agent.py`:

```python
hardcoded_weather_data = {
    "your_city": {"weather": "sunny", "temp_c": 25.0},
    # ... existing cities
}
```

### Adding New Hotel Types

Add new hotel options to the `hotel_options` dictionary in the `book_hotel` function:

```python
hotel_options = {
    "your_hotel_type": {
        "amenities": ["feature1", "feature2", "feature3"],
        "price_range": "$price_range/night"
    },
    # ... existing hotels
}
```

### Customizing Activity Recommendations

Modify the activity lists in the `create_travel_itinerary` function:

```python
outdoor_activities = ["new_activity", "another_activity", ...]
indoor_activities = ["indoor_activity1", "indoor_activity2", ...]
```

### Customizing the Agent

Modify the agent configuration in `agent.py`:
- Change the model: `model="gemini-2.0-flash"`
- Update instructions and descriptions
- Add new tools/functions to the tools list: `tools=[get_weather, create_travel_itinerary, book_hotel, your_new_tool]`

### Tool Usage Patterns

The agent supports various usage patterns:
1. **Sequential**: Weather → Itinerary → Hotel booking
2. **Individual**: Use any tool independently
3. **Conditional**: Create itinerary based on weather, then book appropriate hotel
4. **Comprehensive**: Complete trip planning in one conversation

## License

This project is part of the Google ADK examples and follows the same licensing terms.