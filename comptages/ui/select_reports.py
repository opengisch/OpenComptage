from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QRadioButton,
    QVBoxLayout,
    QScrollArea,
    QWidget,
)


class SelectSectionsToReport(QDialog):
    def __init__(self, *args, **kwargs):
        self.items = kwargs.pop("sections_ids")

        super().__init__(*args, **kwargs)

        self.setMinimumWidth(550)
        self.setWindowTitle("Please select the sections to include in the report...")
        self.layout = QVBoxLayout()

        # Parent layout
        self.layout = QVBoxLayout()

        # Basic controls
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Radio: all
        self.all_selector = QRadioButton()
        self.all_selector.setChecked(True)
        self.all_selector.toggled.connect(lambda: self.select("all"))
        self.all_selector_label = QLabel()
        self.all_selector_label.setText("Select all")
        self.all_selector_label.setBuddy(self.all_selector)
        self.layout.addWidget(self.all_selector_label)
        self.layout.addWidget(self.all_selector)

        # Radio: none
        self.none_selector = QRadioButton()
        self.none_selector.toggled.connect(lambda: self.select("none"))
        self.none_selector_label = QLabel()
        self.none_selector_label.setText("Unselect all")
        self.none_selector_label.setBuddy(self.none_selector)
        self.layout.addWidget(self.none_selector_label)
        self.layout.addWidget(self.none_selector)

        # Checkboxes: containers
        self.scrollarea = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        # Checkboxes: items
        self.items_check_boxes = {}
        for item in self.items:
            check_box = QCheckBox(item)
            check_box.setChecked(True)
            check_box.clicked.connect(self.update_selected)
            label = QLabel()
            label.setBuddy(check_box)
            self.vbox.addWidget(label)
            self.vbox.addWidget(check_box)
            self.items_check_boxes[item] = check_box

        # Checkbox: containers: populate layout
        self.widget.setLayout(self.vbox)
        self.scrollarea.setWidget(self.widget)
        self.layout.addWidget(self.scrollarea)

        # Selected
        self.selected = QLabel()
        selected_text = f"Selected: {self.count_selected()} out of {len(self.items)}"
        self.selected.setText(selected_text)
        self.layout.addWidget(self.selected)

        # Buttons
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def update_selected(self):
        self.selected.setText(
            f"Selected: {self.count_selected()} out of {len(self.items)}"
        )

    def count_selected(self) -> int:
        return len(
            [
                checkbox
                for checkbox in self.items_check_boxes.values()
                if checkbox.isChecked()
            ]
        )

    def select(self, desired: str):
        for check_box in self.items_check_boxes.values():
            check_box.setChecked(desired == "all")
        self.update_selected()

    def get_inputs(self) -> list[str]:
        return [
            item.text() for item in self.items_check_boxes.values() if item.isChecked()
        ]
