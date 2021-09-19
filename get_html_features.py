import sys
from bs4 import BeautifulSoup, Tag
from typing import List
from elems import *

header_tag_names = [f"h{header_type}" for header_type in range(1, 6 + 1)]
text_tags = header_tag_names + ["p", "span", "div"]


def maybe_create_obj(tag: Tag):
    if not isinstance(tag, Tag):
        return
    is_text = tag.name in text_tags and tag.string
    if is_text:
        return TextElem(tag)

    is_img = False
    try:
        is_img = "background-image" in tag["style"]
    except:
        pass
    is_img = is_img or tag.name in ["svg", "canvas"]

    if is_img:
        return ImgElem(tag)

    is_button = tag.name == "button"
    if not is_button:
        if tag.has_attr("href") and tag.name not in ["link"]:
            is_button = is_button or tag["href"] is not None
        if tag.has_attr("onclick"):
            is_button = is_button or tag["onclick"] is not None
    if is_button:
        #         print("button", tag)
        return ButtonElem(tag)

    is_input = tag.name == "input"
    if is_input:
        return InputElem(tag)


def soup_dfs(tags: List[Tag], valuable_elements):
    for tag in tags:
        obj = maybe_create_obj(tag)
        if obj is not None:
            valuable_elements.append(obj)

        if hasattr(tag, "children"):
            soup_dfs(list(tag.children), valuable_elements)


def get_features(file_pth):
    with open(file_pth) as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")

    valuable_elements = []
    soup_dfs(soup.children, valuable_elements)

    uniq_elems = []
    for elem in valuable_elements:
        if elem not in uniq_elems:
            uniq_elems.append(elem)

    return uniq_elems


if __name__ == "__main__":
    features = get_features(sys.argv[1])

    print(f"Элементы, извлечённый из {sys.argv[1]}:")
    for elem in features:
        print(elem)
