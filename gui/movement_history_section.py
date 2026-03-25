from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QApplication)
from gui.section_base import SectionBase
from models.equipment_movement_history import EquipmentMovementHistory
from models.equipment import Equipment
import sys


class MovementHistorySection(SectionBase):

    def __init__(self):
        super().__init__("📋 История перемещений")
        self.selected_id = None
        self.init_content()
        self.load_data()

    def init_content(self):
        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Фильтр по оборудованию:"))
        
        self.equipment_combo = QComboBox()
        self.equipment_combo.addItem("Все оборудование", None)
        self.load_equipment()
        self.equipment_combo.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(self.equipment_combo)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Инв.номер', 'Оборудование', 'Аудитория', 'Корпус', 'Дата перемещения'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.clicked.connect(self.load_data)
        btn_layout.addWidget(self.refresh_btn)
        
        self.clear_filter_btn = QPushButton("❌ Сбросить фильтр")
        self.clear_filter_btn.clicked.connect(self.clear_filter)
        btn_layout.addWidget(self.clear_filter_btn)
        
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        self.get_content_layout().addLayout(layout)

    def load_equipment(self):
        self.equipment_combo.clear()
        self.equipment_combo.addItem("Все оборудование", None)
        data = Equipment.get_all()
        for row in data:
            self.equipment_combo.addItem(f"{row[1]} - {row[2]}", row[0])

    def load_data(self):
        equipment_id = self.equipment_combo.currentData()
        
        if equipment_id:
            data = EquipmentMovementHistory.get_by_equipment(equipment_id)
        else:
            data = EquipmentMovementHistory.get_all()
        
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))
        
        self.table.resizeColumnsToContents()

    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()

    def clear_filter(self):
        self.equipment_combo.setCurrentIndex(0)
        self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovementHistorySection()
    window.show()
    sys.exit(app.exec_())
