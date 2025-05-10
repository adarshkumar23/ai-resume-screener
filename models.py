from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import preprocess_corpus

class ResumeRanker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)  # Include bigrams
        )
        
    def rank_resumes(self, resumes, job_description):
        """
        Rank resumes based on similarity to job description
        
        Args:
            resumes: List of resume texts
            job_description: Job description text
            
        Returns:
            List of tuples (resume_index, score) sorted by score in descending order
        """
        if not resumes or not job_description:
            return []
            
        # Preprocess all texts
        processed_resumes = preprocess_corpus(resumes)
        processed_jd = preprocess_corpus([job_description])[0]
        
        # Create corpus with job description at the end
        corpus = processed_resumes + [processed_jd]
        
        # Fit and transform corpus
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        
        # Extract resume vectors and job description vector
        resume_vectors = tfidf_matrix[:-1]  # All but last
        jd_vector = tfidf_matrix[-1]        # Last vector
        
        # Calculate similarity
        similarity_scores = cosine_similarity(resume_vectors, jd_vector.reshape(1, -1)).flatten()
        
        # Create list of (index, score) tuples
        ranked_resumes = [(i, float(score)) for i, score in enumerate(similarity_scores)]
        
        # Sort by score in descending order
        ranked_resumes.sort(key=lambda x: x[1], reverse=True)
        
        return ranked_resumes
