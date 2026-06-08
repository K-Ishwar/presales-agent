
from pdf_generator.generator import generate_pdf

data = {
    "title":"AI Proposal",
    "score":90,
    "strengths":"Good Team",
    "weaknesses":"Budget Risk",
    "pricing":[
        {
            "name":"Development",
            "cost":"5000"
        }
    ]
}

generate_pdf(
    data,
    "final_proposal.pdf"
)

