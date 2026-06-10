import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data securely on first run
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

def preprocess_text(text):
    """
    Complete NLP preprocessing pipeline.
    Demonstrates: Lowercasing, Punctuation Removal, Tokenization, and Stop Word Removal.
    """
    # 1. Lowercasing: Convert all text to lowercase
    text = text.lower()
    
    # 2. Remove Punctuation using Regular Expressions
    # Replaces anything that is not a word character (\w) or whitespace (\s) with an empty string
    text = re.sub(r'[^\w\s]', '', text)
    
    # 3. Tokenization: Break the sentence into a list of words
    try:
        tokens = word_tokenize(text)
    except LookupError:
        # Fallback if NLTK punkt fails to load
        tokens = text.split()
    
    # 4. Stop-word Removal: Remove common but uninformative words (e.g., 'the', 'is', 'how', 'do')
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [word for word in tokens if word not in stop_words]
    
    return cleaned_tokens

def extract_keywords_string(text):
    """
    Returns the preprocessed tokens as a single space-separated string.
    Useful for displaying to the user.
    """
    tokens = preprocess_text(text)
    return " ".join(tokens)
    