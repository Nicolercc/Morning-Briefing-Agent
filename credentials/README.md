# Credentials Directory

Put local Google credential JSON files here.

Expected personal Gmail setup:

```text
credentials/google_oauth_client.json
```

Do not commit JSON credential files. `.gitignore` excludes `credentials/*.json`.

The service-account JSON you mentioned is not the right default for personal
Gmail. Use it only if this project is later configured for Google Workspace
domain-wide delegation.
