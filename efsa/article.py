class Article:
    def __init__(self, ref_id, title, sections, abstract_text):
        self.ref_id = ref_id
        self.title = title
        self.sections = sections
        self.abstract_text = abstract_text
        self.body_text = self.get_body_text()

    def __repr__(self):
        return 'Article(RefId: %s, Title=%s)' % (self.ref_id, self.title)

    def get_body_text(self):
        body_text = []
        if self.abstract_text:
            body_text.append(self.abstract_text)

        for section in self.sections:
            if "heading" in section:
                body_text.append(section['heading'])
            if "text" in section:
                body_text.append(section['text'])
        return " ".join(body_text)
