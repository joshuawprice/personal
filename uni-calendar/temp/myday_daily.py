# myday_daily.py
import base64
import hashlib
import json
import pathlib
import secrets
from html.parser import HTMLParser
from urllib.parse import parse_qs, quote, urlencode, urljoin, urlsplit, urlunsplit

import requests

CFG_FILE = pathlib.Path("myday_config.json")
cfg = json.loads(CFG_FILE.read_text())
AUTH_HOST = "auth.myday.cloud"


def b64url(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


class FormFields(HTMLParser):
    """Collects hidden <input> fields from a response_mode=form_post page."""

    def __init__(self):
        super().__init__()
        self.fields = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "input" and a.get("name"):
            self.fields[a["name"]] = a.get("value", "")


def silent_authorize(s):
    parts = urlsplit(cfg["authorize_url"])
    q = {k: v[0] for k, v in parse_qs(parts.query).items()}
    verifier = b64url(secrets.token_bytes(32))
    state = secrets.token_urlsafe(16)
    q.update(
        {  # response_type, scope, redirect_uri, response_mode stay as the browser sent them
            "code_challenge": b64url(hashlib.sha256(verifier.encode()).digest()),
            "code_challenge_method": "S256",
            "state": state,
            "nonce": secrets.token_urlsafe(16),
            "prompt": "none",  # never show a login page; fail instead
        }
    )
    url = urlunsplit(parts._replace(query=urlencode(q, quote_via=quote)))

    for _ in range(10):
        r = s.get(url, allow_redirects=False, timeout=30)
        if r.is_redirect:
            nxt = urljoin(url, r.headers["Location"])
            host = urlsplit(nxt).hostname
            if host == AUTH_HOST:
                url = nxt
                continue
            if host and "microsoftonline" in host:
                raise RuntimeError(
                    "Sent to Microsoft: auth.myday.cloud session expired. Re-copy cookies."
                )
            f = urlsplit(nxt)  # redirected back to myday with code in query/fragment
            resp = {k: v[0] for k, v in parse_qs(f.query).items()}
            resp.update({k: v[0] for k, v in parse_qs(f.fragment).items()})
            break
        p = FormFields()
        p.feed(r.text)  # form_post: code + id_token are hidden inputs
        resp = p.fields
        break
    else:
        raise RuntimeError("Too many redirects")

    if "error" in resp:
        raise RuntimeError(
            f"Silent login failed: {resp['error']}. "
            "login_required = log in via browser and re-copy the auth.myday.cloud cookies."
        )
    if resp.get("state") != state or "code" not in resp:
        raise RuntimeError(f"Unexpected authorize response, fields: {list(resp)}")
    return q, verifier, resp


def jwt_claims(tok):
    p = tok.split(".")[1]
    p += "=" * (-len(p) % 4)
    return json.loads(base64.urlsafe_b64decode(p))


def get_access_token(s):
    q, verifier, resp = silent_authorize(s)
    print("Authorize returned fields:", list(resp))
    idt = resp.get("id_token", "")
    print("id_token present:", bool(idt))
    if idt:
        c = jwt_claims(idt)
        print(
            "id_token claims:",
            {k: c.get(k) for k in ("iss", "aud", "exp", "nonce", "c_hash")},
        )

    body = {
        "grant_type": "authorization_code",
        "client_id": q["client_id"],
        "redirect_uri": q["redirect_uri"],
        "code": resp["code"],
        "code_verifier": verifier,
        "id_token": idt,
    }
    r = requests.post(
        cfg["token_url"], data=body, headers=cfg.get("extra_headers", {}), timeout=30
    )
    if not r.ok:
        print("Status:", r.status_code)
        print("Response headers:", dict(r.headers))
        print("Body:", r.text[:2000])
        r.raise_for_status()
    return r.json()["access_token"]


def main():
    s = requests.Session()
    for name, value in cfg["auth_cookies"].items():
        s.cookies.set(name, value, domain=AUTH_HOST, path="/")

    token = get_access_token(s)

    # Save any cookies the server refreshed, so the session can slide forward
    cfg["auth_cookies"] = {
        c.name: c.value for c in s.cookies if c.domain.lstrip(".") == AUTH_HOST
    }
    CFG_FILE.write_text(json.dumps(cfg, indent=2))
    CFG_FILE.chmod(0o600)

    api = requests.get(
        cfg["api_url"], headers={"Authorization": f"Bearer {token}"}, timeout=30
    )
    api.raise_for_status()
    print(api.json())


if __name__ == "__main__":
    main()
