import icalendar
from qgis.core import QgsMessageLog, Qgis
from qgis.PyQt.QtWidgets import QFileDialog

from comptages.core.utils import push_info


class IcsImporter:
    def __init__(self, layers):
        self.layers = layers
        self.ask_for_file()

    def ask_for_file(self):
        file_dialog = QFileDialog()
        title = "Importer fichier ics"
        path = "/"
        file_path = QFileDialog.getOpenFileName(
            file_dialog, title, path, "Data file (*.ICS *.ics)"
        )[0]

        if not file_path:
            return

        self.import_file(file_path)

    def import_file(self, file_path):
        ics = open(file_path, "rb")
        cal = icalendar.Calendar.from_ical(ics.read())
        ics.close()

        for event in cal.walk("vevent"):
            if "DTSTART" not in event and "DTEND" not in event:
                continue

            summary = ""
            if "SUMMARY" in event:
                summary = str(event["SUMMARY"])

            location = ""
            if "LOCATION" in event:
                location = str(event["LOCATION"])

            self.layers.write_special_period(
                event["DTSTART"].dt, event["DTEND"].dt, summary, location, ""
            )

            # str(event['PRIORITY'])
            # event['CATEGORIES'].cats

        push_info("Importation terminée")
        QgsMessageLog.logMessage("Import ics finished", "Comptages", Qgis.Info)
