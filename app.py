import streamlit as st

st.title("🏫 ISU Classroom Availability Tracker")
st.subheader("BS Chemistry & Campus Room Finder")

# Initialize room statuses in session state
if "rooms" not in st.session_state:
    st.session_state.rooms = {
        "Chem Lab 101": {"location": "Science Wing", "status": "Available"},
        "Lecture Hall A": {"location": "Main Building", "status": "Available"},
        "Room 203": {"location": "Main Building", "status": "Occupied"},
    }

# Create tabs for Student and Teacher views
tab1, tab2 = st.tabs(["🎓 Student View", "👨‍🏫 Teacher View"])

with tab1:
    st.write("### Available Classrooms")
    for room, info in st.session_state.rooms.items():
        status_color = "🔴" if info["status"] == "Occupied" else "🟢"
        st.write(f"{status_color} **{room}** ({info['location']}) — **{info['status']}**")

with tab2:
    st.write("### 🔒 Teacher Portal")
    
    # Simple passcode input
    password = st.text_input("Enter Teacher Passcode:", type="password")
    
    if password == "ISU2026":  # You can change "ISU2026" to your preferred password
        st.success("Access Granted!")
        st.write("### Update Room Status")
        
        selected_room = st.selectbox("Select Classroom:", list(st.session_state.rooms.keys()))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Mark as Occupied"):
                st.session_state.rooms[selected_room]["status"] = "Occupied"
                st.success(f"{selected_room} marked as Occupied!")
        with col2:
            if st.button("Mark as Available"):
                st.session_state.rooms[selected_room]["status"] = "Available"
                st.success(f"{selected_room} marked as Available!")
                
    elif password != "":
        st.error("Incorrect passcode. Access denied.")
    else:
        st.info("Please enter the passcode to access teacher controls.")
        
