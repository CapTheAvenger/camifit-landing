#!/usr/bin/env python3
"""Holt die Besuchsstatistik der Landingpage (Cloudflare Web Analytics, GraphQL) und den
Mitgliederstand der Skool-Community und schreibt beides als Tageshistorie nach stats/daily.json.

Läuft täglich in GitHub Actions (.github/workflows/stats.yml). Braucht:
  CF_API_TOKEN   – Cloudflare-API-Token mit der Berechtigung „Account Analytics: Read" (Repo-Secret)
  CF_ACCOUNT_ID  – Cloudflare-Konto-ID (optional, Standard unten)
  CF_SITE_TAG    – Site-Tag der Web-Analytics-Site (optional, Standard unten)

Aufruf: python3 scripts/fetch_stats.py --out out/daily.json [--since 2026-10-28] [--refresh 3]

Die Datei enthält pro Berliner Kalendertag Besuche/Seitenaufrufe gesamt sowie nach Pfad, Land,
Referrer, Gerät, Browser und Stunde. Virtuelle Pfade (/clic-…, /ver-…, /tiempo-…, /entrada-…) sind
Ereignisse der Landingpage, keine echten Seiten (siehe README „Besuchsstatistik").
Die letzten --refresh Tage werden bei jedem Lauf neu geholt (Daten können nachlaufen), ältere Tage
bleiben, wie sie sind. Fehlt ein Tag seit --since, wird er nachgeholt.
"""
import argparse, datetime as dt, json, os, re, sys, time, urllib.request, urllib.error
from zoneinfo import ZoneInfo

ACCOUNT = os.environ.get("CF_ACCOUNT_ID", "8c6b5d8d1b12e338cb15ab2a547a249f")
SITE = os.environ.get("CF_SITE_TAG", "7dfa306a1adb40178a822cb7da1f6f33")
TOKEN = os.environ.get("CF_API_TOKEN", "")
GRAPHQL = "https://api.cloudflare.com/client/v4/graphql"
SKOOL_ABOUT = "https://www.skool.com/momlifecamila/about"
TZ = ZoneInfo("Europe/Berlin")
LAUNCH = "2026-10-28"
DIMS = {  # Alias → GraphQL-Dimension, Limit
    "paths": ("requestPath", 200),
    "countries": ("countryName", 200),
    "referers": ("refererHost", 100),
    "devices": ("deviceType", 20),
    "browsers": ("userAgentBrowser", 30),
    "hours": ("datetimeHour", 48),
}


def day_range_utc(day: dt.date):
    """Berliner Kalendertag → [Anfang, Ende] in UTC (ISO, Sekunden)."""
    start = dt.datetime.combine(day, dt.time.min, TZ)
    end = dt.datetime.combine(day, dt.time(23, 59, 59), TZ)
    f = lambda d: d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f(start), f(end)


def build_query(days):
    blocks = []
    for i, day in enumerate(days):
        geq, leq = day_range_utc(day)
        flt = f'filter:{{AND:[{{datetime_geq:"{geq}",datetime_leq:"{leq}"}},{{bot:0}},{{siteTag_in:["{SITE}"]}}]}}'
        blocks.append(f"d{i}_total: rumPageloadEventsAdaptiveGroups({flt}, limit:1){{count avg{{sampleInterval}} sum{{visits}}}}")
        for alias, (dim, lim) in DIMS.items():
            order = "" if dim == "datetimeHour" else ", orderBy:[sum_visits_DESC]"
            blocks.append(
                f"d{i}_{alias}: rumPageloadEventsAdaptiveGroups({flt}, limit:{lim}{order})"
                f"{{count avg{{sampleInterval}} sum{{visits}} dimensions{{metric: {dim}}}}}"
            )
    return "{ viewer { accounts(filter:{accountTag:\"%s\"}) { %s } } }" % (ACCOUNT, " ".join(blocks))


def graphql(query):
    req = urllib.request.Request(
        GRAPHQL, data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode())
            if data.get("errors"):
                raise RuntimeError("GraphQL-Fehler: " + json.dumps(data["errors"])[:2000])
            return data["data"]["viewer"]["accounts"][0]
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == 2:
                raise
            time.sleep(5 * (attempt + 1))


def pv(row):
    """Seitenaufrufe: count ist die Stichprobe, sampleInterval der Faktor (bei kleinem Traffic 1)."""
    return int(round(row.get("count", 0) * (row.get("avg", {}).get("sampleInterval") or 1)))


def norm_path(p):
    p = (p or "/").split("?")[0]
    if p.endswith("/index.html"):
        p = p[: -len("index.html")]
    if len(p) > 1 and p.endswith("/"):
        p = p[:-1]
    return p or "/"


def parse_day(acc, i):
    tot = acc.get(f"d{i}_total") or [{}]
    out = {"visits": int((tot[0].get("sum") or {}).get("visits", 0) or 0), "pageviews": pv(tot[0]) if tot else 0}
    for alias in DIMS:
        d = {}
        for row in acc.get(f"d{i}_{alias}") or []:
            key = (row.get("dimensions") or {}).get("metric", "")
            if alias == "paths":
                key = norm_path(key)
            elif alias == "referers" and not key:
                key = "(direkt)"
            elif not key:
                key = "(unbekannt)"
            e = d.setdefault(key, {"pv": 0, "visits": 0})
            e["pv"] += pv(row)
            e["visits"] += int((row.get("sum") or {}).get("visits", 0) or 0)
        out[alias] = d
    return out


def fetch_skool_members():
    """Mitgliederzahl (alle Stufen) von der öffentlichen Infoseite der Community. None bei Fehler."""
    req = urllib.request.Request(SKOOL_ABOUT, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
        "Accept-Language": "es,en;q=0.8",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            html = r.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        print("Skool nicht erreichbar:", e, file=sys.stderr)
        return None
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if m:
        try:
            data = json.loads(m.group(1))
            n = data["props"]["pageProps"]["currentGroup"]["metadata"]["totalMembers"]
            return int(n)
        except Exception as e:  # noqa: BLE001
            print("Skool-Daten unerwartet:", e, file=sys.stderr)
    m = re.search(r'"totalAdmins":\d+,"totalMembers":(\d+)', html)
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--since", default=LAUNCH)
    ap.add_argument("--refresh", type=int, default=3)
    ap.add_argument("--batch", type=int, default=6)
    ap.add_argument("--skip-skool", action="store_true")
    a = ap.parse_args()
    if not TOKEN:
        sys.exit("CF_API_TOKEN fehlt (Repo-Secret).")

    data = {"site": "momlifecamila.com", "timezone": "Europe/Berlin", "launch_date": LAUNCH, "days": {}, "skool": {}}
    if os.path.exists(a.out):
        with open(a.out, encoding="utf-8") as f:
            old = json.load(f)
        data["days"] = old.get("days", {})
        data["skool"] = old.get("skool", {})

    today = dt.datetime.now(TZ).date()
    since = dt.date.fromisoformat(a.since)
    wanted = []
    d = since
    while d <= today:
        key = d.isoformat()
        if key not in data["days"] or (today - d).days < a.refresh or data["days"][key].get("partial"):
            wanted.append(d)
        d += dt.timedelta(days=1)
    print(f"Tage zu holen: {[x.isoformat() for x in wanted]}")

    for start in range(0, len(wanted), a.batch):
        chunk = wanted[start:start + a.batch]
        acc = graphql(build_query(chunk))
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        for i, day in enumerate(chunk):
            rec = parse_day(acc, i)
            rec["fetched_at"] = now
            rec["partial"] = day == today  # heutiger Tag ist noch nicht komplett
            data["days"][day.isoformat()] = rec

    if not a.skip_skool:
        n = fetch_skool_members()
        if n is not None:
            data["skool"][today.isoformat()] = n
            print("Skool-Mitglieder:", n)
        else:
            print("Skool-Mitgliederzahl heute nicht ermittelbar.", file=sys.stderr)

    data["days"] = dict(sorted(data["days"].items()))
    data["skool"] = dict(sorted(data["skool"].items()))
    data["generated_at"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, sort_keys=False)
    tot_v = sum(x["visits"] for x in data["days"].values())
    print(f"geschrieben: {a.out} – {len(data['days'])} Tage, {tot_v} Besuche seit {LAUNCH}")


if __name__ == "__main__":
    main()
