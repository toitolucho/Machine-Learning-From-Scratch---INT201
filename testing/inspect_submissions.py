import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()
DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo')
TOKEN = os.environ.get('MOODLE_TOKEN')
ENDPOINT = f'{DOMAIN}/webservice/rest/server.php'

def call(fn, params={}):
    p = {'wstoken': TOKEN, 'wsfunction': fn, 'moodlewsrestformat': 'json'}
    p.update(params)
    r = requests.post(ENDPOINT, data=p)
    return r.json()

tz = datetime.timezone(datetime.timedelta(hours=-4))

# Enrolled users
users_data = call('core_enrol_get_enrolled_users', {'courseid': 6582})
users = {u['id']: u for u in users_data} if isinstance(users_data, list) else {}

# Submissions
subs = call('mod_assign_get_submissions', {'assignmentids[0]': 77028})
assign_subs = subs['assignments'][0]['submissions']

submitted = [s for s in assign_subs if s.get('status') == 'submitted']
print(f"Total submissions: {len(submitted)}")

rows = []
for s in submitted:
    uid = s['userid']
    u = users.get(uid, {})
    name = u.get('fullname', f"User_{uid}")
    email = u.get('email', '')
    tc = s.get('timecreated')
    tm = s.get('timemodified')
    dt_c = datetime.datetime.fromtimestamp(tc, tz) if tc else None
    dt_m = datetime.datetime.fromtimestamp(tm, tz) if tm else None
    duration = (tm - tc) if (tc and tm) else 0
    
    # Check if submitted after duedate (1790685000 = 08:30:00)
    # tolerance is until cutoffdate (1790685300 = 08:35:00)
    is_after_due = tm > 1790685000
    secs_late = tm - 1790685000 if is_after_due else 0
    
    rows.append({
        'userid': uid,
        'name': name,
        'email': email,
        'timecreated': dt_c,
        'timemodified': dt_m,
        'duration_min': round(duration / 60, 2),
        'timestamp_created': tc,
        'timestamp_modified': tm,
        'is_after_due': is_after_due,
        'secs_late': secs_late
    })

rows.sort(key=lambda r: r['timecreated'])

print(f"{'ID':<8} | {'Fullname':<35} | {'Created (Start)':<16} | {'Submitted (End)':<16} | {'Duration':<10} | {'Late?':<12}")
print("-" * 105)
for r in rows:
    c_str = r['timecreated'].strftime('%H:%M:%S') if r['timecreated'] else ''
    m_str = r['timemodified'].strftime('%H:%M:%S') if r['timemodified'] else ''
    dur_str = f"{r['duration_min']} min"
    late_str = f"+{r['secs_late']}s TOL" if r['is_after_due'] else "ON TIME"
    print(f"{r['userid']:<8} | {r['name']:<35} | {c_str:<16} | {m_str:<16} | {dur_str:<10} | {late_str:<12}")
