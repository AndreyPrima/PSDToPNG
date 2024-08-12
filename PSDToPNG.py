import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QProgressBar, QComboBox, QMessageBox, QCheckBox, QGroupBox, 
                             QRadioButton, QSpinBox, QHBoxLayout)
from PyQt5.QtCore import QDir, Qt, QThread, pyqtSignal, QTranslator, QLocale
from PyQt5.QtGui import QPalette, QColor
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from Language import Language

class PSDtoImageConverter(QWidget):
    """Main widget for converting PSD files to other image formats."""
    
    def __init__(self, language='en'):
        super().__init__()
        self.last_input_dir = QDir.homePath()
        self.last_output_dir = QDir.homePath()
        self.lang = Language(language)
        self.initUI()

    def initUI(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()

        # Label and buttons for directory selection
        self.label = QLabel(self.lang.get_text('select_directory'), self)
        layout.addWidget(self.label)

        self.selectButton = QPushButton(self.lang.get_text('select_directory'), self)
        self.selectButton.clicked.connect(self.selectDirectory)
        layout.addWidget(self.selectButton)

        self.outputButton = QPushButton(self.lang.get_text('select_output_directory'), self)
        self.outputButton.clicked.connect(self.selectOutputDirectory)
        self.outputButton.setEnabled(False)
        layout.addWidget(self.outputButton)

        # Conversion settings group
        self.createConversionOptions(layout)

        # Theme selection group
        self.createThemeOptions(layout)

        # Language selection group
        self.createLanguageOptions(layout)

        # Convert button
        self.convertButton = QPushButton(self.lang.get_text('convert_psd_to_image'), self)
        self.convertButton.clicked.connect(self.startConversion)
        self.convertButton.setEnabled(False)
        layout.addWidget(self.convertButton)

        # Progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setVisible(False)
        layout.addWidget(self.progressBar)

        self.setLayout(layout)
        self.setWindowTitle(self.lang.get_text('convert_psd_to_image'))
        self.setGeometry(300, 300, 500, 300)

        self.updateTheme()  # Set initial theme

    def createConversionOptions(self, layout):
        """Create the conversion settings group."""
        self.optionsGroup = QGroupBox(self.lang.get_text('conversion_settings'), self)
        optionsLayout = QVBoxLayout()

        self.formatLabel = QLabel(self.lang.get_text('select_output_format'), self)
        optionsLayout.addWidget(self.formatLabel)

        self.formatComboBox = QComboBox(self)
        self.formatComboBox.addItems(["PNG", "JPEG", "BMP", "TIFF"])
        self.formatComboBox.currentIndexChanged.connect(self.updateConversionOptions)
        optionsLayout.addWidget(self.formatComboBox)

        self.qualityLabel = QLabel(self.lang.get_text('jpeg_quality'), self)
        self.qualityLabel.setVisible(False)
        optionsLayout.addWidget(self.qualityLabel)

        self.qualitySpinBox = QSpinBox(self)
        self.qualitySpinBox.setRange(1, 100)
        self.qualitySpinBox.setValue(90)
        self.qualitySpinBox.setVisible(False)
        optionsLayout.addWidget(self.qualitySpinBox)

        self.loggingCheckBox = QCheckBox(self.lang.get_text('log_errors'), self)
        optionsLayout.addWidget(self.loggingCheckBox)

        self.optionsGroup.setLayout(optionsLayout)
        layout.addWidget(self.optionsGroup)

    def createThemeOptions(self, layout):
        """Create the theme selection group."""
        self.themeGroup = QGroupBox(self.lang.get_text('theme_selection'), self)
        themeLayout = QVBoxLayout()

        self.lightThemeRadioButton = QRadioButton(self.lang.get_text('light_theme'), self)
        self.lightThemeRadioButton.setChecked(True)
        self.lightThemeRadioButton.toggled.connect(self.updateTheme)
        themeLayout.addWidget(self.lightThemeRadioButton)

        self.darkThemeRadioButton = QRadioButton(self.lang.get_text('dark_theme'), self)
        self.darkThemeRadioButton.toggled.connect(self.updateTheme)
        themeLayout.addWidget(self.darkThemeRadioButton)

        self.themeGroup.setLayout(themeLayout)
        layout.addWidget(self.themeGroup)

    def createLanguageOptions(self, layout):
        """Create the language selection group."""
        self.languageGroup = QGroupBox(self.lang.get_text('language_selection'), self)
        languageLayout = QHBoxLayout()

        self.languageComboBox = QComboBox(self)
        self.languageComboBox.addItems(["English", "Русский", "Українська"])
        self.languageComboBox.currentIndexChanged.connect(self.switchLanguage)
        languageLayout.addWidget(self.languageComboBox)

        self.languageGroup.setLayout(languageLayout)
        layout.addWidget(self.languageGroup)

    def selectDirectory(self):
        """Select a directory to search for PSD files."""
        self.last_input_dir = QFileDialog.getExistingDirectory(self, self.lang.get_text('select_directory'), self.last_input_dir)
        if self.last_input_dir:
            self.label.setText(f"{self.lang.get_text('select_directory')}: {self.last_input_dir}")
            self.outputButton.setEnabled(True)

    def selectOutputDirectory(self):
        """Select a directory to save the converted files."""
        self.last_output_dir = QFileDialog.getExistingDirectory(self, self.lang.get_text('select_output_directory'), self.last_output_dir)
        if self.last_output_dir:
            self.convertButton.setEnabled(True)

    def updateTheme(self):
        """Update the application theme based on the selection."""
        palette = QPalette()
        if self.darkThemeRadioButton.isChecked():
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.white)
        
        QApplication.setPalette(palette)

    def switchLanguage(self):
        """Switch the language of the application based on user selection."""
        selected_language = self.languageComboBox.currentText()
        if selected_language == "English":
            self.lang.set_language('en')
        elif selected_language == "Русский":
            self.lang.set_language('ru')
        elif selected_language == "Українська":
            self.lang.set_language('uk')
        self.updateUI()

    def updateConversionOptions(self):
        """Update options based on the selected output format."""
        if self.formatComboBox.currentText() == "JPEG":
            self.qualityLabel.setVisible(True)
            self.qualitySpinBox.setVisible(True)
        else:
            self.qualityLabel.setVisible(False)
            self.qualitySpinBox.setVisible(False)

    def updateUI(self):
        """Update the text of all UI elements to match the selected language."""
        self.label.setText(self.lang.get_text('select_directory'))
        self.selectButton.setText(self.lang.get_text('select_directory'))
        self.outputButton.setText(self.lang.get_text('select_output_directory'))
        self.optionsGroup.setTitle(self.lang.get_text('conversion_settings'))
        self.formatLabel.setText(self.lang.get_text('select_output_format'))
        self.qualityLabel.setText(self.lang.get_text('jpeg_quality'))
        self.loggingCheckBox.setText(self.lang.get_text('log_errors'))
        self.themeGroup.setTitle(self.lang.get_text('theme_selection'))
        self.lightThemeRadioButton.setText(self.lang.get_text('light_theme'))
        self.darkThemeRadioButton.setText(self.lang.get_text('dark_theme'))
        self.languageGroup.setTitle(self.lang.get_text('language_selection'))
        self.convertButton.setText(self.lang.get_text('convert_psd_to_image'))
        self.setWindowTitle(self.lang.get_text('convert_psd_to_image'))

    def startConversion(self):
        """Start the conversion process in a separate thread."""
        self.progressBar.setVisible(True)
        self.conversionThread = PSDConversionThread(self.last_input_dir, self.last_output_dir,
                                                    self.formatComboBox.currentText().lower(),
                                                    self.qualitySpinBox.value() if self.formatComboBox.currentText() == "JPEG" else None,
                                                    self.loggingCheckBox.isChecked())
        self.conversionThread.progressUpdated.connect(self.progressBar.setValue)
        self.conversionThread.conversionCompleted.connect(self.onConversionComplete)
        self.conversionThread.start()

    def onConversionComplete(self, success, errors):
        """Handle the completion of the conversion process."""
        self.progressBar.setVisible(False)
        if success:
            QMessageBox.information(self, self.lang.get_text('conversion_completed'), self.lang.get_text('conversion_successful'))
        else:
            error_message = "\n".join(errors) if errors else self.lang.get_text('errors_occurred')
            QMessageBox.warning(self, self.lang.get_text('conversion_completed'), error_message)

class PSDConversionThread(QThread):
    """Thread for converting PSD files to images."""
    
    progressUpdated = pyqtSignal(int)
    conversionCompleted = pyqtSignal(bool, list)

    def __init__(self, inputDir, outputDir, format, quality=None, log_errors=False):
        super().__init__()
        self.inputDir = inputDir
        self.outputDir = outputDir
        self.format = format
        self.quality = quality
        self.log_errors = log_errors
        self.errors = []

    def run(self):
        """Run the conversion process."""
        psd_files = [os.path.join(self.inputDir, f) for f in os.listdir(self.inputDir) if f.lower().endswith('.psd')]
        total_files = len(psd_files)
        if total_files == 0:
            self.conversionCompleted.emit(True, [])
            return

        with ThreadPoolExecutor() as executor:
            for idx, psd_file in enumerate(psd_files):
                executor.submit(self.convert_psd, psd_file)
                self.progressUpdated.emit(int((idx + 1) / total_files * 100))

        self.conversionCompleted.emit(len(self.errors) == 0, self.errors)

    def convert_psd(self, psd_file):
        """Convert a single PSD file to the desired format."""
        try:
            image = Image.open(psd_file)
            output_file = os.path.join(self.outputDir, f"{os.path.splitext(os.path.basename(psd_file))[0]}.{self.format}")
            if self.format == 'jpeg' and self.quality:
                image.convert('RGB').save(output_file, quality=self.quality)
            else:
                image.save(output_file)
        except Exception as e:
            error_message = f"Error converting {os.path.basename(psd_file)}: {str(e)}"
            self.errors.append(error_message)
            if self.log_errors:
                with open("conversion_errors.log", "a") as log_file:
                    log_file.write(error_message + "\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    translator = QTranslator()
    locale = QLocale.system().name()
    if locale.startswith('ru'):
        translator.load("ru.qm")
    elif locale.startswith('uk'):
        translator.load("uk.qm")
    else:
        translator.load("en.qm")
    app.installTranslator(translator)

    window = PSDtoImageConverter()
    window.show()

    sys.exit(app.exec_())
