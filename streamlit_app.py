from __future__ import annotations
import requests # this is how google sheets is connected frfr
from uuid import uuid4 # this is how we import each submission into google drive
import time #thank you tiya ily its tiiime for keeping time! haha! ha. its two am.
from zoneinfo import ZoneInfo
from datetime import datetime # tracks the time someone submits a CME so we can see


import streamlit as st # the website we using for the cme submissions
import base64 # dis is how we upload photos and pdfs for THCME!
GOOGLE_SHEET_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyE8-HIyXG1YAmOLgjPmq_4tKZ9vsaq2D9YX7mHqfq24e2RdksrtrIZxWeuZjf8tBdr/exec"
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

PACK_CHECK_OPTIONS = [
	"All Vitals Kits (BP Cuff, Penlight, BGL Kit, Sp02)",
	"All Sx Relief",
	"BLS Equipment (AED, BVM, Pocket Masks, Adjuncts)",
	"Shock Equipment (Oxygen + Tubing, Blanket)",
	"MSK stuff",
]
	
# i will fill these out properly with protocol once code and google sheets are finalized tee hee
# here are the dictionaries! lowkey dictionary inside of dictionary inside of dictionary inside of
MUST_SEES = { #this is dictionary 1
    "Airway Emergency": { # dict 2 to specify each kind of sit we evalin
        "Assessment MUST-SEES": [ #now we have a list of the must-sees
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
##### OKAY STOPWATCH WIDGET HERE #####
def get_stopwatch_time():
    """Return current elapsed stopwatch time in seconds."""

    elapsed = st.session_state.stopwatch_elapsed

    if st.session_state.stopwatch_running:
        elapsed += time.time() - st.session_state.stopwatch_started_at

    return elapsed


def format_stopwatch(seconds):
    """Turn seconds into HH:MM:SS.xx"""

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"


  
#dis will save one form submission to a CSV file to keep track, it should appear in the same folder as this python file? i hope???
##NAH I COMPLETELY FORGOT THIS IS GOING TO A GOOGLE SHEET NOT A CSV FILE LAWDDDD HAVE MERCY ignore what i just said
def save_submission_to_google():
    credited_responders = list(
        dict.fromkeys(
            [who_runnin_sit] + credit_sit_who
        )
    )

    payload = {
        "secret": st.secrets["cme_secret"],
        "submission_id": str(uuid4()),
        "who_runnin_sit": who_runnin_sit,
        "credit_sit_who": credited_responders,
        "which_sit": which_sit,
        "selected_sits": selected_sits,
        "completed_must_sees": flatten_sections(
            completed_by_section
        ),
        "missed_must_sees": flatten_sections(
            missed_by_section
        ),
        "additional_must_sees": additional_must_sees,
        "goal1": goal1,
        "goal": goal or "",
        "general_feedback": general_feedback,
    }

    response = requests.post(
        st.secrets["google_script_url"],
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if not result.get("ok"):
        raise RuntimeError(
            result.get(
                "error",
                "Unknown Google Sheets error"
            )
        )

    return result
	

def join_items(items: list[str]) -> str:
#
    return "; ".join(items)
def flatten_sections(
    sections: dict[str, list[str]]
) -> str:

    output = []

    for section_name, items in sections.items():

        for item in items:
            output.append(
                f"{section_name}: {item}"
            )

    return "; ".join(output)



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
st.image(
    "header.png",
    use_container_width=True
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
# -----------------------------
# STOPWATCH STATE
# -----------------------------

if "stopwatch_running" not in st.session_state:
    st.session_state.stopwatch_running = False

if "stopwatch_started_at" not in st.session_state:
    st.session_state.stopwatch_started_at = None

if "stopwatch_elapsed" not in st.session_state:
    st.session_state.stopwatch_elapsed = 0.0

if "stopwatch_timestamps" not in st.session_state:
    st.session_state.stopwatch_timestamps = []
	
who_runnin_sit = st.selectbox(
    "who runnin sit *",
    [""] + sorted(RUNNING_SIT_WHO, key=str.casefold)
)
# i am no longer a lazy chud this should fix the alphabetical order 

credit_sit_who = st.multiselect(
    "who else is recieving credit for this sit? *",
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
st.divider()

st.divider()
### WATCH TIME ######################################## bro my soul... ty youtube and streamlit forums!
st.subheader("⏱️ sit stopwatch")


refresh_rate = (
    "250ms"
    if st.session_state.stopwatch_running
    else None
)


@st.fragment(run_every=refresh_rate)
def show_stopwatch():

    elapsed = get_stopwatch_time()

    st.markdown(
        f"""
        <div style="
            font-size: 42px;
            font-weight: 700;
            text-align: center;
            font-family: monospace;
            padding: 15px;
        ">
            {format_stopwatch(elapsed)}
        </div>
        """,
        unsafe_allow_html=True,
    )


show_stopwatch()


timer_col1, timer_col2, timer_col3 = st.columns(3)


with timer_col1:

    if st.button(
        "▶️ Start",
        disabled=st.session_state.stopwatch_running,
        use_container_width=True,
    ):

        st.session_state.stopwatch_started_at = time.time()
        st.session_state.stopwatch_running = True

        st.rerun()


with timer_col2:

    if st.button(
        "⏸️ Pause",
        disabled=not st.session_state.stopwatch_running,
        use_container_width=True,
    ):

        st.session_state.stopwatch_elapsed = (
            get_stopwatch_time()
        )

        st.session_state.stopwatch_running = False
        st.session_state.stopwatch_started_at = None

        st.rerun()


with timer_col3:

    if st.button(
        "🔄 Reset",
        use_container_width=True,
    ):

        st.session_state.stopwatch_running = False
        st.session_state.stopwatch_started_at = None
        st.session_state.stopwatch_elapsed = 0.0
        st.session_state.stopwatch_timestamps = []

        st.rerun()


st.markdown("#### 📍 add timestamps from your sit here if you'd like! (optional lol but can be helpful for feedback)")


timestamp_note = st.text_input(
    "What happened?",
    placeholder="e.g. ABCB's cleared, Tx administered, you get the gist",
    key="timestamp_note",
)


if st.button(
    "📍 Mark timestamp",
    use_container_width=True,
):

    current_elapsed = get_stopwatch_time()

    clock_time = datetime.now(
        ZoneInfo("America/Toronto")
    ).strftime("%H:%M:%S")

    note = timestamp_note.strip()

    if not note:
        note = (
            f"Timestamp "
            f"{len(st.session_state.stopwatch_timestamps) + 1}"
        )

    st.session_state.stopwatch_timestamps.append(
        {
            "Elapsed": format_stopwatch(current_elapsed),
            "Event": note,
            "Clock time": clock_time,
        }
    )

    st.rerun()


if st.session_state.stopwatch_timestamps:

    st.markdown("#### 📝 Sit timeline")

    st.dataframe(
        st.session_state.stopwatch_timestamps,
        use_container_width=True,
        hide_index=True,
    )

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

suhani_pack_check = []

for item in PACK_CHECK_OPTIONS:
    if st.checkbox(
        item,
        key=f"pack_check_{item}"
    ):
        completed_pack_check.append(item)
all_pack_items = list(PACK_CHECK_OPTIONS)

if len(suhani_pack_check) == len(all_pack_items):
    st.success("✅ Pack check complete!")
else:
    remaining = len(all_pack_items) - len(completed_pack_check)

    st.info(
        f"{remaining} pack item(s) still need to be checked. I'm deeply sorry but you will be haunted by the ghoust of Suhani Verma."
    )


uploaded_files = st.file_uploader(
    "If suhani and jen said to submit a photo of something, it probably goes here",
    type=["jpg", "jpeg", "png", "pdf", "doc", "docx"],
    accept_multiple_files=True,
    help="Accepted files: JPEG, PNG, PDF, DOC, DOCX, idk what other files you got bruv"
)
######### OKAY. So what's up next is after submit button is pressed
if st.button("submit cme 🚑"):

    if not who_runnin_sit:
        st.error(
            "pls choose who ran the sit!"
        )

    elif not credit_sit_who:
        st.error(
            "pls choose who gets credit!"
        )

    elif not which_sit:
        st.error(
            "pls choose which CME this is!"
        )

    elif not selected_sits:
        st.error(
            "pls choose at least one emergency type!"
        )

    elif goal is None:
        st.error(
            "pls answer whether the goal was achieved!"
        )

    else:

        try:

            result = save_submission_to_google()

            number_saved = result["rows_added"]

            st.success(
                f"CME submitted!! ay ay ay 🚑 "
                f"{number_saved} responder(s) "
                f"received credit."
            )

        except Exception as e:

            st.error(
                "submission couldn't be saved i am sorry shayla :("
            )

            st.code(str(e))

