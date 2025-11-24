import streamlit as st

# --- Konfiguration muss immer als erstes stehen ---
st.set_page_config(
    page_title="ISO-OSI Nachbarschaft",
    page_icon="🏘️",
    layout="wide"
)

# --- CSS Styling ---
st.markdown("""
    <style>
    /* Container für die Ausrichtung in den Spalten */
    .element-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }

    /* Der grafische Haus-Block */
    .house-block {
        text-align: center;
        padding: 8px;
        color: white;
        font-weight: bold;
        position: relative;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: transform 0.3s;
        border: 1px solid rgba(0,0,0,0.1);
        margin-bottom: 5px;
    }
    
    .house-block:hover {
        transform: scale(1.05);
        z-index: 10;
    }

    /* Verbindungslinie in der Mitte */
    .connection-line {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        color: #888;
        font-size: 0.8em;
        margin-bottom: 5px;
    }

    /* --- Formen & Farben --- */
    
    /* Dach (Layer 7) */
    .shape-roof {
        width: 140px; 
        height: 60px;
        background: linear-gradient(135deg, #8e44ad, #9b59b6);
        border-radius: 50% 50% 5px 5px;
        clip-path: polygon(15% 0%, 85% 0%, 100% 100%, 0% 100%);
    }

    /* Stockwerke (Layer 3-6) */
    .shape-floor {
        width: 180px;
        height: 50px;
    }

    /* Fundament (Layer 2) */
    .shape-foundation {
        width: 200px;
        height: 40px;
        background: repeating-linear-gradient(45deg, #7f8c8d, #7f8c8d 5px, #95a5a6 5px, #95a5a6 10px);
    }

    /* Boden (Layer 1) */
    .shape-ground {
        width: 220px;
        height: 60px;
        background-color: #5d4037;
        background-image: url("https://www.transparenttextures.com/patterns/dark-matter.png");
        border-radius: 0 0 15px 15px;
    }
    
    /* Farb-Klassen */
    .bg-blue { background-color: #3498db; border-left: 4px solid #2980b9; }
    .bg-green { background-color: #2ecc71; border-left: 4px solid #27ae60; }
    .bg-yellow { background-color: #f1c40f; color: #333; border-left: 4px solid #f39c12; }
    .bg-orange { background-color: #e67e22; border-left: 4px solid #d35400; }

    /* Dekorationen */
    .window { font-size: 1.2em; position: absolute; top: 10px;}
    .win-l { left: 10px; }
    .win-r { right: 10px; }
    
    /* PDU Badge */
    .pdu-badge {
        background-color: #262730;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
        border: 1px solid #444;
        white-space: nowrap;
        margin-top: -12px; /* Positionierung auf der Linie */
        z-index: 2;
    }
    
    /* Platzhalter für ungebautes */
    .placeholder-box {
        border: 2px dashed #444;
        color: #666;
        padding: 10px;
        border-radius: 8px;
        background-color: rgba(255,255,255,0.05);
        font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Umfangreiche Daten (Wiederhergestellt!) ---
osi_layers = {
    7: {
        "name": "Application", 
        "pdu": "Daten", 
        "shape": "shape-roof", 
        "deco": "📡",
        "desc_house": "Die Bewohner schreiben Briefe oder telefonieren. Hier findet die eigentliche Interaktion statt.",
        "desc_tech": "Schnittstelle zum User (HTTP, SMTP, FTP). Anwendungen greifen auf Netzwerkdienste zu."
    },
    6: {
        "name": "Presentation", 
        "pdu": "Daten", 
        "shape": "shape-floor bg-blue", 
        "deco": "🖼️",
        "desc_house": "Der Dolmetscher. Er übersetzt die Sprache der Bewohner in ein Standardformat und verschlüsselt Briefe.",
        "desc_tech": "Datenformatierung, Verschlüsselung (SSL/TLS), Kompression (JPEG, MPEG)."
    },
    5: {
        "name": "Session", 
        "pdu": "Daten", 
        "shape": "shape-floor bg-green", 
        "deco": "🪟",
        "desc_house": "Verwaltet Gespräche. Wer darf wann reden? Wiederaufnahme, wenn jemand unterbrochen wird.",
        "desc_tech": "Steuerung der logischen Verbindungen (Sessions). Aufbau, Abbau und Synchronisation."
    },
    4: {
        "name": "Transport", 
        "pdu": "Segmente", 
        "shape": "shape-floor bg-yellow", 
        "deco": "🛋️",
        "desc_house": "Die Zimmeraufteilung. Sorgt dafür, dass Möbel (Daten) im richtigen Raum (Anwendung) landen.",
        "desc_tech": "End-to-End Verbindung. Fehlerkontrolle (TCP) oder Schnelligkeit (UDP). Adressierung über Ports."
    },
    3: {
        "name": "Network", 
        "pdu": "Pakete", 
        "shape": "shape-floor bg-orange", 
        "deco": "🚪",
        "desc_house": "Die Adresse & der Postbote. Findet den besten Weg durch die Stadt zum Zielhaus.",
        "desc_tech": "Logische Adressierung (IP-Adressen) und Routing durch das Netzwerk (Router)."
    },
    2: {
        "name": "Data Link", 
        "pdu": "Frames", 
        "shape": "shape-foundation", 
        "deco": "🏗️",
        "desc_house": "Die Auffahrt & der Zugang. Regelt den direkten Zugang zum Nachbarn oder zur Straße.",
        "desc_tech": "Physikalische Adressierung (MAC-Adressen), Fehlererkennung, Zugriffskontrolle (Switches)."
    },
    1: {
        "name": "Physical", 
        "pdu": "Bits", 
        "shape": "shape-ground", 
        "deco": "🔌",
        "desc_house": "Der Boden & die Leitungen. Das physische Medium, auf dem alles steht.",
        "desc_tech": "Übertragung von rohen Bits über Kupfer, Glasfaser oder Funk (Spannung, Frequenzen)."
    }
}

# --- Session State ---
if 'level' not in st.session_state:
    st.session_state.level = 0

# --- Seiten-Titel ---
st.title("🏘️ ISO-OSI Nachbarschaft")
st.markdown("""
**Lernziel:** Baue die Kommunikation zwischen zwei Häusern (Sender & Empfänger) auf.
Klicke in der Mitte auf **"📖 Infos"**, um zu verstehen, was die jeweilige Schicht tut.
""")

# --- Layout ---
col_ctrl, col_space, col_vis = st.columns([1, 0.1, 3])

# --- Linke Spalte: Steuerung ---
with col_ctrl:
    st.subheader("🚧 Bauleitung")
    
    current = st.session_state.level
    
    if current < 7:
        next_layer = current + 1
        layer_data = osi_layers[next_layer]
        
        # Info Box zum nächsten Schritt
        st.info(f"**Auftrag:** Wir brauchen Schicht {next_layer}!")
        st.markdown(f"Tipp: {layer_data['desc_house']}")
        
        # Dropdown Auswahl
        options_list = ["Bitte wählen..."] + [v['name'] for k,v in osi_layers.items()]
        selected = st.selectbox("Welches Bauteil passt?", options_list)
        
        if st.button("🔨 Bauen", use_container_width=True):
            if selected == layer_data['name']:
                st.session_state.level += 1
                st.balloons()
                st.rerun()
            elif selected != "Bitte wählen...":
                st.error("Das ist das falsche Bauteil! Schau dir die Funktion nochmal an.")
    else:
        st.success("🎉 Kommunikation läuft!")
        st.markdown("Das Netzwerk ist vollständig und Daten können fließen.")
        if st.button("♻️ Alles abreißen & neu lernen"):
            st.session_state.level = 0
            st.rerun()

    # Legende links unten
    st.markdown("---")
    st.caption("PDU = Protocol Data Unit (Wie heißen die Datenpakete hier?)")

# --- Rechte Spalte: Visualisierung ---
with col_vis:
    
    # Header für die Häuser
    h1, h2, h3 = st.columns([1, 1, 1])
    h1.markdown("<div style='text-align:center'><h3>🏠 Sender</h3></div>", unsafe_allow_html=True)
    h2.markdown("<div style='text-align:center; color:#888'><small>logische Verbindung</small></div>", unsafe_allow_html=True)
    h3.markdown("<div style='text-align:center'><h3>🏠 Empfänger</h3></div>", unsafe_allow_html=True)
    
    # Wir iterieren von oben (7) nach unten (1)
    for i in range(7, 0, -1):
        layer = osi_layers[i]
        
        # Spalten-Layout für diese Zeile
        cols = st.columns([1, 1.2, 1], gap="small") 
        # Mittlere Spalte (1.2) etwas breiter für den Text
        
        # --- ZUSTAND: GEBAUT ---
        if i <= st.session_state.level:
            
            # Haus A (Links)
            with cols[0]:
                st.markdown(f"""
                <div class="element-container">
                    <div class="house-block {layer['shape']}">
                        <div class="window win-l">{layer['deco']}</div>
                        <div>L{i}: {layer['name']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Mitte (Verbindung + Infos)
            with cols[1]:
                # CSS für Linie (Durchgezogen bei Layer 1, gestrichelt sonst)
                border_style = "solid" if i == 1 else "dashed"
                border_width = "4px" if i == 1 else "2px"
                line_color = "#555"
                
                # Die Linie und das Badge
                st.markdown(f"""
                <div class="connection-line" style="border-bottom: {border_width} {border_style} {line_color}; height: 25px;">
                    <span class="pdu-badge">{layer['pdu']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Der WICHTIGE Teil: Die Infos zurückbringen
                with st.expander(f"📖 L{i} Infos", expanded=False):
                    st.markdown(f"**🏠 Haus:** {layer['desc_house']}")
                    st.divider()
                    st.markdown(f"**💻 Tech:** {layer['desc_tech']}")

            # Haus B (Rechts)
            with cols[2]:
                st.markdown(f"""
                <div class="element-container">
                    <div class="house-block {layer['shape']}">
                        <div class="window win-r">{layer['deco']}</div>
                        <div>L{i}: {layer['name']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # --- ZUSTAND: NÄCHSTER SCHRITT ---
        elif i == st.session_state.level + 1:
            with cols[0]:
                st.markdown('<div class="element-container"><div class="placeholder-box">🏗️ ???</div></div>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown('<div style="text-align:center; padding-top:10px;">⏳ <i>Wird gebaut...</i></div>', unsafe_allow_html=True)
            with cols[2]:
                st.markdown('<div class="element-container"><div class="placeholder-box">🏗️ ???</div></div>', unsafe_allow_html=True)
        
        # --- ZUSTAND: NOCH NICHT DRAN ---
        else:
            # Leere Platzhalter, um Layout stabil zu halten
            with cols[0]: st.empty()
            with cols[1]: st.empty()
            with cols[2]: st.empty()
