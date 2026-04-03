# sources/zotero.py
import os
from pyzotero import zotero
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ZOTERO_API_KEY")
USER_ID = os.getenv("ZOTERO_USER_ID")

SKIP_TYPES = {"attachment", "note", "computerProgram"}

def connect():
    """Connect to Zotero library"""
    zot = zotero.Zotero(USER_ID, 'user', API_KEY)
    return zot

def fetch_all(zot):
    """Fetch all items with progress indicator"""
    total = zot.count_items()
    print(f"Zotero library contains {total} items")
    
    all_items = []
    start = 0
    batch_size = 100
    
    while start < total:
        batch = zot.items(limit=batch_size, start=start)
        if not batch:
            break
        all_items.extend(batch)
        print(f"  Fetched {len(all_items)}/{total}...", end="\r")
        start += batch_size
    
    print(f"\nFetch complete")
    return all_items

def parse_items(items):
    """Parse Zotero items into clean dictionaries"""
    articles = []
    skipped = 0
    
    for item in items:
        data = item.get("data", {})
        
        if data.get("itemType", "") in SKIP_TYPES:
            skipped += 1
            continue
        
        authors = []
        for creator in data.get("creators", []):
            lastname = creator.get("lastName", "")
            firstname = creator.get("firstName", "")
            if lastname:
                authors.append(f"{lastname} {firstname}".strip())
        
        doi = data.get("DOI", "").strip()
        
        articles.append({
            "zotero_key": data.get("key", ""),
            "title": data.get("title", "No title"),
            "abstract": data.get("abstractNote", ""),
            "year": str(data.get("date", ""))[:4],
            "authors": authors,
            "journal": data.get("publicationTitle", ""),
            "doi": doi,
            "tags": [t["tag"] for t in data.get("tags", [])],
            "url": f"https://doi.org/{doi}" if doi else "",
            "source": "zotero",
            "item_type": data.get("itemType", "")
        })
    
    print(f"Parsed {len(articles)} items, skipped {skipped} attachments/notes")
    return articles

def audit(articles):
    """Print a summary of what was extracted"""
    print(f"\n{'='*50}")
    print(f"ZOTERO AUDIT REPORT")
    print(f"{'='*50}")
    print(f"Total items: {len(articles)}")
    
    # Count by type
    types = {}
    for a in articles:
        t = a.get("item_type", "unknown")
        types[t] = types.get(t, 0) + 1
    print(f"\nItem types:")
    for t, count in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")
    
    # Count missing fields
    no_abstract = sum(1 for a in articles if not a["abstract"])
    no_doi = sum(1 for a in articles if not a["doi"])
    no_authors = sum(1 for a in articles if not a["authors"])
    no_year = sum(1 for a in articles if not a["year"] or a["year"] == "")
    
    print(f"\nData completeness:")
    print(f"  Missing abstract: {no_abstract}")
    print(f"  Missing DOI:      {no_doi}")
    print(f"  Missing authors:  {no_authors}")
    print(f"  Missing year:     {no_year}")
    
    # Year distribution
    years = {}
    for a in articles:
        y = a.get("year", "")[:4]
        if y.isdigit():
            decade = f"{y[:3]}0s"
            years[decade] = years.get(decade, 0) + 1
    print(f"\nBy decade:")
    for decade in sorted(years):
        bar = "█" * (years[decade] // 5)
        print(f"  {decade}: {bar} {years[decade]}")