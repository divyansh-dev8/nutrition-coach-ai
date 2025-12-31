import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Divyansh Nutrition Coach",
    layout="wide"
)

# ================= BACKGROUND =================
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1558611848-73f7eb4001a1");
    background-size: cover;
    background-attachment: fixed;
}
.block-container {
    background: rgba(0,0,0,0.78);
    padding: 2rem;
    border-radius: 20px;
}
h1, h2, h3, p, label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("<h1 style='text-align:center;'>💪 Divyansh Nutrition Coach</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align:center;'>Elite Personal Nutrition & Fitness Blueprint</h3>",
    unsafe_allow_html=True
)

# ================= USER INPUTS =================
st.markdown("## 🧍 Personal Details")

age = st.slider("Age (years)", 16, 60, 22)
weight = st.slider("Weight (kg)", 40, 130, 75)
height = st.slider("Height (cm)", 140, 200, 170)

gender = st.selectbox("Gender", ["Male", "Female"])
activity = st.selectbox("Activity Level", ["Low", "Medium", "High"])
goal = st.selectbox("Goal", ["Fat Loss", "Muscle Gain", "Maintenance"])
preference = st.selectbox("Food Preference", ["Veg", "Non-Veg", "Both"])

# ================= SUPPLEMENTS =================
st.markdown("## 💊 Supplements & Medicines (Optional)")

supplements = st.multiselect(
    "Select what you consume",
    [
        "Protein Powder",
        "Creatine",
        "Fish Oil (Omega-3)",
        "Vitamin D3",
        "Vitamin B12",
        "Multivitamin",
        "Calcium",
        "Iron"
    ]
)

# ================= CALCULATIONS =================
def calculate_bmr(age, weight, height, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

activity_map = {"Low": 1.2, "Medium": 1.55, "High": 1.75}
goal_map = {"Fat Loss": -500, "Muscle Gain": 300, "Maintenance": 0}

bmr = calculate_bmr(age, weight, height, gender)
tdee = bmr * activity_map[activity]
target_calories = int(tdee + goal_map[goal])
protein_target = int(2 * weight)

# ================= MAIN BUTTON =================
if st.button("🔥 Generate Personalized Diet Plan"):

    if not supplements:
        supplements = ["No supplements selected"]

    # ---------- SUMMARY ----------
    st.markdown("## 📊 Nutrition Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Calories / Day", f"{target_calories} kcal")
    c2.metric("Protein Target", f"{protein_target} g")
    c3.metric("Goal", goal)

    # ---------- GRAPH ----------
    fig, ax = plt.subplots()
    ax.bar(
        ["Protein Calories", "Remaining Calories"],
        [protein_target * 4, target_calories - protein_target * 4]
    )
    ax.set_ylabel("Calories")
    ax.set_title("Daily Macro Distribution")
    st.pyplot(fig)

    # ---------- MEAL PLAN ----------
    st.markdown("## 🍽 Practical Meal Plan (Real Life Based)")

    meal_plan = [
        "Breakfast: Greek Yogurt (200g), Oats (1 bowl)",
        "Lunch: Paneer / Chicken (150g), Rice (1 cup), Sabzi",
        "Dinner: Chicken Breast / Dal, Roti (2)",
        "Snacks: Milk (1 glass), Nuts (small handful)"
    ]

    for meal in meal_plan:
        st.markdown(f"- {meal}")

    # ================= PDF FUNCTION =================
    def generate_pdf_report():
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph(
            "<b>Welcome to Divyansh Fitness & Nutrition Consulting</b>",
            styles["Title"]
        ))
        content.append(Spacer(1, 15))

        content.append(Paragraph(
            "Hello,<br/>"
            "I am <b>Divyansh – Fitness Influencer</b>.<br/>"
            "This is your personalized diet & nutrition report.",
            styles["Normal"]
        ))
        content.append(Spacer(1, 15))

        content.append(Paragraph("<b>User Details</b>", styles["Heading2"]))
        content.append(Paragraph(f"Age: {age}", styles["Normal"]))
        content.append(Paragraph(f"Weight: {weight} kg", styles["Normal"]))
        content.append(Paragraph(f"Height: {height} cm", styles["Normal"]))
        content.append(Paragraph(f"Gender: {gender}", styles["Normal"]))
        content.append(Paragraph(f"Activity Level: {activity}", styles["Normal"]))
        content.append(Paragraph(f"Goal: {goal}", styles["Normal"]))
        content.append(Spacer(1, 12))

        content.append(Paragraph("<b>Daily Nutrition Targets</b>", styles["Heading2"]))
        content.append(Paragraph(f"Calories Required: {target_calories} kcal", styles["Normal"]))
        content.append(Paragraph(f"Protein Target: {protein_target} g", styles["Normal"]))
        content.append(Spacer(1, 12))

        content.append(Paragraph("<b>Meal Plan</b>", styles["Heading2"]))
        for meal in meal_plan:
            content.append(Paragraph(f"- {meal}", styles["Normal"]))

        content.append(Spacer(1, 12))
        content.append(Paragraph("<b>Supplements & Medicines</b>", styles["Heading2"]))
        for supp in supplements:
            content.append(Paragraph(f"- {supp}", styles["Normal"]))

        content.append(Spacer(1, 20))
        content.append(Paragraph(
            "<b>For Paid Consultation & Coaching</b><br/>"
            "📞 Contact: 9336874843",
            styles["Normal"]
        ))

        doc.build(content)
        buffer.seek(0)
        return buffer

    # ================= DOWNLOAD BUTTON =================
    pdf_data = generate_pdf_report()

    st.download_button(
        label="📥 Download Your Diet Report (PDF)",
        data=pdf_data,
        file_name="Divyansh_Fitness_Diet_Report.pdf",
        mime="application/pdf"
    )