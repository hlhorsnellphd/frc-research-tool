from pubmed import search_pubmed, fetch_details, parse_articles, save_results
from biorxiv import search_biorxiv

# Your search terms - edit these anytim
SEARCH_QUERY = "fibroblastic reticular cells secondary lymphoid organs"

def main():
    # PubMed search
    ids = search_pubmed(SEARCH_QUERY, max_results=50)
    xml_data = fetch_details(ids)
    pubmed_articles = parse_articles(xml_data)
    print(f"PubMed: {len(pubmed_articles)} articles")
    
    # bioRxiv search
    biorxiv_articles = search_biorxiv("fibroblastic reticular")
    print(f"bioRxiv: {len(biorxiv_articles)} preprints")
    
    # Combine
    all_articles = pubmed_articles + biorxiv_articles
    print(f"\nTotal: {len(all_articles)} papers found")
    
    # Preview
    print(f"\n--- First 3 PubMed results ---")
    for article in pubmed_articles[:3]:
        print(f"\nTitle: {article['title']}")
        print(f"Year:  {article['year']}")
        print(f"URL:   {article['url']}")
   
    # Preview
    print(f"\n--- First 3 BioRxiv results ---")
    for article in biorxiv_articles[:3]:
        print(f"\nTitle: {article['title']}")
        print(f"Year:  {article['year']}")
        print(f"URL:   {article['url']}")
 
    # Save combined results
    save_results(all_articles, "all_results.json")

if __name__ == "__main__":
    main()
