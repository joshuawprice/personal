import json
from datetime import UTC, datetime
from time import sleep

import requests

TOKEN_URL = "https://api.myday.cloud/sessions/token"
CLIENT_ID = "myday-web-4e0f11f9-046e-4505-9cb8-db2152311e21"
CALENDAR_URL = "https://api.myday.cloud/legacy/api/aggregate/v2/calendaritem?$filter=End%20gt%20datetime%272026-09-28T00:00:00Z%27%20and%20Start%20lt%20datetime%272026-11-09T00:00:00Z%27"
ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjgwREU5MzQ2RjA5MEFGMDI4MjUwRjUyNzQ1QjMwMjkwMDYyM0RBQ0VSUzI1NiIsIng1dCI6ImdONlRSdkNRcndLQ1VQVW5SYk1Da0FZajJzNCIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgubXlkYXkuY2xvdWQiLCJuYmYiOjE3OTI2MjA1NzAsImlhdCI6MTc5MjYyMDU3MCwiZXhwIjoxNzkyNzA2OTcwLCJhdWQiOiJteWRheS13ZWItNGUwZjExZjktMDQ2ZS00NTA1LTljYjgtZGIyMTUyMzExZTIxIiwiYW1yIjpbImV4dGVybmFsIl0sIm5vbmNlIjoiTjAuMDM1NzM3MDkxNTc2ODgxMzIxNzkyNjIwNTIzNDUwIiwiY19oYXNoIjoiaXZhSGZhSTNxZkNEaXBpTjRidnhLdyIsInNpZCI6Ijc1OUE4RDFDQ0FBNDREMUZENTRDOTk4MzZEMzI4RUREIiwic3ViIjoiNmEwMDViNGQtMWM3ZS00MzM0LTg4NTUtMzI1NjZlZDc3MDZiIiwiYXV0aF90aW1lIjoxNzkyNjIwNTcwLCJpZHAiOiJhYWQiLCJteWRheV9zaWQiOiI3NTlBOEQxQ0NBQTQ0RDFGRDU0Qzk5ODM2RDMyOEVERCIsInJvbGUiOiJzdGQiLCJ0ZW5hbnQiOiI0ZTBmMTFmOS0wNDZlLTQ1MDUtOWNiOC1kYjIxNTIzMTFlMjEiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiIyNjIwNjUzQHN0dWRlbnQudXd0c2QuYWMudWsiLCJnaXZlbl9uYW1lIjoiSm9zaHVhIiwiZmFtaWx5X25hbWUiOiJQcmljZSIsIm5hbWUiOiJKb3NodWEgUHJpY2UgKDI2MjA2NTMpIiwiZW1haWwiOiIyNjIwNjUzQHN0dWRlbnQudXd0c2QuYWMudWsiLCJ1cGRhdGVkX2F0IjoiMjAyNi0wOS0yOVQxNDo0MjozOFoiLCJyb2xlX3Blcm1pc3Npb24iOlsiVGVuYW50UmVhZCIsIlVzZXJSZWFkIl0sIl9jbGFpbV9uYW1lcyI6eyJncm91cHMiOiJzcmMxIn0sIl9jbGFpbV9zb3VyY2VzIjp7InNyYzEiOnsiZW5kcG9pbnQiOiJodHRwczovL2F1dGgubXlkYXkuY2xvdWQvYXBpL2dyb3Vwc19jbGFpbXMifX19.pCNcJ2KhL_Ae31PYF_tz1BXCKTBc0YVeMyIAVEjGqN_KLFa_hnDcN-QSyC_sqbbNYKVpInubfAo3VxBdSdkPVD06wGQH9lS3hILaVSZRMPisQQvoHpTlQvwF9wdcyZ33XLbRDF3pdnY_0Sh43mW9hfJt3vUJCWxrcZrBd030IjavlLIIn498KFwLy3i_IsQ6bojOoIF5OPi0QUn6Y0GcVXddhxpP3vA1GfAHPuhQh19nadLZJ6iS1wIc31C_C04j5fwZY6H-DPyEKtEeEPODWmZ_MrxuPZTz64t2g4sPUQYSt5suesRsWLZ9pDeABqLfp3W9uq4fVYu-uGMusiq_B7V4iOMqO6AeNAn0vdLiuujddcTOg7QzJaLxBO8ZtsW8OTIoHGhtjGUpFHgFqFmmn9IY9jwjv0duk7wdFWCq0zNPROpgqqnwpyVmBEyXFzmBBQC1IyBODX4qZFf3MKYO2WZzl6xr7BF72g12cZiV8uBEEVqSkXhfpkebE4Ig0kuQdn6K-ClfYAmZXqokb2vRHQABM4gQ7QC5-UD72pTjOZI11lEZDe6AmNbq9Q-mlD6Mwx5ct510h6KgqlFT9KW4LIGe8doBOLVUHVlegOh0H7k1xjQPHcAUg7fsQRNmtKKnJM35KiTs3AyGrkaK-17GDbSS_Ex8vBgCZqXWgKXeN4s"
# This *is* from the device code on first auth
CODE = "3SpjGDNSijXN4rmdQlBFO5p9"


def renew():
    print("Renewing access token...")
    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "get_token",
            "client_id": CLIENT_ID,
            "id_token": ID_TOKEN,
            "code": CODE,
        },
    )
    r.raise_for_status()
    d = r.json()
    print(datetime.now(UTC))
    print("access_token:", d["access_token"])
    print("expires_in:", d["expires_in"])


while True:
    renew()
    sleep(3540)
