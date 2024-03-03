import os

credentials = {
  "type": "service_account",
  "project_id": "endless-apogee-269606",
  "private_key_id": "6b1a0b598d929ecf24709a436a489ee7296ca06c",
  "private_key": os.environ["credentials_private_key"].replace('\\n', '\n'),
  "client_email": "js-job-wheel@endless-apogee-269606.iam.gserviceaccount.com",
  "client_id": "104807242441753118900",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/js-job-wheel%40endless-apogee-269606.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
