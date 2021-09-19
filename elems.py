from bs4 import Tag


class Elem:
    def __eq__(self, other):
        return isinstance(self, other.__class__) or isinstance(other, self.__class__)


class TextElem(Elem):
    def __init__(self, tag: Tag):
        self.category = "text"
        self.tag = tag

        self.text = tag.string
        self.text_eq = "".join([line.strip() for line in self.text.split()])

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        #         print("eq of texts", self)
        #         print("other", other)
        #         print(self.text == other.text)
        return self.text_eq == other.text_eq

    def __repr__(self):
        return f"TextElem(text: {self.text})"


class ImgElem(Elem):
    def __init__(self, tag: Tag):
        self.category = "image"
        #         print("create img elem", tag)
        self.tag = tag
        if self.tag.has_attr("class"):
            self.tag_class = self.tag["class"]
        else:
            self.tag_class = None

        self.is_picture = tag.name in ["svg", "canvas"]
        self.url = None
        if not self.is_picture:
            self.url = tag["style"][tag["style"].find("url(") + 5: -3]

    def __repr__(self):
        return f"ImgElem(is_picture: {self.is_picture}, url: {self.url}, class: {self.tag_class})"

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if self.is_picture:
            if self.tag.has_attr("class") and other.tag.has_attr("class"):
                return self.tag["class"] == other.tag["class"]
            else:
                return True
        #                 # both don't have classes
        #                 return ("class" not in self.tag) and ("class" not in other.tag)

        else:
            return self.url == other.url


class ButtonElem(Elem):
    def __init__(self, tag: Tag):
        self.category = "button"
        self.tag = tag

        self.action = None

        if self.tag.has_attr("href"):
            self.href = self.tag["href"]
        else:
            self.href = None

        if self.tag.name == "button":
            self.action = self.tag.text.strip()
        else:
            #             print("beb", tag)
            if self.tag.has_attr("onclick"):
                self.action = self.tag["onclick"]
            else:
                self.action = self.tag["href"]

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        #         print("Compare", self.action, other.action)
        return self.action == other.action

    def __repr__(self):
        return f"ButtonElem(action: {self.action})"


class InputElem(Elem):
    def __init__(self, tag: Tag):
        self.category = "input"
        self.tag = tag
        self.placeholder = self.tag["placeholder"] if self.tag.has_attr("placeholder") else None

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return self.placeholder == other.placeholder or (self.placeholder is None and other.placeholder is None)

    def __repr__(self):
        return f"InputElem(placeholder: {self.placeholder})"
