# -*- coding: utf-8 -*-
"""
Прозрачный холст для рисования
Полноэкранное прозрачное окно поверх всех приложений
"""

from typing import Optional, List
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QCursor, QRegion, QPaintEvent, QMouseEvent
from src.config import (ToolType, MAX_DRAWINGS, DEBUG_MODE, 
                        ERASER_RADIUS_MULTIPLIER, OVERLAY_OPACITY, MOUSE_LOG_INTERVAL)
from src.tools import PenTool, LineTool, RectangleTool, CircleTool, ArrowTool, EraserTool, Tool


class TransparentCanvas(QWidget):
    """Прозрачный холст для рисования поверх экрана"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Список завершённых рисунков
        self.drawings = []
        
        # Текущий инструмент в процессе рисования
        self.current_tool = None
        
        # Настройки текущего инструмента
        self.current_tool_type = ToolType.PEN
        self.current_color = QColor(255, 59, 48)  # Красный по умолчанию
        self.current_width = 3
        
        # Флаг активности рисования
        self.is_drawing = False
        
        # Область панели инструментов (чтобы не перехватывать клики на ней)
        self.toolbar_rect = None
    
    def init_ui(self) -> None:
        """Инициализация интерфейса окна"""
        # Получаем размеры экрана
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        # Настройки окна
        self.setWindowTitle('PaintPro Canvas')
        
        # Делаем окно прозрачным и поверх всех окон
        # ВАЖНО: Не используем WindowTransparentForInput - он блокирует ввод!
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |       # Поверх всех окон
            Qt.FramelessWindowHint |         # Без рамки
            Qt.Tool                          # Окно-инструмент
        )
        
        # Прозрачный фон
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Курсор - перекрестие при рисовании
        self.setCursor(Qt.CrossCursor)
        
        # Изначально скрываем окно
        self.hide()
    
    def set_tool(self, tool_type: ToolType) -> None:
        """Установить текущий инструмент"""
        self.current_tool_type = tool_type
        
        # Меняем курсор в зависимости от инструмента
        if tool_type == ToolType.ERASER:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.CrossCursor)
    
    def set_color(self, color: QColor) -> None:
        """Установить текущий цвет"""
        self.current_color = color
    
    def set_width(self, width: int) -> None:
        """Установить толщину линии"""
        self.current_width = width
    
    def set_toolbar_rect(self, rect: QRect) -> None:
        """Установить область панели инструментов и обновить маску холста"""
        self.toolbar_rect = rect
        print(f'📍 Область панели инструментов установлена: {rect}')
        self.update_mask()
    
    def update_mask(self) -> None:
        """Обновить маску холста, исключая область панели инструментов"""
        if not self.toolbar_rect:
            return
        
        # Создаём регион на весь экран
        screen_region = QRegion(self.rect())
        
        # Создаём регион панели инструментов в глобальных координатах
        # Преобразуем в локальные координаты холста
        toolbar_local = QRect(
            self.toolbar_rect.x() - self.x(),
            self.toolbar_rect.y() - self.y(),
            self.toolbar_rect.width(),
            self.toolbar_rect.height()
        )
        toolbar_region = QRegion(toolbar_local)
        
        # Вычитаем область панели из области холста
        canvas_region = screen_region.subtracted(toolbar_region)
        
        # Применяем маску
        self.setMask(canvas_region)
        print(f'✂️  Маска холста обновлена, панель исключена из области холста')
    
    def enable_drawing(self) -> None:
        """Включить режим рисования (показать холст)"""
        print('👁️  Показываю холст...')
        self.show()
        self.activateWindow()
        self.raise_()
        print('✅ Холст активен и поверх всех окон')
    
    def disable_drawing(self) -> None:
        """Выключить режим рисования (скрыть холст)"""
        print('🙈 Скрываю холст...')
        self.hide()
        print('✅ Холст скрыт')
    
    def clear_canvas(self) -> None:
        """Очистить весь холст"""
        print(f'🗑️  Очистка холста... (было рисунков: {len(self.drawings)})')
        self.drawings.clear()
        self.current_tool = None
        self.update()
        print('✅ Холст очищен')
    
    def _check_memory_limit(self) -> None:
        """Проверить и применить ограничение на количество рисунков"""
        if len(self.drawings) > MAX_DRAWINGS:
            # Удаляем самые старые рисунки
            excess = len(self.drawings) - MAX_DRAWINGS
            self.drawings = self.drawings[excess:]
            if DEBUG_MODE:
                print(f'⚠️  Удалено {excess} старых рисунков (лимит: {MAX_DRAWINGS})')
    
    def create_tool(self) -> Tool:
        """Создать новый инструмент на основе текущих настроек"""
        tool_map = {
            ToolType.PEN: PenTool,
            ToolType.LINE: LineTool,
            ToolType.RECTANGLE: RectangleTool,
            ToolType.CIRCLE: CircleTool,
            ToolType.ARROW: ArrowTool,
            ToolType.ERASER: EraserTool,
        }
        
        tool_class = tool_map.get(self.current_tool_type, PenTool)
        return tool_class(self.current_color, self.current_width)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Обработка нажатия кнопки мыши"""
        # Используем левую кнопку для рисования
        if event.button() == Qt.LeftButton:
            if DEBUG_MODE:
                print(f'🖱️  Нажата левая кнопка мыши в точке ({event.pos().x()}, {event.pos().y()})')
            self.is_drawing = True
            self.current_tool = self.create_tool()
            if DEBUG_MODE:
                print(f'✏️  Начато рисование инструментом: {self.current_tool_type.value}')
            
            # Для инструментов с одной точкой начала
            if self.current_tool_type in [ToolType.LINE, ToolType.RECTANGLE, 
                                          ToolType.CIRCLE, ToolType.ARROW]:
                self.current_tool.set_start_point(event.pos())
            
            # Для карандаша добавляем первую точку
            elif self.current_tool_type == ToolType.PEN:
                self.current_tool.add_point(event.pos())
            
            # Для ластика
            elif self.current_tool_type == ToolType.ERASER:
                self.erase_at_point(event.pos())
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Обработка движения мыши"""
        if not self.is_drawing or not self.current_tool:
            return
        
        # Логируем движение только в режиме отладки и с интервалом
        if DEBUG_MODE and event.pos().x() % MOUSE_LOG_INTERVAL == 0:
            print(f'↔️  Движение мыши: ({event.pos().x()}, {event.pos().y()})')
        
        # Для инструментов с конечной точкой
        if self.current_tool_type in [ToolType.LINE, ToolType.RECTANGLE, 
                                      ToolType.CIRCLE, ToolType.ARROW]:
            self.current_tool.set_end_point(event.pos())
            self.update()
        
        # Для карандаша добавляем точки
        elif self.current_tool_type == ToolType.PEN:
            self.current_tool.add_point(event.pos())
            self.update()
        
        # Для ластика продолжаем стирать
        elif self.current_tool_type == ToolType.ERASER:
            self.erase_at_point(event.pos())
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Обработка отпускания кнопки мыши"""
        if event.button() == Qt.LeftButton and self.is_drawing:
            if DEBUG_MODE:
                print(f'🖱️  Отпущена левая кнопка мыши')
            self.is_drawing = False
            
            # Сохраняем завершённый рисунок (кроме ластика)
            if self.current_tool and self.current_tool_type != ToolType.ERASER:
                self.drawings.append(self.current_tool)
                # Проверяем лимит памяти
                self._check_memory_limit()
                if DEBUG_MODE:
                    print(f'💾 Рисунок сохранён! Всего рисунков: {len(self.drawings)}')
            
            self.current_tool = None
            self.update()
            if DEBUG_MODE:
                print(f'🔄 Холст обновлён')
    
    def erase_at_point(self, point: QPoint) -> None:
        """Стереть рисунки в указанной точке"""
        eraser_radius = self.current_width * ERASER_RADIUS_MULTIPLIER
        
        # Проверяем каждый рисунок
        drawings_to_remove = []
        for drawing in self.drawings:
            # Проверяем пересечение с точками рисунка
            if hasattr(drawing, 'points') and drawing.points:
                for draw_point in drawing.points:
                    distance = ((point.x() - draw_point.x()) ** 2 + 
                               (point.y() - draw_point.y()) ** 2) ** 0.5
                    if distance < eraser_radius:
                        drawings_to_remove.append(drawing)
                        break
            
            # Проверяем пересечение с линией/фигурой
            elif drawing.start_point and drawing.end_point:
                import math
                # Вычисляем расстояние от точки до отрезка
                x1, y1 = drawing.start_point.x(), drawing.start_point.y()
                x2, y2 = drawing.end_point.x(), drawing.end_point.y()
                px, py = point.x(), point.y()
                
                dx = x2 - x1
                dy = y2 - y1
                
                if dx == 0 and dy == 0:
                    # Линия - это точка
                    dist = math.sqrt((px - x1)**2 + (py - y1)**2)
                else:
                    # Параметр t проекции точки на линию
                    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
                    
                    # Ближайшая точка на отрезке
                    closest_x = x1 + t * dx
                    closest_y = y1 + t * dy
                    
                    # Расстояние до ближайшей точки
                    dist = math.sqrt((px - closest_x)**2 + (py - closest_y)**2)
                
                if dist < eraser_radius:
                    drawings_to_remove.append(drawing)
        
        # Удаляем помеченные рисунки
        for drawing in drawings_to_remove:
            if drawing in self.drawings:
                self.drawings.remove(drawing)
                if DEBUG_MODE:
                    print(f'🧹 Стёрт рисунок типа: {type(drawing).__name__}')
        
        if drawings_to_remove:
            self.update()
    
    def paintEvent(self, event: QPaintEvent) -> None:
        """Отрисовка всех элементов на холсте"""
        painter = QPainter(self)
        
        # Включаем сглаживание для красивых линий
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        
        # Рисуем полупрозрачный фон чтобы было видно, что режим рисования активен
        painter.fillRect(self.rect(), QColor(0, 0, 0, OVERLAY_OPACITY))  # Тёмный полупрозрачный фон
        
        # Рисуем все завершённые рисунки
        for drawing in self.drawings:
            drawing.draw(painter)
        
        # Рисуем текущий инструмент в процессе рисования
        if self.current_tool and self.is_drawing:
            self.current_tool.draw(painter)
