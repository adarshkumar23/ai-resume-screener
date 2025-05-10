import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import ResumeRanker
from file_handler import extract_text

def test_ranker():
    # Sample data
    resumes = [
        "Experienced Python developer with 5 years of experience in Flask, Django, and machine learning.",
        "Java developer with 3 years of experience in Spring Boot and Hibernate.",
        "Full stack engineer with Python, JavaScript, and React experience."
    ]
    
    job_description = "Looking for a senior Python developer with Flask experience for a machine learning project."
    
    # Create ranker
    ranker = ResumeRanker()
    
    # Rank resumes
    ranked_results = ranker.rank_resumes(resumes, job_description)
    
    # Print results
    print("Ranked Resumes:")
    for idx, score in ranked_results:
        print(f"Score: {score:.4f} - Resume: {resumes[idx][:50]}...")
        
    # Expected: first resume should rank highest
    assert ranked_results[0][0] == 0, "Expected the first resume to rank highest"

if __name__ == "__main__":
    test_ranker()
    print("All tests passed!")
