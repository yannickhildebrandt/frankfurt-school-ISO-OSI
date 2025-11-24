import streamlit as st

# --- Konfiguration der Seite ---
st.set_page_config(
    page_title="ISO-OSI Nachbarschaft",
    page_icon="🏘️",
    layout="wide"
)

# --- CSS Styling ---
# Wir zentrieren die Inhalte in den Spalten
st.markdown("""
    <style>
    /* Genereller Container für Haus-Elemente */
    .element-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }

    /* Basis-Stil für Haus-Blöcke */
    .house-block {
        text-align: center;
        padding: 8px;
        color: white;
        font-weight: bold;
        position: relative;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: transform 0.3s;
        border: 1px solid rgba(0,0,0,0.1);
        margin-bottom: 5px; /* Abstand zwischen den Schichten */
    }
    
    .house-block:hover {
        transform: scale(1.05);
        z-index: 10;
    }

    /* Die Verbindung in der Mitte */
    .connection-line {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 50px; /* Muss zur Höhe der Blöcke passen */
        color: #666;
        font-size: 0.8em;
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
        white-space: nowrap;
    }
    
    /* Platzhalter Box */
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

# --- Layout Aufteilung ---
col_ctrl, col_space, col_vis = st.columns([1, 0.2, 3])

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
        # Um das Quiz nicht zu nervig zu machen, ist die richtige Antwort vorausgewählt,
        # kann aber für Hard-Mode geändert werden auf index=None
        options_list = ["Wählen..."] + [v['name'] for k,v in osi_layers.items()]
        
        selected = st.selectbox("Welches Bauteil kommt jetzt?", options_list)
        
        if st.button("🔨 Bauteil setzen", use_container_width=True):
            if selected == layer_info['name']:
                st.session_state.level += 1
                st.success("Korrekt!")
                st.rerun()
            elif selected != "Wählen...":
                st.error("Falsches Bauteil! Das passt statisch nicht.")
    else:
        st.success("🎉 Verbindung hergestellt!")
        if st.button("Neustart", type="primary"):
            st.session_state.level = 0
            st.rerun()

    # Legende
    st.divider()
    st.caption("**PDU:** Protocol Data Unit (Wie heißen die Daten auf dieser Ebene?)")

# --- Visualisierung (Rechts) ---
with col_vis:
    
    # Header Zeile für die Häuser
    h_col1, h_col2, h_col3 = st.columns([1, 1, 1])
    h_col1.markdown("<h3 style='text-align:center;'>🏠 Haus A</h3>", unsafe_allow_html=True)
    h_col2.markdown("<h5 style='text-align:center; color:#888;'>Verbindung</h5>", unsafe_allow_html=True)
    h_col3.markdown("<h3 style='text-align:center;'>🏠 Haus B</h3>", unsafe_allow_html=True)
    
    # Loop von oben (7) nach unten (1)
    for i in range(7, 0, -1):
        layer = osi_layers[i]
        
        # Wir erstellen für JEDE Schicht eine neue Zeile mit 3 Spalten
        # Das verhindert Layout-Verschiebungen und Markdown-Code-Fehler
        row_cols = st.columns([1, 1, 1])
        
        # --- Wenn Schicht bereits gebaut ist ---
        if i <= st.session_state.level:
            
            # 1. Spalte: Haus A
            with row_cols[0]:
                st.markdown(f"""
                <div class="element-container">
                    <div class="house-block {layer['shape']}">
                        <div class="window win-l">{layer['deco']}</div>
                        <div>L{i}: {layer['name']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # 2. Spalte: Verbindung
            with row_cols[1]:
                conn_style = "border-bottom: 4px solid #333; border-style: solid;" if i == 1 else "border-bottom: 2px dashed #ccc;"
                icon_mid = "🔌" if i == 1 else "↔️"
                
                st.markdown(f"""
                <div class="connection-line" style="{conn_style}">
                    <span style="background:#0e1117; padding:0 5px; font-size:1.2em;">{icon_mid}</span>
                    <span class="pdu-badge">{layer['pdu']}</span>
                </div>
                """, unsafe_allow_html=True)

            # 3. Spalte: Haus B
            with row_cols[2]:
                st.markdown(f"""
                <div class="element-container">
                    <div class="house-block {layer['shape']}">
                        <div class="window win-r">{layer['deco']}</div>
                        <div>L{i}: {layer['name']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
        # --- Wenn dies die nächste zu bauende Schicht ist (Ghost View) ---
        elif i == st.session_state.level + 1:
            with row_cols[0]:
                st.markdown('<div class="element-container"><div class="placeholder-box">🏗️ ???</div></div>', unsafe_allow_html=True)
            with row_cols[1]:
                st.markdown('<div style="text-align:center; color:#444;">⏳</div>', unsafe_allow_html=True)
            with row_cols[2]:
                 st.markdown('<div class="element-container"><div class="placeholder-box">🏗️ ???</div></div>', unsafe_allow_html=True)
        
        # --- Leere Zeilen für die Zukunft (damit das Layout stabil bleibt) ---
        else:
             # Optionale leere Platzhalter, damit die Höhe konstant bleibt
             with row_cols[0]:
                 st.markdown('<div style="height:60px;"></div>', unsafe_allow_html=True)
