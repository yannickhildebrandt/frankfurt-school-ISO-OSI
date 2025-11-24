import streamlit as st

# --- Konfiguration der Seite ---
st.set_page_config(
    page_title="ISO-OSI Hausbau",
    page_icon="🏠",
    layout="wide"
)

# --- CSS Styling (Das ist der Zauber für den Haus-Look) ---
st.markdown("""
    <style>
    /* Container für das Haus zentrieren */
    .house-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
        width: 100%;
        padding-top: 20px;
    }

    /* Basis-Stil für alle Blöcke */
    .layer-block {
        text-align: center;
        padding: 15px;
        color: white;
        font-weight: bold;
        transition: all 0.5s ease;
        position: relative;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        text-shadow: 1px 1px 2px black;
    }

    /* Spezifische Stile für die Haus-Teile */
    
    /* Layer 7: Das Dach */
    .layer-7 {
        width: 50%;
        background: linear-gradient(135deg, #8e44ad, #9b59b6); /* Lila Dachziegel */
        border-radius: 50% 50% 5px 5px; /* Rundes Dach / Kuppel */
        border-bottom: 5px solid #5e3370;
        margin-bottom: 2px;
        clip-path: polygon(15% 0%, 85% 0%, 100% 100%, 0% 100%); /* Trapezform */
    }

    /* Layer 6: Obergeschoss */
    .layer-6 {
        width: 70%;
        background-color: #3498db; /* Blau */
        border-left: 5px solid #2980b9;
        border-right: 5px solid #2980b9;
        margin-bottom: 2px;
    }

    /* Layer 5: Obergeschoss */
    .layer-5 {
        width: 70%;
        background-color: #2ecc71; /* Grün */
        border-left: 5px solid #27ae60;
        border-right: 5px solid #27ae60;
        margin-bottom: 2px;
    }

    /* Layer 4: 1. Stock */
    .layer-4 {
        width: 70%;
        background-color: #f1c40f; /* Gelb */
        color: #333; /* Dunkle Schrift für Gelb */
        text-shadow: none;
        border-left: 5px solid #f39c12;
        border-right: 5px solid #f39c12;
        margin-bottom: 2px;
    }

    /* Layer 3: Erdgeschoss (Eingang) */
    .layer-3 {
        width: 70%;
        background-color: #e67e22; /* Orange */
        border-left: 5px solid #d35400;
        border-right: 5px solid #d35400;
        border-bottom: 2px solid #d35400;
        margin-bottom: 2px;
    }

    /* Layer 2: Fundamentplatte */
    .layer-2 {
        width: 85%; /* Breiter als das Haus */
        background: repeating-linear-gradient(
            45deg,
            #7f8c8d,
            #7f8c8d 10px,
            #95a5a6 10px,
            #95a5a6 20px
        ); /* Beton-Look */
        border: 2px solid #34495e;
        border-radius: 5px;
        margin-bottom: 5px;
    }

    /* Layer 1: Erde / Untergrund */
    .layer-1 {
        width: 100%; /* Volle Breite */
        background-color: #5d4037;
        background-image: url("https://www.transparenttextures.com/patterns/dark-matter.png"); /* Struktur */
        border-radius: 0 0 15px 15px;
        padding: 25px;
    }

    /* Dekorationen */
    .window { font-size: 1.5em; position: absolute; }
    .window-left { left: 20px; }
    .window-right { right: 20px; }
    .door { font-size: 2em; }

    </style>
    """, unsafe_allow_html=True)

# --- Daten ---
osi_layers = {
    1: {
        "name": "L1: Physical",
        "house_part": "Grundstück & Leitungen",
        "css_class": "layer-1",
        "icon": "⛏️",
        "desc": "Bits, Kabel, Signale",
        "detail": "Hier liegen die physischen Leitungen im Boden."
    },
    2: {
        "name": "L2: Data Link",
        "house_part": "Beton-Fundament",
        "css_class": "layer-2",
        "icon": "🏗️",
        "desc": "MAC-Adressen, Switches",
        "detail": "Die stabile Bodenplatte, die zwei Punkte verbindet."
    },
    3: {
        "name": "L3: Network",
        "house_part": "Erdgeschoss & Hausnummer",
        "css_class": "layer-3",
        "icon": "🚪", # Tür Icon für Eingang
        "desc": "IP-Adressen, Routing",
        "detail": "Der Haupteingang mit der Adresse (IP)."
    },
    4: {
        "name": "L4: Transport",
        "house_part": "1. Stock & Zimmer",
        "css_class": "layer-4",
        "icon": "🛋️",
        "desc": "TCP/UDP, Ports",
        "detail": "Verteilung in die richtigen Zimmer (Ports)."
    },
    5: {
        "name": "L5: Session",
        "house_part": "2. Stock & Flure",
        "css_class": "layer-5",
        "icon": "🪟", # Fenster
        "desc": "Session Mngt.",
        "detail": "Verwaltung der offenen Verbindungen."
    },
    6: {
        "name": "L6: Presentation",
        "house_part": "Obergeschoss & Deko",
        "css_class": "layer-6",
        "icon": "🖼️", # Bild/Deko
        "desc": "Verschlüsselung, Formate",
        "detail": "Der Übersetzer & Innenarchitekt."
    },
    7: {
        "name": "L7: Application",
        "house_part": "Dachstuhl & Bewohner",
        "css_class": "layer-7",
        "icon": "📡", # Antenne auf Dach
        "desc": "HTTP, FTP, SMTP",
        "detail": "Die Anwendung, die der User sieht."
    }
}

# --- Session State ---
if 'current_level' not in st.session_state:
    st.session_state.current_level = 0

# --- Hauptbereich ---
st.title("🏗️ Interaktiver OSI-Hausbau")

col1, col2 = st.columns([1, 2], gap="large")

# --- Linke Spalte: Steuerung ---
with col1:
    st.markdown("### 👷 Bauleiter-Menü")
    
    # Game Logic
    if st.session_state.current_level < 7:
        st.info(f"Wir bauen gerade Schicht {st.session_state.current_level + 1}.")
        
        # Liste für Dropdown generieren
        options_map = {f"{v['name']} - {v['house_part']}": k for k, v in osi_layers.items()}
        
        choice = st.selectbox(
            "Wähle das nächste Bauteil:", 
            list(options_map.keys()), 
            index=None, 
            placeholder="Baumaterial auswählen..."
        )
        
        if st.button("🛠️ Bauen!"):
            if choice:
                chosen_layer_id = options_map[choice]
                required_layer = st.session_state.current_level + 1
                
                if chosen_layer_id == required_layer:
                    st.session_state.current_level += 1
                    st.toast(f"Klasse! {osi_layers[chosen_layer_id]['house_part']} erfolgreich gebaut!", icon="✅")
                    st.rerun()
                elif chosen_layer_id <= st.session_state.current_level:
                    st.warning("Das haben wir schon gebaut! Wir brauchen das nächste Teil.")
                else:
                    st.error(f"🛑 HALT! Du kannst {choice} nicht bauen, bevor der Unterbau fertig ist! (Physik beachten!)")
            else:
                st.warning("Wähle erst ein Material aus.")
                
    else:
        st.success("🎉 Das Haus ist fertiggestellt! Alle Schichten sind korrekt.")
        st.balloons()
        if st.button("Abriss & Neubau"):
            st.session_state.current_level = 0
            st.rerun()
    
    # Legende / Erklärung des zuletzt gebauten Teils
    if st.session_state.current_level > 0:
        st.markdown("---")
        curr = osi_layers[st.session_state.current_level]
        st.markdown(f"**Zuletzt gebaut:** {curr['name']}")
        st.caption(curr['detail'])

# --- Rechte Spalte: Die Baustelle (Visualisierung) ---
with col2:
    st.markdown("### 🏡 Die Baustelle")
    
    # Container Start
    st.markdown('<div class="house-container">', unsafe_allow_html=True)
    
    # Wir loopen rückwärts (7 oben, 1 unten)
    # Wir zeigen placeholders an für Dinge, die noch nicht gebaut sind, damit man die "Lücke" sieht
    
    for i in range(7, 0, -1):
        layer = osi_layers[i]
        
        if i <= st.session_state.current_level:
            # --- GEBAUTER TEIL ---
            
            # Dekoration: Fenster hinzufügen für Schichten 4,5,6
            deco_html = ""
            if i == 3:
                 deco_html = '<div class="door">🚪</div>' # Tür im EG
            elif i in [4, 5, 6]:
                deco_html = '<span class="window window-left">🪟</span><span class="window window-right">🪟</span>'
            elif i == 7:
                deco_html = '<div style="margin-bottom:5px;">📡</div>'

            st.markdown(f"""
            <div class="layer-block {layer['css_class']}">
                {deco_html}
                <div style="font-size: 0.9em;">{layer['name']}</div>
                <div style="font-size: 1.1em;">{layer['house_part']}</div>
                <small>{layer['desc']}</small>
            </div>
            """, unsafe_allow_html=True)
            
        elif i == st.session_state.current_level + 1:
            # --- NÄCHSTER SCHRITT (Geisterbild) ---
            st.markdown(f"""
            <div style="width: 60%; border: 2px dashed #ccc; color: #ccc; padding: 20px; margin: 5px; text-align: center; border-radius: 10px;">
                🏗️ Hier muss Schicht {i} hin
            </div>
            """, unsafe_allow_html=True)
        else:
            # --- LUFT (Noch weit entfernt) ---
            # Zeigen wir einfach als leeren Raum an oder gar nicht, damit das Haus von unten wächst
            pass

    st.markdown('</div>', unsafe_allow_html=True) # Ende Container
