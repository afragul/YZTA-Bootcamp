from schemas.api_contract import CVUploadResponse, JobMatchItem
from schemas.cv_analysis import CVAnalysisOutput, EducationItem, RoleScores, RoleReason
from schemas.learning_plan import RankedRole
from services.learning_service import rank_roles

def build_mock_upload_response(cv_id: str, filename: str) -> CVUploadResponse:
    role_scores = RoleScores(
        backend_developer=85,
        frontend_developer=70,
        fullstack_developer=80,
        mobile_developer=30,
        devops_engineer=50,
        cloud_engineer=45,
        machine_learning_engineer=40,
        data_scientist=45,
        data_engineer=55,
        data_analyst=60,
        bi_analyst=50,
        database_administrator=65,
        cybersecurity_specialist=30,
        systems_administrator=40,
        ui_ux_designer=55,
        graphic_designer=20,
        product_manager=40,
        project_manager=35,
        business_analyst=50,
        digital_marketing_specialist=15,
        hr_specialist=10,
        customer_success_specialist=25,
    )
    analysis = CVAnalysisOutput(
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
            role_scores=role_scores,
            top_role_reasons=[
                RoleReason(
                    role="backend_developer",
                    score=85,
                    reason="Python ve FastAPI ile REST API gelistirme deneyimi ve SQL bilgisi "
                           "bu rolun cekirdek gereksinimlerini karsiliyor.",
                ),
                RoleReason(
                    role="fullstack_developer",
                    score=80,
                    reason="Hem React hem FastAPI tarafinda calismis olmasi full-stack rolu icin "
                           "guclu bir temel sunuyor.",
                ),
                RoleReason(
                    role="frontend_developer",
                    score=70,
                    reason="React ve JavaScript deneyimi mevcut; ancak ileri seviye state yonetimi "
                           "ve test araclarina dair kanit CV'de gorunmuyor.",
                ),
            ],
    )
    rankings = rank_roles(role_scores.model_dump())
    return CVUploadResponse(
        cv_id=cv_id,
        filename=filename,
        status="completed",
        message="Mock yanit - Hafta 1 entegrasyon kontrati (22 Rol Uyumlu)",
        analysis=analysis,
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
        role_rankings=[RankedRole(**r) for r in rankings],
    )
