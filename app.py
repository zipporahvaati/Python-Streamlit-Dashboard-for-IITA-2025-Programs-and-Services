import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ----------------------------
# Page setup

# ----------------------------
st.set_page_config(page_title="IITA 2025 KPI Dashboard", layout="wide")

# ----------------------------
# Load Excel files
# ----------------------------
excel1 = pd.read_excel("excel1.xlsx", engine="openpyxl")  # KPI by Nr
excel2 = pd.read_excel("excel2.xlsx", engine="openpyxl")  # Aggregated
excel3 = pd.read_excel("excel3.xlsx", engine="openpyxl")  # KPI Nr 2025-2030
excel4 = pd.read_excel("excel4.xlsx", engine="openpyxl")  # KPI Nr by Program for 2025


# TOP BANNER WITH LOGO AND TITLE
st.image("IITA_logo.png", width=200,output_format="PNG")
st.markdown("""
<div style="background-color:#ffffff; padding:15px;">
    <h1 style="color:#00891a; margin:10px; font-size:28px; text-align:center;">
        IITA Agricultural KPI Dashboard
    </h1>
</div>
""", unsafe_allow_html=True)

st.header("Programs and Services")


# ----------------------------
# CSS for uniform tab style
# ----------------------------
st.markdown("""
<style>
/* Make Streamlit tabs look like buttons */
div[data-baseweb="tab-list"] button {
    background-color: #00891a;   /* green button */
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 15px;
    font-weight: bold;
    margin-right: 8px;
    transition: 0.2s;
}

/* Remove focus outline */
div[data-baseweb="tab-list"] button:focus {
    outline: none;
}

/* Highlight selected tab */
div[data-baseweb="tab-list"] button[selected] {
    background-color: #005500;   /* darker green for selected */
}
</style>
""",
    unsafe_allow_html=True)


# ----------------------------
# Main Tabs
# ----------------------------
main_tab = st.tabs([
    "2025 IITA Programs Output KPIs", 
    "2025 IITA Service Unit Output KPIs"
])

# Programs Output KPIs Tab
# ----------------------------
# ----------------------------
# Programs Output KPIs Tab
# ----------------------------
with main_tab[0]:
    #st.subheader("📈 Programs Output KPIs 2025")
    st.write("Select KPI view below:")

    # ----------------------------
    # Define subtabs
    # ----------------------------
    programs_subtab = st.tabs([
        "KPI by NR Aggregated",
        "Research, Training, Product Development",
        "Recognition/Reputation, Societal Impact and Inclusivity"
    ])

    # ----------------------------
    # KPI by NR Aggregated: table + heatmap
    # ----------------------------
    with programs_subtab[0]:
        #st.write(" 🧮 KPI by Number Aggregated |")
        
        # Create two columns: table | heatmap
        col_table, col_heatmap = st.columns([2.0, 2.0])

        # Left: Excel table
        with col_table:
            st.subheader("📋 KPI Table")
            st.dataframe(excel2, height=400)

        # Right: Heatmap
        with col_heatmap:
            st.subheader("🔥 KPI Heatmap")
            
            df_heat = excel2.copy()

            # Fill down category
            if 'Unnamed: 0' in df_heat.columns:
                df_heat['Category'] = df_heat['Unnamed: 0'].ffill()
            else:
                df_heat['Category'] = 'All'

            # Ensure numeric columns
            for col in ['Annual Target', '2025 Actual value', '% Female (where applicable)']:
                df_heat[col] = pd.to_numeric(df_heat[col], errors='coerce')

            # Pivot for heatmap
            heatmap_data = df_heat.pivot(index='KPI Nr', columns='Category', values='2025 Actual value')

            # Plot heatmap
            fig = px.imshow(
                heatmap_data,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(
                xaxis_title="Category",
                yaxis_title="KPI Number"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # Research, Training, Product Development
    # ----------------------------
    with programs_subtab[1]:
        st.write("🔬 Research | 🎓 Training | 🛠️ Product Development ")
        subtab_rtpd = st.tabs([
            "KPI Nr 2025-2030",
            "KPI Nr by Program for 2025",
            "KPI FTE By Program",
            "KPI $ By Program"
        ])
        
        with subtab_rtpd[0]:
            #st.write("KPI Nr 2025-2030 content here")
            st.dataframe(excel3)
        with subtab_rtpd[1]:
            #st.write("KPI Nr by Program for 2025 content here")
            st.dataframe(excel4)
        with subtab_rtpd[2]:
            st.write("KPI FTE By Program content here")
        with subtab_rtpd[3]:
            st.write("KPI $ By Program content here")
    
    # ----------------------------
    # Recognition/Reputation, Societal Impact and Inclusivity
    # ----------------------------
    with programs_subtab[2]:
        st.write("🏆 Recognition / Reputation |🌱 Societal Impact| 🤝 Inclusivity|")
        rec_tabs = st.tabs([
            "Recognition / Reputation",
            "Societal Impact",
            "Inclusivity"
        ])

        with rec_tabs[0]:
            st.write("Coming Soon: Recognition / Reputation content")
        with rec_tabs[1]:
            st.write("Coming Soon: Societal Impact content")
        with rec_tabs[2]:
            st.write("Coming Soon: Inclusivity content")

# Service Unit Output KPIs Tab
# ----------------------------
with main_tab[1]:
    # Load Excel
    excel1 = pd.read_excel("excel1.xlsx", engine="openpyxl")

    st.subheader("🧩 2025 IITA Service Unit Output KPIs")

    # Create two columns
    col1, col2 = st.columns([2.0, 2.0])

    # ----------------------------
    # Left column: Excel table
    # ----------------------------
    with col1:
        def highlight_target(val):
            color = ""  # default: no color

            if isinstance(val, str):
                if "Meeting at least 75%" in val:
                    color = "#8BC34A"  # green
                elif "Meeting at least 50%" in val:
                    color = "#FFEB3B"  # yellow
                elif val.strip() != "":  # any other non-empty string
                    color = "#FF7043"  # orange/red

            if color:  # only return CSS if color is set
                return f'background-color: {color}; font-weight: bold'
            return ''

        # Apply styling to the Excel table
        st.dataframe(excel1, height=400)

    # ----------------------------
    # Right column: Pie chart with bordered card
    # ----------------------------
    with col2:
        st.markdown(
            """
            <div style="
                border: 2px solid #00891a;
                border-radius: 10px;
                padding: 10px;
                background-color: #f9f9f9;
            ">
            """,
            unsafe_allow_html=True
        )
        
        # Pie chart inside the bordered div
        fig = px.pie(
            excel1,
            names='Meeting or Exceeding  Target',
            title="Overall Target Achievement",
            color_discrete_sequence=px.colors.sequential.Oranges
        )
        st.plotly_chart(fig)
        
        # Close the div
        st.markdown("</div>", unsafe_allow_html=True)