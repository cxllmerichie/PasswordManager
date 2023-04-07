from PyQt5.QtWidgets import QStackedWidget, QWidget
from PyQt5.QtCore import Qt

from .sign_in import SignIn
from .sign_up import SignUp
from ..widgets import VLayout, HLayout, Frame
from .left_menu import LeftMenu
from .right_pages import RightPages
from .central_pages import CentralPages
from .panel import Panel


class CentralWidget(QStackedWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self) -> 'CentralWidget':
        self.layout().setAlignment(Qt.AlignHCenter)
        self.addWidget(await SignIn(self).init())
        self.addWidget(await SignUp(self).init())
        self.addWidget(await MainView(self).init())
        self.setCurrentIndex(0)
        self.setCurrentIndex(0) if not self.parent().settings.value('token') else self.setCurrentIndex(2)
        return self


class MainView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self) -> 'MainView':
        vbox = await VLayout().init()
        vbox.addWidget(await Panel(self).init(), alignment=Qt.AlignTop)

        hbox = await HLayout(self).init()
        hbox.addWidget(await LeftMenu(self, 220).init())
        hbox.addWidget(await CentralPages(self).init())
        hbox.addWidget(await RightPages(self, 350).init())

        vbox.addWidget(await Frame(self, 'MainViewFrame').init(layout=hbox))
        self.setLayout(vbox)
        return self
