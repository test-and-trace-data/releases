from slugify import slugify


def render_csv(env, template, **kwargs):

    # render the original file
    output_path = f"{env.outpath}/{template.name}"
    template.stream(**kwargs).dump(output_path)

    # render the html table version
    csv_template = env.get_template("_csv_table.html")
    output_path = f"{env.outpath}/{template.name.replace('.csv','.html')}"
    csv_template.stream(**kwargs).dump(output_path)

    # render the html list items
    resource = kwargs["resource"]
    data_dir = template.name.split("/")[0]
    for item in resource:
        csv_template = env.get_template("_csv_item.html")
        slug = slugify(f"{resource['name']}-item-{item['version']}")
        output_path = f"{env.outpath}/{data_dir}/{slug}.html"
        csv_template.stream(item=item, **kwargs).dump(output_path)


def render_datapackage(env, template, **kwargs):

    # render the html version
    datapackage_template = env.get_template("_datapackage.html")
    output_path = f"{env.outpath}/{template.name.replace('.json','.html')}"
    datapackage_template.stream(**kwargs).dump(output_path)

    # render the original file too
    output_path = f"{env.outpath}/{template.name}"
    template.stream(**kwargs).dump(output_path)


def render_markdown(env, template, **kwargs):
    content_template = env.get_template("_content.html")
    output_path = f"{env.outpath}/{template.name.replace('.md','.html')}"
    content_template.stream(**kwargs).dump(output_path)
