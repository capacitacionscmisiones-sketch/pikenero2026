# INFORME EJECUTIVO
# Plan de Incorporación Kantutani - Enero 2026
# Dashboard Interactivo + Análisis de Datos

---

## 📋 RESUMEN EJECUTIVO

Este documento presenta el análisis completo del Plan de Incorporación Kantutani correspondiente a Enero 2026, incluyendo:

- ✅ Dashboard interactivo en Streamlit (web)
- 📊 Análisis de 38 asesores en capacitación
- 🎯 12 hallazgos clave basados en evidencia
- 💡 10 recomendaciones priorizadas
- ⚠️ 4 alertas de calidad de datos

**Conclusión principal:** El programa logra alta aprobación (96.3%) pero presenta desconexión entre conocimiento teórico (nota promedio 75.9) y conversión comercial (44.7% con ventas), con oportunidades claras de mejora en la ejecución práctica.

---

## 1️⃣ PERFILADO DEL ARCHIVO Y DICCIONARIO DE DATOS

### Resumen general
- **Archivo:** documento_para_CLAUDE_pik_enero_2026.xlsx
- **Hojas:** 1 (Hoja1)
- **Registros:** 38 asesores válidos
- **Columnas:** 13
- **Período:** Enero 2026

### Diccionario de datos

| Columna | Tipo | Completitud | Únicos | Descripción |
|---------|------|-------------|---------|-------------|
| N° | Numérico | 97.4% | 38 | Identificador secuencial del asesor |
| NOMBRE COMPLETO | Texto | 97.4% | 38 | Nombre y apellido del asesor |
| Equipo | Categórico | 97.4% | 11 | Equipo/agencia de pertenencia |
| Ciudad | Categórico | 97.4% | 2 | SC (Santa Cruz) o MONTERO |
| Postulando a AI/AE | Categórico | 97.4% | 2 | INTERNO o EXTERNO (inicial) |
| Ingresa como | Categórico | 69.2% | 2 | INTERNO o EXTERNO (final) |
| EQUIPO DESTINO | Categórico | 69.2% | 11 | Equipo definitivo |
| CERTIFICADO | Categórico | 69.2% | 3 | Destacado/Aprobación/Asistencia |
| NOTA | Numérico | 69.2% | 17 | Calificación 0-100 |
| Cuota Inicial | Numérico | 41.0% | 4 | % o monto de cuota inicial |
| VENTA | Numérico | 100% | 15 | Ventas en USD |
| Evaluación capacitación | Texto | 69.2% | 27 | Comentarios cualitativos |
| Observaciones finales | Texto | 97.4% | 12 | Notas del director |

### Análisis de calidad

**Completitud:**
- ✅ VENTA: 100% (sin valores faltantes)
- ✅ N° y NOMBRE: 97.4%
- ⚠️ NOTA y CERTIFICADO: 69.2% (30.8% faltante)
- ⚠️ Cuota Inicial: 41.0% (59% faltante)

**Duplicados:**
- ✅ 0 registros duplicados por nombre

**Categorías detectadas:**
- **Equipos:** PANTERAS (8), ELITE (7), RRHH (6), JAGUARES (5), AGUILAS (3), COBRAS (2), FENIX (2), KRAKEN (2), otros (4)
- **Ciudades:** SC (27), MONTERO (11)
- **Condición inicial:** INTERNO (31, 81.6%), EXTERNO (7, 18.4%)
- **Condición final:** INTERNO (15, 55.6%), EXTERNO (12, 44.4%)
- **Certificados:** Aprobación (16), Destacado (8), Asistencia (3)

**Rangos numéricos:**
- **NOTA:** Min: 59 | Max: 89 | Promedio: 75.9 | Mediana: 77
- **VENTA:** Min: $0 | Max: $49,766 | Promedio: $2,552 | Mediana: $0

---

## 2️⃣ LIMPIEZA Y NORMALIZACIÓN

### Transformaciones aplicadas

1. **Conversión de tipos:**
   - NOTA, VENTA, Cuota Inicial → numérico
   - Textos → mayúsculas, trimmed

2. **Normalización de categorías:**
   - AI/AE → INTERNO/EXTERNO

3. **Campos derivados creados:**
   - `Condición`: simplificación de tipo de asesor
   - `Cambió_Condición`: boolean (INTERNO→EXTERNO o viceversa)
   - `Rango_Nota`: Excelente (85-100), Bueno (75-84), Regular (60-74), Insuficiente (<60)
   - `Nivel_Ventas`: Alto (>$5k), Medio ($1k-$5k), Bajo (<$1k), Sin Ventas
   - `Tiene_Ventas`: boolean (ventas > 0)
   - `Aprobado`: boolean (nota ≥ 60)

### Detección de outliers (método IQR)

**NOTA:**
- Rango esperado: 62.5 - 90.5
- **Outlier detectado:** LUIS MARCELO SEAS ORTIZ (59 puntos)
- Acción: marcado, no eliminado (única reprobación)

**VENTA:**
- Rango esperado (ventas > 0): -$375 - $6,625
- **Outliers detectados:**
  - Registro sin nombre: $49,766 (extremo)
  - MARILIN PAZ ARAUZ: $8,600
- Acción: marcados para investigación cualitativa

---

## 3️⃣ DEFINICIÓN DE KPIs

### A) KPIs de volumen

| KPI | Fórmula | Valor | Unidad |
|-----|---------|-------|--------|
| Total asesores | COUNT(registros) | 38 | asesores |
| Total equipos | COUNT(DISTINCT Equipo) | 11 | equipos |
| INTERNOS | % de condición | 81.6% | porcentaje |
| EXTERNOS | % de condición | 18.4% | porcentaje |

### B) KPIs de desempeño

| KPI | Fórmula | Valor | Umbral | Estado |
|-----|---------|-------|--------|--------|
| Nota promedio | AVG(NOTA) | 75.9 | ≥80 = Excelente | 🟡 Bueno |
| Nota mediana | MEDIAN(NOTA) | 77.0 | - | - |
| Desviación estándar | STDEV(NOTA) | 6.5 | <5 = homogéneo | 🟢 Normal |

**Distribución por rango:**
- Bueno (75-84): 44.7%
- Regular (60-74): 21.1%
- Excelente (85-100): 2.6%
- Insuficiente (<60): 2.6%
- Sin Calificación: 31.6%

### C) KPIs de cumplimiento

| KPI | Fórmula | Valor | Meta | Estado |
|-----|---------|-------|------|--------|
| % Aprobados | (NOTA ≥ 60 / Total) × 100 | 96.3% | ≥90% | 🟢 Excelente |
| % Destacados | (Destacado / Total cert.) × 100 | 20.5% | ≥30% | 🟡 Límite |
| % Aprobación | (Aprobación / Total cert.) × 100 | 59.3% | - | - |

### D) KPIs de ventas

| KPI | Fórmula | Valor | Meta | Estado |
|-----|---------|-------|------|--------|
| Ventas totales | SUM(VENTA) | $99,532 | - | - |
| Venta promedio | AVG(VENTA) | $2,552 | - | ⚠️ Sesgado |
| Venta mediana | MEDIAN(VENTA) | $0 | - | ⚠️ Crítico |
| % Con ventas | (VENTA > 0 / Total) × 100 | 44.7% | ≥50% | 🟡 Bueno |
| Asesores sin ventas | COUNT(VENTA = 0) | 22 (57.9%) | - | 🔴 Alto |

**Top 5 asesores por ventas:**
1. Registro sin nombre: $49,766
2. MARILIN PAZ ARAUZ: $8,600
3. MONICA ULMIRA IRIGOYEN: $5,050
4. MEYLIND ANTELO HURTADO: $4,000
5. NAIR SUAREZ PADILLA: $4,000

### E) KPIs comparativos (INTERNO vs EXTERNO)

| Métrica | INTERNO | EXTERNO | Diferencia |
|---------|---------|---------|------------|
| Nota promedio | 75.2 | 78.5 | +3.3 (EXTERNO mejor) |
| Venta promedio | $1,328 | $1,229 | +$99 (INTERNO mejor) |
| % Con ventas | 48.4% | 14.3% | +34.1 pp (INTERNO mejor) |

### F) KPIs de conversión y retención

| KPI | Valor | Interpretación |
|-----|-------|----------------|
| Cambios de condición | 18 (66.7%) | Alto |
| INTERNO → EXTERNO | 6 | 🔴 Downgrades crítico |
| EXTERNO → INTERNO | 0 | No hay upgrades |

---

## 4️⃣ DASHBOARD INTERACTIVO

### Tecnología: Streamlit + Plotly

**Características principales:**
- ✅ Dashboard web responsive
- ✅ 5 filtros interactivos (equipo, ciudad, condición, certificado, rango nota)
- ✅ 5 KPIs en tarjetas con deltas
- ✅ 5 pestañas organizadas por temática
- ✅ 15+ gráficos interactivos (histogramas, box plots, scatter, barras, pie)
- ✅ Tabla con búsqueda y exportación CSV
- ✅ Cross-filtering entre visuales

### Estructura del dashboard

**Pestaña 1: Panorama General**
- Distribución de notas (histograma)
- Box plot de dispersión
- Distribución por rango (pie chart)
- Distribución de certificados (barras)

**Pestaña 2: Análisis por Equipo**
- Ranking de equipos por nota (barras horizontales)
- Cantidad de asesores por equipo
- Ventas promedio por equipo

**Pestaña 3: Análisis de Ventas**
- Top 10 asesores por ventas
- Distribución por nivel de ventas
- Correlación nota vs ventas (scatter + trendline)

**Pestaña 4: Comparativos**
- Box plots INTERNO vs EXTERNO (nota y ventas)
- Tabla de cambios de condición
- Métricas de upgrades/downgrades

**Pestaña 5: Datos Detallados**
- Tabla completa interactiva
- Buscador por nombre
- Exportación a CSV

### Archivos entregados

1. **app.py** - Aplicación Streamlit completa (700+ líneas)
2. **requirements.txt** - Dependencias (streamlit, pandas, plotly, openpyxl)
3. **README.md** - Instrucciones de instalación y despliegue
4. **documento_para_CLAUDE_pik_enero_2026.xlsx** - Datos fuente

### Instrucciones de despliegue

**Local:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

**Cloud (Streamlit Community Cloud):**
1. Subir archivos a repositorio GitHub
2. Conectar en https://share.streamlit.io/
3. Desplegar (2-5 minutos)
4. Obtener URL pública

---

## 5️⃣ INSIGHTS Y HALLAZGOS

### 🔍 12 Hallazgos Clave (Basados en Evidencia)

#### 1. Desempeño académico bueno pero con margen de mejora
- **Dato:** Nota promedio 75.9/100 puntos
- **Evidencia:** Mediana 77, rango 59-89
- **Impacto:** Grupo en zona "Bueno" pero no alcanza excelencia (≥80). 44.7% en rango 75-84.

#### 2. Tasa de aprobación excelente
- **Dato:** 96.3% aprobados (nota ≥ 60)
- **Evidencia:** 26 de 27 con calificación válida
- **Impacto:** Solo 1 reprobó. Sistema efectivo para aprobar pero pocos destacan.

#### 3. Conversión a ventas en zona aceptable pero mejorable
- **Dato:** 44.7% realizó al menos una venta
- **Evidencia:** 17 de 38 asesores con ventas > $0
- **Impacto:** 57.9% sin ventas. Brecha entre conocimiento (nota) y ejecución (venta).

#### 4. Alta concentración de ventas en pocos asesores
- **Dato:** Top 5 genera 71.8% del total de ventas
- **Evidencia:** $71,416 de $99,532 totales
- **Impacto:** Dependencia de pocos performers. Necesidad de nivelar capacidades.

#### 5. Outlier extremo distorsiona métricas
- **Dato:** Venta máxima $49,766
- **Evidencia:** Siguiente máximo $8,600. Diferencia de 5.8x
- **Impacto:** Promedio inflado. Mediana ($0) más representativa.

#### 6. EXTERNOS superan a INTERNOS en nota promedio
- **Dato:** EXTERNO 78.5 vs INTERNO 75.2
- **Evidencia:** Diferencia +3.3 puntos
- **Impacto:** EXTERNOS más preparados. Cuestiona criterio de asignación.

#### 7. INTERNOS convierten 3.4x más que EXTERNOS
- **Dato:** INTERNO 48.4% vs EXTERNO 14.3% con ventas
- **Evidencia:** 15 de 31 INTERNOS vs 1 de 7 EXTERNOS
- **Impacto:** EXTERNOS mejor nota pero menor conversión. Gap teoría-práctica.

#### 8. Alto porcentaje de downgrades
- **Dato:** 6 asesores (19.4% de INTERNOS) bajaron a EXTERNO
- **Evidencia:** vs 0 upgrades
- **Impacto:** Sobrestimación inicial o problemas en desarrollo del rol.

#### 9. Equipo HALCONES lidera en desempeño
- **Dato:** HALCONES 80.0 puntos promedio
- **Evidencia:** vs promedio general 75.9
- **Impacto:** Mejores prácticas replicables. Investigar factores de éxito.

#### 10. Casi un tercio sin certificado
- **Dato:** 12 asesores (31.6%) sin certificado
- **Evidencia:** vs 27 con certificado
- **Impacto:** Problema administrativo o proceso incompleto.

#### 11. Pocos alcanzan nivel Destacado
- **Dato:** 8 asesores (20.5% de certificados)
- **Evidencia:** vs 16 Aprobación (59.3%)
- **Impacto:** Sistema diferencia bien pero pocos destacan.

#### 12. Correlación débil nota-ventas
- **Dato:** Coeficiente r = -0.061
- **Evidencia:** Valor cercano a 0, sin relación lineal
- **Impacto:** Nota alta no predice ventas. Capacitación y ejecución son dimensiones distintas.

---

## 6️⃣ CONCLUSIONES EJECUTIVAS

1. **El programa logra aprobar al 96.3% pero solo 20.5% alcanza Destacado**, indicando brecha entre competencia básica y excelencia.

2. **Desconexión significativa entre desempeño académico (75.9) y conversión comercial (44.7% con ventas)**, sugiriendo que el conocimiento no se traduce en habilidades de venta.

3. **EXTERNOS obtienen mejores notas (+3.3 puntos) pero convierten menos (14.3% vs 48.4% de INTERNOS)**, indicando diferentes perfiles o necesidades de desarrollo.

4. **Alta concentración de ventas** (top 5 = 71.8% del total) y outlier extremo ($49,766) muestran que se generan algunos performers excepcionales pero no se nivela al grupo.

5. **19.4% de INTERNOS degradados a EXTERNOS sin ningún upgrade**, señalando problemas en evaluación inicial o desarrollo durante capacitación.

6. **30.8% sin certificado y correlación débil nota-ventas (r=-0.061)** apuntan a oportunidades en proceso administrativo y vínculo formación-práctica.

7. **Variabilidad significativa entre equipos** (rango 74.0-80.0) sugiere que liderazgo, cultura y recursos influyen más allá de capacidades individuales.

---

## 7️⃣ RECOMENDACIONES ACCIONABLES

### 🔴 ALTO IMPACTO / BAJA DIFICULTAD (Implementar inmediatamente)

#### 1. Cerrar brechas administrativas
- **Acción:** Asignar certificados a 12 asesores pendientes (30.8%)
- **Responsable:** RRHH / Administración
- **Plazo:** 1 semana

#### 2. Bootcamp comercial para EXTERNOS
- **Acción:** Programa intensivo 2 semanas (solo 1/7 vendió)
- **Enfoque:** Cierre, objeciones, práctica de campo
- **Responsable:** Capacitación + Gerente Comercial
- **Plazo:** 2-4 semanas

#### 3. Documentar mejores prácticas del top 5
- **Acción:** Entrevistar top performers, crear kit de herramientas
- **Entregable:** Manual de técnicas, argumentos, proceso
- **Responsable:** Capacitación + Top performers
- **Plazo:** 2 semanas

#### 4. Revisar proceso de asignación INTERNO/EXTERNO
- **Acción:** Refinar criterios (6 downgrades, 0 upgrades)
- **Responsable:** Director + RRHH
- **Plazo:** 3 semanas

---

### 🟡 ALTO IMPACTO / MEDIA DIFICULTAD (Planificar próximo ciclo)

#### 5. Coaching diferenciado por perfil
- **Track 1 EXTERNOS:** Refuerzo en ejecución comercial práctica
- **Track 2 INTERNOS:** Refuerzo en fundamentos técnicos
- **Responsable:** Capacitación
- **Plazo:** 1-2 meses

#### 6. Sistema de mentorías cruzadas
- **Acción:** Emparejar 22 sin ventas con 17 que sí vendieron
- **Frecuencia:** 1 sesión/semana × 4 semanas
- **Responsable:** Gerente Comercial + Coordinadores
- **Plazo:** 1 mes

#### 7. Rediseñar módulo de práctica comercial
- **Acción:** Incrementar role-play, simulaciones, campo
- **Justificación:** Correlación débil nota-ventas
- **Responsable:** Capacitación + Diseño Instruccional
- **Plazo:** 2 meses

#### 8. Benchmark entre equipos
- **Acción:** Sesión mensual de compartir estrategias
- **Teams:** HALCONES, LEONES, AGUILAS (top) → resto
- **Responsable:** Directores de equipo
- **Plazo:** 1 mes (recurrente)

---

### 🔵 MEDIO IMPACTO / SEGUIMIENTO CONTINUO

#### 9. Dashboard en tiempo real
- **Acción:** Actualización semanal, alertas automáticas
- **Responsable:** BI / IT
- **Plazo:** Implementado (mantener)

#### 10. Investigación cualitativa del outlier $49,766
- **Acción:** Entender qué hizo diferente
- **Objetivo:** Replicar si posible, ajustar expectativas si único
- **Responsable:** Gerente Comercial
- **Plazo:** 1 semana

---

## 8️⃣ ALERTAS DE CALIDAD DE DATOS

⚠️ **1. 30.8% sin certificado asignado**
→ Seguimiento administrativo urgente

⚠️ **2. 1 registro sin nombre (NAN) con ventas de $49,766**
→ Identificar y corregir en base de datos

⚠️ **3. 30.8% de notas faltantes**
→ Verificar si no completaron evaluación o error de captura

⚠️ **4. Correlación débil NOTA-VENTA (r=-0.061)**
→ Métricas de evaluación no predicen éxito comercial

---

## 9️⃣ MATRIZ DE PRIORIZACIÓN

```
┌─────────────────────────┬──────────────────┬──────────────────┐
│                         │  Baja Dificultad │ Media Dificultad │
├─────────────────────────┼──────────────────┼──────────────────┤
│ Alto Impacto            │ IMPLEMENTAR YA   │ PLANIFICAR       │
│                         │ • Cerrar gaps    │ • Coaching       │
│                         │   admin (1 sem)  │   diferenciado   │
│                         │ • Bootcamp       │   (1-2 meses)    │
│                         │   EXTERNOS       │ • Mentorías      │
│                         │   (2-4 sem)      │   (1 mes)        │
│                         │ • Documentar     │ • Rediseño       │
│                         │   mejores        │   módulo         │
│                         │   prácticas      │   (2 meses)      │
│                         │   (2 sem)        │ • Benchmark      │
│                         │ • Revisar        │   equipos        │
│                         │   asignación     │   (1 mes, recur) │
│                         │   (3 sem)        │                  │
├─────────────────────────┼──────────────────┼──────────────────┤
│ Medio Impacto           │ SEGUIMIENTO      │                  │
│                         │ • Dashboard RT   │                  │
│                         │ • Investigar     │                  │
│                         │   outlier        │                  │
└─────────────────────────┴──────────────────┴──────────────────┘
```

---

## 🔟 MODELO DE DATOS (ESTRELLA)

### Tabla de hechos: fact_asesores_capacitacion
- **Granularidad:** 1 fila por asesor
- **Métricas:**
  - NOTA (calificación)
  - VENTA (monto USD)
  - Cuota_Inicial (porcentaje/monto)
- **Llaves foráneas:**
  - asesor_id → dim_asesor
  - equipo_id → dim_equipo
  - ciudad_id → dim_ciudad
  - certificado_id → dim_certificado

### Dimensiones

**dim_asesor:**
- asesor_id (PK)
- nombre_completo
- condicion_postulacion (INTERNO/EXTERNO)
- condicion_final (INTERNO/EXTERNO)
- cambio_condicion (Sí/No)

**dim_equipo:**
- equipo_id (PK)
- nombre_equipo
- cantidad_asesores

**dim_ciudad:**
- ciudad_id (PK)
- nombre_ciudad (SC/MONTERO)

**dim_certificado:**
- certificado_id (PK)
- nivel_certificado (Destacado/Aprobación/Asistencia)

---

## 📁 ARCHIVOS ENTREGABLES

### Carpeta principal: /mnt/user-data/outputs/

1. **app.py** (8.5 KB)
   - Dashboard Streamlit completo
   - 5 pestañas, 15+ visualizaciones
   - Filtros interactivos, exportación CSV

2. **requirements.txt** (0.1 KB)
   - streamlit==1.31.0
   - pandas==2.2.0
   - plotly==5.18.0
   - openpyxl==3.1.2

3. **README.md** (6 KB)
   - Instrucciones de instalación local
   - Guía de despliegue en Streamlit Cloud
   - Documentación de uso
   - Solución de problemas

4. **documento_para_CLAUDE_pik_enero_2026.xlsx** (original)
   - Datos fuente

5. **INFORME_EJECUTIVO.md** (este archivo)
   - Análisis completo
   - Insights y recomendaciones
   - Documentación técnica

---

## 📞 CONTACTO Y SOPORTE

Para desplegar el dashboard o consultas sobre el análisis:
- Seguir instrucciones en README.md
- Documentación Streamlit: https://docs.streamlit.io
- Verificar dependencias instaladas correctamente

---

**Fecha de generación:** Febrero 2, 2026  
**Herramienta:** Claude (Anthropic) + Python + Streamlit + Plotly  
**Autor:** Análisis BI automatizado  
**Versión:** 1.0
