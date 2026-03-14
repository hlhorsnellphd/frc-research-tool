import requests
from datetime import datetime, timedelta

BASE_URL = "https://api.biorxiv.org/details/biorxiv/"

def search_biorxiv(query, days_back=1825):
    """Search bioRxiv for preprints matching a query"""
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    print(f"Searching bioRxiv from {start_date} to {end_date}")
    
    # Hardcoded FRC field terms
    key_terms = [
        "fibroblastic reticular cell",
        "FRC",
        "lymphoid stroma",
        "stromal cell lymph node",
        "CCL19", "CCL21",
        "T cell zone",
        "lymph node fibroblast"
    ]
    
    matching = []
    cursor = 0
    
    while True:
        url = f"{BASE_URL}{start_date}/{end_date}/{cursor}"
        print(f"  Fetching page at cursor {cursor}...", end="\r")
        
        response = requests.get(url)
        data = response.json()
        papers = data.get("collection", [])
        
        if not papers:
            break
        
        for paper in papers:
            text = (paper.get("title", "") + " " + paper.get("abstract", "")).lower()
            if any(term.lower() in text for term in key_terms):
                matching.append({
                    "pmid": paper.get("doi", ""),
                    "title": paper.get("title", ""),
                    "abstract": paper.get("abstract", ""),
                    "year": paper.get("date", "")[:4],
                    "authors": [paper.get("authors", "")],
                    "url": f"https://biorxiv.org/abs/{paper.get('doi', '')}",
                    "source": "bioRxiv"
                })
        
        cursor += 100
        
        if cursor > 500:
            print(f"\n  Reached page limit, stopping")
            break
    
    print(f"\nFound {len(matching)} matching preprints")
    return matching
