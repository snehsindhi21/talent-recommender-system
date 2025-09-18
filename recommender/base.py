from abc import ABC, abstractmethod
import pandas as pd

class BaseRecommender(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @abstractmethod
    def recommend(self, job_id: str, top_n: int = 10):
        """Return top N recommended candidates for a job posting."""
        pass
