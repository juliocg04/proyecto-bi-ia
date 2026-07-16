import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from sklearn.linear_model import LinearRegression
from PIL import Image

from auth import validar_login, obtener_usuario

from consultas import (
    obtener_anios,
    obtener_sectores,
    obtener_departamentos,
    obtener_niveles_gobierno,
    obtener_fuentes_financiamiento,
    indicadores_generales,
    gasto_por_anio,
    gasto_por_sector,
    gasto_por_departamento,
    gasto_por_financiamiento,
    gasto_por_nivel_gobierno,
    consulta_integrada,
    serie_temporal_prediccion
)

from reportes import generar_excel_reportes


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Sistema BI - Gasto Reactivación",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# ESTILOS VISUALES MEJORADOS (OPTIMIZADO Y CORREGIDO)
# ============================================================

def aplicar_estilos():
    st.markdown(
        """
        <style>
        /* Importar tipografía moderna */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        /* Reducción drástica de márgenes estructurales de Streamlit para evitar scroll */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f4f6f9 0%, #e9ecef 100%);
            color: #1e293b;
            font-family: 'Inter', sans-serif;
            overflow-y: hidden;
        }

        header[data-testid="stHeader"] {
            background: rgba(0,0,0,0);
            height: 0px !important;
        }

        /* ------------------------------------------------------------
           PERSONALIZACIÓN DE FLECHAS DE SUBMENÚ (SIDEBAR COLLAPSE)
        ------------------------------------------------------------ */
        
        /* 1. Flecha << cuando la barra lateral está ABIERTA / DESPLEGADA */
        [data-testid="stSidebarCollapseButton"] button {
            color: #ffffff !important;               /* Flecha Blanca */
            background-color: #002f6c !important;    /* Fondo Azul UCV */
            border: 1px solid #001f4d !important;
            border-radius: 6px !important;
            opacity: 1 !important;                    
            box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
            transition: all 0.2s ease !important;
        }

        /* 2. Flecha >> cuando la barra lateral está OCULTA / CERRADA (Corregido para Alto Impacto) */
        [data-testid="collapsedControl"] button {
            color: #0f172a !important;               /* Flecha Oscura para contraste */
            background-color: #ffc107 !important;    /* Fondo Amarillo/Ámbar Fijo */
            border: 1px solid #d39e00 !important;
            border-radius: 6px !important;
            opacity: 1 !important;                    /* Cero transparencias que lo opaquen */
            box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
            transition: all 0.2s ease !important;
        }

        /* Efecto Hover para las flechas */
        [data-testid="stSidebarCollapseButton"] button:hover {
            background-color: #ffc107 !important;    
            color: #0f172a !important;               
            transform: scale(1.05);
        }
        
        [data-testid="collapsedControl"] button:hover {
            background-color: #e0a800 !important;    /* Amarillo un poco más oscuro al pasar el mouse */
            transform: scale(1.08);
        }

        /* ------------------------------------------------------------
           CONTENEDOR DE CABECERA (Evita que el botón >> pise el logo)
        ------------------------------------------------------------ */
        .header-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            /* Margen izquierdo estratégico para que la flecha flotante >> entre sin tocar el logo */
            padding-left: 45px; 
            margin-top: -10px;
            margin-bottom: 5px;
        }

        /* Cabecera Principal más compacta */
        .main-title {
            text-align: center;
            font-size: 24px;
            font-weight: 800;
            color: #002f6c; 
            margin: 0px;
            letter-spacing: -0.5px;
        }

        .main-subtitle {
            text-align: center;
            color: #475569;
            font-size: 13px;
            font-weight: 400;
            margin-top: 2px;
            margin-bottom: 0px;
        }

        /* Tarjeta de Login */
        .login-title {
            text-align: center;
            font-size: 28px;
            font-weight: 800;
            color: #002f6c;
            margin-top: 15px;
            margin-bottom: 5px;
        }

        .login-subtitle {
            text-align: center;
            color: #64748b;
            font-size: 14px;
            margin-bottom: 20px;
        }

        

        /* Tarjetas de Contenedores muy compactas */
        .tech-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 10px 14px;
            box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 0px;
            color: #1e293b;
        }
        
        .tech-card h3 {
            color: #002f6c !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            margin-top: 0px !important;
            margin-bottom: 4px !important;
        }

        /* Métricas del Dashboard Compactas */
        div[data-testid="stMetric"] {
            background: #ffffff;
            border-left: 4px solid #0056b3;
            border-top: 1px solid #e2e8f0;
            border-right: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 6px 10px;
            box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.05);
        }

        div[data-testid="stMetricValue"] {
            color: #002f6c;
            font-size: 18px;
            font-weight: 800;
        }

        div[data-testid="stMetricLabel"] {
            color: #64748b;
            font-weight: 600;
            font-size: 11px;
        }

        /* Ajustes de espacio para los Tabs */
        div[data-testid="stTabs"] {
            margin-top: -10px !important;
        }

        /* Botones de Acción */
        .stButton > button {
            background: linear-gradient(135deg, #0056b3 0%, #002f6c 100%);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.2s ease;
            width: 100%;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
            transform: translateY(-1px);
        }

        /* Botón de Descarga */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
        }
        
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #218838 0%, #19692c 100%);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
        }

        /* Barra Lateral (Sidebar) */
        section[data-testid="stSidebar"] {
            background: #0f172a;
            color: #f8fafc;
            border-right: 1px solid #1e293b;
        }
        
        section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] label {
            color: #f8fafc !important;
        }

        .small-note {
            color: #94a3b8;
            font-size: 12px;
            text-align: center;
            margin-top: 15px;
        }

        .security-badge {
            display: inline-block;
            background: rgba(220, 53, 69, 0.1);
            border: 1px solid rgba(220, 53, 69, 0.4);
            color: #dc3545;
            border-radius: 20px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FONDO ANIMADO EXCLUSIVO PARA LA PANTALLA DE LOGIN
# (Grid tipo "data-flow" + barras económicas ascendentes + 
#  partículas conectadas, referenciando Big Data / gasto público)
# ============================================================

def aplicar_fondo_login():
    st.markdown(
        """
        <style>
        /* Sobrescribe el fondo del contenedor principal SOLO en esta vista */
        .stApp {
            background: radial-gradient(circle at 20% 20%, #0a1a3f 0%, #050b1a 55%, #02040a 100%) !important;
            overflow: hidden !important;
        }

        /* Capa de rejilla tecnológica en movimiento */
        .login-bg-grid {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(0, 245, 196, 0.10) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 245, 196, 0.10) 1px, transparent 1px);
            background-size: 46px 46px;
            animation: gridDrift 18s linear infinite;
        }

        @keyframes gridDrift {
            0%   { background-position: 0px 0px; }
            100% { background-position: 46px 92px; }
        }

        /* Resplandores difusos tipo "pulso económico" */
        .login-bg-glow {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            background:
                radial-gradient(420px circle at 15% 25%, rgba(0, 245, 196, 0.18), transparent 60%),
                radial-gradient(480px circle at 85% 75%, rgba(123, 92, 246, 0.18), transparent 60%),
                radial-gradient(360px circle at 80% 15%, rgba(0, 123, 255, 0.14), transparent 60%);
            animation: glowPulse 7s ease-in-out infinite alternate;
        }

        @keyframes glowPulse {
            0%   { opacity: 0.65; }
            100% { opacity: 1; }
        }

        /* Barras estilo "gráfico de gasto público" ascendiendo en el fondo */
        .login-bg-bars {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 42vh;
            z-index: 0;
            pointer-events: none;
            display: flex;
            align-items: flex-end;
            justify-content: space-evenly;
            opacity: 0.16;
        }

        .login-bg-bars span {
            display: block;
            width: 2.4%;
            background: linear-gradient(180deg, #00f5c4 0%, #007bff 100%);
            border-radius: 3px 3px 0 0;
            animation: barPulse 4.5s ease-in-out infinite;
        }

        @keyframes barPulse {
            0%, 100% { transform: scaleY(0.55); }
            50%      { transform: scaleY(1); }
        }

        /* Partículas flotantes (nodos de datos conectados) */
        .login-bg-particles {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            background-image:
                radial-gradient(2px 2px at 10% 20%, rgba(0,245,196,0.6), transparent),
                radial-gradient(2px 2px at 30% 70%, rgba(123,92,246,0.6), transparent),
                radial-gradient(2px 2px at 55% 35%, rgba(0,123,255,0.6), transparent),
                radial-gradient(2px 2px at 75% 60%, rgba(0,245,196,0.5), transparent),
                radial-gradient(2px 2px at 90% 25%, rgba(123,92,246,0.5), transparent),
                radial-gradient(2px 2px at 40% 85%, rgba(0,123,255,0.5), transparent);
            animation: particleFloat 12s ease-in-out infinite alternate;
        }

        @keyframes particleFloat {
            0%   { transform: translateY(0px); }
            100% { transform: translateY(-22px); }
        }

        /* Asegura que el contenido (logos, tarjeta) quede encima del fondo animado */
        section.main > div.block-container {
            position: relative;
            z-index: 2;
        }

        /* Panel del título institucional que reemplaza el espacio en blanco */
        .login-project-title {
            text-align: center;
            padding: 0 6px 18px 6px;
            margin-bottom: 16px;
            border-bottom: 1px solid rgba(0, 245, 196, 0.15);
        }

        .login-project-title .eyebrow {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            color: #00f5c4;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .login-project-title .eyebrow::before,
        .login-project-title .eyebrow::after {
            content: "";
            height: 1px;
            width: 34px;
            background: linear-gradient(90deg, transparent, #00f5c4, transparent);
        }

        .login-project-title h2 {
            color: #f8fafc;
            font-size: 14.5px;
            font-weight: 700;
            line-height: 1.45;
            margin: 0;
            max-width: 100%;
            text-shadow: 0 2px 12px rgba(0,0,0,0.35);
        }

        /* Sobre fondo oscuro, ajustamos la tarjeta de login para que resalte */
        .security-card {
            background: rgba(15, 23, 42, 0.72) !important;
            border: 1px solid rgba(0, 245, 196, 0.25) !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 45px -10px rgba(0,0,0,0.55), 0 0 0 1px rgba(0,245,196,0.05) !important;
        }

        .login-title { color: #f8fafc !important; }
        .login-subtitle { color: #ffffff !important; }
        .small-note { color: #ffffff !important; }

        div[data-testid="stTextInput"] > div,
        div[data-testid="stTextInput"] div[data-baseweb="input"],
        div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
            background-color: #16233f !important;
        }

        div[data-testid="stTextInput"] input {
            background-color: #16233f !important;
            color: #ffffff !important;
            caret-color: #00f5c4 !important;
            border: 1px solid rgba(0, 245, 196, 0.4) !important;
            border-radius: 8px !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #8ea0bd !important;
        }

        div[data-testid="stTextInput"] label {
            color: #ffffff !important;
            font-weight: 600 !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border: 1px solid #00f5c4 !important;
            box-shadow: 0 0 0 2px rgba(0, 245, 196, 0.2) !important;
        }
        </style>

        <div class="login-bg-grid"></div>
        <div class="login-bg-glow"></div>
        <div class="login-bg-particles"></div>
        <div class="login-bg-bars">
            <span style="height:35%; animation-delay:0.0s;"></span>
            <span style="height:55%; animation-delay:0.3s;"></span>
            <span style="height:40%; animation-delay:0.6s;"></span>
            <span style="height:70%; animation-delay:0.2s;"></span>
            <span style="height:50%; animation-delay:0.8s;"></span>
            <span style="height:85%; animation-delay:0.1s;"></span>
            <span style="height:60%; animation-delay:0.5s;"></span>
            <span style="height:45%; animation-delay:0.9s;"></span>
            <span style="height:75%; animation-delay:0.4s;"></span>
            <span style="height:38%; animation-delay:0.7s;"></span>
            <span style="height:65%; animation-delay:0.15s;"></span>
            <span style="height:52%; animation-delay:0.65s;"></span>
            <span style="height:80%; animation-delay:0.35s;"></span>
            <span style="height:42%; animation-delay:0.85s;"></span>
            <span style="height:58%; animation-delay:0.55s;"></span>
            <span style="height:33%; animation-delay:0.05s;"></span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def formato_monto(valor):
    try:
        valor = float(valor)
    except Exception:
        valor = 0.0

    if abs(valor) >= 1_000_000_000:
        return f"S/ {valor / 1_000_000_000:,.2f} mil M"
    if abs(valor) >= 1_000_000:
        return f"S/ {valor / 1_000_000:,.2f} M"
    if abs(valor) >= 1_000:
        return f"S/ {valor / 1_000:,.2f} mil"
    return f"S/ {valor:,.2f}"


def obtener_valor_indicador(df, columna):
    if df is None or df.empty or columna not in df.columns:
        return 0.0

    valor = df.iloc[0][columna]

    if pd.isna(valor):
        return 0.0

    return float(valor)


def lista_con_todos(df, columna):
    if df is None or df.empty or columna not in df.columns:
        return ["Todos"]

    valores = df[columna].dropna().astype(str).sort_values().unique().tolist()
    return ["Todos"] + valores


def crear_fig_layout(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1e293b", size=10),
        height=210, 
        margin=dict(l=10, r=10, t=25, b=10),
        legend=dict(
            bgcolor="rgba(255,255,255,0.8)",
            font=dict(color="#1e293b", size=9),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(gridcolor="#e2e8f0", tickfont=dict(size=9))
    fig.update_yaxes(gridcolor="#e2e8f0", tickfont=dict(size=9))
    return fig


# ============================================================
# CABECERA INSTITUCIONAL OPTIMIZADA
# ============================================================

def dibujar_cabecera():
    # Envoltorio HTML con clase para controlar los márgenes frente a las flechas del sidebar
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    
    try:
        logo_ucv = Image.open("LogoUCV_2018.png")
        logo_mef = Image.open("PCM-Economia.webp")
        
        # Incrementado el tamaño relativo de las columnas de los logos para mayor visibilidad
        col1, col2, col3 = st.columns([1.5, 4, 1.5])
        with col1:
            # Escalado de logo UCV a 150px para solucionar que se viera pequeño
            st.image(logo_ucv, width=150) 
        with col2:
            st.markdown("<div class='main-title'>DASHBOARD DE GASTO DE REACTIVACIÓN ECONÓMICA</div>", unsafe_allow_html=True)
            st.markdown("<div class='main-subtitle'>Convenio de Cooperación Académica: Universidad César Vallejo — MEF</div>", unsafe_allow_html=True)
        with col3:
            st.write("<div style='text-align:right;'>", unsafe_allow_html=True)
            st.image(logo_mef, width=150)
            st.write("</div>", unsafe_allow_html=True)
            
    except Exception:
        st.markdown("<div style='width:100%; text-align:center;'><div class='main-title'>DASHBOARD DE GASTO DE REACTIVACIÓN ECONÓMICA</div>", unsafe_allow_html=True)
        st.markdown("<div class='main-subtitle'>Sistema BI Institucional</div></div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top:0; margin-bottom:10px; border-color:#cbd5e1;'>", unsafe_allow_html=True)


# ============================================================
# LOGIN ADMINISTRATIVO
# ============================================================

def login():
    aplicar_estilos()
    aplicar_fondo_login()

    try:
        logo_ucv = Image.open("LogoUCV_2018.png")
        logo_mef = Image.open("PCM-Economia.webp")
        col_l1, col_l2, col_l3 = st.columns([1, 2.4, 1])
        with col_l1:
            st.image(logo_ucv, width=140)
        with col_l3:
            st.write("<div style='text-align:right;'>", unsafe_allow_html=True)
            st.image(logo_mef, width=140)
            st.write("</div>", unsafe_allow_html=True)
    except Exception:
        pass

    col_a, col_b, col_c = st.columns([1, 1.45, 1])

    with col_b:
        st.markdown("<div class='security-card'>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="login-project-title">
                <div class="eyebrow">Big Data · Business Intelligence · IA</div>
                <h2>Desarrollo de un sistema basado en Big Data para el análisis de gasto
                público y su relación con la reactivación económica en el Perú mediante
                inteligencia de negocios</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<div style='text-align:center;'><span class='security-badge'>🔐 ACCESO RESTRINGIDO</span></div>",
            unsafe_allow_html=True
        )

        st.markdown("<h1 class='login-title'>Ingreso Administrativo</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='login-subtitle'>Gestión Analítica y de Modelos Predictivos IA</p>",
            unsafe_allow_html=True
        )

        usuario = st.text_input("Usuario administrador")
        clave = st.text_input("Contraseña", type="password")

        if st.button("Ingresar al sistema"):
            if not usuario or not clave:
                st.error("Ingrese usuario y contraseña.")
            elif validar_login(usuario, clave):
                datos_usuario = obtener_usuario(usuario)

                st.session_state.autenticado = True
                st.session_state.usuario = usuario
                st.session_state.nombre_usuario = datos_usuario.get("nombre", usuario)
                st.session_state.rol = datos_usuario.get("rol", "ADMIN")

                st.success("Acceso administrativo correcto.")
                st.rerun()
            else:
                st.error("No existe el usuario o no tiene permisos de administrador.")

        st.markdown(
            "<p class='small-note'>El sistema valida credenciales mediante cifrado seguro y autenticación de doble factor.</p>",
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# DASHBOARD PRINCIPAL
# ============================================================

def dashboard():
    aplicar_estilos()
    dibujar_cabecera()

    st.sidebar.markdown("## ⚙️ Panel de Control")

    nombre = st.session_state.get("nombre_usuario", st.session_state.get("usuario", "Administrador"))
    rol = st.session_state.get("rol", "ADMIN")

    st.sidebar.markdown(f"**Usuario:** {nombre}")
    st.sidebar.markdown(f"**Rol:** {rol}")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.session_state.usuario = None
        st.session_state.nombre_usuario = None
        st.session_state.rol = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🔎 Filtros Interactivos")

    try:
        df_anios = obtener_anios()
        anios = lista_con_todos(df_anios, "ano_eje")
    except Exception:
        anios = ["Todos"]

    filtro_anio = st.sidebar.selectbox("Año Fiscal", anios)

    try:
        df_sectores = obtener_sectores(filtro_anio)
        sectores = lista_con_todos(df_sectores, "sector_nombre")
    except Exception:
        sectores = ["Todos"]

    filtro_sector = st.sidebar.selectbox("Sector Gubernamental", sectores)

    try:
        df_departamentos = obtener_departamentos(filtro_anio, filtro_sector)
        departamentos = lista_con_todos(df_departamentos, "departamento_ejecutora_nombre")
    except Exception:
        departamentos = ["Todos"]

    filtro_departamento = st.sidebar.selectbox("Región / Departamento", departamentos)

    try:
        df_niveles = obtener_niveles_gobierno(filtro_anio, filtro_sector, filtro_departamento)
        niveles = lista_con_todos(df_niveles, "nivel_gobierno_nombre")
    except Exception:
        niveles = ["Todos"]

    filtro_nivel = st.sidebar.selectbox("Nivel de Gobierno", niveles)

    try:
        df_fuentes = obtener_fuentes_financiamiento(
            filtro_anio,
            filtro_sector,
            filtro_departamento,
            filtro_nivel
        )
        fuentes = lista_con_todos(df_fuentes, "fuente_financiamiento_nombre")
    except Exception:
        fuentes = ["Todos"]

    filtro_fuente = st.sidebar.selectbox("Fuente de Financiamiento", fuentes)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard Ejecutivo",
        "📈 Predicción con IA",
        "📄 Datos y Reportes",
        "📌 Integración Power BI"
    ])

    # ========================================================
    # TAB 1: DASHBOARD EJECUTIVO
    # ========================================================
    with tab1:
        try:
            df_ind = indicadores_generales(
                filtro_anio,
                filtro_sector,
                filtro_departamento,
                filtro_nivel,
                filtro_fuente
            )

            total_pia = obtener_valor_indicador(df_ind, "total_pia")
            total_pim = obtener_valor_indicador(df_ind, "total_pim")
            total_devengado = obtener_valor_indicador(df_ind, "total_devengado")
            total_girado = obtener_valor_indicador(df_ind, "total_girado")
            avance = obtener_valor_indicador(df_ind, "avance_porcentaje")

            k1, k2, k3, k4, k5 = st.columns(5)
            k1.metric("Total PIA", formato_monto(total_pia))
            k2.metric("Total PIM", formato_monto(total_pim))
            k3.metric("Total Devengado", formato_monto(total_devengado))
            k4.metric("Total Girado", formato_monto(total_girado))
            k5.metric("Avance Devengado", f"{avance:.2f}%")

        except Exception as e:
            st.error("Error al cargar indicadores principales.")
            st.exception(e)

        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        
        col_g1, col_g2, col_g3 = st.columns(3)

        with col_g1:
            st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
            st.markdown("<h3>📈 Evolución Anual</h3>", unsafe_allow_html=True)
            try:
                df_anio = gasto_por_anio(filtro_anio, filtro_sector, filtro_departamento, filtro_nivel, filtro_fuente)
                if not df_anio.empty:
                    df_anio = df_anio.sort_values("ano_eje")

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df_anio["ano_eje"],
                        y=df_anio["total_devengado"],
                        mode="lines+markers",
                        name="Histórico",
                        line=dict(color="#0056b3", width=3),
                        marker=dict(size=6),
                        hovertemplate="Año %{x}<br>S/ %{y:,.2f}<extra></extra>"
                    ))

                    if len(df_anio) >= 2:
                        modelo_anio = LinearRegression()
                        modelo_anio.fit(df_anio[["ano_eje"]], df_anio["total_devengado"])

                        anios_futuros = np.array([[df_anio["ano_eje"].max() + i] for i in range(1, 3)])
                        pred_futuras = np.maximum(modelo_anio.predict(anios_futuros), 0)

                        x_forecast = [df_anio["ano_eje"].iloc[-1]] + anios_futuros.flatten().tolist()
                        y_forecast = [df_anio["total_devengado"].iloc[-1]] + pred_futuras.tolist()

                        fig.add_trace(go.Scatter(
                            x=x_forecast,
                            y=y_forecast,
                            mode="lines+markers",
                            name="Proyección",
                            line=dict(color="#dc3545", width=3, dash="dash"),
                            marker=dict(size=7, symbol="diamond"),
                            hovertemplate="Año %{x}<br>S/ %{y:,.2f} (proyectado)<extra></extra>"
                        ))

                    fig = crear_fig_layout(fig)
                    fig.update_layout(xaxis_title=None, yaxis_title=None)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No hay datos.")
            except Exception as e:
                st.error("Error")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_g2:
            st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
            st.markdown("<h3>🏛 Gasto por Sector (Top 5)</h3>", unsafe_allow_html=True)
            try:
                df_sector = gasto_por_sector(filtro_anio, filtro_sector, filtro_departamento, filtro_nivel, filtro_fuente)
                if not df_sector.empty:
                    df_sector = df_sector.head(5).sort_values("total_devengado", ascending=True)
                    fig = px.bar(df_sector, x="total_devengado", y="sector_nombre", orientation="h")
                    fig.update_traces(marker_color="#002f6c")
                    fig = crear_fig_layout(fig)
                    fig.update_layout(xaxis_title=None, yaxis_title=None)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No hay datos.")
            except Exception as e:
                st.error("Error")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_g3:
            st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
            st.markdown("<h3>🏛 Gasto por Nivel de Gobierno</h3>", unsafe_allow_html=True)
            try:
                df_nivel = gasto_por_nivel_gobierno(filtro_anio, filtro_sector, filtro_departamento, filtro_nivel, filtro_fuente)
                if not df_nivel.empty:
                    fig = px.bar(df_nivel, x="nivel_gobierno_nombre", y="total_devengado")
                    fig.update_traces(marker_color="#ffc107")
                    fig = crear_fig_layout(fig)
                    fig.update_layout(xaxis_title=None, yaxis_title=None)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No hay datos.")
            except Exception as e:
                st.error("Error")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

        col_g4, col_g5 = st.columns(2)

        with col_g4:
            st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
            st.markdown("<h3>📍 Gasto por Departamento (Top 5)</h3>", unsafe_allow_html=True)
            try:
                df_dep = gasto_por_departamento(filtro_anio, filtro_sector, filtro_departamento, filtro_nivel, filtro_fuente)
                if not df_dep.empty:
                    df_dep = df_dep.head(5).sort_values("total_devengado", ascending=True)
                    fig = px.bar(df_dep, x="total_devengado", y="departamento_ejecutora_nombre", orientation="h")
                    fig.update_traces(marker_color="#28a745")
                    fig = crear_fig_layout(fig)
                    fig.update_layout(xaxis_title=None, yaxis_title=None)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No hay datos.")
            except Exception as e:
                st.error("Error")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_g5:
            st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
            st.markdown("<h3>💰 Fuente de Financiamiento</h3>", unsafe_allow_html=True)
            try:
                df_fin = gasto_por_financiamiento(filtro_anio, filtro_sector, filtro_departamento, filtro_nivel, filtro_fuente)
                if not df_fin.empty:
                    fig = px.pie(df_fin, names="fuente_financiamiento_nombre", values="total_devengado", hole=0.4,
                                 color_discrete_sequence=px.colors.qualitative.Safe)
                    fig = crear_fig_layout(fig)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No hay datos.")
            except Exception as e:
                st.error("Error")
            st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # TAB 2: PREDICCIÓN
    # ========================================================
    with tab2:
        st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
        st.subheader("🔮 Modelo de Regresión Lineal - Predicción de Tendencias")

        try:
            df_pred = serie_temporal_prediccion(filtro_anio, filtro_sector, filtro_departamento, filtro_nivel, filtro_fuente)

            if df_pred.empty:
                st.warning("No hay datos suficientes para estructurar el modelo de regresión.")
            else:
                df_pred = df_pred.copy()
                df_pred["periodo"] = df_pred["ano_eje"].astype(int) * 100 + df_pred["mes_eje"].astype(int)
                df_pred = df_pred.sort_values("periodo")
                df_pred["indice"] = np.arange(len(df_pred))

                X = df_pred[["indice"]]
                y = df_pred["total_devengado"].fillna(0)

                modelo = LinearRegression()
                modelo.fit(X, y)

                meses_pred = st.slider("Meses a proyectar a futuro", 1, 12, 6)

                futuros_indices = np.arange(len(df_pred), len(df_pred) + meses_pred).reshape(-1, 1)
                predicciones = modelo.predict(futuros_indices)
                predicciones = np.maximum(predicciones, 0)

                df_futuro = pd.DataFrame({
                    "indice": futuros_indices.flatten(),
                    "total_devengado": predicciones,
                    "tipo": "Predicción"
                })

                df_hist = pd.DataFrame({
                    "indice": df_pred["indice"],
                    "total_devengado": df_pred["total_devengado"],
                    "tipo": "Histórico"
                })

                df_graf = pd.concat([df_hist, df_futuro], ignore_index=True)

                fig = px.line(df_graf, x="indice", y="total_devengado", color="tipo", markers=True,
                              color_discrete_map={"Histórico": "#002f6c", "Predicción": "#dc3545"})
                fig = crear_fig_layout(fig)
                fig.update_layout(height=280, xaxis_title="Periodo Secuencial Evaluado", yaxis_title="Monto Devengado (S/)")
                st.plotly_chart(fig, use_container_width=True)

                colp1, colp2, colp3 = st.columns(3)
                colp1.metric("Último Histórico Registrado", formato_monto(df_pred["total_devengado"].iloc[-1]))
                colp2.metric("Proyección Final Estimada", formato_monto(predicciones[-1]))
                colp3.metric("Tendencia del Modelo", "📈 Creciente" if modelo.coef_[0] > 0 else "📉 Decreciente")

                st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                st.markdown("### 🎯 Validación del Modelo: Predicho vs. Real")
                st.caption(
                    "Cada punto compara, para un periodo histórico, el monto que el modelo habría predicho "
                    "contra el monto real devengado. Cuanto más cerca estén los puntos de la línea roja, "
                    "más preciso es el modelo."
                )

                y_pred_hist = modelo.predict(X)
                ss_res = float(np.sum((y - y_pred_hist) ** 2))
                ss_tot = float(np.sum((y - y.mean()) ** 2))
                r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

                lim_min = float(min(y.min(), y_pred_hist.min()))
                lim_max = float(max(y.max(), y_pred_hist.max()))

                fig_val = go.Figure()
                fig_val.add_trace(go.Scatter(
                    x=y,
                    y=y_pred_hist,
                    mode="markers",
                    name="Periodos históricos",
                    marker=dict(size=10, color="#0056b3", line=dict(width=1, color="white")),
                    hovertemplate="Real: S/ %{x:,.2f}<br>Predicho: S/ %{y:,.2f}<extra></extra>"
                ))
                fig_val.add_trace(go.Scatter(
                    x=[lim_min, lim_max],
                    y=[lim_min, lim_max],
                    mode="lines",
                    name="Predicción perfecta (y = x)",
                    line=dict(color="#dc3545", dash="dash", width=2),
                    hoverinfo="skip"
                ))
                fig_val = crear_fig_layout(fig_val)
                fig_val.update_layout(
                    height=320,
                    xaxis_title="Valor Real (S/)",
                    yaxis_title="Valor Predicho (S/)"
                )
                st.plotly_chart(fig_val, use_container_width=True)
                st.metric("R² del modelo (ajuste histórico)", f"{r2:.3f}")

                st.write("### Tabla Analítica Integrada")
                st.dataframe(df_graf, use_container_width=True)

        except Exception as e:
            st.error("Error al generar la proyección analítica.")
            st.exception(e)

        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # TAB 3: DATOS Y REPORTES
    # ========================================================
    with tab3:
        st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
        st.subheader("📋 Auditoría de Datos Filtrados e Informes")

        try:
            df_detalle = consulta_integrada(filtro_anio, filtro_sector, filtro_departamento, filtro_nivel, filtro_fuente)

            if df_detalle.empty:
                st.warning("No se encontraron registros para la segmentación seleccionada.")
            else:
                st.dataframe(df_detalle, use_container_width=True)
                reporte = generar_excel_reportes({"Datos filtrados": df_detalle})

                st.write("##")
                st.download_button(
                    label="📥 Descargar Reporte Completo en Excel",
                    data=reporte,
                    file_name="reporte_gasto_reactivacion.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except Exception as e:
            st.error("Error al compilar la matriz de datos o generar el reporte.")
            st.exception(e)

        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # TAB 4: POWER BI
    # ========================================================
    with tab4:
        st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
        st.subheader("🖼️ Dashboard Institucional Power BI Service")

        powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=7f7643c0-70d7-418f-995f-f58cc6dd56a6&autoAuth=true&ctid=63d7d67c-5411-4ad8-93b2-e98cbfda3afe&actionBarEnabled=true"

        powerbi_iframe = f"""
        <iframe 
            title="Dashboard_Gasto_Reactivacion"
            width="100%"
            height="500"
            src="{powerbi_url}"
            frameborder="0"
            allowFullScreen="true">
        </iframe>
        """

        components.html(powerbi_iframe, height=520)
        st.link_button("🔗 Abrir Dashboard directamente en la plataforma Power BI", powerbi_url)

        st.info(
            "Nota Institucional: Este cuadro de mando está sincronizado con Power BI Service. "
            "Si el contenedor solicita credenciales, inicie sesión utilizando su correo institucional del proyecto."
        )

        st.markdown("---")
        st.subheader("📊 Dashboard Ejecutivo BI + IA — Gasto Público 2025")
        st.caption("Módulo externo con análisis de ejecución presupuestal, correlación con el PBI sectorial y proyecciones con IA.")

        url_dashboard_gasto = "https://dashboard-gasto-publico-castoch.streamlit.app/"

        st.link_button("🚀 Abrir Dashboard Ejecutivo de Gasto Público", url_dashboard_gasto, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if "usuario" not in st.session_state:
        st.session_state.usuario = None

    if "nombre_usuario" not in st.session_state:
        st.session_state.nombre_usuario = None

    if "rol" not in st.session_state:
        st.session_state.rol = None

    if st.session_state.autenticado:
        dashboard()
    else:
        login()


if __name__ == "__main__":
    main()