import streamlit as st
import random

# 1. Basic Page Configuration
st.set_page_config(
    page_title="UPSC PrepQuest",
    page_icon="⚡",
    layout="centered"
)

# 2. Syllabus Data Pool
SUBJECTS = ["📜 INDIAN POLITY", "🏛️ MODERN HISTORY", "🌍 GEOGRAPHY", "📈 ECONOMY", "🧬 SCIENCE & TECH"]

CORE_TOPICS = {
    "📜 INDIAN POLITY": [
        {"q": "Consider Article {param} of the Constitution. Which foundational pillar does it fundamentally protect?", "ans": "Fundamental Rights of Citizens", "opts": ["Fundamental Rights of Citizens", "Directive Principles", "Emergency Legislative Powers", "Local Municipal Governance"], "fact": "Part III (Articles 12-35) forms the core shield for individual civil liberties in India."},
        {"q": "The landmark 'Basic Structure Doctrine' limiting parliamentary amendment powers was established in which year context?", "ans": "Kesavananda Bharati Case", "opts": ["Kesavananda Bharati Case", "Golaknath Case", "Minerva Mills Case", "Maneka Gandhi Case"], "fact": "The Supreme Court in 1973 ruled that certain core features of the Constitution cannot be altered by Parliament."}
    ],
    "🏛️ MODERN HISTORY": [
        {"q": "In the nationalist timeline, the historic Poorna Swaraj resolution was adopted at which major assembly?", "ans": "Lahore Session of 1929", "opts": ["Lahore Session of 1929", "Calcutta Session of 1920", "Karachi Session of 1931", "Bombay Session of 1942"], "fact": "Under Jawaharlal Nehru's presidency, the Indian National Congress unfurled the tricolor demanding absolute independence."},
        {"q": "The Indigo Revolt in 19th-century Bengal was direct mass resistance against:", "ans": "Forced exploitative cash cropping", "opts": ["Forced exploitative cash cropping", "Salt manufacturing monopolies", "High religious entry taxes", "Vernacular press censorship laws"], "fact": "Peasants defied British planters who used coercive contracts to force indigo planting over essential food crops."}
    ],
    "🌍 GEOGRAPHY": [
        {"q": "The vital 'Ten Degree Channel' forms a strategic geographic separation boundary between:", "ans": "Andaman and Nicobar Islands", "opts": ["Andaman and Nicobar Islands", "Lakshadweep and Maldivian Atolls", "Sumatra and Java Islands", "Sri Lanka and Mainland India"], "fact": "It is a water body lying on the 10° N parallel in the Bay of Bengal separating the two major island groups."},
        {"q": "Which distinctive ocean current directly alters the subcontinental summer monsoon dynamic?", "ans": "Somali Current", "opts": ["Somali Current", "Agulhas Current", "Kuroshio Current", "Oyashio Current"], "fact": "The seasonal reversal of the Somali Current heavily influences low-pressure dynamics over the Arabian Sea."}
    ],
    "📈 ECONOMY": [
        {"q": "When the Reserve Bank of India increases the Repo Rate by {param} basis points, it usually results in:", "ans": "Contraction of market liquidity", "opts": ["Contraction of market liquidity", "Expansion of consumer credit", "Depreciation of domestic currency", "Surge in fiscal deficit"], "fact": "Higher repo rates make borrowing expensive for commercial banks, which cools down circulating market liquidity to fight inflation."},
        {"q": "What core characteristic defines Demand-Pull Inflation in an expanding macro-economy?", "ans": "Aggregate demand outpacing total aggregate supply", "opts": ["Aggregate demand outpacing total aggregate supply", "Sudden supply-chain manufacturing shocks", "Inefficient distribution and hoarding infrastructure", "Rapid depreciation of foreign exchange reserves"], "fact": "When economic demand rises faster than goods can be produced, prices get pulled upwards naturally."}
    ],
    "🧬 SCIENCE & TECH": [
        {"q": "The disruptive CRISPR-Cas9 scientific tool is utilized globally for which application?", "ans": "Targeted genome and gene editing", "opts": ["Targeted genome and gene editing", "Secure quantum network data routing", "Deep-sea tectonic structural mapping", "Advanced solid biofuel synthesis parameters"], "fact": "It acts as programmable molecular scissors allowing scientists to alter specific DNA sequence lines."},
        {"q": "What fundamental principle enables Web 3.0 ecosystems to operate without tech monopolies?", "ans": "Decentralized cryptographic ledger networks", "opts": ["Decentralized cryptographic ledger networks", "Centralized cloud computing pipelines", "Hyper-speed optical fiber tracking setups", "Monetized corporate web data silos"], "fact": "Web3 leverages peer-to-peer blockchain validation models so users retain data ownership sovereignty."}
    ]
}

# 3. Dynamic Question Generator Engine
def get_dynamic_question(level, q_num):
    random.seed(level * 777 + q_num)
    subj = random.choice(SUBJECTS)
    template = random.choice(CORE_TOPICS[subj])
    
    if q_num < 30:
        diff = "Simple"
    elif q_num < 80:
        diff = "Medium"
    else:
        diff = "Hard"
        
    param_val = random.randint(10 + level, 250 + level)
    q_text = template["q"].format(param=param_val)
    
    shuffled_options = list(template["opts"])
    random.shuffle(shuffled_options)
    
    return {
        "subject": subj,
        "difficulty": diff,
        "question": q_text,
        "options": shuffled_options,
        "answer": template["ans"],
        "fact": template["fact"]
    }

# 4. State Management
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 5
if 'chosen_ans' not in st.session_state:
    st.session_state.chosen_ans = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

# Sidebar Configuration
st.sidebar.title("🎮 UPSC Quest Panel")
st.sidebar.metric(label="🔥 Day Streak", value=f"{st.session_state.streak} Days")
st.sidebar.metric(label="⚡ Total Score (XP)", value=f"{st.session_state.xp} XP")

input_level = st.sidebar.number_input("Jump to Level (1-1000)", min_value=1, max_value=1000, value=st.session_state.level)

if input_level != st.session_state.level:
    st.session_state.level = input_level
    st.session_state.q_idx = 0
    st.session_state.chosen_ans = None
    st.session_state.answered = False
    st.rerun()

# 5. Application Main Headers
st.title("⚡ UPSC PrepQuest")
st.subheader(f"Level {st.session_state.level} — Question {st.session_state.q_idx + 1} of 100")

st.progress(st.session_state.q_idx / 100)

MAX_QUESTIONS = 100

if st.session_state.q_idx >= MAX_QUESTIONS:
    st.balloons()
    st.success(f"🏆 Level {st.session_state.level} Finished! You gained +500 XP bonus!")
    if st.button("Unlock Next Level 🚀", type="primary"):
        st.session_state.level += 1
        st.session_state.q_idx = 0
        st.session_state.xp += 500
        st.session_state.chosen_ans = None
        st.session_state.answered = False
        st.rerun()
else:
    current_q = get_dynamic_question(st.session_state.level, st.session_state.q_idx)
    st.warning(f"🏷️ Subject: {current_q['subject']} | 📈 Difficulty: {current_q['difficulty'].upper()}")
    st.info(current_q["question"])

    for i, opt in enumerate(current_q["options"]):
        btn_key = f"q_{st.session_state.level}_{st.session_state.q_idx}_{i}"
        
        if not st.session_state.answered:
            if st.button(opt, key=btn_key, use_container_width=True):
                st.session_state.chosen_ans = opt
                st.session_state.answered = True
                if opt == current_q["answer"]:
                    st.session_state.xp += 20
                st.rerun()
        else:
            if opt == current_q["answer"]:
                st.success(f"✅ {opt} (Correct Answer)")
            elif opt == st.session_state.chosen_ans:
                st.error(f"❌ {opt} (Your Selection)")
            else:
                st.button(opt, key=f"dis_{btn_key}", disabled=True, use_container_width=True)

    if st.session_state.answered:
        st.markdown("---")
        if st.session_state.chosen_ans == current_q["answer"]:
            st.success("🎉 Correct! +20 XP Added to profile!")
        else:
            st.error("❌ Incorrect answer. Keep learning!")
            
        st.markdown(f"**📚 Exam Insight Fact:** {current_q['fact']}")
        
        if st.button("Continue Journey ➡️", type="primary", use_container_width=True):
            st.session_state.q_idx += 1
            st.session_state.chosen_ans = None
            st.session_state.answered = False
            st.rerun()

st.markdown("---")
st.caption("🚀 Created by **Charan Singh** | Designed to make learning addictive.")
