from datetime import datetime, timedelta

def get_todays_events(events):
    today = datetime.today().date()
    return [e for e in events if e['date'] == str(today)]

def get_weeks_events(events):
    today = datetime.today().date()
    week_later = today + timedelta(days=7)
    return [e for e in events if today <= datetime.strptime(e['date'], "%Y-%m-%d").date() <= week_later]

def answer_query(events, query):
    query = query.lower()
    if "today" in query:
        return get_todays_events(events)
    elif "week" in query:
        return get_weeks_events(events)
    elif "all" in query or "everything" in query:
        return events
    else:
        return [{"title": "🤖 I don't understand that yet!", "date": "", "time": "", "desc": ""}]
