# linear-author-to-gh-reviewers

This project is a GitHub action that request review of the Linear author.

Usage example:

```
name: Linear automation

on:
  pull_request:
    branches: [ "main" ]
    types: [ "opened", "synchronize", "reopened", "edited" ]


permissions: write-all

jobs:
  add-linear-author-as-reviewer:
    runs-on: ubuntu-latest
    steps:
      - name: Add reviewers
        uses: Mergifyio/add-linear-author-as-reviewer@main
        with:
           GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
           LINEAR_API_KEY: ${{ secrets.LINEAR_API_KEY }}
           EMAIL_MAPPING: |
             sileht@mergify.com sileht
             jd@mergify.com jd
```
