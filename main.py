import requests
import streamlit as st
from streamlit_cookies_controller import CookieController
import xmltodict

from CSS.styles import CARD_CSS

# 2. ฟังก์ชันตรวจสอบ session_id กับ API
def check_session_with_api(session_id):
    try:
        response = requests.post("https://www3.tisi.go.th/session/CheckAdmin.asp", params={"SessionID": session_id}, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return None
        parsed_dict = xmltodict.parse(response.text)
        return parsed_dict
    except Exception:
        return None

controller = CookieController()
st.session_state["_cookie_controller"] = controller


# ไลบรารี CookieController เก็บ cookie ไว้ใน self.__cookies ซึ่งบางจังหวะ (ตอน
# ยังไม่ sync จากเบราว์เซอร์เสร็จ) จะเป็น None แทนที่จะเป็น dict ว่างๆ ทำให้
# controller.get()/.set()/.remove() โยน TypeError ตรงๆ (`in`/item assignment/
# .pop() บน None) ห่อฟังก์ชันเหล่านี้ไว้ให้ปฏิบัติกับ None เหมือน "ยังไม่มี
# cookie นี้" แทนที่จะพัง แล้วรอรอบ rerun ถัดไปค่อยอ่านค่าจริงได้
def cookie_get(name):
    try:
        return controller.get(name)
    except TypeError:
        return None


def cookie_set(name, value):
    try:
        controller.set(name, value)
    except TypeError:
        pass  # cookie ยังไม่ sync จากเบราว์เซอร์ รอ rerun ถัดไป


def cookie_remove(name):
    try:
        controller.remove(name)
    except (TypeError, KeyError):
        pass  # cookie ยังไม่ sync หรือไม่มีอยู่แล้ว ไม่ต้องทำอะไรเพิ่ม


# บนรันแรกสุดของ session (เช่นตอน refresh หน้าเว็บ) ค่า cookie จากเบราว์เซอร์ยัง
# sync มาไม่ทัน (custom component ต้องรอบราวเซอร์ตอบกลับก่อนถึงจะรู้ค่าจริง รอบแรก
# จะได้ default ว่างๆ เสมอ) ถ้าเช็คทันทีจะเข้าใจผิดว่ายังไม่มี cookie ทั้งที่จริงๆ
# มีอยู่แล้วแค่ยังอ่านไม่ทัน เลยต้องรีรันเปล่าๆ 1 รอบก่อน ให้เวลา sync เสร็จก่อน
# ค่อยเช็คค่าจริง
if "_cookie_synced" not in st.session_state:
    st.session_state["_cookie_synced"] = True
    st.rerun()

# 0. หน้าเริ่มต้น - แสดงก่อนเช็ค session ใดๆ ทั้งสิ้น ต้องกดปุ่มก่อนถึงจะเริ่มเช็ค
# session/cookie และเมื่อ logout ก็จะย้อนกลับมาที่หน้านี้อีกครั้ง
# เช็คสองที่ประกอบกัน:
# - session_state["_started"]: อัปเดตทันที เชื่อถือได้ในรีรัน/เปลี่ยนหน้าภายใน
#   session เดิม (ไม่โดนกลไก routing ของ st.navigation แตะเหมือน query_params)
#   แต่ไม่รอดจากการ refresh หน้าเว็บจริง
# - cookie app_started: รอดจากการ refresh แต่การเขียน/อ่านเป็น async ผ่าน
#   custom component บางจังหวะอาจยังไม่ sync ทัน (เขียนไม่ติดในรอบที่กดปุ่มพอดี)
#   ถ้าใช้ตัวเดียวแล้วมันไม่ทำงาน ผู้ใช้จะกดปุ่มแล้วไม่ไปไหนเลย
# ใช้ "ผ่านอันใดอันหนึ่งก็พอ" กันเคสที่ตัวใดตัวหนึ่งเพี้ยน
if not st.session_state.get("_started") and cookie_get('app_started') != '1':
    st.set_page_config(
        page_title="Intranet Portal",
        page_icon="🏠",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    st.html(CARD_CSS)

    st.markdown(
        """
        <div class="tw-login-card">
            <div class="badge">🏠</div>
            <h2>Intranet Portal</h2>
            <p>กดปุ่มด้านล่างเพื่อเริ่มใช้งานระบบ</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 เข้าสู่ระบบ", key="start_btn", width="stretch"):
            st.session_state["_started"] = True
            cookie_set('app_started', '1')
            st.rerun()

    st.html(
        """
        <style>
        .st-key-start_btn button {
            background: linear-gradient(90deg,#7C3AED,#4F46E5);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }
        .st-key-start_btn button:hover {
            filter: brightness(1.08);
        }
        </style>
        """
    )
    st.stop()

session_id = cookie_get('SessionAdmin')

# 3. ตรวจสอบการ Login จาก Cookie
if session_id:
    # เก็บผลตรวจสอบ session ไว้ใน state แล้วรันครั้งถัดๆ ไปถ้า session_id ตัวเดียวกัน
    # เคยตรวจผ่านแล้ว ให้ดึงจาก state มาใช้เลย ไม่ต้องยิง API ไปหา SSO ซ้ำทุกรัน
    if st.session_state.get("_validated_session_id") == session_id and st.session_state.get("is_authenticated"):
        user_data = st.session_state.get("user_info")
    else:
        user_data = check_session_with_api(session_id)
        if user_data:
            st.session_state["_validated_session_id"] = session_id

    if user_data:
        # บันทึกสถานะลงใน Session State
        st.session_state.is_authenticated = True
        st.session_state.user_info = user_data
        st.session_state["shared_data"] = user_data

        # 1. ตรวจสอบและดึงข้อมูลชื่ออย่างปลอดภัย (ป้องกัน KeyError หาก API ตอบกลับมาไม่ตรงโครงสร้าง)
        user_info = st.session_state.get("user_info", {})
    else:
        # ❌ บั๊กที่คุณเจอ: Cookie มี แต่ API SSO บอกว่าพัง/หมดอายุแล้ว!
        # ต้องจัดการเคลียร์ซากทิ้งตรงนี้ทันที
        cookie_remove('SessionAdmin')
        st.session_state.is_authenticated = False
        st.session_state.user_info = None
        st.session_state.pop("_validated_session_id", None)
        st.rerun() # รีเฟรชเพื่อให้หลุดจากลูปไปหน้า Login
    try:

        root_key = list(user_info.keys())[0] if user_info else None

        if root_key:
            user_name = user_info["Admin"]["Sessions"]["Name"]["#text"]
        else:
            user_name = "ไม่พบข้อมูล"
    except Exception:
        user_name = "เกิดข้อผิดพลาดในการอ่านข้อมูล"

    # --- กำหนดหน้าทั้งหมดในระบบเมื่อ Login แล้ว ---
    home_page = st.Page("route/home.py", title="หน้าแรก", icon="🏠")
    test_connect_mysql = st.Page("database/db.py", title="ทดสอบเชื่อมต่อ MySQL", icon="🔌")
    dashboard_page = st.Page("route/dashboard.py", title="แดชบอร์ด", icon="📊")
    import_data_page = st.Page("route/import_data.py", title="นำเข้าข้อมูล", icon="📥")

    pg = st.navigation({
        "เมนูระบบ": [home_page, test_connect_mysql, dashboard_page, import_data_page]
    })

    # 2. เพิ่ม Widget หรือปุ่มอื่นๆ ต่อท้ายใน Sidebar
    with st.sidebar:
        st.divider()  # ขีดเส้นคั่นแบ่งสัดส่วน
        st.write(f"👤 Logged in as : คุณ{user_name}")

        # if st.button("⚙️ Profile"):
        #     st.switch_page("pages/profile.py")  # หรือเปิดหน้าโปรไฟล์

        if st.button("🚪 Logout"):
            # เคลียร์สถานะฝั่งแอปแล้วย้อนกลับไปหน้าเริ่มต้น
            st.session_state.is_authenticated = False
            st.session_state.user_info = None
            st.session_state.pop("_validated_session_id", None)
            st.session_state["_started"] = False
            cookie_remove('app_started')
            # st.rerun() เฉยๆ ไม่เคลียร์ sidebar เดิมที่ค้างอยู่ (เนื้อหา sidebar
            # ที่ประกาศนอก pg.run() ไม่ได้ถูกล้างด้วย soft rerun) เลยต้องสั่งรีโหลด
            # หน้าเว็บจริงจากเบราว์เซอร์แทน - ใช้ st.iframe เพราะ script ที่แทรกผ่าน
            # st.markdown/st.html จะไม่ถูกรันจริง (ถูก insert ด้วย
            # dangerouslySetInnerHTML ซึ่งเบราว์เซอร์ไม่รัน <script> ที่ใส่แบบนั้น)
            # ต้องใช้ iframe ถึงจะรัน JS ได้จริง
            st.iframe(
                "<script>window.parent.location.reload();</script>", height=1
            )
            st.stop()
    pg.run()
    
else:
    # หากยังไม่ Login ให้แสดงหน้าแจ้งเตือนตรงนี้ (ไม่ต้องใช้ st.switch_page)
    st.set_page_config(
        page_title="Intranet Portal - Login Required",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

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