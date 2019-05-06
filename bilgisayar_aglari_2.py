import os
import sys
from PyQt5 import QtWidgets
import ftplib

from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QFileDialog, QAction, QLabel, QInputDialog, \
    QLineEdit, QGridLayout, QGroupBox
from PyQt5.QtWidgets import QMessageBox
from Qt import QtCore


class Pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gui()

    def gui(self):
        self.setWindowTitle("FTP UYGULAMASI")
        self.move(500,200)
        self.setFixedSize(300,300)
        self.setStyleSheet("background-color:blue")

        self.etiket = QtWidgets.QLabel(self)
        self.etiket.move(60,90)
        self.etiket.setText("IP ADRESİ:")

        self.etiket2= QtWidgets.QLabel(self)
        self.etiket2.move(60,120)
        self.etiket2.setText("Kullanıcı Adı:")

        self.etiket3 = QtWidgets.QLabel(self)
        self.etiket3.move(60, 150)
        self.etiket3.setText("Şifre:")

        self.ip_text=QtWidgets.QLineEdit(self)
        self.ip_text.setStyleSheet("background-color:White")
        self.ip_text.move(120,90)

        self.kullanici_text=QtWidgets.QLineEdit(self)
        self.kullanici_text.move(120,120)
        self.kullanici_text.setStyleSheet("background-color:White")

        self.sifre_text=QtWidgets.QLineEdit(self)
        self.sifre_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sifre_text.setStyleSheet("background-color:White")
        self.sifre_text.move(120,150)

        self.btn=QtWidgets.QPushButton("BAĞLAN",self)
        self.btn.move(110,210)
        self.btn.clicked.connect(self.baglan)
        self.btn.setStyleSheet("background-color:White")
        self.show()

    def baglan(self):

        kullanici_adi = self.kullanici_text.text()
        ip = self.ip_text.text()
        sifre = self.sifre_text.text()
        ftp = ftplib.FTP(ip, kullanici_adi, sifre)
        global files
        files = ftp.nlst()

        if ftp:
            QMessageBox.question(self, 'BAŞARILI GİRİŞ', "FTP UYGULMASINA HOŞGELDİNİZ SAYIN : " + kullanici_adi, QMessageBox.Ok,
                                 QMessageBox.Ok)
            pencere2.fileList(files)

            ftp.quit()
            pencere2.baglan2(ip, kullanici_adi, sifre)
            pencere2.show()

class Pencere2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gui2()

    def fileList(self, files):
        self.files = files
        self.tableWidget = QTableWidget()
        self.tableWidget.setStyleSheet("background-color:White")
        self.tableWidget.setRowCount(len(files))
        self.tableWidget.setFixedSize(135,350)
        self.tableWidget.setColumnCount(1)
        i=0
        for f in files:
            self.tableWidget.setItem(0, i, QTableWidgetItem(f))
            i=i+1
        self.tableWidget.move(0, 0)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.tableWidget.doubleClicked.connect(self.table_click)
        self.local_table = QTableWidget()
        self.local_table.setFixedSize(135,350)
        self.local_table.setStyleSheet("background-color:White")
        self.local_table.setRowCount(len(os.listdir()))
        self.local_table.doubleClicked.connect(self.table_click2)
        self.local_table.setColumnCount(1)
        j = 0
        for f in os.listdir():
            self.local_table.setItem(0, j, QTableWidgetItem(f))
            j = j + 1
        self.local_table.move(0, 0)
        self.layout.addWidget(self.local_table)

        self.down_btn = QtWidgets.QPushButton("DOWNLOAD", self)
        self.down_btn.move(170, 45)
        self.down_btn.clicked.connect(self.download)
        self.down_btn.setStyleSheet("background-color:White")

        self.down_text = QtWidgets.QLineEdit(self)
        self.down_text.move(290, 15)
        self.down_text.setStyleSheet("background-color:White")
        self.down_text.setText("Secilen Dosya:")
        self.down_text.setReadOnly(True)
        self.down_text.setMaximumWidth(250)

        self.upload_btn=QtWidgets.QPushButton("UPLOAD",self)
        self.upload_btn.move(170,445)
        self.upload_btn.clicked.connect(self.upload)
        self.upload_btn.setStyleSheet("background-color:White")

        self.upload_text = QtWidgets.QLineEdit(self)
        self.upload_text.move(170, 415)
        self.upload_text.setStyleSheet("background-color:White")
        self.upload_text.setText("Yüklenecek Dosya:")
        self.upload_text.setReadOnly(True)
        self.upload_text.setMaximumWidth(250)

        self.exit_btn = QtWidgets.QPushButton("EXİT", self)
        self.exit_btn.move(1200,650 )
        self.exit_btn.clicked.connect(self.exit)
        self.exit_btn.setStyleSheet("background-color:Red")

        self.dizin_text = QtWidgets.QLineEdit(self)
        self.dizin_text.move(700, 15)
        self.dizin_text.setStyleSheet("background-color:White")
        self.dizin_text.setText("Dizin İsmi Gir")

        self.dizin_btn = QtWidgets.QPushButton("DİZİN EKLE", self)
        self.dizin_btn.move(700, 45)
        self.dizin_btn.clicked.connect(self.dizin_ekle)
        self.dizin_btn.setStyleSheet("background-color:White")

        self.dizinsil_btn = QtWidgets.QPushButton("DİZİN SİL", self)
        self.dizinsil_btn.move(290, 45)
        self.dizinsil_btn.clicked.connect(self.dizin_sil)
        self.dizinsil_btn.setStyleSheet("background-color:White")

        self.rename_btn = QtWidgets.QPushButton("YENİDEN ADLANDIR", self)
        self.rename_btn.move(410, 45)
        self.rename_btn.clicked.connect(self.rename_dizin)
        self.rename_btn.setStyleSheet("background-color:White")
    def server_table_yenile(self):
        server_list=ftp.nlst()
        i = 0
        for f in server_list:
            self.tableWidget.setItem(0, i, QTableWidgetItem(f))
            i = i + 1
    def local_table_yenile(self):
        j = 0
        for f in os.listdir():
            self.local_table.setItem(0, j, QTableWidgetItem(f))
            j = j + 1

    #     global x
    #     global y
    #     x = 0
    #     y = 0
    #     self.text = "x: {0},  y: {1}".format(x, y)
    #     self.label = QLabel(self.text, self)
    #     self.label.move(300, 45)
    #     self.setMouseTracking(True)
    #
    # def mouseMoveEvent(self, e):
    #     x = e.x()
    #     y = e.y()
    #
    #     text = "x: {0},  y: {1}".format(x, y)
    #     self.label.setText(text)


    # def mousePressEvent(self, event):
    def dizin_ekle(self):
        if self.dizin_text.text()=="Dizin İsmi Gir" or self.dizin_text.text()=="":
            QMessageBox.about(self, "HATA", "Lütfen bir dosya adı girin")
        else:
            if self.dizin_kontrol(self.dizin_text.text())==1:
                ftp.mkd(self.dizin_text.text())
                QMessageBox.about(self, "BAŞARILI", "DİZİN EKLENDİ")
                self.server_table_yenile()
            else:
                QMessageBox.about(self, "HATA", "YANLIŞ KARAKTER KULLANILDI")


    def rename_dizin(self):
        if self.down_text.text()=="Secilen Dosya:":
            QMessageBox.about(self, "HATA", "Lütfen Dosya Seçiniz")
        else:

            text, okPressed = QInputDialog.getText(self, "İsim Değiştir", "Yeni Dosya Adı", QLineEdit.Normal, "")
            server_list=ftp.nlst()
            if okPressed and text != '':
                text_böl=self.down_text.text().split('.')
                text_uzantı="."+text_böl[len(text_böl)-1]
                global text2
                k=0
                text2=text+text_uzantı
                for w in server_list:
                    if text2 == w:
                        k=k+1
                if k!=0:
                    QMessageBox.about(self, "HATA", "Bu isimde bir dosya mevcut. Farklı bir isim giriniz!")
                elif k==0:
                    r = self.dizin_kontrol(text)
                    if r == 1:
                        ftp.rename(self.down_text.text(), text2)
                        QMessageBox.about(self, "BAŞARILI", "İSİM DEĞİŞTİRİLDİ")
                        self.server_table_yenile()
                    else:
                        print("")

    def dizin_kontrol(self,dizin):
        böl1 = dizin.split('/')
        böl2 = dizin.split(':')
        böl3 = dizin.split('*')
        böl4 = dizin.split('?')
        böl5 = dizin.split('"')
        böl6 = dizin.split('<')
        böl7 = dizin.split('>')
        böl8 = dizin.split('|')
        böl9 = dizin.split('\\')
        böl9 = dizin.split('ı')
        böl10 = dizin.split('ş')
        böl11 = dizin.split('ğ')
        böl12 = dizin.split('ü')
        böl13 = dizin.split('ö')
        böl14 = dizin.split('ç')

        if len(böl1) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE / KARAKTERİ ALGILANDI.")
        elif len(böl2) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE : KARAKTERİ ALGILANDI.")
        elif len(böl3) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE * KARAKTERİ ALGILANDI.")
        elif len(böl4) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE ? KARAKTERİ ALGILANDI.")
        elif len(böl5) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE  \" KARAKTERİ ALGILANDI.")
        elif len(böl6) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE < KARAKTERİ ALGILANDI.")
        elif len(böl7) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE > KARAKTERİ ALGILANDI.")
        elif len(böl8) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE | KARAKTERİ ALGILANDI.")
        elif len(böl9) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE ı KARAKTERİ ALGILANDI.")
        elif len(böl10) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE ş KARAKTERİ ALGILANDI.")
        elif len(böl11) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE ğ KARAKTERİ ALGILANDI.")
        elif len(böl12) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE ü KARAKTERİ ALGILANDI.")
        elif len(böl13) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE ö KARAKTERİ ALGILANDI.")
        elif len(böl14) > 1:
            QMessageBox.about(self, "HATA", "DİZİN İSMİNDE ç KARAKTERİ ALGILANDI.")
        else:
            return 1
    def dizin_sil(self):
        if self.down_text.text()=="Secilen Dosya:":
            QMessageBox.about(self, "HATA", "Lütfen Tablodan Dosya Seçin")
        else:
            ftp.rmd(self.down_text.text())
            QMessageBox.about(self, "BAŞARILI", "Silinen Dosya="+self.down_text.text())
            self.server_table_yenile()

    def exit(self):
        QMessageBox.about(self, "BAĞLANTI", "FTP BAĞLANTISI SONLANDIRILDI")
        pencere2.close()
        ftp.quit()


    def table_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.down_text.setText(currentQTableWidgetItem.text())
    def table_click2(self):
        for currentQTableWidgetItem in self.local_table.selectedItems():
            self.upload_text.setText(currentQTableWidgetItem.text())
    def baglan2(self,ip,kullanici_adi,sifre):
        self.ip=ip
        self.kullanici_adi=kullanici_adi
        self.sifre=sifre
        global ftp
        ftp = ftplib.FTP(ip, kullanici_adi, sifre)

    def download(self):
        if self.down_text.text()=="Secilen Dosya:":
            QMessageBox.about(self, "HATA", "Lütfen Tablodan Dosya Seçin")
        else:
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                global filename
                filename = currentQTableWidgetItem.text()
                böl=filename.split(".")
            if len(böl)>1:
                ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write, 1024)
                QMessageBox.question(self, 'İNDİRME BAŞARILI', "İNDİRİLEN DOSYA : " + filename,QMessageBox.Ok,QMessageBox.Ok)
                self.local_table_yenile()
            else:
                QMessageBox.question(self, 'İNDİRME HATASI', "BU BİR KLASÖR : " + filename, QMessageBox.Ok,QMessageBox.Ok)
    def upload(self):
        if self.upload_text.text()=="Yüklenecek Dosya:":
            QMessageBox.about(self, "HATA", "Lütfen Tablodan Dosya Seçin")
        else:
            for currentQTableWidgetItem in self.local_table.selectedItems():
                global upload_dosyasi
                upload_dosyasi=currentQTableWidgetItem.text()
                böl_upload=upload_dosyasi.split(".")
            if (len(böl_upload)>1):
                ftp.storbinary('STOR ' + upload_dosyasi, open(upload_dosyasi, 'rb'))
                QMessageBox.question(self, 'YÜKLEME BAŞARILI', "YÜKLENEN DOSYA : " + upload_dosyasi, QMessageBox.Ok,
                                     QMessageBox.Ok)
                self.server_table_yenile()
            else:
                QMessageBox.question(self, 'YÜKLEME HATASI', "BU BİR KLASÖR : " + upload_dosyasi, QMessageBox.Ok,
                                     QMessageBox.Ok)

        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getOpenFileName(self, "UPLOAD EDİLECEK DOSYAYI SEÇİN", "",
        #                                           "All Files (*);;Python Files (*.py)", options=options)
        #
        # if fileName:
        #     böl=fileName.split('/')
        #     print(böl[len(böl)-1])
        #     ftp.storbinary('STOR ' + böl[len(böl)-1], open(böl[len(böl)-1], 'rb'))
        #     QMessageBox.question(self, 'UPLOAD BAŞARILI', "UPLOAD EDİLEN DOSYA : " + fileName, QMessageBox.Ok,
        #                          QMessageBox.Ok)

    def gui2(self):
        self.setWindowTitle("ANA EKRAN")
        self.move(0, 0)
        self.setFixedSize(1340, 700)
        self.isActiveWindow()
        self.setStyleSheet("background-color:lightblue")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    pencere = Pencere()
    pencere2 = Pencere2()
    sys.exit(app.exec_())