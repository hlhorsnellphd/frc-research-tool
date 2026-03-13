import requests
import json

BASE_URL = "https://api.biorxiv.org/details/biorxiv/"

def search_biorxiv(query, days_back=365):
    """Search bioRxiv for preprints matching a query"""
    from datetime import datetime, timedelta
    
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    print(f"Searching bioRxiv from {start_date} to {end_date}")
    
    url = f"{BASE_URL}{start_date}/{end_date}/0"
    response = requests.get(url)
    data = response.json()
    
    papers = data.get("collection", [])
    
    # Filter by query terms manually
    query_terms = query.lower().split()
    matching = []
    
    for paper in papers:
        text = (paper.get("title", "") + " " + paper.get("abstract", "")).lower()
        if any(term in text for term in query_terms):
            matching.append({
                "pmid": paper.get("doi", ""),
                "title": paper.get("title", ""),
                "abstract": paper.get("abstract", ""),
                "year": paper.get("date", "")[:4],
                "authors": [paper.get("authors", "")[:50]],
                "url": f"https://biorxiv.org/abs/{paper.get('doi', '')}"
            })
    
    print(f"Found {len(matching)} matching preprints")
    return matching
