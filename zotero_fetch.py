import os
from pyzotero import zotero
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ZOTERO_API_KEY")
USER_ID = os.getenv("ZOTERO_USER_ID")

def connect_zotero():
    """Connect to your Zotero library"""
    zot = zotero.Zotero(USER_ID, 'user', API_KEY)
    print("Connected to Zotero successfully")
    return zot

def get_all_items(zot):
    """Fetch all items with progress indicator and safety limit"""
    print("Fetching your Zotero library...")
    
    all_items = []
    start = 0
    batch_size = 100
    max_items = 2000  # safety limit above your known library size
    
    while True:
        batch = zot.items(limit=batch_size, start=start)
        
        if not batch:
            break
        
        all_items.extend(batch)
        print(f"  Fetched {len(all_items)} items so far...", end="\r")
        
        # Safety limit
        if len(all_items) >= max_items:
            print(f"\n  Reached safety limit of {max_items}")
            break
        
        # If batch smaller than requested we're at the end
        if len(batch) < batch_size:
            break
        
        start += batch_size
    
    # Deduplicate by key
    seen = set()
    unique_items = []
    for item in all_items:
        key = item["data"]["key"]
        if key not in seen:
            seen.add(key)
            unique_items.append(item)
    
    print(f"\nFinished — {len(unique_items)} unique items fetched")
    return unique_items

def parse_zotero_items(items):
    """Extract clean data from Zotero items"""
    articles = []
    
    for item in items:
        data = item.get("data", {})
        
        # Skip attachments, notes, and non-paper items
        item_type = data.get("itemType", "")
        if item_type in ["attachment", "note", "computerProgram"]:
            continue
        
        # Extract authors
        authors = []
        for creator in data.get("creators", []):
            lastname = creator.get("lastName", "")
            firstname = creator.get("firstName", "")
            if lastname:
                authors.append(f"{lastname} {firstname}".strip())
        
        # Extract key fields
        title = data.get("title", "No title")
        abstract = data.get("abstractNote", "No abstract")
        year = data.get("date", "")[:4]
        journal = data.get("publicationTitle", "")
        doi = data.get("DOI", "")
        tags = [t["tag"] for t in data.get("tags", [])]
        
        articles.append({
            "zotero_key": data.get("key", ""),
            "title": title,
            "abstract": abstract,
            "year": year,
            "authors": authors,
            "journal": journal,
            "doi": doi,
            "tags": tags,
            "url": f"https://doi.org/{doi}" if doi else "",
            "source": "zotero"
        })
    
    return articles

def get_collections(zot):
    """Fetch all collections/folders in your Zotero library"""
    collections = zot.collections()
    print(f"\nYour Zotero collections:")
    for col in collections:
        name = col["data"]["name"]
        key = col["data"]["key"]
        print(f"  {name} ({key})")
    return collections

def get_collection_items(zot, collection_key):
    """Fetch all items from a specific collection"""
    print(f"Fetching items from collection {collection_key}...")
    items = zot.everything(zot.collection_items(collection_key))
    print(f"Found {len(items)} items in collection")
    return items

import json

def save_zotero_library(articles, filename="zotero_library.json"):
    """Save parsed Zotero library to JSON"""
    with open(filename, "w") as f:
        json.dump(articles, f, indent=2)
    print(f"Saved {len(articles)} items to {filename}")