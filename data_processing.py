# data_processing.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

def train_categorization_model(repo_data):
    # Assuming repo_data is a list of (description, category) tuples
    descriptions, categories = zip(*repo_data)
    
    model = make_pipeline(
        TfidfVectorizer(stop_words='english'),
        MultinomialNB()
    )
    
    model.fit(descriptions, categories)
    return model

def save_model(model, filename='categorization_model.joblib'):
    joblib.dump(model, filename)

def load_model(filename='categorization_model.joblib'):
    return joblib.load(filename)

def categorize_repo(model, description, topics):
    combined_text = f"{description} {' '.join(topics)}"
    return model.predict([combined_text])[0]

if __name__ == "__main__":
    # Example usage
    sample_data = [
        ("A web framework for building APIs", "Web Development"),
        ("A machine learning library", "Machine Learning"),
        ("A tool for container orchestration", "DevOps"),
    ]
    model = train_categorization_model(sample_data)
    save_model(model)
    print("Model trained and saved successfully")