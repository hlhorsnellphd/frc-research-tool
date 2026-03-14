import sys
from pubmed import search_pubmed, fetch_details, parse_articles, save_results
from biorxiv import search_biorxiv
from zotero_fetch import connect_zotero, get_all_items, parse_zotero_items, get_collections, save_zotero_library
from gap_analysis import find_gaps, print_gap_report, save_gap_report

def main():
    # Search query
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "fibroblastic reticular cells secondary lymphoid organs"
    
    print(f"Running search for: {query}")
    print("="*50)

    # PubMed search
    ids = search_pubmed(query, max_results=50)
    xml_data = fetch_details(ids)
    pubmed_articles = parse_articles(xml_data)
    print(f"PubMed: {len(pubmed_articles)} articles")

    # bioRxiv search
    biorxiv_articles = search_biorxiv(query)
    print(f"bioRxiv: {len(biorxiv_articles)} preprints")

    # Combine PubMed + bioRxiv
    all_new_articles = pubmed_articles + biorxiv_articles
    save_results(all_new_articles, "all_results.json")

    # Zotero integration
    print("\n" + "="*50)
    print("ZOTERO LIBRARY")
    print("="*50)
    zot = connect_zotero()
    get_collections(zot)
    items = get_all_items(zot)
    zotero_articles = parse_zotero_items(items)
    save_zotero_library(zotero_articles)

    # Gap analysis
    missing, already_have = find_gaps(pubmed_articles, zotero_articles)
    print_gap_report(missing, already_have)
    save_gap_report(missing)

if __name__ == "__main__":
    main()
