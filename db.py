import pandas as pd
import pymysql
from dotenv import load_dotenv
import os
import streamlit as st

# กำหนดค่าการเชื่อมต่อ MySQL (ปรับเปลี่ยนข้อมูลให้ตรงกับ Server ของคุณ)
load_dotenv()

DB_HOST = os.getenv('DB_HOST')        # หรือ IP Address ของเซิร์ฟเวอร์
DB_USER = os.getenv('DB_USER')             # ชื่อผู้ใช้งาน Database
DB_PASSWORD = os.getenv('DB_PASSWORD')  # รหัสผ่าน
DB_NAME = os.getenv('DB_NAME')            # ชื่อฐานข้อมูล (Database Name)
DB_PORT = int(os.getenv('DB_PORT'))               # พอร์ตมาตรฐานของ MySQL

def get_mysql_connection():
    """สร้างการเชื่อมต่อกับ MySQL Database"""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor # ให้ผลลัพธ์ออกมาเป็น Dictionary
        )
        return connection
    except Exception as e:
        print(f"❌ เชื่อมต่อ MySQL ไม่สำเร็จ: {e}")
        return None

# --- ส่วนของ UI ใน Streamlit ---
st.title("🔌 ทดสอบการเชื่อมต่อ MySQL")

if st.button("คลิกเพื่อทดสอบเชื่อมต่อ Database"):
  # เรียกใช้งานฟังก์ชัน
  result = get_mysql_connection()

  # ตรวจสอบว่าผลลัพธ์เป็น Connection Object หรือ Error Message
  if isinstance(result, str):
    st.error(f"❌ เชื่อมต่อ MySQL ไม่สำเร็จ: {result}")
  else:
    st.success("✅ เชื่อมต่อ MySQL (sojvp) สำเร็จเรียบร้อยแล้ว!")
    # ปิด Connection ทันทีหลังทดสอบเสร็จเพื่อความปลอดภัย
    result.close()

# def fetch_data_from_mysql(query):
#     """ดึงข้อมูลจาก MySQL มาเป็น Pandas DataFrame"""
#     conn = get_mysql_connection()
#     if conn:
#         try:
#             df = pd.read_sql(query, con=conn)
#             return df
#         except Exception as e:
#             print(f"❌ เกิดข้อผิดพลาดในการรัน Query: {e}")
#             return pd.DataFrame()
#         finally:
#             conn.close()
#     return pd.DataFrame()

# def save_dataframe_to_mysql(df, table_name):
#     """บันทึก Pandas DataFrame ลงตาราง MySQL (ใช้ sqlalchemy ช่วยจัดการ)"""
#     from sqlalchemy import create_engine
    
#     # สร้าง Connection String สำหรับ SQLAlchemy (ต้องติดตั้ง sqlalchemy และ pymysql เพิ่ม)
#     # pip install sqlalchemy
#     try:
#         engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4")
        
#         # บันทึกข้อมูลลงตาราง (ถ้ามีตารางอยู่แล้ว ให้เพิ่มข้อมูลต่อท้ายด้วย if_exists='append')
#         df.to_sql(table_name, con=engine, if_exists='append', index=False)
#         return True, "บันทึกข้อมูลลง MySQL สำเร็จ!"
#     except Exception as e:
#         return False, f"❌ บันทึกไม่สำเร็จ: {e}"