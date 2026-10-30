#!/usr/bin/env python3
"""Rechnet aus stats/daily.json (Branch stats) die Kennzahlen für den Tagesblick (Artefakt „Tagesblick momlifecamila").

Aufruf (in der täglichen Claude-Aufgabe):
  curl -sS -o daily.json https://raw.githubusercontent.com/CapTheAvenger/camifit-landing/stats/daily.json
  python3 report_stats.py --in daily.json --out report.json [--today 2026-10-30]

Ausgabe report.json: Zeiträume gestern / Vortag / 7 Tage / Vorwoche / seit Start mit Besuchen, DE-Anteil, Trichter-Ereignissen,
Skool-Klicks, Quoten; Tagesreihe; Herkunft (7 Tage); Skool-Mitglieder. Die Aufgabe ergänzt „insights" (Learnings/To-dos) und
schreibt alles als Dokument reports/latest in die Datenbank des Artefakts.
Definitionen: siehe Projektdokument claude/landingpage-auswertung.md.
"""
import argparse, datetime as dt, json, sys

CLICK_PATHS = {"vip": "/clic-skool-vip", "vip2": "/clic-skool-vip-2cuotas", "premium": "/clic-skool-premium", "standard": "/clic-skool-standard"}
EVENT_PATHS = {"t30": "/tiempo-30s", "t2min": "/tiempo-2min", "video": "/ver-video", "precios": "/ver-precios",
               "detalles": "/ver-detalles", "guia": "/ver-guia", "final": "/ver-final", "wa": "/clic-whatsapp", "bf": "/clic-bf"}


def pv(day, path):
    return int((day.get("paths", {}).get(path) or {}).get("pv", 0) or 0)


def agg(days):
    """Summen über eine Liste von Tagesdatensätzen."""
    out = {"days": len(days), "visits": 0, "visits_de": 0, "pv_home": 0, "clicks": {k: 0 for k in CLICK_PATHS}, "events": {k: 0 for k in EVENT_PATHS}, "entradas": {}}
    for d in days:
        out["visits"] += int(d.get("visits", 0) or 0)
        out["visits_de"] += int((d.get("countries", {}).get("DE") or {}).get("visits", 0) or 0)
        out["pv_home"] += pv(d, "/")
        for k, p in CLICK_PATHS.items():
            out["clicks"][k] += pv(d, p)
        for k, p in EVENT_PATHS.items():
            out["events"][k] += pv(d, p)
        for p, v in d.get("paths", {}).items():
            if p.startswith("/entrada-"):
                out["entradas"][p[len("/entrada-"):]] = out["entradas"].get(p[len("/entrada-"):], 0) + int(v.get("pv", 0) or 0)
    out["clicks"]["total"] = sum(out["clicks"][k] for k in CLICK_PATHS)
    v = out["visits"]
    def rate(n):
        return round(100.0 * n / v, 1) if v else None
    out["rates"] = {"t30": rate(out["events"]["t30"]), "video": rate(out["events"]["video"]), "precios": rate(out["events"]["precios"]),
                    "detalles_guia": rate(out["events"]["detalles"] + out["events"]["guia"]), "clicks": rate(out["clicks"]["total"]),
                    "de": rate(out["visits_de"])}
    out["visits_ohne_de"] = v - out["visits_de"]
    return out


def top(days, key, n, exclude=()):
    acc = {}
    for d in days:
        for k, v in d.get(key, {}).items():
            if k in exclude:
                continue
            acc[k] = acc.get(k, 0) + int(v.get("visits", 0) or 0)
    items = sorted(acc.items(), key=lambda t: -t[1])
    return [[k, c] for k, c in items if c > 0][:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--today", default=None, help="Berliner Datum JJJJ-MM-TT (Standard: heute)")
    a = ap.parse_args()
    with open(a.inp, encoding="utf-8") as f:
        data = json.load(f)
    try:
        from zoneinfo import ZoneInfo
        today = dt.date.fromisoformat(a.today) if a.today else dt.datetime.now(ZoneInfo("Europe/Berlin")).date()
    except Exception:
        today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    days = {k: v for k, v in data.get("days", {}).items() if not v.get("partial")}
    launch = data.get("launch_date", "2026-10-28")
    y = today - dt.timedelta(days=1)
    def rng(a_, b_):  # inkl. Grenzen
        out = []
        d = a_
        while d <= b_:
            if d.isoformat() in days:
                out.append(days[d.isoformat()])
            d += dt.timedelta(days=1)
        return out
    periods = {
        "yesterday": agg(rng(y, y)),
        "daybefore": agg(rng(y - dt.timedelta(days=1), y - dt.timedelta(days=1))),
        "7d": agg(rng(y - dt.timedelta(days=6), y)),
        "prev7d": agg(rng(y - dt.timedelta(days=13), y - dt.timedelta(days=7))),
        "all": agg([days[k] for k in sorted(days)]),
    }
    series = []
    for k in sorted(days):
        d = days[k]
        series.append({"date": k, "visits": int(d.get("visits", 0) or 0), "visits_de": int((d.get("countries", {}).get("DE") or {}).get("visits", 0) or 0),
                       "clicks": sum(pv(d, p) for p in CLICK_PATHS.values()), "precios": pv(d, "/ver-precios"), "t30": pv(d, "/tiempo-30s"), "video": pv(d, "/ver-video")})
    week = rng(y - dt.timedelta(days=6), y)
    origins = {"countries": top(week, "countries", 8), "referers": top(week, "referers", 6, exclude=("momlifecamila.com",)),
               "devices": top(week, "devices", 4), "browsers": top(week, "browsers", 6), "entradas": periods["7d"]["entradas"]}
    hours = [0] * 24
    for d in week:
        for h, v in d.get("hours", {}).items():
            try:
                hours[int(h[11:13])] += int(v.get("visits", 0) or 0)
            except Exception:
                pass
    sk = data.get("skool", {})
    sk_dates = sorted(sk)
    skool = {"latest": sk[sk_dates[-1]] if sk_dates else None, "latest_date": sk_dates[-1] if sk_dates else None, "series": [[k, sk[k]] for k in sk_dates]}
    def delta(d1, d0):
        return (sk[d1] - sk[d0]) if (d1 in sk and d0 in sk) else None
    skool["delta_yesterday"] = delta(today.isoformat(), y.isoformat())
    skool["delta_7d"] = delta(today.isoformat(), (y - dt.timedelta(days=6)).isoformat())
    notes = []
    if today.isoformat() in data.get("days", {}) and data["days"][today.isoformat()].get("partial"):
        notes.append("Heutiger Tag ist unvollständig und nicht enthalten.")
    gen = data.get("generated_at")
    if gen:
        try:
            age_h = (dt.datetime.now(dt.timezone.utc) - dt.datetime.strptime(gen, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)).total_seconds() / 3600
            if age_h > 20:
                notes.append(f"Datenstand veraltet ({age_h:.0f} h alt) – Workflow „Landingpage-Statistik“ prüfen.")
        except Exception:
            pass
    missing = [ (y - dt.timedelta(days=i)).isoformat() for i in range(7) if (y - dt.timedelta(days=i)) >= dt.date.fromisoformat(launch) and (y - dt.timedelta(days=i)).isoformat() not in days ]
    if missing:
        notes.append("Fehlende Tage in den letzten 7: " + ", ".join(sorted(missing)))
    report = {"generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "data_generated_at": gen, "launch_date": launch,
              "today": today.isoformat(), "yesterday": y.isoformat(), "periods": periods, "series": series, "origins7d": origins, "hours7d_utc": hours,
              "skool": skool, "notes": notes}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    p = periods
    print(f"gestern {p['yesterday']['visits']} Besuche ({p['yesterday']['visits_de']} DE), Klicks {p['yesterday']['clicks']['total']} | 7 Tage {p['7d']['visits']} Besuche, Klicks {p['7d']['clicks']['total']} | seit Start {p['all']['visits']} | Skool {skool['latest']} ({skool['delta_yesterday']})")


if __name__ == "__main__":
    main()
