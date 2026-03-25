"""
OTP Anomaly Detection Demo
A hackathon prototype demonstrating rule-based anomaly detection for OTP requests.
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from translations import get_text

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="OTP Anomaly Detector",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize language in session state
if "language" not in st.session_state:
    st.session_state.language = "ka"

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0a0e27 0%, #1a1428 100%);
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    h1, h2 {
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
        color: #fff;
    }

    h1 {
        font-weight: 700;
        font-size: 2.5rem;
        background: linear-gradient(135deg, #3dffa0 0%, #00f0ff 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(61, 255, 160, 0.05) 0%, rgba(0, 240, 255, 0.05) 100%);
        border: 1px solid rgba(61, 255, 160, 0.2);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        background: linear-gradient(135deg, rgba(61, 255, 160, 0.1) 0%, rgba(0, 240, 255, 0.1) 100%);
        border-color: rgba(61, 255, 160, 0.4);
        box-shadow: 0 12px 48px rgba(61, 255, 160, 0.15);
        transform: translateY(-2px);
    }

    .metric-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #a0aec0;
        font-family: 'IBM Plex Mono', monospace;
        margin-bottom: 0.6rem;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2.8rem;
        font-weight: 700;
        font-family: 'IBM Plex Mono', monospace;
        line-height: 1;
    }

    .metric-value.green  { color: #3dffa0; }
    .metric-value.yellow { color: #ffd166; }
    .metric-value.red    { color: #ff4d6d; }
    .metric-value.white  { color: #f0f0f0; }

    .risk-high   { color: #ff4d6d; font-weight: 700; }
    .risk-medium { color: #ffd166; font-weight: 600; }
    .risk-low    { color: #3dffa0; font-weight: 500; }

    .tag {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .tag-block    { background: rgba(255, 77, 109, 0.15); color: #ff4d6d; border: 1px solid rgba(255, 77, 109, 0.5); }
    .tag-throttle { background: rgba(255, 209, 102, 0.15); color: #ffd166; border: 1px solid rgba(255, 209, 102, 0.5); }
    .tag-allow    { background: rgba(61, 255, 160, 0.15); color: #3dffa0; border: 1px solid rgba(61, 255, 160, 0.5); }

    .section-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #a0aec0;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 2px solid rgba(61, 255, 160, 0.3);
        font-weight: 600;
    }

    .explain-box {
        background: linear-gradient(135deg, rgba(61, 255, 160, 0.05) 0%, rgba(0, 240, 255, 0.05) 100%);
        border-left: 4px solid #3dffa0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        font-size: 0.9rem;
        line-height: 1.8;
        color: #e2e8f0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(61, 255, 160, 0.2);
    }

    .proto-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(255, 209, 102, 0.2) 0%, rgba(255, 209, 102, 0.1) 100%);
        color: #ffd166;
        border: 1px solid rgba(255, 209, 102, 0.5);
        border-radius: 24px;
        padding: 0.3rem 1.2rem;
        font-size: 0.75rem;
        font-family: 'IBM Plex Mono', monospace;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-left: 1rem;
        vertical-align: middle;
        font-weight: 600;
    }

    .control-panel {
        background: linear-gradient(135deg, rgba(26, 20, 40, 0.8) 0%, rgba(15, 17, 23, 0.8) 100%);
        border: 1px solid rgba(61, 255, 160, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .control-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #a0aec0;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: block;
    }

    .dataframe {
        background: rgba(26, 20, 40, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DATA GENERATION
# ──────────────────────────────────────────────

PHONES   = [f"+1555{str(i).zfill(7)}" for i in range(1, 60)]
IPS_NORMAL  = [f"192.168.{random.randint(1,50)}.{random.randint(1,250)}" for _ in range(30)]
IPS_ABUSE   = [f"10.0.{random.randint(1,5)}.{random.randint(1,10)}"      for _ in range(5)]
DEVICES  = ["iPhone 15", "Samsung S24", "Pixel 8", "Chrome/Mac", "Firefox/Win", "Safari/iPad"]
COUNTRIES = ["GE", "US", "GB", "DE", "FR", "CA", "AU", "IN", "BR"]
COUNTRIES_GEORGIA = ["GE"]
COUNTRIES_OTHER = ["US", "GB", "DE", "FR", "CA", "AU", "IN", "BR"]


def generate_normal_events(n: int, base_time: datetime) -> list[dict]:
    """Generate realistic normal OTP requests spread across many users. ~50% from Georgia."""
    events = []
    for _ in range(n):
        phone = random.choice(PHONES[:40])
        # ~50% from Georgia, ~50% from other countries
        country = random.choice(COUNTRIES_GEORGIA) if random.random() < 0.5 else random.choice(COUNTRIES_OTHER)
        events.append({
            "timestamp": base_time - timedelta(minutes=random.uniform(0, 60)),
            "phone":     phone,
            "ip":        random.choice(IPS_NORMAL),
            "device":    random.choice(DEVICES[:4]),
            "country":   country,
            "status":    random.choices(["sent", "failed"], weights=[90, 10])[0],
            "label":     "normal",
        })
    return events


def generate_suspicious_events(n: int, base_time: datetime) -> list[dict]:
    """Generate suspicious events: same phone hammered with OTPs repeatedly. ~50% from Georgia."""
    events = []
    # Pick a few phones that are being spammed
    suspect_phones = random.sample(PHONES[:40], k=min(3, len(PHONES)))
    for _ in range(n):
        phone = random.choice(suspect_phones)
        # ~50% from Georgia, ~50% from other countries
        country = random.choice(COUNTRIES_GEORGIA) if random.random() < 0.5 else random.choice(COUNTRIES_OTHER)
        events.append({
            "timestamp": base_time - timedelta(minutes=random.uniform(0, 15)),
            "phone":     phone,
            "ip":        random.choice(IPS_NORMAL[:5]),
            "device":    random.choice(DEVICES),
            "country":   country,
            "status":    random.choices(["sent", "failed"], weights=[40, 60])[0],
            "label":     "suspicious",
        })
    return events


def generate_abuse_events(n: int, base_time: datetime) -> list[dict]:
    """Generate abuse events: one attacker IP hitting many different phone numbers."""
    events = []
    attacker_ip = random.choice(IPS_ABUSE)
    for _ in range(n):
        events.append({
            "timestamp": base_time - timedelta(minutes=random.uniform(0, 10)),
            "phone":     random.choice(PHONES[30:]),   # targets a different pool
            "ip":        attacker_ip,
            "device":    random.choice(DEVICES[-2:]),  # often same device/browser
            "country":   random.choice(["RU", "CN", "NG", "VN"]),
            "status":    random.choices(["sent", "failed"], weights=[60, 40])[0],
            "label":     "abuse",
        })
    return events


@st.cache_data(show_spinner=False)
def generate_dataset(n_normal: int, n_suspicious: int, n_abuse: int, seed: int) -> pd.DataFrame:
    """Build and shuffle the full synthetic dataset."""
    random.seed(seed)
    np.random.seed(seed)

    base_time = datetime.now()
    rows = (
        generate_normal_events(n_normal, base_time)
        + generate_suspicious_events(n_suspicious, base_time)
        + generate_abuse_events(n_abuse, base_time)
    )
    df = pd.DataFrame(rows).sort_values("timestamp").reset_index(drop=True)
    return df


# ──────────────────────────────────────────────
# FEATURE ENGINEERING
# ──────────────────────────────────────────────

def compute_features(df: pd.DataFrame,
                     window_phone_min: int,
                     window_ip_min: int,
                     window_device_hours: int) -> pd.DataFrame:
    """
    For every row, compute:
      - otp_per_phone   : how many OTPs this phone received in the last N minutes
      - phones_per_ip   : how many unique phones came from this IP in the last N minutes
      - devices_per_phone: unique devices seen for this phone in the last N hours
      - country_change  : did the country change from the previous request for this phone?
      - fail_streak     : consecutive failed attempts for this phone
    """
    df = df.copy().sort_values("timestamp").reset_index(drop=True)
    ts = df["timestamp"]

    otp_per_phone    = []
    phones_per_ip    = []
    devices_per_phone = []
    country_change   = []
    fail_streak      = []

    for i, row in df.iterrows():
        t = row["timestamp"]

        # --- OTPs per phone in last `window_phone_min` minutes ---
        w_phone = t - timedelta(minutes=window_phone_min)
        mask_phone = (df["phone"] == row["phone"]) & (ts >= w_phone) & (ts <= t)
        otp_per_phone.append(int(mask_phone.sum()))

        # --- Unique phones per IP in last `window_ip_min` minutes ---
        w_ip = t - timedelta(minutes=window_ip_min)
        mask_ip = (df["ip"] == row["ip"]) & (ts >= w_ip) & (ts <= t)
        phones_per_ip.append(int(df.loc[mask_ip, "phone"].nunique()))

        # --- Unique devices per phone in last `window_device_hours` hours ---
        w_dev = t - timedelta(hours=window_device_hours)
        mask_dev = (df["phone"] == row["phone"]) & (ts >= w_dev) & (ts <= t)
        devices_per_phone.append(int(df.loc[mask_dev, "device"].nunique()))

        # --- Country change vs previous request from same phone ---
        prev = df[(df["phone"] == row["phone"]) & (ts < t)]
        if prev.empty:
            country_change.append(False)
        else:
            last_country = prev.iloc[-1]["country"]
            country_change.append(last_country != row["country"])

        # --- Consecutive failures for this phone (look back up to 5 events) ---
        prior = df[(df["phone"] == row["phone"]) & (ts < t)].tail(5)
        streak = 0
        for _, pr in prior[::-1].iterrows():
            if pr["status"] == "failed":
                streak += 1
            else:
                break
        if row["status"] == "failed":
            streak += 1
        fail_streak.append(streak)

    df["otp_per_phone"]     = otp_per_phone
    df["phones_per_ip"]     = phones_per_ip
    df["devices_per_phone"] = devices_per_phone
    df["country_change"]    = country_change
    df["fail_streak"]       = fail_streak
    return df


# ──────────────────────────────────────────────
# RISK SCORING
# ──────────────────────────────────────────────

def score_row(row: pd.Series) -> tuple[int, str, str]:
    """
    Rule-based risk scoring (0–100).
    Returns (score, reason_text, action).
    """
    score = 0
    reasons = []

    # Signal 1: Too many OTPs to the same phone recently
    if row["otp_per_phone"] >= 10:
        score += 35
        reasons.append(f"{row['otp_per_phone']} OTPs to this phone in short window")
    elif row["otp_per_phone"] >= 5:
        score += 15
        reasons.append(f"{row['otp_per_phone']} OTPs to this phone recently")

    # Signal 2: One IP blasting many different phones
    if row["phones_per_ip"] >= 10:
        score += 40
        reasons.append(f"IP targeted {row['phones_per_ip']} different phones")
    elif row["phones_per_ip"] >= 5:
        score += 20
        reasons.append(f"IP targeted {row['phones_per_ip']} different phones")

    # Signal 3: Multiple devices for the same phone
    if row["devices_per_phone"] >= 4:
        score += 15
        reasons.append(f"{row['devices_per_phone']} devices used for this phone")
    elif row["devices_per_phone"] >= 2:
        score += 5
        reasons.append(f"{row['devices_per_phone']} devices for this phone")

    # Signal 4: Country changed between requests
    if row["country_change"]:
        score += 10
        reasons.append("Country changed since last request")

    # Signal 5: Repeated failures
    if row["fail_streak"] >= 4:
        score += 15
        reasons.append(f"{row['fail_streak']} consecutive failures")
    elif row["fail_streak"] >= 2:
        score += 5
        reasons.append(f"{row['fail_streak']} consecutive failures")

    score = min(score, 100)

    if not reasons:
        reason_text = "No anomalies detected"
    else:
        reason_text = " · ".join(reasons)

    # Decide action
    if score >= 70:
        action = "block"
    elif score >= 35:
        action = "throttle"
    else:
        action = "allow"

    return score, reason_text, action


def apply_scoring(df: pd.DataFrame) -> pd.DataFrame:
    """Apply risk scoring to every row."""
    results = df.apply(score_row, axis=1, result_type="expand")
    results.columns = ["risk_score", "reason", "action"]
    return pd.concat([df, results], axis=1)


# ──────────────────────────────────────────────
# DISPLAY HELPERS
# ──────────────────────────────────────────────

def highlight_risk(row: pd.Series) -> list[str]:
    """Return row background colour based on risk score."""
    s = row.get("risk_score", 0)
    if s >= 70:
        bg = "background-color: #ff4d6d18;"
    elif s >= 35:
        bg = "background-color: #ffd16618;"
    else:
        bg = ""
    return [bg] * len(row)


def risk_badge(score: int) -> str:
    if score >= 70:
        return f'<span class="risk-high">■ {score}</span>'
    elif score >= 35:
        return f'<span class="risk-medium">▲ {score}</span>'
    else:
        return f'<span class="risk-low">● {score}</span>'


def action_tag(action: str) -> str:
    cls = {"block": "tag-block", "throttle": "tag-throttle", "allow": "tag-allow"}[action]
    return f'<span class="tag {cls}">{action.upper()}</span>'


def country_to_flag(country_code: str) -> str:
    """Convert country code to flag emoji and return with country code."""
    flag_map = {
        "GE": "🇬🇪", "US": "🇺🇸", "GB": "🇬🇧", "DE": "🇩🇪", "FR": "🇫🇷",
        "CA": "🇨🇦", "AU": "🇦🇺", "IN": "🇮🇳", "BR": "🇧🇷",
        "RU": "🇷🇺", "CN": "🇨🇳", "NG": "🇳🇬", "VN": "🇻🇳",
    }
    flag = flag_map.get(country_code, "🏴")
    return f"{flag} {country_code}"


# ──────────────────────────────────────────────
# HEADER & CONTROLS
# ──────────────────────────────────────────────

# Language selector (top right)
col_lang = st.columns([10, 1])
with col_lang[1]:
    lang_option = st.selectbox(
        "🌐",
        options=["English", "ქართული (Georgian)"],
        index=0 if st.session_state.language == "en" else 1,
        key="lang_selector",
        label_visibility="collapsed"
    )
    st.session_state.language = "en" if lang_option.startswith("English") else "ka"

# Get translation function
t = lambda key: get_text(key, st.session_state.language)

# Header
st.markdown(
    f'<h1>🔐 {t("page_title")}<span class="proto-badge">Prototype</span></h1>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<p style="color:#a0aec0;margin-top:0;font-size:1rem;margin-bottom:1.5rem">'
    f'{t("page_subtitle")}</p>',
    unsafe_allow_html=True,
)

# Control Panel
st.markdown(f'<div class="control-panel">', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:0.8rem;text-transform:uppercase;color:#a0aec0;letter-spacing:1.5px;font-weight:600;margin-bottom:1.5rem">{t("controls")}</p>', unsafe_allow_html=True)

ctrl_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1])

with ctrl_cols[0]:
    st.markdown('<span class="control-label">📊 ' + t("normal_events") + '</span>', unsafe_allow_html=True)
    n_normal = st.slider(t("normal_events"), min_value=10, max_value=300, value=120, step=10, key="n_normal", label_visibility="collapsed")

with ctrl_cols[1]:
    st.markdown('<span class="control-label">⚠️ ' + t("suspicious_events") + '</span>', unsafe_allow_html=True)
    n_suspicious = st.slider(t("suspicious_events"), min_value=5, max_value=100, value=30, step=5, key="n_suspicious", label_visibility="collapsed")

with ctrl_cols[2]:
    st.markdown('<span class="control-label">🔴 ' + t("abuse_events") + '</span>', unsafe_allow_html=True)
    n_abuse = st.slider(t("abuse_events"), min_value=5, max_value=100, value=20, step=5, key="n_abuse", label_visibility="collapsed")

with ctrl_cols[3]:
    st.markdown('<span class="control-label">📱 OTP Window</span>', unsafe_allow_html=True)
    window_phone = st.slider("OTP Window", 5, 30, 10, key="window_phone", label_visibility="collapsed")

with ctrl_cols[4]:
    st.markdown('<span class="control-label">🌐 IP Window</span>', unsafe_allow_html=True)
    window_ip = st.slider("IP Window", 5, 30, 15, key="window_ip", label_visibility="collapsed")

with ctrl_cols[5]:
    st.markdown('<span class="control-label">📲 Device Window</span>', unsafe_allow_html=True)
    window_device = st.slider("Device Window", 1, 48, 24, key="window_device", label_visibility="collapsed")

with ctrl_cols[6]:
    st.markdown('<span class="control-label">🎲 Seed</span>', unsafe_allow_html=True)
    seed = st.number_input("Seed", value=42, step=1, key="seed", label_visibility="collapsed")

with ctrl_cols[7]:
    st.markdown('<span class="control-label">🔄 Action</span>', unsafe_allow_html=True)
    if st.button("🔄 Regenerate", width='stretch'):
        st.cache_data.clear()

st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PIPELINE
# ──────────────────────────────────────────────

with st.spinner("Generating and analysing data…"):
    raw_df      = generate_dataset(n_normal, n_suspicious, n_abuse, seed=int(seed))
    featured_df = compute_features(raw_df, window_phone, window_ip, window_device)
    scored_df   = apply_scoring(featured_df)

total    = len(scored_df)
flagged  = (scored_df["risk_score"] >= 35).sum()
blocked  = (scored_df["action"] == "block").sum()
throttled = (scored_df["action"] == "throttle").sum()
flag_pct = flagged / total * 100 if total else 0


# ──────────────────────────────────────────────
# METRICS ROW
# ──────────────────────────────────────────────

st.markdown(f'<p class="section-header">{t("overview")}</p>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

def metric_card(col, label, value, colour):
    col.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value {colour}">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

metric_card(c1, t("total_events"),   total,                  "white")
metric_card(c2, t("flagged"),        flagged,                "yellow")
metric_card(c3, t("blocked"),        blocked,                "red")
metric_card(c4, t("throttled"),      throttled,              "yellow")
metric_card(c5, t("flag_rate"),      f"{flag_pct:.1f}%",     "white" if flag_pct < 10 else "yellow")

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# CHARTS
# ──────────────────────────────────────────────

st.markdown(f'<p class="section-header">{t("distribution")}</p>', unsafe_allow_html=True)
ch1, ch2 = st.columns(2)

with ch1:
    st.markdown(f"**{t('risk_score_distribution')}**")
    bins = pd.cut(
        scored_df["risk_score"],
        bins=[0, 10, 34, 69, 100],
        labels=[t("low_risk"), t("moderate_risk"), t("high_risk"), t("critical_risk")],
    )
    dist = bins.value_counts().reindex([t("low_risk"), t("moderate_risk"), t("high_risk"), t("critical_risk")])
    st.bar_chart(dist, color="#3dffa0", height=220)

with ch2:
    st.markdown(f"**{t('action_breakdown')}**")
    action_counts = scored_df["action"].value_counts()
    st.bar_chart(action_counts, color="#ffd166", height=220)

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# FLAGGED EVENTS TABLE
# ──────────────────────────────────────────────

st.markdown(f'<p class="section-header">{t("flagged_events")}</p>', unsafe_allow_html=True)
st.markdown(f"**{t('events_requiring_attention')}**")

flagged_df = (
    scored_df[scored_df["risk_score"] >= 35]
    .sort_values("risk_score", ascending=False)
    .reset_index(drop=True)
)

if flagged_df.empty:
    st.info(t("no_flagged_events"))
else:
    # Separate flagged events by region
    flagged_georgia = flagged_df[flagged_df["country"] == "GE"].reset_index(drop=True)
    flagged_other = flagged_df[flagged_df["country"] != "GE"].reset_index(drop=True)
    
    # Create tabs for each region
    tab_georgia, tab_other = st.tabs([f"🇬🇪 Georgian Region ({len(flagged_georgia)})", 
                                       f"🌍 Other Countries ({len(flagged_other)})"])
    
    display_cols = ["timestamp", "phone", "ip", "country", "device",
                    "status", "risk_score", "action", "reason"]
    
    # Georgian Region Tab
    with tab_georgia:
        if flagged_georgia.empty:
            st.info("No flagged events from Georgian region")
        else:
            display_df_georgia = flagged_georgia[display_cols].copy()
            display_df_georgia["country"] = display_df_georgia["country"].apply(country_to_flag)
            styled_georgia = (
                display_df_georgia
                .style
                .apply(highlight_risk, axis=1)
                .format({"timestamp": lambda x: x.strftime("%H:%M:%S"), "risk_score": "{:.0f}"})
                .background_gradient(subset=["risk_score"], cmap="Reds", vmin=0, vmax=100)
            )
            st.dataframe(styled_georgia, width='stretch', height=320)
            csv_georgia = flagged_georgia[display_cols].to_csv(index=False)
            st.download_button(
                t("download_flagged_csv"),
                data=csv_georgia,
                file_name="flagged_georgian_region.csv",
                mime="text/csv",
            )
    
    # Other Countries Tab
    with tab_other:
        if flagged_other.empty:
            st.info("No flagged events from other countries")
        else:
            display_df_other = flagged_other[display_cols].copy()
            display_df_other["country"] = display_df_other["country"].apply(country_to_flag)
            styled_other = (
                display_df_other
                .style
                .apply(highlight_risk, axis=1)
                .format({"timestamp": lambda x: x.strftime("%H:%M:%S"), "risk_score": "{:.0f}"})
                .background_gradient(subset=["risk_score"], cmap="Reds", vmin=0, vmax=100)
            )
            st.dataframe(styled_other, width='stretch', height=320)
            csv_other = flagged_other[display_cols].to_csv(index=False)
            st.download_button(
                t("download_flagged_csv"),
                data=csv_other,
                file_name="flagged_other_countries.csv",
                mime="text/csv",
            )

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# FULL FEATURE TABLE
# ──────────────────────────────────────────────

with st.expander(t("full_dataset"), expanded=False):
    all_cols = [
        "timestamp", "phone", "ip", "country", "device", "status", "label",
        "otp_per_phone", "phones_per_ip", "devices_per_phone",
        "country_change", "fail_streak",
        "risk_score", "action", "reason",
    ]
    
    # Separate data by region
    full_georgia = scored_df[scored_df["country"] == "GE"].reset_index(drop=True)
    full_other = scored_df[scored_df["country"] != "GE"].reset_index(drop=True)
    
    # Create tabs for each region
    tab_full_georgia, tab_full_other = st.tabs([f"🇬🇪 Georgian Region ({len(full_georgia)})", 
                                                  f"🌍 Other Countries ({len(full_other)})"])
    
    # Georgian Region Tab
    with tab_full_georgia:
        if full_georgia.empty:
            st.info("No data from Georgian region")
        else:
            full_df_georgia = full_georgia[all_cols].copy()
            full_df_georgia["country"] = full_df_georgia["country"].apply(country_to_flag)
            full_styled_georgia = (
                full_df_georgia
                .style
                .apply(highlight_risk, axis=1)
                .format({
                    "timestamp": lambda x: x.strftime("%H:%M:%S"),
                    "risk_score": "{:.0f}",
                    "country_change": lambda x: t("country_change_icon") if x else t("country_no_change_icon"),
                })
            )
            st.dataframe(full_styled_georgia, width='stretch', height=400)
            csv_georgia = full_georgia[all_cols].to_csv(index=False)
            st.download_button(
                t("download_full_csv"),
                data=csv_georgia,
                file_name="full_dataset_georgian_region.csv",
                mime="text/csv",
            )
    
    # Other Countries Tab
    with tab_full_other:
        if full_other.empty:
            st.info("No data from other countries")
        else:
            full_df_other = full_other[all_cols].copy()
            full_df_other["country"] = full_df_other["country"].apply(country_to_flag)
            full_styled_other = (
                full_df_other
                .style
                .apply(highlight_risk, axis=1)
                .format({
                    "timestamp": lambda x: x.strftime("%H:%M:%S"),
                    "risk_score": "{:.0f}",
                    "country_change": lambda x: t("country_change_icon") if x else t("country_no_change_icon"),
                })
            )
            st.dataframe(full_styled_other, width='stretch', height=400)
            csv_other = full_other[all_cols].to_csv(index=False)
            st.download_button(
                t("download_full_csv"),
                data=csv_other,
                file_name="full_dataset_other_countries.csv",
                mime="text/csv",
            )

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# HOW IT WORKS
# ──────────────────────────────────────────────

st.markdown(f'<p class="section-header">{t("how_it_works")}</p>', unsafe_allow_html=True)

with st.expander(t("explanation"), expanded=True):
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"#### {t('signals_used')}")
        st.markdown(
            f'<div class="explain-box">'
            f'<b>{t("signal_1_title")}</b><br>'
            f'{t("signal_1_desc")}<br><br>'
            f'<b>{t("signal_2_title")}</b><br>'
            f'{t("signal_2_desc")}<br><br>'
            f'<b>{t("signal_3_title")}</b><br>'
            f'{t("signal_3_desc")}<br><br>'
            f'<b>{t("signal_4_title")}</b><br>'
            f'{t("signal_4_desc")}<br><br>'
            f'<b>{t("signal_5_title")}</b><br>'
            f'{t("signal_5_desc")}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(f"#### {t('scoring_actions')}")
        st.markdown(
            f'<div class="explain-box">'
            f'{t("scoring_intro")}<br><br>'
            f'<b>{t("allow")}</b> — {t("allow_desc")}<br><br>'
            f'<b>{t("throttle")}</b> — {t("throttle_desc")}<br><br>'
            f'<b>{t("block")}</b> — {t("block_desc")}<br><br>'
            f'<hr style="border-color:rgba(61, 255, 160, 0.2)">'
            f'{t("prototype_warning")}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(f"#### {t('scenarios')}")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            f'<div class="explain-box">'
            f'{t("scenario_normal_title")}<br>'
            f'{t("scenario_normal_desc")}'
            f'</div>',
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f'<div class="explain-box">'
            f'{t("scenario_suspicious_title")}<br>'
            f'{t("scenario_suspicious_desc")}'
            f'</div>',
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            f'<div class="explain-box">'
            f'{t("scenario_abuse_title")}<br>'
            f'{t("scenario_abuse_desc")}'
            f'</div>',
            unsafe_allow_html=True,
        )

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

st.markdown(
    f'<hr style="border-color:rgba(61, 255, 160, 0.2);margin-top:3rem;margin-bottom:2rem">'
    f'<p style="text-align:center;color:#a0aec0;font-size:0.8rem;font-family:\'IBM Plex Mono\',monospace;letter-spacing:0.5px">'
    f'{t("final_footer")}'
    f'</p>',
    unsafe_allow_html=True,
)
