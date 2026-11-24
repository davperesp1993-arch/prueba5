import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Simulador Cable Preensamblado 2x50+1x50",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Simulador de Producción: Cable Preensamblado")
st.subheader("CABLE PREENSAMBLADO ASC - AAAC 2 X 50 + 1 X 50 MM2 | Actual vs. Compactado")
st.markdown("Ingresa el metraje a fabricar y ajusta recetas, tiempos por proceso y costos indirectos en vivo.")
st.divider()

# 1. PANEL LATERAL: VOLUMEN Y COSTOS BASE
st.sidebar.header("📏 1. Orden de Producción")
metros = st.sidebar.number_input(
    "Cantidad a fabricar (Metros):",
    min_value=1,
    max_value=1000000,
    value=1000,
    step=100
)
km = metros / 1000.0
st.sidebar.caption(f"Equivalente a: **{km:,.3f} km**")

st.sidebar.divider()
st.sidebar.header("💲 2. Costos de Materia Prima ($/kg)")
costo_al_1350 = st.sidebar.number_input(
    "ALAMBRE DE ALUMINIO 1350 9.50 MM H14 ($/kg):",
    min_value=0.0,
    value=4.2700,
    step=0.01,
    format="%.4f"
)
costo_al_6201 = st.sidebar.number_input(
    "ALAMBRE DE ALUMINIO 6201 3.00 MM ($/kg):",
    min_value=0.0,
    value=5.2416,
    step=0.01,
    format="%.4f"
)
costo_xlpe = st.sidebar.number_input(
    "XLPE NEG ($/kg):",
    min_value=0.0,
    value=2.2865,
    step=0.01,
    format="%.4f"
)

# 2. CONFIGURACIÓN DE RECETAS DE MATERIA PRIMA
with st.expander("📦 Ver / Editar Recetas de Materia Prima (kg/km)", expanded=False):
    df_recetas = pd.DataFrame([
        {"Componente": "Fase ASC (x2) - Al 1350", "Actual (kg/km)": 135.97, "Compactado (kg/km)": 135.97},
        {"Componente": "Fase ASC (x2) - XLPE NEG", "Actual (kg/km)": 53.60, "Compactado (kg/km)": 41.00},
        {"Componente": "Neutro AAAC (x1) - Al 6201", "Actual (kg/km)": 134.17, "Compactado (kg/km)": 134.17},
        {"Componente": "Neutro AAAC (x1) - XLPE NEG", "Actual (kg/km)": 53.73, "Compactado (kg/km)": 53.73},
    ])
    recetas_edit = st.data_editor(df_recetas, hide_index=True, use_container_width=True)

# 3. ESTRUCTURA DE PESTAÑAS
tab1, tab2, tab3, tab4 = st.tabs([
    "🏭 Tiempos y Costos Indirectos (Modificable)",
    "⏱️ Comparativa Tiempos y Costos Totales",
    "📋 Comparativa Materia Prima", 
    "📈 Gráficos Ejecutivos"
])

# PESTAÑA 1: CONFIGURACIÓN MODIFICABLE DE TIEMPOS Y COSTOS POR PROCESO
with tab1:
    st.markdown("### ⏱️ 1. Tiempos Modificables por Proceso: Actual vs. Compactado (hrs/km)")
    st.markdown("Edita los tiempos de máquina (`hrs/km`) para cada escenario. Usa el **Multiplicador** si el proceso se ejecuta varias veces (ej. `2` para las 2 fases, `3` para 3 conductores).")
    
    df_tiempos_base = pd.DataFrame([
        {"Proceso": "Trefilado", "Actual (hrs/km)": 0.45, "Compactado (hrs/km)": 0.45, "Multiplicador": 2, "Detalle / Alcance": "Trefilado de conductores de fase"},
        {"Proceso": "Cableado", "Actual (hrs/km)": 0.80, "Compactado (hrs/km)": 0.90, "Multiplicador": 2, "Detalle / Alcance": "Cableado normal vs. compactado en fases"},
        {"Proceso": "Extrusado", "Actual (hrs/km)": 1.10, "Compactado (hrs/km)": 0.95, "Multiplicador": 3, "Detalle / Alcance": "Aislamiento XLPE (2 fases + 1 neutro)"},
        {"Proceso": "Trenzado", "Actual (hrs/km)": 0.90, "Compactado (hrs/km)": 0.85, "Multiplicador": 1, "Detalle / Alcance": "Reunido / Preensamblado final del haz"},
    ])
    
    tiempos_edit = st.data_editor(
        df_tiempos_base,
        use_container_width=True,
        hide_index=True,
        disabled=["Proceso"],
        column_config={
            "Proceso": st.column_config.TextColumn("Proceso"),
            "Actual (hrs/km)": st.column_config.NumberColumn("Tiempo Actual (hrs/km)", min_value=0.0, format="%.2f", required=True),
            "Compactado (hrs/km)": st.column_config.NumberColumn("Tiempo Compactado (hrs/km)", min_value=0.0, format="%.2f", required=True),
            "Multiplicador": st.column_config.NumberColumn("Pasadas / Multiplicador", min_value=1, step=1, required=True),
            "Detalle / Alcance": st.column_config.TextColumn("Observación")
        }
    )

    st.divider()
    st.markdown("### 🏭 2. Costos Indirectos y Mano de Obra por Proceso ($/Hora-Máquina)")
    st.markdown("Edita los valores por hora para cada proceso. La columna **Total ($/hr)** se suma automáticamente.")
    
    df_procesos_base = pd.DataFrame([
        {
            "Proceso": "Trefilado",
            "Costo Mano de Obra Directa": 12.00,
            "Costo Mano de Obra Indirecta": 5.00,
            "Costos Indirectos de Fabricación": 18.00
        },
        {
            "Proceso": "Cableado",
            "Costo Mano de Obra Directa": 14.00,
            "Costo Mano de Obra Indirecta": 6.00,
            "Costos Indirectos de Fabricación": 22.00
        },
        {
            "Proceso": "Extrusado",
            "Costo Mano de Obra Directa": 16.00,
            "Costo Mano de Obra Indirecta": 7.50,
            "Costos Indirectos de Fabricación": 28.00
        },
        {
            "Proceso": "Trenzado",
            "Costo Mano de Obra Directa": 15.00,
            "Costo Mano de Obra Indirecta": 6.50,
            "Costos Indirectos de Fabricación": 24.00
        }
    ])
    
    procesos_edit = st.data_editor(
        df_procesos_base,
        use_container_width=True,
        hide_index=True,
        disabled=["Proceso"],
        column_config={
            "Proceso": st.column_config.TextColumn("Proceso / Línea"),
            "Costo Mano de Obra Directa": st.column_config.NumberColumn("Costo Mano de Obra Directa ($/hr)", min_value=0.0, format="$%.2f", required=True),
            "Costo Mano de Obra Indirecta": st.column_config.NumberColumn("Costo Mano de Obra Indirecta ($/hr)", min_value=0.0, format="$%.2f", required=True),
            "Costos Indirectos de Fabricación": st.column_config.NumberColumn("Costos Indirectos de Fabricación ($/hr)", min_value=0.0, format="$%.2f", required=True),
        }
    )
    
    # Asegurar valores numéricos y calcular Total ($/hr)
    for col in ["Costo Mano de Obra Directa", "Costo Mano de Obra Indirecta", "Costos Indirectos de Fabricación"]:
        procesos_edit[col] = pd.to_numeric(procesos_edit[col], errors="coerce").fillna(0.0)
        
    procesos_edit["Total ($/hr)"] = (
        procesos_edit["Costo Mano de Obra Directa"] +
        procesos_edit["Costo Mano de Obra Indirecta"] +
        procesos_edit["Costos Indirectos de Fabricación"]
    )
    
    tarifas_dict = procesos_edit.set_index("Proceso").to_dict(orient="index")
    
    st.markdown("#### 📊 Tarifas Totales Activas por Proceso ($/hr)")
    cols_proc = st.columns(4)
    for idx, row in procesos_edit.iterrows():
        cols_proc[idx].metric(
            label=f"⚙️ {row['Proceso']}",
            value=f"${row['Total ($/hr)']:,.2f} / hr",
            delta=f"MOD: ${row['Costo Mano de Obra Directa']:.2f} | MOI: ${row['Costo Mano de Obra Indirecta']:.2f} | CIF: ${row['Costos Indirectos de Fabricación']:.2f}",
            delta_color="off"
        )

# Resumen en barra lateral
st.sidebar.divider()
st.sidebar.header("🏭 3. Tarifas por Proceso ($/hr)")
for proc_nombre, datos_p in tarifas_dict.items():
    st.sidebar.text(f"• {proc_nombre}: ${datos_p['Total ($/hr)']:,.2f}/hr")

# 4. MOTOR DE CÁLCULO (ACTUAL VS COMPACTADO)
def calcular_escenario(tipo):
    col_val = f"{tipo} (kg/km)"
    
    al_1350_fase = recetas_edit.loc[0, col_val]
    xlpe_fase = recetas_edit.loc[1, col_val]
    al_6201_neutro = recetas_edit.loc[2, col_val]
    xlpe_neutro = recetas_edit.loc[3, col_val]
    
    kg_km_1350 = al_1350_fase * 2
    kg_km_6201 = al_6201_neutro * 1
    kg_km_xlpe = (xlpe_fase * 2) + (xlpe_neutro * 1)
    
    tot_kg_1350 = kg_km_1350 * km
    tot_kg_6201 = kg_km_6201 * km
    tot_kg_xlpe = kg_km_xlpe * km
    peso_total_kg = tot_kg_1350 + tot_kg_6201 + tot_kg_xlpe
    
    costo_tot_1350 = tot_kg_1350 * costo_al_1350
    costo_tot_6201 = tot_kg_6201 * costo_al_6201
    costo_tot_xlpe = tot_kg_xlpe * costo_xlpe
    costo_mp_total = costo_tot_1350 + costo_tot_6201 + costo_tot_xlpe
    
    col_t = f"{tipo} (hrs/km)"
    procesos_detalle = []
    horas_totales = 0.0
    
    tot_mod = 0.0
    tot_moi = 0.0
    tot_cif = 0.0
    costo_indirecto_total = 0.0
    
    for _, row in tiempos_edit.iterrows():
        proc = row["Proceso"]
        tarifas_p = tarifas_dict.get(proc, {"Costo Mano de Obra Directa": 0, "Costo Mano de Obra Indirecta": 0, "Costos Indirectos de Fabricación": 0, "Total ($/hr)": 0})
        
        hrs_proc = row[col_t] * row["Multiplicador"] * km
        c_mod = hrs_proc * tarifas_p["Costo Mano de Obra Directa"]
        c_moi = hrs_proc * tarifas_p["Costo Mano de Obra Indirecta"]
        c_cif = hrs_proc * tarifas_p["Costos Indirectos de Fabricación"]
        c_tot_proc = hrs_proc * tarifas_p["Total ($/hr)"]
        
        horas_totales += hrs_proc
        tot_mod += c_mod
        tot_moi += c_moi
        tot_cif += c_cif
        costo_indirecto_total += c_tot_proc
        
        procesos_detalle.append({
            "Proceso": proc,
            "Horas": hrs_proc,
            "Tarifa_Hr": tarifas_p["Total ($/hr)"],
            "MOD": c_mod,
            "MOI": c_moi,
            "CIF": c_cif,
            "Costo_Total_Proc": c_tot_proc
        })
        
    costo_gran_total = costo_mp_total + costo_indirecto_total
    costo_por_metro = costo_gran_total / metros
    
    df_mp = pd.DataFrame([
        {"Materia Prima": "ALAMBRE DE ALUMINIO 1350 9.50 MM H14", "Kg/Km Cable": kg_km_1350, "Consumo Total (kg)": tot_kg_1350, "Costo Total ($)": costo_tot_1350},
        {"Materia Prima": "ALAMBRE DE ALUMINIO 6201 3.00 MM", "Kg/Km Cable": kg_km_6201, "Consumo Total (kg)": tot_kg_6201, "Costo Total ($)": costo_tot_6201},
        {"Materia Prima": "XLPE NEG (2 Fases + 1 Neutro)", "Kg/Km Cable": kg_km_xlpe, "Consumo Total (kg)": tot_kg_xlpe, "Costo Total ($)": costo_tot_xlpe},
    ])
    
    return {
        "df_mp": df_mp,
        "df_procesos": pd.DataFrame(procesos_detalle),
        "peso_total": peso_total_kg,
        "costo_mp": costo_mp_total,
        "horas_totales": horas_totales,
        "tot_mod": tot_mod,
        "tot_moi": tot_moi,
        "tot_cif": tot_cif,
        "costo_ind_total": costo_indirecto_total,
        "costo_total": costo_gran_total,
        "costo_metro": costo_por_metro,
        "kg_xlpe": tot_kg_xlpe,
        "costo_xlpe": costo_tot_xlpe
    }

act = calcular_escenario("Actual")
comp = calcular_escenario("Compactado")

diff_costo_tot = comp["costo_total"] - act["costo_total"]
diff_pct_tot = (diff_costo_tot / act["costo_total"]) * 100 if act["costo_total"] > 0 else 0
diff_xlpe_kg = comp["kg_xlpe"] - act["kg_xlpe"]
diff_xlpe_usd = comp["costo_xlpe"] - act["costo_xlpe"]
diff_horas = comp["horas_totales"] - act["horas_totales"]
diff_ind_tot = comp["costo_ind_total"] - act["costo_ind_total"]

# 5. TARJETAS DE IMPACTO EJECUTIVO (KPIs)
st.subheader(f"📊 Resultados de Simulación para {metros:,} metros ({km:,.2f} km)")

# Fila 1: Costos Totales y Ahorro de Material
st.markdown("**Resumen General y Materia Prima**")
k1, k2, k3 = st.columns(3)

k1.metric(
    "💰 Costo Total: ACTUAL",
    f"${act['costo_total']:,.2f}",
    f"${act['costo_metro']:,.4f} / metro",
    delta_color="off"
)

k2.metric(
    "🚀 Costo Total: COMPACTADO",
    f"${comp['costo_total']:,.2f}",
    f"{diff_costo_tot:+,.2f} ({diff_pct_tot:+.2f}%)",
    delta_color="inverse"
)

k3.metric(
    "🛢️ Ahorro XLPE NEG",
    f"{abs(diff_xlpe_kg):,.2f} kg",
    f"{diff_xlpe_usd:+,.2f} USD en aislamiento",
    delta_color="inverse"
)

# Fila 2: Comparativa Explícita de Tiempos y Costos Indirectos (Actual vs Compactado)
st.markdown("**Comparativa de Tiempos y Costos Indirectos Totales**")
t1, t2, c1, c2 = st.columns(4)

t1.metric(
    "⏱️ Tiempo Total: ACTUAL",
    f"{act['horas_totales']:,.2f} hrs",
    "Línea base de producción",
    delta_color="off"
)

t2.metric(
    "⚡ Tiempo Total: COMPACTADO",
    f"{comp['horas_totales']:,.2f} hrs",
    f"{diff_horas:+,.2f} hrs vs Actual",
    delta_color="inverse"
)

c1.metric(
    "🏭 Costo Indirecto: ACTUAL",
    f"${act['costo_ind_total']:,.2f}",
    "MOD + MOI + CIF (Actual)",
    delta_color="off"
)

c2.metric(
    "🏭 Costo Indirecto: COMPACTADO",
    f"${comp['costo_ind_total']:,.2f}",
    f"{diff_ind_tot:+,.2f} USD vs Actual",
    delta_color="inverse"
)

st.divider()

# 6. PESTAÑA 2: COMPARATIVA DETALLADA DE TIEMPOS Y COSTOS INDIRECTOS
with tab2:
    st.markdown("### ⏱️ Comparativa por Proceso: Tiempos Totales vs. Costos Indirectos Totales")
    
    df_comp_proc = pd.DataFrame({
        "Proceso": act["df_procesos"]["Proceso"],
        "Tarifa ($/hr)": act["df_procesos"]["Tarifa_Hr"],
        "Horas Actual": act["df_procesos"]["Horas"],
        "Horas Compactado": comp["df_procesos"]["Horas"],
        "Dif. Horas": comp["df_procesos"]["Horas"] - act["df_procesos"]["Horas"],
        "Costo Total Actual ($)": act["df_procesos"]["Costo_Total_Proc"],
        "Costo Total Compactado ($)": comp["df_procesos"]["Costo_Total_Proc"],
        "Dif. Costo ($)": comp["df_procesos"]["Costo_Total_Proc"] - act["df_procesos"]["Costo_Total_Proc"]
    })
    
    # Fila de Totales Generales
    fila_total = pd.DataFrame([{
        "Proceso": "TOTAL GENERAL",
        "Tarifa ($/hr)": None,
        "Horas Actual": df_comp_proc["Horas Actual"].sum(),
        "Horas Compactado": df_comp_proc["Horas Compactado"].sum(),
        "Dif. Horas": df_comp_proc["Dif. Horas"].sum(),
        "Costo Total Actual ($)": df_comp_proc["Costo Total Actual ($)"].sum(),
        "Costo Total Compactado ($)": df_comp_proc["Costo Total Compactado ($)"].sum(),
        "Dif. Costo ($)": df_comp_proc["Dif. Costo ($)"].sum()
    }])
    
    df_comp_proc_final = pd.concat([df_comp_proc, fila_total], ignore_index=True)
    
    st.dataframe(
        df_comp_proc_final.style.format({
            "Tarifa ($/hr)": lambda x: f"${x:,.2f}" if pd.notnull(x) else "—",
            "Horas Actual": "{:,.2f} hrs",
            "Horas Compactado": "{:,.2f} hrs",
            "Dif. Horas": "{:+,.2f} hrs",
            "Costo Total Actual ($)": "${:,.2f}",
            "Costo Total Compactado ($)": "${:,.2f}",
            "Dif. Costo ($)": "${:+,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("#### 🧾 Desglose Acumulado por Elemento de Costo (MOD, MOI y CIF)")
    df_res_conv = pd.DataFrame([
        {"Rubro": "Costo Mano de Obra Directa (MOD)", "Actual ($)": act["tot_mod"], "Compactado ($)": comp["tot_mod"], "Diferencia ($)": comp["tot_mod"] - act["tot_mod"]},
        {"Rubro": "Costo Mano de Obra Indirecta (MOI)", "Actual ($)": act["tot_moi"], "Compactado ($)": comp["tot_moi"], "Diferencia ($)": comp["tot_moi"] - act["tot_moi"]},
        {"Rubro": "Costos Indirectos de Fabricación (CIF)", "Actual ($)": act["tot_cif"], "Compactado ($)": comp["tot_cif"], "Diferencia ($)": comp["tot_cif"] - act["tot_cif"]},
        {"Rubro": "TOTAL COSTOS INDIRECTOS Y MANO DE OBRA", "Actual ($)": act["costo_ind_total"], "Compactado ($)": comp["costo_ind_total"], "Diferencia ($)": comp["costo_ind_total"] - act["costo_ind_total"]},
    ])
    st.dataframe(
        df_res_conv.style.format({
            "Actual ($)": "${:,.2f}",
            "Compactado ($)": "${:,.2f}",
            "Diferencia ($)": "${:+,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

# 7. PESTAÑA 3: COMPARATIVA MATERIA PRIMA
with tab3:
    st.markdown("### Desglose de Materia Prima (2 Fases ASC + 1 Neutro AAAC)")
    
    df_comp_mp = pd.DataFrame({
        "Materia Prima": act["df_mp"]["Materia Prima"],
        "Actual (kg/km)": act["df_mp"]["Kg/Km Cable"],
        "Compactado (kg/km)": comp["df_mp"]["Kg/Km Cable"],
        "Consumo Actual (kg)": act["df_mp"]["Consumo Total (kg)"],
        "Consumo Compactado (kg)": comp["df_mp"]["Consumo Total (kg)"],
        "Costo Actual ($)": act["df_mp"]["Costo Total ($)"],
        "Costo Compactado ($)": comp["df_mp"]["Costo Total ($)"],
        "Diferencia ($)": comp["df_mp"]["Costo Total ($)"] - act["df_mp"]["Costo Total ($)"]
    })
    
    st.dataframe(
        df_comp_mp.style.format({
            "Actual (kg/km)": "{:,.2f}",
            "Compactado (kg/km)": "{:,.2f}",
            "Consumo Actual (kg)": "{:,.2f}",
            "Consumo Compactado (kg)": "{:,.2f}",
            "Costo Actual ($)": "${:,.2f}",
            "Costo Compactado ($)": "${:,.2f}",
            "Diferencia ($)": "${:+,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

# 8. PESTAÑA 4: GRÁFICOS EJECUTIVOS
with tab4:
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("**Comparativa de Costos Indirectos por Proceso ($): Actual vs. Compactado**")
        df_g_proc = pd.concat([
            act["df_procesos"][["Proceso", "Costo_Total_Proc"]].assign(Escenario="Actual"),
            comp["df_procesos"][["Proceso", "Costo_Total_Proc"]].assign(Escenario="Compactado")
        ])
        fig_proc = px.bar(
            df_g_proc, x="Proceso", y="Costo_Total_Proc", color="Escenario", barmode="group", text_auto=".2f",
            labels={"Costo_Total_Proc": "Costo Total ($)"},
            color_discrete_map={"Actual": "#EF553B", "Compactado": "#00CC96"}
        )
        fig_proc.update_layout(xaxis_title="", legend_title="")
        st.plotly_chart(fig_proc, use_container_width=True)

    with col_g2:
        st.markdown("**Comparativa de Tiempos Totales por Proceso (hrs): Actual vs. Compactado**")
        df_g_hrs = pd.concat([
            act["df_procesos"][["Proceso", "Horas"]].assign(Escenario="Actual"),
            comp["df_procesos"][["Proceso", "Horas"]].assign(Escenario="Compactado")
        ])
        fig_hrs = px.bar(
            df_g_hrs, x="Proceso", y="Horas", color="Escenario", barmode="group", text_auto=".2f",
            labels={"Horas": "Tiempo Total (hrs)"},
            color_discrete_map={"Actual": "#EF553B", "Compactado": "#00CC96"}
        )
        fig_hrs.update_layout(xaxis_title="", legend_title="")
        st.plotly_chart(fig_hrs, use_container_width=True)
