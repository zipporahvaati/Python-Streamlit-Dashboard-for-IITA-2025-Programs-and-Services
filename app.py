import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="IITA 2025 KPI Dashboard", layout="wide")

# ----------------------------
# Top Banner
# ----------------------------
st.image("IITA_logo.png", width=200)
st.markdown("""
<div style="background-color:#ffffff; padding:15px;">
    <h1 style="color:#00891a; margin:10px; font-size:28px; text-align:center;">
        International Institute of Tropical Agriculture Dashboard
    </h1>
</div>
""", unsafe_allow_html=True)
st.write("Programs and Service output KPIs")

# ----------------------------
# CSS for tabs
# ----------------------------
st.markdown("""
<style>
div[data-baseweb="tab-list"] button {
    background-color: #00891a; 
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 15px;
    font-weight: bold;
    margin-right: 8px;
    transition: 0.2s;
}
div[data-baseweb="tab-list"] button:focus { outline: none; }
div[data-baseweb="tab-list"] button[selected] { background-color: #005500; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Main Tabs
# ----------------------------
main_tab = st.tabs([
    "2025 IITA Programs Output KPIs",
    "2025 IITA Service Unit Output KPIs"
])

# ============================
# Programs Output KPIs Tab
# ============================
with main_tab[0]:
    # Load Excel2 (Aggregated)
    excel2 = pd.read_excel("excel2.xlsx", engine="openpyxl")
    excel2.columns = [str(c).strip().replace('\n',' ').replace('\r','') for c in excel2.columns]

    # Fill down Category
    if 'Unnamed: 0' in excel2.columns:
        excel2['Category'] = excel2['Unnamed: 0'].ffill()
    else:
        excel2['Category'] = 'All'

    # Ensure numeric columns
    numeric_cols2 = ['Annual Target', '2025 Actual value', '% Female (where applicable)']
    for col in numeric_cols2:
        if col in excel2.columns:
            excel2[col] = pd.to_numeric(excel2[col], errors='coerce')

    # Show table and heatmap side by side
    col_table, col_heatmap = st.columns([2, 2])

    # --- Table ---
    with col_table:
        st.subheader("📋 KPI Table")

        def iita_highlight(val):
            try:
                val = float(val)
                if val >= 0.75: return 'background-color: #00891a; color: white; font-weight: bold'
                elif val >= 0.5: return 'background-color: #FFA500; color: black; font-weight: bold'
                elif val > 0: return 'background-color: #FFE5B4; color: black'
                else: return ''
            except:
                return ''

        format_dict2 = {
            'Annual Target': "{:.2f}",
            '2025 Actual value': "{:.2f}",
            '% Female (where applicable)': "{:.0%}"
        }

        st.dataframe(
            excel2.style.applymap(iita_highlight, subset=numeric_cols2)
                         .format(format_dict2),
            height=500,
            use_container_width=True
        )

    # --- Heatmap ---
    with col_heatmap:
        st.subheader("🔥 KPI Heatmap")
        if '2025 Actual value' not in excel2.columns or 'KPI Nr' not in excel2.columns:
            st.error("Columns '2025 Actual value' or 'KPI Nr' not found! Check Excel headers.")
            st.write("Current columns:", excel2.columns.tolist())
        else:
            heatmap_data = excel2.pivot(index='KPI Nr', columns='Category', values='2025 Actual value')
            min_val = np.nanmin(heatmap_data.values)
            max_val = np.nanmax(heatmap_data.values)

            fig = px.imshow(
                heatmap_data,
                text_auto=True,
                aspect="auto",
                color_continuous_scale=['#FFE5B4', '#FFA500', '#00891a'],
                zmin=min_val,
                zmax=max_val
            )
            fig.update_layout(xaxis_title="Category", yaxis_title="KPI Number")
            st.plotly_chart(fig, use_container_width=True)

    # Remaining subtabs
    programs_subtab = st.tabs([
        "Research, Training, Product Development",
        "Recognition/Reputation, Societal Impact and Inclusivity"
    ])

    # --- Research/Training/Product Development ---
    with programs_subtab[0]:
        subtab_rtpd = st.tabs([
            "KPI Nr 2025-2030",
            "KPI Nr by Program for 2025",
            "KPI FTE By Program",
            "KPI $ By Program"
        ])

        # --- Excel3 ---
        with subtab_rtpd[0]:
            excel3 = pd.read_excel("excel3.xlsx", engine="openpyxl")
            excel3 = excel3.dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)
            excel3.columns = [str(c).strip().replace('\n',' ') for c in excel3.columns]

            numeric_cols3 = [c for c in excel3.columns if c not in ['KPI Nr','KPI Metrics']]

            for col in numeric_cols3:
                excel3[col] = pd.to_numeric(excel3[col], errors='coerce')

            def iita_highlight3(val):
                try:
                    val = float(val)
                    if val >= 0.75: return 'background-color: #00891a; color: white; font-weight: bold'
                    elif val >= 0.5: return 'background-color: #FFA500; color: black; font-weight: bold'
                    elif val > 0: return 'background-color: #FFE5B4; color: black'
                    else: return ''
                except: return ''

            format_dict3 = {col: "{:.2f}" for col in numeric_cols3}

            st.dataframe(
                excel3.style.applymap(iita_highlight3, subset=numeric_cols3)
                             .format(format_dict3),
                use_container_width=True,
                height=500
            )

        # --- Excel4 ---
        with subtab_rtpd[1]:
            excel4 = pd.read_excel("excel4.xlsx", engine="openpyxl")
            excel4 = excel4.dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)
            excel4.columns = [str(c).strip().replace('\n',' ') for c in excel4.columns]

            numeric_cols4 = [c for c in excel4.columns if c not in ['KPI Nr','KPI Metrics']]
            for col in numeric_cols4:
                excel4[col] = pd.to_numeric(excel4[col], errors='coerce')

            def iita_highlight4(val):
                try:
                    val = float(val)
                    if val >= 0.75: return 'background-color: #00891a; color: white; font-weight: bold'
                    elif val >= 0.5: return 'background-color: #FFA500; color: black; font-weight: bold'
                    elif val > 0: return 'background-color: #FFE5B4; color: black'
                    else: return ''
                except: return ''

            format_dict4 = {col: "{:.2f}" for col in numeric_cols4}

            st.dataframe(
                excel4.style.applymap(iita_highlight4, subset=numeric_cols4)
                      .format(format_dict4),
                use_container_width=True,
                height=500
            )

        with subtab_rtpd[2]:
            st.write("KPI FTE By Program content coming soon")
        with subtab_rtpd[3]:
            st.write("KPI $ By Program content coming soon")

    # --- Recognition/Societal Impact/Inclusivity ---
    with programs_subtab[1]:
        rec_tabs = st.tabs([
            "Recognition / Reputation",
            "Societal Impact",
            "Inclusivity"
        ])
        with rec_tabs[0]: st.write("Coming Soon")
        with rec_tabs[1]: st.write("Coming Soon")
        with rec_tabs[2]: st.write("Coming Soon")

# ============================
# Service Unit Output KPIs Tab
# ============================
with main_tab[1]:
    excel1 = pd.read_excel("excel1.xlsx", engine="openpyxl")
    excel1 = excel1.dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)
    excel1.columns = [str(c).strip().replace('\n',' ') for c in excel1.columns]

    percent_cols = [c for c in excel1.columns if 'Target' in c or 'Actual' in c]
    for col in percent_cols:
        excel1[col] = pd.to_numeric(excel1[col], errors='coerce')

    def iita_highlight(val):
        try:
            val = float(val)
            if val >= 0.75: return 'background-color: #00891a; color: white; font-weight: bold'
            elif val >= 0.5: return 'background-color: #FFA500; color: black; font-weight: bold'
            elif val > 0: return 'background-color: #FFE5B4; color: black'
            else: return ''
        except:
            return ''

    header_style = [{'selector': 'th',
                     'props': 'background-color: #00891a; color: white; font-weight: bold; text-align: center;'}]

    st.dataframe(
        excel1.style.applymap(iita_highlight, subset=percent_cols)
                    .format({col: "{:.0%}" for col in percent_cols})
                    .set_table_styles(header_style),
        use_container_width=True,
        height=500
    )