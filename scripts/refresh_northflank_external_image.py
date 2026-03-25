#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


API_BASE = "https://api.northflank.com/v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Restart a Northflank service that already uses an external image.")
    parser.add_argument("--dry-run", action="store_true", help="Print the request target without calling the API.")
    return parser.parse_args()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def restart_service(api_token: str, project_id: str, service_id: str, dry_run: bool) -> None:
    url = f"{API_BASE}/projects/{project_id}/services/{service_id}/restart"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
        "User-Agent": "northflank-refresh-external-image/1.0",
    }

    if dry_run:
        print(json.dumps({"dry_run": True, "method": "POST", "url": url}, ensure_ascii=False))
        return

    request = urllib.request.Request(url, headers=headers, data=b"{}", method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Northflank HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Northflank network error: {exc}") from exc

    print(json.dumps({"success": True, "project_id": project_id, "service_id": service_id, "response": payload}, ensure_ascii=False))


def main() -> int:
    args = parse_args()
    api_token = require_env("NF_API_TOKEN")
    # Replace these example values with your own Northflank project ID and service ID.
    project_id = "a86"
    service_id = "b94"
    restart_service(api_token, project_id, service_id, args.dry_run)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[FATAL] {exc}", file=sys.stderr)
        raise
