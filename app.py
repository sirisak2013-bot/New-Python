import streamlit as st
import asyncio
import json
import httpx  # ใช้แทน requests สำหรับ async
import xml.etree.ElementTree as ET
from playwright.async_api import async_playwright

async def capture_sso_session(url):
    async with async_playwright() as p:
        # เปิด browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto(url)
        
        # ปรับเปลี่ยน: ใช้ st.info แทน input() เพื่อแจ้งให้ผู้ใช้ทราบ
        st.info("กรุณาล็อกอินในหน้าต่าง Browser ที่เด้งขึ้นมา แล้วกดปุ่ม 'ตรวจสอบสิทธิ์' ในหน้าเว็บนี้")
        
        # รอให้ผู้ใช้ login (วิธีนี้เป็นแบบหยาบๆ ต้องให้ผู้ใช้กดยืนยันปุ่มใน Streamlit อีกที)
        # จริงๆ ควรใช้การดักจับ event ว่า login สำเร็จหรือยัง
        storage = await context.storage_state()
        cookies = storage.get('cookies', [])
        session_admin_value = next((c['value'] for c in cookies if c['name'] == 'SessionAdmin'), None)
        
        await browser.close()
        return session_admin_value

async def verify_with_sso_api(token):
    sso_api_url = "https://www3.tisi.go.th/session/CheckAdmin.asp"
    async with httpx.AsyncClient() as client:
        payload = {'session_id': token}
        response = await client.post(sso_api_url, data=payload, timeout=10.0)
        
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            status = root.find('status').text
            if status == "OK":
                return root.find('username').text
    return None

# --- ส่วน UI ---
st.title("ระบบตรวจสอบสิทธิ์ผ่าน SSO API")

if st.button("เริ่มกระบวนการ Login"):
    # ทำงานแบบ async
    token = asyncio.run(capture_sso_session("https://service.tisi.go.th/newintranet/web/index.php?r=site%2Flogin"))
    
    if token:
        st.write("ได้รับ Token แล้ว กำลังตรวจสอบ...")
        username = asyncio.run(verify_with_sso_api(token))
        if username:
            st.success(f"ยินดีต้อนรับคุณ {username}")
        else:
            st.error("ตรวจสอบสิทธิ์ล้มเหลว")
    else:
        st.error("ไม่พบ SessionAdmin กรุณาล็อกอินใหม่")