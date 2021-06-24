from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import mainwindow
import adi
import os
import pyqtgraph as pg

# the ui will be a global variable so you ca access it anywhere
ui = mainwindow.Ui_MainWindow()
adpd_pod_tab = []
caturing = 0
modes = []

def proofOfConcept():
	# comboBox
	ui.cmbBoxPods.currentTextChanged.connect(lambda value: print("Pod changed to:", value))
	# or
	ui.cmbBoxDataRate.currentTextChanged.connect(on_cmbBoxDataRate_changed)

	# spinBox
	ui.spinBoxValue.valueChanged.connect(lambda value: print("SpinBox value changed to:", value))

	ui.lnEditRPI1.returnPressed.connect(try_connect_pi1)
	ui.lnEditRPI2.returnPressed.connect(try_connect_pi2)
	ui.lnEditRPI3.returnPressed.connect(try_connect_pi3)
	ui.lnEditRPI4.returnPressed.connect(try_connect_pi4)

	ui.lnEditFileName.returnPressed.connect(open_save_file)

	ui.lnEditComment.returnPressed.connect(insert_comment)

	ui.btnStop.clicked.connect(close_save_file)

	ui.btnStart.clicked.connect(start_saving_data)


def try_connect_pi1():
	global modes
	adpd_pod_tab.append(adi.adpd188(uri="ip:" + ui.lnEditRPI1.text()))
	print("Connected to", ui.lnEditRPI1.text())
	adpd_pod_tab[0]._ctrl.context.set_timeout(0)
	adpd_pod_tab[0].rx_enabled_channels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	modes = list(adpd_pod_tab[0].mode_available.split())
def try_connect_pi2():
	adpd_pod_tab.append(adi.ad7124(uri="ip:" + ui.lnEditRPI2.text()))
def try_connect_pi3():
	adpd_pod_tab.append(adi.adpd188(uri="ip:" + ui.lnEditRPI3.text()))
def try_connect_pi4():
	adpd_pod_tab.append(adi.adpd188(uri="ip:" + ui.lnEditRPI4.text()))

def open_save_file():
	global save_file
	save_file = open(ui.lnEditFileName.text(), "a")
	txt = "Open {} file"
	print(txt.format(ui.lnEditFileName.text()))

def insert_comment():
	try:
		cmt = ui.lnEditComment.text() + "\n"
		save_file.write(cmt)
		save_file.flush()
		os.fsync(save_file.fileno())
		print("Comment added")
	except:
		print("Open a file first.")

def close_save_file():
	save_file.close()
	txt = "File {} closed"
	print(txt.format(os.path.basename(save_file.name)))

def start_saving_data():
#	try:
	adpd_pod_tab[0].mode = modes[-1]
	data = adpd_pod_tab[0].rx()
	for dim in data:
		data_str = ' '.join(map(str, dim))
		save_file.write(data_str)
		save_file.write("\n")
	save_file.flush()
	os.fsync(save_file.fileno())
	adpd_pod_tab[0].mode = modes[0]
	print("Data written")

	plot_win = ui.widgetPlotContainer
	sample = [1,2,3,4,5,6,7,8]
	colors = ["r", "g", "b", "c", "m", "y", "k", "w"]

	plot_win.clear()
	i = 0
	for dim in data:
		plot_win.plot(sample, dim, pen = colors[i])
		i = i + 1
#	except:
#		print("Connect to device.")


def on_cmbBoxDataRate_changed(value):
	print("Data Rate changed to: ", value)
	# do your code


if __name__ == "__main__":

	# build the application and the window
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()

	# setup the ui in the window
	ui.setupUi(MainWindow)

	# our playground
	proofOfConcept()

	# show the window
	MainWindow.show()
	sys.exit(app.exec_())
