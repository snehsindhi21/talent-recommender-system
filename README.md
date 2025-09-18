# 🎯 Talent Recommender System

A **Talent Recommendation Engine** that matches job postings with the most relevant candidates based on skills, budget, location, verticals, gender preference, creative styles, embeddings, and popularity.  
Built with **FastAPI**, **Pandas**, and **Sentence Transformers**.

---

## 📂 Project Structure
```
data_slush
├─ app.py                # FastAPI entrypoint
├─ main.py               # Script runner (optional)
├─ data
│  └─ talent_profiles.csv  # Sample talent dataset
├─ recommender
│  ├─ base.py            # Abstract base class
│  ├─ embeddings.py      # EmbeddingEngine using SentenceTransformers
│  ├─ jobs.py            # Predefined job postings
│  ├─ preprocess.py      # DataPreprocessor for cleaning
│  ├─ recommender.py     # TalentRecommender core logic
│  ├─ scoring.py         # ScoringEngine (skills, budget, location, etc.)
├─ requirements.txt      # Dependencies
└─ README.md             # Documentation
```

---

## ⚙️ Features
- ✅ Candidate-job **matching** using weighted scoring
- ✅ **Skills**, **budget**, **location**, **verticals**, **gender preference**, and **styles** support
- ✅ **Sentence embeddings** (`all-MiniLM-L6-v2`) for semantic similarity
- ✅ Popularity boost based on profile views
- ✅ **FastAPI REST API** for job and recommendation queries
- ✅ Supports **predefined jobs** and **custom job postings**

---

## 🚀 Getting Started

### 1️⃣ Clone Repository
```bash
git clone https://github.com/snehsindhi21/talent-recommender-system.git
cd talent-recommender-system
```

### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3️⃣ Run FastAPI Server
```bash
uvicorn app:app --reload
```

Server runs at:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📡 API Endpoints

### Root
```http
GET /
```
**Response:**
```json
{"message": "Talent Recommender API is running 🚀"}
```

### Get All Jobs
```http
GET /jobs
```

### Recommend Candidates for Predefined Job
```http
POST /recommend
```
**Body:**
```json
{
  "job_id": "job1"
}
```

### Recommend Candidates for Custom Job
```http
POST /recommend/custom
```
**Body:**
```json
{
  "title": "UI/UX Designer",
  "skills": ["Figma", "Prototyping"],
  "verticals": ["Productivity", "Education"],
  "location": "United States",
  "budget": 2000,
  "rate_type": "monthly",
  "gender_preference": "Female"
}
```

---

## 🧮 Scoring System
Each candidate is evaluated using multiple criteria:

| Criteria            | Weight |
|---------------------|--------|
| Skills Match        | 40%    |
| Content Verticals   | 15%    |
| Location Match      | 10%    |
| Budget Alignment    | 10%    |
| Creative Styles     | 5%     |
| Gender Preference   | 5%     |
| Embedding Similarity| 5%     |
| Popularity (Views)  | 10%    |

---

## 📊 Example Output
```json
{
  "job": {
    "title": "Video Editor",
    "skills": ["Splice & Dice", "Rough Cut & Sequencing", "2D Animation"],
    "verticals": ["Entertainment", "Lifestyle & Vlogs"],
    "location": "Asia",
    "budget": 2500,
    "rate_type": "monthly"
  },
  "recommendations": [
    {
      "name": "John Doe",
      "score": 87.5,
      "skills": "splice & dice, 2d animation",
      "software": "premiere pro, after effects",
      "job_types": "freelance",
      "location": "Mumbai, India",
      "monthly_rate": 2000,
      "hourly_rate": 25
    }
  ]
}
```

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **FastAPI** + **Uvicorn**
- **Pandas / NumPy**
- **Scikit-learn**
- **Sentence Transformers**
- **tqdm**, **python-dotenv**

---

## 👨‍💻 Author
Built with ❤️ for talent-job matching.  
Feel free to fork, improve, and contribute 🚀

Sneh Sindhi | snehsindhi2004@gmail.com
