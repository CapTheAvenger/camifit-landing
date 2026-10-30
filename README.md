# Landingpage Camila Haushalter · Plan Trimestral

Eine einzelne, selbstständige HTML-Seite (`index.html`), keine Abhängigkeiten außer Google Fonts.
Sprache der Seite: Spanisch (Lateinamerika). Alle Preise in USD.

Dateien:

| Datei | Zweck |
| --- | --- |
| `index.html` | Die Seite. Vollständiges HTML, direkt deploybar. Hier wird gearbeitet. |
| `aviso-legal.html`, `privacidad.html`, `terminos.html` | Impressum (ES+DE), Datenschutzerklärung (ES), AGB + Widerrufsbelehrung (ES). Gemeinsames Stylesheet `assets/legal.css`. |
| `assets/` | Fotos, Video, Schriften (siehe unten). |
| `artifact/` | Nur für die Vorschau als Claude-Artefakt; wird von `build_artifact.py` erzeugt. Nicht von Hand bearbeiten, nicht deployen. |
| `calls-synthese.md` | Auswertung der fünf Verkaufscalls (Copy-Grundlage). |

## Kaufweg über Skool (Stand 27.10.2026, 17 Uhr)

Skool hat **keine eigenen Checkout-Links pro Preis**, aber der Stufenwähler `/plans` nimmt den Parameter
`?tier=vip|premium|standard` entgegen (Hausi hat die Seite `skool.com/momlifecamila/plans` am Handy
entdeckt; Parameter im Skool-Seitencode `pages/[group]/plans` geprüft: `router.query.tier` → Stufe wird
vorgewählt, Parameter aus der URL entfernt; bei **eingeloggten** Nutzerinnen öffnet sich sofort der
Kauf-Dialog der Stufe, bei ausgeloggten greift die Vorwahl erst, sobald `self` da ist, also nach der
Kontoanlage – ob Skool nach der Registrierung auf dieselbe URL zurückkehrt, am Handy ausgeloggt testen).
Deshalb zeigen die Kauf-Buttons seit 27.10. direkt auf `/plans?tier=…` statt auf die Infoseite; das spart
den Schritt Infoseite → „Join“. **Ausgeloggt geprüft (27.10., 19 Uhr, Browser der Claude-App ohne Skool-Konto):** die Plan-Seite
öffnet trotz Parameter mit dem Standard-Tab; „Trete VIP bei“ öffnet das Registrierformular in der Seite, die URL mit
`tier=vip` bleibt erhalten, sodass Skool nach der Registrierung laut Code den VIP-Kauf öffnet. Weil die Vorwahl ohne Konto
nicht geht, zeigt die Seite seit 20 Uhr beim Klick auf „Empezar“/„Unirme“ den **Kauf-Wegweiser** (`guiaCompra`):
ein Dialog mit nachgebauter Skool-Tableiste (Standard | Premium | **VIP**), Finger-Hinweis „Toca VIP“, 3 Schritten
(Tab → Beitreten + Konto → anual/mensual je nach Auswahl) und dem Button „Ir a Skool y comprar“. Unter jedem Button steht
außerdem, welche Stufe/Option zu wählen ist:

| Angebot auf der Seite | Stufe in Skool | Hinweistext (Feld in `CAMI_CONFIG`) |
| --- | --- | --- |
| Pago completo 347 USD | VIP → anual (Einmalzahlung für 3 Monate; Team kündigt die Verlängerung) | `hintFull` |
| 2 cuotas 174 USD | VIP → mensual (2 Abbuchungen; Team kündigt nach der 2.) | `hint2x` |
| Comunidad CORE 29 USD/mes | Premium → mensual (oder anual 119) | `hintSkool` |
| Cita de evaluación 29 USD | Estándar (Einmalzahlung; Cita + 2 Wochen Zugang; Skool zeigt „anual", Team kündigt sofort) | `hintCita` |

Logged-out-Ansicht der Skool-Seite geprüft (26.10.): Überschrift „$29/year", Button „Join", darunter der
Block „Opciones al unirte" mit den drei Einstiegen. Die Stufenauswahl selbst erscheint erst nach der
Kontoanlage; das lässt sich ohne echtes Testkonto nicht ansehen.

## Konfiguration

Alles steht in `index.html` im Block `CAMI_CONFIG` (im `<head>`):

| Feld | Was rein muss | Stand | Verhalten, solange leer |
| --- | --- | --- | --- |
| `skoolUrl` | Gruppen-Infoseite, Fallback für leere Links | `https://www.skool.com/momlifecamila/about` | Kaufbutton ausgegraut (sollte nie leer sein) |
| `checkoutFull`, `checkout2x` | Stufenwähler mit VIP vorgewählt | `https://www.skool.com/momlifecamila/plans?tier=vip` | = `skoolUrl` |
| `comunidadUrl` | Stufenwähler mit Premium vorgewählt (Button „Unirme a la comunidad") | `…/plans?tier=premium` | = `skoolUrl` |
| `citaUrl` | Stufenwähler mit Estándar vorgewählt. Alternativ `whatsappUrl` eintragen, wenn Interessentinnen erst persönlich schreiben sollen | `…/plans?tier=standard` | = `skoolUrl` mit Hinweis Estándar |
| `hintFull`, `hint2x`, `hintSkool`, `hintCita` | Hinweistexte unter den Buttons (Spanisch) | gesetzt | ausgeblendet |
| `guiaCompra` | `true` = Kauf-Wegweiser (Dialog mit nachgebauter Skool-Tableiste, markierter Stufe und 3 Schritten) vor dem Absprung zu Skool; `false` = direkt zu Skool | `true` (seit 27.10., 20 Uhr) | |
| `whatsappUrl` | WhatsApp-Link | `wa.me/4917623749515` mit vorbelegtem Text (seit 27.10.; vorher wa.link-Kurzlink = Drittanbieter) | |
| `videoFile` | Pfad zum selbst gehosteten Verkaufsvideo | `assets/video.mp4` (liegt drin, 30 MB, 1024×576, 5:30 min – Originalqualität, Entscheidung Hausi) | wenn leer: siehe `videoEmbedUrl` |
| `videoAutoplay` | `true` = Autostart stumm mit Ton-Knopf (seit 27.10.); `false` = Poster mit Play-Button | `true` | |
| `videoEmbedUrl` | Alternative: Einbettungs-Link (YouTube/Vimeo), nur wenn `videoFile` leer ist | leer | sind beide leer, zeigt der Hero „Video en producción" (`videoMostrarSinUrl: true`) bzw. blendet den Player aus (`false`) |
| `legalUrl`, `privacyUrl`, `termsUrl` | Impressum, Datenschutz, AGB | `aviso-legal.html`, `privacidad.html`, `terminos.html` | Footer-Links und der Satz „Al pagar aceptas…" unter dem Kaufbutton ausgeblendet |

Launch-Mechanik (Doc „Plan de lanzamiento · Noviembre"), ebenfalls in `CAMI_CONFIG`:

| Feld | Bedeutung | Pflege |
| --- | --- | --- |
| `cuposTotal` | Zahl der neuen 1:1-Mamás im Monat. **Aktuell 0** = Cupos-Zeilen komplett aus (Entscheidung Hausi 27.10.: Knappheit erst einsetzen, wenn das Projekt größer ist). Zum Einschalten z. B. 10 eintragen | später |
| `cuposRestantes` | verbleibende Plätze; bei 0 wird der Kaufbutton zur Warteliste (WhatsApp) und die Zahlungsauswahl gesperrt | nach jeder Buchung um 1 senken (Hausi, montags) |
| `cuposMes`, `listaEsperaMes` | Monatsnamen in den Texten | pro Launch-Monat |
| `precioHasta` | bis wann 347 als „precio de lanzamiento" gilt; "" = ohne Datum | am 1. Dezember entscheiden: Preis ändern oder Datum verlängern mit neuem Grund |
| `bonoHasta` | festes Enddatum des Bonus für alle, aktuell `"2026-11-30"` (bis 23:59 Ortszeit der Besucherin). Countdown „Quedan 34 días 11 h“ bis zu einem echten Datum, kein localStorage. Entscheidung Hausi 27.10. statt 72-h-Timer (UWG Anhang Nr. 7). **Nicht** jeden Monat denselben Bonus mit neuem Datum verlängern (BGH: eine „nur bis…“-Aktion, die planmäßig verlängert wird, ist irreführend) – siehe Abschnitt Launch-Mechanik unten | pro Launch |
| `bonoActivo`, `bonoHoras`, `bonoTexto` | `bonoHoras` ist seit 27.10. **0** (72-h-Timer pro Browser abgeschaltet). Wird er je wieder eingeschaltet, muss der localStorage-Absatz in `privacidad.html` (Ziff. 2 und 4) zurück. `bonoActivo: false` blendet den Bonus komplett aus | – |

Ehrlicher Kaufdruck (Stand 27.10.): Erlaubt ist alles, was wahr ist. (1) Launch-Bonus mit echtem Enddatum (November: `bonoHasta`).
Danach entweder ein **anderer** Bonus mit neuem Grund (Dezember: z. B. „bono navideño“ mit anderem Inhalt) oder gar keiner – derselbe
Bonus mit monatlich neuem Datum wäre eine planmäßig verlängerte Frist und damit wieder irreführend. (2) Echte Knappheit: `cuposTotal`/
`cuposRestantes` zeigen die wirklich freien 1:1-Plätze; das ist der dauerhafte, legale Kaufdruck, solange die Zahl gepflegt wird.
(3) Für Interessentinnen aus DM/Cita: „Bono de decisión rápida“ – Bonus nur, wenn der Kauf innerhalb von 7 Tagen nach Cita oder
erstem Kontakt erfolgt. Das kann Camila prüfen (Datum des Calls/der DM ist bekannt) und muss es konsequent tun; dann ist die
Aussage wahr und auf der Seite nennbar („Si decides en los 7 días siguientes a tu cita o a tu primer mensaje…“).

Zahlungsoptionen: nur Vollzahlung 347 USD und 2 × 174 USD. Die Option 3 × 130 USD wurde am 22.10.2026
gestrichen, weil Skool sie nicht abbilden kann (siehe `skool-umstellung-runbook.md` im Projekt).

## Rechtsseiten (Pflicht, Betreiberin sitzt in Deutschland)

- `aviso-legal.html`: Impressum nach § 5 DDG, zweisprachig (Spanisch oben, Deutsch unten), mit VSBG-Hinweis.
  Kein Link zur EU-ODR-Plattform (eingestellt im Juli 2025).
- `privacidad.html`: Datenschutzerklärung auf Spanisch (Sprache der Kundinnen, Art. 12 DSGVO). Beschreibt genau
  diese Seite: GitHub Pages (Server-Logs), kein Cookie/Analytics, localStorage für den 72-h-Bonus, selbst gehostete
  Schriften und Video, Links zu Instagram/WhatsApp/Skool, Kauf in Skool, Gesundheitsdaten im 1:1 (Art. 9, ausdrückliche
  Einwilligung im Formulario de inicio), Google Forms, Calendly/Meet, Aufbewahrung, Rechte.
- `terminos.html`: AGB auf Spanisch (die Kundin muss sie verstehen können, sonst werden sie nicht Vertragsbestandteil),
  mit Leistungsbeschreibung aller vier Angebote, Vertragsschluss über Skool, 2-Raten-Verpflichtung, Laufzeiten,
  Gesundheitshinweis, Haftung, gesetzlicher Widerrufsbelehrung (14 Tage) samt Muster-Widerrufsformular,
  deutsches Recht. **Keine Geld-zurück-Garantie mehr** (Entscheidung Hausi 27.10., 19:50: „Es gibt keine Möglichkeit, Geld zurückzubekommen“ – Garantie von Seite, AGB Ziff. 9, Datenschutz, FAQ, OG-Text und Zapier-Mail v3 entfernt; AGB jetzt Ziff. 1–11).
- Betreiberangaben sind eingetragen (26.10.): Maria Camila Haushalter, Hauptstraße 21a, 14624 Dallgow-Döberitz,
  camifit4u@gmail.com, +49 176 23749515; Aufsichtsbehörde LDA Brandenburg. Keine USt-IdNr. vorhanden, deshalb
  keine Zeile dazu. Die Steuernummer gehört **nicht** ins Impressum (nicht vorgeschrieben, Missbrauchsrisiko).
- Die Texte sind sorgfältig erstellt, aber keine Rechtsberatung. Vor dem Livegang einmal von einer Anwältin oder
  einem Generator-Anbieter (z. B. eRecht24) gegenlesen lassen, vor allem Widerruf und Gesundheitsdaten.
- Unabhängig geprüft am 26.10. (Prüfagent, 31 Befunde); alle Text-Befunde sind eingearbeitet. Drei Punkte liegen
  **außerhalb der Seite** und müssen im Betrieb passieren, sonst greifen die AGB nicht:
  1. **Skool-Infoseite muss die AGB verlinken** (sonst sind sie beim Kauf nicht einbezogen, § 305 BGB, und die
     Widerrufsfrist läuft bis 12 Monate + 14 Tage). In den Block „Opciones al unirte" aufnehmen:
     „Al unirte aceptas los Términos y condiciones de Camila, incluida la información sobre tu derecho de
     desistimiento: https://momlifecamila.com/terminos.html · Política de privacidad: https://momlifecamila.com/privacidad.html".
     (Erst eintragen, wenn die Seite unter der Domain erreichbar ist – vorher wären es tote Links.)
     Außerdem die Stufen dort so benennen wie auf der Seite: „Nivel Estándar («Entrada»)", „Nivel Premium =
     Comunidad CORE", „Nivel VIP = Programa 1:1". → Auftrag für den Skool-Runbook-Chat.
  2. **Bestätigungs-E-Mail nach jedem Kauf** (§ 312f BGB): **erledigt, automatisch** (27.10.). Zapier-Zap „Skool: confirmación
     de compra (AGB + desistimiento)“ im Zapier-Konto camifit4u: Auslöser Skool „New Paid Member“ (alle 15 min, liefert Name +
     E-Mail, keine Stufe) → Gmail von camifit4u an die Kundin. Inhalt: nächste Schritte für alle drei Stufen mit Kurs-Links,
     Hinweis auf die Skool-Direktnachricht, komplette AGB inkl. Widerrufsbelehrung und Muster-Widerrufsformular im Mailtext
     (Text: `plantilla-correo-confirmacion.md`). Testmail an camifit4u verschickt und geprüft. Zapier-Pro-Test endet 10.11.,
     danach Free-Plan (100 Mails/Monat, 2-Schritt-Zap – der Zap hat genau 2 Schritte). Bei Textänderungen an den AGB den
     Mailtext im Zap nachziehen.
     Zusätzlich ist in Skool die **automatische Direktnachricht an neue Mitglieder** eingeschaltet (Text mit den drei Einstiegen
     und den Kurs-Links, 294/300 Zeichen).
  3. **Pflicht-Häkchen „ausdrückliches Verlangen"** im Formulario de inicio (Google Forms,
     `claude/formulario-inicio-apps-script.gs` im Projekt) und in den Calendly-Vorfragen. Ohne gültige Erklärung
     kann die Kundin nach Diagnose, Rutina, Menú und 2 Wochen Betreuung innerhalb von 14 Tagen widerrufen und
     100 % zurückverlangen. Text: „☐ Quiero que Camila empiece a prestar el servicio (diagnóstico, rutina, menú,
     acompañamiento y acceso a la comunidad) antes de que termine el plazo de desistimiento de 14 días. Sé que, si
     desisto después, deberé pagar la parte proporcional del servicio ya prestado, y que el derecho de desistimiento
     se extingue cuando el servicio se haya prestado por completo." Die AGB (Ziff. 8) verweisen genau auf dieses
     Häkchen. Dazu im selben Formular das Einwilligungs-Häkchen für Gesundheitsdaten (Art. 9 DSGVO), auf das die
     Datenschutzerklärung (Ziff. 8) verweist.
- Entscheidungen, die noch offen sind (siehe Chat vom 26.10.): Evergreen-Timer 72 h (UWG-Risiko, Vorschlag:
  festes Datum), Google Workspace statt privatem Gmail für Gesundheitsdaten (AV-Vertrag), „nutricionista",
  (WhatsApp-Link: erledigt, wa.me seit 27.10.)
- Hinweis zur Ratenzahlung: Die AGB sagen, dass die 2. Rate auch bei Kündigung in Skool geschuldet bleibt
  („Compromiso de 2 cuotas", Entscheidung 23.10.). Durchsetzen lässt sich das bei Kundinnen in Kolumbien praktisch
  kaum; die Klausel hält aber die Erwartung klar.
- Schriften: Abril Fatface und Poppins liegen jetzt in `assets/fonts/` (SIL Open Font License, Lizenzdateien dabei)
  und werden per `@font-face` geladen. Keine Anfrage mehr an Google-Server.

Video: Die Seite spielt `assets/video.mp4` direkt ab (HTML5-Player, kein YouTube/Vimeo, also keine
Drittanbieter-Cookies). **Seit 27.10. (Hausi): Autostart.** Das Video läuft beim Seitenaufruf von selbst,
stumm (Browser erlauben Autostart nur ohne Ton), mit dem Knopf „Toca para activar el sonido", der den Ton
einschaltet, von vorn startet und die Bedienleiste einblendet. Der Button „Ver el video" im Hero ist weg.
Blockiert der Browser den Autostart (oder Datensparmodus / „reduzierte Bewegung"), bleibt das Poster mit
Play-Button wie vorher (Click-to-load mit Ton). Schalter: `videoAutoplay` in `CAMI_CONFIG`.
Entscheidung Hausi (27.10., 18:30): **Originalqualität bleibt** (1024×576, H.264/AAC, 30 MB, 5:30 min) – wer
nicht schauen will, drückt Stopp. Eine komprimierte Fassung (854×480, 13,8 MB) war kurz live und liegt als
Reserve in der Sitzung; bei Bedarf: `ffmpeg -i video-original.mp4 -vf "hqdn3d=2:1.5:4:4,scale=854:480" -c:v libx264
-preset slow -crf 30 -profile:v main -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 64k -ac 2 -ar 44100 video.mp4`.
Wer das Video austauscht: gleiche Datei überschreiben (`assets/video.mp4`), mit dem Befehl oben komprimieren
(sonst lädt jede Besucherin die volle Datei). Alternative ohne Datei: `videoFile: ""`
und `videoEmbedUrl` als `https://www.youtube-nocookie.com/embed/VIDEO_ID` bzw.
`https://player.vimeo.com/video/VIDEO_ID?dnt=1`.
Für die Claude-Artefakt-Vorschau nutzt `build_artifact.py` automatisch die kleinere `artifact/video-preview.mp4`
(Limit 15 MB je Datei); diese Datei gehört nicht ins Deployment.

## Bilder

Ordner `assets/`, Dateinamen genau so:

| Datei | Verwendung | Format |
| --- | --- | --- |
| `video.mp4` | Das Verkaufsvideo in Originalqualität (Kopie `video-original.mp4` nur lokal) | liegt drin |
| `video-poster.jpg` | Vorschaubild des Video-Players im Hero vor dem Klick (Foto 1 im Querformat, 1280×720) | liegt drin |
| `camila-hero.jpg` | Reserve (Foto 1 im Hochformat), aktuell nicht verwendet | liegt drin |
| `camila-about.jpg` | Abschnitt „Hola, soy Cami" | liegt drin (Foto 4 vom 23.10., 960×1200) |
| `antes-despues-1.jpg` … `-6.jpg` | Ergebnisse, 6 Kacheln (liegen bereits drin; Einverständnis der Kundinnen vorausgesetzt) | quadratisch, 1200 px |
| `og.jpg` | Vorschaubild beim Teilen per WhatsApp/Instagram | liegt drin (1200×630); nur noch die Domain in `og:image` eintragen |

Alle Bilder liegen bereits in `assets/`. Fehlt eines, zeigt die Seite an seiner Stelle einen beschrifteten Platzhalter.
`og:image` zeigt auf `https://momlifecamila.com/assets/og.jpg` (absolute URL, seit 27.10. eingetragen).

## Texte, die Camila noch liefern oder bestätigen muss

- Testimonials: die fünf Community-Posts (Dulce, Suleimy, Daniela, Alejandra, Karina) liegen als Screenshots in `assets/testimonio-1.jpg` … `-5.jpg`. Nur der Nachname ist unkenntlich gemacht, Profilbild und Vorname bleiben. Wenn die Frauen einer Veröffentlichung mit vollem Namen zustimmen, die Dateien einfach durch die Originale ersetzen (gleiche Dateinamen). Einverständnis für die Veröffentlichung an sich bitte einholen.
- Berufsbezeichnung: geklärt 27.10. Camila hat bei OTL (Online Trainer Lizenz) Ernährungscoach, Personal Coach und Trainer-A/B-Lizenz gemacht, kein Hochschulstudium Ernährung. „Nutricionista" ist in Kolumbien ein geschützter Hochschulberuf, deshalb steht jetzt überall „entrenadora postparto y coach de nutrición certificada" (Seite, Footer, Meta, Aviso legal mit Nennung der OTL-Zertifikate). Instagram-Bio sollte Camila bei Gelegenheit angleichen.
- Preisrahmen: Die Seite zeigt keinen Streichpreis. $597 USD ist der Preis „con arranque en llamada con Cami" (Start über persönliche Beratung/Buchung bei Cami), $347 USD der Preis beim Start direkt über die Seite. Das ist nur dann sauber, wenn Camila bei Direktanfragen (DM/Call) tatsächlich 597 nennt bzw. ein entsprechendes Skool-Produkt existiert (offener Punkt im Skool-Runbook-Chat). Das Video nennt ebenfalls 347 USD.
- Raten: Die Seite verspricht „nach der zweiten Cuota wird nichts mehr abgebucht". Skool kennt keine Ratenpläne mit festem Ende; das 174-$-Abo muss nach der 2. Zahlung manuell gekündigt werden (Routine in Abschnitt 6 des Runbooks). Das Versprechen gilt nur, wenn diese Routine zuverlässig läuft.
- Die Community heißt auf der Seite durchgehend „Comunidad CORE" (in den Calls: „ya no se llama Booty Club"). Die PDF der Präsentation ist an der Stelle veraltet.
- „Rutina personalizada": geklärt 27.10. (Hausi): 1:1-Kundinnen bekommen einen individuellen Trainingsplan, die Comunidad-Routinen sind für alle gleich. Seite und AGB sagen deshalb „rutina personalizada" / „plan de entrenamiento personalizado". Der Skool-Nutzentext für VIP („rutinas de la comunidad") ist damit zu vorsichtig formuliert, stört aber nicht.
- „Hipopresivos" wurde am 26.10. aus der Comunidad-CORE-Karte gestrichen, weil der Kurs in Skool für Premium nicht enthalten ist (25 USD extra). Im VIP-Plan ist er enthalten (so in den AGB).
- Live-Klasse: „cada miércoles" ohne Uhrzeit, weil die Zeitzone der 17-Uhr-Angabe aus den Calls nicht sicher ist.

## Vor dem Livegang (Pflicht)

- [x] Impressum, Datenschutzerklärung, AGB/Widerruf verlinkt (`legalUrl`, `privacyUrl`, `termsUrl`) – Seiten liegen drin (26.10.).
- [x] Betreiberangaben in den drei Rechtsseiten eingetragen (26.10.).
- [x] Rechtsseiten durch unabhängigen Prüfagenten gegengelesen, Befunde eingearbeitet (26.10.). Anwältin optional.
- [x] Pflicht-Häkchen im Formulario de inicio (vorzeitiger Beginn + Gesundheitsdaten, 27.10.) und in Calendly (Termintyp „Cita de Evaluación“, Pflichtfrage 7 „Consentimiento (RGPD art. 9)…“ als Checkbox, 27.10., per API geprüft).
- [ ] Skool-Infoseite: AGB/Datenschutz verlinkt, Stufennamen angeglichen – Text (988/1000 Zeichen) liegt vor, wartet auf Hausis „Skool ok“ (27.10.).
- [x] Zapier-Bestätigungsmail v2 (27.10., 15 Uhr): Links zu terminos/privacidad/aviso-legal unter der Versionszeile im Block „INFORMACIÓN LEGAL“.
- [x] Automatische Bestätigungsmail per Zapier (Skool → Gmail) live seit 27.10.; Skool-Auto-DM an neue Mitglieder an.
- [x] Google Fonts entfernt, Schriften selbst gehostet (26.10.).
- [x] Alle Kauf-Buttons führen zum Skool-Gruppenlink, Hinweise zur Stufenwahl stehen darunter (26.10.). Beim ersten echten Kauf prüfen, dass die Kundin die richtige Stufe findet.
- [x] `og:image`, `og:url` und `canonical` auf https://momlifecamila.com gesetzt (27.10.).
- [x] Video liegt als `assets/video.mp4` drin und spielt (geprüft 26.10. in Chrome); Autostart + Ton-Knopf live geprüft 27.10. (Chrome Desktop).
- [ ] Inhalt des Videos gegen den Leitfaden geprüft (Preise 597/347, keine „solo por hoy"-Aussagen, keine Cupos/Bonus-Zahlen, die auf der Seite anders stehen). Dafür Transkript (Plaud) schicken.
- [x] Einverständnis der Frauen auf den Vorher/Nachher-Fotos und in den Testimonial-Screenshots: laut Hausi (27.10.) geklärt, nichts weiter nötig.
- [x] Domain **momlifecamila.com** gekauft (27.10., Cloudflare Registrar; Entscheidung: gleicher Name wie Instagram und Skool). Die Datei `CNAME` im Ordner enthält die Domain, GitHub Pages übernimmt sie beim ersten Deploy automatisch. Offen: ICANN-Bestätigungsmail von Cloudflare anklicken (Frist 14 Tage, sonst wird die Domain gesperrt). `camifit4u.com` bleibt frei; bei Bedarf später kaufen und auf momlifecamila.com umleiten.
- [x] Repo angelegt (27.10., 14:48, Hausi klickt „Create repository“ – öffentliche Repos darf Claude nicht selbst anlegen): https://github.com/CapTheAvenger/camifit-landing, Pages aktiv (main, root), Custom Domain aus `CNAME`, „Enforce HTTPS“ an (Zertifikat war binnen Minuten da). Live seit 27.10., ca. 14:50 Uhr unter https://momlifecamila.com. Im Repo liegen nur index.html, die drei Rechtsseiten, assets/, CNAME, .nojekyll und eine Kurz-README – keine internen Notizen (diese README, Plantilla, Call-Synthese bleiben lokal).
- [x] DNS bei Cloudflare (Hausi klickt „Save“, DNS-Änderungen darf Claude nicht selbst speichern): A @ → 185.199.108.153 (14:46), CNAME www → captheavenger.github.io (14:52); weitere A-Records .109/.110/.111 zur Ausfallsicherheit nachtragen.
- [ ] Seite auf dem Handy geöffnet: Hero, Video (mit Ton), Zahlungsauswahl, Kaufbutton, WhatsApp-Button.

## Hosting über GitHub Pages (empfohlen)

1. Öffentliches Repo `CapTheAvenger/camifit-landing` (angelegt 27.10.; GitHub Pages ist im Free-Plan nur für öffentliche Repos kostenlos; die Seite ist ohnehin öffentlich).
2. Deploy-Inhalt = `index.html`, die drei Rechtsseiten, `assets/`, `CNAME`, `.nojekyll`, Kurz-README. **Nicht** ins Repo: diese README, `plantilla-correo-confirmacion.md`, `instagram-voz-*.md`, `calls-synthese.md`, `artifact/`, `build_artifact.py`. Lokaler Klon für Updates: `/home/claude/deploy/camifit-landing` (Git-Proxy der Sitzung hat Push-Rechte; `git add -A && git commit && git push`). Jede Änderung an `index.html`/Rechtsseiten dorthin kopieren und pushen; Pages baut in ~1 min.
3. Repo → Settings → Pages → Source: „Deploy from a branch", Branch `main`, Ordner `/ (root)`.
4. Eigene Domain: Die Datei `CNAME` (Inhalt `momlifecamila.com`) liegt im Ordner, GitHub trägt die Domain damit selbst unter Pages → „Custom domain" ein. Danach „Enforce HTTPS" aktivieren, sobald das Zertifikat da ist (bis zu einer Stunde; braucht vorher die DNS-Einträge).
5. Bei Cloudflare (Registrar der Domain) → DNS → Records, alle mit **Proxy-Status „DNS only"** (graue Wolke; hinter dem Cloudflare-Proxy bekommt GitHub kein eigenes Zertifikat ausgestellt):
   - Apex-Domain `momlifecamila.com`: vier A-Records auf `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www`: CNAME auf `captheavenger.github.io` (GitHub leitet www auf die Apex-Domain um)
   - Platzhalter-Records, die Cloudflare beim Kauf evtl. angelegt hat (z. B. A/AAAA auf 192.0.2.1 „parking"), vorher löschen.
   Hosting direkt bei Cloudflare (Workers/Pages) ist keine Option, solange `video.mp4` 28,6 MiB groß ist: Cloudflare erlaubt pro Datei nur 25 MiB, GitHub Pages 100 MB.
6. Nach dem ersten Deploy: Seite auf dem Handy öffnen, Kaufbutton testen, Checkout-Vorschau jedes Zahlungsplans ansehen.

Alternative mit gleichem Aufwand: Cloudflare Pages oder Netlify (Drag-and-drop des Ordners). Vorteil gegenüber
GitHub Pages: Formulare und einfache Redirects. Für diese Seite nicht nötig.

## Besuchsstatistik: Cloudflare Web Analytics (seit 28.10.)

Eingerichtet in Hausis Cloudflare-Konto (Observability → Web Analytics → Site `momlifecamila.com`, Modus „Enable with JS
Snippet installation“, weil die DNS-Einträge „DNS only“ sind und Cloudflare das Skript deshalb nicht selbst einfügen kann).
Konto-ID `8c6b5d8d1b12e338cb15ab2a547a249f`, Site-Tag `7dfa306a1adb40178a822cb7da1f6f33` (beides keine Geheimnisse).
Der Beacon (`static.cloudflareinsights.com/beacon.min.js`, Token = öffentliche Site-Kennung, `spa: true`) wird im `<head>`
aller vier Seiten von einem kleinen Lader eingehängt. Ohne Cookies, ohne Profile → kein Banner; Datenschutzerklärung Punkt 4.
**Dashboard:** Cloudflare → Observability → Analytics → Web analytics: Besuche, Seitenaufrufe, Länder, Referrer, Geräte,
Browser, Pfade; Zeitraum oben rechts. Daten ab 28.10., ca. 9:45 Uhr.

**Eigenausschluss:** einmal `momlifecamila.com/?nostats=1` öffnen → dieser Browser wird nicht mehr gezählt (Marke im
localStorage; `?nostats=0` hebt es auf). Hausi und Camila sollten das auf Handy und Rechner einmal machen – **und zwar je
Browser**: der Instagram-In-App-Browser hat eigenen Speicher, also den Link auch einmal aus der eigenen Instagram-Bio heraus
mit `?nostats=1` öffnen (oder nach dem Antippen des Bio-Links `?nostats=1` an die Adresse hängen). Bis dahin gilt:
Besuche aus Deutschland (DE) sind fast sicher eigene Tests (Zielgruppe ist spanischsprachig).

**Trichter als virtuelle Seiten** (Mechanik `window.__cfTrack` im `<head>`; je einmal pro Aufruf, echte URL bleibt `/`):

| Pfad | Bedeutung |
|---|---|
| `/entrada-<quelle>` | Einstieg über einen Link mit `?de=<quelle>` – z. B. Bio `momlifecamila.com/?de=ig`, Story `?de=story`, WhatsApp `?de=wa`. Der Parameter verschwindet sofort aus der Adresszeile. |
| `/ver-video` | Video gestartet (Play auf dem Poster) |
| `/ver-precios` | Preis-Kacheln gesehen (20 % im Bild) |
| `/ver-detalles` | ein „Ver detalles“ aufgeklappt |
| `/ver-guia` | Kauf-Wegweiser geöffnet |
| `/ver-final` | Schlussblock (Abschieds-Text/WhatsApp) gesehen |
| `/tiempo-30s`, `/tiempo-2min` | 30 s bzw. 2 min sichtbar auf der Seite (Hintergrund-Tab zählt nicht) |
| `/clic-skool-vip`, `/clic-skool-vip-2cuotas`, `/clic-skool-premium`, `/clic-skool-standard` | Absprung nach Skool (aus Wegweiser oder direkt) |
| `/clic-whatsapp` | WhatsApp-Button |

Technik: Der Beacon zählt mit `spa:true` jede URL-Änderung (in Chrome/Android/Safari ≥ 26 über das `navigate`-Event, in
älteren Browsern über einen `pushState`-Wrapper plus `popstate`; er zählt nur, wenn sich Pfad+Query gegenüber der zuletzt
gesehenen URL ändern – derselbe Pfad zweimal hintereinander, z. B. zwei WhatsApp-Klicks, zählt also einmal). Der Lader im
`<head>` registriert seine Listener VOR dem Beacon und unterdrückt genau die Rückstellung auf die echte URL
(`stopImmediatePropagation`) sowie Sprunglinks (`#precios`), so dass jedes Ereignis genau einmal zählt und „/“ nicht
aufgebläht wird. Der Beacon sammelt die Ereignisse und schickt sie erst beim Verlassen/Ausblenden der Seite (Zeitstempel =
Besuchsende). Im alten Zweig (pushState + `history.back()`) zusätzlich: `scrollRestoration='manual'` während der
Rückstellung (sonst Scroll-Sprung), Fallback nach 1,5 s und bei `pageshow` aus dem bfcache, Vorwärts-Geste auf einen
virtuellen Eintrag wird still auf die echte URL zurückgesetzt. Beacon blockiert (`onerror`) → keine Events, `?de=` wird trotzdem
aus der Adresszeile entfernt. Lokal getestet mit einem Beacon-Stub für beide
Zweige (`scratchpad/check_track.js`), live im Chrome-Dashboard gegengeprüft. Die Artefakt-Vorschau lädt den Beacon nicht
(`build_artifact.py` ersetzt das `appendChild`).

**Tägliche Datei + automatische Auswertung (seit 28.10.):** Der Workflow `.github/workflows/stats.yml` holt täglich um
03:30 UTC (04:30/05:30 Berlin) per Cloudflare-GraphQL (`scripts/fetch_stats.py`, Token-Secret `CF_API_TOKEN`, nur „Account Analytics: Read“)
pro Berliner Tag Besuche/Seitenaufrufe nach Pfad, Land, Referrer, Gerät, Browser, Stunde und zusätzlich die
Skool-Mitgliederzahl (öffentliche Infoseite, `totalMembers`, alle Stufen) und schreibt alles nach Branch `stats`,
Datei `daily.json` (öffentlich lesbar, nur aggregierte Zahlen). Eine automatische Claude-Aufgabe („Landingpage-Auswertung
momlifecamila“) liest diese Datei um 07:41 Uhr Berlin – täglich bis 11.11.2026, danach montags – und schickt Hausi
Kennzahlen, Trichter, Herkunft und bis zu drei Verbesserungsvorschläge als Benachrichtigung. Die Aufgabe liest nur;
Änderungen an der Seite laufen weiter über den Chat.

## Black-Friday-Kampagne (Hausi 30.10.; AKTIV, sichtbar ab 11.11.)

Schalter: `CAMI_CONFIG.bf.activo` (true seit 30.10.). Die Seite rechnet die Phasen nach der Uhr der Besucherin, zeigt einen
Aktionspreis aber **nur, wenn `bf.json` bestätigt, dass Skool wirklich auf diesen Preis steht** (`precioSkool`). So kann die
Seite nie 249 versprechen, während Skool 347 verlangt. `bf.json` liegt neben index.html und wird ab 15 min vor Beginn alle
30 s gelesen (Cache-Bust pro 30 s), sonst alle 10 min.

| Phase | Zeitraum (deutsche Zeit) | Bedingung | Seite |
|---|---|---|---|
| Countdown | 11.11. 00:00 – 27.11. 18:00 | – | Herz fliegt beim Laden hoch, Leiste nur „♥ Faltan 16 d 16 h 59 min“ (Zeit groß, bewusst mysteriös – Hausi 30.10.: kein „Black Friday“, kein „Angebot“ im Text), Kasten in der 1:1-Kachel „El 27 nov a las 18:00 (hora de Alemania) pasa algo especial con el Plan 1:1, solo para las 10 primeras“, **ohne Preis** (Absicht: bis dahin kauft niemand zum vollen Preis und ärgert sich). Leiste in beiden Farbschemata dunkelgrün (`--moss`) mit heller Zeit. |
| wait | 27.11. 18:00–18:30 | Skool noch nicht bestätigt | „La oferta … se abre en unos minutos“, Preis bleibt 347. Nach 18:30 ohne Bestätigung: Kampagne unsichtbar (fail-safe). |
| Stufe 1 | ab 18:00 | `precioSkool: 249` | 347 durchgestrichen, 249 fällt Ziffer für Ziffer herein, Badge „Oferta especial“ (das Wort „Black Friday“ erscheint nirgends auf der Seite), Chip „$249 hoy“, 2 Raten ausgeblendet. Wortlaut (`mostrarHoraCierre:false`): „solo para las 10 primeras · cupos limitados · la oferta puede cerrarse en cualquier momento“ – **kein** Countdown, **keine** Behauptung „ausverkauft“. Mit `mostrarHoraCierre:true` stattdessen „hasta las 20:00 o hasta agotar cupos“ + Countdown. `mostrarCupos:true` zeigt „Quedan X de 10“ nur mit echtem Stand (`cupos1Restantes`), sonst nie. |
| Stufe 2 | bis Sa 28.11. 20:00 | `precioSkool: 299` | 299, „La oferta de $249 para las 10 primeras ya está cerrada“ (wahr: zu, egal ob Zeit oder Cupos), Countdown bis Sa 20:00. |
| vorbei | ab Sa 20:00 oder `precioSkool: 347` | – | alles normal. |

Pflichtzeile in Stufe 1/2 (PAngV): „Precio normal y precio más bajo de los últimos 30 días: $347 USD“. Nie behaupten, die 10
Plätze seien verkauft, wenn es nicht stimmt (UWG Anhang Nr. 7). Kaufen mehr als 10 zu 249, weil Skool erst um 20:00 umgestellt
wird: in Ordnung (Hausi 30.10.).

**Skool-Umstellung – vier terminierte Claude-Aufgaben über Hausis Laptop (Chrome, eingeloggt), weil die Seite nur anzeigt:**

| Aufgabe | Zeit (Berlin) | Reihenfolge |
|---|---|---|
| 1/3 | Fr 27.11. 17:52 | Skool VIP anual 347 → 249, **nachlesen** (Precios neu laden + /plans), erst dann `bf.json` → 249 und warten, bis es live ist. Seite zeigt 249 ab 18:00. |
| 1b Zähler | Fr 18:02–19:55 | Jede Minute Mitgliederliste lesen (VIP, 249, heute beigetreten). Bei 10 Käufen: `bf.json` → 299, warten bis live, dann Skool → 299. Damit ist „solo para las 10 primeras“ wahr; technisch bedingte Überschreitungen (gleichzeitige Käufe, Deploy-Minuten) sind laut Hausi in Ordnung. |
| 2/3 | Fr 19:57 | Erst `bf.json` → 299 und warten, bis es live ist, dann Skool → 299 (steht Skool schon auf 299, nur prüfen). |
| 3/3 | Sa 28.11. 20:00 | `bf.json` → 347, dann Skool → 347 (Seite blendet um 20:00 ohnehin aus). |

Grundregel: Skool ist nie teurer als die Seite. Preis runter → erst Skool, dann Seite; Preis rauf → erst Seite (live gesehen),
dann Skool. Weg in Skool (geprüft 30.10.): Infoseite → „Configuración“ → Reiter „Precios“ → VIP-Karte → Preis „$174/mes o
$347/año“ antippen → Dialog „Cambiar precio“ (Felder $/mes und $/año, „Mensual y anual“ belassen) → „CAMBIAR“; Skool:
Bestandskundinnen behalten ihren Preis. Monatspreis 174 bleibt (deshalb keine 2 Raten im Black Friday; 2-Raten-Sätze auf der
Seite sind in der Aktionszeit per `data-bf-hide` ausgeblendet, 347-Nennungen per `data-price-full` ersetzt, Kauf-Wegweiser
nennt den aktuellen Preis). Reiter „Pagos“ in Skool sind Auszahlungen, keine Einzelkäufe – Käufe zählt man in der
Mitgliederliste (`/momlifecamila/-/members`: Stufe, Beitrittsdatum, Preis). Vorschau im Artefakt: `build_artifact.py` setzt
`bfPreview: "countdown"`, unten links Schalter für die vier Phasen (simuliert auch `precioSkool`). Prüfagent 30.10.: 12 Befunde,
alle umgesetzt (u. a. Wegweiser-Preis, Reihenfolge/Deploy-Latenz, Leiste nach Herzflug, Intl-Zeitformat, `/clic-bf`-Ereignis).

## Preisbereich seit 28.10. (Hausi: Alternativen auf einen Blick)

Statt einer großen 1:1-Karte mit den Alternativen weit unten gibt es jetzt **drei kompakte Kacheln** (`.tiers`):
Plan 1:1 (hervorgehoben, Badge „Acompañamiento personal“), Comunidad CORE, Cita de evaluación – am Handy untereinander,
am Desktop nebeneinander. Jede Kachel zeigt Titel, Einzeiler, Preis und den **Kauf-Button direkt**; alles Weitere
(Leistungen, Zahlungsoptionen 347/2×174, Skool-Hinweis, AGB-Satz, Bono, Trust-Zeile, Schritte, zweiter Kauf-Button)
steckt in einem aufklappbaren `<details>` „Ver detalles (y formas de pago)“. Über den Kacheln stehen drei **Übersichts-Chips**
(Plan 1:1 $347 · Comunidad $29/mes · Cita $29), die zur jeweiligen Kachel springen – so sieht man am Handy sofort, dass es
günstigere Einstiege gibt. „o 2 cuotas de $174“ in der 1:1-Kachel ist klickbar: öffnet die Details und wählt die 2 Raten.
Die IDs (`buyBtn`, `payFull`/`pay2x`, `payNote`, `payHint`, `payLegal`, `bonoLine`, `cuposLine`, `skoolBtn`, `citaBtn`,
`skoolHint`, `citaHint`) sind unverändert, die Skript-Logik auch. Der AGB-Satz steht zusätzlich im Kauf-Wegweiser.

## Änderungen an der Seite

Die Seite ist bewusst eine Datei. Texte stehen direkt im HTML, Farben und Schriften oben im `:root`-Block.
Der Preisblock liest die Zahlungslinks aus `CAMI_CONFIG`; die Beträge (347 / 174) stehen im HTML und im
Skript (`plans`) und müssen bei einer Preisänderung an beiden Stellen geändert werden.
Nach jeder Änderung `python3 build_artifact.py` ausführen, wenn die Claude-Artefakt-Vorschau aktuell bleiben soll.
