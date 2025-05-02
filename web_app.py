import streamlit as st
import re
import json
import os
import matplotlib.pyplot as plt

# --- DATABASE GYMNASTICS ---
db_gymnastics = {
    "pull up": ("Gymnastics", "trazione", "barra", "schiena"),
    "push up": ("Gymnastics", "spinta", "corpo libero", "petto/spalle"),
    "air squat": ("Gymnastics", "squat", "corpo libero", "gambe"),
    "ring row": ("Gymnastics", "trazione", "anelli", "schiena"),
    "hspu": ("Gymnastics", "spinta", "parete", "spalle/tricipiti"),
    "muscle-up": ("Gymnastics", "trazione", "anelli/sbarra", "total body"),
    "ring dip": ("Gymnastics", "spinta", "anelli", "tricipiti/spalle"),
    "toes to bar": ("Gymnastics", "core", "barra", "addome"),
    "kipping pull up": ("Gymnastics", "trazione", "barra", "schiena"),
    "chest to bar": ("Gymnastics", "trazione", "barra", "schiena"),
    "wall walk": ("Gymnastics", "spinta", "parete", "spalle"),
    "handstand push up": ("Gymnastics", "spinta", "parete", "spalle/tricipiti")
}

# --- DATABASE WEIGHTLIFTING ---
db_weightlifting = {
    "deadlift": ("Weightlifting", "hinge", "bilanciere", "posterior chain"),
    "snatch": ("Weightlifting", "hinge", "bilanciere", "total body"),
    "clean": ("Weightlifting", "hinge", "bilanciere", "total body"),
    "clean and jerk": ("Weightlifting", "hinge/spinta", "bilanciere", "total body"),
    "push jerk": ("Weightlifting", "spinta", "bilanciere", "spalle"),
    "thruster": ("Weightlifting", "squat/spinta", "bilanciere", "gambe/spalle"),
    "power clean": ("Weightlifting", "hinge", "bilanciere", "total body"),
    "power snatch": ("Weightlifting", "hinge", "bilanciere", "total body"),
    "overhead squat": ("Weightlifting", "squat", "bilanciere", "gambe/spalle"),
    "front squat": ("Weightlifting", "squat", "bilanciere", "gambe"),
    "back squat": ("Weightlifting", "squat", "bilanciere", "gambe"),
    "jerk": ("Weightlifting", "spinta", "bilanciere", "spalle"),
    "push press": ("Weightlifting", "spinta", "bilanciere", "spalle"),
    "kettlebell swing": ("Weightlifting", "hinge", "kettlebell", "posterior chain"),
    "kb clean": ("Weightlifting", "hinge", "kettlebell", "total body"),
    "kb snatch": ("Weightlifting", "hinge", "kettlebell", "total body"),
    "kb goblet squat": ("Weightlifting", "squat", "kettlebell", "gambe"),
    "kb thruster": ("Weightlifting", "squat/spinta", "kettlebell", "gambe/spalle"),
    "kb deadlift": ("Weightlifting", "hinge", "kettlebell", "posterior chain"),
    "db snatch": ("Weightlifting", "hinge", "manubrio", "total body"),
    "db clean": ("Weightlifting", "hinge", "manubrio", "total body"),
    "db push press": ("Weightlifting", "spinta", "manubrio", "spalle"),
    "db thruster": ("Weightlifting", "squat/spinta", "manubrio", "gambe/spalle"),
    "landmine press": ("Weightlifting", "spinta", "landmine", "spalle"),
    "landmine trunk rotation": ("Weightlifting", "rotazione", "landmine", "core")
}

# --- DATABASE MONOSTRUCTURAL ---
db_monostructural = {
    "row": ("Monostructural", "locomozione", "rower", "full body"),
    "run": ("Monostructural", "locomozione", "pista/strada", "gambe"),
    "bike": ("Monostructural", "locomozione", "bike", "gambe"),
    "echo bike": ("Monostructural", "locomozione", "echo bike", "gambe"),
    "assault bike": ("Monostructural", "locomozione", "assault bike", "gambe"),
    "ski erg": ("Monostructural", "locomozione", "ski erg", "full body"),
    "double unders": ("Monostructural", "locomozione", "corda", "spalle/polpacci"),
    "single unders": ("Monostructural", "locomozione", "corda", "polpacci"),
    "shuttle run": ("Monostructural", "locomozione", "area aperta", "gambe"),
    "burpee": ("Monostructural", "locomozione", "corpo libero", "total body")
}
# --- DATABASE ENERGETICO ---
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
import streamlit as st
import re
import json
import os
import matplotlib.pyplot as plt

# --- DATABASES (GYM, WL, MONO) --
db_weightlifting_with_load = {
    "deadlift": {"carico_max": 200},
    "clean": {"carico_max": 130},
    "snatch": {"carico_max": 100},
    "clean and jerk": {"carico_max": 140},
    "push press": {"carico_max": 90},
    "thruster": {"carico_max": 100},
    "front squat": {"carico_max": 150},
    "back squat": {"carico_max": 180}
}

# --- DATABASE ENERGETICO ---
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

# --- Funzione Fittizia di Analisi WOD ---
def analizza_wod(testo):
    return {
        "formato": "AMRAP" if "amrap" in testo.lower() else "For time",
        "durata": 10 if "5" in testo else 20,
        "movimenti": ["deadlift", "push press"] if "push" in testo else ["row", "run"]
    }

# --- Analisi Sistema Energetico ---
def analizza_sistema_energetico(wod_info, carichi_sollevati=None):
    durata = wod_info.get("durata", 0)
    movimenti = wod_info.get("movimenti", [])
    system = "aerobico"

    for movimento in movimenti:
        if movimento in db_weightlifting_with_load and carichi_sollevati:
            carico_max = db_weightlifting_with_load[movimento]["carico_max"]
            if carichi_sollevati >= 0.8 * carico_max:
                system = "anaerobico alattacido"
                break
    else:
        if any(m in movimenti for m in ["snatch", "clean", "muscle-up"]):
            system = "anaerobico alattacido"
        elif wod_info.get("formato") in ["AMRAP", "For time"]:
            if durata > 12:
                system = "aerobico"
            else:
                system = "anaerobico lattacido"
        else:
            system = "anaerobico lattacido"

    systems_used = [system]
    if system == "aerobico":
        systems_used.append("anaerobico lattacido")
    elif system == "anaerobico lattacido":
        systems_used.append("aerobico")

    return energy_systems_db[system], systems_used

# --- Grafico a torta dei sistemi energetici ---
def crea_grafico_energetico(systems_used):
    labels = list(set(systems_used))
    sizes = [systems_used.count(label) for label in labels]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax.axis('equal')
    st.pyplot(fig)

# --- Funzione per generare versioni scalate ---
scaling_map = {
    "push press": "dumbbell push press",
    "deadlift": "kettlebell deadlift",
    "clean": "hang power clean",
    "snatch": "kettlebell swing",
    "row": "bike",
    "run": "row",
    "muscle-up": "pull-up",
    "pull-up": "ring row",
    "ring row": "jumping pull-up"
}

beginner_map = {
    "dumbbell push press": "strict press con bastone",
    "kettlebell deadlift": "box good morning",
    "hang power clean": "box squat + curl",
    "kettlebell swing": "russian swing",
    "bike": "assault bike lento",
    "row": "row leggero",
    "pull-up": "ring row",
    "ring row": "row con piedi avanzati",
    "jumping pull-up": "ring row con elastico"
}

def genera_versioni_wod(wod, movimenti):
    scaled = wod
    beginner = wod
    for mov in movimenti:
        base = scaling_map.get(mov, mov)
        scaled = re.sub(rf"\b{re.escape(mov)}\b", base, scaled, flags=re.IGNORECASE)
        beg = beginner_map.get(base, base)
        beginner = re.sub(rf"\b{re.escape(base)}\b", beg, beginner, flags=re.IGNORECASE)
    return scaled.strip(), beginner.strip()

# --- UI Streamlit ---
st.title("💥 WOD Analyzer con Sistema Energetico e Grafico")
st.markdown("Analizza il tuo WOD e scopri quale sistema energetico viene principalmente sollecitato. Inserisci il carico sollevato per movimenti pesanti.")

wod_input = st.text_area("\u270d\ufe0f Inserisci il tuo WOD:", "AMRAP 5: 10/15 calorie row\n10 push-ups\nRest 5:00\nAMRAP 5: 10/15 calorie row\n10 push-ups", key="wod_input")
carico_sollevato = st.number_input("💪 Carico sollevato per i movimenti di peso (in kg):", min_value=0, step=1)

if wod_input:
    risultato = analizza_wod(wod_input)
    system_info, systems_used = analizza_sistema_energetico(risultato, carico_sollevato)

    st.subheader(f"💥 Sistema Energetico principale: {nome_sistema}")
    st.markdown(f"**Sforzo richiesto:** {system_info['sforzo']}")
    st.markdown(f"**Durata tipica:** {system_info['durata']}")
    st.markdown(f"**Esempi di esercizi:** {', '.join(system_info['esempi'])}")
    st.markdown(f"**Tipico WOD:** {', '.join(system_info['tipico_wod'])}")

    st.subheader("\ud83d\udd0b Sistemi Energetici utilizzati:")
    st.markdown(f"- {', '.join(systems_used)}")

    st.subheader("\ud83d\udcca Distribuzione dei Sistemi Energetici:")
    crea_grafico_energetico(systems_used)

    st.subheader("\ud83d\udd04 Versioni del WOD")
    scaled, beginner = genera_versioni_wod(wod_input, risultato["movimenti"])

    with st.expander("\ud83c\udfcb\ufe0f Versione RX (originale)"):
        st.code(wod_input.strip())
    with st.expander("\ud83d\udd3b Versione Scaled"):
        st.code(scaled)
    with st.expander("\ud83d\udc76 Versione Beginner"):
        st.code(beginner)

# --- Funzione Fittizia di Analisi WOD ---
def analizza_wod(testo):
    return {
        "formato": "AMRAP" if "amrap" in testo.lower() else "For time",
        "durata": 10 if "5" in testo else 20,
        "movimenti": ["deadlift", "push press"] if "push" in testo else ["row", "run"]
    }

# --- Analisi Sistema Energetico ---
def analizza_sistema_energetico(wod_info, carichi_sollevati=None):
    durata = wod_info.get("durata", 0)
    movimenti = wod_info.get("movimenti", [])
    system = "aerobico"  # default

    for movimento in movimenti:
        if movimento in db_weightlifting_with_load and carichi_sollevati:
            carico_max = db_weightlifting_with_load[movimento]["carico_max"]
            if carichi_sollevati >= 0.8 * carico_max:
                system = "anaerobico alattacido"
                break
    else:
        if any(m in movimenti for m in ["snatch", "clean", "muscle-up"]):
            system = "anaerobico alattacido"
        elif wod_info.get("formato") in ["AMRAP", "For time"]:
            if durata > 12:
                system = "aerobico"
            else:
                system = "anaerobico lattacido"
        else:
            system = "anaerobico lattacido"

    systems_used = [system]
    if system == "aerobico":
        systems_used.append("anaerobico lattacido")
    elif system == "anaerobico lattacido":
        systems_used.append("aerobico")

    return energy_systems_db[system], systems_used

# --- Grafico a torta dei sistemi energetici ---
def crea_grafico_energetico(systems_used):
    labels = list(set(systems_used))
    sizes = [systems_used.count(label) for label in labels]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax.axis('equal')
    st.pyplot(fig)

# --- UI Streamlit ---
st.title("\ud83d\udca5 WOD Analyzer con Sistema Energetico e Grafico")
st.markdown("Analizza il tuo WOD e scopri quale sistema energetico viene principalmente sollecitato. Inserisci il carico sollevato per movimenti pesanti.")

wod_input = st.text_area("\u270d\ufe0f Inserisci il tuo WOD:", "AMRAP 5: 10/15 calorie row\n10 push-ups\nRest 5:00\nAMRAP 5: 10/15 calorie row\n10 push-ups", key="wod_input")
carico_sollevato = st.number_input("\ud83d\udcaa Carico sollevato per i movimenti di peso (in kg):", min_value=0, step=1)

if wod_input:
    risultato = analizza_wod(wod_input)
    system_info, systems_used = analizza_sistema_energetico(risultato, carico_sollevato)

    st.subheader(f"\ud83d\udca5 Sistema Energetico principale: {list(energy_systems_db.keys())[list(energy_systems_db.values()).index(system_info)].capitalize()}")
    st.markdown(f"**Sforzo richiesto:** {system_info['sforzo']}")
    st.markdown(f"**Durata tipica:** {system_info['durata']}")
    st.markdown(f"**Esempi di esercizi:** {', '.join(system_info['esempi'])}")
    st.markdown(f"**Tipico WOD:** {', '.join(system_info['tipico_wod'])}")

    st.subheader("\ud83d\udd0b Sistemi Energetici utilizzati:")
    st.markdown(f"- {', '.join(systems_used)}")

    st.subheader("\ud83d\udcca Distribuzione dei Sistemi Energetici:")
    crea_grafico_energetico(systems_used)
