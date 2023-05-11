from qcontext.widgets import Window
from qcontext import CONTEXT
from PyQt5.QtCore import Qt


class App(Window):
    # all imports must be placed only in the class, otherwise `Process finished with exit code -1073740791 (0xC0000409)`
    # issue: while running (init load) it sees the import and usage from PyQt5 in `assets`, and PyQt5 itself conflicts
    # with main created thread in `main.py` creating more threads in `assets`

    def __init__(self):
        from . import stylesheets

        super().__init__(self.__class__.__name__, stylesheet=stylesheets.status_bar.css +
                                                             stylesheets.app.css)

    async def init(self) -> 'App':
        from .misc import SIZES

        self.resize(SIZES.App)
        self.setWindowFlag(Qt.FramelessWindowHint)
        if not CONTEXT['storage']:
            from .components import IntroPopup

            fspopup = await IntroPopup(self).init()
        else:
            from .views.central_widget import CentralWidget
            from desktop.src.components.status_bar import StatusBar

            statusbar = await StatusBar(self).init()
            self.setCentralWidget(await CentralWidget(self).init())
            self.setStatusBar(statusbar)
            await statusbar.post_init()
        return self
