import json

import markdown
from frictionless import Package
from slugify import slugify


def read_datapackage(template):
    package = Package("datapackage.json")
    return {
        "json": json.dumps(
            package.to_dict(), sort_keys=True, indent=2, separators=(",", ": ")
        )
    }


def read_csv(template):
    package = Package("datapackage.json")
    resource_name = template.name.split("/")[1].replace(".csv", "")
    resource = package.get_resource(resource_name)
    data = [row.to_dict() for row in resource.read_rows()]
    for item in data:
        item["slug"] = slugify(f"{resource['name']}-item-{item['version']}")
    data = sorted(data, key=lambda k: k["date"])
    return {"data": data, "filename": template.name, "resource": resource}


def read_markdown(template):
    markdown_formatter = markdown.Markdown(output_format="html5")
    with open(template.filename) as markdownfile:
        markdown_content = markdownfile.read()
        return {"html": markdown_formatter.convert(markdown_content)}
