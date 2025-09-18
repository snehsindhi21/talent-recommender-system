import pandas as pd
from .scoring import ScoringEngine
from .embeddings import EmbeddingEngine

class TalentRecommender:
    def __init__(self, df: pd.DataFrame, job_postings: dict):
        self.df = df
        self.jobs = job_postings
        self.embedder = EmbeddingEngine()

    def recommend(self, job_id: str, top_n: int = 10):
        job = self.jobs[job_id]
        scorer = ScoringEngine(job)

        results = []
        max_views = self.df["# of Views by Creators"].max()

        for _, row in self.df.iterrows():
            # -------------------------------
            # 1. Skills (hard-ish filter)
            # -------------------------------
            skill_score = scorer.skill_score(
                row["Skills"], row["Software"], row["Job Types"]
            )
            if skill_score == 0:
                continue  # reject if no skill overlap

            # -------------------------------
            # 2. Budget
            # -------------------------------
            budget_score = scorer.budget_score(
                row["Monthly Rate"], row["Hourly Rate"]
            )
            if budget_score == 0:
                continue  # reject if out of tolerance

            # -------------------------------
            # 3. Location
            # -------------------------------
            location_score = scorer.location_score(
                row["Country"], row["City"]
            )

            # -------------------------------
            # 4. Content Verticals
            # -------------------------------
            vertical_score = scorer.vertical_score(
                row["Content Verticals"]
            )

            # -------------------------------
            # 5. Gender Preference
            # -------------------------------
            gender_score = scorer.gender_score(
                row["Gender"]
            )

            # -------------------------------
            # 6. Creative Styles
            # -------------------------------
            style_score = scorer.style_score(
                row["Creative Styles"]
            )

            # -------------------------------
            # 7. Embedding similarity (soft skills)
            # -------------------------------
            emb_score = self.embedder.similarity(
                job["title"], row["Profile Description"]
            )

            # -------------------------------
            # 8. Popularity (normalized)
            # -------------------------------
            pop_score = row["# of Views by Creators"] / max_views

            # -------------------------------
            # Final Weighted Score
            # -------------------------------
            final_score = (
                0.40 * skill_score +
                0.15 * vertical_score +
                0.10 * location_score +
                0.10 * budget_score +
                0.05 * style_score +
                0.05 * gender_score +
                0.05 * emb_score +
                0.10 * pop_score
            )

            results.append({
                "name": f"{row['First Name']} {row['Last Name']}",
                "score": round(final_score * 100, 2),
                "skills": row["Skills"],
                "software": row["Software"],
                "job_types": row["Job Types"],
                "location": f"{row['City']}, {row['Country']}",
                "monthly_rate": row["Monthly Rate"],
                "hourly_rate": row["Hourly Rate"]
            })

        ranked = sorted(results, key=lambda x: x["score"], reverse=True)
        return ranked[:top_n]
