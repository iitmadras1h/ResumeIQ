"""
ResumeIQ - AI Resume Analyzer
AI-powered resume analysis system with ATS scoring, skills identification,
career roadmaps, gap analysis, and company recommendations.
"""

import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class ATSScore:
    """ATS (Applicant Tracking System) Score analysis"""
    overall_score: int  # 0-100
    formatting_score: int
    keyword_match_score: int
    experience_score: int
    education_score: int
    recommendations: List[str]


@dataclass
class SkillAnalysis:
    """Identified skills from resume"""
    technical_skills: List[str]
    soft_skills: List[str]
    domain_skills: List[str]
    certifications: List[str]
    proficiency_levels: Dict[str, str]  # skill -> level (beginner/intermediate/advanced)


@dataclass
class CareerRoadmap:
    """Personalized career progression roadmap"""
    current_level: str
    target_roles: List[str]
    timeline: str
    milestones: List[Dict[str, str]]
    learning_path: List[str]


@dataclass
class GapAnalysis:
    """Gap analysis for target job profile"""
    target_profile: str
    missing_skills: List[str]
    skills_to_improve: List[str]
    experience_gap: str
    education_gap: Optional[str]
    recommendations: List[str]


@dataclass
class CompanyRecommendation:
    """Company recommendations based on profile"""
    company_name: str
    match_score: int
    reasons: List[str]
    culture_fit: str
    role_suggestions: List[str]


class ResumeAnalyzer:
    """Main Resume Analysis Engine"""

    def __init__(self):
        self.ats_keywords = self._load_ats_keywords()
        self.skill_database = self._load_skill_database()
        self.company_database = self._load_company_database()

    def _load_ats_keywords(self) -> Dict[str, List[str]]:
        """Load ATS keyword database"""
        return {
            "software_engineering": [
                "python", "java", "javascript", "react", "node.js", "aws", "docker",
                "kubernetes", "agile", "scrum", "git", "ci/cd", "microservices",
                "rest api", "sql", "nosql", "mongodb", "postgresql"
            ],
            "data_science": [
                "machine learning", "deep learning", "python", "r", "tensorflow",
                "pytorch", "pandas", "numpy", "scikit-learn", "nlp", "computer vision",
                "statistics", "data analysis", "sql", "big data", "spark"
            ],
            "product_management": [
                "product strategy", "roadmap", "user stories", "agile", "scrum",
                "stakeholder management", "analytics", "a/b testing", "user research",
                "wireframing", "jira", "product lifecycle"
            ],
            "marketing": [
                "digital marketing", "seo", "sem", "social media", "content marketing",
                "analytics", "google analytics", "campaign management", "brand strategy",
                "email marketing", "crm", "roi analysis"
            ]
        }

    def _load_skill_database(self) -> Dict[str, Dict[str, List[str]]]:
        """Load comprehensive skill database"""
        return {
            "technical": {
                "programming": ["Python", "Java", "JavaScript", "C++", "Go", "Rust", "TypeScript"],
                "frameworks": ["React", "Angular", "Vue.js", "Django", "Flask", "Spring Boot"],
                "cloud": ["AWS", "Azure", "GCP", "Kubernetes", "Docker", "Terraform"],
                "databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch"],
                "tools": ["Git", "Jenkins", "GitLab CI", "Jira", "Confluence"]
            },
            "soft_skills": [
                "Leadership", "Communication", "Problem Solving", "Team Collaboration",
                "Critical Thinking", "Adaptability", "Time Management", "Creativity"
            ],
            "domain": {
                "finance": ["Financial Modeling", "Risk Management", "Compliance", "Trading"],
                "healthcare": ["HIPAA", "Clinical Workflows", "Medical Coding", "Patient Care"],
                "ecommerce": ["Payment Systems", "Inventory Management", "Customer Analytics"]
            }
        }

    def _load_company_database(self) -> List[Dict[str, Any]]:
        """Load company database for recommendations"""
        return [
            {
                "name": "Tech Giants (FAANG)",
                "categories": ["software", "data", "product"],
                "culture": "fast-paced, innovative, high-performance",
                "skills_required": ["algorithms", "system design", "coding excellence"],
                "experience_level": "mid to senior"
            },
            {
                "name": "Startups (Series A-B)",
                "categories": ["software", "product", "marketing"],
                "culture": "agile, flexible, ownership-driven",
                "skills_required": ["full-stack", "rapid prototyping", "adaptability"],
                "experience_level": "junior to mid"
            },
            {
                "name": "Enterprise Companies",
                "categories": ["software", "data", "consulting"],
                "culture": "structured, process-oriented, stable",
                "skills_required": ["domain expertise", "stakeholder management", "scalability"],
                "experience_level": "mid to senior"
            },
            {
                "name": "Consulting Firms",
                "categories": ["consulting", "product", "data"],
                "culture": "client-focused, analytical, travel-heavy",
                "skills_required": ["problem solving", "presentation", "business acumen"],
                "experience_level": "all levels"
            }
        ]

    def analyze_ats_score(self, resume_text: str, job_description: str = "") -> ATSScore:
        """Analyze ATS compatibility score"""
        # Formatting analysis
        formatting_score = self._check_formatting(resume_text)

        # Keyword matching
        keyword_score = self._analyze_keywords(resume_text, job_description)

        # Experience analysis
        experience_score = self._analyze_experience(resume_text)

        # Education analysis
        education_score = self._analyze_education(resume_text)

        # Calculate overall score
        overall = int((formatting_score * 0.2 + keyword_score * 0.4 +
                      experience_score * 0.25 + education_score * 0.15))

        # Generate recommendations
        recommendations = self._generate_ats_recommendations(
            formatting_score, keyword_score, experience_score, education_score
        )

        return ATSScore(
            overall_score=overall,
            formatting_score=formatting_score,
            keyword_match_score=keyword_score,
            experience_score=experience_score,
            education_score=education_score,
            recommendations=recommendations
        )

    def _check_formatting(self, resume_text: str) -> int:
        """Check resume formatting quality"""
        score = 100

        # Check for clear sections
        sections = ["experience", "education", "skills"]
        for section in sections:
            if section.lower() not in resume_text.lower():
                score -= 10

        # Check for contact information
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.search(email_pattern, resume_text):
            score -= 15

        # Check length (too short or too long)
        word_count = len(resume_text.split())
        if word_count < 200:
            score -= 20
        elif word_count > 1000:
            score -= 10

        return max(0, score)

    def _analyze_keywords(self, resume_text: str, job_description: str) -> int:
        """Analyze keyword matching"""
        resume_lower = resume_text.lower()

        # If no job description, do general keyword analysis
        if not job_description:
            total_keywords = 0
            found_keywords = 0

            for category, keywords in self.ats_keywords.items():
                total_keywords += len(keywords)
                for keyword in keywords:
                    if keyword.lower() in resume_lower:
                        found_keywords += 1

            return int((found_keywords / total_keywords) * 100) if total_keywords > 0 else 50

        # Match against job description
        jd_lower = job_description.lower()
        jd_words = set(re.findall(r'\b\w+\b', jd_lower))
        resume_words = set(re.findall(r'\b\w+\b', resume_lower))

        # Filter meaningful words (length > 3)
        jd_words = {w for w in jd_words if len(w) > 3}
        matching_words = jd_words.intersection(resume_words)

        match_ratio = len(matching_words) / len(jd_words) if jd_words else 0
        return int(match_ratio * 100)

    def _analyze_experience(self, resume_text: str) -> int:
        """Analyze work experience quality"""
        score = 50  # Base score

        # Check for years of experience mentioned
        year_patterns = [r'\d+\+?\s*years?', r'\d{4}\s*-\s*\d{4}', r'\d{4}\s*-\s*present']
        years_found = sum(1 for pattern in year_patterns if re.search(pattern, resume_text, re.IGNORECASE))
        score += min(years_found * 10, 30)

        # Check for action verbs
        action_verbs = ['led', 'managed', 'developed', 'created', 'implemented', 'designed',
                       'improved', 'increased', 'reduced', 'achieved', 'delivered']
        verbs_found = sum(1 for verb in action_verbs if verb in resume_text.lower())
        score += min(verbs_found * 3, 20)

        return min(score, 100)

    def _analyze_education(self, resume_text: str) -> int:
        """Analyze education credentials"""
        score = 50

        # Check for degrees
        degrees = ['bachelor', 'master', 'phd', 'doctorate', 'mba', 'b.s.', 'm.s.', 'b.a.', 'm.a.']
        degree_found = any(degree in resume_text.lower() for degree in degrees)
        if degree_found:
            score += 30

        # Check for university/college mention
        edu_keywords = ['university', 'college', 'institute', 'school']
        if any(keyword in resume_text.lower() for keyword in edu_keywords):
            score += 20

        return min(score, 100)

    def _generate_ats_recommendations(self, formatting: int, keywords: int,
                                     experience: int, education: int) -> List[str]:
        """Generate ATS improvement recommendations"""
        recommendations = []

        if formatting < 70:
            recommendations.append("Improve resume formatting: Include clear section headers for Experience, Education, and Skills")
            recommendations.append("Add contact information including email and phone number")

        if keywords < 60:
            recommendations.append("Increase keyword density by incorporating industry-specific terms from job descriptions")
            recommendations.append("Add relevant technical skills and tools to match target roles")

        if experience < 60:
            recommendations.append("Use stronger action verbs to describe accomplishments (e.g., 'led', 'developed', 'achieved')")
            recommendations.append("Quantify achievements with metrics and numbers")

        if education < 60:
            recommendations.append("Clearly list educational credentials with degree type and institution")

        return recommendations

    def identify_skills(self, resume_text: str) -> SkillAnalysis:
        """Identify and categorize skills from resume"""
        resume_lower = resume_text.lower()

        technical_skills = []
        soft_skills = []
        domain_skills = []
        certifications = []
        proficiency_levels = {}

        # Extract technical skills
        for category, skills in self.skill_database["technical"].items():
            for skill in skills:
                if skill.lower() in resume_lower:
                    technical_skills.append(skill)
                    # Infer proficiency level
                    if re.search(rf'\b(expert|advanced|senior)\s+{skill.lower()}', resume_lower):
                        proficiency_levels[skill] = "Advanced"
                    elif re.search(rf'\b(intermediate|proficient)\s+{skill.lower()}', resume_lower):
                        proficiency_levels[skill] = "Intermediate"
                    else:
                        proficiency_levels[skill] = "Beginner"

        # Extract soft skills
        for skill in self.skill_database["soft_skills"]:
            if skill.lower() in resume_lower:
                soft_skills.append(skill)

        # Extract domain skills
        for domain, skills in self.skill_database["domain"].items():
            for skill in skills:
                if skill.lower() in resume_lower:
                    domain_skills.append(skill)

        # Extract certifications
        cert_patterns = [
            r'certified\s+[\w\s]+', r'certification:\s*[\w\s]+',
            r'\b(AWS|Azure|GCP)\s+\w+', r'\bPMP\b', r'\bCFA\b', r'\bCPA\b'
        ]
        for pattern in cert_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            certifications.extend(matches)

        return SkillAnalysis(
            technical_skills=list(set(technical_skills)),
            soft_skills=list(set(soft_skills)),
            domain_skills=list(set(domain_skills)),
            certifications=list(set(certifications)),
            proficiency_levels=proficiency_levels
        )

    def generate_career_roadmap(self, resume_text: str, target_role: str = "") -> CareerRoadmap:
        """Generate personalized career roadmap"""
        skills = self.identify_skills(resume_text)

        # Determine current level
        years_exp = self._extract_years_of_experience(resume_text)
        if years_exp < 2:
            current_level = "Junior"
        elif years_exp < 5:
            current_level = "Mid-Level"
        elif years_exp < 10:
            current_level = "Senior"
        else:
            current_level = "Staff/Principal"

        # Suggest target roles based on skills
        if not target_role:
            if len(skills.technical_skills) > 5:
                target_roles = ["Senior Software Engineer", "Tech Lead", "Engineering Manager"]
            else:
                target_roles = ["Software Engineer", "Full Stack Developer", "Backend Developer"]
        else:
            target_roles = [target_role]

        # Create timeline
        timeline = self._create_timeline(current_level, target_roles[0])

        # Define milestones
        milestones = [
            {"milestone": "Skill Enhancement", "timeframe": "0-3 months",
             "description": "Master core technical skills and fill knowledge gaps"},
            {"milestone": "Project Leadership", "timeframe": "3-6 months",
             "description": "Lead small to medium projects, demonstrate impact"},
            {"milestone": "Mentorship & Visibility", "timeframe": "6-12 months",
             "description": "Mentor junior developers, increase cross-team collaboration"},
            {"milestone": "Role Transition", "timeframe": "12-18 months",
             "description": "Apply for target role with proven track record"}
        ]

        # Create learning path
        learning_path = self._create_learning_path(skills, target_roles[0])

        return CareerRoadmap(
            current_level=current_level,
            target_roles=target_roles,
            timeline=timeline,
            milestones=milestones,
            learning_path=learning_path
        )

    def _extract_years_of_experience(self, resume_text: str) -> int:
        """Extract total years of experience"""
        # Look for explicit mentions
        match = re.search(r'(\d+)\+?\s*years?\s+of\s+experience', resume_text, re.IGNORECASE)
        if match:
            return int(match.group(1))

        # Calculate from date ranges
        year_ranges = re.findall(r'(\d{4})\s*-\s*(?:(\d{4})|present)', resume_text, re.IGNORECASE)
        if year_ranges:
            total_years = 0
            current_year = datetime.now().year
            for start, end in year_ranges:
                end_year = int(end) if end else current_year
                total_years += (end_year - int(start))
            return total_years

        return 0

    def _create_timeline(self, current_level: str, target_role: str) -> str:
        """Create realistic timeline for career progression"""
        if current_level == "Junior":
            return "18-24 months"
        elif current_level == "Mid-Level":
            return "12-18 months"
        else:
            return "6-12 months"

    def _create_learning_path(self, skills: SkillAnalysis, target_role: str) -> List[str]:
        """Create personalized learning path"""
        learning_items = []

        # Based on common role requirements
        role_lower = target_role.lower()

        if "senior" in role_lower or "lead" in role_lower:
            learning_items.extend([
                "System Design and Architecture",
                "Leadership and Team Management",
                "Technical Decision Making"
            ])

        if "engineer" in role_lower or "developer" in role_lower:
            if len(skills.technical_skills) < 5:
                learning_items.append("Master 2-3 additional programming languages/frameworks")
            learning_items.extend([
                "Advanced Algorithms and Data Structures",
                "Cloud Architecture (AWS/Azure/GCP)",
                "DevOps and CI/CD Practices"
            ])

        if "manager" in role_lower:
            learning_items.extend([
                "Project Management Methodologies",
                "Stakeholder Communication",
                "Team Building and Conflict Resolution"
            ])

        return learning_items[:5]  # Top 5 items

    def perform_gap_analysis(self, resume_text: str, job_description: str) -> GapAnalysis:
        """Perform gap analysis against target job profile"""
        current_skills = self.identify_skills(resume_text)

        # Extract required skills from job description
        jd_lower = job_description.lower()
        required_skills = []

        # Check technical skills
        for category, skills in self.skill_database["technical"].items():
            for skill in skills:
                if skill.lower() in jd_lower and skill not in current_skills.technical_skills:
                    required_skills.append(skill)

        # Analyze experience gap
        current_years = self._extract_years_of_experience(resume_text)
        required_years_match = re.search(r'(\d+)\+?\s*years', job_description, re.IGNORECASE)
        required_years = int(required_years_match.group(1)) if required_years_match else 0

        if current_years < required_years:
            experience_gap = f"Need {required_years - current_years} more years of experience"
        else:
            experience_gap = "Experience requirement met"

        # Education gap
        education_gap = None
        if "master" in jd_lower or "mba" in jd_lower:
            if not any(deg in resume_text.lower() for deg in ["master", "mba", "m.s.", "m.a."]):
                education_gap = "Master's degree or MBA preferred"

        # Skills to improve
        skills_to_improve = []
        for skill in current_skills.technical_skills:
            if current_skills.proficiency_levels.get(skill) == "Beginner" and skill.lower() in jd_lower:
                skills_to_improve.append(skill)

        # Generate recommendations
        recommendations = [
            f"Acquire missing skills: {', '.join(required_skills[:5])}" if required_skills else "Skill set aligns well",
            f"Gain {required_years - current_years} more years of relevant experience" if current_years < required_years else "Experience level is appropriate",
            "Build projects or certifications to demonstrate proficiency",
            "Tailor resume to highlight relevant experience for this role"
        ]

        return GapAnalysis(
            target_profile=self._extract_job_title(job_description),
            missing_skills=required_skills[:10],
            skills_to_improve=skills_to_improve[:5],
            experience_gap=experience_gap,
            education_gap=education_gap,
            recommendations=recommendations
        )

    def _extract_job_title(self, job_description: str) -> str:
        """Extract job title from description"""
        # Look for common patterns
        title_match = re.search(r'(?:position|role|title):\s*([^\n]+)', job_description, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()

        # Look for "Software Engineer" type patterns at the start
        lines = job_description.split('\n')
        if lines:
            return lines[0].strip()[:100]

        return "Target Role"

    def recommend_companies(self, resume_text: str, preferences: Dict[str, Any] = None) -> List[CompanyRecommendation]:
        """Recommend companies based on profile"""
        skills = self.identify_skills(resume_text)
        years_exp = self._extract_years_of_experience(resume_text)

        recommendations = []

        for company_profile in self.company_database:
            match_score = 0
            reasons = []

            # Experience level match
            exp_level = company_profile["experience_level"]
            if years_exp < 2 and "junior" in exp_level:
                match_score += 30
                reasons.append("Good fit for your experience level")
            elif 2 <= years_exp < 5 and "mid" in exp_level:
                match_score += 30
                reasons.append("Matches your mid-level experience")
            elif years_exp >= 5 and "senior" in exp_level:
                match_score += 30
                reasons.append("Suitable for senior-level professionals")
            elif "all levels" in exp_level:
                match_score += 20

            # Skills alignment
            skill_matches = sum(1 for req_skill in company_profile["skills_required"]
                              if any(req_skill.lower() in skill.lower()
                                    for skill in skills.technical_skills + skills.soft_skills))
            if skill_matches > 0:
                match_score += min(skill_matches * 15, 40)
                reasons.append(f"Your skills align with their requirements")

            # Add variety of reasons
            if match_score > 50:
                reasons.append(f"Culture: {company_profile['culture']}")

            # Suggest roles
            role_suggestions = []
            if "software" in company_profile["categories"]:
                role_suggestions.append("Software Engineer")
            if "data" in company_profile["categories"]:
                role_suggestions.append("Data Analyst/Scientist")
            if "product" in company_profile["categories"]:
                role_suggestions.append("Product Manager")

            if match_score > 30:  # Only include reasonable matches
                recommendations.append(CompanyRecommendation(
                    company_name=company_profile["name"],
                    match_score=min(match_score, 100),
                    reasons=reasons,
                    culture_fit=company_profile["culture"],
                    role_suggestions=role_suggestions
                ))

        # Sort by match score
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        return recommendations[:5]

    def generate_full_report(self, resume_text: str, job_description: str = "",
                           target_role: str = "") -> Dict[str, Any]:
        """Generate comprehensive resume analysis report"""

        report = {
            "analysis_date": datetime.now().isoformat(),
            "ats_score": asdict(self.analyze_ats_score(resume_text, job_description)),
            "skills_analysis": asdict(self.identify_skills(resume_text)),
            "career_roadmap": asdict(self.generate_career_roadmap(resume_text, target_role)),
        }

        if job_description:
            report["gap_analysis"] = asdict(self.perform_gap_analysis(resume_text, job_description))

        company_recs = self.recommend_companies(resume_text)
        report["company_recommendations"] = [asdict(rec) for rec in company_recs]

        return report


def main():
    """Main function for command-line usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python resume_analyzer.py <resume_file> [job_description_file] [target_role]")
        sys.exit(1)

    # Read resume
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        resume_text = f.read()

    # Read job description if provided
    job_description = ""
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            job_description = f.read()

    # Get target role if provided
    target_role = sys.argv[3] if len(sys.argv) > 3 else ""

    # Create analyzer and generate report
    analyzer = ResumeAnalyzer()
    report = analyzer.generate_full_report(resume_text, job_description, target_role)

    # Save report
    output_file = "resume_analysis_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"✓ Analysis complete! Report saved to {output_file}")
    print(f"\nOverall ATS Score: {report['ats_score']['overall_score']}/100")
    print(f"Skills Identified: {len(report['skills_analysis']['technical_skills'])} technical, "
          f"{len(report['skills_analysis']['soft_skills'])} soft skills")
    print(f"Career Level: {report['career_roadmap']['current_level']}")
    print(f"Top Company Match: {report['company_recommendations'][0]['company_name']} "
          f"({report['company_recommendations'][0]['match_score']}% match)")


if __name__ == "__main__":
    main()
