import datetime
import streamlit as st

st.title("🏫 ISU Classroom Availability Tracker")
st.subheader("BS Chemistry & Campus Room Finder")

# Initialize room statuses and schedules in session state
if "rooms" not in st.session_state:
    st.session_state.rooms = {
        "Chem Lab 101": {
            "location": "Science Wing",
            "status": "Available",
            "schedule": "",
        },
        "Lecture Hall A": {
            "location": "Main Building",
            "status": "Available",
            "schedule": "",
        },
        "Room 203": {
            "location": "Main Building",
            "status": "Occupied",
            "schedule": "1:00 PM – 2:30 PM",
        },
    }

# Create tabs for Student and Teacher views
tab1, tab2 = st.tabs(["🎓 Student View", "👨‍🏫 Teacher View"])

with tab1:
    st.write("### Available Classrooms")
    for room, info in st.session_state.rooms.items():
        status_color = "🔴" if info["status"] == "Occupied" else "🟢"
        schedule_text = (
            f" ({info['schedule']})"
            if info["status"] == "Occupied" and info["schedule"]
            else ""
        )
        st.write(
            f"{status_color} **{room}** ({info['location']}) — **{info['status']}**{schedule_text}"
        )

with tab2:
    st.write("### 🔒 Teacher Portal")

    # Passcode authentication
    password = st.text_input("Enter Teacher Passcode:", type="password")

    if password == "ISU2026":
        st.success("Access Granted!")
        st.write("### Update Room Status")

        selected_room = st.selectbox(
            "Select Classroom:", list(st.session_state.rooms.keys())
        )

        st.write("---")
        st.write("#### Mark as Occupied with Schedule")

        # Time pickers for schedule window
        col_time1, col_time2 = st.columns(2)
        with col_time1:
            start_time = st.time_input("Start Time:", datetime.time(13, 0))
        with col_time2:
            end_time = st.time_input("End Time:", datetime.time(14, 30))

        if st.button("Mark as Occupied"):
            # Format times into readable strings (e.g., 01:00 PM - 02:30 PM)
            formatted_start = start_time.strftime("%I:%M %p")
            formatted_end = end_time.strftime("%I:%M %p")
            time_str = f"{formatted_start} – {formatted_end}"

            st.session_state.rooms[selected_room]["status"] = "Occupied"
            st.session_state.rooms[selected_room]["schedule"] = time_str
            st.success(
                f"{selected_room} marked as Occupied ({time_str})!"
            )

        st.write("---")
        st.write("#### Free Up Room")
        if st.button("Mark as Available"):
            st.session_state.rooms[selected_room]["status"] = "Available"
            st.session_state.rooms[selected_room]["schedule"] = ""
            st.success(f"{selected_room} is now Available!")

    elif password != "":
        st.error("Incorrect passcode. Access denied.")
    else:
        st.info("Please enter the passcode to access teacher controls.")
        
