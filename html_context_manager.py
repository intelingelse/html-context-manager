class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "</html>"
        return html


class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        html = f"<{self.tag}>\n"
        for child in self.children:
            html += "\t" + str(child) + "\n"
        html += f"</{self.tag}>\n"
        return html


class Tag:
    def __init__(self, tag, klass=None, **kwargs):
        self.tag = tag
        self.text = ""

        self.attributes = {}

        self_closing_tags = {
            "area", "base", "br", "col", "command",
            "embed", "hr", "img", "input", "keygen",
            "link", "menu", "item", "meta", "param",
            "source", "track", "wbr"}

        self.is_single = True if self.tag in self_closing_tags else False

        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(f'{attribute}="{value}"')
        attrs = " ".join(attrs)

        if len(self.children) > 0:
            if attrs:
                opening = f"<{self.tag} {attrs}>"
            else:
                opening = f"<{self.tag}>"

            if self.text and not self.is_single:
                internal = f"{self.text}"
            else:
                internal = ""
            for child in self.children:
                internal += "\n\t\t" + str(child)
            ending = f"\n\t</{self.tag}>"
            return opening + internal + ending
        else:
            if self.is_single and attrs:
                return f"<{self.tag} {attrs}/>"
            elif self.is_single and not attrs:
                return f"<{self.tag}/>"
            elif not self.is_single and attrs:
                return f"<{self.tag} {attrs}>{self.text}</{self.tag}>"
            else:
                return f"<{self.tag}>{self.text}</{self.tag}>"


def main(output=None):
    with HTML() as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("hr", klass=("main-line", "sep-line")) as hr:
                hr.text="sup"
                body+=hr

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag(
                        "img", is_single=True, src="/icon.png", data_image="responsive"
                ) as img:
                    div += img

                body += div

            doc += body


if __name__ == "__main__":
    main()
