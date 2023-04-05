from PyQt5.QtWidgets import QScrollArea, QWidget

from ..widgets import Frame, VLayout


class ScrollArea(QScrollArea):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    async def init(self, items: list[QWidget]) -> 'ScrollArea':
        widget = Frame(self, f'{self.objectName()}Widget')
        layout = await VLayout(widget).init()
        for item in items:
            layout.addWidget(item)
        self.setWidget(await widget.init(layout=layout))
        return self
