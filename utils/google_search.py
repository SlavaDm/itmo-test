import requests


def google_search(query, api_key, gse_key, num_results=3):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": gse_key,
        "num": num_results,
        "rights": "cc_publicdomain, cc_noncommercial, cc_nonderived",
    }
    response = requests.get(search_url, params=params)
    return response.json()
