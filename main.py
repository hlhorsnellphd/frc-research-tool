# main.py
import sys
from config import (
    SEARCH_QUERY, DATE_RANGES, MAX_RESULTS_PER_ERA,
    PUBMED_FILE, ZOTERO_FILE, COMBINED_FILE,
    MISSING_FILE, READING_LIST_FILE, NETWORK_FILE
)
from sources.pubmed import fetch_all_eras
from sources.zotero import connect, fetch_all, parse_items, audit
from database import save, load, deduplicate
from analysis import find_gaps, print_gap_report, export_reading_list, build_author_network

def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else SEARCH_QUERY
    print(f"Query: {query}")
    print("="*50)

    # --- PubMed ---
    print("\nPUBMED SEARCH")
    pubmed_articles = fetch_all_eras(query, DATE_RANGES, MAX_RESULTS_PER_ERA)
    pubmed_articles = deduplicate(pubmed_articles)
    save(pubmed_articles, PUBMED_FILE)

    # --- Zotero ---
    print("\nZOTERO LIBRARY")
    zot = connect()
    raw_items = fetch_all(zot)
    zotero_articles = parse_items(raw_items)
    zotero_articles = deduplicate(zotero_articles)
    save(zotero_articles, ZOTERO_FILE)
    audit(zotero_articles)

    # --- Gap analysis ---
    missing, already_have = find_gaps(pubmed_articles, zotero_articles)
    print_gap_report(missing, already_have)
    save(missing, MISSING_FILE)

    # --- Reading list ---
    export_reading_list(zotero_articles, READING_LIST_FILE)

    # --- Author network ---
    print("\nBUILDING AUTHOR NETWORK")
    all_papers = pubmed_articles + zotero_articles
    all_papers = deduplicate(all_papers)
    save(all_papers, COMBINED_FILE)
    network = build_author_network(all_papers)
    save(network["nodes"], NETWORK_FILE.replace(".json", "_nodes.json"))
    save(network["edges"], NETWORK_FILE.replace(".json", "_edges.json"))

if __name__ == "__main__":
    main()