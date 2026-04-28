import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mentor Clean Code",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;900&family=Fira+Code:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* ── Background : grille blueprint ── */
    .stApp {
        background-color: #05070f;
        background-image:
            linear-gradient(rgba(56,189,248,0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56,189,248,0.04) 1px, transparent 1px),
            radial-gradient(ellipse 70% 50% at 20% 30%, rgba(99,102,241,0.1), transparent),
            radial-gradient(ellipse 50% 60% at 85% 70%, rgba(56,189,248,0.07), transparent);
        background-size: 40px 40px, 40px 40px, 100% 100%, 100% 100%;
        min-height: 100vh;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 0 !important;
        padding-bottom: 3rem !important;
        max-width: 620px !important;
    }

    /* ── Hero section ── */
    .hero {
        position: relative;
        padding: 3.5rem 0 2rem;
        text-align: center;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.2);
        border-radius: 100px;
        padding: 5px 14px;
        font-family: 'Fira Code', monospace;
        font-size: 10px;
        color: #38bdf8;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .hero-badge::before {
        content: '';
        width: 6px; height: 6px;
        background: #38bdf8;
        border-radius: 50%;
        box-shadow: 0 0 8px #38bdf8;
        animation: blink 2s ease-in-out infinite;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 48px;
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.04em;
        color: #f8faff;
        margin: 0 0 0.6rem;
    }

    .hero-title .accent {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-sub {
        font-family: 'Fira Code', monospace;
        font-size: 12px;
        color: #2d3a5a;
        letter-spacing: 0.5px;
    }

    /* ── Section label ── */
    .slabel {
        font-family: 'Fira Code', monospace;
        font-size: 9px;
        color: #38bdf8;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 1.4rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .slabel::before {
        content: '//';
        color: rgba(56,189,248,0.3);
    }

    .slabel::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(56,189,248,0.15), transparent);
    }

    /* ── Inputs ── */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        font-family: 'Fira Code', monospace !important;
        font-size: 10px !important;
        color: #3a4a6a !important;
        text-transform: uppercase;
        letter-spacing: 2.5px;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(56,189,248,0.03) !important;
        border: 1px solid rgba(56,189,248,0.1) !important;
        border-radius: 12px !important;
        color: #e2e8f8 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 13px !important;
        padding: 13px 16px !important;
        caret-color: #38bdf8 !important;
        transition: all 0.2s !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(56,189,248,0.45) !important;
        box-shadow: 0 0 0 4px rgba(56,189,248,0.06), inset 0 0 20px rgba(56,189,248,0.03) !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #1e2840 !important;
    }

    /* ── Selectbox ── */
    [data-baseweb="select"] > div {
        background: rgba(56,189,248,0.03) !important;
        border: 1px solid rgba(56,189,248,0.1) !important;
        border-radius: 12px !important;
        color: #e2e8f8 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 12px !important;
        transition: border-color 0.2s !important;
    }

    [data-baseweb="select"] > div:hover {
        border-color: rgba(56,189,248,0.35) !important;
    }

    /* ── Primary button ── */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase;
        padding: 15px 28px !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        margin-top: 0.6rem !important;
    }

    .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 32px rgba(56,189,248,0.2), 0 4px 12px rgba(99,102,241,0.2) !important;
    }

    .stButton > button:active {
        transform: scale(0.985) translateY(0) !important;
    }

    /* ── Switch link ── */
    .auth-switch {
        text-align: center;
        margin-top: 1.4rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        font-family: 'Outfit', sans-serif;
        font-size: 14px;
        color: #2d3a5a;
    }

    .auth-switch strong {
        color: #38bdf8;
        font-weight: 600;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #030509 !important;
        border-right: 1px solid rgba(56,189,248,0.07) !important;
    }

    [data-testid="stSidebarContent"] {
        padding: 1.5rem 1rem !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: rgba(56,189,248,0.06) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56,189,248,0.15) !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 11px !important;
        letter-spacing: 1.5px;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(56,189,248,0.12) !important;
        transform: none !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stRadio > label {
        font-family: 'Fira Code', monospace !important;
        font-size: 9px !important;
        color: #1e2840 !important;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        font-family: 'Outfit', sans-serif !important;
        font-size: 14px !important;
        color: #4a5a7a !important;
    }

    /* ── User badge ── */
    .user-badge {
        background: rgba(56,189,248,0.05);
        border: 1px solid rgba(56,189,248,0.12);
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
    }

    .user-badge::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(56,189,248,0.4), transparent);
    }

    .user-badge-tag {
        font-family: 'Fira Code', monospace;
        font-size: 9px;
        color: #38bdf8;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .user-badge-name {
        font-family: 'Outfit', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #f0f4ff;
        letter-spacing: -0.01em;
    }

    /* ── Alerts ── */
    .stSuccess > div {
        background: rgba(34,197,94,0.07) !important;
        border: 1px solid rgba(34,197,94,0.2) !important;
        border-radius: 12px !important;
        color: #4ade80 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 12px !important;
    }

    .stError > div {
        background: rgba(248,113,113,0.07) !important;
        border: 1px solid rgba(248,113,113,0.2) !important;
        border-radius: 12px !important;
        color: #f87171 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 12px !important;
    }

    .stWarning > div {
        background: rgba(251,191,36,0.07) !important;
        border: 1px solid rgba(251,191,36,0.2) !important;
        border-radius: 12px !important;
        color: #fbbf24 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 12px !important;
    }

    .stSpinner > div { border-top-color: #38bdf8 !important; }

    /* ── Markdown output ── */
    .stMarkdown p, .stMarkdown li {
        font-family: 'Fira Code', monospace !important;
        font-size: 13px !important;
        color: #94a3c8 !important;
        line-height: 1.9 !important;
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #e2e8f8 !important;
        font-weight: 700 !important;
    }

    .stMarkdown code {
        background: rgba(56,189,248,0.08) !important;
        color: #7dd3fc !important;
        border-radius: 5px !important;
        padding: 2px 7px !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 12px !important;
        border: 1px solid rgba(56,189,248,0.12) !important;
    }

    /* ── Result box ── */
    .result-wrap {
        background: rgba(56,189,248,0.02);
        border: 1px solid rgba(56,189,248,0.1);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-top: 0.5rem;
        position: relative;
        overflow: hidden;
    }

    .result-wrap::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
    }

    /* ── Stats row ── */
    .stats-row {
        display: flex;
        gap: 6px;
        justify-content: flex-end;
        margin-top: -8px;
        margin-bottom: 6px;
    }

    .stat-chip {
        font-family: 'Fira Code', monospace;
        font-size: 10px;
        color: #2d3a5a;
        background: rgba(56,189,248,0.04);
        border: 1px solid rgba(56,189,248,0.08);
        border-radius: 6px;
        padding: 3px 9px;
    }

    .stTextArea textarea { min-height: 280px !important; }
    [data-testid="column"] { padding: 0 6px !important; }
    </style>
    """, unsafe_allow_html=True)


def render_hero(mode="login"):
    subs = {
        "login":    "// Authentifie-toi pour accéder à l'agent IA",
        "register": "// Crée ton compte · Moins de 30 secondes",
        "app":      "// Analyse · Refactorise · Améliore",
    }
    st.markdown(f"""
    <div class="hero">
        <div class="hero-badge">v2.0 · stable</div>
        <h1 class="hero-title">Mentor<br><span class="accent">Clean Code</span></h1>
        <p class="hero-sub">{subs.get(mode, '')}</p>
    </div>
    """, unsafe_allow_html=True)


# ── Login ──────────────────────────────────────────────────────────────────────
def login_page():
    render_hero("login")

    st.markdown('<div class="slabel">Connexion</div>', unsafe_allow_html=True)

    username = st.text_input("Identifiant", placeholder="jdupont")
    password = st.text_input("Mot de passe", type="password", placeholder="••••••••")

    if st.button("Se connecter →", key="btn_login"):
        if not username or not password:
            st.error("Identifiant et mot de passe requis.")
            return
        try:
            r = requests.post(
                f"{API_URL}/login",
                json={"username": username, "password": password}
            )
            if r.status_code == 200:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success("Connexion réussie.")
                st.rerun()
            else:
                try:
                    st.error(r.json()["detail"])
                except Exception:
                    st.error("Identifiants incorrects.")
        except Exception:
            st.error("Serveur inaccessible — vérifie que l'API tourne.")

    # ── Lien vers inscription ─────────────────────────────────────────────────
    st.markdown("""
    <div class="auth-switch">
        Pas encore de compte ? <strong>↓</strong>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✦  Créer un compte gratuitement", key="goto_register"):
        st.session_state["page"] = "register"
        st.rerun()


# ── Register ───────────────────────────────────────────────────────────────────
def register_page():
    render_hero("register")

    st.markdown('<div class="slabel">Nouveau compte</div>', unsafe_allow_html=True)

    username = st.text_input("Identifiant", placeholder="jdupont")
    password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
    confirm  = st.text_input("Confirmer le mot de passe", type="password", placeholder="••••••••")

    if st.button("Créer le compte →", key="btn_register"):
        if not username or not password:
            st.error("Champs obligatoires manquants.")
            return
        if password != confirm:
            st.error("Les mots de passe ne correspondent pas.")
            return
        try:
            r = requests.post(
                f"{API_URL}/register",
                json={"username": username, "password": password}
            )
            if r.status_code == 200:
                st.success("Compte créé avec succès. Connecte-toi maintenant.")
                st.session_state["page"] = "login"
                st.rerun()
            else:
                try:
                    st.error(r.json()["detail"])
                except Exception:
                    st.error("Erreur lors de la création du compte.")
        except Exception:
            st.error("Serveur inaccessible.")

    st.markdown("""
    <div class="auth-switch">
        Déjà un compte ? <strong>↓</strong>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Retour à la connexion", key="goto_login"):
        st.session_state["page"] = "login"
        st.rerun()


# ── App principale ─────────────────────────────────────────────────────────────
def mentor_page():
    with st.sidebar:
        st.markdown(f"""
        <div class="user-badge">
            <div class="user-badge-tag">◈ session active</div>
            <div class="user-badge-name">@{st.session_state['username']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⎋  Déconnexion"):
            st.session_state["authenticated"] = False
            st.session_state["username"] = ""
            st.rerun()

    render_hero("app")

    st.markdown('<div class="slabel">Configuration</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Langage", ["python", "javascript", "java", "c++"])
    with col2:
        mode = st.selectbox(
            "Mode",
            ["Clean Code", "Performance", "Sécurité", "Architecture", "Débutant pédagogique"],
        )

    st.markdown('<div class="slabel" style="margin-top:1.2rem;">Éditeur</div>', unsafe_allow_html=True)

    code = st.text_area(
        "code",
        placeholder=f"# Collez votre code {language} ici…",
        height=300,
        label_visibility="collapsed",
    )

    lines = code.count('\n') + 1 if code.strip() else 0
    chars = len(code)
    st.markdown(f"""
    <div class="stats-row">
        <span class="stat-chip">{lines} lignes</span>
        <span class="stat-chip">{chars} chars</span>
        <span class="stat-chip">{language}</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("◈  Analyser →"):
        if not code.strip():
            st.warning("Colle du code avant de lancer l'analyse.")
        else:
            with st.spinner("Analyse en cours…"):
                try:
                    r = requests.post(
                        f"{API_URL}/analyze",
                        json={"code": code, "language": language, "mode": mode},
                    )
                    if r.status_code == 200:
                        result = r.json()
                        st.markdown(
                            '<div class="slabel" style="margin-top:1.5rem;">Résultat</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<div class="result-wrap">{result["analysis"]}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.error("Erreur lors de l'analyse.")
                        try:
                            st.write(r.json()["detail"])
                        except Exception:
                            st.write(r.text)
                except Exception:
                    st.error("Serveur inaccessible.")


# ── Entry point ────────────────────────────────────────────────────────────────
inject_css()

for key, default in [("authenticated", False), ("username", ""), ("page", "login")]:
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state["authenticated"]:
    mentor_page()
else:
    if st.session_state["page"] == "register":
        register_page()
    else:
        login_page()