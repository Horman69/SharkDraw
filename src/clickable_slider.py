# -*- coding: utf-8 -*-
"""
Кастомный слайдер с поддержкой клика по всей полосе
"""

from PyQt5.QtWidgets import QSlider, QStyleOptionSlider, QStyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent


class ClickableSlider(QSlider):
    """Слайдер с поддержкой клика в любом месте для перемещения ползунка"""
    
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Обработка клика мыши - перемещение ползунка в точку клика"""
        if event.button() == Qt.LeftButton:
            # Получаем позицию клика
            if self.orientation() == Qt.Horizontal:
                # Для горизонтального слайдера
                click_pos = event.pos().x()
                slider_width = self.width()
                
                # Вычисляем значение на основе позиции клика
                value_range = self.maximum() - self.minimum()
                new_value = self.minimum() + (click_pos / slider_width) * value_range
                
                # Устанавливаем новое значение
                self.setValue(int(new_value))
            else:
                # Для вертикального слайдера
                click_pos = event.pos().y()
                slider_height = self.height()
                
                # Вычисляем значение (инвертировано для вертикального)
                value_range = self.maximum() - self.minimum()
                new_value = self.maximum() - (click_pos / slider_height) * value_range
                
                # Устанавливаем новое значение
                self.setValue(int(new_value))
            
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Обработка перетаскивания - обновление значения при движении мыши"""
        if event.buttons() & Qt.LeftButton:
            # Аналогично mousePressEvent
            if self.orientation() == Qt.Horizontal:
                click_pos = event.pos().x()
                slider_width = self.width()
                value_range = self.maximum() - self.minimum()
                new_value = self.minimum() + (click_pos / slider_width) * value_range
                self.setValue(int(new_value))
            else:
                click_pos = event.pos().y()
                slider_height = self.height()
                value_range = self.maximum() - self.minimum()
                new_value = self.maximum() - (click_pos / slider_height) * value_range
                self.setValue(int(new_value))
            
            event.accept()
        else:
            super().mouseMoveEvent(event)
