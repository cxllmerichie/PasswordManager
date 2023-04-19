from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import Qt

from ._wrapper import Wrapper


class StackedWidget(Wrapper, QStackedWidget):
    def __init__(self, parent: QWidget, name: str, visible: bool = True, stylesheet: str = None):
        QStackedWidget.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)
        if stylesheet:
            self.setStyleSheet(stylesheet)
            self.setAttribute(Qt.WA_StyledBackground, True)

        # костыль мирового масштаба, причина появления проблемы неизвестна
        # бех этой хуйни, первый виджет в стаке имеет проблемы с родителем
        # починка костыля включает в себя перезапись метода `setCurrentIndex`
        self.addWidget(QWidget(self))

    def setCurrentIndex(self, index: int) -> None:
        super().setCurrentIndex(index + 1)
