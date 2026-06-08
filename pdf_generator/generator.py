from jinja2 import Environment
from jinja2 import FileSystemLoader

from weasyprint import HTML

def generate_pdf(data, output_path):

    env = Environment(
        loader=FileSystemLoader(
            "pdf_generator/templates"
        )
    )

    template = env.get_template(
        "proposal.html"
    )

    html = template.render(**data)

    HTML(
        string=html
    ).write_pdf(
        output_path
    )