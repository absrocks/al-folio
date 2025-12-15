#!/usr/bin/env python

import os
import sys
import yaml, json
from datetime import datetime
from scholarly import scholarly


def load_scholar_user_id() -> str:
    """Load the Google Scholar user ID from the configuration file."""
    config_file = "_data/socials.yml"
    if not os.path.exists(config_file):
        print(
            f"Configuration file {config_file} not found. Please ensure the file exists and contains your Google Scholar user ID."
        )
        sys.exit(1)
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        scholar_user_id = config.get("scholar_userid")
        if not scholar_user_id:
            print(
                "No 'scholar_userid' found in the configuration file. Please add 'scholar_userid' to _data/socials.yml."
            )
            sys.exit(1)
        return scholar_user_id
    except yaml.YAMLError as e:
        print(
            f"Error parsing YAML file {config_file}: {e}. Please check the file for correct YAML syntax."
        )
        sys.exit(1)


SCHOLAR_USER_ID: str = load_scholar_user_id()
OUTPUT_FILE: str = "_data/citations.yml"
OUTPUT_PROFILE: str = "_data/scholar_profile.yml"
OUTPUT_JSON: str = "_data/citations_last5y.json"

def yml_is_current(path: str, today: str) -> bool:
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        last = (data.get("metadata") or {}).get("last_updated")
        if last == today:
            print(f"{path}: already up-to-date (last_updated={last}). Skipping fetch.")
            return True
        if last:
            print(f"{path}: last_updated={last} (will update).")
        return False
    except Exception as e:
        print(f"Warning: Could not read {path}: {e} (will update).")
        return False
def json_is_current(path: str, today: str) -> bool:
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        last = (data.get("metadata") or {}).get("last_updated")
        if last == today:
            print(f"{path}: already up-to-date (last_updated={last}). Skipping fetch.")
            return True
        if last:
            print(f"{path}: last_updated={last} (will update).")
        return False
    except Exception as e:
        print(f"Warning: Could not read {path}: {e} (will update).")
        return False

def write_scholar_profile_and_timeseries() -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    scholarly.set_timeout(15)
    scholarly.set_retries(3)
    if yml_is_current(OUTPUT_PROFILE, today) and json_is_current(OUTPUT_JSON, today):
        return
    try:
        author = scholarly.search_author_id(SCHOLAR_USER_ID)
    except Exception as e:
        print(
            f"Error fetching author data from Google Scholar for user ID '{SCHOLAR_USER_ID}': {e}. Please check your internet connection and Scholar user ID."
        )
        sys.exit(1)
    now_year = datetime.utcnow().year
    cutoff_year = now_year - 5
    cited_all = int(author.get("citedby", 0) or 0)
    cited_5y = int(scholarly.fill(author, sections=['basics', 'indices']).get("citedby5y") or 0)
    h_all = int(author.get("hindex", 0) or 0)
    h_5y = int(scholarly.fill(author, sections=['basics', 'indices']).get("hindex5y", 0) or 0)
    i10_all = int(author.get("i10index", 0) or 0)
    i10_5y = int(scholarly.fill(author, sections=['basics', 'indices']).get("i10index5y", 0) or 0)
    author = scholarly.fill(author, sections=["indices", "counts"])
    cites_per_year = author.get("cites_per_year") or {}

    years = list(range(now_year - 4, now_year + 1))  # last 5 years inclusive
    values = [int(cites_per_year.get(y, 0) or 0) for y in years]
    citation_data = {
        "metadata": {"last_updated": today},
        "scholar": {
            "since_year": cutoff_year,
            "all": {
                "citations": cited_all,
                "h_index": h_all,
                "i10_index": i10_all,
            },
            "since": {
                "citations": cited_5y,
                "h_index": h_5y,
                "i10_index": i10_5y,
            },
        }
    }
    try:
        with open(OUTPUT_PROFILE, "w") as f:
            yaml.dump(citation_data, f, width=1000, sort_keys=False)
        print(f"Citation data saved to {OUTPUT_PROFILE}")
    except Exception as e:
        print(
            f"Error writing citation data to {OUTPUT_PROFILE}: {e}. Please check file permissions and disk space."
        )
        sys.exit(1)
    payload = {
        "metadata": {"last_updated": today},
        "since_year": cutoff_year,
        "years": years,
        "citations": values,
    }
    try:
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=10)
        print(f"Citation data saved to {OUTPUT_JSON}")
    except Exception as e:
        print(
            f"Error writing citation data to {OUTPUT_JSON}: {e}. Please check file permissions and disk space."
        )
        sys.exit(1)
def get_scholar_citations() -> None:
    """Fetch and update Google Scholar citation data."""
    print(f"Fetching citations for Google Scholar ID: {SCHOLAR_USER_ID}")
    today = datetime.now().strftime("%Y-%m-%d")

    # Check if the output file was already updated today
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r") as f:
                existing_data = yaml.safe_load(f)
            if (
                existing_data
                and "metadata" in existing_data
                and "last_updated" in existing_data["metadata"]
            ):
                print(f"Last updated on: {existing_data['metadata']['last_updated']}")
                if existing_data["metadata"]["last_updated"] == today:
                    print("Citations data is already up-to-date. Skipping fetch.")
                    return
        except Exception as e:
            print(
                f"Warning: Could not read existing citation data from {OUTPUT_FILE}: {e}. The file may be missing or corrupted."
            )

    citation_data = {"metadata": {"last_updated": today}, "papers": {}}

    scholarly.set_timeout(15)
    scholarly.set_retries(3)
    try:
        author = scholarly.search_author_id(SCHOLAR_USER_ID)
        author_data = scholarly.fill(author)
    except Exception as e:
        print(
            f"Error fetching author data from Google Scholar for user ID '{SCHOLAR_USER_ID}': {e}. Please check your internet connection and Scholar user ID."
        )
        sys.exit(1)

    if not author_data:
        print(
            f"Could not fetch author data for user ID '{SCHOLAR_USER_ID}'. Please verify the Scholar user ID and try again."
        )
        sys.exit(1)

    if "publications" not in author_data:
        print(f"No publications found in author data for user ID '{SCHOLAR_USER_ID}'.")
        sys.exit(1)

    for pub in author_data["publications"]:
        try:
            pub_id = pub.get("pub_id") or pub.get("author_pub_id")
            if not pub_id:
                print(
                    f"Warning: No ID found for publication: {pub.get('bib', {}).get('title', 'Unknown')}. This publication will be skipped."
                )
                continue

            title = pub.get("bib", {}).get("title", "Unknown Title")
            year = pub.get("bib", {}).get("pub_year", "Unknown Year")
            citations = pub.get("num_citations", 0)

            print(f"Found: {title} ({year}) - Citations: {citations}")

            citation_data["papers"][pub_id] = {
                "title": title,
                "year": year,
                "citations": citations,
            }
        except Exception as e:
            print(
                f"Error processing publication '{pub.get('bib', {}).get('title', 'Unknown')}': {e}. This publication will be skipped."
            )

    # Compare new data with existing data
    if existing_data and existing_data.get("papers") == citation_data["papers"]:
        print("No changes in citation data. Skipping file update.")
        return

    try:
        with open(OUTPUT_FILE, "w") as f:
            yaml.dump(citation_data, f, width=1000, sort_keys=True)
        print(f"Citation data saved to {OUTPUT_FILE}")
    except Exception as e:
        print(
            f"Error writing citation data to {OUTPUT_FILE}: {e}. Please check file permissions and disk space."
        )
        sys.exit(1)


if __name__ == "__main__":
    try:
        get_scholar_citations()
        write_scholar_profile_and_timeseries()
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
