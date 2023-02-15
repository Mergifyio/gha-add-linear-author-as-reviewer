import os
import re
import sys

import httpx

REGEX = re.compile(r"MRGFY-\d+")


def main() -> None:
    linear_api_key = os.environ["INPUT_LINEAR_API_KEY"]
    pull_request_body = os.environ["INPUT_PULL_REQUEST_BODY"]
    raw_mapping = os.environ["INPUT_EMAIL_MAPPING"]

    email_mapping = {}
    for line in raw_mapping.split("\n"):
        if line:
            email, _, login = line.strip().partition(" ")
            email_mapping[email] = login.strip()

    linear_ids = REGEX.findall(pull_request_body)
    if not linear_ids:
        print("No linear ticket found")
        return

    issue_queries = ""
    for linear_id in linear_ids:
        issue_queries += f'{linear_id.replace("-", "_")}: issue(id: "{linear_id}") {{ creator {{ email }} }} '

    query = {"query": f"query {{ {issue_queries} }}"}
    print(query)

    with httpx.Client(
        base_url="https://api.linear.app",
        headers={"Content-Type": "application/json", "Authorization": linear_api_key},
    ) as linear:
        responses = linear.post("/graphql", json=query).json()
        if "error" in responses:
            print(responses)
            sys.exit(1)

        creators = ",".join(
            email_mapping[response["creator"]["email"]]
            for response in responses["data"].values()
            if response.get("creator") and response["creator"].get("email")
        )
        if creators:
            print(f"::set-output name=CREATORS::{creators}")


main()
