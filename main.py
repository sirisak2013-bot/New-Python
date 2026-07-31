import requests
import streamlit as st
from streamlit_cookies_controller import CookieController
import xmltodict

from styles import CARD_CSS

# 1. สร้าง controller สำหรับอ่าน Cookies
controller = CookieController()
session_id = controller.get('SessionAdmin')

# 2. ฟังก์ชันตรวจสอบ session_id กับ API
def check_session_with_api(session_id):
    try:
        response = requests.post("https://www3.tisi.go.th/session/CheckAdmin.asp", params={"SessionID": session_id}, timeout=10)
        response.encoding = 'utf-8'
        return xmltodict.parse(response.text)
    except Exception:
        return None

# 3. ตรวจสอบการ Login จาก Cookie
if session_id:
    user_data = check_session_with_api(session_id)
    
    # บันทึกสถานะลงใน Session State
    st.session_state.is_authenticated = True
    st.session_state.user_info = user_data
    st.session_state["shared_data"] = user_data

    # --- กำหนดหน้าทั้งหมดในระบบเมื่อ Login แล้ว ---
    home_page = st.Page("pages/home.py", title="หน้าแรก", icon="🏠")
    test_connect_mysql = st.Page("db.py", title="ทดสอบเชื่อมต่อ MySQL", icon="🔌")
    dashboard_page = st.Page("pages/dashboard.py", title="แดชบอร์ด", icon="📊")

    pg = st.navigation({
        "เมนูระบบ": [home_page, test_connect_mysql, dashboard_page]
    })

    # 2. เพิ่ม Widget หรือปุ่มอื่นๆ ต่อท้ายใน Sidebar
    with st.sidebar:
        st.divider()  # ขีดเส้นคั่นแบ่งสัดส่วน
        st.write("👤 **Logged in as:** Admin")

        if st.button("⚙️ Profile"):
            st.switch_page("pages/profile.py")  # หรือเปิดหน้าโปรไฟล์

        if st.button("🚪 Logout"):
            # โค้ดสำหรับเคลียร์ Session หรือเปลี่ยนสถานะการล็อกอิน
            st.session_state["logged_in"] = False
            st.rerun()
    pg.run()
    
else:
    # หากยังไม่ Login ให้แสดงหน้าแจ้งเตือนตรงนี้ (ไม่ต้องใช้ st.switch_page)
    st.set_page_config(page_title="Intranet Portal - Login Required", page_icon="🔐", layout="centered")

    st.html(CARD_CSS)

    st.markdown(
        """
        <div class="tw-login-card">
            <div class="badge">🔐</div>
            <h2>ไม่พบการเข้าสู่ระบบ</h2>
            <p>กรุณาดำเนินการ Login ผ่านระบบกลางเพื่อเข้าใช้งาน Intranet Portal</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button(
            "👉 ไปหน้า Login",
            "https://service.tisi.go.th/newintranet/web/index.php?r=site%2Flogin",
            width="stretch",
            key="login_btn",
        )

    st.html(
        """
        <style>
        .st-key-login_btn button {
            background: linear-gradient(90deg,#7C3AED,#4F46E5);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }
        .st-key-login_btn button:hover {
            filter: brightness(1.08);
        }
        </style>
        """
    )