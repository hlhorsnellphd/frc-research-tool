# database.py
import json
import os

def save(data, filepath):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} items to {filepath}")

def load(filepath):
    """Load data from JSON file"""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return []
    with open(filepath, "r") as f:
        return json.load(f)

def deduplicate(articles):
    """Remove duplicates preferring DOI match then title match"""
    seen_dois = set()
    seen_titles = set()
    unique = []
    duplicates = 0
    
    for article in articles:
        doi = article.get("doi", "").strip().lower()
        title = article.get("title", "").strip().lower()
        
        if doi and doi in seen_dois:
            duplicates += 1
            continue
        if title and title in seen_titles:
            duplicates += 1
            continue
        
        if doi:
            seen_dois.add(doi)
        if title:
            seen_titles.add(title)
        
        unique.append(article)
    
    print(f"Deduplication: {len(articles)} → {len(unique)} items ({duplicates} removed)")
    return unique