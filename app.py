import streamlit as st
from auth import register_user, authenticate_user, delete_user, get_all_users
from streamlit_calendar import calendar


st.set_page_config(page_title="Smart Calendar Login", layout="centered")

if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.username = ""
    st.session_state.role = ""

menu = ["Login", "Register"]
if st.session_state.auth:
    menu = ["Home", "Admin Panel", "Logout"]

choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        ok, msg = register_user(username, password)
        st.success(msg) if ok else st.error(msg)

elif choice == "Login":
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        success, role = authenticate_user(username, password)
        if success:
            st.session_state.auth = True
            st.session_state.username = username
            st.session_state.role = role
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")


elif choice == "Home":
    st.title(f"📅 Smart Calendar – {st.session_state.username}")

    st.subheader("➕ Add Event")
    title = st.text_input("Event Title")
    date = st.date_input("Date")
    time = st.time_input("Time")
    desc = st.text_area("Description")

    if st.button("Add Event"):
        event = {
            "title": title,
            "date": str(date),
            "time": str(time),
            "desc": desc
        }
        add_event(st.session_state.username, event)
        st.success("Event added!")

    st.subheader("📋 My Events")
    events = get_user_events(st.session_state.username)
    for i, e in enumerate(events):
        st.write(f"**{e['title']}** - {e['date']} {e['time']}")
        st.write(f"{e['desc']}")
        if st.button(f"Delete {i}", key=f"del_{i}"):
            delete_event(st.session_state.username, i)
            st.success("Deleted.")
            st.experimental_rerun()
        st.markdown("---")
        
    from datetime import datetime

    today_events = [e for e in events if e['date'] == str(datetime.today().date())]
    for e in today_events:
        event_time = datetime.strptime(e['time'], "%H:%M:%S").time()
        if datetime.now().time() < event_time:
            st.info(f"⏰ Upcoming: **{e['title']}** at {e['time']}")

    for i, e in enumerate(events):
        st.write(f"**{e['title']}** - {e['date']} {e['time']}")
        st.write(f"{e['desc']}")
        if st.button(f"Delete {i}", key=f"del_{i}"):
            delete_event(st.session_state.username, i)
            st.success("Deleted.")
            st.experimental_rerun()
        st.markdown("---")
        

elif choice == "Calendar View":
    st.title("📆 Calendar View")

    raw_events = get_user_events(st.session_state.username)
    cal_events = []

    # Convert to FullCalendar format
    for e in raw_events:
        cal_events.append({
            "title": e["title"],
            "start": f"{e['date']}T{e['time']}",
            "description": e["desc"]
        })

    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": False,
        "selectable": False,
        "headerToolbar": {
            "start": "prev,next today",
            "center": "title",
            "end": "dayGridMonth,timeGridWeek,timeGridDay"
        }
    }

    calendar(events=cal_events, options=calendar_options)



elif choice == "Admin Panel" and st.session_state.role == "admin":
    st.title("👮 Admin Dashboard")
    st.subheader("Registered Users")
    users = get_all_users()
    st.table([{"Username": u, "Role": r["role"]} for u, r in users.items()])

    st.subheader("➕ Add New User")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["user", "admin"])
    if st.button("Add User"):
        ok, msg = register_user(new_user, new_pass, new_role)
        st.success(msg) if ok else st.error(msg)

    st.subheader("🗑 Delete User")
    user_to_delete = st.selectbox("Select user", list(users.keys()))
    if st.button("Delete User"):
        if user_to_delete != st.session_state.username:
            if delete_user(user_to_delete):
                st.success("User deleted.")
                st.experimental_rerun()
            else:
                st.error("Failed to delete.")
        else:
            st.warning("You cannot delete yourself.")

    st.subheader("📂 All User Events")
    all_events = get_all_events()
    for user, evlist in all_events.items():
        if evlist:
            st.markdown(f"### 👤 {user}")
            for e in evlist:
                st.write(f"📌 **{e['title']}** – {e['date']} {e['time']}")
                st.write(f"📝 {e['desc']}")
                st.markdown("---")
                

elif choice == "Chat Assistant":
    from assistant import answer_query
    st.title("🤖 Smart Calendar Assistant")

    user_input = st.text_input("Ask your calendar...", placeholder="What events do I have today?")
    if user_input:
        my_events = get_user_events(st.session_state.username)
        result = answer_query(my_events, user_input)

        if result:
            st.subheader("📋 Response:")
            for r in result:
                st.markdown(f"**{r['title']}** - {r['date']} {r['time']}")
                st.markdown(r["desc"])
                st.markdown("---")
        else:
            st.info("No matching events found.")


elif choice == "Logout":
    st.session_state.auth = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.success("Logged out.")
    st.experimental_rerun()
