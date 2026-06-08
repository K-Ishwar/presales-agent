from jinja2 import Environment
from jinja2 import FileSystemLoader

env = Environment(
    loader=FileSystemLoader(
        "pdf_generator/templates"
    )
)

template = env.get_template(
    "proposal.html"
)

data = {
    "title": "AI Proposal",
    "score": 95,
    "strengths": "Strong AI Team",
    "weaknesses": "Limited Timeline",
    "pricing": [
        {"name":"Development","cost":"5000"},
        {"name":"Hosting","cost":"1000"}
    ]
}

html = template.render(data)

with open(
    "preview.html",
    "w",
    encoding="utf-8"
) as f:
    f.write(html)