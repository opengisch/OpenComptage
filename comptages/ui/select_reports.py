from datetime import datetime
from functools import partial
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QScrollArea,
    QWidget,
)


class SelectSectionsToReport(QDialog):
    fmt = "%d-%m-%Y"

    def __init__(self, *args, **kwargs):
        sections_ids: list[str] = kwargs.pop("sections_ids")
        mondays: list[datetime] = kwargs.pop("mondays")
        mondays_as_datestr = [d.strftime(self.fmt) for d in mondays]

        super().__init__(*args, **kwargs)

        self.max_selected = len(sections_ids) * len(mondays)
        self.setMinimumWidth(550)
        self.setWindowTitle(
            "Please select the sections and dates to include in the report..."
        )
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
        self.all_selector.toggled.connect(partial(self.select_all_none, "all"))
        self.all_selector_label = QLabel()
        self.all_selector_label.setText("Select all")
        self.all_selector_label.setBuddy(self.all_selector)
        self.layout.addWidget(self.all_selector_label)
        self.layout.addWidget(self.all_selector)

        # Radio: none
        self.none_selector = QRadioButton()
        self.none_selector.toggled.connect(partial(self.select_all_none, "none"))
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
        for item in sections_ids:
            item_checkbox = QCheckBox(f"section {item}")
            item_checkbox.setChecked(True)
            item_checkbox.clicked.connect(partial(self.update_children_of, item))
            label = QLabel()
            label.setBuddy(item_checkbox)

            self.vbox.addWidget(label)
            self.vbox.addWidget(item_checkbox)
            self.items_check_boxes[item] = {
                "checkbox": item_checkbox,
                "subcheckboxes": {},
            }

            # Checkboxes: subitems
            for subitem in mondays_as_datestr:
                subitem_checkbox = QCheckBox(subitem)
                subitem_checkbox.setStyleSheet("QCheckBox { padding-left: 15px; }")
                subitem_checkbox.setChecked(True)
                subitem_checkbox.clicked.connect(self.update_selected_count)
                label = QLabel()
                label.setBuddy(subitem_checkbox)

                self.vbox.addWidget(label)
                self.vbox.addWidget(subitem_checkbox)
                self.items_check_boxes[item]["subcheckboxes"][
                    subitem
                ] = subitem_checkbox

        # Checkbox: containers: populate layout
        self.widget.setLayout(self.vbox)
        self.scrollarea.setWidget(self.widget)
        self.layout.addWidget(self.scrollarea)

        # Selected
        self.selected = QLabel()
        selected_text = f"Selected: {self.count_selected()} out of {self.max_selected}"
        self.selected.setText(selected_text)
        self.layout.addWidget(self.selected)

        # Buttons
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def update_selected_count(self):
        self.selected.setText(
            f"Selected: {self.count_selected()} out of {self.max_selected}"
        )

    def count_selected(self) -> int:
        count = 0
        for item in self.items_check_boxes.values():
            if item["checkbox"].isChecked():
                for subcheckbox in item["subcheckboxes"].values():
                    if subcheckbox.isChecked():
                        count += 1
        return count

    def update_children_of(self, item: str):
        new_state = self.items_check_boxes[item]["checkbox"].isChecked()
        for subcheckbox in self.items_check_boxes[item]["subcheckboxes"].values():
            subcheckbox.setChecked(new_state)
        self.update_selected_count()

    def select_all_none(self, desired: str):
        new_state = desired == "all"
        for item in self.items_check_boxes.values():
            item["checkbox"].setChecked(new_state)
            for subcheckbox in item["subcheckboxes"].values():
                subcheckbox.setChecked(new_state)
        self.update_selected_count()

    def get_inputs(self) -> dict[str, list[str]]:
        builder = {}
        for section_id, item in self.items_check_boxes.items():
            builder[section_id] = [
                datetime.strptime(monday_datestr, self.fmt)
                for monday_datestr, subcheckbox in item["subcheckboxes"].items()
                if subcheckbox.isChecked()
            ]
        return builder
