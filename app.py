from pathlib import Path
import sys
import sqlite3
import subprocess
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.data_processing import quality_report

st.set_page_config(page_title="Public Transport Passenger Analytics", page_icon="🚌", layout="wide")

@st.cache_data(show_spinner="Dataset yuklanmoqda...")
def get_data():
    db_path = ROOT / "database" / "transport_analytics.db"
    if not db_path.exists():
        subprocess.run([sys.executable, str(ROOT / "database" / "build_db.py")], check=True, cwd=ROOT)
    with sqlite3.connect(db_path) as con:
        return pd.read_sql_query("""
            SELECT a.agency_code AS agency, r.source_route_id AS route_id,
                   rp.period_code, rp.summary_begin_date, rp.source_file,
                   rp.stops, rp.avg_on_per_trip, rp.avg_trips, rp.sum_ons, rp.avg_ons
            FROM route_period rp
            JOIN route r ON r.route_pk = rp.route_pk
            JOIN agency a ON a.agency_id = r.agency_id
            ORDER BY a.agency_code, r.source_route_id, rp.period_code
        """, con)

@st.cache_data
def get_quality():
    return quality_report(ROOT / "data" / "raw")

st.markdown("<h1 style='margin-bottom:0'>🚌 Public Transport Passenger Analytics System</h1>", unsafe_allow_html=True)
st.caption("Jamoat transporti yo‘lovchilari va qatnov ko‘rsatkichlarini tahlil qilish tizimi")
try:
    df = get_data()
except Exception as e:
    st.error(f"Datasetni yuklashda xatolik: {e}")
    st.stop()

with st.sidebar:
    st.header("Filtrlar")
    agencies = st.multiselect("Transport agentligi", sorted(df.agency.unique()), default=sorted(df.agency.unique()))
    periods = st.multiselect("Davr", ["12", "17"], default=["12", "17"], format_func=lambda x: "Boshlang‘ich (12)" if x == "12" else "Taqqoslash (17)")
    metric_label = st.selectbox("Asosiy ko‘rsatkich", ["sum_ons", "avg_ons", "avg_trips", "avg_on_per_trip", "stops"], format_func=lambda x: {"sum_ons":"SUMons — jami yo‘lovchi ko‘rsatkichi", "avg_ons":"AVGons — o‘rtacha yo‘lovchi ko‘rsatkichi", "avg_trips":"AVGtrips — o‘rtacha qatnovlar", "avg_on_per_trip":"AVGonPERtrip", "stops":"Bekatlar soni"}[x])
    st.caption("12/17 — manba faylidagi davr belgilari. Aniq markup sanasi har bir agentlikda farq qiladi.")

f = df[df.agency.isin(agencies) & df.period_code.isin(periods)].copy()
if f.empty:
    st.warning("Tanlangan filtrlar bo‘yicha ma'lumot yo‘q.")
    st.stop()

# Summary KPIs describe the currently filtered observations.
c1,c2,c3,c4 = st.columns(4)
c1.metric("Agentliklar", f.agency.nunique())
c2.metric("Yo‘nalish-davr yozuvlari", f.shape[0])
c3.metric("Yo‘nalishlar", f[["agency","route_id"]].drop_duplicates().shape[0])
c4.metric("Bo‘sh qiymatlar", int(f.isna().sum().sum()))

p1,p2,p3,p4,p5 = st.tabs(["Umumiy ko‘rinish", "Agentliklar", "Yo‘nalishlar", "Davr taqqoslash", "Ma'lumotlar"])
with p1:
    st.subheader("Asosiy ko‘rsatkichlar bo‘yicha agentliklar")
    agg_fn = "sum" if metric_label == "sum_ons" else "mean"
    agg = f.groupby(["agency","period_code"], as_index=False)[metric_label].agg(agg_fn)
    fig = px.bar(agg, x="agency", y=metric_label, color="period_code", barmode="group", title=f"{metric_label} — agentliklar va davrlar kesimida ({agg_fn})", labels={"agency":"Agentlik","period_code":"Manba davri",metric_label:metric_label})
    st.plotly_chart(fig, use_container_width=True)
    st.info("SUMons va boshqa ko‘rsatkichlar manba faylidagi route-level agregat metrikalardir. Ularni turli agentliklar bo‘yicha mutlaq bozor ulushi sifatida talqin qilmang.")
    st.subheader("Ko‘rsatkichlar taqsimoti")
    fig2=px.box(f,x="agency",y=metric_label,color="period_code",points="outliers",title=f"{metric_label} taqsimoti")
    st.plotly_chart(fig2,use_container_width=True)
with p2:
    st.subheader("Agentliklar kesimida")
    agency_summary=f.groupby(["agency","period_code"],as_index=False).agg(routes=("route_id","nunique"),sum_ons=("sum_ons","sum"),avg_ons=("avg_ons","mean"),avg_trips=("avg_trips","mean"),avg_on_per_trip=("avg_on_per_trip","mean"))
    st.dataframe(agency_summary, use_container_width=True, hide_index=True)
    fig=px.scatter(f,x="avg_trips",y="sum_ons",color="agency",symbol="period_code",hover_data=["route_id","summary_begin_date"],title="Qatnovlar va SUMons o‘rtasidagi bog‘liqlik")
    st.plotly_chart(fig,use_container_width=True)
with p3:
    st.subheader("Yo‘nalishlar reytingi")
    chosen=f[f.period_code==("17" if "17" in periods else periods[0])].copy()
    chosen=chosen.sort_values(metric_label,ascending=False).head(25)
    fig=px.bar(chosen.sort_values(metric_label),x=metric_label,y="route_id",color="agency",orientation="h",hover_data=["summary_begin_date"],title=f"Top 25 yo‘nalish — {metric_label}")
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(chosen[["agency","route_id","period_code","summary_begin_date","stops","avg_trips","sum_ons","avg_ons"]],use_container_width=True,hide_index=True)
with p4:
    st.subheader("Boshlang‘ich va taqqoslash davri")
    wide=df.pivot_table(index=["agency","route_id"],columns="period_code",values=metric_label,aggfunc="first").reset_index()
    if "12" in wide.columns and "17" in wide.columns:
        wide["absolute_change"]=wide["17"]-wide["12"]
        wide["percent_change"]=wide.apply(lambda r: ((r["17"]-r["12"])/r["12"]*100) if pd.notna(r["12"]) and r["12"]!=0 else None,axis=1)
        st.metric("O‘rtacha foizli o‘zgarish", f"{wide.percent_change.mean():.2f}%" if wide.percent_change.notna().any() else "Hisoblanmadi")
        fig=px.histogram(wide,x="percent_change",color="agency",barmode="overlay",title=f"{metric_label}: yo‘nalishlar bo‘yicha foizli o‘zgarish")
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(wide.sort_values("percent_change"),use_container_width=True,hide_index=True)
    else:
        st.warning("Davr taqqoslash uchun 12 va 17 davrlarini birgalikda tanlang.")
with p5:
    st.subheader("Dataset sifati")
    st.dataframe(get_quality(),use_container_width=True,hide_index=True)
    st.subheader("Standartlashtirilgan ma'lumotlar")
    st.dataframe(f,use_container_width=True,hide_index=True)
    st.download_button("Filtrlangan ma'lumotlarni CSV yuklab olish",f.to_csv(index=False).encode("utf-8-sig"),"transport_analytics_filtered.csv","text/csv")

st.divider()
st.caption("Dataset: Berrebi, Joshi & Watkins — Route-Level Ridership and Frequency Data in Four Transit Agencies (STRIDE project A2), Zenodo. Tizim o‘quv-tahliliy maqsadlar uchun.")
