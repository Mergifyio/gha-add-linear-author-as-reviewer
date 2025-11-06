# add-linear-author-as-reviewer

This project is a GitHub action that requests a review from the Linear issue author.

Usage example:

```
name: Linear automation

on:
  pull_request:
    branches: [ "main" ]
    types: [ "opened", "synchronize", "reopened", "edited" ]


permissions:
  pull-requests: write
  contents: read

jobs:
  add-linear-author-as-reviewer:
    runs-on: ubuntu-latest
    steps:
      - name: Add reviewers
        uses: Mergifyio/add-linear-author-as-reviewer@main
        with:
           GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
           LINEAR_API_KEY: ${{ secrets.LINEAR_API_KEY }}
           LINEAR_ISSUE_REGEX: "MRGFY-\d+"
           EMAIL_MAPPING: ${{ vars.EMAIL_MAPPING }}
           DEFAULT_REVIEWER: "gh_username_or_team"
```

The email mapping GitHub Action variables format is:

```
user1@example.com github-user-login-1
user2@example.com github-user-login-2
```
