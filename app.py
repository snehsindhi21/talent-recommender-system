from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from recommender.preprocess import DataPreprocessor
from recommender.recommender import TalentRecommender
from recommender.jobs import JOB_POSTINGS

app = FastAPI(title="Talent Recommender API")

# -------------------------
# CORS Middleware (must be before routes)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in production, restrict: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request Models
# -------------------------
class JobRequest(BaseModel):
    job_id: str   # predefined job id


class CustomJobRequest(BaseModel):
    title: str
    skills: list[str]
    verticals: list[str] = []
    location: str = "all"
    budget: float | None = None
    rate_type: str = "monthly"
    gender_preference: str | None = None

# -------------------------
# Routes
# -------------------------
@app.get("/")
def root():
    return {"message": "Talent Recommender API is running 🚀"}


@app.get("/jobs")
def get_jobs():
    return JOB_POSTINGS


@app.post("/recommend")
def get_recommendations(request: JobRequest):
    job_id = request.job_id
    if job_id not in JOB_POSTINGS:
        return {"error": "Invalid job_id. Use one of: job1, job2, job3"}

    df = pd.read_csv("data/talent_profiles.csv")
    df = DataPreprocessor(df).clean()
    recommender = TalentRecommender(df, JOB_POSTINGS)

    results = recommender.recommend(job_id)
    return {"job": JOB_POSTINGS[job_id], "recommendations": results}


@app.post("/recommend/custom")
def get_custom_recommendations(job: CustomJobRequest):
    custom_job = {
        "title": job.title,
        "skills": job.skills,
        "verticals": job.verticals,
        "location": job.location,
        "budget": job.budget,
        "rate_type": job.rate_type,
        "gender_preference": job.gender_preference,
    }

    df = pd.read_csv("data/talent_profiles.csv")
    df = DataPreprocessor(df).clean()
    recommender = TalentRecommender(df, {"custom": custom_job})

    results = recommender.recommend("custom")
    return {"job": custom_job, "recommendations": results}
