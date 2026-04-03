# config.py — all settings in one place

# PubMed search settings
SEARCH_QUERY = "fibroblastic reticular cells secondary lymphoid organs"

DATE_RANGES = [
    ("1990/01/01", "2000/12/31", "era_1990_2000"),
    ("2001/01/01", "2016/12/31", "era_2001_2016"),
    ("2017/01/01", "2026/12/31", "era_2017_2026"),
]

MAX_RESULTS_PER_ERA = 100

# File paths
DATA_DIR = "data"
OUTPUTS_DIR = "outputs"
PUBMED_FILE = "data/pubmed_results.json"
ZOTERO_FILE = "data/zotero_library.json"
COMBINED_FILE = "data/all_papers.json"
MISSING_FILE = "data/missing_papers.json"
READING_LIST_FILE = "outputs/reading_list.txt"
NETWORK_FILE = "outputs/network.json"