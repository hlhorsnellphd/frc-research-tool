import json

def load_json(filename):
    """Load a JSON file"""
    with open(filename, "r") as f:
        return json.load(f)

def extract_titles(articles):
    """Extract lowercase titles for comparison"""
    return [a["title"].lower().strip() for a in articles]

def find_gaps(pubmed_articles, zotero_articles):
    """Find papers in PubMed that are not in your Zotero library"""
    print("\nRunning gap analysis...")
    
    zotero_titles = extract_titles(zotero_articles)
    
    missing = []
    already_have = []
    
    for paper in pubmed_articles:
        title = paper["title"].lower().strip()
        
        # Check if any zotero title is similar
        found = any(
            title in zt or zt in title
            for zt in zotero_titles
        )
        
        if found:
            already_have.append(paper)
        else:
            missing.append(paper)
    
    return missing, already_have

def print_gap_report(missing, already_have):
    """Print a summary of what you have and what you're missing"""
    print(f"\n{'='*50}")
    print(f"GAP ANALYSIS REPORT")
    print(f"{'='*50}")
    print(f"Papers already in Zotero: {len(already_have)}")
    print(f"Papers missing from Zotero: {len(missing)}")
    
    if missing:
        print(f"\n--- Papers to add to Zotero ---")
        for paper in missing:
            print(f"\nTitle: {paper['title']}")
            print(f"Year:  {paper['year']}")
            print(f"URL:   {paper['url']}")

def save_gap_report(missing, filename="missing_papers.json"):
    """Save missing papers to JSON"""
    with open(filename, "w") as f:
        json.dump(missing, f, indent=2)
    print(f"\nSaved {len(missing)} missing papers to {filename}")