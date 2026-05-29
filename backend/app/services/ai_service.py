from groq import Groq
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.ai_match import AIMatch
from app.models.skill import FreelancerSkill, Skill
from app.config import settings
import json

class AIService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    async def match_freelancers(
        self,
        project: Project,
        freelancers: list,
        db: Session
    ) -> list:
        """Analyzes the project and finds the best freelancers."""
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
            freelancer_data.append({
                "id": f.id,
                "bio": f.bio or "",
                "hourly_rate": f.hourly_rate or 0,
                "skills": [s.name for s in skills],
                "rating": f.average_rating,
                "experience_years": f.experience_years
            })

        prompt = f"""
        Analyze this project and find 3 best freelancers.
        
        PROJECT:
        {json.dumps(project_data, indent=2)}
        
        FREELANCERS:
        {json.dumps(freelancer_data, indent=2)}
        
        Return ONLY this JSON:
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
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a freelancer recruiting expert. Return ONLY valid JSON."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

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
        """Analyzes the project and suggests skills and budget."""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze freelance projects. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": f"""Analyze: {description}
                    
                    Return this JSON:
                    {{
                        "skills": ["skill1", "skill2"],
                        "budget_range": {{"min": 0, "max": 0}},
                        "complexity": "low|medium|high",
                        "estimated_duration": "X weeks"
                    }}"""
                }
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

ai_service = AIService()