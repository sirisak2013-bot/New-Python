import streamlit as st
import pandas as pd

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

    # 2. Header พร้อมตกแต่งด้วย Container และไอคอนเด่นชัด
    with st.container():
        st.title("📊 แดชบอร์ดผู้ดูแลระบบ")
        st.caption("ระบบจัดการหลังบ้าน นำเข้าข้อมูลผ่าน Excel และตรวจสอบสถานะระบบ")

    st.markdown("---")

    # 3. แสดงผลสถิติด้วย Metric แบบจัดกลุ่มใน Container เดียวกัน
    st.markdown("### 📈 ภาพรวมระบบ (System Metrics)")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric(label="สถานะระบบ", value="Active", delta="Normal")
    with metric_col2:
        st.metric(label="ผู้ใช้งานออนไลน์", value="1 คน", delta="Secure Session")
    with metric_col3:
        st.metric(label="การเชื่อมต่อ API", value="Connected", delta="100%")

    st.markdown("---")




if __name__ == "__main__":
    render_dashboard()