# %%writefile app.py
import streamlit as st

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Streamlit Calculator", page_icon="🔢")

# Use custom CSS to make it look like a real calculator


st.title("🔢 Python Calculator1")

# --- 2. STATE MANAGEMENT ---
# We use session_state to remember the numbers as you click buttons
if 'expression' not in st.session_state:
    st.session_state.expression = ""

# --- 3. DISPLAY ---
# Show the current typed expression
st.markdown(f'<div class="result-box">{st.session_state.expression if st.session_state.expression else "0"}</div>', unsafe_allow_html=True)

# --- 4. BUTTON GRID ---
# Define the layout
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['C', '0', '=', '+']
]

for row in buttons:
    cols = st.columns(4)
    for i, button_text in enumerate(row):
        if cols[i].button(button_text):
            if button_text == 'C':
                st.session_state.expression = ""
                st.rerun()
            elif button_text == '=':
                try:
                    # eval() performs the math calculation automatically
                    result = eval(st.session_state.expression)
                    st.session_state.expression = str(result)
                except:
                    st.session_state.expression = "Error"
                st.rerun()
            else:
                # Add the character to our math string
                st.session_state.expression += button_text
                st.rerun()

st.info("Tip: Click 'C' to clear or use the operators for math.")
