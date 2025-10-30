#!/usr/bin/env python3
"""
SkillMaster Demo - AI-Powered Skill Breakdown and Feedback System

A PocketFlow-style workflow implementation for analyzing skills,
breaking them down into actionable distinctions, and providing
personalized feedback based on the "Skilled Success" methodology.
"""

import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import openai
from dotenv import load_dotenv


# ============================================================================
# Core Workflow Framework (PocketFlow-style)
# ============================================================================

class NodeStatus(Enum):
    """Status of a workflow node execution"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkflowContext:
    """Shared context passed between workflow nodes"""
    skill_name: str
    proficiency_level: str
    distinctions: Optional[List[Dict[str, Any]]] = None
    insights: Optional[List[str]] = None
    next_steps: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary"""
        return asdict(self)


class WorkflowNode:
    """Base class for workflow nodes in the agent graph"""
    
    def __init__(self, name: str):
        self.name = name
        self.status = NodeStatus.PENDING
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        """
        Execute the node's logic and return updated context
        
        Args:
            context: Current workflow context
            
        Returns:
            Updated workflow context
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def run(self, context: WorkflowContext) -> WorkflowContext:
        """
        Run the node with status tracking
        
        Args:
            context: Current workflow context
            
        Returns:
            Updated workflow context
        """
        print(f"\n{'='*60}")
        print(f"🔄 Executing Node: {self.name}")
        print(f"{'='*60}")
        
        self.status = NodeStatus.RUNNING
        try:
            updated_context = self.execute(context)
            self.status = NodeStatus.COMPLETED
            print(f"✅ Node '{self.name}' completed successfully")
            return updated_context
        except Exception as e:
            self.status = NodeStatus.FAILED
            print(f"❌ Node '{self.name}' failed: {str(e)}")
            raise


class Workflow:
    """Agent graph workflow composed of multiple nodes"""
    
    def __init__(self, name: str):
        self.name = name
        self.nodes: List[WorkflowNode] = []
    
    def add_node(self, node: WorkflowNode) -> 'Workflow':
        """Add a node to the workflow (builder pattern)"""
        self.nodes.append(node)
        return self
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        """
        Execute all nodes in sequence
        
        Args:
            context: Initial workflow context
            
        Returns:
            Final workflow context after all nodes
        """
        print(f"\n{'#'*60}")
        print(f"🚀 Starting Workflow: {self.name}")
        print(f"{'#'*60}")
        
        current_context = context
        for node in self.nodes:
            current_context = node.run(current_context)
        
        print(f"\n{'#'*60}")
        print(f"🎉 Workflow '{self.name}' completed successfully!")
        print(f"{'#'*60}\n")
        
        return current_context


# ============================================================================
# AI-Powered Workflow Nodes
# ============================================================================

class SkillAnalysisNode(WorkflowNode):
    """Analyzes a skill and breaks it down into key distinctions"""
    
    def __init__(self, api_key: str):
        super().__init__("Skill Analysis")
        self.client = openai.OpenAI(api_key=api_key)
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        """Analyze skill and extract distinctions"""
        
        prompt = f"""You are an expert skill coach using the "Skilled Success" methodology.

Analyze the skill: "{context.skill_name}"
Current proficiency level: {context.proficiency_level}

Break down this skill into 5-7 key distinctions (fundamental components or sub-skills).
Each distinction should be:
1. Specific and actionable
2. Measurable or observable
3. Progressive (can be improved incrementally)

Return your response as a JSON array of objects with this structure:
[
  {{
    "name": "Distinction name",
    "description": "Brief description",
    "importance": "Why this matters",
    "current_level": "Beginner/Intermediate/Advanced"
  }}
]

Only return the JSON array, no additional text."""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a skill analysis expert. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        distinctions_text = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        if distinctions_text.startswith("```"):
            distinctions_text = distinctions_text.split("```")[1]
            if distinctions_text.startswith("json"):
                distinctions_text = distinctions_text[4:]
        
        distinctions = json.loads(distinctions_text)
        context.distinctions = distinctions
        
        print(f"\n📊 Identified {len(distinctions)} key distinctions:")
        for i, dist in enumerate(distinctions, 1):
            print(f"  {i}. {dist['name']}")
        
        return context


class InsightGenerationNode(WorkflowNode):
    """Generates actionable insights based on skill analysis"""
    
    def __init__(self, api_key: str):
        super().__init__("Insight Generation")
        self.client = openai.OpenAI(api_key=api_key)
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        """Generate personalized insights"""
        
        distinctions_summary = "\n".join([
            f"- {d['name']}: {d['description']}"
            for d in context.distinctions
        ])
        
        prompt = f"""Based on this skill analysis:

Skill: {context.skill_name}
Proficiency: {context.proficiency_level}

Key Distinctions:
{distinctions_summary}

Generate 3-5 actionable insights for someone at the {context.proficiency_level} level.
Each insight should:
1. Be specific and practical
2. Connect to one or more distinctions
3. Provide a clear learning principle or strategy

Return as a JSON array of strings. Only return the JSON array, no additional text."""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a learning coach. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        insights_text = response.choices[0].message.content.strip()
        if insights_text.startswith("```"):
            insights_text = insights_text.split("```")[1]
            if insights_text.startswith("json"):
                insights_text = insights_text[4:]
        
        insights = json.loads(insights_text)
        context.insights = insights
        
        print(f"\n💡 Generated {len(insights)} insights")
        
        return context


class NextStepsNode(WorkflowNode):
    """Generates specific next steps and practice recommendations"""
    
    def __init__(self, api_key: str):
        super().__init__("Next Steps Generation")
        self.client = openai.OpenAI(api_key=api_key)
    
    def execute(self, context: WorkflowContext) -> WorkflowContext:
        """Generate next steps"""
        
        prompt = f"""Based on this skill development plan:

Skill: {context.skill_name}
Proficiency: {context.proficiency_level}
Number of distinctions identified: {len(context.distinctions)}

Create 3-5 specific next steps for practice and improvement.
Each step should include:
1. A clear action to take
2. Expected time commitment
3. Success criteria (how to know you've completed it)
4. Which distinction(s) it develops

Return as a JSON array of objects:
[
  {{
    "action": "Specific action to take",
    "time_commitment": "e.g., 15 minutes daily",
    "success_criteria": "How to measure completion",
    "develops": ["Distinction 1", "Distinction 2"]
  }}
]

Only return the JSON array, no additional text."""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a practice coach. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        steps_text = response.choices[0].message.content.strip()
        if steps_text.startswith("```"):
            steps_text = steps_text.split("```")[1]
            if steps_text.startswith("json"):
                steps_text = steps_text[4:]
        
        next_steps = json.loads(steps_text)
        context.next_steps = next_steps
        
        print(f"\n📋 Generated {len(next_steps)} next steps")
        
        return context


# ============================================================================
# Main Application
# ============================================================================

def display_results(context: WorkflowContext):
    """Display the final results in a formatted way"""
    
    print("\n" + "="*60)
    print("📚 SKILL ANALYSIS RESULTS")
    print("="*60)
    
    print(f"\n🎯 Skill: {context.skill_name}")
    print(f"📊 Current Level: {context.proficiency_level}")
    
    print("\n" + "-"*60)
    print("🔍 KEY DISTINCTIONS")
    print("-"*60)
    for i, dist in enumerate(context.distinctions, 1):
        print(f"\n{i}. {dist['name']}")
        print(f"   Description: {dist['description']}")
        print(f"   Importance: {dist['importance']}")
        print(f"   Your Level: {dist['current_level']}")
    
    print("\n" + "-"*60)
    print("💡 ACTIONABLE INSIGHTS")
    print("-"*60)
    for i, insight in enumerate(context.insights, 1):
        print(f"\n{i}. {insight}")
    
    print("\n" + "-"*60)
    print("📋 NEXT STEPS")
    print("-"*60)
    for i, step in enumerate(context.next_steps, 1):
        print(f"\n{i}. {step['action']}")
        print(f"   ⏱️  Time: {step['time_commitment']}")
        print(f"   ✅ Success: {step['success_criteria']}")
        print(f"   🎯 Develops: {', '.join(step['develops'])}")
    
    print("\n" + "="*60 + "\n")


def main():
    """Main application entry point"""
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        return
    
    # Welcome message
    print("\n" + "="*60)
    print("🎓 Welcome to SkillMaster - AI-Powered Skill Development")
    print("="*60)
    
    # Get user input
    skill_name = input("\n📝 Enter the skill you want to develop: ").strip()
    
    print("\nProficiency levels:")
    print("  1. Beginner")
    print("  2. Intermediate")
    print("  3. Advanced")
    level_choice = input("\n📊 Select your current level (1-3): ").strip()
    
    level_map = {"1": "Beginner", "2": "Intermediate", "3": "Advanced"}
    proficiency_level = level_map.get(level_choice, "Beginner")
    
    # Create workflow context
    context = WorkflowContext(
        skill_name=skill_name,
        proficiency_level=proficiency_level
    )
    
    # Build and execute workflow
    workflow = (Workflow("Skill Analysis Workflow")
                .add_node(SkillAnalysisNode(api_key))
                .add_node(InsightGenerationNode(api_key))
                .add_node(NextStepsNode(api_key)))
    
    try:
        final_context = workflow.execute(context)
        display_results(final_context)
        
        # Optional: Save results
        save = input("💾 Save results to JSON file? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"skillmaster_{skill_name.replace(' ', '_').lower()}.json"
            with open(filename, 'w') as f:
                json.dump(final_context.to_dict(), f, indent=2)
            print(f"✅ Results saved to {filename}")
    
    except Exception as e:
        print(f"\n❌ Error during workflow execution: {str(e)}")
        return


if __name__ == "__main__":
    main()

