import requests
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("PUBMED_EMAIL")
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def search_pubmed(query, max_results=20):
    """Search PubMed and return a list of article IDs"""
    print(f"Searching PubMed for: {query}")
    
    url = BASE_URL + "esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "email": EMAIL
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    ids = data["esearchresult"]["idlist"]
    print(f"Found {len(ids)} articles")
    return ids

# This function will feth articles

def fetch_details(pubmed_ids):
    """Fetch title, abstract and authors for a list of PubMed IDs"""
    print(f"Fetching details for {len(pubmed_ids)} articles...")
    
    url = BASE_URL + "efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml",
        "rettype": "abstract",
        "email": EMAIL
    }
    
    response = requests.get(url, params=params)
    return response.text

# This extracts the data

import xml.etree.ElementTree as ET

def parse_articles(xml_text):
    """Parse XML response into a clean list of article dictionaries"""
    articles = []
    root = ET.fromstring(xml_text)
    
    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="No title")
        abstract = article.findtext(".//AbstractText", default="No abstract")
        year = article.findtext(".//PubDate/Year", default="Unknown")
        
        authors = []
        for author in article.findall(".//Author"):
            lastname = author.findtext("LastName", default="")
            forename = author.findtext("ForeName", default="")
            if lastname:
                authors.append(f"{lastname} {forename}".strip())
        
        pmid = article.findtext(".//PMID", default="")
        
        articles.append({
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "year": year,
            "authors": authors,  # [:3] first 3 authors only
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        })
    
    return articles

# This makes a json file with the data

import json

def save_results(articles, filename="results.json"):
    """Save articles to a JSON file"""
    with open(filename, "w") as f:
        json.dump(articles, f, indent=2)
    print(f"Saved {len(articles)} articles to {filename}")
