from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from pynput.keyboard import* #(Importing Key, Controller)
import time
import cv2
import pytesseract
import sys
import threading


class CustomizedTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet('QTextEdit {border: none; background-color: rgb(25,25,25); color: rgb(34,145,240)}')

        verticalScroll = QScrollBar()
        verticalScroll.setStyleSheet("""
                QScrollBar:vertical {
                    border: none;
                    background:transparent;
                    width:7px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:vertical {
                    background: rgb(50,50,50);
                    min-height: 0px;
                }
                QScrollBar::add-line:vertical {
                    background: rgb(50,50,50);
                    height: 0px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                QScrollBar::sub-line:vertical {
                    background: rgb(50,50,50);
                    height: 0 px;
                    subcontrol-position: top;
                    subcontrol-origin: margin
                }""")

        horizontalScroll = QScrollBar()
        horizontalScroll.setStyleSheet("""QScrollBar:horizontal {border: none; background: transparent; height: 5px; 
                margin: 0px 0px 0px 0px
                } 
                QScrollBar::handle:horizontal {background: rgb(34,145,240); min-width: 0 px
                }
                QScrollBar::add-line:horizontal {background: rgb(34,145,240); width: 0 px; subcontrol-position: left; 
                subcontrol-origin: margin
                }
                QScrollBar::sub-line:horizontal {background: rgb(34,145,240); width: 0 px; subcontrol-position: right; 
                subcontrol-origin: margin
                }""")

        self.setVerticalScrollBar(verticalScroll)
        self.setHorizontalScrollBar(horizontalScroll)


class ITCMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(900)
        self.setFixedHeight(700)
        self.move(500, 200)
        self.setStyleSheet('QMainWindow {background-color: rgb(20,20,20)}')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(
            'E:\Python Projects\Inventory System\Kyl1-Inventory System\ImageToText\\ITTicon1-a.png'))
        self.oldPos = self.pos()
        self.titleBar()
        self.selectionInterface()
        self.resultInterface()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        print(self.oldPos)

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
        print('Delta')
        print(delta)



    def titleBar(self):
        self.titleBarFrame = QFrame(self)
        self.titleBarFrame.setGeometry(0, 0, 900, 30)
        self.titleBarFrame.setStyleSheet('QFrame {background-color: rgb(30,30,30)}')


        self.appWindowIcon = QLabel(self.titleBarFrame)
        self.appWindowIcon.setPixmap(QPixmap(
            'E:\Python Projects\Inventory System\Kyl1-Inventory System\ImageToText\\ITTicon3.png'))
        self.appWindowIcon.setGeometry(2, 0, 50, 30)

        self.appWindowTitle = QLabel(self.titleBarFrame)
        self.appWindowTitle.setGeometry(30, 4, 150, 20)
        self.appWindowTitle.setText('Image Character Generator')
        appWindowTitleFont = QFont('Calibri', 10)
        appWindowTitleFont.setBold(True)
        self.appWindowTitle.setFont(appWindowTitleFont)
        self.appWindowTitle.setStyleSheet('QLabel {background-color: transparent; color: rgb(228,232,237)}')

        def minimizeWindow():
            self.showMinimized()

        self.minimizeButton = QPushButton(self.titleBarFrame)
        self.minimizeButton.setGeometry(810, 3, 40, 25)
        self.minimizeButton.setIcon(QIcon('E:\Python Projects\Inventory System\Kyl1-Inventory System\Images\\minimize.png'))
        self.minimizeButton.setFocusPolicy(Qt.NoFocus)
        self.minimizeButton.setIconSize(QSize(25, 25))
        self.minimizeButton.setToolTip('Minimize Window')
        self.minimizeButton.setStyleSheet('QPushButton {background-color: rgb(15,15,15)}')
        self.minimizeButton.clicked.connect(minimizeWindow)

        def closeWindow():
            self.close()

        self.closeButton = QPushButton(self.titleBarFrame)
        self.closeButton.setGeometry(855, 3, 40, 25)
        self.closeButton.setIcon(
            QIcon('E:\Python Projects\Inventory System\Kyl1-Inventory System\Images\\close.png'))
        self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.closeButton.setIconSize(QSize(25, 25))
        self.closeButton.setToolTip('Close Window')
        self.closeButton.setStyleSheet('QPushButton {background-color: rgb(15,15,15)}')
        self.closeButton.clicked.connect(closeWindow)

    def selectionInterface(self):
        print('selection interface')
        self.frame1 = QFrame(self)
        self.frame1.setGeometry(10, 40, 400, 650)
        self.frame1.setStyleSheet('QFrame {background-color: rgb(30,30,30)}')

        self.pictureFrame = QFrame(self.frame1)
        self.pictureFrame.setGeometry(5, 5, 390, 540)
        self.pictureFrame.setStyleSheet('QFrame {background-color: rgb(25,25,25)}')

        self.pictureLocation = QLineEdit(self.frame1)
        self.pictureLocation.setGeometry(5, 550, 390, 30)
        self.pictureLocation.setText('')
        self.pictureLocation.setReadOnly(True)
        self.pictureLocation.setStyleSheet(
            'QLineEdit {border:none; background-color: rgb(25,25,25); color: rgb(120,120,120)}')
        self.pictureLocation.setFocusPolicy(Qt.NoFocus)

        self.selectedPicture = QLabel(self.pictureFrame)
        self.selectedPicture.setGeometry(1, 1, 389, 539)
        if self.pictureLocation.text() == '':
            self.selectedPicture.setPixmap(QPixmap(
                'E:\Python Projects\Inventory System\Kyl1-Inventory System\ImageToText\\ITTDefaultPic1.png'))



        def browseImage():
            print('Browse Image to Generate')
            openImage = QFileDialog.getOpenFileName(self.frame1, 'Open File', 'C\\', 'Image Files(*.jpg *.png)')
            imageLocation = openImage[0]
            self.pictureLocation.setText(imageLocation)

            if self.pictureLocation.text() == '':
                self.selectedPicture.setPixmap(QPixmap(
                    'E:\Python Projects\Inventory System\Kyl1-Inventory System\ImageToText\\ITTDefaultPic1.png'))

            else:
                self.selectedPicture.setPixmap(QPixmap(imageLocation))
                self.selectedPicture.setScaledContents(True)

        self.browseButton = QPushButton(self.frame1)
        self.browseButton.setGeometry(5, 585, 100, 60)
        self.browseButton.setToolTip('Browse / Select an Image')
        #self.browseButton.setText('Browse')
        self.browseButton.setIcon(QIcon(
            'E:\Python Projects\Inventory System\Kyl1-Inventory System\ImageToText\\ITTBrowse.png'))
        self.browseButton.setIconSize(QSize(40, 40))
        self.browseButton.clicked.connect(browseImage)
        self.browseButton.setStyleSheet('QPushButton {background-color: rgb(50,50,50)}')
        self.browseButton.setFocusPolicy(Qt.NoFocus)


        def generateText():

            def generatingTime():
                print('Generating Time')
                loadingTime = 0
                while loadingTime <= 100:
                    print(loadingTime)
                    self.generationProgressBar.setValue(loadingTime)
                    time.sleep(.20)
                    loadingTime += 1
                else:
                    return False

            self.thread2 = threading.Thread(target=generatingTime)
            self.thread2.start()
            try:

                selectedImage = self.pictureLocation.text()
                print(selectedImage)
                print('Generate Text')
                pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
                image = cv2.imread(selectedImage, cv2.IMREAD_ANYCOLOR)
                print(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                resultGenerated = pytesseract.image_to_string(image)
                print(resultGenerated)

                self.resultTable.setText(resultGenerated)

            except:
                print('Its Error')
                self.pictureLocation.setText('Select An Image First Before Generating')

        self.generateTextButton = QPushButton(self.frame1)
        self.generateTextButton.setGeometry(110, 585, 285, 60)
        self.generateTextButton.setToolTip('Generate Character')
        self.generateTextButton.setIcon(QIcon(
            'E:\Python Projects\Inventory System\Kyl1-Inventory System\ImageToText\\ITTGenerate.png'))
        self.generateTextButton.setIconSize(QSize(50, 35))
        self.generateTextButton.clicked.connect(generateText)
        self.generateTextButton.setStyleSheet('QPushButton {background-color: rgb(50,50,50)}')
        self.generateTextButton.setFocusPolicy(Qt.NoFocus)

    def resultInterface(self):
        self.frame2 = QFrame(self)
        self.frame2.setGeometry(420, 40, 470, 650)
        self.frame2.setStyleSheet('QFrame {background-color: rgb(30,30,30)}')

        self.resultTable = CustomizedTextEdit(self.frame2)
        self.resultTable.setGeometry(5, 5, 460, 575)
        self.resultTable.setText('')
        self.resultTable.setReadOnly(True)
        # self.resultTable.setStyleSheet(
        #     'QTextEdit {border: none; background-color: rgb(25,25,25); color: rgb(34,145,240)}')


        self.generationProgressBar = QProgressBar(self.frame2)
        self.generationProgressBar.setGeometry(5, 585, 460, 20)
        self.generationProgressBar.setValue(0)
        self.generationProgressBar.setStyleSheet('QProgressBar {border: 1px solid gray; text-align: center;'
                                                 'background-color: rgb(25,25,25); '
                                                 'color: rgb(225,225,225)}'
                                                 'QProgressBar::chunk {background-color: rgb(34,145,240)}')

        def copyGeneratedText():
            print('Copy Generated Text Result')
            keyboardController = Controller()

            keyboardController.press(Key.ctrl)
            keyboardController.press('a')
            keyboardController.release('a')
            keyboardController.release(Key.ctrl)

            keyboardController.press(Key.ctrl)
            keyboardController.press('c')
            keyboardController.release('c')
            keyboardController.release(Key.ctrl)


        self.copyButton = QPushButton(self.frame2)
        self.copyButton.setGeometry(5, 610, 460, 35)
        self.copyButton.setToolTip('Copy the Generated Texts')
        self.copyButton.setIcon(QIcon('E:\Python Projects\Inventory System\Kyl1-Inventory System\ImageToText\\ITTCopy.png'))
        self.copyButton.setIconSize(QSize(50, 30))
        self.copyButton.setStyleSheet('QPushButton {background-color: rgb(50,50,50)}')
        self.copyButton.clicked.connect(copyGeneratedText)
        self.copyButton.setFocusPolicy(Qt.NoFocus)











def MainApplication():
    application = QApplication(sys.argv)
    application.setStyle('Fusion')
    mainWindow = ITCMainWindow()
    mainWindow.show()
    sys.exit(application.exec())

MainApplication()

