#!/usr/bin/env python
# quitter.py- provide a button to quit this "program"
 
import sys
import re

from PySide import QtCore, QtGui
from PySide.QtCore import QTimer, QRegExp
from PySide.QtGui import QMainWindow, QPushButton, QApplication, QPixmap
 
from tier_optimizer_ui import Ui_MainWindow

import threading as t
from tier_optimizer import Genetic
import lib.Const
 
class GeneticInitThread(t.Thread):
	def __init__(self):
		''' Constructor. '''
		t.Thread.__init__(self)
		self.gen = None

	def run(self):
		self.gen = Genetic()
		self.gen.init_population()

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.thread = GeneticInitThread()
		self.thread.setDaemon(True)
		self.generation = None
		self.initalizeButton.clicked.connect(self.initialize_population)
		self.evolutionButton.clicked.connect(self.calculate_population)
		self.evolutionButton.setEnabled(False)

	def initialize_population(self):
		self.statusbar.showMessage("Calculating initial population... (This may take a while)")
		self.thread.start()
		self.initalizeButton.setEnabled(False)
		QTimer.singleShot(50, self.check_completed_initialize)

	def check_completed_initialize(self):
		if self.thread.is_alive():
			if (len(self.thread.gen.population) > 0 and len(self.thread.gen.population) <= 13):
				rx = QRegExp("poketeam_\d+")
				pop_teams = self.population.findChildren(QtGui.QWidget, rx)
				for g in range(len(self.thread.gen.population)):
					plabel = pop_teams[g].findChildren(QtGui.QLabel)
					for idx, pokename in enumerate(self.thread.gen.population[g].team_names):
						pixmap = QPixmap("./sprites/" + pokename + ".png")
						plabel[idx].setPixmap(pixmap)


			self.progress.setValue(len(self.thread.gen.population)*10)
			QTimer.singleShot(50, self.check_completed_initialize)
		else:
			self.evolutionButton.setEnabled(True)
			self.generation = self.thread.gen
			self.progress.setValue(0)
			self.fill_ranking()
			self.statusbar.showMessage("Done! Now press Calculate Generations to begin")

	def fill_ranking(self):
		rank = self.generation.ranking
		best = rank.ranking[0]
		rest = rank.ranking[1:]

		rx = QRegExp("pok\d+")
		best_pokelabels = self.ranking.findChildren(QtGui.QLabel, rx)

		for idx, pokename in enumerate(best.team_names):
			pixmap = QPixmap("./sprites/" + pokename + ".png")
			pixmap = pixmap.scaled(60, 40, QtCore.Qt.KeepAspectRatio) 
			best_pokelabels[idx].setPixmap(pixmap)

		rx = QRegExp("poketeam_\d+")
		pop_teams = self.ranking.findChildren(QtGui.QWidget, rx)
		for g in range(len(rest)):
			plabel = pop_teams[g].findChildren(QtGui.QLabel)
			for idx, pokename in enumerate(rest[g].team_names):
				pixmap = QPixmap("./sprites/" + pokename + ".png")
				plabel[idx].setPixmap(pixmap)



	def calculate_population():
		pass

if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	app.exec_()