# SkillMaster 🎓

An AI-powered skill breakdown and feedback system based on PocketFlow (agent-graph workflows) and the "Skilled Success" research methodology.

## Overview

SkillMaster helps you develop any skill by:
- **Breaking down skills** into key distinctions (fundamental components)
- **Generating actionable insights** based on your proficiency level
- **Creating personalized next steps** for deliberate practice
- **Tracking progress** through structured feedback loops

## ✨ Features

### 🎨 Perplexity-Inspired UI
- ✅ **Dark minimalist design** with teal accents (#20808d)
- ✅ **Search-first interface** - centered search that transitions to top on results
- ✅ **Sources section** with numbered reference badges
- ✅ **Related questions** for deeper exploration
- ✅ **Smooth animations** and progress indicators
- ✅ **Responsive design** for mobile and desktop

### 🤖 AI-Powered Analysis
- ✅ **PocketFlow-style Workflow Engine**: Modular agent graph with composable nodes
- ✅ **Skill Breakdown**: Identifies 5 key distinctions per skill
- ✅ **Personalized Insights**: 4 strategic recommendations based on proficiency
- ✅ **Action Plans**: 3 specific next steps with time commitments
- ✅ **OpenAI Integration**: Uses GPT-4o-mini for intelligent analysis

### 💾 Interactive Features
- ✅ **Save Analysis**: Persist to browser localStorage
- ✅ **Export JSON**: Download complete analysis data
- ✅ **Share Results**: Web Share API with clipboard fallback
- ✅ **Print/PDF**: Clean print-friendly layout
- ✅ **Mock/Live Toggle**: Switch between demo and real API

### 🏗️ Full Stack Architecture
- ✅ **Frontend**: Vanilla JavaScript (no dependencies)
- ✅ **Backend**: FastAPI with CORS support
- ✅ **CLI Tool**: Python command-line interface
- ✅ **REST API**: Auto-generated OpenAPI docs
- ✅ **JSON Export**: Structured data output

## 🚀 Quick Start

**📖 See [QUICKSTART.md](QUICKSTART.md) for detailed instructions!**

### Option 1: Try the UI (No Setup Required)

```bash
open skillmaster-demo.html
```

Uses mock data - perfect for exploring the interface!

### Option 2: Full Stack (Real AI)

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up API key**:
```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here
```

3. **Start the API server**:
```bash
python api_server.py
```

4. **Open the UI and toggle "Live API"**:
```bash
open skillmaster-demo.html
```

### Option 3: CLI Only

```bash
python skillmaster-demo.py
```

---

## 📁 Project Structure

```
SkillMaster2/
├── skillmaster-demo.html    # Perplexity-style web interface
├── skillmaster-demo.py       # CLI tool with workflow engine
├── api_server.py             # FastAPI backend
├── test_api.py               # API test suite
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── QUICKSTART.md             # Detailed setup guide
└── README.md                 # This file
```

---

## 🎯 Usage Examples

### Web Interface

1. Open `skillmaster-demo.html`
2. Enter a skill (e.g., "Guitar Playing")
3. Select proficiency level
4. Click "Analyze →"
5. Explore results with sources and related questions
6. Save, export, or share your analysis

### API Endpoint

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "Public Speaking",
    "proficiency_level": "Beginner"
  }'
```

### CLI Tool

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Running the CLI Demo

```bash
python skillmaster-demo.py
```

Follow the prompts to:
1. Enter a skill you want to develop (e.g., "Public Speaking", "Python Programming")
2. Select your current proficiency level (Beginner/Intermediate/Advanced)
3. Review the AI-generated analysis, insights, and next steps
4. Optionally save results to a JSON file

### Viewing the Web Demo

Simply open `skillmaster-demo.html` in your web browser. No server required!

The demo includes:
- Interactive skill input form
- Workflow visualization
- Mock data for "Public Speaking" skill
- Responsive design for mobile and desktop

## Architecture

### PocketFlow-Style Workflow Pattern

SkillMaster uses a modular agent graph architecture:

```
WorkflowContext (shared state)
    ↓
SkillAnalysisNode → InsightGenerationNode → NextStepsNode
    ↓                      ↓                        ↓
Distinctions          Insights              Next Steps
```

### Core Components

#### 1. **WorkflowContext**
- Shared state object passed between nodes
- Contains skill name, proficiency level, and analysis results
- Immutable pattern for predictable state management

#### 2. **WorkflowNode** (Base Class)
- Abstract base for all workflow nodes
- Implements `execute()` method for node logic
- Includes status tracking (PENDING, RUNNING, COMPLETED, FAILED)

#### 3. **Workflow** (Orchestrator)
- Manages node execution sequence
- Builder pattern for composing workflows
- Error handling and logging

#### 4. **Specialized Nodes**
- **SkillAnalysisNode**: Breaks skills into 5-7 key distinctions
- **InsightGenerationNode**: Creates actionable learning strategies
- **NextStepsNode**: Generates specific practice recommendations

## Project Structure

```
SkillMaster2/
├── skillmaster-demo.py      # Python CLI with AI workflow
├── skillmaster-demo.html    # Standalone web demo
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Extending the System

### Adding New Workflow Nodes

Create a new node by extending `WorkflowNode`:

```python
class MyCustomNode(WorkflowNode):
    def __init__(self, api_key: str):
        super().__init__("My Custom Node")
        self.client = openai.OpenAI(api_key=api_key)
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        # Your custom logic here
        # Modify and return the context
        return context
```

Add it to the workflow:

```python
workflow = (Workflow("Custom Workflow")
            .add_node(SkillAnalysisNode(api_key))
            .add_node(MyCustomNode(api_key))  # Add your node
            .add_node(NextStepsNode(api_key)))
```

### Example Extensions

#### 1. **Experiment Logger Node**
```python
class ExperimentLoggerNode(WorkflowNode):
    """Logs practice experiments and outcomes"""
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        # Prompt user to log practice session
        # Store in context.metadata['experiments']
        return context
```

#### 2. **Progress Tracker Node**
```python
class ProgressTrackerNode(WorkflowNode):
    """Compares current vs. previous assessments"""
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        # Load previous analysis from file
        # Compare distinctions and levels
        # Add progress metrics to context
        return context
```

#### 3. **Feedback Loop Node**
```python
class FeedbackLoopNode(WorkflowNode):
    """Refines recommendations based on practice results"""
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        # Analyze what worked/didn't work
        # Adjust next steps accordingly
        return context
```

## Frontend-Backend Integration Plan

### Recommended Approach: FastAPI + REST API

**Why FastAPI?**
- Modern, fast, and easy to use
- Automatic API documentation (Swagger UI)
- Built-in async support for scalability
- Type hints and validation with Pydantic

**Implementation Steps:**

1. **Create API Server** (`api_server.py`):
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SkillRequest(BaseModel):
    skill_name: str
    proficiency_level: str

@app.post("/api/analyze")
async def analyze_skill(request: SkillRequest):
    # Run workflow
    # Return results as JSON
    pass
```

2. **Update HTML to Call API**:
```javascript
async function analyzeSkill() {
    const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            skill_name: skillName,
            proficiency_level: proficiencyLevel
        })
    });
    const data = await response.json();
    displayResults(data);
}
```

3. **Run the Server**:
```bash
pip install fastapi uvicorn
uvicorn api_server:app --reload
```

### Alternative: WebSocket for Real-Time Updates

For streaming node execution updates:
```python
@app.websocket("/ws/analyze")
async def websocket_analyze(websocket: WebSocket):
    await websocket.accept()
    # Stream node completion events
    # Update frontend in real-time
```

## Development Best Practices

### Code Quality
- ✅ Type hints for better IDE support
- ✅ Docstrings for all classes and methods
- ✅ Dataclasses for structured data
- ✅ Enum for status tracking
- ✅ Error handling with try/except

### Testing Strategy
```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v --cov=skillmaster
```

### Virtual Environment Management
```bash
# Create environment
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Deactivate
deactivate
```

### Dependency Management
```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt
```

## Deployment Options

### Option 1: Local Development
- Run CLI directly: `python skillmaster-demo.py`
- Open HTML file in browser

### Option 2: Web Server (Future)
```bash
# Install FastAPI
pip install fastapi uvicorn

# Run server
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### Option 3: Docker (Future)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "skillmaster-demo.py"]
```

## Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
- Ensure `.env` file exists in the project root
- Check that the API key is correctly formatted
- Verify the file is named `.env` (not `.env.txt`)

**"Module not found" errors**
- Activate your virtual environment
- Run `pip install -r requirements.txt`

**JSON parsing errors**
- OpenAI occasionally returns markdown-wrapped JSON
- The code handles this automatically
- If issues persist, check your API key quota

**Rate limiting**
- OpenAI has rate limits on API calls
- Add delays between requests if needed
- Consider upgrading your OpenAI plan

## Contributing

This is a rapid prototype. Future improvements welcome:
- Database integration (SQLite, PostgreSQL, Supabase)
- User authentication and profiles
- Enhanced UI with React/Vue/Svelte
- Mobile app (React Native, Flutter)
- Advanced analytics and visualizations
- Multi-language support

## License

MIT License - feel free to use and modify for your projects.

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PocketFlow Concepts](https://github.com/pocketflow)
- "Skilled Success" Research Methodology

## Support

For questions or issues:
1. Check this README
2. Review the code comments
3. Test with the HTML demo first
4. Verify your OpenAI API key is valid

---

**Built with ❤️ for deliberate skill development**

