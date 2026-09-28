# EnergiePilot – Prototype

EnergiePilot verarbeitet einen strukturierten EnergieAufmaß-Export und führt nacheinander folgende Agenten aus:

1. Data Checker
2. FörderScout mit aktueller Websuche
3. iSFP Planner mit drei unterschiedlichen Sanierungsfahrplänen
4. Technical Inspector
5. Final Advisor

## Lokal starten

Voraussetzungen:
- Python 3.11+
- OpenAI API-Key

```bash
cd energiepilot
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
pip install -r requirements.txt
set OPENAI_API_KEY=DEIN_API_KEY
streamlit run app.py
```

PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:OPENAI_API_KEY="DEIN_API_KEY"
streamlit run app.py
```

Danach im Browser öffnen:

`http://localhost:8501`

## Test

Ohne eigenen EnergieAufmaß-Export kann im UI das integrierte Testprojekt `sample_project.json` verwendet werden.

## Geplanter Produktzugang

Kurzfristig: eigenständige EnergiePilot-Weboberfläche.

Zielintegration in EnergieAufmaß:

`Projekt → Gebäudeaufnahme abschließen → KI-Energieberatung → EnergiePilot`

Dort soll der aktuelle Projektdatensatz direkt an EnergiePilot übergeben werden, sodass kein manueller JSON-Upload mehr nötig ist.

## Wichtiger Hinweis

Die drei erzeugten Sanierungsfahrpläne sind eine KI-gestützte Vorplanung und kein automatisch offiziell ausgestellter iSFP. Förderbedingungen werden zum Zeitpunkt der Analyse aktuell recherchiert; finale Förderfähigkeit, technische Nachweise und offizielle iSFP-Ausgabe müssen fachlich geprüft werden.
