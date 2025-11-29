import os
import time
import requests
import pandas as pd

API_KEY = os.getenv("SERPAPI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "Environment variable SERPAPI_API_KEY is not set. "
        "Set it before running the script."
    )

ORDER_PLATFORMS = {
    "glovoapp.com": "glovo",
    "pyszne.pl": "pyszne",
    "ubereats": "uber",
    "bolt": "bolt",
    "wolt": "wolt",
    "foodora": "foodora",
    "bistro.sk": "bistro",
    "lokomenu": "loko",
    "delivery": "delivery",
}


def clean_links(all_links, social_profiles=None):
    result = {
        "Facebook": "",
        "Instagram": "",
        "Order": set(),
    }

    if social_profiles:
        for profile in social_profiles:
            link = profile.get("link", "").lower()
            if "instagram.com" in link:
                result["Instagram"] = profile["link"]
            elif "facebook.com" in link:
                result["Facebook"] = profile["link"]

    for link in set(all_links):
        l = link.lower()

        if "facebook.com" in l and not result["Facebook"]:
            if all(excl not in l for excl in ["sharer", "plugins", "dialog/feed"]):
                result["Facebook"] = link

        elif "instagram.com" in l and not result["Instagram"]:
            result["Instagram"] = link

        for domain, platform in ORDER_PLATFORMS.items():
            if domain in l:
                result["Order"].add(platform)

    return {
        "Facebook": result["Facebook"],
        "Instagram": result["Instagram"],
        "Order": ", ".join(sorted(result["Order"])),
    }


def get_knowledge_data(name, city):
    query = f"{name} {city}"
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "hl": "en",
        "gl": "pl",
        "api_key": API_KEY,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    result = {
        "Website": "",
        "Google Reviews": "",
        "Phone": "",
        "Facebook": "",
        "Instagram": "",
        "Order": "",
    }

    panel = data.get("knowledge_graph", {}) or {}

    result["Website"] = panel.get("menu", "")
    result["Google Reviews"] = panel.get("review_count", "")
    result["Phone"] = panel.get("phone", "")

    all_links = []

    # list в knowledge_graph
    all_links += [
        item.get("link", "")
        for item in panel.get("list", [])
        if "link" in item
    ]

    
    source = panel.get("source", {})
    if isinstance(source, dict):
        link = source.get("link", "")
        if isinstance(link, list):
            all_links += link
        elif isinstance(link, str):
            all_links.append(link)

  
    for item in data.get("organic_results", []):
        link = item.get("link", "")
        if link:
            all_links.append(link)

    social_profiles = panel.get("profiles", [])

    cleaned = clean_links(all_links, social_profiles)
    result["Facebook"] = cleaned["Facebook"]
    result["Instagram"] = cleaned["Instagram"]
    result["Order"] = cleaned["Order"]

    return result


def main():
    df = pd.read_excel("leads.xlsx")

    if not {"Name", "City"}.issubset(df.columns):
        raise ValueError("The file must contain the columns ‘Name’ and ‘City’.")

    results = []

    for i, row in df.iterrows():
        name = str(row["Name"])
        city = str(row["City"])
        print(f"[{i + 1}/{len(df)}] {name} ({city})")

        try:
            info = get_knowledge_data(name, city)
            results.append(info)
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append(
                {
                    key: ""
                    for key in [
                        "Website",
                        "Google Reviews",
                        "Phone",
                        "Facebook",
                        "Instagram",
                        "Order",
                    ]
                }
            )

        time.sleep(1.5)

    final_df = pd.concat([df, pd.DataFrame(results)], axis=1)
    final_df.to_excel("leads_with_info.xlsx", index=False)
    print("✅ready. Saved in leads_with_info.xlsx")


if __name__ == "__main__":
    main()
