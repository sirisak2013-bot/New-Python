import requests
import streamlit as st
from streamlit_cookies_controller import CookieController
import xmltodict
import json

# ตั้งค่าหน้าเว็บหลัก
st.set_page_config(page_title="Intranet Portal", page_icon="🔐", layout="wide")


st.warning("ไม่พบการเข้าสู่ระบบ กรุณาดำเนินการ Login")
st.link_button("ไปหน้า Login", "https://service.tisi.go.th/newintranet/web/index.php?r=site%2Flogin", use_container_width=True)