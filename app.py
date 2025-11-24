import streamlit as st

# --- Konfiguration der Seite ---
st.set_page_config(
    page_title="ISO-OSI Nachbarschaft",
    page_icon="🏘️",
    layout="wide"
)

# --- CSS Styling ---
st.markdown("""
    <style>
    /* Hauptcontainer für die "Straße" */
    .neighborhood {
        display: flex;
        flex-direction: column;
        width: 100%;
        padding-top: 10px;
    }

    /* Eine Zeile im OSI-Modell (Linkes Haus - Mitte - Rechtes Haus) */
    .layer-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 4px;
        width: 100%;
    }

    /* Basis-Stil für Haus-Blöcke */
    .house-block {
        text-align: center;
        padding: 10px;
        color: white;
        font-weight: bold;
        position: relative;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: transform 0.3s;
        border: 1px solid rgba(0,0,0,0.1);
    }
    
    .house-block:hover {
        transform: scale(1.02);
        z-index: 10;
    }

    /* Die Verbindung in der Mitte */
    .connection-line {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 10px;
        color: #666;
        font-size: 0.8em;
        border-bottom: 1px dashed #ccc;
        height: 40px; /* Fixe Höhe zur Ausrichtung */
    }

    /* Spezifische Formen für die Schichten */
    
    /* L7: Dach */
    .shape-roof {
        width: 140px; 
        height: 60px;
        background: linear-gradient(135deg, #8e44ad, #9b59b6);
        border-radius: 50% 50% 5px 5px;
        clip-path: polygon(15% 0%, 85% 0%, 100% 100%, 0% 100%);
    }

    /* L3-L6: Wohnbereich */
    .shape-floor {
        width: 180px;
        height: 50px;
    }

    /* L2: Fundament */
    .shape-foundation {
        width: 200px;
        height: 40px;
        background: repeating-linear-gradient(45deg, #7f8c8d, #7f8c8d 5px, #95a5a6 5px, #95a5a6 10px);
    }

    /* L1: Erde / Kabel */
    .shape-ground {
        width: 220px;
        height: 60px;
        background-color: #5d4037;
        background-image: url("https://www.transparenttextures.com/patterns/dark-matter.png");
        border-radius: 0 0 15px 15px;
    }
    
    /* Farben der Stockwerke */
    .bg-blue { background-color: #3498db; border-left: 4px solid #2980b9; }
    .bg-green { background-color: #2ecc71; border-left: 4px solid #27ae60; }
    .bg-yellow { background-color: #f1c40f; color: #333; border-left: 4px solid #f39c12; }
    .bg-orange { background-color: #e67e22; border-left: 4px solid #d35400; }

    /* Dekorationen */
    .window { font-size: 1.2em; position: absolute; top: 10px;}
    .win-l { left: 10px; }
    .win-r { right: 10px; }
    
    /* PDU Badge in der Mitte */
    .pdu-badge {
        background-color: #eee;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
        border: 1px solid #ccc;
    }

    </style>
    """, unsafe_allow_html=True)

# --- Daten ---
osi_layers = {
    7: {"name": "Application", "pdu": "Daten", "shape": "shape-roof", "desc": "HTTP, Mail", "deco": "📡"},
    6: {"name": "Presentation", "pdu": "Daten", "shape": "shape-floor bg-blue", "desc": "Verschlüsselung", "deco": "🖼️"},
    5: {"name": "Session", "pdu": "Daten", "shape": "shape-floor bg-green", "desc": "Sitzung", "deco": "🪟"},
    4: {"name": "Transport", "pdu": "Segmente", "shape": "shape-floor bg-yellow", "desc": "TCP/UDP Ports", "deco": "🛋️"},
    3: {"name": "Network", "pdu": "Pakete", "shape": "shape-floor bg-orange", "desc": "IP-Adresse", "deco": "🚪"},
    2: {"name": "Data Link", "pdu": "Frames", "shape": "shape-foundation", "desc": "MAC / Switch", "deco": "🏗️"},
    1: {"name": "Physical", "pdu": "Bits", "shape": "shape-ground", "desc": "Kabel / Funk", "deco": "🔌"}
}

# --- State ---
if 'level' not in st.session_state:
    st.session_state.level = 0

# --- Header ---
st.title("🏘️ ISO-OSI Nachbarschaft")
st.markdown("""
Hier bauen wir **Sender (Haus A)** und **Empfänger (Haus B)** gleichzeitig auf. 
Damit Kommunikation funktioniert, müssen beide Seiten die gleichen Protokolle auf der gleichen Schicht sprechen.
""")

# --- Layout ---
col_ctrl, col_vis = st.columns([1, 3])

# --- Steuerung (Links) ---
with col_ctrl:
    st.subheader("Bauleitung")
    
    current = st.session_state.level
    
    if current < 7:
        next_layer = current + 1
        layer_info = osi_layers[next_layer]
        
        st.info(f"Nächster Schritt: **Schicht {next_layer}**")
        st.markdown(f"*{layer_info['desc']}*")
        
        # Aufgabe: Wähle das Richtige
        options = {v['name']: k for k, v in osi_layers.items()}
        # Mische Optionen für Quiz-Effekt wäre hier möglich, wir halten es simpel:
        
        selected = st.selectbox("Welches Bauteil kommt jetzt?", ["Wählen..."] + [v['name'] for k,v in osi_layers.items()])
        
        if st.button("🔨 Bauteil setzen"):
            if selected == layer_info['name']:
                st.session_state.level += 1
                st.success("Korrekt! Beide Häuser wachsen.")
                st.rerun()
            elif selected != "Wählen...":
                st.error("Falsches Bauteil! Das passt statisch nicht.")
    else:
        st.success("🎉 Verbindung hergestellt!")
        if st.button("Neustart"):
            st.session_state.level = 0
            st.rerun()

    # Legende
    st.markdown("---")
    st.markdown("**PDU:** Protocol Data Unit (Wie heißen die Daten auf dieser Ebene?)")

# --- Visualisierung (Rechts) ---
with col_vis:
    
    # Kopfzeile Häuser
    c1, c2, c3 = st.columns([1, 1, 1])
    c1.markdown("### 🏠 Haus A (Sender)")
    c3.markdown("### 🏠 Haus B (Empfänger)")
    
    st.markdown('<div class="neighborhood">', unsafe_allow_html=True)

    # Loop von oben (7) nach unten (1)
    for i in range(7, 0, -1):
        layer = osi_layers[i]
        
        # Wenn gebaut:
        if i <= st.session_state.level:
            
            # Visualisierung der "Logischen Verbindung" in der Mitte
            conn_content = ""
            if i == 1:
                # Layer 1 ist physisch verbunden
                conn_style = "border-bottom: 5px solid #333; border-style: solid;"
                conn_text = "Physische Leitung"
                icon_mid = "🔌"
            else:
                # Layer 2-7 sind logisch verbunden
                conn_style = "border-style: dashed;"
                conn_text = f"Austausch: {layer['pdu']}"
                icon_mid = "↔️"

            # HTML Aufbau für eine Zeile
            st.markdown(f"""
            <div class="layer-row">
                <!-- HAUS A -->
                <div class="house-block {layer['shape']}">
                    <div class="window win-l">{layer['deco']}</div>
                    <div>L{i}: {layer['name']}</div>
                </div>

                <!-- VERBINDUNG -->
                <div class="connection-line" style="{conn_style}">
                    <span style="background:#fff; padding:0 5px;">{icon_mid}</span>
                    <span class="pdu-badge">{conn_text}</span>
                </div>

                <!-- HAUS B -->
                <div class="house-block {layer['shape']}">
                    <div class="window win-r">{layer['deco']}</div>
                    <div>L{i}: {layer['name']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        elif i == st.session_state.level + 1:
            # Geister-Ebene (Next Step)
            st.markdown(f"""
            <div class="layer-row" style="opacity: 0.3;">
                <div class="house-block" style="width: 150px; border: 2px dashed #ccc; color: black;">🏗️ ???</div>
                <div class="connection-line" style="border: none;">⏳</div>
                <div class="house-block" style="width: 150px; border: 2px dashed #ccc; color: black;">🏗️ ???</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
