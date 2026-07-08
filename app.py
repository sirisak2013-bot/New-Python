import streamlit as st
import requests
import xml.etree.ElementTree as ET

# --- 1. ส่วนของฟังก์ชันสำหรับจัดการข้อมูล (Logic) ---
def verify_with_sso_api(token):
    sso_api_url = "https://www3.tisi.go.th/session/CheckAdmin.asp"
    try:
        # โดยปกติการ POST ไปยัง .asp มักต้องส่งค่าผ่าน 'data' (form-data) 
        # คุณอาจต้องสอบถามเจ้าหน้าที่ว่าต้องส่งชื่อ parameter ว่าอะไร เช่น 'session_id' หรือ 'token'
        payload = {'session_id': token} 
        
        # ส่ง POST request
        response = requests.post(sso_api_url, data=payload, timeout=5)
        
        if response.status_code == 200:
            # วิเคราะห์ข้อมูล XML ที่ได้รับกลับมา
            root = ET.fromstring(response.content)
            
            # สมมติว่าโครงสร้าง XML เป็นแบบ <result><status>OK</status><username>...</username></result>
            # คุณต้องปรับแก้ตาม Tag จริงที่ API ตอบกลับมาครับ
            status = root.find('status').text
            if status == "OK":
                return {"username": root.find('username').text}
            else:
                return None
        else:
            return None
            
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการติดต่อ SSO API: {e}")
        return None

# --- 2. ส่วนแสดงผลบนหน้าเว็บ (Main UI) ---
# ย้ายคำสั่ง st มาไว้ด้านนอกฟังก์ชัน เพื่อให้โหลดขึ้นหน้าเว็บทันที
st.title("ระบบตรวจสอบสิทธิ์ผ่าน SSO API")
st.write("ถ้าเห็นข้อความนี้แสดงว่าระบบหน้าเว็บทำงานปกติแล้วครับ!")

# สร้างช่องให้กรอก Token และปุ่มกด
token_input = st.text_input("กรุณากรอก Session Token / ID ของคุณ:")

if st.button("ตรวจสอบสิทธิ์"):
    if token_input:
        with st.spinner("กำลังตรวจสอบสิทธิ์..."):
            result = verify_with_sso_api(token_input)
            
        if result:
            st.success(f"ยินดีต้อนรับคุณ {result['username']} เข้าสู่ระบบ!")
        else:
            st.error("ไม่สามารถตรวจสอบสิทธิ์ได้ หรือ Token ไม่ถูกต้อง")
    else:
        st.warning("กรุณากรอกข้อมูลลงในช่องก่อนกดปุ่มครับ")
