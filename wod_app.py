import streamlit as st
import re
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# --- DATABASE ESERCIZI GYMNASTICS ---
gymnastics_db = {
    "air squat": {"pattern_motorio": "squat", "attrezzo": "corpo libero", "focus_muscolare": ["gambe"], "difficoltà": "Base"},
    "push-up": {"pattern_motorio": "spinta orizzontale", "attrezzo": "corpo libero", "focus_muscolare": ["petto", "tricipiti", "core"], "difficoltà": "Base"},
    "push ups": {"pattern_motorio": "spinta orizzontale", "attrezzo": "corpo libero", "focus_muscolare": ["petto", "tricipiti", "core"], "difficoltà": "Base"},
    "pull-up": {"pattern_motorio": "trazione verticale", "attrezzo": "barra", "focus_muscolare": ["dorsali", "bicipiti", "core"], "difficoltà": "Intermedio"},
    "pull ups": {"pattern_motorio": "trazione verticale", "attrezzo": "barra", "focus_muscolare": ["dorsali", "bicipiti", "core"], "difficoltà": "Intermedio"},
    "ring row": {"pattern_motorio": "trazione orizzontale", "attrezzo": "anelli", "focus_muscolare": ["schiena", "bicipiti"], "difficoltà": "Base"},
    "dips": {"pattern_motorio": "spinta verticale", "attrezzo": "parallele", "focus_muscolare": ["tricipiti", "petto"], "difficoltà": "Intermedio"},
    "ring dip": {"pattern_motorio": "spinta verticale", "attrezzo": "anelli", "focus_muscolare": ["tricipiti", "petto"], "difficoltà": "Intermedio"},
    "handstand push-up": {"pattern_motorio": "spinta verticale", "attrezzo": "parete", "focus_muscolare": ["spalle", "tricipiti", "core"], "difficoltà": "Avanzato"},
    "hspu": {"pattern_motorio": "spinta verticale", "attrezzo": "parete", "focus_muscolare": ["spalle", "tricipiti", "core"], "difficoltà": "Avanzato"},
    "toes to bar": {"pattern_motorio": "flessione del tronco", "attrezzo": "barra", "focus_muscolare": ["addome", "flessori", "grip"], "difficoltà": "Avanzato"},
    "t2b": {"pattern_motorio": "flessione del tronco", "attrezzo": "barra", "focus_muscolare": ["addome", "flessori", "grip"], "difficoltà": "Avanzato"},
    "knees to elbows": {"pattern_motorio": "flessione del tronco", "attrezzo": "barra", "focus_muscolare": ["addome"], "difficoltà": "Intermedio"},
    "k2e": {"pattern_motorio": "flessione del tronco", "attrezzo": "barra", "focus_muscolare": ["addome"], "difficoltà": "Intermedio"},
    "sit-up": {"pattern_motorio": "flessione del tronco", "attrezzo": "corpo libero", "focus_muscolare": ["addome"], "difficoltà": "Base"},
    "sit ups": {"pattern_motorio": "flessione del tronco", "attrezzo": "corpo libero", "focus_muscolare": ["addome"], "difficoltà": "Base"},
    "burpee": {"pattern_motorio": "spinta orizzontale + salto", "attrezzo": "corpo libero", "focus_muscolare": ["total body"], "difficoltà": "Base"},
    "handstand walk": {"pattern_motorio": "locomozione in verticale", "attrezzo": "corpo libero", "focus_muscolare": ["spalle", "core", "equilibrio"], "difficoltà": "Avanzato"},
    "box jump": {"pattern_motorio": "spinta orizzontale + salto", "attrezzo": "plyo box", "focus_muscolare": ["glutei", "quadricipiti", "polpacci"], "difficoltà": "Base"},
    "box step-up": {"pattern_motorio": "spinta unilaterale", "attrezzo": "plyo box", "focus_muscolare": ["gambe", "glutei"], "difficoltà": "Base"},
    "pistol squat": {"pattern_motorio": "squat unilaterale", "attrezzo": "corpo libero", "focus_muscolare": ["quadricipiti", "core", "equilibrio"], "difficoltà": "Avanzato"},
    "walking lunge": {"pattern_motorio": "affondo dinamico", "attrezzo": "corpo libero", "focus_muscolare": ["gambe", "glutei"], "difficoltà": "Base"},
    "wall walk": {"pattern_motorio": "spinta verticale", "attrezzo": "parete", "focus_muscolare": ["spalle", "core"], "difficoltà": "Avanzato"},
    "muscle-up": {"pattern_motorio": "trazione + transizione + spinta", "attrezzo": "barra/anelli", "focus_muscolare": ["dorsali", "tricipiti", "core"], "difficoltà": "Avanzato"},
    "bar muscle-up": {"pattern_motorio": "trazione + transizione + spinta", "attrezzo": "barra", "focus_muscolare": ["dorsali", "tricipiti", "core"], "difficoltà": "Avanzato"},
    "ring muscle-up": {"pattern_motorio": "trazione + transizione + spinta", "attrezzo": "anelli", "focus_muscolare": ["dorsali", "tricipiti", "core"], "difficoltà": "Avanzato"}
}
# --- DATABASE ESERCIZI WEIGHTLIFTING ---
weightlifting_db = {
    "deadlift": {"pattern_motorio": "hip hinge", "attrezzo": "bilanciere", "focus_muscolare": ["posterior chain"], "difficoltà": "Base"},
    "sumo deadlift high pull": {"pattern_motorio": "hip hinge", "attrezzo": "bilanciere", "focus_muscolare": ["posterior chain", "spalle"], "difficoltà": "Intermedio"},
    "power clean": {"pattern_motorio": "hip hinge", "attrezzo": "bilanciere", "focus_muscolare": ["posterior chain", "trapezi"], "difficoltà": "Intermedio"},
    "thruster": {"pattern_motorio": "squat + spinta verticale", "attrezzo": "bilanciere", "focus_muscolare": ["gambe", "spalle", "core"], "difficoltà": "Intermedio"},
    "snatch": {"pattern_motorio": "hip hinge + spinta", "attrezzo": "bilanciere", "focus_muscolare": ["total body"], "difficoltà": "Avanzato"},
    "kettlebell swing": {"pattern_motorio": "hip hinge", "attrezzo": "kettlebell", "focus_muscolare": ["glutei", "lombari"], "difficoltà": "Base"},
    "goblet squat": {"pattern_motorio": "squat", "attrezzo": "kettlebell", "focus_muscolare": ["gambe", "core"], "difficoltà": "Base"},
    "dumbbell thruster": {"pattern_motorio": "squat + spinta verticale", "attrezzo": "manubri", "focus_muscolare": ["gambe", "spalle"], "difficoltà": "Base"},
    "clean and jerk": {"pattern_motorio": "hip hinge + spinta", "attrezzo": "bilanciere", "focus_muscolare": ["total body"], "difficoltà": "Avanzato"}
}

# --- DATABASE ESERCIZI MONOSTRUCTURAL ---
monostructural_db = {
    "run": {"pattern_motorio": "locomozione", "attrezzo": "pista/strada", "focus_muscolare": ["gambe", "cardio"], "difficoltà": "Base"},
    "row": {"pattern_motorio": "locomozione", "attrezzo": "remoergometro", "focus_muscolare": ["gambe", "schiena", "core"], "difficoltà": "Base"},
    "bike erg": {"pattern_motorio": "locomozione", "attrezzo": "bike erg", "focus_muscolare": ["gambe", "cardio"], "difficoltà": "Base"},
    "air bike": {"pattern_motorio": "locomozione", "attrezzo": "air bike", "focus_muscolare": ["gambe", "spalle", "cardio"], "difficoltà": "Base"},
    "ski erg": {"pattern_motorio": "locomozione", "attrezzo": "ski erg", "focus_muscolare": ["spalle", "core"], "difficoltà": "Base"},
    "jump rope": {"pattern_motorio": "locomozione", "attrezzo": "corda", "focus_muscolare": ["polpacci", "spalle", "cardio"], "difficoltà": "Base"},
    "double unders": {"pattern_motorio": "locomozione", "attrezzo": "corda", "focus_muscolare": ["polpacci", "spalle", "core"], "difficoltà": "Intermedio"},
    "shuttle run": {"pattern_motorio": "locomozione", "attrezzo": "outdoor/pista", "focus_muscolare": ["gambe", "cardio"], "difficoltà": "Base"}
}
# --- FUNZIONE DI ANALISI WOD ---
def analizza_wod(testo_wod):
    wod_info = {
        "formato": None,
        "durata": None,
        "movimenti": [],
        "tipologia": [],
        "pattern_motorio": [],
        "attrezzatura": [],
        "livello_tecnico": "Base",
        "focus_muscolare": [],
        "modality": []
    }
    testo_wod_lower = testo_wod.lower()
    testo_wod_clean = re.sub(r"[^\w\s]", "", testo_wod_lower)
    sinonimi = {
        "pullups": "pull ups", "pushups": "push ups", "situps": "sit ups",
        "muscleups": "muscle-up", "hspu": "handstand push-up",
        "t2b": "toes to bar", "k2e": "knees to elbows"
    }
    for variante, canonico in sinonimi.items():
        testo_wod_clean = testo_wod_clean.replace(variante, canonico)
    if re.search(r"\bamrap\b", testo_wod_clean):
        wod_info["formato"] = "AMRAP"
    elif re.search(r"\bfor time\b", testo_wod_clean):
        wod_info["formato"] = "For time"
    elif re.search(r"\bemom\b", testo_wod_clean):
        wod_info["formato"] = "EMOM"
    elif re.search(r"\bchipper\b", testo_wod_clean):
        wod_info["formato"] = "Chipper"
    durata_match = re.search(r"(\d{1,3})\s*(minuti|min|')", testo_wod_clean)
    if durata_match:
        wod_info["durata"] = int(durata_match.group(1))
    for db, tipo in [(gymnastics_db, "Gymnastics"), (weightlifting_db, "Weightlifting"), (monostructural_db, "Monostructural")]:
        for mov, props in db.items():
            pattern = rf"\b{re.escape(mov)}\b"
            if re.search(pattern, testo_wod_clean):
                wod_info["movimenti"].append(mov)
                wod_info["tipologia"].append(tipo)
                wod_info["pattern_motorio"].append(props["pattern_motorio"])
                wod_info["attrezzatura"].append(props["attrezzo"])
                wod_info["focus_muscolare"].extend(props["focus_muscolare"])
                wod_info["modality"].append(tipo[0])
    wod_info["pattern_motorio"] = list(set(wod_info["pattern_motorio"]))
    wod_info["attrezzatura"] = list(set(wod_info["attrezzatura"]))
    wod_info["focus_muscolare"] = list(set(wod_info["focus_muscolare"]))
    wod_info["modality"] = list(set(wod_info["modality"]))
    difficolta_map = {"Base": 1, "Intermedio": 2, "Avanzato": 3}
    max_difficolta = 1
    for mov in wod_info["movimenti"]:
        for db in [gymnastics_db, weightlifting_db, monostructural_db]:
            if mov in db:
                livello = db[mov]["difficoltà"]
                max_difficolta = max(max_difficolta, difficolta_map[livello])
    livello_tecnico_inv = {v: k for k, v in difficolta_map.items()}
    wod_info["livello_tecnico"] = livello_tecnico_inv[max_difficolta]
    return wod_info
# --- SEMPLIFICAZIONE MOVIMENTI ---
scaling_map = {
    "pull-up": "ring row",
    "pull ups": "ring row",
    "ring dip": "box dip",
    "handstand push-up": "pike push-up",
    "hspu": "pike push-up",
    "toes to bar": "knees to chest",
    "t2b": "knees to chest",
    "muscle-up": "pull-up + ring dip",
    "bar muscle-up": "pull-up + box dip",
    "ring muscle-up": "pull-up + ring dip",
    "pistol squat": "box step-up",
    "snatch": "kettlebell swing",
    "clean and jerk": "dumbbell clean & press"
}

beginner_map = {
    "ring row": "ring row (feet under rings)",
    "push-ups": "knee push-ups",
    "pull-up": "jumping pull-up",
    "pike push-up": "incline push-up",
    "kettlebell swing": "russian swing",
    "double unders": "single unders",
    "box jump": "step-up",
    "deadlift": "dumbbell deadlift"
}

def genera_versioni_wod(original_wod, movimenti):
    scaled_wod = original_wod
    beginner_wod = original_wod

    for mov in movimenti:
        base_mov = scaling_map.get(mov, mov)
        scaled_wod = re.sub(rf"\b{re.escape(mov)}\b", base_mov, scaled_wod, flags=re.IGNORECASE)

        beginner_mov = beginner_map.get(base_mov, base_mov)
        beginner_wod = re.sub(rf"\b{re.escape(base_mov)}\b", beginner_mov, beginner_wod, flags=re.IGNORECASE)

    return {
        "RX": original_wod.strip(),
        "Scaled": scaled_wod.strip(),
        "Beginner": beginner_wod.strip()
    }

# --- UI: Visualizzazione Versioni WOD ---
def mostra_versioni_wod(wod_input, movimenti):
    versioni = genera_versioni_wod(wod_input, movimenti)

    st.subheader("🔁 Versioni del WOD")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**🏋️‍♂️ RX (originale):**")
        st.code(versioni["RX"], language="text")

    with col2:
        st.markdown("**⚙️ Scaled (intermedio):**")
        st.code(versioni["Scaled"], language="text")

    with col3:
        st.markdown("**🧩 Beginner (principiante):**")
        st.code(versioni["Beginner"], language="text")


# --- SISTEMA ENERGETICO ---
energy_systems_db = {
    "aerobico": {
        "sforzo": "basso/medio",
        "durata": "lunga",
        "esempi": ["corsa lunga", "rowing", "jump rope"],
        "tipico_wod": ["AMRAP", "For time (con durata lunga)"]
    },
    "anaerobico lattacido": {
        "sforzo": "medio/alto",
        "durata": "media",
        "esempi": ["burpee", "kettlebell swing", "running intervallato"],
        "tipico_wod": ["Chipper", "EMOM (con esercizi misti)"]
    },
    "anaerobico alattacido": {
        "sforzo": "altissimo",
        "durata": "breve",
        "esempi": ["snatch", "clean & jerk", "deadlift massimale"],
        "tipico_wod": ["For time (con carichi pesanti)", "Chipper (carichi esplosivi)"]
    }
}

def analizza_sistema_energetico(wod_info):
    """
    Analizza le caratteristiche del WOD e restituisce un dizionario
    che descrive il sistema energetico principale coinvolto.

    Args:
        wod_info (dict): Dizionario con i dettagli del WOD analizzato

    Returns:
        dict: Informazioni sul sistema energetico (durata, sforzo, esempi, ecc.)
    """
    durata = wod_info["durata"] or 0
    movimenti = wod_info["movimenti"]

    if any(m in movimenti for m in ["snatch", "clean and jerk", "deadlift", "muscle-up"]):
        return energy_systems_db["anaerobico alattacido"]
    elif wod_info["formato"] in ["AMRAP", "For time"]:
        return energy_systems_db["aerobico"] if durata > 12 else energy_systems_db["anaerobico lattacido"]
    else:
        return energy_systems_db["anaerobico lattacido"]

def calcola_sistema_energetico(wod: str) -> str:
    """
    Stima il sistema energetico dominante basandosi sul testo del WOD.

    Args:
        wod (str): Testo descrittivo del WOD

    Returns:
        str: Nome del sistema energetico principale
    """
    wod = wod.lower()
    durata_match = re.search(r"(\d{1,3})\s*(minuti|min|')", wod)
    durata = int(durata_match.group(1)) if durata_match else None

    if "sprint" in wod or "tabata" in wod or "emom 1" in wod or (durata and durata <= 5):
        return "Anaerobico alattacido"
    elif durata and 6 <= durata <= 12:
        return "Anaerobico lattacido"
    elif durata and durata > 12:
        return "Aerobico"
    elif "emom" in wod or "amrap" in wod:
        return "Aerobico"
    return "Aerobico"


    wod = wod.lower()
    
    if "emom" in wod or "tabata" in wod:
        return "Anaerobico alattacido"  # lavoro intermittente breve
    elif "for time" in wod or "amrap" in wod:
        if any(t in wod for t in ["5 min", "6 min", "7 min", "8 min"]):
            return "Anaerobico lattacido"
        elif any(t in wod for t in ["10 min", "12 min", "15 min", "20 min", "30 min"]):
            return "Aerobico"
        elif "sprint" in wod or "max effort" in wod:
            return "Anaerobico alattacido"
    elif "sprint" in wod or "100m" in wod or "row 250" in wod:
        return "Anaerobico alattacido"
    
    # fallback
    return "Aerobico"


# --- UI Streamlit ---
st.set_page_config(page_title="WOD Analyzer", page_icon="💪", layout="centered")
st.title("WOD Analyzer 💥")

wod_input = st.text_area("✍️ Inserisci il tuo WOD:", "AMRAP 20 minuti\n100 pull-ups\n200 push-ups\n300 air squat")

if wod_input:
    risultato = analizza_wod(wod_input)
    system_info = analizza_sistema_energetico(risultato)
    
    try:
        nome_sistema = calcola_sistema_energetico(wod_input)
    except:
        nome_sistema = "Non rilevato"
    
    mostra_versioni_wod(wod_input, risultato["movimenti"])

    st.success("✅ Analisi completata!")


    st.subheader("📋 Informazioni chiave")
    st.markdown(f"**Formato:** {risultato['formato'] or 'Non rilevato'}")
    st.markdown(f"**Durata (minuti):** {risultato['durata'] if risultato['durata'] else 'Variabile'}")
    st.markdown(f"**Pattern motori:** {', '.join(risultato['pattern_motorio']) or '---'}")
    st.markdown(f"**Livello tecnico stimato:** {risultato['livello_tecnico']}")

    st.subheader("🧩 Modalità e attrezzi")
    st.markdown(f"**Modality (MGW):** {', '.join(risultato['modality']) or '---'}")
    st.markdown(f"**Attrezzi necessari:** {', '.join(risultato['attrezzatura']) or '---'}")
    st.markdown(f"**Focus muscolare:** {', '.join(risultato['focus_muscolare']) or '---'}")

    st.subheader("💥 Sistema Energetico principale")
    st.markdown(f"**Tipo:** {nome_sistema}")
    st.markdown(f"**Sforzo richiesto:** {system_info['sforzo']}")
    st.markdown(f"**Durata tipica:** {system_info['durata']}")
    st.markdown(f"**Esempi di esercizi:** {', '.join(system_info['esempi'])}")
    st.markdown(f"**Tipico WOD:** {', '.join(system_info['tipico_wod'])}")

    # GRAFICI
    if risultato["pattern_motorio"]:
        pattern_counts = Counter(risultato["pattern_motorio"])
        fig, ax = plt.subplots()
        ax.bar(pattern_counts.keys(), pattern_counts.values())
        ax.set_title("Distribuzione dei Pattern Motori")
        ax.set_xlabel("Pattern")
        ax.set_ylabel("Conteggio")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    if risultato["modality"]:
        modality_counts = Counter(risultato["modality"])
        fig, ax = plt.subplots()
        ax.pie(modality_counts.values(), labels=modality_counts.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title("Distribuzione delle Modalità MGW")
        st.pyplot(fig)

    if risultato["focus_muscolare"]:
        focus_counts = Counter(risultato["focus_muscolare"])
        labels = list(focus_counts.keys())
        values = list(focus_counts.values())
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]
        values += values[:1]
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.plot(angles, values, color='blue', linewidth=2)
        ax.fill(angles, values, color='cyan', alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_yticklabels([])
        ax.set_title("Distribuzione dei Focus Muscolari nel WOD")
        st.pyplot(fig)


  
