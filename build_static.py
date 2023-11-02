import os
import shutil

import yaml

from app import app


def validate_pages(pages):
    paths = []

    for page in pages:

        if page["path"] in paths:
            raise Exception(f"Page `{page['path']}` is not unique !")
        else:
            paths.append(page["path"])

        if os.path.exists(f"./build/{page['path']}"):
            raise Exception(f"File {page['path']} already exists.")


def build(pages):
    cli = app.test_client()
    for page in pages:
        r = cli.get(f"/{page['path']}")
        folder, name = os.path.split(page['path'])
        if folder:
            os.makedirs(f"./build/{folder}", exist_ok=True)

        with open(f"./build/{page['path']}", "w") as f:
            f.write(r.data.decode())

    shutil.copytree("./static", "./build/static", dirs_exist_ok=True)


def main():
    with open("./blog.yaml") as fblog:
        blog = yaml.safe_load(fblog.read())

    with open("./posts/publish.yaml") as fpublish:
        posts = yaml.safe_load(fpublish.read())

    pages = blog["pages"] + posts
    validate_pages(pages)
    build(pages)


if __name__ == '__main__':
    main()
