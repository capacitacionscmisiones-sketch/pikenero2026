import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Plan de Incorporación Kantutani",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.2rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data
def load_data():
    """Carga y procesa el archivo Excel"""
    try:
        # Leer el archivo
        df = pd.read_excel('documento_para_CLAUDE_pik_enero_2026.xlsx', 
                          sheet_name='Hoja1', skiprows=1)
        
        # Usar primera fila como headers
        new_headers = df.iloc[0].values
        df = df.iloc[1:].copy()
        df.columns = new_headers
        df = df.reset_index(drop=True)
        
        # Limpieza y conversión de tipos
        df['NOTA'] = pd.to_numeric(df['NOTA'], errors='coerce')
        df['VENTA'] = pd.to_numeric(df['VENTA'], errors='coerce').fillna(0)
        df['Cuota Inicial'] = pd.to_numeric(df['Cuota Inicial'], errors='coerce')
        df['N°'] = pd.to_numeric(df['N°'], errors='coerce').fillna(0).astype(int)
        
        # Normalizar textos
        text_cols = ['NOMBRE COMPLETO', 'Equipo', 'Ciudad', 
                     'Postulando a Asesor Interno (AI) / Asesor Externo (AE)',
                     'Al final del proceso ingresa como:', 'EQUIPO DESTINO', 'CERTIFICADO']
        
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper()
        
        # Normalizar categorías
        df['Postulando a Asesor Interno (AI) / Asesor Externo (AE)'] = \
            df['Postulando a Asesor Interno (AI) / Asesor Externo (AE)'].replace({
                'AI': 'INTERNO', 'AE': 'EXTERNO'
            })
        
        df['Al final del proceso ingresa como:'] = \
            df['Al final del proceso ingresa como:'].replace({
                'AI': 'INTERNO', 'AE': 'EXTERNO', 'NAN': np.nan
            })
        
        # Campos derivados
        df['Condición'] = df['Postulando a Asesor Interno (AI) / Asesor Externo (AE)']
        
        df['Cambió_Condición'] = (
            df['Postulando a Asesor Interno (AI) / Asesor Externo (AE)'] != 
            df['Al final del proceso ingresa como:']
        ).fillna(False)
        
        # Clasificación de nota
        def clasificar_nota(nota):
            if pd.isna(nota):
                return 'Sin Calificación'
            elif nota >= 85:
                return 'Excelente (85-100)'
            elif nota >= 75:
                return 'Bueno (75-84)'
            elif nota >= 60:
                return 'Regular (60-74)'
            else:
                return 'Insuficiente (<60)'
        
        df['Rango_Nota'] = df['NOTA'].apply(clasificar_nota)
        
        # Clasificación de ventas
        def clasificar_ventas(venta):
            if pd.isna(venta) or venta == 0:
                return 'Sin Ventas'
            elif venta < 1000:
                return 'Bajo (<$1k)'
            elif venta < 5000:
                return 'Medio ($1k-$5k)'
            else:
                return 'Alto (>$5k)'
        
        df['Nivel_Ventas'] = df['VENTA'].apply(clasificar_ventas)
        
        df['Tiene_Ventas'] = df['VENTA'] > 0
        df['Aprobado'] = df['NOTA'] >= 60
        
        # Filtrar registros válidos
        df = df[df['NOMBRE COMPLETO'] != 'NAN'].copy()
        
        return df
        
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return None

# Cargar datos
df = load_data()

if df is not None:
    # Header
    st.markdown('<div class="main-header">📊 Dashboard Plan de Incorporación Kantutani</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Análisis de Capacitación y Desempeño - Enero 2026</div>', 
                unsafe_allow_html=True)
    
    # Sidebar - Filtros
    st.sidebar.header("🎯 Filtros")
    
    # Filtro por equipo
    equipos = ['TODOS'] + sorted([e for e in df['Equipo'].unique() if e != 'NAN'])
    equipo_seleccionado = st.sidebar.selectbox("Equipo", equipos)
    
    # Filtro por ciudad
    ciudades = ['TODAS'] + sorted([c for c in df['Ciudad'].unique() if c != 'NAN'])
    ciudad_seleccionada = st.sidebar.selectbox("Ciudad", ciudades)
    
    # Filtro por condición
    condiciones = ['TODAS', 'INTERNO', 'EXTERNO']
    condicion_seleccionada = st.sidebar.selectbox("Condición", condiciones)
    
    # Filtro por certificado
    certificados = ['TODOS'] + sorted([c for c in df['CERTIFICADO'].unique() if c != 'NAN'])
    certificado_seleccionado = st.sidebar.selectbox("Certificado", certificados)
    
    # Filtro por rango de nota
    rango_nota = st.sidebar.slider(
        "Rango de nota",
        min_value=int(df['NOTA'].min()) if not df['NOTA'].isna().all() else 0,
        max_value=int(df['NOTA'].max()) if not df['NOTA'].isna().all() else 100,
        value=(int(df['NOTA'].min()) if not df['NOTA'].isna().all() else 0, 
               int(df['NOTA'].max()) if not df['NOTA'].isna().all() else 100)
    )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if equipo_seleccionado != 'TODOS':
        df_filtrado = df_filtrado[df_filtrado['Equipo'] == equipo_seleccionado]
    
    if ciudad_seleccionada != 'TODAS':
        df_filtrado = df_filtrado[df_filtrado['Ciudad'] == ciudad_seleccionada]
    
    if condicion_seleccionada != 'TODAS':
        df_filtrado = df_filtrado[df_filtrado['Condición'] == condicion_seleccionada]
    
    if certificado_seleccionado != 'TODOS':
        df_filtrado = df_filtrado[df_filtrado['CERTIFICADO'] == certificado_seleccionado]
    
    df_filtrado = df_filtrado[
        (df_filtrado['NOTA'] >= rango_nota[0]) & 
        (df_filtrado['NOTA'] <= rango_nota[1])
    ]
    
    # KPIs principales
    st.markdown("### 📈 Indicadores Clave")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_asesores = len(df_filtrado)
        st.metric("Total Asesores", f"{total_asesores}", 
                 delta=f"{total_asesores - len(df)} vs total" if total_asesores != len(df) else None)
    
    with col2:
        promedio_nota = df_filtrado['NOTA'].mean()
        st.metric("Nota Promedio", f"{promedio_nota:.1f}", 
                 delta=f"{promedio_nota - df['NOTA'].mean():.1f}" if promedio_nota != df['NOTA'].mean() else None)
    
    with col3:
        pct_aprobados = (df_filtrado['Aprobado'].sum() / len(df_filtrado['NOTA'].dropna()) * 100) \
                        if len(df_filtrado['NOTA'].dropna()) > 0 else 0
        st.metric("% Aprobados", f"{pct_aprobados:.1f}%")
    
    with col4:
        total_ventas = df_filtrado['VENTA'].sum()
        st.metric("Ventas Totales", f"${total_ventas:,.0f}")
    
    with col5:
        pct_con_ventas = (df_filtrado['Tiene_Ventas'].sum() / len(df_filtrado) * 100) \
                         if len(df_filtrado) > 0 else 0
        st.metric("% Con Ventas", f"{pct_con_ventas:.1f}%")
    
    st.markdown("---")
    
    # Tabs para organizar visualizaciones
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Panorama General", 
        "👥 Análisis por Equipo",
        "💰 Análisis de Ventas",
        "🎯 Comparativos",
        "📋 Datos Detallados"
    ])
    
    with tab1:
        st.markdown("### Panorama general de desempeño")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución de notas
            fig_dist = px.histogram(
                df_filtrado[df_filtrado['NOTA'].notna()],
                x='NOTA',
                nbins=20,
                title='Distribución de notas',
                labels={'NOTA': 'Nota', 'count': 'Frecuencia'},
                color_discrete_sequence=['#1f77b4']
            )
            fig_dist.update_layout(
                showlegend=False,
                xaxis_title='Nota',
                yaxis_title='Cantidad de asesores'
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            # Box plot de notas
            fig_box = px.box(
                df_filtrado[df_filtrado['NOTA'].notna()],
                y='NOTA',
                title='Dispersión de notas (Box Plot)',
                labels={'NOTA': 'Nota'},
                color_discrete_sequence=['#1f77b4']
            )
            fig_box.update_layout(showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Distribución por rango de nota
            rango_counts = df_filtrado['Rango_Nota'].value_counts()
            fig_rango = px.pie(
                values=rango_counts.values,
                names=rango_counts.index,
                title='Distribución por rango de nota',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_rango, use_container_width=True)
        
        with col4:
            # Distribución de certificados
            cert_counts = df_filtrado[df_filtrado['CERTIFICADO'] != 'NAN']['CERTIFICADO'].value_counts()
            fig_cert = px.bar(
                x=cert_counts.index,
                y=cert_counts.values,
                title='Distribución de certificados',
                labels={'x': 'Tipo de Certificado', 'y': 'Cantidad'},
                color=cert_counts.index,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_cert.update_layout(showlegend=False)
            st.plotly_chart(fig_cert, use_container_width=True)
    
    with tab2:
        st.markdown("### Análisis de desempeño por equipo")
        
        # Ranking de equipos por nota promedio
        equipos_nota = df_filtrado.groupby('Equipo')['NOTA'].agg(['mean', 'count']).reset_index()
        equipos_nota = equipos_nota[equipos_nota['Equipo'] != 'NAN'].sort_values('mean', ascending=True)
        
        fig_equipos_nota = px.bar(
            equipos_nota,
            y='Equipo',
            x='mean',
            title='Ranking de equipos por nota promedio',
            labels={'mean': 'Nota Promedio', 'Equipo': ''},
            orientation='h',
            text=equipos_nota['mean'].apply(lambda x: f'{x:.1f}'),
            color='mean',
            color_continuous_scale='Blues'
        )
        fig_equipos_nota.update_traces(textposition='outside')
        fig_equipos_nota.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_equipos_nota, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cantidad de asesores por equipo
            equipo_counts = df_filtrado['Equipo'].value_counts()
            equipo_counts = equipo_counts[equipo_counts.index != 'NAN']
            
            fig_equipo_count = px.bar(
                x=equipo_counts.values,
                y=equipo_counts.index,
                title='Cantidad de asesores por equipo',
                labels={'x': 'Cantidad', 'y': 'Equipo'},
                orientation='h',
                color_discrete_sequence=['#2ca02c']
            )
            st.plotly_chart(fig_equipo_count, use_container_width=True)
        
        with col2:
            # Promedio de ventas por equipo
            equipos_venta = df_filtrado.groupby('Equipo')['VENTA'].mean().reset_index()
            equipos_venta = equipos_venta[equipos_venta['Equipo'] != 'NAN'].sort_values('VENTA', ascending=False)
            
            fig_equipo_venta = px.bar(
                equipos_venta,
                x='Equipo',
                y='VENTA',
                title='Ventas promedio por equipo',
                labels={'VENTA': 'Venta Promedio ($)', 'Equipo': ''},
                color_discrete_sequence=['#ff7f0e']
            )
            fig_equipo_venta.update_xaxis(tickangle=45)
            st.plotly_chart(fig_equipo_venta, use_container_width=True)
    
    with tab3:
        st.markdown("### Análisis de ventas y conversión")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 asesores por ventas
            top_ventas = df_filtrado.nlargest(10, 'VENTA')[['NOMBRE COMPLETO', 'VENTA', 'NOTA']]
            
            fig_top_ventas = px.bar(
                top_ventas,
                y='NOMBRE COMPLETO',
                x='VENTA',
                title='Top 10 asesores por ventas',
                labels={'VENTA': 'Ventas ($)', 'NOMBRE COMPLETO': ''},
                orientation='h',
                text=top_ventas['VENTA'].apply(lambda x: f'${x:,.0f}'),
                color='VENTA',
                color_continuous_scale='Greens'
            )
            fig_top_ventas.update_traces(textposition='outside')
            fig_top_ventas.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_top_ventas, use_container_width=True)
        
        with col2:
            # Distribución de ventas por nivel
            nivel_counts = df_filtrado['Nivel_Ventas'].value_counts()
            
            fig_nivel = px.pie(
                values=nivel_counts.values,
                names=nivel_counts.index,
                title='Distribución de asesores por nivel de ventas',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_nivel, use_container_width=True)
        
        # Relación nota vs ventas
        fig_scatter = px.scatter(
            df_filtrado[df_filtrado['NOTA'].notna()],
            x='NOTA',
            y='VENTA',
            title='Relación entre nota y ventas',
            labels={'NOTA': 'Nota', 'VENTA': 'Ventas ($)'},
            color='Condición',
            size='VENTA',
            hover_data=['NOMBRE COMPLETO', 'Equipo'],
            trendline='ols'
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Calcular correlación
        correlacion = df_filtrado[['NOTA', 'VENTA']].corr().iloc[0, 1]
        st.info(f"**Correlación Nota-Ventas:** {correlacion:.3f}")
    
    with tab4:
        st.markdown("### Comparativos INTERNO vs EXTERNO")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Comparación de notas
            fig_comp_nota = px.box(
                df_filtrado[df_filtrado['NOTA'].notna()],
                x='Condición',
                y='NOTA',
                title='Comparación de notas: INTERNO vs EXTERNO',
                labels={'Condición': 'Condición', 'NOTA': 'Nota'},
                color='Condición',
                color_discrete_map={'INTERNO': '#1f77b4', 'EXTERNO': '#ff7f0e'}
            )
            st.plotly_chart(fig_comp_nota, use_container_width=True)
            
            # Estadísticas
            for cond in ['INTERNO', 'EXTERNO']:
                subset = df_filtrado[df_filtrado['Condición'] == cond]['NOTA']
                if len(subset) > 0:
                    st.write(f"**{cond}:** Promedio = {subset.mean():.1f}, Mediana = {subset.median():.0f}")
        
        with col2:
            # Comparación de ventas
            fig_comp_venta = px.box(
                df_filtrado,
                x='Condición',
                y='VENTA',
                title='Comparación de ventas: INTERNO vs EXTERNO',
                labels={'Condición': 'Condición', 'VENTA': 'Ventas ($)'},
                color='Condición',
                color_discrete_map={'INTERNO': '#1f77b4', 'EXTERNO': '#ff7f0e'}
            )
            st.plotly_chart(fig_comp_venta, use_container_width=True)
            
            # Estadísticas
            for cond in ['INTERNO', 'EXTERNO']:
                subset = df_filtrado[df_filtrado['Condición'] == cond]
                if len(subset) > 0:
                    pct_ventas = (subset['Tiene_Ventas'].sum() / len(subset)) * 100
                    st.write(f"**{cond}:** {pct_ventas:.1f}% con ventas, Promedio = ${subset['VENTA'].mean():,.0f}")
        
        # Tabla de cambios de condición
        st.markdown("#### Cambios de condición")
        cambios_df = df_filtrado[df_filtrado['Cambió_Condición'] == True][[
            'NOMBRE COMPLETO', 
            'Postulando a Asesor Interno (AI) / Asesor Externo (AE)', 
            'Al final del proceso ingresa como:',
            'NOTA',
            'VENTA'
        ]]
        cambios_df.columns = ['Asesor', 'Condición Inicial', 'Condición Final', 'Nota', 'Ventas']
        st.dataframe(cambios_df, use_container_width=True, height=300)
        
        col1, col2 = st.columns(2)
        with col1:
            interno_a_externo = len(df_filtrado[
                (df_filtrado['Condición'] == 'INTERNO') & 
                (df_filtrado['Al final del proceso ingresa como:'] == 'EXTERNO')
            ])
            st.metric("INTERNO → EXTERNO (downgrade)", interno_a_externo)
        
        with col2:
            externo_a_interno = len(df_filtrado[
                (df_filtrado['Condición'] == 'EXTERNO') & 
                (df_filtrado['Al final del proceso ingresa como:'] == 'INTERNO')
            ])
            st.metric("EXTERNO → INTERNO (upgrade)", externo_a_interno)
    
    with tab5:
        st.markdown("### Tabla de datos completa")
        
        # Preparar columnas para mostrar
        columnas_mostrar = [
            'N°', 'NOMBRE COMPLETO', 'Equipo', 'Ciudad', 'Condición',
            'Al final del proceso ingresa como:', 'CERTIFICADO', 'NOTA',
            'VENTA', 'Rango_Nota', 'Nivel_Ventas'
        ]
        
        df_mostrar = df_filtrado[columnas_mostrar].copy()
        df_mostrar.columns = [
            'N°', 'Nombre Completo', 'Equipo', 'Ciudad', 'Condición Inicial',
            'Condición Final', 'Certificado', 'Nota', 'Ventas ($)', 
            'Rango Nota', 'Nivel Ventas'
        ]
        
        # Buscador
        busqueda = st.text_input("🔍 Buscar por nombre del asesor")
        if busqueda:
            df_mostrar = df_mostrar[
                df_mostrar['Nombre Completo'].str.contains(busqueda.upper(), na=False)
            ]
        
        st.dataframe(
            df_mostrar.style.format({
                'Nota': '{:.1f}',
                'Ventas ($)': '${:,.2f}'
            }),
            use_container_width=True,
            height=500
        )
        
        # Botón de descarga
        csv = df_mostrar.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar datos filtrados (CSV)",
            data=csv,
            file_name='datos_filtrados_kantutani.csv',
            mime='text/csv'
        )
    
    # Footer con estadísticas resumidas
    st.markdown("---")
    st.markdown("### 📊 Resumen estadístico")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Desviación estándar (Nota)", f"{df_filtrado['NOTA'].std():.2f}")
    
    with col2:
        st.metric("Mediana de nota", f"{df_filtrado['NOTA'].median():.0f}")
    
    with col3:
        st.metric("Venta mediana", f"${df_filtrado['VENTA'].median():,.0f}")
    
    with col4:
        st.metric("Total equipos", df_filtrado['Equipo'].nunique())

else:
    st.error("No se pudieron cargar los datos. Verifica que el archivo Excel esté en el directorio correcto.")
