# SkillMaster Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key (for live AI analysis)
- Modern web browser

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

---

## 📱 Usage Options

### Option 1: Frontend Only (Mock Data)
**Perfect for testing the UI without API costs**

1. Open `skillmaster-demo.html` in your browser:
```bash
open skillmaster-demo.html
```

2. The interface will use mock data by default
3. Try analyzing "Public Speaking" to see the demo

**Features:**
- ✅ Full Perplexity-style UI
- ✅ Sources, related questions
- ✅ Save, export, share functionality
- ✅ No API key required
- ❌ Uses pre-defined mock data only

---

### Option 2: CLI Tool (Real AI)
**Command-line interface with real OpenAI analysis**

1. Make sure your `.env` file has your OpenAI API key

2. Run the CLI:
```bash
python skillmaster-demo.py
```

3. Follow the prompts:
```
Enter the skill you want to develop: Guitar Playing
Enter your current proficiency level (Beginner/Intermediate/Advanced): Beginner
```

4. Results are saved to `skill_analysis_TIMESTAMP.json`

**Features:**
- ✅ Real AI-powered analysis
- ✅ Workflow visualization
- ✅ JSON export
- ❌ No web interface

---

### Option 3: Full Stack (Frontend + Backend)
**Complete system with live AI analysis in the web UI**

#### Step 1: Start the API Server

```bash
python api_server.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### Step 2: Test the API

Open another terminal and test:
```bash
curl http://localhost:8000/
```

Should return:
```json
{
  "status": "online",
  "service": "SkillMaster API",
  "version": "1.0.0"
}
```

#### Step 3: Open the Frontend

```bash
open skillmaster-demo.html
```

#### Step 4: Enable Live API

In the web interface:
1. Toggle the checkbox in the top-right corner from "Mock Data" to "Live API"
2. Enter a skill name
3. Click "Analyze →"
4. Watch the real AI analysis happen!

**Features:**
- ✅ Full Perplexity-style UI
- ✅ Real AI-powered analysis
- ✅ Sources, related questions
- ✅ Save, export, share functionality
- ✅ RESTful API
- ✅ CORS enabled for local development

---

## 🎯 Feature Guide

### Interactive Features

#### 💾 Save Analysis
- Saves to browser's localStorage
- Persists across sessions
- Access via browser DevTools → Application → Local Storage

#### 📄 Export JSON
- Downloads complete analysis as JSON file
- Includes timestamp and all data
- Can be imported into other tools

#### 🔗 Share
- Uses native Web Share API (mobile)
- Falls back to clipboard copy (desktop)
- Shares link + description

#### 🖨️ Print
- Opens browser print dialog
- Clean, print-friendly layout
- Save as PDF option

#### 💭 Related Questions
- Click any question to see what would happen
- In full version, triggers new analysis
- Contextual to the analyzed skill

---

## 🏗️ Architecture

### Frontend (skillmaster-demo.html)
- **Framework:** Vanilla JavaScript (no dependencies)
- **Style:** Perplexity-inspired dark theme
- **Features:** 
  - Responsive design
  - Smooth animations
  - Progress indicators
  - Mock/Live API toggle

### Backend (api_server.py)
- **Framework:** FastAPI
- **AI:** OpenAI GPT-4o-mini
- **Architecture:** PocketFlow-style workflow nodes
- **Endpoints:**
  - `GET /` - Health check
  - `POST /api/analyze` - Skill analysis

### CLI (skillmaster-demo.py)
- **Framework:** Pure Python
- **AI:** OpenAI GPT-4o-mini
- **Output:** Console + JSON file

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
OPENAI_API_KEY=sk-your-key-here
```

### API Configuration (in HTML)
```javascript
const API_BASE_URL = 'http://localhost:8000';
const USE_MOCK_DATA = true; // Toggle in UI or change default
```

### Mock Data
Edit the `mockData` object in `skillmaster-demo.html` to add more skills:
```javascript
const mockData = {
    "Your Skill": {
        distinctions: [...],
        insights: [...],
        next_steps: [...],
        sources: [...],
        relatedQuestions: [...]
    }
};
```

---

## 🐛 Troubleshooting

### "OpenAI API key not configured"
- Make sure `.env` file exists in the project root
- Check that `OPENAI_API_KEY` is set correctly
- Restart the API server after changing `.env`

### "Failed to fetch" or CORS errors
- Make sure API server is running (`python api_server.py`)
- Check that you're using `http://localhost:8000` not `https://`
- Verify the toggle is set to "Live API"

### Mock data not showing
- Make sure the skill name matches exactly (case-sensitive)
- Default fallback is "Public Speaking"
- Check browser console for errors (F12)

### API server won't start
- Check if port 8000 is already in use
- Try: `lsof -ti:8000 | xargs kill` (Mac/Linux)
- Or change port in `api_server.py`: `uvicorn.run(app, port=8001)`

---

## 📊 API Documentation

Once the server is running, visit:
- **Interactive docs:** http://localhost:8000/docs
- **OpenAPI schema:** http://localhost:8000/openapi.json

### Example API Request

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "Python Programming",
    "proficiency_level": "Intermediate"
  }'
```

### Example Response

```json
{
  "skill_name": "Python Programming",
  "proficiency_level": "Intermediate",
  "distinctions": [
    {
      "name": "Data Structures",
      "description": "Understanding lists, dicts, sets, tuples",
      "importance": "Foundation for efficient code",
      "current_level": "Intermediate"
    }
  ],
  "insights": ["..."],
  "next_steps": [{...}],
  "sources": [{...}],
  "related_questions": ["..."]
}
```

---

## 🚢 Deployment

### Deploy Backend (FastAPI)

**Option 1: Railway**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Option 2: Render**
1. Push code to GitHub
2. Connect Render to your repo
3. Add `OPENAI_API_KEY` environment variable
4. Deploy!

**Option 3: Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploy Frontend

**Option 1: Netlify/Vercel**
1. Drag and drop `skillmaster-demo.html`
2. Update `API_BASE_URL` to your deployed backend
3. Done!

**Option 2: GitHub Pages**
1. Push to GitHub
2. Enable Pages in repo settings
3. Update `API_BASE_URL`

---

## 🎓 Next Steps

1. **Test with different skills** - Try "Guitar", "Cooking", "Leadership"
2. **Customize the UI** - Edit colors, fonts, layout in the `<style>` section
3. **Add more workflow nodes** - Extend the analysis with new capabilities
4. **Integrate a database** - Store analyses in PostgreSQL/MongoDB
5. **Add authentication** - Protect the API with JWT tokens
6. **Build a mobile app** - Use the API with React Native/Flutter

---

## 📚 Resources

- **OpenAI API Docs:** https://platform.openai.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **PocketFlow Concept:** Agent-graph workflow architecture
- **Skilled Success:** Research-based skill development methodology

---

## 💡 Tips

- Start with mock data to design your UI
- Use the CLI for quick testing without the frontend
- Monitor API costs in OpenAI dashboard
- Export analyses to build a personal skill library
- Share results with mentors or study groups

---

**Happy Learning! 🚀**

