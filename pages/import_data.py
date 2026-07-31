import streamlit as st
import pandas as pd
import os

from styles import CARD_CSS, panel_header

st.html(CARD_CSS)

# 4. ส่วนจัดการไฟล์ Excel (แบ่งสัดส่วน ซ้าย-ขวา ชัดเจนด้วย Card Borders)
st.markdown(
    panel_header(
        "📂",
        "จัดการข้อมูลผ่านไฟล์ Excel",
        "ดาวน์โหลด Template หรืออัปโหลดไฟล์เพื่อนำเข้าข้อมูลเข้าสู่ระบบ",
        "#f59e0b",
    ),
    unsafe_allow_html=True,
)

col_dl, col_ul = st.columns(2, gap="medium")

# ฝั่งซ้าย: ดาวน์โหลด Template
with col_dl:
    with st.container(border=True):
        st.markdown("#### 📥 1. ดาวน์โหลดไฟล์ต้นแบบ")
        st.text("ดาวน์โหลด Template สำหรับใช้กรอกข้อมูลลงระบบ")
        st.markdown("") # เว้นระยะห่าง
        
        current_dir = os.path.dirname(__file__)
        template_path = os.path.abspath(os.path.join(current_dir, "..", "assets", "template.xlsx"))
        
        try:
            with open(template_path, "rb") as file:
                template_bytes = file.read()
                
            st.download_button(
                label="📥 ดาวน์โหลด Excel Template",
                data=template_bytes,
                file_name="import_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch"
            )
        except FileNotFoundError:
            st.warning("⚠️ ไม่พบไฟล์ Template ในโฟลเดอร์ assets/template.xlsx")

# ฝั่งขวา: อัปโหลดไฟล์ Excel
with col_ul:
    with st.container(border=True):
        st.markdown("#### 📤 2. อัปโหลดข้อมูลเข้าระบบ")
        uploaded_file = st.file_uploader(
            "เลือกไฟล์ Excel ที่กรอกข้อมูลแล้ว (.xlsx)", 
            type=["xlsx", "xls"], 
            key="excel_uploader"
        )

# 5. ส่วนแสดงตัวอย่างข้อมูลเมื่ออัปโหลดไฟล์สำเร็จ
if uploaded_file is not None:
    st.markdown("---")
    with st.container(border=True):
        st.markdown("### 👀 ตรวจสอบข้อมูลก่อนบันทึก")
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"อ่านไฟล์สำเร็จ! (พบข้อมูลทั้งหมด {df.shape[0]} แถว, {df.shape[1]} คอลัมน์)")
            
            # แสดงตารางแบบปรับความกว้างอัตโนมัติ
            st.dataframe(df.head(10), width="stretch")

            col_btn1, col_btn2 = st.columns([1, 4])
            with col_btn1:
                if st.button("🚀 ยืนยันบันทึก", type="primary", width="stretch"):
                    st.success("🎉 บันทึกข้อมูลลง Database สำเร็จ!")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")

st.markdown("---")

# 6. ข้อมูลเซสชันและปุ่มออกจากระบบ (จัดให้อยู่ใน Expander เพื่อความสะอาดตา)
with st.expander("🛠️ เมนูขั้นสูง & ข้อมูลเซสชันระบบ (Session State)"):
    if st.session_state.get("user_info"):
        st.json(st.session_state.user_info)
    else:
        st.info("ไม่พบข้อมูลดิบของ Session")
    
    st.markdown("")
    if st.button("🚪 ออกจากระบบ (Logout)", type="secondary"):
        st.session_state.is_authenticated = False
        st.session_state.user_info = None
        st.query_params.clear()
        st.success("ออกจากระบบสำเร็จ กำลังพาคุณกลับสู่หน้าแรก...")
        st.switch_page("app.py")