# sources/pubmed.py
import requests
import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("PUBMED_EMAIL")
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def search_pubmed(query, max_results=100, date_from=None, date_to=None):
    """Search PubMed and return list of article IDs"""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "email": EMAIL
    }
    
    if date_from and date_to:
        params["mindate"] = date_from
        params["maxdate"] = date_to
        params["datetype"] = "pdat"
    
    response = requests.get(BASE_URL + "esearch.fcgi", params=params)
    data = response.json()
    ids = data["esearchresult"]["idlist"]
    return ids

def fetch_details(pubmed_ids):
    """Fetch full details for a list of PubMed IDs"""
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml",
        "rettype": "abstract",
        "email": EMAIL
    }
    response = requests.get(BASE_URL + "efetch.fcgi", params=params)
    return response.text

def parse_articles(xml_text):
    """Parse XML into clean article dictionaries"""
    articles = []
    root = ET.fromstring(xml_text)
    
    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="No title")
        abstract = article.findtext(".//AbstractText", default="No abstract")
        year = article.findtext(".//PubDate/Year", default="Unknown")
        pmid = article.findtext(".//PMID", default="")
        journal = article.findtext(".//Journal/Title", default="")
        
        # Extract DOI
        doi = ""
        for id_elem in article.findall(".//ArticleId"):
            if id_elem.get("IdType") == "doi":
                doi = id_elem.text or ""
        
        # Extract all authors
        authors = []
        for author in article.findall(".//Author"):
            lastname = author.findtext("LastName", default="")
            forename = author.findtext("ForeName", default="")
            if lastname:
                authors.append(f"{lastname} {forename}".strip())
        
        articles.append({
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "year": year,
            "authors": authors,
            "journal": journal,
            "doi": doi,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "source": "pubmed"
        })
    
    return articles

def fetch_era(query, date_from, date_to, max_results=100):
    """Fetch papers for a specific date range era"""
    print(f"  Searching {date_from[:4]}–{date_to[:4]}...")
    ids = search_pubmed(query, max_results, date_from, date_to)
    print(f"  Found {len(ids)} articles")
    if not ids:
        return []
    xml_data = fetch_details(ids)
    articles = parse_articles(xml_data)
    return articles

def fetch_all_eras(query, date_ranges, max_per_era=100):
    """Fetch papers across multiple date ranges"""
    all_articles = []
    
    for date_from, date_to, era_name in date_ranges:
        print(f"\nEra: {era_name}")
        articles = fetch_era(query, date_from, date_to, max_per_era)
        
        # Tag each article with its era
        for a in articles:
            a["era"] = era_name
        
        all_articles.extend(articles)
        print(f"  Parsed {len(articles)} articles")
    
    print(f"\nTotal PubMed articles: {len(all_articles)}")
    return all_articles