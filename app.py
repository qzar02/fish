from datetime import date

import yaml
from flask import Flask, abort, render_template

app = Flask(__name__)
app.jinja_env.add_extension('jinja_markdown.MarkdownExtension')

blog = yaml.safe_load(open("blog.yaml").read())
publish = yaml.safe_load(open("posts/publish.yaml").read())
draft = yaml.safe_load(open("posts/publish.yaml").read())


@app.route("/<path:path>")
def page(path):

    for post in (publish + draft + blog["pages"]):
        if post["path"] == path:
            break
    else:
        abort(404)

    context = {
        "blog": blog,
        "today": date.today,
        "post": post,
        "publish": publish
    }

    return render_template(post["template"], **context)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(port=5432)
