from schemas.api_contract import CVUploadResponse, JobMatchItem
from schemas.cv_analysis import CVAnalysisOutput, EducationItem, RoleScores


def build_mock_upload_response(cv_id: str, filename: str) -> CVUploadResponse:
    return CVUploadResponse(
        cv_id=cv_id,
        filename=filename,
        status="completed",
        message="Mock yanit - Hafta 1 entegrasyon kontrati",
        analysis=CVAnalysisOutput(
            skills=["Python", "FastAPI", "React", "JavaScript", "SQL", "Git"],
            experience_years=1.5,
            education=[
                EducationItem(
                    degree="Lisans",
                    school="Istanbul Teknik Universitesi",
                    department="Bilgisayar Muhendisligi",
                    graduation_year=2025,
                )
            ],
            strengths=[
                "Full-stack web gelistirme temelleri guclu",
                "FastAPI ile REST API gelistirme deneyimi var",
                "Iyi derecede algoritma ve veri yapilari bilgisi",
            ],
            gaps=[
                "Machine Learning projelerinde deneyim eksikligi",
                "Docker ve CI/CD sureclerinde pratik eksikligi",
                "Bulut bilisim (AWS/GCP) tecrubesi bulunmuyor",
            ],
            role_scores=RoleScores(
                backend_developer=85,
                frontend_developer=70,
                machine_learning_engineer=40,
                data_scientist=45,
                devops_engineer=50,
            ),
        ),
        top_matches=[
            JobMatchItem(
                title="Backend Developer (Python/FastAPI)",
                job_domain="Backend",
                work_type="Remote",
                job_location="Istanbul",
                match_percent=88.5,
                description="FastAPI ve PostgreSQL ile mikroservis gelistirme.",
            ),
            JobMatchItem(
                title="Full Stack Developer",
                job_domain="Full Stack",
                work_type="Hybrid",
                job_location="Ankara",
                match_percent=76.2,
                description="React ve Python ile urun odakli gelistirme.",
            ),
        ],
    )
