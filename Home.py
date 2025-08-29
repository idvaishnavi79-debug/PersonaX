# PersonaX - Streamlit Personality Quiz (MBTI-style)
# Save this file as Home.py and run with: streamlit run personaX_app.py

import streamlit as st
import base64
import json
from io import BytesIO

st.set_page_config(page_title="PersonaX", page_icon="🧭", layout="centered")

# Simple SVG logo encoded as data URI (self-contained)
SVG_LOGO = '''data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240' viewBox='0 0 240 240'>
  <rect rx='24' width='240' height='240' fill='%230f172a'/>
  <g transform='translate(30,30)'>
    <circle cx='60' cy='60' r='46' fill='%231e293b' stroke='%2388b7ff' stroke-width='4'/>
    <path d='M60 20 L75 60 L60 100 L45 60 Z' fill='%2388b7ff' opacity='0.9'/>
    <circle cx='60' cy='60' r='10' fill='%23f8fafc'/>
    <text x='8' y='150' font-family='Arial' font-size='20' fill='%23e6eef8'>PersonaX</text>
  </g>
</svg>'''

# App header
st.image(SVG_LOGO, width=110)
st.title("PersonaX — Fast MBTI-style Personality Predictor")
st.markdown("A quick, friendly personality quiz that predicts your MBTI-like type. Built with Streamlit for your project submissions.")

# Short instructions
st.info("Click **Start Now** to begin the quiz. Answer honestly — there are no right or wrong answers.")

# Start button
if 'started' not in st.session_state:
    st.session_state.started = False

if st.button("Start Now", use_container_width=True):
    st.session_state.started = True

# Questions bank (40 questions across 4 dimensions)
# Each question: (text, dimension, positive_trait)
# dimension keys: 'EI', 'SN', 'TF', 'JP'
# positive_trait indicates which side a positive score favors (first letter in dimension)
QUESTIONS = [
    ("I enjoy large social gatherings and meeting new people.", 'EI', 'E'),
    ("I prefer spending quiet time alone to recharge.", 'EI', 'I'),
    ("I often start conversations with strangers.", 'EI', 'E'),
    ("I usually think before speaking and prefer listening.", 'EI', 'I'),

    ("I focus on facts and present realities more than possibilities.", 'SN', 'S'),
    ("I enjoy imagining future possibilities and patterns.", 'SN', 'N'),
    ("I trust experience and tried-and-true methods.", 'SN', 'S'),
    ("I like exploring abstract theories and underlying meanings.", 'SN', 'N'),

    ("I base decisions mostly on logic and objective analysis.", 'TF', 'T'),
    ("I consider people's feelings and values when making decisions.", 'TF', 'F'),
    ("I prefer to be fair and apply rules consistently.", 'TF', 'T'),
    ("I tend to be warm and compassionate toward others' concerns.", 'TF', 'F'),

    ("I like having things decided and planned in advance.", 'JP', 'J'),
    ("I prefer to stay open to new information and adapt as I go.", 'JP', 'P'),
    ("I appreciate schedules and structure.", 'JP', 'J'),
    ("I often act spontaneously and enjoy flexibility.", 'JP', 'P'),

    # More questions to increase reliability (repeat pattern)
    ("I feel energized after spending time with a group of friends.", 'EI', 'E'),
    ("I prefer to reflect quietly rather than talk through every idea.", 'EI', 'I'),
    ("I like to talk things out to process them.", 'EI', 'E'),
    ("I plan my time carefully and dislike last-minute plans.", 'JP', 'J'),

    ("I often notice small facts others miss.", 'SN', 'S'),
    ("I enjoy interpreting symbols and hidden meanings.", 'SN', 'N'),
    ("I make decisions using clear pros and cons.", 'TF', 'T'),
    ("I find it easy to sense how others feel in a room.", 'TF', 'F'),

    ("I prefer to finish one project before starting another.", 'JP', 'J'),
    ("I adapt my plans frequently and enjoy variety.", 'JP', 'P'),
    ("I trust data and objective tests more than personal stories.", 'TF', 'T'),
    ("I often think about the future and possibilities more than details.", 'SN', 'N'),

    ("I enjoy being the center of attention sometimes.", 'EI', 'E'),
    ("I keep a small circle of close friends rather than many acquaintances.", 'EI', 'I'),
    ("I value traditions and proven methods.", 'SN', 'S'),
    ("I like playing with hypotheticals and "what if" scenarios.", 'SN', 'N'),

    ("When criticized, I try to analyze it objectively.", 'TF', 'T'),
    ("I respond to others' emotions and offer comfort.", 'TF', 'F'),
    ("I prefer clear deadlines and checkpoints.", 'JP', 'J'),
    ("I enjoy improvising and figuring things out on the fly.", 'JP', 'P'),

    ("I speak up in meetings even if I might be wrong.", 'EI', 'E'),
    ("I like to read and reflect rather than share every opinion.", 'EI', 'I'),
    ("I get energized planning long-term goals and systems.", 'SN', 'N'),
    ("I prefer concrete proof over speculative ideas.", 'SN', 'S')
]

# Response scale mapping: Strongly Agree -> +2, Agree -> +1, Disagree -> -1, Strongly Disagree -> -2
SCALE = {
    "Strongly agree": 2,
    "Agree": 1,
    "Neutral": 0,
    "Disagree": -1,
    "Strongly disagree": -2
}

OPTIONS = list(SCALE.keys())

# Utility: compute type
def compute_mbti(responses):
    # responses: list of scores aligned with QUESTIONS
    totals = {'EI': 0, 'SN': 0, 'TF': 0, 'JP': 0}
    for (q, dim, pos_trait), score in zip(QUESTIONS, responses):
        # score positive means leaning toward "Agree"
        # If pos_trait is the first letter in dimension (e.g., 'E' in 'EI'), add score to totals
        first_letter = dim[0]
        if pos_trait == first_letter:
            totals[dim] += score
        else:
            totals[dim] -= score

    # Decide letters
    result = ''
    strengths = {}
    for dim, val in totals.items():
        if dim == 'EI':
            letter = 'E' if val > 0 else 'I'
        elif dim == 'SN':
            letter = 'S' if val > 0 else 'N'
        elif dim == 'TF':
            letter = 'T' if val > 0 else 'F'
        elif dim == 'JP':
            letter = 'J' if val > 0 else 'P'
        result += letter
        strengths[dim] = abs(val)

    return result, totals, strengths

# Explanations for MBTI letters (short)
EXPLANATIONS = {
    'E': "Extraversion: energized by social interaction, outgoing.",
    'I': "Introversion: energized by quiet time, reflective.",
    'S': "Sensing: focuses on facts, details, and practical reality.",
    'N': "Intuition: focuses on patterns, possibilities, and big-picture ideas.",
    'T': "Thinking: decisions guided by logic and objective analysis.",
    'F': "Feeling: decisions guided by values and people's feelings.",
    'J': "Judging: prefers structure, plans, and settled decisions.",
    'P': "Perceiving: prefers flexibility, spontaneity, and open options."
}

# Main quiz UI
if st.session_state.started:
    st.markdown("---")
    st.subheader("PersonaX Quiz — Answer honestly")

    # Use a form so user can answer all and submit once
    with st.form(key='quiz_form'):
        responses = []
        cols_per_row = 1
        for idx, (q_text, dim, pos) in enumerate(QUESTIONS, start=1):
            prompt = f"{idx}. {q_text}"
            resp = st.radio(prompt, OPTIONS, key=f'q{idx}')
            responses.append(SCALE[resp])
        submitted = st.form_submit_button("Predict Personality")

    if submitted:
        mbti, totals, strengths = compute_mbti(responses)
        st.success(f"Predicted personality: **{mbti}**")
        st.write("\n**Detailed breakdown:**")
        for i, dim in enumerate(['EI','SN','TF','JP']):
            letter_a, letter_b = dim[0], dim[1]
            val = totals[dim]
            preferred = letter_a if val>0 else letter_b
            st.write(f"**{dim}**: {preferred} (score {val}) — {EXPLANATIONS[preferred]}")

        # Strength percentages (normalize by max possible)
        max_possible = 2 * len([d for d in QUESTIONS if d[1] == 'EI']) # rough per-dimension variation
        # For better normalization compute per-dim counts
        counts = {k: sum(1 for q in QUESTIONS if q[1]==k) for k in ['EI','SN','TF','JP']}
        st.write("\n**Strengths (relative):**")
        for dim, val in totals.items():
            cnt = counts[dim]
            max_score = cnt * 2
            strength_pct = int((abs(val) / max_score) * 100) if max_score else 0
            st.write(f"{dim}: {strength_pct}%")

        # Short personality summary
        summaries = {
            'ISTJ': "Responsible, practical, and organized — prefers clear plans.",
            'ISFJ': "Warm, responsible, and attentive to others' needs.",
            'INFJ': "Insightful, idealistic, and focused on meaningful connections.",
            'INTJ': "Strategic, independent, and future-focused.",
            'ISTP': "Practical, hands-on problem solver who values flexibility.",
            'ISFP': "Gentle, creative, and tuned to personal values.",
            'INFP': "Idealistic, value-driven, and imaginative.",
            'INTP': "Analytical, curious, and theoretical.",
            'ESTP': "Action-oriented, adaptable, and enjoys lively experiences.",
            'ESFP': "Sociable, spontaneous, and present-focused.",
            'ENFP': "Enthusiastic, imaginative, and people-centered.",
            'ENTP': "Inventive, idea-focused, and enjoys debate.",
            'ESTJ': "Organized, decisive, and likes to lead.",
            'ESFJ': "Caring, cooperative, and community-focused.",
            'ENFJ': "Charismatic, organized, and helps others develop.",
            'ENTJ': "Confident, strategic leader who drives projects forward."
        }

        summary_text = summaries.get(mbti, "A unique combination — your score suggests traits across the spectrum.")
        st.markdown(f"**About {mbti}:** {summary_text}")

        # Offer download of full result JSON
        result = {
            'mbti': mbti,
            'totals': totals,
            'strengths': strengths,
            'answers': {f'q{idx+1}': ans for idx, ans in enumerate(responses)}
        }
        result_json = json.dumps(result, indent=2)
        st.download_button("Download result (JSON)", data=result_json, file_name='personaX_result.json')

        # Option to retake
        if st.button("Retake Quiz"):
            for k in list(st.session_state.keys()):
                if k.startswith('q'):
                    del st.session_state[k]
            st.session_state.started = True
            st.experimental_rerun()

else:
    st.caption("When you're ready, hit Start Now to begin the PersonaX assessment.")

# Footer & usage tips
st.markdown("---")
st.markdown("**Tips:** This is a project-ready baseline. If you want: Add more questions, weight certain items, save results to a database, or show visual charts. I can help extend any of these.")

