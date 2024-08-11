from PySide2 import QtGui, QtCore, QtWidgets


class TextureRetargeterUI(QtWidgets.QWidget):
    """ Sets up the UI for the texture retarget

    Comprised of MVC tableview, filedialog button and push button

    """
    def __init__(self, model, texture_retargeter):
        super(TextureRetargeterUI, self).__init__()
        self.model = model
        self.texture_retargeter = texture_retargeter

        self.selected_folder = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.Popup)

        main_layout = QtWidgets.QVBoxLayout(self)

        # Create the table view and set the model
        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table_view)

        # Create the horizontal folder label layout
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("Retarget Location: ")
        self.location_label = QtWidgets.QLabel("No folder selected")
        self.horizontal_layout.addWidget(self.label)
        self.horizontal_layout.addWidget(self.location_label)
        main_layout.addLayout(self.horizontal_layout)

        # Create the file browser button
        self.folder_browser_button = QtWidgets.QPushButton("Retarget Folder")
        self.folder_browser_button.clicked.connect(self.open_folder_dialog)
        main_layout.addWidget(self.folder_browser_button)

        # Create the retarget button and link it
        self.retarget_button = QtWidgets.QPushButton("Retarget")
        self.retarget_button.clicked.connect(self.retarget_textures)
        main_layout.addWidget(self.retarget_button)

    def open_folder_dialog(self):
        """ Opens a folder search window.

        Opens a file dialog widget that allows a user to select a folder to
        search for files.

        """
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:  # Update the label only if a folder was selected
            self.selected_folder = folder_path
            self.location_label.setText(folder_path)
            print("Selected folder:", folder_path)

    def retarget_textures(self):
        """ Searches the selected folder for the filenames contained in the
        table

        Uses the selected folder variable and the values of key value pairs in
        the table data to find the name of the value in the folder.

        :return:
        """
        self.texture_retargeter.retarget_from_folder(self.selected_folder)
        new_data = [
            [key, value] for key, value in
            self.texture_retargeter.files_to_retarget.items()
        ]
        self.model.set_all_data(new_data)

        QtWidgets.QMessageBox.information(
            self,
            "Retargeting Complete",
            "The retargeting process has been completed successfully."
        )
