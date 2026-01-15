# -*- coding: utf-8 -*-
"""
SharkDraw Styles
Централизованные стили для современного UI с glassmorphism эффектами
"""

from PyQt5.QtGui import QColor

# ============================================================================
# SHARKDRAW COLOR PALETTE
# ============================================================================

# Основные цвета бренда
SHARK_GRAY = QColor(107, 123, 140)      # #6B7B8C
BANANA_YELLOW = QColor(255, 217, 61)    # #FFD93D
DEEP_OCEAN = QColor(26, 35, 50)         # #1A2332
WHITE_TEETH = QColor(248, 249, 250)     # #F8F9FA

# Акцентные цвета
DANGER_RED = QColor(255, 107, 107)      # #FF6B6B
SUCCESS_GREEN = QColor(81, 207, 102)    # #51CF66
INFO_BLUE = QColor(77, 171, 247)        # #4DABF7

# ============================================================================
# GLASSMORPHISM PANEL STYLE
# ============================================================================

GLASSMORPHISM_PANEL = """
QWidget#toolbar {
    background: rgba(26, 35, 50, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
}
"""

# ============================================================================
# HEADER STYLE
# ============================================================================

HEADER_STYLE = """
QLabel#header_title {
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 14px;
    font-weight: bold;
    color: #FFD93D;
    padding: 4px;
}

QLabel#header_logo {
    padding: 4px;
}

QPushButton#close_btn {
    background: rgba(255, 149, 0, 0.2);
    border: none;
    border-radius: 6px;
    color: #FF9500;
    font-size: 16px;
    font-weight: bold;
    padding: 0px;
    min-width: 24px;
    max-width: 24px;
    min-height: 24px;
    max-height: 24px;
}

QPushButton#close_btn:hover {
    background: rgba(255, 149, 0, 0.4);
}

QPushButton#close_btn:pressed {
    background: rgba(255, 149, 0, 0.6);
}
"""

# ============================================================================
# TOOL BUTTONS STYLE
# ============================================================================

ICON_BUTTON_STYLE = """
QPushButton {
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 8px;
    padding: 8px;
}

QPushButton:hover {
    background: rgba(255, 255, 255, 0.2);
}

QPushButton:pressed {
    background: rgba(255, 255, 255, 0.15);
}

QPushButton:checked {
    background: rgba(255, 217, 61, 0.2);
    border: 2px solid rgba(255, 217, 61, 0.6);
}

QPushButton:checked:hover {
    background: rgba(255, 217, 61, 0.3);
    border-color: rgba(255, 217, 61, 0.8);
}
"""

TOOL_BUTTON_STYLE = """
QPushButton {
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 6px;
    color: #F8F9FA;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 500;
    padding: 4px 8px;
    text-align: center;
}

QPushButton:hover {
    background: rgba(255, 255, 255, 0.2);
}

QPushButton:pressed {
    background: rgba(255, 255, 255, 0.15);
}

QPushButton:checked {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #FFD93D, stop:1 #FFA500
    );
    color: #1A2332;
    font-weight: 600;
}
"""

# ============================================================================
# COLOR BUTTONS STYLE
# ============================================================================

COLOR_BUTTON_STYLE = """
QPushButton {
    border: 2px solid transparent;
    border-radius: 16px;
    min-width: 32px;
    max-width: 32px;
    min-height: 32px;
    max-height: 32px;
}

QPushButton:hover {
    border: 2px solid rgba(255, 255, 255, 0.3);
}

QPushButton:checked {
    border: 2px solid #FFD93D;
}
"""

# ============================================================================
# SLIDER STYLE
# ============================================================================

SLIDER_STYLE = """
QSlider::groove:horizontal {
    background: rgba(107, 123, 140, 0.3);
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #FFD93D, stop:1 #FFA500
    );
    border: none;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #FFD93D;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #FFD93D, stop:1 #FFA500
    );
    border-radius: 3px;
}
"""

# ============================================================================
# LABEL STYLE
# ============================================================================

LABEL_STYLE = """
QLabel {
    color: #F8F9FA;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 11px;
}

QLabel#section_title {
    color: #6B7B8C;
    font-size: 10px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 0;
}
"""

# ============================================================================
# SEPARATOR STYLE
# ============================================================================

SEPARATOR_STYLE = """
QLabel#separator {
    background: rgba(107, 123, 140, 0.3);
    max-height: 1px;
    min-height: 1px;
}
"""

# ============================================================================
# ACTION BUTTONS STYLE (Toggle, Clear)
# ============================================================================

TOGGLE_BUTTON_STYLE = """
QPushButton#toggle_btn {
    background: rgba(255, 149, 0, 0.15);
    border: 2px solid rgba(255, 149, 0, 0.5);
    border-radius: 8px;
    color: #FF9500;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 11px;
    font-weight: bold;
    padding: 12px;
    min-height: 40px;
}

QPushButton#toggle_btn:hover {
    background: rgba(255, 149, 0, 0.25);
    border-color: rgba(255, 149, 0, 0.7);
}

QPushButton#toggle_btn:pressed {
    background: rgba(255, 149, 0, 0.35);
}

QPushButton#toggle_btn:checked {
    background: rgba(255, 217, 61, 0.2);
    border: 2px solid rgba(255, 217, 61, 0.6);
    color: #FFD93D;
}

QPushButton#toggle_btn:checked:hover {
    background: rgba(255, 217, 61, 0.3);
    border-color: rgba(255, 217, 61, 0.8);
}
"""

CLEAR_BUTTON_STYLE = """
QPushButton#clear_btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: #F8F9FA;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 11px;
    font-weight: bold;
    padding: 10px;
    min-height: 36px;
}

QPushButton#clear_btn:hover {
    background: rgba(255, 107, 107, 0.3);
    border: 1px solid #FF6B6B;
    color: #FF6B6B;
}

QPushButton#clear_btn:pressed {
    background: rgba(255, 107, 107, 0.4);
}
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_tool_icon(tool_type: str) -> str:
    """Получить иконку для инструмента"""
    icons = {
        'pen': '✏️',
        'line': '━',
        'rectangle': '▢',
        'circle': '○',
        'arrow': '➜',
        'eraser': '🧹'
    }
    return icons.get(tool_type, '?')

def apply_glow_effect(widget, color: QColor, radius: int = 10):
    """Применить эффект свечения к виджету"""
    from PyQt5.QtWidgets import QGraphicsDropShadowEffect
    
    glow = QGraphicsDropShadowEffect()
    glow.setBlurRadius(radius)
    glow.setColor(color)
    glow.setOffset(0, 0)
    widget.setGraphicsEffect(glow)
