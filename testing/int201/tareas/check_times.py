import os
import json
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
t01_dir = os.path.join(script_dir, "tarea_420907_inst_77380")
t02_dir = os.path.join(script_dir, "tarea_420908_inst_77381")

tz = datetime.timezone(datetime.timedelta(hours=-4))
DUE_TS = 1792681200    # 2026-10-22 11:00:00
CUTOFF_TS = 1792683000 # 2026-10-22 11:30:00

def check_times(assign_dir, label):
    print("=" * 60)
    print(f"SUBMISSION TIMING: {label}")
    print("=" * 60)
    with open(os.path.join(assign_dir, "submissions_summary.json"), "r", encoding="utf-8") as f:
        subs = json.load(f)
        
    for s in subs:
        if s.get('status') != 'submitted':
            continue
        uid = s['userid']
        name = s['fullname']
        tc = s.get('timecreated')
        tm = s.get('timemodified')
        
        dt_c = datetime.datetime.fromtimestamp(tc, tz) if tc else None
        dt_m = datetime.datetime.fromtimestamp(tm, tz) if tm else None
        
        late_secs = tm - DUE_TS if tm and tm > DUE_TS else 0
        is_late = late_secs > 0
        late_min = round(late_secs / 60, 2)
        
        time_str = dt_m.strftime("%Y-%m-%d %H:%M:%S") if dt_m else "N/A"
        late_str = f"+{late_min} min (TOLERANCIA)" if is_late else "A TIEMPO"
        print(f"User {uid:<8} | {name:<35} | {time_str} | {late_str}")

check_times(t01_dir, "T01 (CMID 420907)")
check_times(t02_dir, "T02 (CMID 420908)")

