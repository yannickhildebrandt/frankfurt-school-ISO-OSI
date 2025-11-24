import streamlit as st

# --- Kofiguration der Seite ---
st.set_page_config(
    page_title="ISO-OSI Hausbau",
    page_icon="🏠",
    layout="wide"
)

# --- CSS für schöneres Styling ---
st.markdown("""
    <style>
    .layer-box {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: white;
        font-weight: bold;
        text-align: center;
        border: 2px solid #333;
    }
    .success-msg {
        color: green;
        font-weight: bold;
    }
    .error-msg {
        color: red;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Daten: Das OSI-Modell als Haus ---
# Wir definieren die Schichten von unten (1) nach oben (7)
osi_layers = {
    1: {
        "name": "Physical Layer (Bitübertragungsschicht)",
        "house_part": "Das Fundament & Grundstück",
        "color": "#5D4037", # Braun
        "desc_house": "Ohne Boden und Fundament steht nichts. Hier liegen die physischen Steine und Leitungen.",
        "desc_tech": "Übertragung von rohen Bits über Kabel, Glasfaser oder Funk (Volt, Frequenzen)."
    },
    2: {
        "name": "Data Link Layer (Sicherungsschicht)",
        "house_part": "Die Bodenplatte & Zufahrt",
        "color": "#795548", # Helleres Braun
        "desc_house": "Eine sichere Basis auf dem Fundament, die den direkten Zugang zum Haus ermöglicht.",
        "desc_tech": "Fehlerfreie Übertragung zwischen zwei direkt verbundenen Knoten (MAC-Adressen, Switches)."
    },
    3: {
        "name": "Network Layer (Vermittlungsschicht)",
        "house_part": "Die Hausnummer & Adresse",
        "color": "#FF9800", # Orange
        "desc_house": "Damit die Post ankommt, braucht das Haus eine Adresse, damit man es im Stadtplan findet.",
        "desc_tech": "Logische Adressierung und Routing der Pakete durch das Netzwerk (IP-Adressen, Router)."
    },
    4: {
        "name": "Transport Layer (Transportschicht)",
        "house_part": "Wände & Zimmeraufteilung",
        "color": "#FFC107", # Gelb
        "desc_house": "Die Struktur des Hauses. Sie sorgt dafür, dass Dinge (Möbel/Daten) sicher in die richtigen Räume kommen.",
        "desc_tech": "Segmentierung des Datenstroms, Fehlerkontrolle und Zuordnung zu Anwendungen (TCP/UDP, Ports)."
    },
    5: {
        "name": "Session Layer (Sitzungsschicht)",
        "house_part": "Türen & Schlösser",
        "color": "#4CAF50", # Grün
        "desc_house": "Regelt, wer wann reinkommen darf und hält die Verbindung (Tür) offen oder schließt sie.",
        "desc_tech": "Steuerung der Verbindungen (Sessions) zwischen Computern (Aufbau, Verwaltung, Abbau)."
    },
    6: {
        "name": "Presentation Layer (Darstellungsschicht)",
        "house_part": "Inneneinrichtung & Dolmetscher",
        "color": "#2196F3", # Blau
        "desc_house": "Sorgt dafür, dass der Besuch sich wohlfühlt (Sprache, Formatierung, Entschlüsselung).",
        "desc_tech": "Übersetzung der Daten in ein verständliches Format, Verschlüsselung, Kompression (JPEG, ASCII, SSL)."
    },
    7: {
        "name": "Application Layer (Anwendungsschicht)",
        "house_part": "Die Bewohner & Interaktion",
        "color": "#9C27B0", # Lila
        "desc_house": "Die Menschen, die im Haus leben, Briefe schreiben und das Telefon benutzen.",
        "desc_tech": "Schnittstelle zum Benutzer, Netzwerkdienste für Anwendungen (HTTP, SMTP, FTP)."
    }
}

# --- Session State Initialisierung ---
if 'current_level' not in st.session_state:
    st.session_state.current_level = 0 # 0 bedeutet, noch nichts gebaut
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Header ---
st.title("🏠 Baue dein ISO-OSI Haus")
st.markdown("""
Willkommen auf der Baustelle! 
Deine Aufgabe ist es, das Haus **Schicht für Schicht von unten nach oben** aufzubauen. 
Jedes Bauteil entspricht einer Schicht des ISO-OSI-Modells.
""")

# --- Layout ---
col_control, col_display = st.columns([1, 2])

# --- Logik & Controls (Linke Spalte) ---
with col_control:
    st.subheader("Werkzeugkasten")
    
    # Fortschrittsanzeige
    progress = st.session_state.current_level / 7
    st.progress(progress, text=f"Baufortschritt: {st.session_state.current_level}/7 Schichten")

    if st.session_state.current_level < 7:
        st.info("Wähle das nächste logische Bauteil aus, um das Haus weiterzubauen.")
        
        # Wir erstellen eine Liste aller Schichten für das Dropdown
        # Um es schwieriger zu machen, zeigen wir alle Namen an, nicht nur den nächsten
        options = {k: f"{v['name']} ({v['house_part']})" for k, v in osi_layers.items()}
        
        # User Auswahl
        selected_option_label = st.selectbox(
            "Welches Bauteil kommt als nächstes?",
            options=list(options.values()),
            index=None,
            placeholder="Bitte wählen..."
        )

        # Button zum Bauen
        if st.button("Bauteil hinzufügen"):
            if selected_option_label:
                # Finde die ID basierend auf dem Label
                selected_id = [k for k, v in options.items() if v == selected_option_label][0]
                
                # Prüfung: Ist es die korrekte nächste Schicht?
                next_required = st.session_state.current_level + 1
                
                if selected_id == next_required:
                    st.session_state.current_level += 1
                    st.balloons() # Kleiner Effekt bei Erfolg
                    st.rerun()
                elif selected_id <= st.session_state.current_level:
                    st.error("Dieses Bauteil hast du bereits verbaut!")
                else:
                    st.error(f"Das funktioniert nicht! Du kannst Schicht {selected_id} nicht bauen, bevor Schicht {next_required} fertig ist. Das Haus würde einstürzen!")
            else:
                st.warning("Bitte wähle zuerst ein Bauteil aus.")
    else:
        st.success("Glückwunsch! Dein Haus (und dein Netzwerk-Stack) ist fertig!")
        if st.button("Neustart"):
            st.session_state.current_level = 0
            st.rerun()

# --- Visualisierung (Rechte Spalte) ---
with col_display:
    st.subheader("Die Baustelle")
    
    # Wir zeigen das Haus von oben nach unten an (Layer 7 oben, Layer 1 unten)
    # Aber wir zeigen nur das an, was schon gebaut wurde (current_level)
    
    if st.session_state.current_level == 0:
        st.image("https://img.icons8.com/ios/100/000000/construction-worker.png", width=100)
        st.markdown("*Hier ist noch nichts. Fang an zu bauen!*")
    
    # Loop rückwärts von 7 bis 1, aber zeige nur an wenn i <= current_level
    for i in range(7, 0, -1):
        if i <= st.session_state.current_level:
            layer = osi_layers[i]
            
            # Container für jede Schicht
            with st.container():
                # HTML/CSS Block für die visuelle Darstellung
                st.markdown(f"""
                <div class="layer-box" style="background-color: {layer['color']};">
                    <h3>Schicht {i}: {layer['name']}</h3>
                    <h4>🏗️ {layer['house_part']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Erklärung als Expander (damit es nicht zu voll wird, aber info da ist)
                with st.expander(f"ℹ️ Erklärung: {layer['house_part']}"):
                    st.markdown(f"**🏠 Haus-Analogie:** {layer['desc_house']}")
                    st.markdown(f"**💻 Technik:** {layer['desc_tech']}")
        
        elif i == st.session_state.current_level + 1:
            # Platzhalter für die nächste Schicht (Ghost view)
            st.markdown(f"""
            <div style="border: 2px dashed #ccc; padding: 20px; margin-bottom: 10px; text-align: center; color: #ccc; border-radius: 10px;">
                ❓ Hier entsteht bald Schicht {i}
            </div>
            """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.caption("Interaktive Lern-App für das ISO-OSI Modell | Erstellt mit Streamlit")
