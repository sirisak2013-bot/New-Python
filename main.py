import requests
import streamlit as st
from streamlit_cookies_controller import CookieController
import xmltodict

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
    pg.run()
    
else:
    # หากยังไม่ Login ให้แสดงหน้าแจ้งเตือนตรงนี้ (ไม่ต้องใช้ st.switch_page)
    st.set_page_config(page_title="Intranet Portal - Login Required", page_icon="🔐", layout="centered")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.warning("⚠️ ไม่พบการเข้าสู่ระบบ กรุณาดำเนินการ Login ผ่านระบบกลาง")
        st.link_button("👉 ไปหน้า Login", "https://service.tisi.go.th/newintranet/web/index.php?r=site%2Flogin", use_container_width=True)