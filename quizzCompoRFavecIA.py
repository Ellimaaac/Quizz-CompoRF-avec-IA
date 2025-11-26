# -*- coding: utf-8 -*-
import os
import random

import streamlit as st
from openai import OpenAI  # client compatible Groq


# ================== CLIENT GROQ ==================
# La clé est lue en priorité dans les secrets Streamlit,
# sinon dans la variable d'environnement GROQ_API_KEY.
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def get_ai_explanation(question_text, choices, user_index, correct_index):
    """
    Utilise Groq (API OpenAI-compatible) pour expliquer la bonne réponse
    et pourquoi la réponse donnée est juste ou fausse.
    Les index sont 1-based comme dans ton quiz.
    """
    # Si la clé n'est pas configurée, on renvoie un message simple
    if not GROQ_API_KEY:
        return (
            "L'IA d'explication n'est pas configurée (clé GROQ_API_KEY manquante).\n"
            "Tu peux l'ajouter dans .streamlit/secrets.toml pour activer cette fonction."
        )

    user_answer = choices[user_index - 1]
    correct_answer = choices[correct_index - 1]

    prompt = f"""
Tu es un professeur qui explique simplement l'électronique et les semi-conducteurs à un élève.

Question :
{question_text}

Choix possibles :
""" + "\n".join([f"{i+1}. {c}" for i, c in enumerate(choices)]) + f"""

Réponse de l'élève : {user_index}. {user_answer}
Bonne réponse : {correct_index}. {correct_answer}

1. Explique en quelques phrases pourquoi la bonne réponse est correcte.
2. Si la réponse de l'élève est fausse, explique en quoi sa réponse est trompeuse.
3. Reste concis, niveau ENSEA, en français.
"""

    response = client.responses.create(
        model="openai/gpt-oss-20b",  # modèle Groq, à adapter si tu veux
        input=prompt,
        instructions="Réponds en français, de manière pédagogique mais concise.",
    )

    return response.output_text.strip()


# ================== BANQUE DE QUESTIONS ==================
questions = [
    # ===================== Cours 1 =====================
    {
        "course": 1,
        "text": "Pour décaler le niveau de Fermi vers la bande de valence,",
        "choices": [
            "il faut doper P",
            "il faut chauffer le matériau",
            "il faut doper N",
            "il faut apporter des atomes donneurs",
        ],
        "answer": 1,
    },
    {
        "course": 1,
        "text": "La masse effective d'un électron",
        "choices": [
            "est inversement proportionnelle à la courbure des bandes d'énergie",
            "est la masse de l'électron au repos",
            "est proportionnelle à la dérivée des bandes d'énergie",
            "est inversement proportionnelle à la dérivée des bandes d'énergie",
        ],
        "answer": 1,
    },
    {
        "course": 1,
        "text": "Le niveau de Fermi",
        "choices": [
            "détermine le peuplement des bandes d'énergie",
            "annule la fonction d'onde",
            "est un niveau de tension",
            "annule la fonction de Fermi-Dirac",
        ],
        "answer": 1,
    },
    {
        "course": 1,
        "text": "Le dopage d'un semi-conducteur par des atomes accepteurs",
        "choices": [
            "est un dopage de type NP",
            "est un dopage de type PN",
            "est un dopage de type P",
            "constitue une jonction PN",
        ],
        "answer": 3,
    },
    {
        "course": 1,
        "text": "Le niveau de Fermi d'un semi-conducteur intrinsèque est",
        "choices": [
            "dans la bande de valence",
            "entre les vallées L et X",
            "dans la bande de conduction",
            "approximativement au milieu de la bande interdite",
        ],
        "answer": 4,
    },
    {
        "course": 1,
        "text": "Un trou est un manque",
        "choices": [
            "d'ion positif",
            "d'électron",
            "d'ion négatif",
            "d'atome",
        ],
        "answer": 2,
    },
    {
        "course": 1,
        "text": 'Un matériau isolant a un "grand" gap.',
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 1,
        "text": "Les matériaux à gap direct sont adaptés à la fabrication de composants opto-électroniques.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 1,
        "text": "À faible champ électrique, la mobilité est le coefficient de proportionnalité "
                "entre la vitesse des porteurs de charges mobiles et le champ électrique.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 1,
        "text": "Les électrons ont tendance à remplir d'abord les niveaux d'énergie de plus haute énergie.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 1,
        "text": "La position du niveau de Fermi dans la bande interdite détermine le peuplement "
                "en électrons de la bande de conduction.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 1,
        "text": "Un semi-conducteur extrinsèque est un semi-conducteur dans lequel ont été introduits "
                "des atomes d'impuretés.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },

    # ===================== Cours 2 =====================
    {
        "course": 2,
        "text": "Les contacts ohmiques d'une diode sont",
        "choices": [
            "des dépôts métalliques de part et d'autre du composant.",
            "des pointes de mesures.",
            "une résistance de protection en parallèle avec la diode.",
            "des résistances de protection en série avec la diode.",
        ],
        "answer": 1,
    },
    {
        "course": 2,
        "text": "Pour décaler le niveau de Fermi vers la bande de valence,",
        "choices": [
            "il faut doper P",
            "il faut apporter des atomes donneurs",
            "il faut chauffer le matériau",
            "il faut doper N",
        ],
        "answer": 1,
    },
    {
        "course": 2,
        "text": "Lors du tracé du diagramme des bandes d'une jonction PN, il faut",
        "choices": [
            "aligner les niveaux E₀ des deux côtés",
            "aligner les niveaux Ev des deux côtés",
            "aligner les niveaux de Fermi des deux côtés",
            "aligner les niveaux Ec des deux côtés",
        ],
        "answer": 3,
    },
    {
        "course": 2,
        "text": "Lorsqu'une jonction PN est polarisée en direct,",
        "choices": [
            "les électrons restent confinés dans la région dopée N.",
            "la barrière de potentiel interne diminue.",
            "les trous restent confinés dans la région dopée P.",
            "la barrière d'énergie interne augmente.",
        ],
        "answer": 2,
    },
    {
        "course": 2,
        "text": "Le dopage d'un semi-conducteur par des atomes accepteurs",
        "choices": [
            "est un dopage de type P",
            "est un dopage de type PN",
            "est un dopage de type NP",
            "constitue une jonction PN",
        ],
        "answer": 1,
    },
    {
        "course": 2,
        "text": "Dans une jonction PN à l'équilibre, le champ électrique est maximal "
                "(en valeur absolue) au niveau de la jonction.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 2,
        "text": "Lorsqu'une diode est polarisée en inverse, le courant est rigoureusement nul.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 2,
        "text": "Les électrons ont tendance à remplir d'abord les niveaux d'énergie de plus haute énergie.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 2,
        "text": "La position du niveau de Fermi dans la bande interdite détermine le peuplement "
                "en électrons de la bande de conduction.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 2,
        "text": "Un semi-conducteur extrinsèque est un semi-conducteur dans lequel ont été introduits "
                "des atomes d'impuretés.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },

    # ===================== Cours 3 =====================
    {
        "course": 3,
        "text": "La loi donnant la caractéristique statique de la jonction PN est connue sous le nom de :",
        "choices": [
            "loi de Moore.",
            "loi de Kilby.",
            "loi de Shockley.",
            "loi de Boltzmann.",
        ],
        "answer": 3,
    },
    {
        "course": 3,
        "text": "Les contacts ohmiques d'une diode sont",
        "choices": [
            "des résistances de protection en série avec la diode.",
            "une résistance de protection en parallèle avec la diode.",
            "des dépôts métalliques de part et d'autre du composant.",
            "des pointes de mesures.",
        ],
        "answer": 3,
    },
    {
        "course": 3,
        "text": "Pour une jonction N+P, l'efficacité d'injection est définie par la relation",
        "choices": [
            "Jn/Jp",
            "Jp/Jn",
            "(Jp+Jn)/Jn",
            "(Jp+Jn)/Jp",
        ],
        "answer": 1,
    },
    {
        "course": 3,
        "text": "Lorsqu'une jonction PN est polarisée en direct,",
        "choices": [
            "les électrons restent confinés dans la région dopée N.",
            "la barrière de potentiel interne diminue.",
            "les trous restent confinés dans la région dopée P.",
            "la barrière d'énergie interne augmente.",
        ],
        "answer": 2,
    },
    {
        "course": 3,
        "text": "Dans une jonction PN, le phénomène d'avalanche se produit",
        "choices": [
            "lorsque la tension de polarisation est nulle.",
            "lorsqu'il fait très froid.",
            "lorsque la tension de polarisation en direct est importante.",
            "lorsque la tension de polarisation en inverse est importante.",
        ],
        "answer": 4,
    },
    {
        "course": 3,
        "text": "Lorsque l'on applique une tension Va = 0,6 V sur les contacts ohmiques, "
                "une jonction PN de tension de diffusion 0,8 V voit une tension de",
        "choices": [
            "0,6 V",
            "0,8 V",
            "1,4 V",
            "0,2 V",
        ],
        "answer": 4,
    },
    {
        "course": 3,
        "text": "Dans une jonction PN à l'équilibre, le champ électrique est maximal "
                "(en valeur absolue) au niveau de la jonction.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 3,
        "text": "Lorsqu'une diode est polarisée en inverse, le courant est rigoureusement nul.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },

    # ===================== Cours 4 =====================
    {
        "course": 4,
        "text": "Le gain en courant d'un transistor bipolaire correspond approximativement à",
        "choices": [
            "l'efficacité d'injection de la jonction base-émetteur.",
            "l'efficacité d'injection des porteurs fixes.",
            "l'efficacité d'injection de la jonction base-collecteur.",
            "l'efficacité d'injection de la jonction émetteur-collecteur.",
        ],
        "answer": 1,
    },
    {
        "course": 4,
        "text": "Le modèle petit signal d'un transistor bipolaire est valable si",
        "choices": [
            "vbe >> Vt",
            "vbe << Vt",
            "Vt = 26 mV",
            "Vt << 26 mV",
        ],
        "answer": 2,
    },
    {
        "course": 4,
        "text": "Les jonctions base-émetteur et base-collecteur sont polarisées en direct. "
                "Le transistor est donc en mode",
        "choices": [
            "normal.",
            "saturé.",
            "bloqué.",
            "inverse.",
        ],
        "answer": 2,
    },
    {
        "course": 4,
        "text": "Lorsqu'un transistor bipolaire est polarisé en mode normal,",
        "choices": [
            "la jonction BE est passante et la jonction BC est bloquée.",
            "la jonction BE est passante et la jonction BC est passante.",
            "la jonction BE est bloquée et la jonction BC est passante.",
            "la jonction BE est bloquée et la jonction BC est bloquée.",
        ],
        "answer": 1,
    },
    {
        "course": 4,
        "text": "Lors du blocage d'une jonction PN, le courant s'éteint instantanément.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 4,
        "text": "Dans une jonction PN en régime dynamique, les variations de charges stockées "
                "peuvent être modélisées par une capacité.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 4,
        "text": "La résistance dynamique d'une diode est d'autant plus élevée que le courant "
                "de polarisation est élevé.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 4,
        "text": "La structure d'un transistor bipolaire est symétrique.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 4,
        "text": "Pour une structure donnée, un transistor PNP est plus rapide qu'un transistor NPN.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },

    # ===================== Cours 5 =====================
    {
        "course": 5,
        "text": "Dans la jonction base-émetteur d'un TBH,",
        "choices": [
            "la barrière d'énergie vue par les trous de l'émetteur est inférieure à "
            "celle vue par les trous de la base.",
            "la barrière d'énergie vue par les électrons de l'émetteur est inférieure à "
            "celle vue par les trous de la base.",
            "la barrière d'énergie vue par les électrons de l'émetteur est supérieure à "
            "celle vue par les trous de la base.",
            "la barrière d'énergie vue par les électrons de l'émetteur est identique à "
            "celle vue par les trous de la base.",
        ],
        "answer": 2,
    },
    {
        "course": 5,
        "text": "Les contacts ohmiques d'une diode sont",
        "choices": [
            "des pointes de mesures.",
            "des résistances de protection en série avec la diode.",
            "une résistance de protection en parallèle avec la diode.",
            "des dépôts métalliques de part et d'autre du composant.",
        ],
        "answer": 4,
    },
    {
        "course": 5,
        "text": "L'hétérojonction base-collecteur d'un TBDH est utile pour",
        "choices": [
            "améliorer le gain en courant du transistor sans perdre en rapidité.",
            "améliorer l'efficacité d'injection du transistor sans perdre en rapidité.",
            "améliorer le champ de claquage du transistor sans perdre en rapidité.",
            "améliorer la tenue en tension du transistor sans perdre en rapidité.",
        ],
        "answer": 4,
    },
    {
        "course": 5,
        "text": "Dans un transistor bipolaire à hétérojonction,",
        "choices": [
            "il n'y a pas d'effet Early.",
            "la jonction base-émetteur est bloquée.",
            "le gain en tension est très faible.",
            "le courant de collecteur est très faible.",
        ],
        "answer": 1,
    },
    {
        "course": 5,
        "text": "La base d'un TBH est fabriquée dans un matériau à plus grand gap "
                "que celui de l'émetteur.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 5,
        "text": "Dans un TBH, la résistance d'Early est quasi-nulle.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },

    # ===================== Cours 6 =====================
    {
        "course": 6,
        "text": "La barrière Schottky s'oppose au passage des électrons du métal vers le "
                "semi-conducteur. Elle est due à la différence",
        "choices": [
            "entre les affinités électroniques des deux semi-conducteurs.",
            "entre l'affinité électronique du métal et l'affinité électronique du semi-conducteur.",
            "entre le travail d'extraction du métal et l'affinité électronique du semi-conducteur.",
            "entre le travail d'extraction du semi-conducteur et l'affinité électronique du métal.",
        ],
        "answer": 3,
    },
    {
        "course": 6,
        "text": "Le courant en polarisation inverse d'une diode Schottky est dû",
        "choices": [
            "au courant de trous provenant du métal.",
            "à l'effet d'avalanche.",
            "aux effets thermiques.",
            "à l'effet tunnel.",
        ],
        "answer": 4,
    },
    {
        "course": 6,
        "text": "Une diode Schottky a une meilleure tenue en tension inverse qu'une diode PN "
                "aux dimensions équivalentes.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 6,
        "text": "Le MeSFET est un transistor rapide car sa grille est constituée d'une jonction Schottky.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 6,
        "text": "Dans la jonction base-émetteur d'un TBH,",
        "choices": [
            "la barrière d'énergie vue par les électrons de l'émetteur est identique "
            "à celle vue par les trous de la base.",
            "la barrière d'énergie vue par les électrons de l'émetteur est supérieure "
            "à celle vue par les trous de la base.",
            "la barrière d'énergie vue par les électrons de l'émetteur est inférieure "
            "à celle vue par les trous de la base.",
            "la barrière d'énergie vue par les trous de l'émetteur est inférieure "
            "à celle vue par les trous de la base.",
        ],
        "answer": 3,
    },
    {
        "course": 6,
        "text": "L'hétérojonction base-collecteur d'un TBDH est utile pour",
        "choices": [
            "améliorer la tenue en tension du transistor sans perdre en rapidité.",
            "améliorer l'efficacité d'injection du transistor sans perdre en rapidité.",
            "améliorer le champ de claquage du transistor sans perdre en rapidité.",
            "améliorer le gain en courant du transistor sans perdre en rapidité.",
        ],
        "answer": 1,
    },

    # ===================== Cours 7 =====================
    {
        "course": 7,
        "text": "Le canal d'un HEMT est",
        "choices": [
            "fortement dopé P.",
            "non dopé.",
            "autant dopé que la couche barrière.",
            "fortement dopé N.",
        ],
        "answer": 2,
    },
    {
        "course": 7,
        "text": "À faible tension VDS, un transistor à effet de champ",
        "choices": [
            "est en régime inverse.",
            "est en régime normal.",
            "est en régime de saturation.",
            "est en régime ohmique.",
        ],
        "answer": 4,
    },
    {
        "course": 7,
        "text": "Le transistor HEMT est",
        "choices": [
            "un transistor à grille isolée du canal.",
            "un composant bipolaire.",
            "un transistor unipolaire rapide.",
            "un transistor de puissance.",
        ],
        "answer": 3,
    },
    {
        "course": 7,
        "text": "L'hétérojonction base-collecteur d'un TBH permet d'augmenter la rapidité du transistor "
                "sans perte de gain en courant.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 7,
        "text": "La mobilité électronique est d'autant plus élevée que le dopage est important.",
        "choices": ["Vrai", "Faux"],
        "answer": 2,
    },
    {
        "course": 7,
        "text": "La transconductance d'un FET donne les variations du courant de sortie "
                "par rapport à la tension d'entrée.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },

    # ===================== Cours 8 =====================
    {
        "course": 8,
        "text": "En introduisant des contraintes mécaniques dans le canal de conduction d'un mosfet,",
        "choices": [
            "on peut améliorer la mobilité électronique dans le canal.",
            "on améliore la tenue en tension du transistor.",
            "on peut réduire les courants de fuite.",
            "on peut améliorer la densité d'intégration.",
        ],
        "answer": 1,
    },
    {
        "course": 8,
        "text": "Le mosfet a la particularité",
        "choices": [
            "d'amplifier le courant d'entrée.",
            "d'avoir la grille isolée électriquement du canal.",
            "d'être nécessairement un composant de puissance.",
            "d'être un composant bipolaire.",
        ],
        "answer": 2,
    },
    {
        "course": 8,
        "text": "La fréquence de transition d'un transistor à effet de champ dépend de sa transconductance.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 8,
        "text": 'L\'épaisseur du "spacer" d\'un HEMT a une influence sur le courant dans le canal.',
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
    {
        "course": 8,
        "text": "Le silicium est un matériau piézo-résistif.",
        "choices": ["Vrai", "Faux"],
        "answer": 1,
    },
]


# ================== FONCTIONS UTILITAIRES ==================
def reset_quiz(selected_course):
    """Initialise ou réinitialise le quiz dans st.session_state."""
    if selected_course == "Tous":
        qs = questions.copy()
    else:
        qs = [q for q in questions if q["course"] == selected_course]

    random.shuffle(qs)

    st.session_state.questions_selection = qs
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.completed = False
    st.session_state.last_feedback = ""
    st.session_state.last_correct_answer = ""
    st.session_state.last_explanation = ""


def main():
    st.set_page_config(page_title="Quiz Semi-conducteurs", page_icon="⚡")

    st.title("⚡ Quiz semi-conducteurs / composants (Moodle ENSEA)")
    st.write(
        "Choisis un cours à réviser, réponds aux questions, et je calcule ton score.\n"
        "Les questions sont tirées de tes quiz Moodle."
    )

    # === Initialisation de l'état ===
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        reset_quiz("Tous")

    # === Barre latérale : paramètres ===
    st.sidebar.header("Paramètres du quiz")
    choix_cours = st.sidebar.selectbox(
        "Cours à réviser",
        options=["Tous", 1, 2, 3, 4, 5, 6, 7, 8],
        help="Choisis un numéro de cours ou 'Tous' pour mélanger.",
    )

    if st.sidebar.button("🔁 (Re)commencer le quiz"):
        reset_quiz(choix_cours)

    # === Feedback de la question précédente ===
    if st.session_state.last_feedback:
        if "✅" in st.session_state.last_feedback:
            st.success(st.session_state.last_feedback)
        else:
            st.error(st.session_state.last_feedback)
            if st.session_state.last_correct_answer:
                st.info(f"Bonne réponse : {st.session_state.last_correct_answer}")

        if st.session_state.get("last_explanation"):
            with st.expander("📚 Explication par l'IA"):
                st.write(st.session_state.last_explanation)

    # === Raccourcis vers l'état courant ===
    qs = st.session_state.questions_selection
    idx = st.session_state.current_index
    total = len(qs)

    if total == 0:
        st.warning("Aucune question disponible. Vérifie la banque de questions.")
        return

    # === Quiz terminé ? ===
    if st.session_state.completed or idx >= total:
        st.header("🏁 Quiz terminé")
        score = st.session_state.score
        pourcentage = score / total * 100
        st.write(f"Score final : **{score} / {total}** ({pourcentage:.1f} %)")

        if pourcentage == 100:
            st.balloons()
            st.success("Parfait, tu maîtrises ce(s) cours !")
        elif pourcentage >= 70:
            st.success("Pas mal du tout, encore un peu de révisions et ce sera parfait.")
        else:
            st.warning("Ça vaut le coup de refaire un tour sur le cours et de rejouer le quiz.")

        st.write(
            "Tu peux changer de cours dans la barre latérale et cliquer sur "
            "**(Re)commencer le quiz** pour recommencer."
        )
        return

    # === Affichage de la question courante ===
    question = qs[idx]
    st.markdown(f"### Question {idx + 1} / {total} (cours {question['course']})")
    st.write(question["text"])

    # Radio pour choisir la réponse
    choix = st.radio(
        "Ta réponse :",
        options=list(range(1, len(question["choices"]) + 1)),
        format_func=lambda i: f"{i}. {question['choices'][i - 1]}",
        key=f"q_{idx}_answer",
    )

    # Bouton de validation
    if st.button("Valider et question suivante ➜"):
        bonne_reponse_index = question["answer"]
        bonne_reponse_texte = question["choices"][bonne_reponse_index - 1]

        if choix == bonne_reponse_index:
            st.session_state.score += 1
            st.session_state.last_feedback = "✅ Bonne réponse !"
            st.session_state.last_correct_answer = ""
        else:
            st.session_state.last_feedback = "❌ Mauvaise réponse."
            st.session_state.last_correct_answer = (
                f"{bonne_reponse_index}. {bonne_reponse_texte}"
            )

        # Explication IA (Groq)
        with st.spinner("L'IA prépare une explication..."):
            st.session_state.last_explanation = get_ai_explanation(
                question_text=question["text"],
                choices=question["choices"],
                user_index=choix,
                correct_index=bonne_reponse_index,
            )

        # Passer à la question suivante
        st.session_state.current_index += 1
        if st.session_state.current_index >= total:
            st.session_state.completed = True

        st.rerun()

    # Affichage du score provisoire
    st.progress(idx / total)
    st.caption(f"Score provisoire : {st.session_state.score} / {total}")


if __name__ == "__main__":
    main()
