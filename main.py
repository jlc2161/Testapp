import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import random
import pandas as pd
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ================= CONSTANTS =================
HOME_GOAL = 450_000
INVEST_GOAL = 1_000_000
GOAL_LOG = "goal_tracker_log.txt"
HISTORY_CSV = "monthly_history.csv"
PDF_REPORT = "fire_report.pdf"

# ========== QUOTES ==========
QUOTES = [
    "The best investment you can make is in yourself. – Warren Buffett",
    "An investment in knowledge pays the best interest. – Benjamin Franklin",
    "Your money should be working for you while you sleep. – Anonymous",
    "Financial independence is not a dream, it's a decision. – Jose Cisneros",
    "Do not save what is left after spending, but spend what is left after saving. – Warren Buffett",
    "Time in the market beats timing the market. – Unknown",
    "It's not about having a lot of money. It’s about knowing how to manage it. – Dave Ramsey",
    "Discipline is the bridge between goals and accomplishment. – Jim Rohn",
    "Don’t work for money, make money work for you. – Robert Kiyosaki",
    "Save money. And money will save you. – Jamaican Proverb",
    "A penny saved is a penny earned. – Benjamin Franklin",
    "Wealth is not about having a lot of money, it’s about having a lot of options. – Chris Rock",
    "The goal isn’t more money. The goal is living life on your terms. – Chris Brogan",
    "Live below your means. – Unknown",
    "Budgeting isn't about limiting yourself—it's about making room for the things that matter. – Unknown",
    "The journey to financial freedom starts with one step: saving. – Unknown",
    "You can’t build wealth if you don’t track your spending. – Unknown",
    "Sacrifice a few years of comfort for decades of freedom. – Unknown",
    "The earlier you start, the better. – Compound Interest",
    "Stay consistent. Stay patient. – FIRE Movement",
    "Dream big, save smart, retire early. – FIRE Community",
    "Every dollar you save is a soldier in your army of freedom. – Grant Sabatier",
    "Don’t count every penny. Make every penny count. – Unknown",
    "The future depends on what you do today. – Mahatma Gandhi",
    "Wealth is built in silence. – Unknown",
    "Start where you are. Use what you have. Do what you can. – Arthur Ashe",
    "Freedom is the goal; money is the tool. – Unknown",
    "Success is the sum of small efforts repeated day in and day out. – Robert Collier",
    "You can’t control the market, but you can control your savings rate. – JL Collins",
    "Failing to plan is planning to fail. – Alan Lakein"
]

# ================= STREAMLIT APP SETUP =================
st.set_page_config(page_title="FIRE Tracker", layout="centered")
tab1, tab2, tab3 = st.tabs(["🔥 Tracker", "💸 Budget", "📜 History"])

# ========== TRACKER TAB ==========
with tab1:
    st.title("🔥 Monthly FIRE Tracker for Me")

    st.markdown(f"🧠 *Quote of the Day:* **{random.choice(QUOTES)}**")

    st.subheader("🏠 Home Goal: $450,000 by 2028")
    st.subheader("💼 Investment Goal: $1,000,000")

    with st.form("contribution_form"):
        st.write("### Enter This Month's Contributions:")
        home_input = st.number_input("🏠 Home Savings", min_value=0.0, step=100.0)
        roth_input = st.number_input("🟢 Roth IRA", min_value=0.0, step=100.0)
        brokerage_input = st.number_input("💼 Brokerage", min_value=0.0, step=100.0)
        submitted = st.form_submit_button("Submit & Save")

    if "home_saved" not in st.session_state:
        st.session_state.home_saved = 100_000  # Starting saved
        st.session_state.roth_ira = 0.0
        st.session_state.brokerage = 0.0

    if submitted:
        st.session_state.home_saved += home_input
        st.session_state.roth_ira += roth_input
        st.session_state.brokerage += brokerage_input

        total_invested = st.session_state.roth_ira + st.session_state.brokerage
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to log
        with open(GOAL_LOG, "a") as f:
            f.write(f"\n--- {timestamp} ---\n")
            f.write(f"Home: ${st.session_state.home_saved:,.2f} / ${HOME_GOAL:,}\n")
            f.write(f"Roth IRA: ${st.session_state.roth_ira:,.2f}\n")
            f.write(f"Brokerage: ${st.session_state.brokerage:,.2f}\n")
            f.write(f"Investments: ${total_invested:,.2f} / ${INVEST_GOAL:,}\n")

        # Save to CSV
        data = {
            "Date": [timestamp],
            "Home": [st.session_state.home_saved],
            "Roth IRA": [st.session_state.roth_ira],
            "Brokerage": [st.session_state.brokerage],
            "Investments": [total_invested],
        }
        df = pd.DataFrame(data)
        if not os.path.exists(HISTORY_CSV):
            df.to_csv(HISTORY_CSV, index=False)
        else:
            df.to_csv(HISTORY_CSV, mode="a", header=False, index=False)

        # Save to PDF
        pdf = canvas.Canvas(PDF_REPORT, pagesize=letter)
        width, height = letter
        y = height - 50

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "🔥 Monthly FIRE Tracker Report")
        y -= 30
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y, f"Date: {timestamp}")
        y -= 20
        pdf.drawString(50, y, f"🏠 Home: ${st.session_state.home_saved:,.2f}")
        y -= 20
        pdf.drawString(50, y, f"🟢 Roth IRA: ${st.session_state.roth_ira:,.2f}")
        y -= 20
        pdf.drawString(50, y, f"💼 Brokerage: ${st.session_state.brokerage:,.2f}")
        y -= 20
        pdf.drawString(50, y, f"📈 Total Investments: ${total_invested:,.2f}")
        pdf.save()

        st.success("✅ Contributions saved and report exported!")

    # Display pie charts
    st.markdown("### 🥧 Goal Progress Visuals")
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.pie(
            [st.session_state.home_saved, max(0, HOME_GOAL - st.session_state.home_saved)],
            labels=["Saved", "Remaining"],
            autopct="%1.1f%%",
            startangle=90,
            colors=["orange", "lightgray"],
        )
        ax1.set_title("Home Goal Progress")
        st.pyplot(fig1)

    with col2:
        invest_total = st.session_state.roth_ira + st.session_state.brokerage
        fig2, ax2 = plt.subplots()
        ax2.pie(
            [invest_total, max(0, INVEST_GOAL - invest_total)],
            labels=["Saved", "Remaining"],
            autopct="%1.1f%%",
            startangle=90,
            colors=["green", "lightgray"],
        )
        ax2.set_title("Investment Goal Progress")
        st.pyplot(fig2)

    # Forecast
    st.markdown("### 🔮 Year-End Forecast")
    months_remaining = 12 - datetime.now().month
    forecast_home = st.session_state.home_saved + (home_input * months_remaining)
    forecast_invest = (st.session_state.roth_ira + st.session_state.brokerage) + ((roth_input + brokerage_input) * months_remaining)
    st.info(f"🏠 Forecasted Home by Year-End: **${forecast_home:,.2f}**")
    st.info(f"📈 Forecasted Investments by Year-End: **${forecast_invest:,.2f}**")

# ========== BUDGET TAB ==========
with tab2:
    st.title("💸 Monthly Budget")

    monthly_income = st.number_input("Total Monthly Income After Tax", value=9291.67, step=50.0)
    wants = st.number_input("Wants", value=730.63, step=10.0)
    savings = st.number_input("Savings", value=2922.54, step=10.0)
    needs = monthly_income - (wants + savings)

    st.success(f"✅ Needs auto-calculated: **${needs:,.2f}**")

    st.write("### Expenses by Category")
    budget_categories = {
        "Food": 800,
        "Mortgage": 2571,
        "401k": 512.5,
        "Car Insurance": 208,
        "Phone": 172,
        "Gas": 120,
        "Health Insurance": 350,
        "Internet": 85,
        "Personal": 400,
        "Electricity": 250,
        "Water": 150,
        "Utilities Gas": 20,
        "Kids": 200,
    }

    for category in budget_categories:
        budget_categories[category] = st.number_input(f"{category}", value=float(budget_categories[category]), step=10.0)

    st.markdown("### 📊 Budget Pie Chart")
    fig3, ax3 = plt.subplots()
    ax3.pie(budget_categories.values(), labels=budget_categories.keys(), autopct="%1.1f%%", startangle=90)
    ax3.set_title("Budget Breakdown")
    st.pyplot(fig3)

# ========== HISTORY TAB ==========
with tab3:
    st.title("📜 Contribution & Budget History")
    if os.path.exists(HISTORY_CSV):
        history_df = pd.read_csv(HISTORY_CSV)
        st.dataframe(history_df)
    else:
        st.info("No history available yet. Submit your first entry!")