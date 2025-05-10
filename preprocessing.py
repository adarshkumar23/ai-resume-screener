import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    """Clean text by removing special characters and extra whitespace"""
    if not text:
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    # Replace newlines with spaces
    text = re.sub(r'\n', ' ', text)
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_text(text):
    """Tokenize text into individual words"""
    return word_tokenize(text)

def preprocess_text(text):
    """Preprocess text by cleaning and tokenizing"""
    cleaned_text = clean_text(text)
    tokens = tokenize_text(cleaned_text)
    
    # Remove stopwords (optional)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    return filtered_tokens

def preprocess_corpus(texts):
    """Preprocess a list of texts"""
    preprocessed_texts = []
    
    for text in texts:
        clean = clean_text(text)
        preprocessed_texts.append(clean)
        
    return preprocessed_texts