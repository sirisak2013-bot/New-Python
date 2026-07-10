import requests
import streamlit as st
from streamlit_cookies_controller import CookieController
import xml.etree.ElementTree as ET
import xmltodict
import json


# 1. สร้าง controller สำหรับอ่าน Cookies
controller = CookieController()

# 2. อ่านค่าเฉพาะ Cookie ชื่อ 'SessionAdmin' ที่ Manual ของคุณระบุไว้
# หมายเหตุ: ต้องรันแอปบนโดเมนเดียวกันกับที่ระบบ SSO วาง Cookie ไว้
session_id = controller.get('SessionAdmin')

# 3. ตรวจสอบ session_id กับ API ของคุณ
def check_session_with_api(session_id):
    # เรียก API ของคุณเพื่อตรวจสอบ session_id
    # ตัวอย่าง:
    response = requests.post("https://www3.tisi.go.th/session/CheckAdmin.asp", params={"SessionID": session_id})
    response.encoding = 'utf-8'

    data_dict = xmltodict.parse(response.text)
    data_json = json.dumps(data_dict, ensure_ascii=False, indent=4)
    # return response.status_code == 200
    return data_json  # สมมติว่า API ตอบกลับว่า session ถูกต้อง

if session_id:
    st.success("ตรวจพบ Session ของผู้ใช้งานแล้ว!")
    st.write(f"SessionID ที่ได้รับ: {session_id}")
    

    information = check_session_with_api(session_id)
    st.write("ผลลัพธ์จาก API:")
    st.json(information)
else:
    # หากไม่พบ แปลว่ายังไม่ได้ Login
    st.warning("ไม่พบการเข้าสู่ระบบ กรุณาดำเนินการ Login")
    
    # ปุ่มสำหรับ Redirect ไปหน้า Login
    st.link_button("ไปหน้า Login", "https://service.tisi.go.th/newintranet/web/index.php?r=site%2Flogin")