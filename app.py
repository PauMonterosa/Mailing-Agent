import streamlit as st
import pandas as pd
import g4f
from send_agent import MailingAgent

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Pau's Career Agent", page_icon="💼", layout="wide")

# --- CSS PRO ---
st.markdown("""
    <style>
    [data-testid="stMetric"] { background-color: #1e2129; border-radius: 15px; padding: 15px; }
    .stButton>button { border-radius: 8px; font-weight: 600; transition: all 0.3s; }
    .stButton>button:hover { border-color: #ff4b4b; color: #ff4b4b; transform: translateY(-2px); }
    img { border-radius: 8px; background: white; padding: 2px; }
    </style>
    """, unsafe_allow_html=True)

# Inicialización
SPREADSHEET_ID = "11IxapYiwFgpk-8jOrN45r_ItCuyTbCuH6kF9OohuKJg"
agent = MailingAgent(spreadsheet_id=SPREADSHEET_ID)

# --- FUNCIONES AUXILIARES ---
def get_logo_url(company_name):
    clean_name = company_name.lower().split()[0].replace(".", "").replace("'", "")
    return f"https://www.google.com/s2/favicons?sz=128&domain={clean_name}.com"

def generar_texto_motivacional(empresa, puntos_clave, puesto, idioma):
    idiomas_dict = {"Castellano": "español", "Català": "catalán", "English": "inglés"}
    target_lang = idiomas_dict.get(idioma, "español")
    prompt = f"Ingeniero Físico. Párrafo para {empresa} ({puesto}). Claves: {puntos_clave}. En {target_lang}. Máximo 3 frases."
    try:
        return g4f.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    except:
        return "Error al generar. Escribe algo manual aquí..."

st.title("Agente de mailing")

tab1, tab2 = st.tabs(["Mis aplicaciones", "Añadir nueva aplicación"])

# --- TAB 1: MATRIZ CON LOGOS ---
with tab1:
    rows, _ = agent.load_rows_from_sheet(agent.sheets)
    if rows:
        search = st.text_input("🔍 Buscar empresa...", "")
        filtered_rows = [r for r in rows if search.lower() in r['ENTERPRISE'].lower()]
        
        cols_per_row = 3
        for i in range(0, len(filtered_rows), cols_per_row):
            batch = filtered_rows[i : i + cols_per_row]
            cols = st.columns(cols_per_row)
            for j, row in enumerate(batch):
                with cols[j]:
                    with st.container(border=True):
                        c1, c2 = st.columns([1, 4])
                        with c1:
                            st.image(get_logo_url(row['ENTERPRISE']), width=45)
                        with c2:
                            st.subheader(row['ENTERPRISE'])
                        
                        st.markdown(f"👤 **{row['CONTACT_NAME']}**")
                        
                        status = row.get('STATUS', 'DRAFT').upper()
                        if status == "SENT": st.success("✅ ENVIADO")
                        elif "SCHEDULED" in status or "PROGRAMADO" in status: st.info("📅 PROGRAMADO")
                        else: st.warning("📝 BORRADOR")
                        
                        with st.expander("📄 Detalles"):
                            st.write(f"📧 {row['EMAIL']}")
                            st.write(f"🌍 Idioma: {row['LANG']}")
                            st.caption(f"📝 {row['CUSTOM_LINE']}")
                        
                        st.button("📨 Enviar Email", key=f"send_{row['ENTERPRISE']}_{i}_{j}")
    else:
        st.info("No hay datos todavía.")

# --- TAB 2: REGISTRO CON PREVISUALIZACIÓN ---
with tab2:
    st.subheader("🛠️ Configurador de Candidatura")
    if 'draft_ia' not in st.session_state: st.session_state.draft_ia = ""

    with st.container(border=True):
        col_a, col_b = st.columns(2)
        with col_a:
            empresa = st.text_input("🏢 Empresa*")
            puesto = st.text_input("🔧 Puesto")
            email_cont = st.text_input("📧 Email*")
        with col_b:
            idioma_sel = st.selectbox("🌐 Idioma", ["Castellano", "Català", "English"])
            persona = st.text_input("👤 Contacto")
            template_sel = st.selectbox("📄 Plantilla", ["General Tech", "Research/Lab", "Data Science"])

        st.markdown("---")
        puntos_clave = st.text_area("✨ Puntos clave para la IA")
        
        if st.button("🔍 Generar y Previsualizar"):
            if empresa and puntos_clave:
                with st.spinner("Redactando..."):
                    st.session_state.draft_ia = generar_texto_motivacional(empresa, puntos_clave, puesto, idioma_sel)
                    st.rerun()

        custom_line_final = st.text_area("📝 Texto final para el Excel:", value=st.session_state.draft_ia, height=120)
        
        if st.button("🚀 GUARDAR EN GOOGLE SHEETS"):
            if empresa and email_cont:
                lang_code = {"Castellano": "ES", "Català": "CA", "English": "EN"}[idioma_sel]
                nueva_fila = {
                    "ENTERPRISE": empresa, "CONTACT_NAME": persona, "EMAIL": email_cont,
                    "LANG": lang_code, "TEMPLATE_ID": template_sel.lower().replace(" ", "_"),
                    "CUSTOM_LINE": custom_line_final, "STATUS": "DRAFT"
                }
                if agent.add_new_row(nueva_fila):
                    st.success("✅ ¡Guardado!")
                    st.session_state.draft_ia = ""
                else: st.error("Error al guardar.")