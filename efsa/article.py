class Article:
    def __init__(self, ref_id, title, text):
        self.ref_id = ref_id
        self.title = title
        self.text = text

    def __repr__(self):
        return 'Article(RefId: %s, Title=%s)' % (self.ref_id, self.title)
