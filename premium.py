import streamlit as st

def show_premium():

st.set_page_config(page_title="PersonaX Premium", page_icon="💎")

st.title("💎 PersonaX Premium")
st.markdown("Unlock advanced insights and tools to understand yourself better!")

# Benefits
st.subheader("✨ Premium Benefits")
st.write("""
- 📊 **Detailed personality charts** (visual MBTI breakdown).
- 🎯 **Career guidance** tailored to your type.
- 📚 Download **exclusive growth tips & eBooks**.
- 🚀 Get **early access** to upcoming PersonaX features.
""")

# Pricing Plans
st.subheader("💰 Plans")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Free Plan")
    st.write("₹0 / forever")
    st.write("✔ Take the quiz\n✔ Get MBTI prediction")
    st.button("Current Plan", disabled=True)

with col2:
    st.markdown("#### Premium Plan ⭐")
    st.write("₹200 (one-time demo)")
    st.write("✔ Everything in Free\n✔ Career Guidance\n✔ Growth Tips & eBooks")
    if st.button("Upgrade Now"):
        st.success("🎉 Congratulations! Premium Unlocked (Demo Mode)")
        st.balloons()

# Footer
st.markdown("---")
st.caption("This is a demo version.")

