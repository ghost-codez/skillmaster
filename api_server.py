"""
FastAPI Backend for SkillMaster
Connects the frontend to the PocketFlow-style workflow engine
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

# Import the workflow engine from skillmaster-demo.py
from dataclasses import dataclass
import openai

# Load environment variables
load_dotenv()

app = FastAPI(
    title="SkillMaster API",
    description="AI-powered skill breakdown and feedback system",
    version="1.0.0"
)

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Data Models (Pydantic)
# ============================================================================

class SkillAnalysisRequest(BaseModel):
    skill_name: str
    proficiency_level: str = "Beginner"

class Distinction(BaseModel):
    name: str
    description: str
    importance: str
    current_level: str

class NextStep(BaseModel):
    action: str
    time_commitment: str
    success_criteria: str
    develops: List[str]

class Source(BaseModel):
    title: str
    url: str

class SkillAnalysisResponse(BaseModel):
    skill_name: str
    proficiency_level: str
    distinctions: List[Distinction]
    insights: List[str]
    next_steps: List[NextStep]
    sources: List[Source]
    related_questions: List[str]

# ============================================================================
# Workflow Engine (from skillmaster-demo.py)
# ============================================================================

@dataclass
class WorkflowContext:
    """Shared context passed between workflow nodes"""
    skill_name: str
    proficiency_level: str
    distinctions: Optional[List[Dict[str, Any]]] = None
    insights: Optional[List[str]] = None
    next_steps: Optional[List[Dict[str, Any]]] = None

class WorkflowNode:
    """Base class for workflow nodes"""
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        raise NotImplementedError()

class SkillAnalysisNode(WorkflowNode):
    """Node 1: Analyze skill and identify key distinctions"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        prompt = f"""Analyze the skill "{context.skill_name}" for someone at the {context.proficiency_level} level.

Identify 5 key distinctions (sub-skills or components) that make up this skill.

For each distinction, provide:
1. Name (concise, 2-4 words)
2. Description (one sentence explaining what it is)
3. Importance (why it matters for this skill)
4. Current level assessment for a {context.proficiency_level}

Return ONLY valid JSON in this exact format:
{{
  "distinctions": [
    {{
      "name": "string",
      "description": "string",
      "importance": "string",
      "current_level": "Beginner|Intermediate|Advanced"
    }}
  ]
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        import json
        content = response.choices[0].message.content.strip()
        
        # Handle markdown-wrapped JSON
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        result = json.loads(content)
        context.distinctions = result["distinctions"]
        return context

class InsightGenerationNode(WorkflowNode):
    """Node 2: Generate actionable insights"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        distinctions_text = "\n".join([
            f"- {d['name']}: {d['description']}"
            for d in context.distinctions
        ])
        
        prompt = f"""Based on these distinctions for {context.skill_name} at {context.proficiency_level} level:

{distinctions_text}

Generate 4 actionable insights or strategic recommendations for learning this skill effectively.

Return ONLY valid JSON:
{{
  "insights": ["insight1", "insight2", "insight3", "insight4"]
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        import json
        content = response.choices[0].message.content.strip()
        
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        result = json.loads(content)
        context.insights = result["insights"]
        return context

class NextStepsNode(WorkflowNode):
    """Node 3: Create personalized next steps"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        distinctions_text = "\n".join([
            f"- {d['name']}"
            for d in context.distinctions
        ])
        
        prompt = f"""Create 3 specific, actionable next steps for developing {context.skill_name} at {context.proficiency_level} level.

Available distinctions to develop:
{distinctions_text}

For each step provide:
1. Action (specific practice or exercise)
2. Time commitment (e.g., "10 minutes daily")
3. Success criteria (how to know you've succeeded)
4. Develops (list of distinction names this step improves)

Return ONLY valid JSON:
{{
  "next_steps": [
    {{
      "action": "string",
      "time_commitment": "string",
      "success_criteria": "string",
      "develops": ["distinction1", "distinction2"]
    }}
  ]
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        import json
        content = response.choices[0].message.content.strip()
        
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        result = json.loads(content)
        context.next_steps = result["next_steps"]
        return context

class Workflow:
    """Workflow orchestrator"""
    
    def __init__(self):
        self.nodes: List[WorkflowNode] = []
    
    def add_node(self, node: WorkflowNode) -> 'Workflow':
        self.nodes.append(node)
        return self
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        for node in self.nodes:
            context = node.execute(context)
        return context

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "SkillMaster API",
        "version": "1.0.0"
    }

@app.post("/api/analyze", response_model=SkillAnalysisResponse)
async def analyze_skill(request: SkillAnalysisRequest):
    """
    Analyze a skill and return comprehensive breakdown
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in .env file"
        )
    
    try:
        # Create workflow
        workflow = Workflow()
        workflow.add_node(SkillAnalysisNode(api_key))
        workflow.add_node(InsightGenerationNode(api_key))
        workflow.add_node(NextStepsNode(api_key))
        
        # Execute workflow
        context = WorkflowContext(
            skill_name=request.skill_name,
            proficiency_level=request.proficiency_level
        )
        
        result = workflow.execute(context)
        
        # Generate related questions (mock for now, could be AI-generated)
        related_questions = [
            f"How long does it typically take to master {request.skill_name}?",
            f"What are common mistakes beginners make in {request.skill_name}?",
            f"How can I practice {request.skill_name} effectively?",
            f"What resources are best for learning {request.skill_name}?"
        ]
        
        # Generate sources (mock for now)
        sources = [
            {"title": "Skilled Success Methodology", "url": "#"},
            {"title": "Deliberate Practice Research", "url": "#"},
            {"title": "Cognitive Load Theory", "url": "#"}
        ]
        
        return SkillAnalysisResponse(
            skill_name=result.skill_name,
            proficiency_level=result.proficiency_level,
            distinctions=result.distinctions,
            insights=result.insights,
            next_steps=result.next_steps,
            sources=sources,
            related_questions=related_questions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

