# Streamlit Community Cloud Deployment

Streamlit Community Cloud can deploy this project for free from GitHub.

## Deploy

1. Push the GitHub-ready project to GitHub.
2. Go to `https://share.streamlit.io`.
3. Click **Create app**.
4. Choose your repository and branch.
5. Set:

```text
Main file path: streamlit_app.py
```

6. Deploy.

## Secrets

In Streamlit app settings, add secrets like:

```toml
fixed8_password = "your-login-password"
google_sheet_id = "your-google-sheet-id"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

Share the Google Sheet with the service account `client_email` as an editor.

## Important

If Google Sheets is not configured, paper trading records are stored on the Streamlit instance filesystem. That is fine for testing, but it is not reliable after app reboot or redeploy.
