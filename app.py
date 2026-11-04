import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="מחשבון עץ יוחסין ומוצא גנטי",
    layout="centered"
)

# הגדרת כיוון RTL לממשק בעברית
st.markdown("""
<style>
    .main { direction: rtl; text-align: right; }
    div[data-baseweb="select"] { direction: rtl; }
    input { text-align: right; }
</style>
""", unsafe_allow_html=True)

st.title("🌳 מחשבון עץ יוחסין ומוצא גנטי")

# ניהול מצב השלבים
if "step" not in st.session_state:
    st.session_state.step = 1
if "data" not in st.session_state:
    st.session_state.data = {}

# ---------- שלב 1: הילד והוריו ----------
if st.session_state.step == 1:
    st.subheader("שלב 1 מתוך 4: פרטי הילד והוריו")
    st.caption("הזן את שם הילד/ה ואת שמות ההורים")

    child_name = st.text_input("שם הילד/ה:", value=st.session_state.data.get("child", ""))
    father_name = st.text_input("שם האבא:", value=st.session_state.data.get("father", ""))
    mother_name = st.text_input("שם האמא:", value=st.session_state.data.get("mother", ""))

    if st.button("המשך לשלב 2 >"):
        if not child_name or not father_name or not mother_name:
            st.warning("אנא מלא את כל השדות בשלב זה.")
        else:
            st.session_state.data["child"] = child_name
            st.session_state.data["father"] = father_name
            st.session_state.data["mother"] = mother_name
            st.session_state.step = 2
            st.rerun()

# ---------- שלב 2: סבים וסבתות ----------
elif st.session_state.step == 2:
    father_name = st.session_state.data["father"]
    mother_name = st.session_state.data["mother"]

    st.subheader("שלב 2 מתוך 4: הסבים והסבתות (דור 2)")
    st.caption("הזן את שמות ההורים של האבא והאמא")

    st.markdown(f"**ההורים של {father_name} (צד אבא):**")
    gf_p = st.text_input(f"אבא של {father_name}:", value=st.session_state.data.get("gf_p", ""))
    gm_p = st.text_input(f"אמא של {father_name}:", value=st.session_state.data.get("gm_p", ""))

    st.markdown(f"**ההורים של {mother_name} (צד אמא):**")
    gf_m = st.text_input(f"אבא של {mother_name}:", value=st.session_state.data.get("gf_m", ""))
    gm_m = st.text_input(f"אמא של {mother_name}:", value=st.session_state.data.get("gm_m", ""))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("< חזור"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("המשך לשלב 3 >"):
            st.session_state.data["gf_p"] = gf_p or f"סבא ({father_name})"
            st.session_state.data["gm_p"] = gm_p or f"סבתא ({father_name})"
            st.session_state.data["gf_m"] = gf_m or f"סבא ({mother_name})"
            st.session_state.data["gm_m"] = gm_m or f"סבתא ({mother_name})"
            st.session_state.step = 3
            st.rerun()

# ---------- שלב 3: סבי-רבא ----------
elif st.session_state.step == 3:
    st.subheader("שלב 3 מתוך 4: סבי-רבא (דור 3)")
    st.caption("הזן את שמות ההורים של הסבים והסבתות")

    grandparents = [
        ("gf_p", st.session_state.data["gf_p"]),
        ("gm_p", st.session_state.data["gm_p"]),
        ("gf_m", st.session_state.data["gf_m"]),
        ("gm_m", st.session_state.data["gm_m"])
    ]

    gg_dict = {}
    for key, name in grandparents:
        st.markdown(f"**ההורים של {name}:**")
        c1, c2 = st.columns(2)
        with c1:
            f_name = st.text_input(f"אבא של {name}:", key=f"{key}_f")
        with c2:
            m_name = st.text_input(f"אמא של {name}:", key=f"{key}_m")
        
        gg_dict[f"{key}_f"] = f_name or f"אבא של {name}"
        gg_dict[f"{key}_m"] = m_name or f"אמא של {name}"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("< חזור"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("המשך לשלב 4 >"):
            st.session_state.data["gg_names"] = gg_dict
            st.session_state.step = 4
            st.rerun()

# ---------- שלב 4: דור 5 (סבי-רבא-רבא) והזנת מוצא ----------
elif st.session_state.step == 4:
    st.subheader("שלב 4 מתוך 4: דור 5 והזנת מוצא")
    st.caption("הזן את שמות הקדמונים (16 אבות/אימהות), המוצא והסיווג העדתי")

    ggg_data = {}
    for k, parent_name in st.session_state.data["gg_names"].items():
        with st.expander(f"ההורים של {parent_name}", expanded=False):
            st.markdown(f"**אבא של {parent_name}:**")
            c1, c2, c3 = st.columns([2, 2, 2])
            with c1:
                fn = st.text_input("שם האב", key=f"{k}_f_name")
            with c2:
                fe = st.text_input("מוצא (למשל: פולני)", key=f"{k}_f_eth")
            with c3:
                fc = st.selectbox("סיווג", ["אשכנזי", "מזרחי", "אחר"], key=f"{k}_f_cat")

            st.markdown(f"**אמא של {parent_name}:**")
            c1, c2, c3 = st.columns([2, 2, 2])
            with c1:
                mn = st.text_input("שם האם", key=f"{k}_m_name")
            with c2:
                me = st.text_input("מוצא (למשל: עיראקי)", key=f"{k}_m_eth")
            with c3:
                mc = st.selectbox("סיווג", ["אשכנזי", "מזרחי", "אחר"], key=f"{k}_m_cat")

            ggg_data[f"{k}_f"] = {"name": fn or f"אבא של {parent_name}", "eth": fe, "cat": fc}
            ggg_data[f"{k}_m"] = {"name": mn or f"אמא של {parent_name}", "eth": me, "cat": mc}

    col1, col2 = st.columns(2)
    with col1:
        if st.button("< חזור"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("חשב מוצא והצג תוצאות 📊"):
            st.session_state.data["ggg_data"] = ggg_data
            st.session_state.step = 5
            st.rerun()

# ---------- שלב 5: הצגת התוצאות והתרשימים ----------
elif st.session_state.step == 5:
    child_name = st.session_state.data["child"]
    st.subheader(f"📊 תוצאות מוצא גנטי עבור {child_name}")

    ggg_data = st.session_state.data["ggg_data"]
    eth_counts = {}
    cat_counts = {"אשכנזי": 0.0, "מזרחי": 0.0, "אחר": 0.0}
    total_weight = 0

    for item in ggg_data.values():
        eth = item["eth"].strip()
        cat = item["cat"]
        if eth:
            origins = [x.strip().capitalize() for x in eth.split(",") if x.strip()]
            if origins:
                w = 6.25 / len(origins)
                for o in origins:
                    eth_counts[o] = eth_counts.get(o, 0.0) + w
                cat_counts[cat] = cat_counts.get(cat, 0.0) + 6.25
                total_weight += 6.25

    if total_weight == 0:
        st.warning("לא הוכנס מידע על מוצא. חזור לשלב 4 והזן מוצא לפחות עבור קדמון אחד.")
        if st.button("< חזור לשלב 4"):
            st.session_state.step = 4
            st.rerun()
    else:
        factor = 100.0 / total_weight

        # 1. דוח אחוזים
        st.markdown("### 🧬 אחוזי מוצא גנטי משוערים")
        eth_df = pd.DataFrame([
            {"מוצא": k, "אחוז": round(v * factor, 1)}
            for k, v in sorted(eth_counts.items(), key=lambda x: x[1], reverse=True)
        ])
        st.dataframe(eth_df, use_container_width=True, hide_index=True)

        # 2. תרשים עמודות - מוצאים מפורטים
        st.markdown("### 📈 פילוח מוצא מפורט")
        st.bar_chart(eth_df.set_index("מוצא"))

        # 3. תרשים עוגה - חלוקה עדתית
        st.markdown("### ☯️ חלוקה עדתית (אשכנזי / מזרחי)")
        cat_df = pd.DataFrame([
            {"עדתי": k, "אחוז": round((v / total_weight) * 100, 1)}
            for k, v in cat_counts.items() if v > 0
        ])
        st.dataframe(cat_df, use_container_width=True, hide_index=True)

        if st.button("התחל מחדש 🔄"):
            st.session_state.step = 1
            st.session_state.data = {}
            st.rerun()
