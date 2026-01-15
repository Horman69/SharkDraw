# -*- coding: utf-8 -*-
"""
Инструменты для рисования
Содержит базовый класс Tool и реализации различных инструментов
"""

from abc import ABC, abstractmethod
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QColor
import math


class Tool(ABC):
    """Базовый класс для всех инструментов рисования"""
    
    def __init__(self, color: QColor, width: int):
        """
        Инициализация инструмента
        
        Args:
            color: Цвет рисования
            width: Толщина линии
        """
        self.color = color
        self.width = width
        self.start_point = None
        self.end_point = None
        self.points = []  # Для инструментов с множественными точками
    
    @abstractmethod
    def draw(self, painter: QPainter):
        """Отрисовка инструмента"""
        pass
    
    def set_start_point(self, point: QPoint):
        """Установить начальную точку"""
        self.start_point = point
    
    def set_end_point(self, point: QPoint):
        """Установить конечную точку"""
        self.end_point = point
    
    def add_point(self, point: QPoint):
        """Добавить точку в список (для свободного рисования)"""
        self.points.append(point)


class PenTool(Tool):
    """Инструмент карандаш - свободное рисование"""
    
    def draw(self, painter: QPainter):
        """Отрисовка линии по точкам"""
        if len(self.points) < 2:
            return
        
        pen = QPen(self.color, self.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        
        for i in range(1, len(self.points)):
            painter.drawLine(self.points[i - 1], self.points[i])


class LineTool(Tool):
    """Инструмент линия - прямая линия"""
    
    def draw(self, painter: QPainter):
        """Отрисовка прямой линии"""
        if not self.start_point or not self.end_point:
            return
        
        pen = QPen(self.color, self.width, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(self.start_point, self.end_point)


class RectangleTool(Tool):
    """Инструмент прямоугольник"""
    
    def draw(self, painter: QPainter):
        """Отрисовка прямоугольника"""
        if not self.start_point or not self.end_point:
            return
        
        pen = QPen(self.color, self.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        # Вычисляем координаты прямоугольника
        x = min(self.start_point.x(), self.end_point.x())
        y = min(self.start_point.y(), self.end_point.y())
        width = abs(self.end_point.x() - self.start_point.x())
        height = abs(self.end_point.y() - self.start_point.y())
        
        painter.drawRect(x, y, width, height)


class CircleTool(Tool):
    """Инструмент круг/эллипс"""
    
    def draw(self, painter: QPainter):
        """Отрисовка круга/эллипса"""
        if not self.start_point or not self.end_point:
            return
        
        pen = QPen(self.color, self.width, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        # Вычисляем координаты эллипса
        x = min(self.start_point.x(), self.end_point.x())
        y = min(self.start_point.y(), self.end_point.y())
        width = abs(self.end_point.x() - self.start_point.x())
        height = abs(self.end_point.y() - self.start_point.y())
        
        painter.drawEllipse(x, y, width, height)


class ArrowTool(Tool):
    """Инструмент стрелка"""
    
    def draw(self, painter: QPainter):
        """Отрисовка стрелки с наконечником"""
        if not self.start_point or not self.end_point:
            return
        
        pen = QPen(self.color, self.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        
        # Рисуем основную линию
        painter.drawLine(self.start_point, self.end_point)
        
        # Вычисляем угол стрелки
        dx = self.end_point.x() - self.start_point.x()
        dy = self.end_point.y() - self.start_point.y()
        angle = math.atan2(dy, dx)
        
        # Размер наконечника стрелки
        arrow_size = max(15, self.width * 3)
        arrow_angle = math.pi / 6  # 30 градусов
        
        # Вычисляем точки наконечника
        point1 = QPoint(
            int(self.end_point.x() - arrow_size * math.cos(angle - arrow_angle)),
            int(self.end_point.y() - arrow_size * math.sin(angle - arrow_angle))
        )
        point2 = QPoint(
            int(self.end_point.x() - arrow_size * math.cos(angle + arrow_angle)),
            int(self.end_point.y() - arrow_size * math.sin(angle + arrow_angle))
        )
        
        # Рисуем наконечник
        painter.drawLine(self.end_point, point1)
        painter.drawLine(self.end_point, point2)


class EraserTool(Tool):
    """Инструмент ластик - удаление рисунков"""
    
    def __init__(self, color: QColor, width: int):
        super().__init__(color, width * 3)  # Ластик в 3 раза толще
    
    def draw(self, painter: QPainter):
        """Ластик не рисует, а удаляет (обрабатывается в canvas)"""
        pass
