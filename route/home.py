import streamlit as st

from CSS.styles import CARD_CSS

# ตั้งค่าหน้าเว็บหลัก
st.set_page_config(page_title="Intranet Portal", page_icon="🏠", layout="wide")

st.html(CARD_CSS)

st.markdown(
    """
    <div class="tw-hero">
        <h1>👋 ยินดีต้อนรับเข้าสู่ Intranet Portal</h1>
        <p>เลือกเมนูด้านซ้ายเพื่อเริ่มใช้งานระบบ</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="tw-grid">
        <div class="tw-card" style="--accent:#3b82f6">
            <p style="font-size:1.5rem;margin:0;">🏠</p>
            <p class="tw-value" style="font-size:1.05rem;">หน้าแรก</p>
            <p style="font-size:.85rem;color:#6b7280;margin:0;">ภาพรวมและทางเข้าใช้งานระบบ</p>
        </div>
        <div class="tw-card" style="--accent:#10b981">
            <p style="font-size:1.5rem;margin:0;">🔌</p>
            <p class="tw-value" style="font-size:1.05rem;">ทดสอบเชื่อมต่อ MySQL</p>
            <p style="font-size:.85rem;color:#6b7280;margin:0;">ตรวจสอบสถานะการเชื่อมต่อฐานข้อมูล</p>
        </div>
        <div class="tw-card" style="--accent:#f59e0b">
            <p style="font-size:1.5rem;margin:0;">📊</p>
            <p class="tw-value" style="font-size:1.05rem;">แดชบอร์ด</p>
            <p style="font-size:.85rem;color:#6b7280;margin:0;">ภาพรวมสถานะระบบและการใช้งาน</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
