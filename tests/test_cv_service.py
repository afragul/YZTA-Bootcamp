"""CVAnalysisService retry + dogrulama testleri (Kisi 2).

Gemini API cagirmaz; sahte client ile tamamen offline calisir.
"""
import json

import pytest

from services.cv_service import CVAnalysisService, CVAnalysisError


# Semaya uygun minimal gecerli analiz JSON'u.
# role_scores {} birakilir -> Pydantic 22 rolu 0 default ile doldurur.
_VALID_OUTPUT = {
    "skills": ["Python", "FastAPI"],
    "experience_years": 3.0,
    "education": [],
    "strengths": ["Guclu backend temeli"],
    "gaps": ["Docker deneyimi az"],
    "role_scores": {},
}


class _FakeResponse:
    def __init__(self, text: str):
        self.text = text


class _FakeModels:
    """generate_content her cagrildiginda outcomes'tan sirayla bir oge tuketir.

    Oge str ise .text olarak doner; Exception ornegi ise firlatilir.
    """

    def __init__(self, outcomes):
        self._outcomes = list(outcomes)
        self.calls = 0

    def generate_content(self, **kwargs):
        self.calls += 1
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return _FakeResponse(outcome)


class _FakeClient:
    def __init__(self, outcomes):
        self.models = _FakeModels(outcomes)


def _make_service(monkeypatch, outcomes) -> CVAnalysisService:
    """API anahtarini sahteleyip servisi kurar, client'i sahte ile degistirir."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    service = CVAnalysisService()
    service.client = _FakeClient(outcomes)
    return service


def test_gecerli_cikti_dict_doner(monkeypatch):
    service = _make_service(monkeypatch, [json.dumps(_VALID_OUTPUT)])

    result = service.analyze_cv("herhangi bir CV metni")

    assert isinstance(result, dict)
    assert result["skills"] == ["Python", "FastAPI"]
    assert result["experience_years"] == 3.0
    # role_scores bos gelse de sema tum 22 rolu 0 ile doldurur
    assert result["role_scores"]["backend_developer"] == 0
    assert service.client.models.calls == 1


def test_semaya_uymayan_cikti_CVAnalysisError_verir(monkeypatch):
    # experience_years zorunlu; eksik birakmak Pydantic ValidationError uretir
    bad = json.dumps({"skills": []})
    service = _make_service(monkeypatch, [bad, bad, bad])

    with pytest.raises(CVAnalysisError):
        service.analyze_cv("herhangi bir CV metni")


def test_api_hatasi_sonra_basari(monkeypatch):
    sleeps = []
    monkeypatch.setattr("services.cv_service.time.sleep", lambda s: sleeps.append(s))
    err = RuntimeError("gecici API hatasi (429)")
    service = _make_service(monkeypatch, [err, json.dumps(_VALID_OUTPUT)])

    result = service.analyze_cv("CV")

    assert result["skills"] == ["Python", "FastAPI"]
    assert service.client.models.calls == 2
    assert sleeps == [1.0]  # ilk denemeden sonra 1sn beklendi


def test_cikti_hatasi_beklemeden_tekrar_dener(monkeypatch):
    sleeps = []
    monkeypatch.setattr("services.cv_service.time.sleep", lambda s: sleeps.append(s))
    bad = json.dumps({"skills": []})  # ValidationError -> cikti hatasi
    service = _make_service(monkeypatch, [bad, json.dumps(_VALID_OUTPUT)])

    result = service.analyze_cv("CV")

    assert result["experience_years"] == 3.0
    assert service.client.models.calls == 2
    assert sleeps == []  # cikti hatasinda beklenmez


def test_uc_deneme_de_basarisiz_CVAnalysisError(monkeypatch):
    monkeypatch.setattr("services.cv_service.time.sleep", lambda s: None)
    err = RuntimeError("kalici API hatasi")
    service = _make_service(monkeypatch, [err, err, err])

    with pytest.raises(CVAnalysisError):
        service.analyze_cv("CV")

    assert service.client.models.calls == 3
