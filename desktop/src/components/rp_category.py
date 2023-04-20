from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from typing import Any

from ..widgets import Button, LineInput, Layout, Label, TextInput, Spacer, Frame, ui
from ..custom import FavouriteButton, ImageButton
from ..misc import Icons, api
from .. import css


class RP_Category(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.rp_category.css + css.components.fav_btn + css.components.img_btn)
        self.category = None

    def init(self) -> 'RP_Category':
        self.setLayout(Layout.vertical().init(
            spacing=20, margins=(25, 10, 25, 20),
            items=[
                Layout.horizontal().init(
                    margins=(0, 0, 0, 20),
                    items=[
                        FavouriteButton(self).init(
                            icon=Icons.STAR.adjusted(size=(30, 30)), slot=self.toggle_favourite
                        ), Layout.Left,
                        Button(self, 'EditBtn', False).init(
                            icon=Icons.EDIT.adjusted(size=(30, 30)), slot=self.execute_edit
                        ),
                        Button(self, 'DeleteBtn', False).init(
                            icon=Icons.TRASH.adjusted(size=(30, 30)), slot=self.execute_delete
                        ),
                        Button(self, 'CloseBtn').init(
                            icon=Icons.CROSS.adjusted(size=(30, 30)), slot=ui.RightPages.shrink
                        ), Layout.Right
                    ]
                ),
                ImageButton(self).init(
                    icon=Icons.CATEGORY
                ), Layout.TopCenter,
                LineInput(self, 'TitleInput').init(
                    placeholder='title'
                ), Layout.Top,
                TextInput(self, 'DescriptionInput').init(
                    placeholder='description (optional)'
                ), Layout.Top,
                Spacer(False, True),
                Label(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                Button(self, 'CreateBtn').init(
                    text='Create', slot=self.execute_create
                ), Layout.HCenter,
                Frame(self, 'SaveCancelFrame', False).init(
                    layout=Layout.horizontal().init(
                        spacing=50,
                        items=[
                            Button(self, 'SaveBtn').init(
                                text='Save', slot=self.execute_save
                            ), Layout.Left,
                            Button(self, 'CancelBtn').init(
                                text='Cancel', slot=self.execute_cancel
                            ), Layout.Right
                        ]
                    )
                ), Layout.HCenter,
                Button(self, 'AddItemBtn', False).init(
                    text='Add item', icon=Icons.PLUS, slot=self.add_item
                )
            ]
        ))
        self.FavouriteButton.is_favourite = False
        return self

    @pyqtSlot()
    def toggle_favourite(self):
        if self.category:
            category = {'title': self.TitleInput.text(), 'is_favourite': self.FavouriteButton.is_favourite}
            self.category = api.update_category(self.category['id'], category)
            ui.LeftMenu.refresh_categories(api.get_categories())

    @pyqtSlot()
    def add_item(self):
        Item = self.RightPages.RP_Item
        Item.category_id = self.category['id']
        self.RightPages.setCurrentWidget(Item)
        Item.show_create()

    def show_create(self):
        self.category = None
        self.CreateBtn.setVisible(True)
        self.EditBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(False)
        self.ImageButton.setDisabled(False)
        self.ImageButton.setIcon(Icons.CATEGORY.icon)
        self.FavouriteButton.unset_favourite()
        self.TitleInput.setEnabled(True)
        self.TitleInput.setText('')
        self.DescriptionInput.setDisabled(False)
        self.DescriptionInput.setText('')

        ui.RightPages.setCurrentWidget(ui.RP_Category)
        ui.RightPages.expand()

    @pyqtSlot()
    def execute_delete(self):
        if (category := api.delete_category(self.category['id'])).get('id'):
            self.category = None
            self.TitleInput.setText('')
            self.DescriptionInput.setText('')
            self.DeleteBtn.setVisible(False)
            self.show_create()
            ui.LeftMenu.refresh_categories(api.get_categories())
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def execute_edit(self):
        self.CreateBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(True)
        self.AddItemBtn.setVisible(False)
        self.ImageButton.setDisabled(False)
        self.EditBtn.setVisible(False)
        self.TitleInput.setEnabled(True)
        self.DescriptionInput.setDisabled(False)
        self.DeleteBtn.setVisible(True)

    @pyqtSlot()
    def execute_save(self):
        if not len(title := self.TitleInput.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        category = {'icon': self.ImageButton.icon_bytes, 'title': title,
                    'description': self.DescriptionInput.toPlainText(), 'is_favourite': self.FavouriteButton.is_favourite}
        if (category := api.update_category(self.category['id'], category)).get('id'):
            self.execute_cancel()
            self.category = category
        else:
            self.ErrorLbl.setText('Internal error, please try again')
        self.EditBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        ui.LeftMenu.refresh_categories(api.get_categories())

    @pyqtSlot()
    def execute_cancel(self):
        self.ErrorLbl.setText('')
        self.TitleInput.setEnabled(False)
        self.ImageButton.setDisabled(True)
        self.DescriptionInput.setDisabled(True)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.EditBtn.setVisible(True)

    def show_category(self, category: dict[str, Any]):
        self.category = category
        self.FavouriteButton.set(category['is_favourite'])
        self.TitleInput.setEnabled(False)
        self.TitleInput.setText(category['title'])
        self.ImageButton.setDisabled(True)
        self.ImageButton.setIcon(Icons.from_bytes(category['icon']).icon)
        self.DescriptionInput.setText(category['description'])
        self.DescriptionInput.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(True)
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)

        ui.RightPages.setCurrentWidget(ui.RP_Category)
        ui.RightPages.expand()

        ui.CentralPages.setCurrentWidget(ui.CP_Items)
        ui.CP_Items.refresh_items(category['items'])

    @pyqtSlot()
    def execute_create(self):
        title = self.TitleInput.text()
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        category = {
            'icon': self.ImageButton.icon_bytes, 'title': title,
            'description': self.DescriptionInput.toPlainText(), 'is_favourite': self.FavouriteButton.is_favourite
        }
        if (category := api.create_category(category)).get('id'):
            self.category = category
            self.TitleInput.setText(category['title'])
            self.ImageButton.setIcon(Icons.from_bytes(category['icon']).icon)
            self.ImageButton.setDisabled(True)
            self.ErrorLbl.setText('')
            self.TitleInput.setEnabled(False)
            self.DescriptionInput.setDisabled(True)
            self.AddItemBtn.setVisible(True)
            self.CreateBtn.setVisible(False)
            self.EditBtn.setVisible(True)
        else:
            self.ErrorLbl.setText('Internal error, please try again')
        ui.LeftMenu.refresh_categories(api.get_categories())
