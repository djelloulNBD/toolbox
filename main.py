import streamlit_authenticator as stauth
import streamlit as st
import hashlib

st.set_page_config(page_title="Instance Links", page_icon="🔗", layout="centered")

def _build_credentials_from_secrets():
    auth_secrets = st.secrets.get("auth", {})
    users = auth_secrets.get("users", [])
    credentials = {"usernames": {}}
    if not users:
        fallback_username = st.secrets.get("login_username")
        fallback_password = st.secrets.get("login_password")
        if fallback_username and fallback_password:
            try:
                hashed_pw = stauth.Hasher([fallback_password]).generate()[0]
            except Exception:
                hashed_pw = fallback_password
            credentials["usernames"][fallback_username] = {
                "name": fallback_username,
                "email": "",
                "password": hashed_pw,
            }
        return credentials
    for user in users:
        username = user.get("username")
        if not username:
            continue
        name = user.get("name", username)
        email = user.get("email", "")
        password = user.get("password", "")
        # Accept either bcrypt-hashed or plaintext and hash if needed
        if isinstance(password, str) and not password.startswith("$2"):
            try:
                password = stauth.Hasher([password]).generate()[0]
            except Exception:
                pass
        credentials["usernames"][username] = {
            "name": name,
            "email": email,
            "password": password,
        }
    return credentials

credentials = _build_credentials_from_secrets()
cookie_name = st.secrets.get("auth", {}).get("cookie_name", "toolbox_auth")
cookie_key = st.secrets.get("auth", {}).get("cookie_key", "toolbox_signature")
cookie_expiry_days = int(st.secrets.get("auth", {}).get("cookie_expiry_days", 7))

authenticator = stauth.Authenticate(
    credentials,
    cookie_name,
    cookie_key,
    cookie_expiry_days,
)

authenticator.login(location="main")
authentication_status = st.session_state.get("authentication_status")
if authentication_status is False:
    st.error("Username/password is incorrect.")
    st.stop()
elif authentication_status is None:
    st.info("Please enter your username and password to continue.")
    st.stop()

st.title("🔗 Instance Links Provider")
authenticator.logout("Logout", "sidebar")

# Sidebar cloud selector
with st.sidebar:
    st.markdown("### Cloud Provider")
    if 'cloud' not in st.session_state:
        st.session_state.cloud = 'aws'
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("AWS", use_container_width=True):
            st.session_state.cloud = 'aws'
    with b2:
        if st.button("Azure", use_container_width=True):
            st.session_state.cloud = 'azure'
    with b3:
        if st.button("GCP", use_container_width=True):
            st.session_state.cloud = 'gcp'
    selected_provider = st.session_state.cloud
    st.caption(f"Selected: {selected_provider.upper()}")

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
    # Build remote_id: require secret from secrets.toml (no defaults)
    secret_suffix = st.secrets.get("secret") or st.secrets.get("auth", {}).get("secret")
    if not secret_suffix:
        st.error("Missing 'secret' in secrets.toml (either top-level 'secret' or 'auth.secret').")
        st.stop()
    upper_plus = instance_name.upper() + secret_suffix
    remote_id = hashlib.md5(upper_plus.encode()).hexdigest()[:17]

    # Determine domain based on selected cloud provider; require base domain from secrets
    provider = st.session_state.get('cloud', 'aws')
    base_domain = (
        st.secrets.get('domain')
        or st.secrets.get(provider)
        or st.secrets.get('auth', {}).get('domain')
    )
    if not base_domain or not isinstance(base_domain, str):
        st.error("Missing 'domain' in secrets.toml (expected 'domain' or 'auth.domain', or provider key 'aws'/'azure'/'gcp').")
        st.stop()
    # Normalize base_domain to start with a single dot
    if not base_domain.startswith('.'):
        base_domain = '.' + base_domain.lstrip('.')

    provider_prefix_map = {
        'aws': '',
        'azure': '.c',
        'gcp': '.b',
    }
    prefix = provider_prefix_map.get(provider, '')
    if prefix and not base_domain.startswith(prefix):
        if base_domain.startswith('.'):
            # e.g., prefix '.c' + base '.labs...' -> '.c.labs...'
            domain = f"{prefix}{base_domain}"
        else:
            domain = f"{prefix}.{base_domain}"
    else:
        domain = base_domain

    rdp_link = f"https://console-{remote_id}{domain}#/?username={username_rdp_hash}&password={password_rdp}"
    terminal_link = f"https://terminal-{remote_id}{domain}"
    wireshark_link = f"https://wireshark-{remote_id}{domain}"

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
