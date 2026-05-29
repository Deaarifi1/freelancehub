from openai import OpenAI
from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.freelancer import FreelancerProfile
from app.models.ai_match import AIMatch
from app.models.skill import FreelancerSkill, Skill
from app.config import settings
import json

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def match_freelancers(
        self, 
        project: Project, 
        freelancers: list,
        db: Session
    ) -> list:
        """
        Analyzes the project and finds the best freelancers
        """
        # Prepare data for Ai
        project_data = {
            "title": project.title,
            "description": project.description,
            "budget": f"{project.budget_min}-{project.budget_max}",
        }
        
        freelancer_data = []
        for f in freelancers:
            skills = db.query(Skill).join(FreelancerSkill).filter(
                FreelancerSkill.freelancer_id == f.id
            ).all()
            freelancer_data.append (
                {
                "id": f.id,
                "bio": f.bio or "",
                "hourly_rate": f.hourly_rate or 0,
                "skills": [s.name for s in skills],
                "rating": f.average_rating,
                "experience_years": f.experience_years
                }
            )
        
        prompt = f"""
        Analyze your project and find 3 best freelancers.
        
        PROJECT:
        {json.dumps(project_data, ensure_ascii=False, indent=2)}
        
        AVAILABLE FREELANCERS:
        {json.dumps(freelancer_data, ensure_ascii=False, indent=2)}
        
        Return only JSON:
        {{
            "matches": [
                {{
                    "freelancer_id": <id>,
                    "score": <0-100>,
                    "reason": "<reason>"
                }}
            ]
        }}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in recruiting freelancers. Return ONLY valid JSON."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # save the results in database
        for match in result["matches"]:
            existing = db.query(AIMatch).filter(
                AIMatch.project_id == project.id,
                AIMatch.freelancer_id == match["freelancer_id"]
            ).first()

            if existing:
                existing.score = match["score"]
                existing.reason = match["reason"]
            else:
                ai_match = AIMatch(
                    project_id=project.id,
                    freelancer_id=match["freelancer_id"],
                    score=match["score"],
                    reason=match["reason"]
                )
                db.add(ai_match)

        db.commit()
        return result["matches"]
    
    def analyze_project(self, description: str) -> dict:
        """Analyzes the project and suggests skills and budget - Mock Response."""
        return {
            "skills": ["React", "Node.js", "PostgreSQL"],
            "budget_range": {"min": 1000, "max": 5000},
            "complexity": "medium",
            "estimated_duration": "4-6 weeks"
        }

ai_service = AIService()