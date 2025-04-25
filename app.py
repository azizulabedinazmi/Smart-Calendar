import streamlit as st
# filepath: g:\Smart Calendar\app.py
from assistant import answer_query
from datetime import datetime
from streamlit_calendar import calendar

st.set_page_config(page_title="📅 Smart Calendar", layout="centered")
st.title("📅 Smart Calendar")

menu = ["Add/View Events", "Calendar View", "Chat Assistant"]
choice = st.sidebar.radio("Navigation", menu)

USERNAME = "default_user"  # static user since login is removed

if choice == "Add/View Events":
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
        add_event(USERNAME, event)
        st.success("Event added!")

    st.subheader("📋 My Events")
    events = get_user_events(USERNAME)

    # Reminder for today
    today_events = [e for e in events if e['date'] == str(datetime.today().date())]
    for e in today_events:
        event_time = datetime.strptime(e['time'], "%H:%M:%S").time()
        if datetime.now().time() < event_time:
            st.info(f"⏰ Upcoming: **{e['title']}** at {e['time']}")

    for i, e in enumerate(events):
        st.markdown(f"**{e['title']}** - {e['date']} {e['time']}")
        st.write(e["desc"])
        if st.button(f"Delete {i}", key=f"del_{i}"):
            delete_event(USERNAME, i)
            st.success("Deleted.")
            st.experimental_rerun()
        st.markdown("---")

elif choice == "Calendar View":
    st.subheader("📆 Calendar View")
    events = get_user_events(USERNAME)

    cal_events = [{
        "title": e["title"],
        "start": f"{e['date']}T{e['time']}",
        "description": e["desc"]
    } for e in events]

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

elif choice == "Chat Assistant":
    st.subheader("🤖 Ask Your Calendar")
    query = st.text_input("Ask a question like 'What events do I have today?'")
    if query:
        result = answer_query(get_user_events(USERNAME), query)
        for r in result:
            st.write(f"**{r['title']}** – {r['date']} {r['time']}")
            st.write(r["desc"])
            st.markdown("---")
