from datetime import date

import yaml

from flask import Flask, abort, render_template

app = Flask(__name__)

blog = yaml.safe_load(open("blog.yaml").read())
publish = yaml.safe_load(open("posts/publish.yaml").read())
draft = yaml.safe_load(open("posts/publish.yaml").read())


def get_context(path):
    post = [
        post
        for post in (publish + draft + blog["pages"])
        if post["path"] == path
    ]

    post = post[0] if post else None
    context = {"blog": blog, "today": date.today, "post": post, "publish": publish}
    return context


@app.route("/<path:path>")
def page(path):
    context = get_context(path)
    post = context["post"]
    if post is None:
        abort(404)
    return render_template(post["template"], **context)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(port=5432)
