# export_book_chapter.py
# Exports a specific Zotero collection to a clean JSON and CSV

import json
import csv
import os
from sources.zotero import connect

# Paste your collection key here after running Step 1
COLLECTION_KEY = "E8CR8IC5"
OUTPUT_JSON = "outputs/book_chapter_papers.json"
OUTPUT_CSV = "outputs/book_chapter_papers.csv"

def parse_authors(creators):
    """Split into first, last and middle authors"""
    authors = []
    for c in creators:
        lastname = c.get("lastName", "")
        firstname = c.get("firstName", "")
        if lastname:
            authors.append(f"{lastname} {firstname}".strip())
    
    if not authors:
        return "", "", []
    if len(authors) == 1:
        return authors[0], authors[0], []
    
    first_author = authors[0]
    last_author = authors[-1]
    middle_authors = authors[1:-1]
    
    return first_author, last_author, middle_authors

def fetch_collection(zot, collection_key):
    """Fetch all items from a specific collection"""
    print(f"Fetching collection {collection_key}...")
    items = zot.everything(zot.collection_items(collection_key))
    print(f"Found {len(items)} items")
    return items

def parse_collection_items(items):
    """Parse collection items into clean structured data"""
    papers = []
    skipped = 0
    
    skip_types = {"attachment", "note", "computerProgram"}
    
    for item in items:
        data = item.get("data", {})
        
        if data.get("itemType", "") in skip_types:
            skipped += 1
            continue
        
        # Authors
        first_author, last_author, middle_authors = parse_authors(
            data.get("creators", [])
        )
        
        # DOI
        doi = data.get("DOI", "").strip()
        
        year = str(data.get("date", ""))[:4]
        
        papers.append({
            "title": data.get("title", "No title"),
            "first_author": first_author,
            "last_author": last_author,
            "middle_authors": middle_authors,
            "year": year,
            "journal": data.get("publicationTitle", ""),
            "doi": doi,
            "url": f"https://doi.org/{doi}" if doi else "",
            "abstract": data.get("abstractNote", ""),
            "tags": [t["tag"] for t in data.get("tags", [])],
            "item_type": data.get("itemType", "")
        })
    
    print(f"Parsed {len(papers)} papers, skipped {skipped} attachments/notes")
    return papers

def save_json(papers, filepath):
    """Save to JSON"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(papers, f, indent=2)
    print(f"Saved JSON to {filepath}")

def save_csv(papers, filepath):
    """Save to CSV with your requested column structure"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    fields = [
        "title", "first_author", "last_author",
        "middle_authors", "year", "journal", "doi", "url"
    ]
    
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for paper in papers:
            row = {k: paper.get(k, "") for k in fields}
            # Convert list to string for CSV
            row["middle_authors"] = "; ".join(paper.get("middle_authors", []))
            writer.writerow(row)
    
    print(f"Saved CSV to {filepath}")

def print_preview(papers):
    """Print a preview of the first 5 papers"""
    print(f"\n{'='*60}")
    print(f"BOOK CHAPTER COLLECTION — {len(papers)} papers")
    print(f"{'='*60}")
    for p in papers[:5]:
        print(f"\nTitle:        {p['title']}")
        print(f"First author: {p['first_author']}")
        print(f"Last author:  {p['last_author']}")
        print(f"Year:         {p['year']}")
        print(f"Journal:      {p['journal']}")

def main():
    zot = connect()
    items = fetch_collection(zot, COLLECTION_KEY)
    papers = parse_collection_items(items)
    print_preview(papers)
    save_json(papers, OUTPUT_JSON)
    save_csv(papers, OUTPUT_CSV)
    print(f"\nDone! Files saved to outputs/")

if __name__ == "__main__":
    main()