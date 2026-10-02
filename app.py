from datetime import datetime, time
import pytz
import streamlit as st

st.set_page_config(
    page_title="ISU Room Tracker", page_icon="🏫", layout="centered"
)

st.title("🏫 ISU Classroom Availability Tracker")
st.subheader("BS Chemistry & Campus Room Finder")

# Set local timezone (Asia/Manila for Philippine Standard Time)
local_tz = pytz.timezone("Asia/Manila")

# Initialize room state
if "rooms" not in st.session_state:
    st.session_state.rooms = {
        "Chem Lab 101": {
            "location": "Science Wing",
            "status": "Available",
            "end_timestamp": None,
            "schedule_text": "",
        },
        "Lecture Hall A": {
            "location": "Main Building",
            "status": "Available",
            "end_timestamp": None,
            "schedule_text": "",
        },
        "Room 203": {
            "location": "Main Building",
            "status": "Available",
            "end_timestamp": None,
            "schedule_text": "",
        },
    }

# --- AUTOMATIC TIME CHECK LOGIC ---
now = datetime.now(local_tz)

for room_name, info in st.session_state.rooms.items():
    if info["status"] == "Occupied" and info["end_timestamp"] is not None:
        # Check if the scheduled end time has passed
        if now >= info["end_timestamp"]:
            info["status"] = "Available"
            info["end_timestamp"] = None
            info["schedule_text"] = ""

# --- APP INTERFACE ---
tab1, tab2 = st.tabs(["🎓 Student View", "👨‍🏫 Teacher View"])

with tab1:
    st.write("### Available Classrooms")
    st.caption(f"Current System Time: {now.strftime('%I:%M:%S %p')}")

    for room, info in st.session_state.rooms.items():
        status_color = "🔴" if info["status"] == "Occupied" else "🟢"
        schedule_info = (
            f" ({info['schedule_text']})" if info["schedule_text"] else ""
        )
        st.write(
            f"{status_color} **{room}** ({info['location']}) — **{info['status']}**{schedule_info}"
        )

with tab2:
    st.write("### 🔒 Teacher Portal")

    password = st.text_input("Enter Teacher Passcode:", type="password")

    if password == "ISU2026":
        st.success("Access Granted!")
        st.write("### Update Room Status")

        selected_room = st.selectbox(
            "Select Classroom:", list(st.session_state.rooms.keys())
        )

        st.write("---")
        st.write("#### Mark Room as Occupied")

        col1, col2 = st.columns(2)
        with col1:
            start_t = st.time_input("Start Time", value=now.time())
        with col2:
            end_t = st.time_input(
                "End Time", value=(now.replace(minute=(now.minute + 5) % 60)).time()
            )

        if st.button("Mark as Occupied"):
            # Construct full datetimes for accurate comparison
            today = now.date()
            start_dt = local_tz.localize(datetime.combine(today, start_t))
            end_dt = local_tz.localize(datetime.combine(today, end_t))

            # Handle overnight edge case if end time is earlier than start time
            if end_dt <= start_dt:
                st.error("End time must be after Start time!")
            else:
                formatted_start = start_dt.strftime("%I:%M %p")
                formatted_end = end_dt.strftime("%I:%M %p")
                time_range_str = f"{formatted_start} – {formatted_end}"

                st.session_state.rooms[selected_room]["status"] = "Occupied"
                st.session_state.rooms[selected_room]["end_timestamp"] = end_dt
                st.session_state.rooms[selected_room][
                    "schedule_text"
                ] = time_range_str

                st.success(
                    f"{selected_room} marked as Occupied until {formatted_end}!"
                )
                st.rerun()

        st.write("---")
        st.write("#### Force Free Room (Manual)")
        if st.button("Mark as Available Now"):
            st.session_state.rooms[selected_room]["status"] = "Available"
            st.session_state.rooms[selected_room]["end_timestamp"] = None
            st.session_state.rooms[selected_room]["schedule_text"] = ""
            st.success(f"{selected_room} is now Available!")
            st.rerun()

    elif password != "":
        st.error("Incorrect passcode.")
    else:
        st.info("Enter passcode to manage room status.")
