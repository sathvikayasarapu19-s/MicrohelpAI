import streamlit as st
import sqlite3
from datetime import datetime


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="MicroHelp AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_NAME = "microhelp.db"


# ============================================================
# DATABASE
# ============================================================

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem TEXT,
            category TEXT,
            urgency TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_request(problem, category, urgency):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO requests
        (problem, category, urgency, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            problem,
            category,
            urgency,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()


def save_message(sender, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages
        (sender, message, created_at)
        VALUES (?, ?, ?)
        """,
        (
            sender,
            message,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()


create_database()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "problem" not in st.session_state:
    st.session_state.problem = ""

if "detected_problem" not in st.session_state:
    st.session_state.detected_problem = "Not analyzed"

if "selected_helper" not in st.session_state:
    st.session_state.selected_helper = "Arjun Kumar"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "sender": "AI",
            "message": "Hi! 👋 Tell me your problem and I will help you find the right nearby helper."
        }
    ]


# ============================================================
# HELPER DATA
# ============================================================

helpers = [
    {
        "name": "Arjun Kumar",
        "skill": "Electrical Specialist",
        "distance": "0.8 km",
        "rating": 4.9,
        "eta": "3 min",
        "price": "₹149",
        "icon": "👨‍🔧"
    },
    {
        "name": "Priya Sharma",
        "skill": "Home Repair",
        "distance": "1.5 km",
        "rating": 4.8,
        "eta": "5 min",
        "price": "₹129",
        "icon": "👩‍🔧"
    },
    {
        "name": "Ravi Teja",
        "skill": "Plumbing Expert",
        "distance": "1.2 km",
        "rating": 4.9,
        "eta": "4 min",
        "price": "₹159",
        "icon": "👷"
    },
    {
        "name": "Vikram Singh",
        "skill": "Device Technician",
        "distance": "2.1 km",
        "rating": 4.7,
        "eta": "7 min",
        "price": "₹199",
        "icon": "👨‍💻"
    },
    {
        "name": "Anjali Rao",
        "skill": "Electrical Expert",
        "distance": "2.5 km",
        "rating": 4.8,
        "eta": "8 min",
        "price": "₹149",
        "icon": "👩‍🔧"
    },
    {
        "name": "Kiran Kumar",
        "skill": "Multi-Service Helper",
        "distance": "3.1 km",
        "rating": 4.7,
        "eta": "10 min",
        "price": "₹119",
        "icon": "🧑‍🔧"
    }
]


# ============================================================
# AI PROBLEM DETECTION
# ============================================================

def detect_problem(text):

    text = text.lower()

    if any(word in text for word in [
        "road",
        "pothole",
        "potholes",
        "footpath",
        "pavement",
        "street damage",
        "road damage"
    ]):
        return "Road / Infrastructure"

    if any(word in text for word in [
        "electric",
        "electrical",
        "fan",
        "switch",
        "light",
        "socket",
        "wire",
        "power"
    ]):
        return "Electrical"

    if any(word in text for word in [
        "water",
        "pipe",
        "plumbing",
        "tap",
        "leak",
        "leakage",
        "drain"
    ]):
        return "Plumbing"

    if any(word in text for word in [
        "laptop",
        "computer",
        "pc",
        "wifi",
        "internet",
        "keyboard",
        "mouse",
        "mobile",
        "phone",
        "charger"
    ]):
        return "Device / Internet"

    if any(word in text for word in [
        "bike",
        "car",
        "vehicle",
        "scooter",
        "puncture",
        "tyre",
        "tire"
    ]):
        return "Vehicle"

    return "General Assistance"


# ============================================================
# DARK THEME
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background-color: #070b16;
        }

        section[data-testid="stSidebar"] {
            background-color: #0b1020;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 30px;
        }

        h1, h2, h3, h4, p, label {
            color: white !important;
        }

        .main-title {
            font-size: 52px;
            font-weight: 800;
        }

        .blue {
            color: #00e5ff;
        }

        .purple {
            color: #9b6cff;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 MicroHelp")

    st.caption("AI-Powered Quick Help")

    st.divider()

    pages = [
        "Home",
        "Report Problem",
        "AI Matching",
        "Live Location",
        "Track Helper",
        "AI Chat",
        "Notifications",
        "Profile"
    ]

    for page in pages:

        if st.button(
            page,
            key="page_" + page,
            use_container_width=True
        ):
            st.session_state.page = page
            st.rerun()

    st.divider()

    st.caption("CURRENT LOCATION")

    st.write("📍 Hyderabad, Telangana")


# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    st.markdown(
        '<p class="blue">AI-POWERED QUICK HELP</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">Small problem?<br>'
        '<span class="blue">MicroHelp is here.</span></div>',
        unsafe_allow_html=True
    )

    st.write(
        "Tell us what happened, upload a photo, "
        "and MicroHelp AI finds the right nearby "
        "person to help you quickly."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🚀 Get Quick Help",
            use_container_width=True
        ):
            st.session_state.page = "Report Problem"
            st.rerun()

    with col2:

        if st.button(
            "📍 Find Helpers Near Me",
            use_container_width=True
        ):
            st.session_state.page = "Live Location"
            st.rerun()

    st.write("")

    st.subheader("Quick Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Average Response",
            "4 min"
        )

    with c2:
        st.metric(
            "Nearby Helpers",
            "12+"
        )

    with c3:
        st.metric(
            "AI Match Rate",
            "98%"
        )

    with c4:
        st.metric(
            "Community Rating",
            "4.9 ⭐"
        )

    st.write("")

    st.subheader("Popular Help Categories")

    categories = [
        ("⚡", "Electrical"),
        ("🚰", "Plumbing"),
        ("💻", "Device Help"),
        ("🏠", "Home Repair"),
        ("🚗", "Vehicle"),
        ("🪚", "Carpentry"),
        ("🌐", "Internet"),
        ("🔧", "Other")
    ]

    cols = st.columns(4)

    for i, (icon, name) in enumerate(categories):

        with cols[i % 4]:

            with st.container(border=True):
                st.markdown(f"## {icon}")
                st.write(f"**{name}**")


# ============================================================
# REPORT PROBLEM
# ============================================================

elif st.session_state.page == "Report Problem":

    st.markdown(
        '<div class="main-title">Report Your '
        '<span class="blue">Problem</span></div>',
        unsafe_allow_html=True
    )

    st.write(
        "Describe your problem and optionally upload "
        "a photo. AI will identify the required service."
    )

    left, right = st.columns(2)

    with left:

        st.subheader("📷 Upload Photo")

        image = st.file_uploader(
            "Choose a problem image",
            type=["jpg", "jpeg", "png"]
        )

        if image:
            st.image(
                image,
                caption="Uploaded Problem",
                use_container_width=True
            )

    with right:

        st.subheader("📝 Problem Details")

        category = st.selectbox(
            "Category",
            [
                "Auto Detect",
                "Road / Infrastructure",
                "Electrical",
                "Plumbing",
                "Device / Internet",
                "Vehicle",
                "Home Repair",
                "Other"
            ]
        )

        problem = st.text_area(
            "Describe the problem",
            placeholder=(
                "Example: There is a large pothole "
                "near my college gate..."
            ),
            height=150
        )

        urgency = st.selectbox(
            "Urgency",
            [
                "Low",
                "Medium",
                "High",
                "Emergency"
            ]
        )

        if st.button(
            "🤖 Analyze Problem",
            use_container_width=True
        ):

            if not problem.strip():

                st.warning(
                    "Please describe your problem."
                )

            else:

                detected = detect_problem(problem)

                if category != "Auto Detect":
                    detected = category

                st.session_state.problem = problem
                st.session_state.detected_problem = detected

                save_request(
                    problem,
                    detected,
                    urgency
                )

                st.success(
                    "Problem analyzed successfully!"
                )

                st.session_state.page = "AI Matching"

                st.rerun()


# ============================================================
# AI MATCHING
# ============================================================

elif st.session_state.page == "AI Matching":

    st.markdown(
        '<div class="main-title">AI '
        '<span class="blue">Matching</span></div>',
        unsafe_allow_html=True
    )

    detected = st.session_state.detected_problem

    st.info(
        f"🤖 AI detected: {detected}"
    )

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "AI Confidence",
            "96%"
        )

    with b:
        st.metric(
            "Skill Match",
            "91%"
        )

    with c:
        st.metric(
            "Location Match",
            "98%"
        )

    st.subheader("Recommended Nearby Helpers")

    for index, helper in enumerate(helpers):

        with st.container(border=True):

            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                st.markdown(
                    f"# {helper['icon']}"
                )

            with col2:

                st.subheader(
                    helper["name"]
                )

                st.write(
                    helper["skill"]
                )

                st.write(
                    f"📍 {helper['distance']}   "
                    f"⭐ {helper['rating']}   "
                    f"⏱ {helper['eta']}"
                )

            with col3:

                st.write(
                    f"**{helper['price']}**"
                )

                if st.button(
                    "Request",
                    key=f"request_{index}",
                    use_container_width=True
                ):

                    st.session_state.selected_helper = (
                        helper["name"]
                    )

                    st.session_state.page = "Track Helper"

                    st.rerun()


# ============================================================
# LIVE LOCATION
# ============================================================

elif st.session_state.page == "Live Location":

    st.markdown(
        '<div class="main-title">Live '
        '<span class="blue">Location</span></div>',
        unsafe_allow_html=True
    )

    st.write(
        "Find available helpers around your location."
    )

    st.map(
        {
            "lat": [
                17.3850,
                17.3900,
                17.3800,
                17.3950
            ],
            "lon": [
                78.4867,
                78.4900,
                78.4800,
                78.4750
            ]
        },
        zoom=12
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Nearby Helpers",
            "12"
        )

    with c2:
        st.metric(
            "Nearest ETA",
            "3 min"
        )

    with c3:
        st.metric(
            "Nearest Distance",
            "0.8 km"
        )

    st.info(
        "📍 Demo map using Hyderabad coordinates. "
        "Real GPS can be integrated later."
    )


# ============================================================
# TRACK HELPER
# ============================================================

elif st.session_state.page == "Track Helper":

    selected_name = st.session_state.selected_helper

    selected = helpers[0]

    for helper in helpers:

        if helper["name"] == selected_name:
            selected = helper
            break

    st.markdown(
        '<div class="main-title">Track Your '
        '<span class="blue">Helper</span></div>',
        unsafe_allow_html=True
    )

    st.success(
        f"🛵 {selected['name']} is on the way!"
    )

    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            st.title(
                selected["icon"]
            )

            st.subheader(
                selected["name"]
            )

            st.write(
                selected["skill"]
            )

            st.write(
                f"⭐ Rating: {selected['rating']}"
            )

            st.write(
                f"📍 Distance: {selected['distance']}"
            )

            st.write(
                f"⏱ ETA: {selected['eta']}"
            )

            st.write(
                f"💰 Estimated price: {selected['price']}"
            )

    with right:

        st.subheader("Service Status")

        st.success(
            "✓ Request Accepted"
        )

        st.success(
            "✓ Helper Started"
        )

        st.info(
            "● Arriving Soon"
        )

        st.write(
            "○ Problem Solved"
        )

    if st.button(
        "💬 Chat with Helper",
        use_container_width=True
    ):

        st.session_state.page = "AI Chat"
        st.rerun()


# ============================================================
# AI CHAT
# ============================================================

elif st.session_state.page == "AI Chat":

    st.markdown(
        '<div class="main-title">MicroHelp '
        '<span class="blue">AI Chat</span></div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask me about your problem or finding a helper."
    )

    for message in st.session_state.messages:

        if message["sender"] == "User":

            with st.chat_message("user"):
                st.write(message["message"])

        else:

            with st.chat_message("assistant"):
                st.write(message["message"])

    user_message = st.chat_input(
        "Type your message..."
    )

    if user_message:

        st.session_state.messages.append(
            {
                "sender": "User",
                "message": user_message
            }
        )

        save_message(
            "User",
            user_message
        )

        text = user_message.lower()

        if "road" in text or "pothole" in text:

            response = (
                "This looks like a road/infrastructure "
                "problem. A suitable maintenance helper "
                "can be matched."
            )

        elif (
            "electric" in text
            or "fan" in text
            or "light" in text
        ):

            response = (
                "This looks like an electrical problem. "
                "An electrical specialist can help."
            )

        elif (
            "water" in text
            or "pipe" in text
            or "tap" in text
        ):

            response = (
                "This looks like a plumbing problem. "
                "A plumbing expert can help."
            )

        elif (
            "wifi" in text
            or "internet" in text
            or "laptop" in text
        ):

            response = (
                "This looks like a device or internet "
                "problem. A device technician can help."
            )

        elif (
            "hello" in text
            or "hi" in text
        ):

            response = (
                "Hello! 👋 Tell me what problem "
                "you are facing."
            )

        else:

            response = (
                "Please describe your problem in a little "
                "more detail so I can identify the right "
                "service."
            )

        st.session_state.messages.append(
            {
                "sender": "AI",
                "message": response
            }
        )

        save_message(
            "AI",
            response
        )

        st.rerun()


# ============================================================
# NOTIFICATIONS
# ============================================================

elif st.session_state.page == "Notifications":

    st.markdown(
        '<div class="main-title">'
        '<span class="blue">Notifications</span></div>',
        unsafe_allow_html=True
    )

    notifications = [
        (
            "🛵",
            "Helper is on the way",
            "Your selected helper is travelling to you."
        ),
        (
            "🤖",
            "AI matched your problem",
            "The best service category was identified."
        ),
        (
            "✅",
            "Previous service completed",
            "Your previous request was successfully completed."
        ),
        (
            "👋",
            "Welcome to MicroHelp",
            "Find quick local help whenever you need it."
        )
    ]

    for icon, title, message in notifications:

        with st.container(border=True):

            st.subheader(
                f"{icon} {title}"
            )

            st.write(message)


# ============================================================
# PROFILE
# ============================================================

elif st.session_state.page == "Profile":

    st.markdown(
        '<div class="main-title">My '
        '<span class="blue">Profile</span></div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.title("👤")

        st.header("MicroHelp User")

        st.write(
            "📍 Hyderabad, Telangana"
        )

        st.write(
            "⭐ Community Rating: 4.8"
        )

    st.write("")

    a, b, c, d = st.columns(4)

    with a:
        st.metric(
            "Requests",
            "12"
        )

    with b:
        st.metric(
            "Completed",
            "10"
        )

    with c:
        st.metric(
            "Saved",
            "4"
        )

    with d:
        st.metric(
            "Member Since",
            "2026"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 MicroHelp AI • AI-Powered Quick Help & Smart Matching Platform"
)
