import json
from datetime import UTC, datetime
from time import sleep

import requests

SESSION_EXTEND_URL = (
    "https://api.myday.cloud/sessions/session/D7ED518160E3111744562FB9A67D423E/extend"
)
TOKEN_URL = "https://api.myday.cloud/sessions/token"
CLIENT_ID = "myday-web-4e0f11f9-046e-4505-9cb8-db2152311e21"
CALENDAR_URL = "https://api.myday.cloud/legacy/api/aggregate/v2/calendaritem?$filter=End%20gt%20datetime%272026-09-28T00:00:00Z%27%20and%20Start%20lt%20datetime%272026-11-09T00:00:00Z%27"
ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjgwREU5MzQ2RjA5MEFGMDI4MjUwRjUyNzQ1QjMwMjkwMDYyM0RBQ0VSUzI1NiIsIng1dCI6ImdONlRSdkNRcndLQ1VQVW5SYk1Da0FZajJzNCIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgubXlkYXkuY2xvdWQiLCJuYmYiOjE3OTI2NjQ1MTgsImlhdCI6MTc5MjY2NDUxOCwiZXhwIjoxNzkyNzUwOTE4LCJhdWQiOiJteWRheS13ZWItNGUwZjExZjktMDQ2ZS00NTA1LTljYjgtZGIyMTUyMzExZTIxIiwiYW1yIjpbImV4dGVybmFsIl0sIm5vbmNlIjoiTjAuMjkyNzg0MTgzNTA2MjU0NTcxNzkyNjY0NDk5NDc4IiwiY19oYXNoIjoiMDdlc2loUnI0QmdkcC1FbjFGYzBGdyIsInNpZCI6IkQ3RUQ1MTgxNjBFMzExMTc0NDU2MkZCOUE2N0Q0MjNFIiwic3ViIjoiNmEwMDViNGQtMWM3ZS00MzM0LTg4NTUtMzI1NjZlZDc3MDZiIiwiYXV0aF90aW1lIjoxNzkyNjY0NTE4LCJpZHAiOiJhYWQiLCJteWRheV9zaWQiOiJEN0VENTE4MTYwRTMxMTE3NDQ1NjJGQjlBNjdENDIzRSIsInJvbGUiOiJzdGQiLCJ0ZW5hbnQiOiI0ZTBmMTFmOS0wNDZlLTQ1MDUtOWNiOC1kYjIxNTIzMTFlMjEiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiIyNjIwNjUzQHN0dWRlbnQudXd0c2QuYWMudWsiLCJnaXZlbl9uYW1lIjoiSm9zaHVhIiwiZmFtaWx5X25hbWUiOiJQcmljZSIsIm5hbWUiOiJKb3NodWEgUHJpY2UgKDI2MjA2NTMpIiwiZW1haWwiOiIyNjIwNjUzQHN0dWRlbnQudXd0c2QuYWMudWsiLCJ1cGRhdGVkX2F0IjoiMjAyNi0wOS0yOVQxNDo0MjozOFoiLCJyb2xlX3Blcm1pc3Npb24iOlsiVGVuYW50UmVhZCIsIlVzZXJSZWFkIl0sIl9jbGFpbV9uYW1lcyI6eyJncm91cHMiOiJzcmMxIn0sIl9jbGFpbV9zb3VyY2VzIjp7InNyYzEiOnsiZW5kcG9pbnQiOiJodHRwczovL2F1dGgubXlkYXkuY2xvdWQvYXBpL2dyb3Vwc19jbGFpbXMifX19.N30ci1o38joRNtUTIh4yxg5bUEYoKTawA6Yvx6dAd9yAwu0z5a3nU3MNYHAoI0JPkZDyMabt3ZqPc21S2wt-cymyoV7jQOnVrmklxHhVEjdnSqCcL1Qc9QC9AiJfXDisvJcN5gptNfKZ0JIFX17y8orBwO25jH09Cz9fuE9UYGa_LcB_y4-R1bQli4JCK3HA7jS5h19EP_uy7BHaImfW7yfvMDvLp_tuAd97ncICzPlKGHpXeWtsaTUwjeJfTvRKD-H_TzmEAqUDXejKlvZt_I-Z6Jen6n0V7gCEESDohQHO5McuRTYwiIPto_IXq65I4rjCYDhcg6uRGA3xGLffui4CYzGg-oQqMIFdW5IhWFCMY88VyerMcxhCdNV50VAeEXLSItOZkUVTnsdU4tYfFEWMHeC4m-OB7vOXztTIcmVe2d35SPhrQbLGmqqOxpvou_lICSZj8_g3yEDRJ_ZxGgXD49DBkJ2o_dJDEHe43XByhygY1sEwBqL750gPMPDr9HEf0gc5xPHCu6ZxfohX_Gcuvsr66vkRyIUFlF3vOCP1lcphRoTVhWILNozeTIIFlt68stmY65N85sG8wX7HiSCG9n4FoRDoHItPaCXhq0YQzmkeEon3dKOW7E5SXFHiywD3gTVnbUDyRU2DjS6YNtZlxhU3hd7fdL7HMdN8Rjs"
CODE = "9AaePpXVap5sLd7OrJSPIP8M"


def session_extend(token: str):
    print("Renewing access token...")
    r = requests.post(
        SESSION_EXTEND_URL,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    r.raise_for_status()
    d = r.json()
    print(datetime.now(UTC))
    print("sessionExpires:", d["sessionExpires"])
    print("sessionExpiresInSecs:", d["sessionExpiresInSecs"])


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
    return d["access_token"]


while True:
    access_token: str
    for i in range(4):
        access_token = renew()
        sleep(3540)

    session_extend(access_token)
