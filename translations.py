"""
Language translations for OTP Anomaly Detector
"""

TRANSLATIONS = {
    "en": {
        # Page
        "page_title": "OTP Anomaly Detector",
        "page_subtitle": "Real-time rule-based detection of suspicious one-time password request patterns.",
        
        # Sidebar
        "controls": "⚙️ Controls",
        "event_counts": "Event counts",
        "normal_events": "Normal events",
        "suspicious_events": "Suspicious events",
        "abuse_events": "Abuse events",
        "detection_windows": "Detection windows",
        "otp_phone_window": "OTP / phone window (min)",
        "phones_ip_window": "Phones / IP window (min)",
        "devices_phone_window": "Devices / phone window (h)",
        "random_seed": "Random seed",
        "regenerate_data": "🔄 Regenerate data",
        "footer_text": "🔐 OTP Anomaly Detector<br>Hackathon Prototype · v1.0<br><span style='color:#3dffa0'>Rule-based · Not ML</span>",
        
        # Metrics
        "overview": "Overview",
        "total_events": "Total Events",
        "flagged": "Flagged",
        "blocked": "Blocked",
        "throttled": "Throttled",
        "flag_rate": "Flag Rate",
        
        # Charts
        "distribution": "Distribution",
        "risk_score_distribution": "Risk score distribution",
        "low_risk": "Low (0–10)",
        "moderate_risk": "Moderate (11–34)",
        "high_risk": "High (35–69)",
        "critical_risk": "Critical (70–100)",
        "action_breakdown": "Action breakdown",
        
        # Flagged events
        "flagged_events": "Flagged Events",
        "events_requiring_attention": "Events requiring attention — sorted by risk score (highest first)",
        "no_flagged_events": "No flagged events with current settings.",
        "download_flagged_csv": "⬇️ Download flagged events CSV",
        "flagged_filename": "flagged_otp_events.csv",
        
        # Full dataset
        "full_dataset": "📋 Full dataset with computed features",
        "download_full_csv": "⬇️ Download full dataset CSV",
        "full_filename": "all_otp_events.csv",
        "country_change_icon": "✓",
        "country_no_change_icon": "–",
        
        # How it works
        "how_it_works": "How It Works",
        "explanation": "📖 Explanation — click to expand",
        "signals_used": "🔍 Signals used",
        "signal_1_title": "1. OTPs per phone (short window)",
        "signal_1_desc": "Counts how many OTP requests the same phone number received in the last N minutes. A legitimate user rarely needs more than 1–2 OTPs in a few minutes.",
        "signal_2_title": "2. Unique phones per IP",
        "signal_2_desc": "Counts how many different phone numbers were targeted from the same IP recently. An attacker enumerating phone numbers shows up here.",
        "signal_3_title": "3. Devices per phone",
        "signal_3_desc": "Tracks how many different devices were used for the same phone. Multiple devices can indicate credential sharing or account takeover.",
        "signal_4_title": "4. Country change",
        "signal_4_desc": "Flags if the request country changed since the last OTP for the same phone. Sudden geo-hops are unusual for real users.",
        "signal_5_title": "5. Failure streak",
        "signal_5_desc": "Counts consecutive failed OTP deliveries. Repeated failures often mean the attacker is probing fake or enumerated numbers.",
        
        "scoring_actions": "⚖️ Scoring & actions",
        "scoring_intro": "Each signal adds points to the <b>risk score (0–100)</b>. Signals are additive — the more that fire simultaneously, the higher the score.",
        "allow": "🟢 Allow",
        "allow_desc": "score &lt; 35<br>Request looks normal. OTP is delivered without any friction.",
        "throttle": "🟡 Throttle",
        "throttle_desc": "score 35–69<br>Request is suspicious. Introduce a delay or require CAPTCHA before delivering.",
        "block": "🔴 Block",
        "block_desc": "score ≥ 70<br>Request is highly anomalous. Drop it silently and alert the security team.",
        "prototype_warning": "<b>⚠️ This is a prototype</b><br>Thresholds and weights are hand-tuned heuristics, not trained ML. In production you would calibrate these on real traffic, add ML models, and integrate with your fraud database.",
        
        "scenarios": "🧪 Synthetic data scenarios",
        "scenario_normal_title": "<b>🟢 Normal</b>",
        "scenario_normal_desc": "Diverse users across many IPs, low OTP frequency, consistent countries.",
        "scenario_suspicious_title": "<b>🟡 Suspicious</b>",
        "scenario_suspicious_desc": "A few phones receive many OTPs in a short window — possible account takeover or SMS pumping.",
        "scenario_abuse_title": "<b>🔴 Abuse</b>",
        "scenario_abuse_desc": "One attacker IP rapidly targets many different phone numbers — classic SMS toll-fraud or enumeration attack.",
        
        # Footer
        "final_footer": "OTP Anomaly Detector · Hackathon Prototype · Rule-based, not production ML",
    },
    "ka": {
        # Page
        "page_title": "OTP ანომალიების დეტექტორი",
        "page_subtitle": "ერთჯერადი პაროლის (OTP) საეჭვო მოთხოვნების რეალურ დროში გამოვლენა წესებზე დაფუძნებული ალგორითმით.",
        
        # Sidebar
        "controls": "⚙️ მართვის პანელი",
        "event_counts": "მოვლენების რაოდენობა",
        "normal_events": "ნორმალური მოვლენები",
        "suspicious_events": "საეჭვო მოვლენები",
        "abuse_events": "ბოროტად გამოყენების შემთხვევები",
        "detection_windows": "გამოვლენის ინტერვალები",
        "otp_phone_window": "OTP / ტელეფონის ინტერვალი (წთ)",
        "phones_ip_window": "ტელეფონები / IP ინტერვალი (წთ)",
        "devices_phone_window": "მოწყობილობები / ტელეფონის ინტერვალი (სთ)",
        "random_seed": "შემთხვევითობის პარამეტრი (Seed)",
        "regenerate_data": "🔄 მონაცემების განახლება",
        "footer_text": "🔐 OTP ანომალიების დეტექტორი<br>ჰაკათონის პროტოტიპი · v1.0<br><span style='color:#3dffa0'>Rule-based · არა ML</span>",
        
        # Metrics
        "overview": "ზოგადი მიმოხილვა",
        "total_events": "სულ მოვლენები",
        "flagged": "მონიშნული",
        "blocked": "დაბლოკილი",
        "throttled": "შეზღუდული (Throttled)",
        "flag_rate": "მონიშვნის მაჩვენებელი",
        
        # Charts
        "distribution": "განაწილება",
        "risk_score_distribution": "რისკ-ქულების განაწილება",
        "low_risk": "დაბალი (0–10)",
        "moderate_risk": "საშუალო (11–34)",
        "high_risk": "მაღალი (35–69)",
        "critical_risk": "კრიტიკული (70–100)",
        "action_breakdown": "განხორციელებული ქმედებები",
        
        # Flagged events
        "flagged_events": "მონიშნული მოვლენები",
        "events_requiring_attention": "მოვლენები, რომლებიც ყურადღებას საჭიროებს — დალაგებულია რისკ-ქულის მიხედვით (ჯერ ყველაზე მაღალი)",
        "no_flagged_events": "მოცემული პარამეტრებით საეჭვო მოვლენები არ ფიქსირდება.",
        "download_flagged_csv": "⬇️ მონიშნული მოვლენების CSV ჩამოტვირთვა",
        "flagged_filename": "flagged_otp_events.csv",
        
        # Full dataset
        "full_dataset": "📋 სრული მონაცემები გამოთვლილი პარამეტრებით",
        "download_full_csv": "⬇️ სრული ბაზის CSV ჩამოტვირთვა",
        "full_filename": "all_otp_events.csv",
        "country_change_icon": "✓",
        "country_no_change_icon": "–",
        
        # How it works
        "how_it_works": "როგორ მუშაობს",
        "explanation": "📖 განმარტება — დააჭირეთ გასაშლელად",
        "signals_used": "🔍 გამოყენებული სიგნალები",
        "signal_1_title": "1. OTP-ები ერთ ნომერზე (მოკლე ინტერვალი)",
        "signal_1_desc": "ითვლის, თუ რამდენი OTP მოთხოვნა გაიგზავნა ერთსა და იმავე ნომერზე ბოლო N წუთის განმავლობაში. რეალურ მომხმარებელს იშვიათად სჭირდება 1-2 მოთხოვნაზე მეტი.",
        "signal_2_title": "2. უნიკალური ნომრები ერთ IP-ზე",
        "signal_2_desc": "ითვლის, თუ რამდენი სხვადასხვა ნომერი იქნა მონიშნული ერთი და იმავე IP-დან. ეს მიუთითებს ნომრების მასიურ გადარჩევაზე (enumeration).",
        "signal_3_title": "3. მოწყობილობები ერთ ნომერზე",
        "signal_3_desc": "აკონტროლებს, თუ რამდენი სხვადასხვა მოწყობილობა იქნა გამოყენებული ერთი ნომრისთვის. ეს შესაძლოა მიუთითებდეს ანგარიშის გატეხვაზე ან მონაცემების გაზიარებაზე.",
        "signal_4_title": "4. ქვეყნის ცვლილება",
        "signal_4_desc": "ინიშნება, თუ მოთხოვნის ქვეყანა შეიცვალა წინა OTP-სთან შედარებით. გეოგრაფიული ადგილმდებარეობის მკვეთრი ცვლილება მომხმარებლისთვის უჩვეულოა.",
        "signal_5_title": "5. წარუმატებელი მცდელობების სერია",
        "signal_5_desc": "ითვლის OTP-ს მიწოდების წარუმატებელ მცდელობებს. ხშირი შეცდომები მიანიშნებს, რომ შემტევი ცდილობს გამოიცნოს არსებული ნომრები.",
        
        "scoring_actions": "⚖️ ქულები და ქმედებები",
        "scoring_intro": "თითოეული სიგნალი ამატებს ქულებს <b>რისკ-ქულას (0–100)</b>. სიგნალები ჯამდება — რაც მეტი სიგნალი ფიქსირდება ერთდროულად, მით მაღალია ქულა.",
        "allow": "🟢 დაშვება",
        "allow_desc": "ქულა &lt; 35<br>მოთხოვნა ნორმალურია. OTP იგზავნება ყოველგვარი შეფერხების გარეშე.",
        "throttle": "🟡 შეზღუდვა",
        "throttle_desc": "ქულა 35–69<br>მოთხოვნა საეჭვოა. გამოიყენება დაყოვნება ან CAPTCHA გაგზავნამდე.",
        "block": "🔴 დაბლოკვა",
        "block_desc": "ქულა ≥ 70<br>მოთხოვნა მაღალი რისკის შემცველია. იბლოკება უხმოდ და იგზავნება შეტყობინება უსაფრთხოების გუნდთან.",
        "prototype_warning": "<b>⚠️ ეს არის პროტოტიპი</b><br>ზღურბლები და წონები ეფუძნება ევრისტიკულ წესებს და არა ნასწავლ ML მოდელს. რეალურ გარემოში საჭიროა მათი კალიბრაცია ტრაფიკზე დაყრდნობით.",
        
        "scenarios": "🧪 სინთეტიკური მონაცემების სცენარები",
        "scenario_normal_title": "<b>🟢 ნორმალური</b>",
        "scenario_normal_desc": "სხვადასხვა მომხმარებელი განსხვავებული IP-ებიდან, დაბალი სიხშირე, მუდმივი ქვეყანა.",
        "scenario_suspicious_title": "<b>🟡 საეჭვო</b>",
        "scenario_suspicious_desc": "რამდენიმე ნომერზე იგზავნება ბევრი OTP მოკლე დროში — შესაძლო ანგარიშის გატეხვა ან SMS-პამპინგი.",
        "scenario_abuse_title": "<b>🔴 ბოროტად გამოყენება</b>",
        "scenario_abuse_desc": "ერთი შემტევი IP-დან ხდება ბევრი სხვადასხვა ნომრის მიზანში ამოღება — კლასიკური SMS თაღლითობა.",
        
        # Footer
        "final_footer": "OTP ანომალიების დეტექტორი · ჰაკათონის პროტოტიპი · წესებზე დაფუძნებული სისტემა",
    },
}

def get_text(key: str, lang: str = "en") -> str:
    """Get translated text for a given key and language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
