import json
import os
import streamlit as st
from openai import OpenAI
from agents import DATA_CHECKER, FOERDER_SCOUT, ISFP_PLANNER, INSPECTOR, FINAL_ADVISOR

st.set_page_config(page_title="EnergiePilot", page_icon="⚡", layout="wide")
st.title("⚡ EnergiePilot")
st.caption("EnergieAufmaß → Fördercheck → 3 Sanierungsfahrpläne → Qualitätsprüfung")

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)
if not api_key:
    st.warning("OPENAI_API_KEY fehlt. Für lokale Tests als Umgebungsvariable setzen oder in Streamlit Secrets hinterlegen.")

model = st.sidebar.selectbox("Modell", ["gpt-5.6-terra", "gpt-5.6-sol", "gpt-5.6-luna"], index=0)
uploaded = st.file_uploader("EnergieAufmaß JSON hochladen", type=["json"])

sample_path = os.path.join(os.path.dirname(__file__), "sample_project.json")
with open(sample_path, "r", encoding="utf-8") as f:
    sample_data = json.load(f)

use_sample = st.checkbox("Testprojekt verwenden", value=uploaded is None)

if uploaded:
    try:
        project = json.load(uploaded)
    except Exception as e:
        st.error(f"JSON konnte nicht gelesen werden: {e}")
        st.stop()
elif use_sample:
    project = sample_data
else:
    project = None

if project:
    with st.expander("Eingabedaten anzeigen", expanded=False):
        st.json(project)


def run_agent(client, instructions, input_text, web=False):
    kwargs = {
        "model": model,
        "instructions": instructions,
        "input": input_text,
    }
    if web:
        kwargs["tools"] = [{"type": "web_search"}]
    response = client.responses.create(**kwargs)
    return response.output_text

if st.button("KI-Energieberatung starten", type="primary", disabled=(project is None or not api_key)):
    client = OpenAI(api_key=api_key)
    raw = json.dumps(project, ensure_ascii=False, indent=2)

    with st.status("Agenten arbeiten …", expanded=True) as status:
        st.write("1/5 Datenprüfung")
        data_check = run_agent(client, DATA_CHECKER, raw)

        st.write("2/5 Aktuelle Fördermöglichkeiten prüfen")
        foerder = run_agent(
            client,
            FOERDER_SCOUT,
            f"GEBÄUDEDATEN:\n{raw}\n\nDATA-CHECK:\n{data_check}",
            web=True,
        )

        st.write("3/5 Drei Sanierungsfahrpläne entwickeln")
        plans = run_agent(
            client,
            ISFP_PLANNER,
            f"GEBÄUDEDATEN:\n{raw}\n\nDATA-CHECK:\n{data_check}\n\nFÖRDERCHECK:\n{foerder}",
        )

        st.write("4/5 Technische Qualitätsprüfung")
        inspection = run_agent(
            client,
            INSPECTOR,
            f"GEBÄUDEDATEN:\n{raw}\n\nDATA-CHECK:\n{data_check}\n\nFÖRDERCHECK:\n{foerder}\n\nSANIERUNGSFAHRPLÄNE:\n{plans}",
        )

        st.write("5/5 Entscheidungsvorlage")
        final = run_agent(
            client,
            FINAL_ADVISOR,
            f"SANIERUNGSFAHRPLÄNE:\n{plans}\n\nINSPECTOR:\n{inspection}\n\nFÖRDERCHECK:\n{foerder}",
        )
        status.update(label="Analyse abgeschlossen", state="complete")

    tabs = st.tabs(["Datenprüfung", "Fördercheck", "3 Fahrpläne", "Inspector", "Empfehlung"])
    for tab, text in zip(tabs, [data_check, foerder, plans, inspection, final]):
        with tab:
            st.markdown(text)

    export = {
        "projekt": project,
        "datenpruefung": data_check,
        "foerdercheck": foerder,
        "sanierungsfahrplaene": plans,
        "inspector": inspection,
        "empfehlung": final,
    }
    st.download_button(
        "Gesamtergebnis als JSON herunterladen",
        data=json.dumps(export, ensure_ascii=False, indent=2),
        file_name="energiepilot_ergebnis.json",
        mime="application/json",
    )
