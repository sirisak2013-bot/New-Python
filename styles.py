"""ชุด CSS กลางสำหรับตกแต่งหน้า Streamlit ทุกหน้าในระบบ

ใช้ <style> จริงแทนการโหลด Tailwind ผ่าน CDN <script> เพราะ Streamlit render
HTML ด้วย dangerouslySetInnerHTML ซึ่งเบราว์เซอร์จะไม่รัน <script> ที่แทรกเข้ามาแบบนั้น
(ข้อจำกัดของ DOM ไม่ใช่ Streamlit) การเขียน CSS ตรงแบบนี้จึงเป็นวิธีเดียวที่ใช้งานได้จริง
และไม่พึ่งพาอินเทอร์เน็ตภายนอก ซึ่งสำคัญเพราะระบบรันบน intranet ภายใน
"""

CARD_CSS = """
<style>
.tw-card{background:#fff;border:1px solid #ececef;border-radius:14px;
  box-shadow:0 1px 3px rgba(0,0,0,.06);padding:1.25rem;
  border-left:4px solid var(--accent,#3b82f6);
  transition:box-shadow .15s ease;}
.tw-card:hover{box-shadow:0 6px 16px rgba(0,0,0,.10);}
.tw-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;margin-bottom:.5rem;}
.tw-label{font-size:.72rem;font-weight:600;color:#9ca3af;text-transform:uppercase;letter-spacing:.05em;margin:0;}
.tw-value{font-size:1.5rem;font-weight:800;color:#1f2937;margin:.25rem 0;}
.tw-badge{font-size:.72rem;font-weight:600;color:var(--accent,#3b82f6);}

.tw-hero{padding:2rem;border-radius:18px;color:#fff;margin-bottom:1.5rem;
  background:linear-gradient(90deg,#6366f1,#8b5cf6);
  box-shadow:0 8px 24px rgba(99,102,241,.25);}
.tw-hero h1{margin:0;font-size:1.5rem;font-weight:800;}
.tw-hero p{margin:.25rem 0 0;color:#e0e7ff;font-size:.9rem;}

.tw-panel{background:#fff;border:1px solid #ececef;border-radius:14px;
  border-left:4px solid var(--accent,#3b82f6);padding:1.5rem;margin-bottom:1rem;
  box-shadow:0 1px 3px rgba(0,0,0,.06);}
.tw-panel .icon{font-size:1.5rem;line-height:1;}
.tw-panel h2{font-size:1.1rem;font-weight:700;color:#1f2937;margin:.35rem 0 0;}
.tw-panel p{font-size:.85rem;color:#6b7280;margin:.15rem 0 0;}

.tw-login-card{max-width:420px;margin:4rem auto 0;padding:2rem;text-align:center;
  background:#fff;border:1px solid #ececef;border-radius:18px;
  box-shadow:0 20px 40px rgba(0,0,0,.08);}
.tw-login-card .badge{width:64px;height:64px;margin:0 auto 1rem;
  display:flex;align-items:center;justify-content:center;
  border-radius:999px;background:#fef2f2;font-size:1.75rem;}
.tw-login-card h2{font-size:1.2rem;font-weight:700;color:#1f2937;margin:0;}
.tw-login-card p{font-size:.85rem;color:#6b7280;margin:.5rem 0 0;}
</style>
"""


def stat_card(label: str, value: str, badge: str, accent: str) -> str:
    return f"""
    <div class="tw-card" style="--accent:{accent}">
        <p class="tw-label">{label}</p>
        <p class="tw-value">{value}</p>
        <span class="tw-badge">● {badge}</span>
    </div>
    """


def panel_header(icon: str, title: str, subtitle: str, accent: str) -> str:
    return f"""
    <div class="tw-panel" style="--accent:{accent}">
        <p class="icon">{icon}</p>
        <h2>{title}</h2>
        <p>{subtitle}</p>
    </div>
    """
