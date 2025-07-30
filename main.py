import streamlit as st
import hashlib

st.set_page_config(page_title="Instance Links", page_icon="🔗", layout="centered")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login Required")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
    if login_btn:
        valid_username = st.secrets.get("login_username")
        valid_password = st.secrets.get("login_password")
        if username == valid_username and password == valid_password:
            st.session_state.logged_in = True
            st.success("Login successful! Please proceed.")
            st.rerun()
        else:
            st.error("Invalid username or password.")
    st.stop()

st.title("🔗 Instance Links Generator")

st.markdown("""
Enter your **Instance Name** below to generate your Remote ID and quick-access links. 
""")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    instance_name = st.text_input("Instance Name", placeholder="e.g. LBLI-5GEB-1745411368365-10")
    hash_btn = st.button("Generate Links", use_container_width=True)

if hash_btn and instance_name:
    instance_name_lower = instance_name.lower()
    username_rdp = instance_name_lower.split('-')[0] if '-' in instance_name_lower else instance_name_lower
    username_rdp_hash = hashlib.md5(username_rdp.encode()).hexdigest()
    password_rdp = hashlib.md5(instance_name_lower.encode()).hexdigest()
    upper_plus = instance_name.upper() + st.secrets.get("secret")
    remote_id = hashlib.md5(upper_plus.encode()).hexdigest()[:17]

    rdp_link = f"https://console-{remote_id}{st.secrets.get("domain")}#/?username={username_rdp_hash}&password={password_rdp}"
    terminal_link = f"https://terminal-{remote_id}{st.secrets.get("domain")}"
    wireshark_link = f"https://wireshark-{remote_id}{st.secrets.get("domain")}"

    st.markdown("---")
    st.subheader("🔑 Generated Links")
    with st.container():
        st.markdown(f"**Remote ID:** `{remote_id}` ")
        st.markdown(f"**RDP Link:** [Open RDP]({rdp_link})")
        st.code(rdp_link, language="text")
        st.markdown(f"**Terminal Link:** [Open Terminal]({terminal_link})")
        st.code(terminal_link, language="text")
        st.markdown(f"**Wireshark Link:** [Open Wireshark]({wireshark_link})")
        st.code(wireshark_link, language="text")
    st.success("All links and credentials generated! Use the copy buttons for convenience.")

elif hash_btn and not instance_name:
    st.warning("Please enter an Instance Name to generate links.")
