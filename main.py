from pubmed import search_pubmed, fetch_details, parse_articles, save_results

# Your search terms - edit these anytime
SEARCH_QUERY = "fibroblastic reticular cells secondary lymphoid organs"

def main():
    # Search PubMed
    ids = search_pubmed(SEARCH_QUERY, max_results=50)
    
    if not ids:
        print("No results found")
        return
    
    # Fetch and parse details
    xml_data = fetch_details(ids)
    articles = parse_articles(xml_data)
    
    # Print a preview
    print(f"\n--- Preview of first 3 results ---")
    for article in articles[:3]:
        print(f"\nTitle: {article['title']}")
        print(f"Year:  {article['year']}")
        print(f"Authors: {', '.join(article['authors'])}")
        print(f"URL: {article['url']}")
    
    # Save everything
    save_results(articles)

if __name__ == "__main__":
    main()
