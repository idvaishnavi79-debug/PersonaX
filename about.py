import streamlit as st

def show_about():

st.set_page_config(page_title="About PersonaX", page_icon="ℹ️")

st.title("ℹ️ About PersonaX")
st.markdown("---")

# Mission
st.subheader("🌟 Our Mission")
st.write("""
PersonaX was created to help people **understand themselves better** through 
a quick, friendly MBTI-style personality quiz.  
It’s built with the vision of empowering students and young minds 
to discover their strengths, career directions, and growth potential.
""")

# About Me
st.subheader("👩‍💻 About the Creator")
st.write("""
Hi! I'm **Vaishnavi**, a Class 10 student, innovator, and author of several books.  
I love combining **spirituality, science, and innovation** to build projects that inspire and guide others.  

PersonaX is one of my initiatives, blending psychology and technology to make 
self-discovery fun and accessible for everyone.
""")

# Future
st.subheader("🚀 Future Vision")
st.write("""
PersonaX is just the beginning!  
In the future, I plan to add:
- AI-powered **career guidance system**  
- **Detailed analytics dashboards** with visual reports  
- Integration with **learning & growth resources** for teens and youth  
""")

# Optional Contact
st.subheader("📬 Contact")
st.write("Have feedback or ideas? Reach out to me:")
st.write("- Email: onlineppptdeliv79@gmail.com")

st.markdown("---")
st.caption("PersonaX © 2025 — Created with ❤️ by Vaishnavi")

