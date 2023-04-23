from PyQt5.QtWidgets import QApplication
import sys

from src import App


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    app = App().init()
    app.show()
    sys.exit(qapp.exec_())


# ToDo: fix QPushButton.disabled Icon
# ToDo: Fix 'elided' in CentralPagesItems when resizing SplitterWidgets
# ToDo: Display Category.title (or topic as All/Favourite) when displaying items
# ToDo: when SplitterWidget resized to max resizing the app through Panel breaks
# ToDo: Fix min/max App size (caused by min-size of inner widgets)
# ToDo: Change SplitterHandle color
# ToDo: Item attachments
# ToDo: user profile and settings
# ToDo: local/remote storage (fetch from both if local chosen, any new added to local, colors of local/remote are different)

# ToDo: add password generating procedure (fetch from api)
# ToDo: create "Loader" using threads while waiting for displaying items in CentralPagesItems
# ToDo: multilang (translations)
