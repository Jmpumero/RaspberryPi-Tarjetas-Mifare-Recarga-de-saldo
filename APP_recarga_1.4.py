try: # Raspberry Pi
	import RPi.GPIO as GPIO
except ImportError: # Other system
	GPIO = None

#RPi.GPIO is not None else raise ValueError(f'RPi.GPIO module not imported. Please pip install.')

import SimpleMFRC522
import signal
import time
import logging
import ctypes
import string

from recarga_ui import *
from ventana_ayuda_ui import *




"""
Autor:Jose Medina V20959966
"""
global flag,flag2,cost,number,uids
global h,av_1,band1,av2,tp1,band2,tp2,saf_e
av_1=" SALDO INSUFICIENTE "
t3=" TARJETA INVALIDA "
t1="ERROR T1"
t2="ERROR T2"
t4="ERROR T4"
av_c="Operacion realizada con exito \nRetire la tarjeta"
talk=""
band1=False
band2=False
uids=None
tp1=0
tp2=0
tp3=0
h=0
cost=10
number=5


class ventanita(QtWidgets.QDialog,Ui_Dialog):
	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)
		self.setWindowTitle("ventana de prueba")


class MainWindow(QtWidgets.QMainWindow, Ui_APP_recarga):

	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi(self)
		reg_ex = QtCore.QRegExp("(([0-9]{1,10}[.,][0-9]{1,2})|([0-9]{1,10}))")
		input_validator = QtGui.QRegExpValidator(reg_ex, self.re_line)
		self.re_line.setValidator(input_validator)
		self.setWindowTitle("APP RECARGA")
		self.pushButton.clicked.connect(self.recharge)
		self.Button_proc.clicked.connect(self.process)
		self.re_line.returnPressed.connect(self.recharge)
		self.actionDetener.triggered.connect(self.detener)
		self.actionSalir.triggered.connect(self.closed_window)
		self.actionAyuda.triggered.connect(self.ventana_ayuda)

		self.timer1 = QtCore.QTimer(self, interval=300, timeout=self.listen)
		self.timer1.start()
		self.listen()




	def closed_window(self):
		self.close()

	def detener(self):
		print("end")
		self.timer1.stop()

	def ventana_ayuda(self):
		self.vent = ventanita()
		self.vent.show()


	def cleaning_all(self):
		#self.re_line.setText("")
		self.r_saldo_act_label.setText("")
		self.r_uid_label.setText("")


	def convert(self,txt):

		if txt.find(".")>0:
			print(" ")

		elif  txt.find(",")>0:

			txsp=txt.split(",")
			txi=txsp[0]
			txf=txsp[1]
			txt=txi+"."+txf

			self.accept(txt)
		else:
			txt=txt+"."+"00"

		v=float (txt)
		return(v)


	def process(self):
		global tp2,saf_e

		if saf_e:
			saf_e=False
			self.detener()
			self.cleaning_all()
			self.timer2 = QtCore.QTimer(self, interval=500, timeout=self.thread_2)
			self.timer2.start()
		#self.thread_2()




	def recharge(self):

		global uids

		v=self.convert(self.re_line.text())
		#self.reject("")

		reader = SimpleMFRC522.SimpleMFRC522()
		uid = reader.read_id_no_block()
		reader.Close_MFRC522()


		if(uid is not None):
			reader = SimpleMFRC522.SimpleMFRC522()
			uid = reader.num_to_hex(uid)[1:9]
			reader.Close_MFRC522()
			self.r_uid_label.setText(uid)
			#print(uid)
			reader = SimpleMFRC522.SimpleMFRC522()
			data = reader.read_block(number)
			reader.Close_MFRC522()

			try :
				if float(data[1])==0:
					self.r_saldo_act_label.setAlignment(QtCore.Qt.AlignJustify)
					self.r_saldo_act_label.setText(str(data[1]))

				else:
					if float(data[1]):

						credit=float(data[1])
						r=credit + v

						vt="{0:.2f}".format(r)
						#print("g")

						self.writing(uid,vt,number)
						self.re_line.setText("")
						"""
						#modo una recarga por tarjeta
						if uids != uid:
							uids=uid

							self.writing(uid,vt,number)
						else:
							print("")
						"""
			except ValueError:
				print(".")
				#self.reject(t3)
			except TypeError:
				print("*")
				#self.reject(t4)
			except IndexError:
				print("error tarjeta fuera de corbetura")
		else:
			self.r_saldo_act_label.setText("")
			uids=None




	def writing(self,uid,v,num):
		global av2,band1,tp1

		reader = SimpleMFRC522.SimpleMFRC522()
		uid_act = reader.read_id_no_block()
		reader.Close_MFRC522()
		if(uid_act is not None):
			reader = SimpleMFRC522.SimpleMFRC522()
			uid_act = reader.num_to_hex(uid_act)[1:9]
			reader.Close_MFRC522()
			if uid_act==uid:
				reader = SimpleMFRC522.SimpleMFRC522()
				vc=str(v)
				data = reader.write_block(num, vc.ljust(16))
				reader.Close_MFRC522()
				reader = SimpleMFRC522.SimpleMFRC522()
				data = reader.read_block(number)
				reader.Close_MFRC522()

				try:
					k=float(data[1])
					v=float(vc)
					self.r_saldo_act_label.setAlignment(QtCore.Qt.AlignJustify)
					self.r_saldo_act_label.setText(str(k))
					if k==v:
						self.r_saldo_act_label.setAlignment(QtCore.Qt.AlignJustify)
						self.r_saldo_act_label.setText(str(data[1]))
						#self.re_line.setText("")
						self.accept(av_c)
						band1=True
						tp1=0
					else:
						self.reject("OPERACION NO REALIZADA")
				except TypeError:
					print("")
					#self.reject(t4)
			else:
				# self.writing(self,uid,v,num)
				#ojo llamada recursiva colocar
				self.reject("hora del plan B")
		else:
			self.reject("Acerque la tarjeta al lector")






	def reject(self,a):
		self.aviso_label.setStyleSheet("color: rgb(255, 0, 0);")
		self.aviso_label.setText(a)

	def accept(self,a):
		self.aviso_label.setStyleSheet("color: rgb(0, 170, 0);")
		self.aviso_label.setText(a)




	@QtCore.pyqtSlot()
	def listen(self):
		global number,cost,uids,av2,band1,tp2,saf_e
		reader = SimpleMFRC522.SimpleMFRC522()
		uid = reader.read_id_no_block()
		reader.Close_MFRC522()

		saf_e=True
		band1=False
		tp2=0

		self.time_c_label.setText("")
		self.time_c_label_2.setText("")
		if(uid is not None):

			if band1:
				self.accept(av_c)
			else:
				print("")
				self.accept("Esperando recarga...")
			reader = SimpleMFRC522.SimpleMFRC522()
			uid = reader.num_to_hex(uid)[1:9]
			reader.Close_MFRC522()
			self.r_uid_label.setText(uid)
			reader = SimpleMFRC522.SimpleMFRC522()
			data = reader.read_block(number)
			reader.Close_MFRC522()

			try :
				if float(data[1])==0:
					self.r_saldo_act_label.setAlignment(QtCore.Qt.AlignJustify)
					self.r_saldo_act_label.setText(str(data[1]))
					self.reject(av_1)
				else:
					if float(data[1]):
						self.r_saldo_act_label.setAlignment(QtCore.Qt.AlignCenter)
						self.r_saldo_act_label.setText(str(data[1]))

			except ValueError:
				print("..")
				print(data[1])
			except TypeError:
				print("*")
				print(data[1])
			except IndexError:
				print("error tarjeta fuera de corbetura")
		else:
			self.cleaning_all()
			self.reject("Acerque la tarjeta lector")
			uids=None
			band1=False



	@QtCore.pyqtSlot()
	def thread_2(self):
		global tp1,band1
		tp1+=1
		reader = SimpleMFRC522.SimpleMFRC522()
		uid = reader.read_id_no_block()
		reader.Close_MFRC522()
		tim=19-tp1


		if tp1 <20:
			if band1:
				print("entro")
				self.timer2.stop()
				#self.timer1 = QtCore.QTimer(self, interval=300, timeout=self.listen)
				self.timer1.start()
				#self.listen()
			else:
				if(uid is not None):

					if tp1<20:
						self.recharge()
					else:
						tp1=0
						self.timer2.stop()

						self.timer3 = QtCore.QTimer(self, interval=300, timeout=self.thread_3)
						self.timer3.start()
						self.thread_3()

				else:

					self.reject("Debe acercar la tarjeta al lector \nPara poder procesar su recarga")
					self.time_c_label.setText("Tiempo restante:")
					self.time_c_label_2.setText(str(tim))
					uids=None
		else:
			#print("entra 2")
			tp1=0
			self.timer2.stop()

			self.timer3 = QtCore.QTimer(self, interval=300, timeout=self.thread_3)
			self.timer3.start()
			self.thread_3()


	@QtCore.pyqtSlot()
	def thread_3(self):
		global tp2

		#print("tp2=",str(tp2))
		self.re_line.setText("")

		tp2+=1
		if tp2<10:
			self.reject("Tiempo agotado \nOperacion CANCELADA")

		else:
			self.timer3.stop()
			self.timer1.start()






if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()
