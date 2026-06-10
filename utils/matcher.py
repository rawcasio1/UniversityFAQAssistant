from utils.preprocessing import preprocess_text
from utils.database import get_all_faqs

def find_best_match(user_query):
    """
    Matches the user query against the FAQ database.
    Calculates a confidence score based on token intersection.
    """
    # 1. Preprocess the user's question
    user_tokens = preprocess_text(user_query)
    
    # If the user typed only stop words or punctuation, return no match
    if not user_tokens:
        return {"error": "Please provide more details."}

    all_faqs = get_all_faqs()
    best_match = None
    highest_score = 0.0

    # 2. Compare against all FAQs in the database
    for faq in all_faqs:
        # Preprocess the keywords stored in the database
        faq_keywords = faq['keywords'].lower().split()
        
        # Calculate intersection (how many words match)
        match_count = len(set(user_tokens).intersection(set(faq_keywords)))
        
        # Calculate score as a percentage of user tokens matched
        # Cap at 1.0 (100%)
        score = min(match_count / len(user_tokens), 1.0)
        
        # Give a slight boost if words from the title also match
        title_tokens = preprocess_text(faq['title'])
        if len(set(user_tokens).intersection(set(title_tokens))) > 0:
            score += 0.2
            score = min(score, 1.0) # Ensure it doesn't exceed 100%

        if score > highest_score:
            highest_score = score
            best_match = faq

    # 3. Return results based on confidence threshold
    if highest_score > 0.25: # At least 25% confidence required
        return {
            "matched": True,
            "title": best_match['title'],
            "policy_section": best_match['policy_section'],
            "answer": best_match['answer'],
            "confidence": f"{int(highest_score * 100)}%",
            "matched_keywords": ", ".join(user_tokens)
        }
    else:
        # Return suggestions if no solid match is found
        suggestions = [faq['title'] for faq in all_faqs[:4]] # Get first 4 titles
        return {
            "matched": False,
            "suggestions": suggestions
        }
        