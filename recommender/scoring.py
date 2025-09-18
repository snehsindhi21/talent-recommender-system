import numpy as np

class ScoringEngine:
    def __init__(self, job_posting: dict):
        self.job = job_posting

    # ----------------------------
    # Skills (skills + software + job types)
    # ----------------------------
    def skill_score(self, candidate_skills: str, candidate_software: str, candidate_jobtypes: str) -> float:
        required = set([s.lower().strip() for s in self.job["skills"]])
        candidate_all = set()

        for field in [candidate_skills, candidate_software, candidate_jobtypes]:
            if isinstance(field, str):
                candidate_all.update([s.lower().strip() for s in field.split(",") if s.strip()])

        matches = required.intersection(candidate_all)
        if len(matches) == 0:
            return 0.0

        return len(matches) / len(required)

    # ----------------------------
    # Budget (+10% tolerance, monthly/hourly aware)
    # ----------------------------
    def budget_score(self, candidate_monthly: float, candidate_hourly: float) -> float:
        budget = self.job.get("budget", None)
        rate_type = self.job.get("rate_type", "monthly")

        if not budget:  # No budget limit
            return 1.0

        candidate_rate = candidate_monthly if rate_type == "monthly" else candidate_hourly
        tolerance = budget * 1.1

        if candidate_rate <= budget:
            return 1.0
        elif candidate_rate <= tolerance:
            return 1 - ((candidate_rate - budget) / (tolerance - budget))
        else:
            return 0.0

    # ----------------------------
    # Location
    # ----------------------------
    def location_score(self, candidate_country: str, candidate_city: str) -> float:
        pref = self.job.get("location", None)
        if not pref or pref.lower() in ["all", "remote"]:
            return 1.0
        if candidate_country.lower() == pref.lower() or candidate_city.lower() == pref.lower():
            return 1.0
        return 0.0

    # ----------------------------
    # Content Verticals (Jaccard)
    # ----------------------------
    def vertical_score(self, candidate_verticals: str) -> float:
        required = set([v.lower().strip() for v in self.job.get("verticals", [])])
        if not required:
            return 1.0

        candidate_set = set([v.lower().strip() for v in candidate_verticals.split(",") if v.strip()])
        if not candidate_set:
            return 0.0

        intersection = len(required.intersection(candidate_set))
        union = len(required.union(candidate_set))
        return intersection / union if union > 0 else 0.0

    # ----------------------------
    # Gender Preference
    # ----------------------------
    def gender_score(self, candidate_gender: str) -> float:
        pref = self.job.get("gender_preference", None)
        if not pref:
            return 1.0
        return 1.0 if candidate_gender.lower() == pref.lower() else 0.5  # partial credit if mismatch

    # ----------------------------
    # Creative Styles (soft boost)
    # ----------------------------
    def style_score(self, candidate_styles: str) -> float:
        required_styles = self.job.get("styles", [])
        if not required_styles:
            return 1.0

        candidate_set = set([s.lower().strip() for s in str(candidate_styles).split(",") if s.strip()])
        if not candidate_set:
            return 0.0

        matches = set([s.lower().strip() for s in required_styles]).intersection(candidate_set)
        return len(matches) / len(required_styles)
