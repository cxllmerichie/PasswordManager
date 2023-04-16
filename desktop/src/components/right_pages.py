from PyQt5.QtWidgets import QStackedWidget, QWidget

from .category import Category
from .item import Item
from ..widgets import SideMenu
from .. import css


class RightPages(QStackedWidget, SideMenu):
    def __init__(self, parent: QWidget, width: int):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(css.right_pages.css)

        self.expand_to = width

    def init(self) -> 'RightPages':
        self.addWidget(Category(self).init())
        self.addWidget(Item(self).init())
        self.shrink()
        return self
