import os
import json
import re
import sys

import httpx


def main() -> None:
    linear_api_key = os.environ["INPUT_LINEAR_API_KEY"]
    linear_issue_regex = os.environ["INPUT_LINEAR_ISSUE_REGEX"]
    pull_request_details = os.environ.get("INPUT_PULL_REQUEST_TITLE", "") + " " + os.environ.get("INPUT_PULL_REQUEST_BODY", "")
    raw_mapping = os.environ["INPUT_EMAIL_MAPPING"]

    email_mapping = {}
    for line in raw_mapping.split("\n"):
        if line:
            email, _, login = line.strip().partition(" ")
            email_mapping[email] = login.strip()

    linear_ids = re.findall(linear_issue_regex, pull_request_details)
    if not linear_ids:
        print("No linear ticket found", file=sys.stderr)
        return

    issue_queries = ""
    for linear_id in linear_ids:
        issue_queries += f'{linear_id.replace("-", "_")}: issue(id: "{linear_id}") {{ creator {{ email }} }} '

    query = {"query": f"query {{ {issue_queries} }}"}
    print(query, file=sys.stderr)

    with httpx.Client(
        base_url="https://api.linear.app",
        headers={"Content-Type": "application/json", "Authorization": linear_api_key},
        timeout=httpx.Timeout(timeout=15.0),
    ) as linear:
        raw_response = linear.post("/graphql", json=query)
        try:
            response_json = raw_response.json()
        except json.JSONDecodeError:
            print("Failed to decode JSON response", file=sys.stderr)
            print(raw_response.text, file=sys.stderr)
            sys.exit(1)

        if "error" in response_json:
            print(response_json, file=sys.stderr)
            sys.exit(1)

        try:
            creators = ",".join(
                email_mapping[response["creator"]["email"]]
                for response in response_json["data"].values()
                if response.get("creator") and response["creator"].get("email")
            )
            if creators:
                print(f"CREATORS={creators}")
        except Exception:
            print(response_json, file=sys.stderr)
            raise


main()
