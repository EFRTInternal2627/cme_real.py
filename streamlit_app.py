from __future__ import annotations
import requests # this is how google sheets is connected frfr
import csv # this is how we import each submission
from datetime import datetime # tracks the time someone submits a CME so we can see
from pathlib import Path

import streamlit as st # the website we using for the cme submissions
import base64 # dis is how we upload photos and pdfs for THCME!
GOOGLE_SHEET_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx2_XU8NUUDZ0ALNhQ_UcXqR8hSunltU8P2W7K1wI5H0WYIeWiZZW9YRVRpaKJJMzk/exec"
SUBMISSIONS_FILE = Path("cme_submissions.csv")
# these are the lists that contain all of us as strings (so you can choose dif people for sits)
RUNNING_SIT_WHO = ["suhani verma", "jen francis", "isra bashir", "amanda chow", "shannon man", "leena han", "otis weeks", "jioh yi", "grace lu", "andrew adamson", "evan zhao", "tiya patel", "kira young", "graham dinniwell", "bodhi mah", "murad ammar", "caroline bazydlo", "olivia lee", "katherine lewis", "shanza imran", "melanie seymour", "david litvinenko", "aiden yoo", "vivian ye", "aydin yung", "jenna chen", "henry holland", "henry ball", "trisha arora"]
# i should put these in alphabetical order but i am a lazy chud
CREDIT_SIT_WHO = ["suhani verma", "jen francis", "isra bashir", "amanda chow", "shannon man", "leena han", "otis weeks", "jioh yi", "grace lu", "andrew adamson", "evan zhao", "tiya patel", "kira young", "graham dinniwell", "bodhi mah", "murad ammar", "caroline bazydlo", "olivia lee", "katherine lewis", "shanza imran", "melanie seymour", "david litvinenko", "aiden yoo", "vivian ye", "aydin yung", "jenna chen", "henry holland", "henry ball", "trisha arora"]

SIT_OPTIONS = ["OCME", "MCME#1", "MCME#2", "MCME#3", "MCEM#4", "THCME"]
#this is something i think is really important! having a clear goal means better quality cmes
# it also means people won't submit unless they're sure the responders improved/learned something from da sit! i hope!
GOAL_OPTIONS = [
    "yes! sit was understood, no further action needed.",
    "we practiced LOQ, then the sit was understood!",
    "we practiced some vitals, then the sit was understood!",
    "we did a stop-and-go sit, then the sit was understood!",
]
# i will fill these out properly with protocol once code and google sheets are finalized tee hee
# here are the dictionaries! lowkey dictionary inside of dictionary inside of dictionary inside of
MUST_SEES = { #this is dictionary 1
    "Airway Emergency": { # dict 2
        "Assessment MUST-SEES": [ #dict 3 lawd  have mercy
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
            "Transport Decision (Stay & Play? or Load and Go?)",
			"Consideration of Pt positioning",
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
            "Transport Decision (Stay & Play? or Load and Go?)",
			"Consideration of Pt positioning",
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
            "Transport Decision (Stay & Play? or Load and Go?)",
			"Consideration of Pt positioning",
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
            "Transport Decision (Stay & Play? or Load and Go?)",
			"Consideration of Pt positioning",
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
            "Transport Decision (Stay & Play? or Load and Go?)",
			"Consideration of Pt positioning",
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
            "Transport Decision (Stay & Play? or Load and Go?)",
			"Consideration of Responder(s) and Pack(s) positioning",
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
   # this can be used to clean up the grammar in the must-sees (lowkey giving me a headache i might get rid of this because it's merging the wrong stuff)
    cleaned = item.lower().strip() #basically makes everything either lowercase or properly capitalized 
    cleaned = cleaned.replace("spo2%", "spo2")
    cleaned = cleaned.replace("sp02", "spo2")
    cleaned = " ".join(cleaned.split())
    return cleaned


def clean_section_name(section_name: str) -> str:
# so this basically is merging the yap that is similar in the must-sees, also giving me a big fat headache
    lower_name = section_name.lower()

    if "vital" in lower_name:
        return "Vital MUST-SEES"

    if "assessment" in lower_name:
        return "Assessment MUST-SEES"

    return section_name


def ordered_unique(items: list[str]) -> list[str]:
    # this  will remove duplicate items while keeping the original order.
    seen = set()
    result = []

    for item in items:
        cleaned = clean_item_name(item)

        if cleaned not in seen:
            result.append(item)
            seen.add(cleaned)

    return result


def combine_must_sees(selected_emergencies: list[str]) -> dict[str, list[str]]: # CORE MERGING SECTION THE BIG KAHUNA
    # Combines must-sees from multiple emergencies when chosen in a dropdown menu (and also keeps the order?) i hope so!
    # Also merges vitals together and removes duplicates because that wasn't working for a while lmao
    combined: dict[str, list[str]] = {} # this is the empty dictionary that stuff will go in oh ya!

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

    #Display a checklist of actual must-sees, and will return completed and missed items in the google doc

    st.markdown(f"### {section_name}")
    st.caption("Check the items the responder completed.")

    completed = []

    for item in items:
        key = f"{section_name}::{item}"
# fun fact an f string lets you convert variables into text, so it'll basically throw whatever assessment chosen into the text!
        if st.checkbox(item, key=key):
            completed.append(item)

    missed = []

    for item in items:
        if item not in completed:
            missed.append(item)

    return completed, missed



def save_submission(row: dict[str, str]) -> None:
  
#dis will save one form submission to a CSV file to keep track, it should appear in the same folder as this python file? i hope???
# row is the name of the dictionary for the submissions btw 
	# keys will be the headers and then the values will be inputed as data woo woo
    file_exists = SUBMISSIONS_FILE.exists()
# this checks if the CSV file already exists, if not...
    with SUBMISSIONS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
# it writes one here,
        if not file_exists:
            writer.writeheader()
# and then saves it in here
        writer.writerow(row)


def join_items(items: list[str]) -> str:
#
    return "; ".join(items)


# Streamlit app  to google sheets stuff. thank you youtube. thank you reddit. thank you google.
def send_to_google_sheet(row: dict[str, str], uploaded_files_data=None) -> None:
    payload = {
        "row": row,
        "files": uploaded_files_data or [],
    }

    response = requests.post(
        GOOGLE_SHEET_WEB_APP_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()
st.set_page_config(
    page_title="CME Submission Form (26'/27')",
    page_icon="🚑", #ehehehehe got to be swagged up
)

def prepare_uploaded_files(uploaded_files):
    prepared_files = []

    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.getvalue()

        prepared_files.append({
            "name": uploaded_file.name,
            "type": uploaded_file.type or "application/octet-stream",
            "content": base64.b64encode(file_bytes).decode("utf-8"),
        })

    return prepared_files
	
st.title("cme submission form")

st.caption ("Each month, each responder is required to complete the CMEs outlined in the monthly training update. All CMEs are due by the last day of the month @23:59, with the exception of THCMEs (due before monthly training).")

st.subheader("happy training everyone! #nocarryovers")
who_runnin_sit = st.selectbox(
    "who runnin sit *",
    [""] + sorted(RUNNING_SIT_WHO, key=str.casefold)
)

credit_sit_who = st.selectbox(
    "Who is getting CME credit? *",
    [""] + sorted(CREDIT_SIT_WHO, key=str.casefold)
)
# i am no longer a lazy chud this should fix the alphabetical order 

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

combined_sections = combine_must_sees(selected_sits)

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

uploaded_files = st.file_uploader(
    "If suhani and jen said to submit a photo of something, it probably goes here",
    type=["jpg", "jpeg", "png", "pdf", "doc", "docx"],
    accept_multiple_files=True,
    help="Accepted files: JPEG, PNG, PDF, DOC, DOCX, idk what other files you got bruv"
)
if st.button("Submit", type="primary"):
    if not who_runnin_sit:
        st.error("Please choose who runnin da sit.")

    elif not selected_sits:
        st.error("Please choose at least one sit type.")

    elif not goal:
        st.error("where??? is yo goal???")

    else:
        row = {
            "submitted_at": datetime.now().isoformat(timespec="seconds"),
            "who_runnin_sit": who_runnin_sit,
			"credit_sit_who": credit_sit_who,
            "which_sit": which_sit,
            "selected_sits": join_items(selected_sits),
			"uploaded_file_names": join_items([file["name"] for file in uploaded_files_data]),
   			"uploaded_file_count": str(len(uploaded_files_data)),
			

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
            send_to_google_sheet(row, uploaded_files_data)
            st.success("Submitted! Your CME is saved!.")

        except Exception as error:
            st.warning(
                "Not saved to google sheet EEK shoot training a quick text. "
            )
            st.write(error)

        st.write("Here is what was saved:")
        st.dataframe([row], use_container_width=True)

