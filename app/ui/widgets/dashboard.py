from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)

from PySide6.QtCore import Qt

import pyqtgraph as pg
from pyqtgraph import PlotWidget

class DataPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(400)
        self.setMinimumWidth(400)
        
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)
        
        self.bar_item = None
        self.text_items = []

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brima Dashboard")
        self.setMinimumSize(800, 600)

        main_layout = QVBoxLayout(self)

        self.title = QLabel("Dashboard")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2a61ad;
            }
        """)
        main_layout.addWidget(self.title)

        self.plot_grid = pg.GraphicsLayoutWidget()
        self.plot_grid.setBackground('w')
        main_layout.addWidget(self.plot_grid)

        self.plot_items = []  # Store plot references for updates

        rows, cols = 3, 2  # 3 rows × 2 columns = 6 plots
        for row in range(rows):
            for col in range(cols):
                plot = self.plot_grid.addPlot(row=row, col=col)
                
                # Disable mouse interaction
                plot.setMouseEnabled(x=False, y=False)  # Disable panning
                plot.hideButtons()  # Hide the auto-scale button
                
                # Disable zooming
                for mouse_event in ['wheel', 'drag']:
                    plot.setMouseEnabled(x=False, y=False)
                
                # Set axis styles
                plot.showGrid(x=True, y=True)
                plot.setLabel('left', 'Count')
                plot.setTitle(f"Plot {row * cols + col + 1}")
                
                # Add padding to view box
                plot.vb.setLimits(xMin=-0.5, 
                                 xMax=3.5,  # Adjust based on number of bars
                                 yMin=0, 
                                 yMax=100)  # Adjust based on expected max value
                
                # Disable auto-range on mouse events
                plot.vb.setMouseEnabled(x=False, y=False)
                
                self.plot_items.append(plot)