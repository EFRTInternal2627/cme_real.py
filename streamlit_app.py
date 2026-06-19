from __future__ import annotations
import requests
import csv
from datetime import datetime
from pathlib import Path

import streamlit as st
GOOGLE_SHEET_WEB_APP_URL = https://script.google.com/macros/s/AKfycbyqMh_n9u7RW38YV3054A6i5GY8M2bopiYgc4vfEsFRh-2gKjHLtDI6P8XiqL6BFpDn/exec
SUBMISSIONS_FILE = Path("cme_submissions.csv")

RUNNING_SIT_WHO = ["suhani verma", "jen francis", "isra bashir", "amanda chow", "shannon man", "leena han", "otis weeks", "jioh yi", "grace lu", "andrew adamson", "evan zhao", "tiya patel", "kira young", "graham dinniwell", "bodhi mah", "murad ammar", "caroline bazydlo", "olivia lee", "katherine lewis", "shanza imran", "melanie seymour", "david litvinenko", "aiden yoo", "vivian ye", "aydin yung", "jenna chen", "henry holland", "henry ball", "trisha arora"]

CREDIT_SIT_WHO = ["suhani verma", "jen francis", "isra bashir", "amanda chow", "shannon man", "leena han", "otis weeks", "jioh yi", "grace lu", "andrew adamson", "evan zhao", "tiya patel", "kira young", "graham dinniwell", "bodhi mah", "murad ammar", "caroline bazydlo", "olivia lee", "katherine lewis", "shanza imran", "melanie seymour", "david litvinenko", "aiden yoo", "vivian ye", "aydin yung", "jenna chen", "henry holland", "henry ball", "trisha arora"]


SIT_OPTIONS = ["MCME#1", "MCME#2", "MCME#3", "THCME"]

GOAL_OPTIONS = [
    "yes! sit was understood, no further action needed.",
    "we practiced LOQ, then the sit was understood!",
    "we practiced some vitals, then the sit was understood!",
    "we did a stop-and-go sit, then the sit was understood!",
]

MUST_SEES = {
    "Airway Emergency": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Determine Airway obstruction",
            "Transport Decision (Stay & Play? or Load and Go?)",
            "Intervention Considered",
            "Suction/Adjunct Consideration",
            "Correct airway intervention if provided",
	    "Reassess Airway after intervention"
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
        ],
    },
    

    "Breathing Emergency": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Coach Breathing Consideration",
            "Transport Decision (Stay & Play? or Load and Go?)",
            "SAMPLE",
            "Sx Relief (Naloxone, Epi, Salbutamol) Consideration",
            "Correct Sx Relief Administration if Provided",
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "six-point ausculation", 
        ],
    },

     "Circulation Emergencies": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Identify Circulation Compromise",
            "Transport Decision (Stay & Play? or Load and Go?)",
            "Successfully Treat Major Bleed/Administer Necessary Sx Relief",
            "SAMPLE",
            "Treat for Hypovolemic Shock if indicated",
            "Prepare for Pt Decompensation",
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "Pulse Quality and Rate"
            "Respiration Quality and Rate"
            "Blood Pressure if ya got time fr"
        ],
    },
     "Abdominal Emergencies": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Transport Decision (Stay & Play? or Load and Go?) + Pt Positioning Consideration",
            "SAMPLE",
            "OPQRST",
            "Full Abdo LOQ",
            "Localized physical exam of abdomen (observation + palpation)",
            "Administration of Sx Relief if indicated",
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "Pulse Quality",
            "Blood Pressure",
            "BGL",
        ],
    },
     "Syncope Emergencies": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Transport Decision (Stay & Play? or Load and Go?) + Pt Positioning Consideration",
            "SAMPLE",
            "Full Syncope LOQ",
            "Lifestyle LOQ",
            "Administration of Sx Relief if indicated",
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES, there should be consideration of trends for syncope!": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "Pulse Quality",
            "Blood Pressure Sitting",
            "Blood Pressure Standing shortly after 1st BP",
            "BGL",
            "Pupils",
        ],
    },
    "Diabetic Emergencies": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Transport Decision (Stay & Play? or Load and Go?) + Pt Positioning Consideration",
            "SAMPLE",
            "Consideration of glucose tablets/Administration if necessary",
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "Pulse Quality",
            "BGL x2 (Initial, and then a second one after administering glucose if hypoglycemic)",
        ],
    },
    "Seizure Emergencies": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Transport Decision (Stay & Play? or Load and Go?) + Pt Positioning Consideration",
            "SAMPLE",
            "Full Seizure Timeline (Aura --> Seizure --> Post-ictal)",
            "Administration of Sx Relief if indicated",
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES: Trends for seizure calls are pretty important!": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "Pulse Quality",
            "Resp Quality",
            "Blood Pressure",
            "BGL",
            "Pupils",
        ],
    },
     "Alcohol/Drug (Intox) Emergencies": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Transport Decision (Stay & Play? or Load and Go?) + Pt Positioning Consideration",
            "SAMPLE",
            "Full Intox LOQ",
            "Consideration of vomit/patent airway",
            "Consideration of Pt decompensation"
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "Pulse Quality",
            "Resp Quality",
            "Blood Pressure",
            "BGL",
            "Pupils",
        ],
    },
      "Musculoskeletal Emergencies": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Transport Decision (Stay & Play? or Load and Go?) + Pt Positioning Consideration",
            "SAMPLE",
            "Full CHOPS Assessment",
            "Immobilization of injured region if possible",
            "Consideration of Sx relief",
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "CSM",
        ],
    },
    "Soft-Tissue Injuries/Burns": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Transport Decision (Stay & Play? or Load and Go?) + Pt Positioning Consideration",
            "SAMPLE",
            "Localized Exam to site of injury",
            "Cleaning and bandaging of injury",
            "Consideration of cold pack",
            "Consideration of Sx relief",
            "Transfer Pad with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "CSM",
        ],
    },
     "BLS": {
        "Assessment MUST-SEES": [
            "Primary Assessment (EMCAP + LOC + ACBC)",
            "Identified Primary Assessment Compromise (ie. No pulse, <8 RR, etc.)",
            "Transport Decision (Stay & Play? or Load and Go?) + Pt Positioning Consideration",
            "Full Don Consideration",
            "Treat Pt for shock (O2)",
            "Adequate preparation of equipment for Pt decomp",
            "Frequent reassesses (every 60s) of Pt",
            "Correct reassess order",
            "Correct CPR/AR Protocol",
            "AED Log with USEFUL STUFF ON IT",
            "Correct Radio Codes! For Everything!",
            "Consideration of Final Transport/Justification of Transport Decided",
        ],
        "Vital MUST-SEES": [
            "Skin (did they FEEL the skin for a temperature?)",
            "SpO2%",
            "Resp Rate",
            "Pulse",
        ],
    },
}


def clean_item_name(item: str) -> str:
    """
    Makes duplicate checking more forgiving.
    Example:
    - SpO2%
    - SpO2
    will be treated as the same thing.
    """
    cleaned = item.lower().strip()
    cleaned = cleaned.replace("spo2%", "spo2")
    cleaned = cleaned.replace("sp02", "spo2")
    cleaned = " ".join(cleaned.split())
    return cleaned


def clean_section_name(section_name: str) -> str:
    """
    Forces similar section names to merge together.
    Example:
    - Airway Vital MUST-SEES
    - Breathing Vital MUST-SEES
    - Vital MUST-SEES
    all become Vital MUST-SEES.
    """
    lower_name = section_name.lower()

    if "vital" in lower_name:
        return "Vital MUST-SEES"

    if "assessment" in lower_name:
        return "Assessment MUST-SEES"

    return section_name


def ordered_unique(items: list[str]) -> list[str]:
    """
    Remove duplicate items while keeping the original order.
    """
    seen = set()
    result = []

    for item in items:
        cleaned = clean_item_name(item)

        if cleaned not in seen:
            result.append(item)
            seen.add(cleaned)

    return result


def combine_must_sees(selected_emergencies: list[str]) -> dict[str, list[str]]:
    """
    Combines must-sees from multiple emergencies.
    Also merges vitals together and removes duplicates.
    """
    combined: dict[str, list[str]] = {}

    for emergency in selected_emergencies:
        for section_name, items in MUST_SEES[emergency].items():
            cleaned_section = clean_section_name(section_name)

            if cleaned_section not in combined:
                combined[cleaned_section] = []

            combined[cleaned_section].extend(items)

    final_combined = {}

    for section_name, items in combined.items():
        final_combined[section_name] = ordered_unique(items)

    return final_combined

def checkbox_list(section_name: str, items: list[str]) -> tuple[list[str], list[str]]:
    """
    Display a checklist.
    Returns:
    - completed items
    - missed items
    """
    st.markdown(f"### {section_name}")
    st.caption("Check the items the responder completed.")

    completed = []

    for item in items:
        key = f"{section_name}::{item}"

        if st.checkbox(item, key=key):
            completed.append(item)

    missed = []

    for item in items:
        if item not in completed:
            missed.append(item)

    return completed, missed


def save_submission(row: dict[str, str]) -> None:
  
#dis will save one form submission to a CSV file to keep track, it should appear in the same folder as this python file? i hope???
  
    file_exists = SUBMISSIONS_FILE.exists()

    with SUBMISSIONS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def join_items(items: list[str]) -> str:
#
    return "; ".join(items)


# Streamlit app starts here. thank you youtube. thank you reddit. thank you google.
def send_to_google_sheet(row: dict[str, str]) -> None:
    response = requests.post(
        GOOGLE_SHEET_WEB_APP_URL,
        json=row,
        timeout=10,
    )
    response.raise_for_status()
st.set_page_config(
    page_title="CME Submission Form (26'/27')",
    page_icon="🚑", #ehehehehe
)

st.title("cme submission form")

st.caption ("Each month, each responder is required to complete the CMEs outlined in the monthly training update. All CMEs are due by the last day of the month @23:59, with the exception of THCMEs (due before monthly training).")

st.subheader("happy training everyone!")

who_runnin_sit = st.selectbox(
    "who runnin dis sit *",
    [""] + RUNNING_SIT_WHO,
)

credit_sit_who = st.multiselect(
    "who is recieving credit for this sit? *",
    list(RUNNING_SIT_WHO),
    help="choose one or more responders!",
)
which_sit = st.selectbox(
    "which CME are you completing?",
    [""] + SIT_OPTIONS,
)

selected_sits = st.multiselect(
    "What kind of sit are you running today? *",
    list(MUST_SEES.keys()),
    help="Choose one or multiple emergency types.",
)

if selected_sits:
    st.success("Selected: " + ", ".join(selected_sits))
else:
    st.info("Choose at least one emergency type to show the MUST-SEES.")


completed_by_section: dict[str, list[str]] = {}
missed_by_section: dict[str, list[str]] = {}

combined_sections = combowombo(selected_sits)

for section_name, items in combined_sections.items():
    st.divider()

    completed, missed = checkbox_list(section_name, items)

    completed_by_section[section_name] = completed
    missed_by_section[section_name] = missed


st.divider()

st.subheader("Final notes")

additional_must_sees = st.text_input(
    "Any additional MUST-SEES in the sit you cooked?"
)

goal1 = st.text_area(
    "what was the goal of your sit fam?"
)

goal = st.radio(
    "Did you achieve your goal? Did you practice any skills/LOQ after? *",
    GOAL_OPTIONS,
    index=None,
)


general_feedback = st.text_area(
    "general feedback for your responder!"
)


if st.button("Submit", type="primary"):
    if not who_runnin_sit:
        st.error("Please choose who runnin da sit.")

    elif not selected_emergencies:
        st.error("Please choose at least one sit type.")

    elif not goal:
        st.error("where??? is yo goal???")

    else:
        row = {
            "submitted_at": datetime.now().isoformat(timespec="seconds"),
            "who_runnin_sit": who_runnin_sit,
            "which_sit": which_sit,
            "selected_emergencies": join_items(selected_emergencies),

            "assessment_completed": join_items(
                completed_by_section.get("Assessment MUST-SEES", [])
            ),
            "assessment_missed": join_items(
                missed_by_section.get("Assessment MUST-SEES", [])
            ),

            "vitals_completed": join_items(
                completed_by_section.get("Vital MUST-SEES", [])
            ),
            "vitals_missed": join_items(
                missed_by_section.get("Vital MUST-SEES", [])
            ),

            "additional_must_sees": additional_must_sees,
            "goal1": goal1,
            "goal": goal,
            "general_feedback": general_feedback,
        }

        save_submission(row)

try:
    send_to_google_sheet(row)
    st.success("Submitted! Saved locally and sent to Google Sheets.")
except Exception as error:
    st.warning(
        "Submitted and saved locally, but Google Sheets did not update. "
        "Check your Apps Script Web App URL and deployment settings."
    )
    st.write(error)

        st.write("Here is what was saved shayla:")
        st.dataframe([row], use_container_width=True)
