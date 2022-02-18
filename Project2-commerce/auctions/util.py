import re


class Markdown:
    def __init__(self, in_str: str) -> None:
        self.work_str: str = in_str
        self._parse()

    def _parse(self):
        self._headings()
        self._list()
        self._paragraphs()
        self._links()
        self._bold()

    def _headings(self):
        h = re.compile("(#+)(.*)")
        while m := h.search(self.work_str):
            h_no = len(m.group(1))
            self.work_str = re.sub(
                h, f"<h{h_no}>{m.group(2).strip()}</h{h_no}>", self.work_str, 1
            )

    def _list(self):
        h = re.compile("\n\\*(.*)")
        while m := h.search(self.work_str):
            self.work_str = re.sub(
                h, f"\n<ul>\n\t<li>{m.group(1).strip()}</li>\n</ul>", self.work_str, 1
            )

    def _paragraphs(self):
        h = re.compile("^[A-Za-z].*(?:\n[A-Za-z].*)*", re.M)

        matches = [x for x in h.findall(self.work_str) if x.strip()]
        for m in matches:
            if not re.search(r"^<\/?(ul|ol|li|h|p|bl)", m):
                self.work_str = re.sub(h, f"<p>{m}</p>", self.work_str, 1)

    def _links(self):
        h = re.compile("\\[([^\\[]+)\\]\\(([^\\)]+)\\)", re.M)
        while m := h.search(self.work_str):
            self.work_str = re.sub(
                h, f'<a href="{m.group(2)}">{m.group(1)}</a>', self.work_str, 1
            )

    def _bold(self):
        h = re.compile("(\*\*|__)(.*?)(\*\*|__)", re.M)
        while m := h.search(self.work_str):
            self.work_str = re.sub(
                h, f"<strong>{m.group(2)}</strong>", self.work_str, 1
            )

    def _new_line(self):
        self.work_str = self.work_str.replace("\n", "</br>")

    def __str__(self) -> str:
        return self.work_str
