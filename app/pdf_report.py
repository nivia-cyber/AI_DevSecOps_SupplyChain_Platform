from fpdf import FPDF

def generate_pdf(event):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200,10,"AI DevSecOps Security Report", ln=True)
    pdf.cell(200,10,f"Artifact: {event['artifact']}", ln=True)
    pdf.cell(200,10,f"Risk Score: {event['risk_score']}", ln=True)
    pdf.cell(200,10,f"Status: {event['status']}", ln=True)

    pdf.output("security_report.pdf")