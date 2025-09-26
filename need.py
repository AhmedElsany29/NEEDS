# -*- coding: utf-8 -*-
import io
import csv
import time
import requests
import pandas as pd
import streamlit as st
import html as html_lib
from datetime import date  # إضافة الاستيراد هنا

# ===================== Google Form (الإرسال) =====================
FORM_ACTION_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLScguQuan3ScwBl-9W_ikNIJOHyl5YrsTr5GskzMWl1Zmqc0xg/formResponse"
)
ENTRY_MISSING = "entry.178037744"   # النواقص
ENTRY_DAY     = "entry.206469232"   # اليوم
ENTRY_STATUS  = "entry.1422450525"  # حالته

# ===================== Google Sheet (العرض) =====================
SPREADSHEET_ID = "1TKMgAw2OJQVf6HTyPAFaELru7X2p794tSMmDfuzlLgE"
RESPONSES_SHEET_NAME = "Form Responses 1"
CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet={requests.utils.quote(RESPONSES_SHEET_NAME)}"
)

# ===================== صفحة التطبيق =====================
st.set_page_config(page_title="النواقص", page_icon="📝", layout="wide")

# ———————— ثيم أبيض + نص أزرق ————————
st.markdown("""
<style>
:root{
  --PRIMARY:#1877F2;       /* الأزرق الأساسي */
  --PRIMARY_DARK:#1460C6;
  --TITLE_BLUE:#0D47A1;    /* أزرق غامق للعناوين/الليبلز */
}

/* اتجاه وخلفية */
html, body, [data-testid="stAppViewContainer"]{
  direction:rtl; background:#FFFFFF; color:var(--PRIMARY); overflow-x: hidden;
}
[data-testid="stHeader"]{background:transparent}
.block-container{max-width:100%; padding-top:.5rem; width:100%; margin:0 auto; padding-left:0; padding-right:0;}
h1.title{
  font-size:2.4rem;font-weight:800;text-align:center;margin:0 0 1rem;
  color:var(--TITLE_BLUE);
}
.top-actions{display:flex;gap:10px;justify-content:space-between;align-items:center;margin:6px 0 16px}
.top-actions button{
  flex:1; height:50px; border-radius:12px;
  font-weight:800; font-size:1rem;
  background:var(--PRIMARY) !important; color:#fff !important; border:none !important;
}
.top-actions button:hover{background:var(--PRIMARY_DARK) !important}
.section-title{font-weight:800; font-size:1.25rem; margin:12px 0;color:var(--TITLE_BLUE)}
label p{font-size:1rem; font-weight:700; color:var(--TITLE_BLUE)}
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] div[role="combobox"]{
  background:#fff !important; color:var(--TITLE_BLUE) !important;
  border:1.7px solid var(--PRIMARY); border-radius:12px; padding:12px; font-size:1rem; height:48px;
  width:100%; box-sizing:border-box;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stSelectbox"] div[role="combobox"]:focus-within{
  border-color:var(--PRIMARY); box-shadow:0 0 0 3px rgba(240,119,242,.15);
}
::placeholder{color:#6aa6ff!important; opacity:1}
button[kind="primary"]{
  background:var(--PRIMARY) !important; color:#fff !important; border:none !important;
  border-radius:12px !important; height:50px !important; font-weight:800 !important; font-size:1rem !important;
  width:100%;
}
button[kind="primary"]:hover{background:var(--PRIMARY_DARK) !important}
div.stAlert div[role="alert"]{
  background:#FFE7E7 !important;
  border:2px solid #E53935 !important;
  color:#B71C1C !important;
  border-radius:12px; padding:12px;
}
.needs-wrap{margin-top:10px; width:100%; box-sizing:border-box;}
.needs-row{
  display:flex;
  flex-wrap:nowrap;
  gap:4px;
  align-items:center;
  padding:8px;
  border-radius:8px;
  border:1px solid #E3F2FD;
  margin-bottom:6px;
  background:#E3F2FD !important;
  min-height: 50px;
  color: #0f172a;
  width:100%;
  overflow-x: auto;
}
.needs-header{
  display:flex;
  flex-wrap:nowrap;
  gap:4px;
  align-items:center;
  padding:8px;
  border-radius:8px;
  margin-bottom:6px;
  background:#D1E9FF;
  color:var(--TITLE_BLUE);
  font-weight:800;
  border: 2px solid var(--PRIMARY);
  overflow-x: auto;
}
.needs-item{
  font-weight:700;
  color: inherit;
  font-size: 1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex:1;
}
.done{text-decoration:line-through; color:#9CA3AF}
.center-title{
  width:100%; 
  display:block; 
  background:#E3F2FD;
  color:#0f172a;
  text-align:center;
  padding:10px; 
  border-radius:8px; 
  margin:6px 0 12px; 
  font-weight:800;
}
button[data-testid="baseButton-secondary"] {
  background: #dc2626 !important;
  color: white !important;
  border: none !important;
  border-radius:6px !important;
  padding: 6px 10px !important;
  font-size: 12px !important;
  cursor: pointer !important;
  height: auto !important;
  min-height: 30px !important;
}
div.row-widget.stHorizontal {
  flex-wrap: nowrap !important;
  overflow-x: auto !important;
  min-width: 100%;
}
[data-testid="column"] {
  flex: none !important;
  min-width: 80px;
  padding: 0 4px;
  box-sizing: border-box;
}
@media (max-width: 600px) {
  .top-actions {flex-direction:row; gap:4px;}
  .top-actions button {height:40px; font-size:0.9rem;}
  div.row-widget.stHorizontal {flex-wrap: nowrap !important; overflow-x: auto !important;}
  [data-testid="column"] {min-width: 60px;}
  .needs-item {font-size:0.85rem;}
  .block-container {padding:0 5px;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">النواقص</h1>', unsafe_allow_html=True)

# ===================== أدوات مساعدة =====================
AR_DAY_NAMES = {0:"الإثنين", 1:"الثلاثاء", 2:"الأربعاء", 3:"الخميس", 4:"الجمعة", 5:"السبت", 6:"الأحد"}

CHECK_TTL_SECONDS = 24 * 3600  # 24 ساعة

def today_ar():
    d = date.today()  # الآن يعمل بفضل الاستيراد
    return AR_DAY_NAMES.get(d.weekday(), "")

@st.cache_data(ttl=60)
def fetch_responses_csv(url: str) -> pd.DataFrame:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    rows = list(csv.reader(io.StringIO(r.text)))
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    if "النواقص" in df.columns:
        df["النواقص"] = df["النواقص"].astype(str).str.strip()
        df = df[df["النواقص"] != ""]
    return df

def submit_to_form(missing_text: str, status_value: str) -> bool:
    day_ar = today_ar()  # اليوم فقط
    payload = {
        ENTRY_MISSING: missing_text.strip(),
        ENTRY_DAY: day_ar,
        ENTRY_STATUS: status_value,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "User-Agent": "Mozilla/5.0",
        "Referer": FORM_ACTION_URL.replace("formResponse", "viewform"),
    }
    try:
        resp = requests.post(FORM_ACTION_URL, data=payload, headers=headers, timeout=15)
        return resp.status_code == 200
    except Exception:
        return False

# ================ حالة الجلسة: العلامات والحذف ==================
if "done_items" not in st.session_state:
    st.session_state["done_items"] = {}
if "deleted_items" not in st.session_state:
    st.session_state["deleted_items"] = set()

def cleanup_done_items():
    now = time.time()
    to_del = [k for k, t in st.session_state["done_items"].items() if now - t >= CHECK_TTL_SECONDS]
    for k in to_del:
        del st.session_state["done_items"][k]

cleanup_done_items()

# ========== دالة عرض الجدول التفاعلي مع خط وحذف (محسّنة) ==========
def render_needs_table_todo(df: pd.DataFrame):
    if "Timestamp" in df.columns:
        ts = pd.to_datetime(df["Timestamp"], errors="coerce")
        df = df.assign(_ts=ts).sort_values("_ts", ascending=False).drop(columns="_ts")

    if "النواقص" in df.columns:
        df = df.dropna(subset=["النواقص"]).drop_duplicates(subset=["النواقص"], keep="first")

    cols = [c for c in ["النواقص", "حالته", "اليوم"] if c in df.columns]
    if not cols:
        st.info("لا توجد بيانات بعد.")
        return

    st.markdown('<div class="center-title">قائمة النواقص</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="needs-header" dir="rtl"><div>النواقص</div><div>الحالة</div><div>اليوم</div><div>إجراءات</div></div>', unsafe_allow_html=True)

    for idx, r in df.iterrows():
        raw_value = r.get("النواقص", "-")
        item_value = str(raw_value) if raw_value is not None else "-"
        item_value = item_value.strip() or "-"

        if item_value in st.session_state["deleted_items"]:
            continue

        is_done = item_value in st.session_state["done_items"]
        
        row_container = st.container()
        
        with row_container:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.markdown(f'<div class="needs-item" style="padding: 4px;">{html_lib.escape(item_value)}</div>', unsafe_allow_html=True)
            with col2:
                status = r.get('حالته', '-')
                st.markdown(f'<div style="padding: 4px; text-align: center;"><strong>{html_lib.escape(str(status))}</strong></div>', unsafe_allow_html=True)
            with col3:
                day = r.get('اليوم', '-')
                st.markdown(f'<div style="padding: 4px; text-align: center; font-size: 0.85em;">{html_lib.escape(str(day))}</div>', unsafe_allow_html=True)
            with col4:
                del_key = f"del_btn__{idx}"
                if st.button("🗑️", key=del_key, help="حذف العنصر", type="secondary"):
                    st.session_state["deleted_items"].add(item_value)
                    try:
                        submit_to_form(item_value, "حذف")
                    except Exception:
                        pass
                    st.rerun()
            
            st.markdown('<hr style="margin: 4px 0; border: 1px solid #eef3f9;">', unsafe_allow_html=True)


# ===================== أزرار الملاحة =====================
c1, c2 = st.columns(2, gap="small")
with c1:
    if st.button("إضافة", key="go_add", use_container_width=True, type="primary"):
        st.session_state["view"] = "add"
with c2:
    if st.button("القائمة", key="go_list", use_container_width=True, type="primary"):
        st.session_state["view"] = "list"
view = st.session_state.get("view", "list")

# ===================== إضافة =====================
if view == "add":
    st.markdown('<div class="section-title">إضافة</div>', unsafe_allow_html=True)

    missing = st.text_input("النواقص *", placeholder="مثال: لمبة 100 وات", label_visibility="visible")

    options = ["قرب يخلص", "خلص"]
    status_index_default = options.index("خلص")
    status = st.selectbox("حالته *", options, index=status_index_default)

    left = st.columns(1)[0]
    dname = today_ar()  # اليوم فقط
    left.write(f"**اليوم:** {dname or '-'}")

    if st.button("حفظ", use_container_width=True, type="primary"):
        if not missing.strip():
            st.error("اكتب اسم/وصف الصنف في خانة (النواقص).")
        else:
            ok = submit_to_form(missing, status)
            if ok:
                st.success("تمت الإضافة 👌")
                time.sleep(0.6)
                st.session_state["view"] = "list"
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("فشل الإرسال — راجع FORM_ACTION_URL و entry.*.")

# ===================== القائمة (تفاعلية) =====================
if view == "list":
    st.markdown('<div class="section-title">قائمة النواقص</div>', unsafe_allow_html=True)
    if st.button("تحديث", use_container_width=True, key="refresh", type="primary"):
        st.cache_data.clear()
        st.rerun()

    try:
        df_raw = fetch_responses_csv(CSV_URL)
        if df_raw.empty:
            st.info("لا توجد بيانات بعد.")
        else:
            render_needs_table_todo(df_raw)
    except requests.HTTPError:
        st.error("401/403: لا يمكن قراءة الشيت كـ CSV.")
        st.caption("افتح الشيت > Share > Anyone with the link و/أو File > Publish to the web ثم انسخ رابط CSV.")
        st.code(CSV_URL)
    except Exception as e:
        st.error("تعذر قراءة الشيت.")
        st.code(str(e))
