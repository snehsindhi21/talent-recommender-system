import pandas as pd

class DataPreprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def clean(self):
        # Normalize text fields
        text_cols = ["Skills", "Software", "Content Verticals", "Job Types"]
        for col in text_cols:
            self.df[col] = self.df[col].fillna("").str.lower()

        # Normalize location
        self.df["Country"] = self.df["Country"].str.strip().str.lower()

        return self.df
