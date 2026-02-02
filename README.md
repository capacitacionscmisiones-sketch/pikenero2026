# Dashboard Plan de Incorporación Kantutani 📊

Dashboard interactivo para análisis de capacitación y desempeño de asesores - Enero 2026

## 📋 Descripción

Este dashboard proporciona análisis completo del Plan de Incorporación Kantutani, incluyendo:

- **KPIs principales**: Total de asesores, notas promedio, % aprobación, ventas totales
- **Análisis de desempeño**: Distribución de notas, rankings por equipo
- **Análisis de ventas**: Top performers, conversión, correlaciones
- **Comparativos**: INTERNO vs EXTERNO en notas y ventas
- **Filtros interactivos**: Por equipo, ciudad, condición, certificado, rango de nota
- **Tabla detallada**: Con búsqueda y exportación a CSV

## 🚀 Instalación Local

### Requisitos previos
- Python 3.8 o superior
- pip

### Pasos de instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Verificar archivos:**
Asegúrate de tener estos archivos en el mismo directorio:
- `app.py` (aplicación principal)
- `requirements.txt` (dependencias)
- `documento_para_CLAUDE_pik_enero_2026.xlsx` (datos fuente)

3. **Ejecutar la aplicación:**
```bash
streamlit run app.py
```

4. **Abrir en navegador:**
La aplicación se abrirá automáticamente en `http://localhost:8501`

## ☁️ Despliegue en Streamlit Community Cloud

### Opción 1: Desde GitHub (Recomendado)

1. **Crear repositorio en GitHub:**
   - Ve a https://github.com/new
   - Crea un nuevo repositorio público
   - Sube los archivos: `app.py`, `requirements.txt`, `documento_para_CLAUDE_pik_enero_2026.xlsx`

2. **Conectar con Streamlit Cloud:**
   - Ve a https://share.streamlit.io/
   - Haz clic en "New app"
   - Conecta tu cuenta de GitHub
   - Selecciona tu repositorio
   - Branch: `main`
   - Main file path: `app.py`
   - Haz clic en "Deploy"

3. **Esperar despliegue:**
   - El despliegue toma 2-5 minutos
   - Recibirás una URL pública (ej: https://tu-app.streamlit.app)

### Opción 2: Desde archivos locales

1. **Comprimir archivos:**
```bash
zip dashboard_kantutani.zip app.py requirements.txt documento_para_CLAUDE_pik_enero_2026.xlsx
```

2. **Subir a GitHub:**
   - Crea un repositorio en GitHub
   - Usa GitHub web interface para subir el ZIP
   - Extrae los archivos

3. **Seguir pasos de despliegue de Opción 1**

## 🔧 Solución de Problemas

### Error: "No module named 'streamlit'"
```bash
pip install streamlit
```

### Error: "FileNotFoundError: documento_para_CLAUDE_pik_enero_2026.xlsx"
Asegúrate de que el archivo Excel esté en el mismo directorio que `app.py`

### Error de memoria en Streamlit Cloud
Si el archivo Excel es muy grande, considera:
- Usar formato Parquet en lugar de Excel
- Pre-procesar los datos y guardar solo lo necesario

### Dashboard no se actualiza
Limpia el caché de Streamlit:
1. En el menú de la app (arriba derecha)
2. Selecciona "Clear cache"
3. Refresca la página

## 📊 Uso del Dashboard

### Filtros disponibles:
- **Equipo**: Filtra por equipo/agencia específico
- **Ciudad**: SC o MONTERO
- **Condición**: INTERNO, EXTERNO o ambos
- **Certificado**: Destacado, Aprobación, Asistencia
- **Rango de nota**: Slider para filtrar por rango de calificación

### Pestañas:

1. **📊 Panorama General**
   - Distribución de notas (histograma y box plot)
   - Clasificación por rangos
   - Distribución de certificados

2. **👥 Análisis por Equipo**
   - Ranking de equipos por nota promedio
   - Cantidad de asesores por equipo
   - Ventas promedio por equipo

3. **💰 Análisis de Ventas**
   - Top 10 asesores por ventas
   - Distribución por niveles de venta
   - Correlación nota vs ventas (scatter plot con línea de tendencia)

4. **🎯 Comparativos**
   - INTERNO vs EXTERNO en notas (box plots)
   - INTERNO vs EXTERNO en ventas
   - Tabla de cambios de condición
   - Métricas de upgrades/downgrades

5. **📋 Datos Detallados**
   - Tabla completa con todos los registros
   - Buscador por nombre
   - Exportación a CSV

### Exportar datos:
En la pestaña "Datos Detallados", usa el botón "📥 Descargar datos filtrados (CSV)" para exportar los datos con los filtros aplicados.

## 📈 Métricas y KPIs

### KPIs Principales:
- **Total Asesores**: Cantidad de asesores en el programa
- **Nota Promedio**: Calificación promedio del grupo
- **% Aprobados**: Porcentaje con nota ≥ 60
- **Ventas Totales**: Suma de todas las ventas en USD
- **% Con Ventas**: Porcentaje de asesores que realizaron ventas

### Umbrales de interpretación:

**Nota Promedio:**
- ≥ 80: Excelente
- 70-79: Bueno ✓
- 60-69: Regular
- < 60: Deficiente

**% Aprobación:**
- ≥ 90%: Excelente ✓
- 80-89%: Bueno
- 70-79%: Regular
- < 70%: Crítico

**% Con Ventas:**
- ≥ 50%: Excelente
- 30-49%: Bueno ✓
- < 30%: Bajo

## 🔄 Actualización de Datos

Para actualizar con nuevos datos:

1. **Reemplazar archivo Excel:**
   - El nuevo archivo debe tener el mismo nombre: `documento_para_CLAUDE_pik_enero_2026.xlsx`
   - O actualizar el nombre en `app.py` línea 71

2. **Formato esperado:**
   - Hoja llamada "Hoja1"
   - Primera fila: fecha (se omite)
   - Segunda fila: encabezados de columna
   - Columnas requeridas: N°, NOMBRE COMPLETO, Equipo, Ciudad, Condición, NOTA, VENTA, etc.

3. **Reiniciar aplicación:**
   - Si es local: detener y volver a ejecutar `streamlit run app.py`
   - Si es Streamlit Cloud: hacer commit y push al repositorio

## 📞 Soporte

Para problemas técnicos o sugerencias:
- Revisa la documentación de Streamlit: https://docs.streamlit.io
- Verifica que todas las dependencias estén instaladas correctamente
- Asegúrate de que el archivo Excel tenga el formato correcto

## 📝 Notas Técnicas

- **Caché de datos**: La aplicación usa `@st.cache_data` para mejorar el rendimiento
- **Formato de moneda**: USD ($)
- **Visualizaciones**: Plotly para gráficos interactivos
- **Responsive**: Se adapta a diferentes tamaños de pantalla

## 🎯 Próximos Pasos Recomendados

1. Agregar filtro por fecha si hay datos históricos
2. Implementar comparación entre períodos
3. Agregar alertas automáticas para KPIs fuera de umbral
4. Exportar reportes en PDF
5. Integrar con base de datos para actualización automática
