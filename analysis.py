# analysis.py
import json

def find_gaps(pubmed_articles, zotero_articles):
    """Find PubMed papers not in Zotero using DOI then title matching"""
    print("\nRunning gap analysis...")
    
    zotero_dois = {
        a["doi"].strip().lower()
        for a in zotero_articles
        if a.get("doi", "").strip()
    }
    zotero_titles = {
        a["title"].strip().lower()
        for a in zotero_articles
        if a.get("title", "").strip()
    }
    
    missing = []
    already_have = []
    
    for paper in pubmed_articles:
        doi = paper.get("doi", "").strip().lower()
        title = paper.get("title", "").strip().lower()
        
        if (doi and doi in zotero_dois) or (title and title in zotero_titles):
            already_have.append(paper)
        else:
            missing.append(paper)
    
    return missing, already_have

def print_gap_report(missing, already_have):
    """Print gap analysis summary"""
    print(f"\n{'='*50}")
    print(f"GAP ANALYSIS REPORT")
    print(f"{'='*50}")
    print(f"Already in Zotero: {len(already_have)}")
    print(f"Missing from Zotero: {len(missing)}")
    
    if missing:
        print(f"\n--- Papers to add ---")
        for p in missing:
            print(f"\n  {p['title']}")
            print(f"  {p['year']} | {p['journal']}")
            print(f"  {p['url']}")

def export_reading_list(articles, filepath):
    """Export formatted reading list sorted by year"""
    sorted_articles = sorted(
        articles,
        key=lambda x: x.get("year", "0000"),
        reverse=True
    )
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w") as f:
        f.write("FRC LITERATURE — READING LIST\n")
        f.write("="*50 + "\n\n")
        
        for i, paper in enumerate(sorted_articles, 1):
            authors = ", ".join(paper["authors"][:3])
            if len(paper["authors"]) > 3:
                authors += " et al."
            f.write(f"{i}. {paper['title']}\n")
            f.write(f"   {authors}\n")
            f.write(f"   {paper.get('journal', '')} ({paper['year']})\n")
            if paper.get("doi"):
                f.write(f"   DOI: {paper['doi']}\n")
            f.write("\n")
    
    print(f"Reading list saved to {filepath}")

def build_author_network(articles):
    """Build author collaboration network from papers"""
    import itertools
    
    nodes = {}
    edges = {}
    
    for paper in articles:
        authors = paper.get("authors", [])
        year = paper.get("year", "")
        title = paper.get("title", "")
        
        # Add each author as a node
        for author in authors:
            if author not in nodes:
                nodes[author] = {
                    "id": author,
                    "papers": [],
                    "paper_count": 0
                }
            nodes[author]["papers"].append(title)
            nodes[author]["paper_count"] += 1
        
        # Add edges between all co-authors on this paper
        for a1, a2 in itertools.combinations(authors, 2):
            edge_key = tuple(sorted([a1, a2]))
            if edge_key not in edges:
                edges[edge_key] = {
                    "source": a1,
                    "target": a2,
                    "papers": [],
                    "weight": 0
                }
            edges[edge_key]["papers"].append(title)
            edges[edge_key]["weight"] += 1
    
    network = {
        "nodes": list(nodes.values()),
        "edges": list(edges.values())
    }
    
    print(f"Network: {len(nodes)} authors, {len(edges)} collaborations")
    return network

import os