import streamlit as st
import pandas as pd

from styles import CARD_CSS, stat_card

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Dashboard - Intranet Portal",
    page_icon="📊",
    layout="wide"
)

def render_dashboard():
    # 1. Security Guard: ตรวจสอบสถานะการเข้าสู่ระบบ
    if "is_authenticated" not in st.session_state or not st.session_state.is_authenticated:
        st.error("⛔ คุณไม่มีสิทธิ์เข้าถึงหน้านี้ กรุณาเข้าสู่ระบบผ่านหน้าแรกก่อน")
        if st.button("🔑 กลับไปหน้า Login / Home"):
            st.switch_page("app.py")
        return

    st.html(CARD_CSS)

    # 2. Header พร้อมตกแต่งด้วย Container และไอคอนเด่นชัด
    with st.container():
        st.title("📊 แดชบอร์ดผู้ดูแลระบบ")
        st.caption("ระบบจัดการหลังบ้าน นำเข้าข้อมูลผ่าน Excel และตรวจสอบสถานะระบบ")

    st.markdown("---")

    # 3. แสดงผลสถิติด้วย Stat Card
    st.markdown("### 📈 ภาพรวมระบบ (System Metrics)")
    st.markdown(
        f"""
        <div class="tw-grid">
            {stat_card("สถานะระบบ", "Active", "Normal", "#10b981")}
            {stat_card("ผู้ใช้งานออนไลน์", "1 คน", "Secure Session", "#3b82f6")}
            {stat_card("การเชื่อมต่อ API", "Connected", "100%", "#8b5cf6")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")




if __name__ == "__main__":
    render_dashboard()