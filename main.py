import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
import yfinance as yf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class StockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Data Viewer")
        self.setGeometry(100, 100, 600, 600)

        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter Stock Ticker Symbol (e.g. AAPL)")
        layout.addWidget(self.input)

        self.button = QPushButton("Get Stock Data")
        layout.addWidget(self.button)

        self.info = QTextEdit()
        self.info.setReadOnly(True)
        layout.addWidget(self.info)

        # Matplotlib Figure
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        self.button.clicked.connect(self.get_stock_data)

    def get_stock_data(self):
        ticker = self.input.text().strip().upper()
        if not ticker:
            QMessageBox.warning(self, "Input Error", "Please enter a ticker symbol.")
            return

        self.info.clear()
        self.figure.clear()

        try:
            stock = yf.Ticker(ticker)

            # Fetch info
            info = stock.info
            hist = stock.history(period="1y")

            if hist.empty:
                raise ValueError("No historical data found.")

            # Display key info
            current_price = info.get('currentPrice', 'N/A')
            market_cap = info.get('marketCap', 'N/A')
            fifty_two_week_high = info.get('fiftyTwoWeekHigh', 'N/A')
            fifty_two_week_low = info.get('fiftyTwoWeekLow', 'N/A')
            previous_close = info.get('previousClose', 'N/A')

            info_text = (
                f"Ticker: {ticker}\n"
                f"Current Price: ${current_price}\n"
                f"Previous Close: ${previous_close}\n"
                f"Market Cap: {market_cap:,}\n"
                f"52-Week High: ${fifty_two_week_high}\n"
                f"52-Week Low: ${fifty_two_week_low}\n"
            )
            self.info.setText(info_text)

            # Plot closing price
            ax = self.figure.add_subplot(111)
            hist['Close'].plot(ax=ax)
            ax.set_title(f"{ticker} Closing Prices - Last 1 Year")
            ax.set_ylabel("Price ($)")
            ax.grid(True)

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch data: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockApp()
    window.show()
    sys.exit(app.exec())
