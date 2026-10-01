import streamlit as st

st.set_page_config(page_title="ISU Room Tracker", layout="centered")

st.title("🏫 ISU Classroom Availability Tracker")
st.subheader("BS Chemistry & Campus Room Finder")

# Sample room state stored in memory
if "rooms" not in st.session_state:
    st.session_state.rooms = {
        "Chem Lab 101": {"status": "Available", "building": "Science Wing"},
        "Lecture Hall A": {"status": "Occupied", "building": "Main Building"},
        "Room 203": {"status": "Available", "building": "Main Building"}
    }

# View tabs
tab1, tab2 = st.tabs(["👨‍‍🎓 Student View", "👩‍🏫 Teacher View"])

with tab1:
    st.write("### Available Classrooms")
    for room, info in st.session_state.rooms.items():
        if info["status"] == "Available":
            st.success(f"🟢 **{room}** ({info['building']}) — **AVAILABLE**")
        else:
            st.error(f"🔴 **{room}** ({info['building']}) — **OCCUPIED**")

with tab2:
    st.write("### Update Room Status")
    selected_room = st.selectbox("Select Classroom:", list(st.session_state.rooms.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Mark as Occupied"):
            st.session_state.rooms[selected_room]["status"] = "Occupied"
            st.rerun()
    with col2:
        if st.button("Mark as Available"):
            st.session_state.rooms[selected_room]["status"] = "Available"
            st.rerun()
