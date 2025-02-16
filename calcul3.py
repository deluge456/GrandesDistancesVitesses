import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QGroupBox
)
from PyQt6.QtGui import QIcon, QPalette, QColor, QPixmap, QBrush
from PyQt6.QtCore import Qt

# Dictionnaires pour les conversions
distance_units = {
    'mètre (m)': 1,
    'kilomètre (km)': 1e3,
    'unité astronomique (ua)': 1.496e11,
    'année-lumière (al)': 9.461e15,
    'parsec (pc)': 3.086e16
}

time_units = {
    'seconde (s)': 1,
    'minute (min)': 60,
    'heure (h)': 3600,
    'jour (j)': 86400,
    'mois (mois)': 2.628e6,  # Approximativement 30,44 jours
    'année (an)': 3.154e7  # Année civile moyenne
}


class ConvertisseurDistance(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Convertisseur de distances et calculateur de vitesses')
        self.setGeometry(100, 100, 500, 600)

        # Appliquer un fond d'écran
        self.set_background()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)

        # --- Styles personnalisés ---
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: #D8DEE9;
                font-family: Arial;
                font-size: 14px;
            }
            QGroupBox {
                border: 2px solid #81A1C1;
                border-radius: 5px;
                margin-top: 20px;
                background-color: rgba(46, 52, 64, 180);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                background-color: #3B4252;
                border: 1px solid #81A1C1;
                border-radius: 3px;
                padding: 5px;
                color: #D8DEE9;
            }
            QPushButton {
                background-color: #81A1C1;
                border: none;
                color: #2E3440;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #88C0D0;
            }
            QPushButton:pressed {
                background-color: #5E81AC;
            }
            QLabel#result_label, QLabel#speed_result_label {
                margin-top: 10px;
            }
        """)

        # --- Section de conversion de distances ---
        distance_group = QGroupBox('Conversion de distances')
        distance_layout = QVBoxLayout()

        # Valeur à convertir
        self.distance_input = QLineEdit()
        distance_layout.addLayout(self.create_horizontal_layout('Valeur :', self.distance_input))

        # Unité de départ
        self.unit_from = QComboBox()
        self.unit_from.addItems(distance_units.keys())
        distance_layout.addLayout(self.create_horizontal_layout('De :', self.unit_from))

        # Unité d'arrivée
        self.unit_to = QComboBox()
        self.unit_to.addItems(distance_units.keys())
        distance_layout.addLayout(self.create_horizontal_layout('À :', self.unit_to))

        # Bouton de conversion
        self.convert_button = QPushButton('Convertir')
        self.convert_button.clicked.connect(self.convert_distance)
        distance_layout.addWidget(self.convert_button)

        # Affichage du résultat
        self.result_label = QLabel('')
        self.result_label.setObjectName('result_label')
        distance_layout.addWidget(self.result_label)

        distance_group.setLayout(distance_layout)
        self.layout.addWidget(distance_group)

        # --- Section de calcul de vitesses ---
        speed_group = QGroupBox('Calcul de vitesses')
        speed_layout = QVBoxLayout()

        # Distance pour la vitesse
        self.distance_speed_input = QLineEdit()
        self.distance_speed_unit = QComboBox()
        self.distance_speed_unit.addItems(distance_units.keys())
        distance_speed_layout = QHBoxLayout()
        distance_speed_layout.addWidget(QLabel('Distance :'))
        distance_speed_layout.addWidget(self.distance_speed_input)
        distance_speed_layout.addWidget(self.distance_speed_unit)
        speed_layout.addLayout(distance_speed_layout)

        # Temps pour la vitesse
        self.time_input = QLineEdit()
        self.time_unit = QComboBox()
        self.time_unit.addItems(time_units.keys())
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel('Temps :'))
        time_layout.addWidget(self.time_input)
        time_layout.addWidget(self.time_unit)
        speed_layout.addLayout(time_layout)

        # Bouton pour calculer la vitesse
        self.speed_button = QPushButton('Calculer la vitesse')
        self.speed_button.clicked.connect(self.calculate_speed)
        speed_layout.addWidget(self.speed_button)

        # Affichage du résultat de la vitesse
        self.speed_result_label = QLabel('')
        self.speed_result_label.setObjectName('speed_result_label')
        speed_layout.addWidget(self.speed_result_label)

        speed_group.setLayout(speed_layout)
        self.layout.addWidget(speed_group)

        self.setLayout(self.layout)

    def set_background(self):
        # Charger une image de fond
        self.background = QPixmap("background.jpg")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(self.background))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def create_horizontal_layout(self, label_text, widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(100)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def convert_distance(self):
        try:
            valeur = float(self.distance_input.text())
            unite_de = self.unit_from.currentText()
            unite_vers = self.unit_to.currentText()
            en_metre = valeur * distance_units[unite_de]
            resultat = en_metre / distance_units[unite_vers]
            self.result_label.setText(f'{valeur} {unite_de} = <b>{resultat:.5e} {unite_vers}</b>')
        except ValueError:
            self.result_label.setText('<span style="color:red;">Veuillez entrer une valeur numérique valide.</span>')

    def calculate_speed(self):
        try:
            # Récupération et conversion de la distance
            distance_value = float(self.distance_speed_input.text())
            distance_unit = self.distance_speed_unit.currentText()
            distance_in_meters = distance_value * distance_units[distance_unit]

            # Récupération et conversion du temps
            time_value = float(self.time_input.text())
            time_unit = self.time_unit.currentText()
            time_in_seconds = time_value * time_units[time_unit]

            # Calcul de la vitesse en m/s
            vitesse_m_s = distance_in_meters / time_in_seconds

            # Conversion de la vitesse en km/h
            vitesse_km_h = (vitesse_m_s * 3600) / 1000

            self.speed_result_label.setText(
                f'Vitesse : <b>{vitesse_m_s:.5e} m/s</b> | <b>{vitesse_km_h:.5e} km/h</b>'
            )
        except ValueError:
            self.speed_result_label.setText(
                '<span style="color:red;">Veuillez entrer des valeurs numériques valides.</span>')
        except ZeroDivisionError:
            self.speed_result_label.setText('<span style="color:red;">Le temps ne peut pas être zéro.</span>')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConvertisseurDistance()
    window.show()
    sys.exit(app.exec())
