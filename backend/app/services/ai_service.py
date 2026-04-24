from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.freelancer import FreelancerProfile
from app.models.ai_match import AIMatch
from app.config import settings
import json

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def match_freelancers(
        self, 
        project: Project, 
        freelancers: list[FreelancerProfile],
        db: Session
    ) -> list[dict]:
        """
        Analizon projektin dhe gjen freelancerët më të përshtatshëm.
        """
        # Përgatit të dhënat për AI
        project_data = {
            "title": project.title,
            "description": project.description,
            "budget": f"{project.budget_min}-{project.budget_max}",
            "required_skills": [ps.skill.name for ps in project.required_skills]
        }
        
        freelancer_data = [
            {
                "id": f.id,
                "name": f.user.username,
                "bio": f.bio,
                "hourly_rate": f.hourly_rate,
                "skills": [fs.skill.name for fs in f.skills],
                "rating": f.average_rating
            }
            for f in freelancers
        ]
        
        prompt = f"""
        Analize këtë projekt dhe gjej 5 freelancerët më të mirë.
        
        PROJEKTI:
        {json.dumps(project_data, ensure_ascii=False, indent=2)}
        
        FREELANCERËT E DISPONUESHËM:
        {json.dumps(freelancer_data, ensure_ascii=False, indent=2)}
        
        Kthe VETËM JSON në formatin:
        {{
            "matches": [
                {{
                    "freelancer_id": <id>,
                    "score": <0-100>,
                    "reason": "<arsyeja e shkurtër>"
                }}
            ]
        }}
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Jeni një ekspert i rekrutimit të freelancerëve. Ktheni VETËM JSON të vlefshëm."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Ruaj rezultatet në databazë
        for match in result["matches"]:
            ai_match = AIMatch(
                project_id=project.id,
                freelancer_id=match["freelancer_id"],
                score=match["score"],
                reason=match["reason"]
            )
            db.add(ai_match)
        db.commit()
        
        return result["matches"]
    
    async def analyze_project(self, description: str) -> dict:
        """Analizon projektin dhe sugjeron skill-et dhe budget-in."""
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Analizoni projektet freelance dhe sugjeroni skill-e dhe budget. Ktheni vetëm JSON."
                },
                {
                    "role": "user",
                    "content": f"Analizoni: {description}\n\nKtheni: {{skills: [], budget_range: {{min, max}}, complexity: 'low|medium|high', estimated_duration: ''}}"
                }
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

ai_service = AIService()