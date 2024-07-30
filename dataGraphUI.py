from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import pandas as pd
import random
import sys


# Widget that sets up and controls the labels for Temp, pH, and Flow Rate
# Changes their status through symbols to indicate if the current data is good or not
class TrackerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # List of symbols that represent status of current data
        # "+" when data is good and matches the target value of the variable
        # "*" when the data is moderately off the target value and warns the user
        # "!" when the data is extremely off the target value and warns the user
        self.statusList = ["+", "*", "!"]

        # List of phrases to explain the status to user when they hover over it
        self.statusPhrase = ["Status: Good", "Status: Off/Unusual", "Status: Warning (Needs Attention)"]

        self.setupUI()

    def setupUI(self):
        # Setup for the tracker frame for Temp, pH, and Flow Rate variables
        self.trackerFrame = QFrame(self)
        self.trackerFrame.setFrameShape(QFrame.Box)
        self.trackerFrame.setFrameShadow(QFrame.Raised)
        self.trackerFrame.setObjectName("trackerFrame")
        self.horizontalLayout_2 = QHBoxLayout(self.trackerFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Setting up individual trackers for each variable
        self.tempTrackerSetup()
        self.pHTrackerSetup()
        self.flowRateTrackerSetup()

        # Layout set up for child widget purposes
        layout = QVBoxLayout(self)
        layout.addWidget(self.trackerFrame)
        self.setLayout(layout)

    def tempTrackerSetup(self):
        # Initialize the frame and add to layout
        self.tempTrackerFrame = QFrame(self.trackerFrame)
        self.tempTrackerFrame.setFrameShape(QFrame.StyledPanel)
        self.tempTrackerFrame.setFrameShadow(QFrame.Raised)
        self.tempTrackerFrame.setObjectName("tempTrackerFrame")
        self.verticalLayout_4 = QVBoxLayout(self.tempTrackerFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # Initialize the head label and add to layout with proper formatting
        self.tempLabelTrack = QLabel(self.tempTrackerFrame)
        font = QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(16)
        font.setUnderline(True)
        self.tempLabelTrack.setFont(font)
        self.tempLabelTrack.setObjectName("tempLabelTrack")
        self.tempLabelTrack.setText("Temperature: 0 °C")
        self.tempLabelTrack.setStyleSheet("background-color: red")
        self.verticalLayout_4.addWidget(self.tempLabelTrack, 0, Qt.AlignHCenter)

        # Initialize the status label
        self.tempStatusLabel = QLabel(self.tempTrackerFrame)
        font = QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        self.tempStatusLabel.setFont(font)
        self.tempStatusLabel.setObjectName("tempStatusLabel")
        self.tempStatusLabel.setText(self.statusList[0])
        self.tempStatusLabel.setToolTip(self.statusPhrase[0])
        self.verticalLayout_4.addWidget(self.tempStatusLabel, 0, Qt.AlignHCenter)
        self.horizontalLayout_2.addWidget(self.tempTrackerFrame)

    def pHTrackerSetup(self):
        # Initialize the frame and add to layout
        self.pHTrackerFrame = QFrame(self.trackerFrame)
        self.pHTrackerFrame.setFrameShape(QFrame.StyledPanel)
        self.pHTrackerFrame.setFrameShadow(QFrame.Raised)
        self.pHTrackerFrame.setObjectName("pHTrackerFrame")
        self.verticalLayout_5 = QVBoxLayout(self.pHTrackerFrame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # Initialize the head label and add to layout with proper formatting
        self.phTrackLabel = QLabel(self.pHTrackerFrame)
        font = QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(16)
        font.setUnderline(True)
        self.phTrackLabel.setFont(font)
        self.phTrackLabel.setObjectName("phTrackLabel")
        self.phTrackLabel.setText("pH: 0")
        self.phTrackLabel.setStyleSheet("background-color: lightgreen")
        self.verticalLayout_5.addWidget(self.phTrackLabel, 0, Qt.AlignHCenter)

        # Initialize the status label
        self.pHStatusLabel = QLabel(self.pHTrackerFrame)
        font = QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        self.pHStatusLabel.setFont(font)
        self.pHStatusLabel.setObjectName("pHStatusLabel")
        self.pHStatusLabel.setText(self.statusList[0])
        self.pHStatusLabel.setToolTip(self.statusPhrase[0])
        self.verticalLayout_5.addWidget(self.pHStatusLabel, 0, Qt.AlignHCenter)
        self.horizontalLayout_2.addWidget(self.pHTrackerFrame)

    def flowRateTrackerSetup(self):
        # Initialize the frame and add to layout
        self.flowRateTrackFrame = QFrame(self.trackerFrame)
        self.flowRateTrackFrame.setFrameShape(QFrame.StyledPanel)
        self.flowRateTrackFrame.setFrameShadow(QFrame.Raised)
        self.flowRateTrackFrame.setObjectName("flowRateTrackFrame")
        self.verticalLayout_6 = QVBoxLayout(self.flowRateTrackFrame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        # Initialize the head label and add to layout with proper formatting
        self.flowRTrackLabel = QLabel(self.flowRateTrackFrame)
        font = QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(16)
        font.setUnderline(True)
        self.flowRTrackLabel.setFont(font)
        self.flowRTrackLabel.setObjectName("flowRTrackLabel")
        self.flowRTrackLabel.setText("Flow Rate: 0 mL/min")
        self.flowRTrackLabel.setStyleSheet("background-color: blue")
        self.verticalLayout_6.addWidget(self.flowRTrackLabel, 0, Qt.AlignHCenter)

        # Initialize the status label
        self.flowRStatusLabel = QLabel(self.flowRateTrackFrame)
        font = QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        self.flowRStatusLabel.setFont(font)
        self.flowRStatusLabel.setObjectName("flowRStatusLabel")
        self.flowRStatusLabel.setText(self.statusList[0])
        self.flowRStatusLabel.setToolTip(self.statusPhrase[0])
        self.verticalLayout_6.addWidget(self.flowRStatusLabel, 0, Qt.AlignHCenter)
        self.horizontalLayout_2.addWidget(self.flowRateTrackFrame)

    # Slot function takes data from the signal and gives the whole class access to it
    def targetValuesSetup(self, targetValues):
        self.targetValues = targetValues

    def trackerManager(self, currentData):
        # Margin of deviation from target value allowed
        # Temporarily set for TESTING Purposes
        TEMP_MARGIN = 1
        PH_MARGIN = 0.05
        FLOW_MARGIN = 1

        # Target Values set up
        if self.targetValues:
            tempTargetValue = float(self.targetValues["Temperature"])
            pHTargetValue = float(self.targetValues["pH"])
            flowRateTargetValue = float(self.targetValues["Flow Rate"])
        else:
            # Default Values
            tempTargetValue = 0
            pHTargetValue = 0
            flowRateTargetValue = 0

        # Conditional managers for each variable, changing status according to data
        if currentData["Temperature"] == tempTargetValue:
            self.tempStatusLabel.setText(self.statusList[0])
            self.tempStatusLabel.setToolTip(self.statusPhrase[0])
        elif (tempTargetValue - TEMP_MARGIN) < currentData["Temperature"] < (tempTargetValue + TEMP_MARGIN):
            self.tempStatusLabel.setText(self.statusList[1])
            self.tempStatusLabel.setToolTip(self.statusPhrase[1])
        else:
            self.tempStatusLabel.setText(self.statusList[2])
            self.tempStatusLabel.setToolTip(self.statusPhrase[2])

        # pH
        if currentData["pH"] == pHTargetValue:
            self.pHStatusLabel.setText(self.statusList[0])
            self.pHStatusLabel.setToolTip(self.statusPhrase[0])
        elif (pHTargetValue - PH_MARGIN) < currentData["pH"] < (pHTargetValue + PH_MARGIN):
            self.pHStatusLabel.setText(self.statusList[1])
            self.pHStatusLabel.setToolTip(self.statusPhrase[1])
        else:
            self.pHStatusLabel.setText(self.statusList[2])
            self.pHStatusLabel.setToolTip(self.statusPhrase[2])

        # Flow Rate
        if currentData["Flow Rate"] == flowRateTargetValue:
            self.flowRStatusLabel.setText(self.statusList[0])
            self.flowRStatusLabel.setToolTip(self.statusPhrase[0])
        elif (flowRateTargetValue - FLOW_MARGIN) < currentData["Flow Rate"] < (flowRateTargetValue + FLOW_MARGIN):
            self.flowRStatusLabel.setText(self.statusList[1])
            self.flowRStatusLabel.setToolTip(self.statusPhrase[1])
        else:
            self.flowRStatusLabel.setText(self.statusList[2])
            self.flowRStatusLabel.setToolTip(self.statusPhrase[2])

        # Passing the current data to update the data displayed on the trackers
        self.updateTrackerData(currentData)

    def updateTrackerData(self, currentData):
        # Updating data with the given current data
        self.tempLabelTrack.setText(f"Temperature: {currentData['Temperature']} °C")
        self.phTrackLabel.setText(f"pH: {currentData['pH']}")
        self.flowRTrackLabel.setText(f"Flow Rate: {currentData['Flow Rate']} mL/min")


# Widget that handles the acquirement of data and how to store it
class DataHandler(QWidget):
    def __init__(self):
        super().__init__()
        # Sets up the data frame dictionary that stores that data plot points
        self.dataFrameSetup = {
            "Elapsed Seconds": [],
            "Temperature": [],
            "pH": [],
            "Flow Rate": []
        }

    # Generates data for testing purposes
    def generateData(self, time_elapsed):
        # Generates random data to fill graph plot points
        temperature = round(random.uniform(20, 50), 2)
        pH = round(random.uniform(6, 8), 2)
        flowRate = round(random.uniform(5, 25), 2)

        # Adding in the new data
        self.dataFrameSetup["Elapsed Seconds"].append(time_elapsed)
        self.dataFrameSetup["Temperature"].append(temperature)
        self.dataFrameSetup["pH"].append(pH)
        self.dataFrameSetup["Flow Rate"].append(flowRate)
        self.currentData = {"Time Elapsed": time_elapsed, "Temperature": temperature, "pH": pH, "Flow Rate": flowRate}

        return self.dataFrameSetup, self.currentData

    # Function that saves the stored data into a csv text file
    def saveData(self, filename="data.csv"):
        # Puts the data from dictionary into a pandas dataframe
        self.dataFrame = pd.DataFrame(self.dataFrameSetup)

        # Saves the new data frame into a csv file
        self.dataFrame.to_csv(filename, index=False)
        QMessageBox.information(None, "Save Data", f"Data saved to {filename}")

    def clearData(self):
        # Resets the data to clear everything
        self.dataFrameSetup = {
            "Elapsed Seconds": [],
            "Temperature": [],
            "pH": [],
            "Flow Rate": []
        }


# Handles the main data shown in the UI with graphs
class DataWidget(QWidget):
    # Signal that sends newly received data point to the tracker widget
    dataPointSignal = pyqtSignal(dict)

    def __init__(self, parent=None, timer_app=None, target_app=None):
        super().__init__(parent)

        # Establishing the DataHandler Object
        self.handleData = DataHandler()

        # Setup frames for the Data widgets and structure
        self.dataPanelFrame = QFrame(self)
        self.dataPanelFrame.setFrameShape(QFrame.StyledPanel)
        self.dataPanelFrame.setFrameShadow(QFrame.Raised)
        self.dataPanelFrame.setObjectName("dataPanelFrame")
        self.verticalLayout_2 = QVBoxLayout(self.dataPanelFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Frame for Data Tabs created
        self.dataTabFrame = QFrame(self.dataPanelFrame)
        self.dataTabFrame.setFrameShape(QFrame.StyledPanel)
        self.dataTabFrame.setFrameShadow(QFrame.Raised)
        self.dataTabFrame.setObjectName("dataTabFrame")
        self.verticalLayout_3 = QVBoxLayout(self.dataTabFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # Setup for individual data tabs
        self.dataTabSetup()

        # Once dataTab is set up, adds it to the layout
        self.verticalLayout_2.addWidget(self.dataTabFrame)

        # Initialize the tracker frame and sets up the format
        self.trackerFrame = TrackerWidget(self.dataPanelFrame)
        self.verticalLayout_2.addWidget(self.trackerFrame, 0, Qt.AlignBottom)

        # Layout setup for parent widget purposes
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.dataPanelFrame)
        self.setLayout(mainLayout)

        # Connecting data signal to tracker widget for updating
        self.dataPointSignal.connect(self.trackerFrame.trackerManager)

        # Connecting the target signal to the tracker widget to pass in target values
        target_app.valueSignal.connect(self.trackerFrame.targetValuesSetup)

        # Slots for graph functions run by timer actions
        timer_app.timerSignal.connect(self.plotGraph)
        timer_app.resetSignal.connect(self.clearGraph)

    def dataTabSetup(self):
        # Setup Data label as header of the tabs
        self.DataLabel = QLabel(self.dataTabFrame)
        font = QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(18)
        font.setBold(True)
        font.setUnderline(True)
        self.DataLabel.setFont(font)
        self.DataLabel.setObjectName("DataLabel")
        self.DataLabel.setText("Data")
        self.verticalLayout_3.addWidget(self.DataLabel, 0, Qt.AlignHCenter)

        # Setting up the tab widget that hold the data graphs
        self.graphTabs = QTabWidget(self.dataTabFrame)
        self.graphTabs.setMinimumSize(QSize(500, 500))
        font = QFont()
        font.setFamily("Rockwell")
        font.setPointSize(12)
        self.graphTabs.setFont(font)
        self.graphTabs.setTabShape(QTabWidget.Rounded)
        self.graphTabs.setObjectName("graphTabs")

        # Individual tab setup
        self.allTabSetup()
        self.tempTabSetup()
        self.pHTabSetup()
        self.flowRateTabSetup()

        # Adding the graph tabs to the layout
        self.verticalLayout_3.addWidget(self.graphTabs)

    def allTabSetup(self):
        # Initialize the tab
        self.all_graph = pg.PlotWidget()
        self.all_graph.showGrid(x=True, y=True)
        self.all_graph.setObjectName("all")

        # Adds graph to the tab
        self.graphTabs.addTab(self.all_graph, "All")

    def tempTabSetup(self):
        # Initialize the tab with the graph
        self.temp_graph = pg.PlotWidget()
        self.temp_graph.showGrid(x=True, y=True)
        self.temp_graph.setLabel("left", "Temperature (°C)")
        self.temp_graph.setLabel("bottom", "Time (sec)")
        self.temp_graph.setObjectName("temp")

        # Adds graph to the tab
        self.graphTabs.addTab(self.temp_graph, "Temperature")

    def pHTabSetup(self):
        # Initialize the tab
        self.pH_graph = pg.PlotWidget()
        self.pH_graph.showGrid(x=True, y=True)
        self.pH_graph.setLabel("left", "pH")
        self.pH_graph.setLabel("bottom", "Time (sec)")
        self.pH_graph.setObjectName("pH")

        self.graphTabs.addTab(self.pH_graph, "pH")

    def flowRateTabSetup(self):
        # Initialize the tab
        self.flowRate_graph = pg.PlotWidget()
        self.flowRate_graph.showGrid(x=True, y=True)
        self.flowRate_graph.setLabel("left", "Flow Rate")
        self.flowRate_graph.setLabel("bottom", "Time (sec)")
        self.flowRate_graph.setObjectName("flowRate")

        self.graphTabs.addTab(self.flowRate_graph, "Flow Rate")

    def plotGraph(self, time_elapsed):
        # Generates random data to fill graph plot points
        newData, currentData = self.handleData.generateData(time_elapsed)

        # Plotting the graphs
        self.plotTempGraph(newData)
        self.plotPHGraph(newData)
        self.plotFlowRateGraph(newData)
        self.plotAllGraph(newData)

        # Sends signal of current Data dict to the tracker manager
        self.dataPointSignal.emit(currentData)

    def plotTempGraph(self, newData):
        # Plots the Temp Graph with given data
        pen = pg.mkPen(color=(175, 60, 60), width=3)
        self.temp_graph.plot(newData["Elapsed Seconds"], newData["Temperature"], pen=pen, symbol="o")

    def plotPHGraph(self, newData):
        # Plots the pH Graph with given data
        pen = pg.mkPen(color=(48, 172, 85), width=3)
        self.pH_graph.plot(newData["Elapsed Seconds"], newData["pH"], pen=pen, symbol="o")

    def plotFlowRateGraph(self, newData):
        # Plots the Flow Rate Graph with given data
        pen = pg.mkPen(color=(76, 87, 186), width=3)
        self.flowRate_graph.plot(newData["Elapsed Seconds"], newData["Flow Rate"], pen=pen, symbol="o")

    def plotAllGraph(self, newData):
        # Plotting all temp, pH, and flow rate graphs in one graph here
        pen = pg.mkPen(color=(175, 60, 60), width=3)
        self.all_graph.plot(newData["Elapsed Seconds"], newData["Temperature"], pen=pen)

        pen = pg.mkPen(color=(48, 172, 85), width=3)
        self.all_graph.plot(newData["Elapsed Seconds"], newData["pH"], pen=pen)

        pen = pg.mkPen(color=(76, 87, 186), width=3)
        self.all_graph.plot(newData["Elapsed Seconds"], newData["Flow Rate"], pen=pen)

    def clearGraph(self):
        # Clears the data from Data Handler side
        self.handleData.clearData()

        # Clears the graphs
        self.temp_graph.clear()
        self.pH_graph.clear()
        self.flowRate_graph.clear()
        self.all_graph.clear()

    def saveData(self):
        # Opens up the file to save data to csv, user managed
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "",
                                                  "CSV Files (*.csv);;All Files (*)", options=options)
        if filename:
            try:
                self.handleData.saveData(filename)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save data: {e}")


# Timer Widget setup and functions
class TimerWidget(QWidget):
    # Timer signal used for updating data
    timerSignal = pyqtSignal(int)

    # Reset timer signal for clearing data
    resetSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Time Label and variable to store time data
        self.time = QTime(0, 0, 0)
        self.time_elapsed = 0

        # Bool flag to track button states
        self.startClicked = False

        self.setupUI()

    def setupUI(self):
        # Setting up the layout
        self.verticalLayout_7 = QVBoxLayout(self)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        # The Timer Header label
        self.watchHeader = QLabel(self)
        self.watchHeader.setMinimumSize(QSize(300, 150))
        font = QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(22)
        font.setBold(True)
        font.setUnderline(True)
        self.watchHeader.setFont(font)
        self.watchHeader.setFrameShape(QFrame.NoFrame)
        self.watchHeader.setTextFormat(Qt.AutoText)
        self.watchHeader.setAlignment(Qt.AlignCenter)
        self.watchHeader.setObjectName("watchHeader")
        self.verticalLayout_7.addWidget(self.watchHeader)
        self.watchHeader.setText("Timer")

        # Setup timer and button widgets
        self.timerSetup()
        self.timerControl()
        self.startButtonSetup()
        self.stopButtonSetup()

    def timerSetup(self):
        # Setting up the Timer label to be displayed
        self.timewatch = QLabel(self)
        self.timewatch.setEnabled(True)
        self.timewatch.setMinimumSize(QSize(300, 50))
        font = QFont()
        font.setPointSize(28)
        self.timewatch.setFont(font)
        self.timewatch.setFrameShape(QFrame.Box)
        self.timewatch.setFrameShadow(QFrame.Plain)
        self.timewatch.setAlignment(Qt.AlignCenter)
        self.timewatch.setObjectName("timewatch")
        self.verticalLayout_7.addWidget(self.timewatch)
        self.timewatch.setText(self.time.toString("hh:mm:ss"))

    def timerControl(self):
        # Control sequence for the timer itself
        eTimer = QTimer(self)
        eTimer.timeout.connect(self.updateTimer)
        eTimer.start(1000)

    def updateTimer(self):
        # Detects when the timer is started and tracks the time
        if self.startClicked:
            self.time = self.time.addSecs(1)
            self.timewatch.setText(self.time.toString("hh:mm:ss"))
            self.time_elapsed += 1

            # Sends a signal to the data side
            if self.time_elapsed % 2 == 0:
                self.timerSignal.emit(self.time_elapsed)

    def startButtonSetup(self):
        # Start button initialized in format
        self.startButton = QPushButton(self)
        self.startButton.setMinimumSize(QSize(0, 25))
        font = QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.verticalLayout_7.addWidget(self.startButton)
        self.startButton.setText("START")

        # When button is pressed, activates mentioned function
        self.startButton.pressed.connect(self.startButtonClicked)

    def startButtonClicked(self):
        # When the user clicks start again while timer is running, opens a dialog window to warn user
        if self.startClicked:
            reply = QMessageBox.question(self, 'Confirmation',
                                         "A timer is already running. Are you sure you want to restart the timer?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.time = QTime(0, 0, 0)
                self.time_elapsed = 0
                self.timerSignal.emit(self.time_elapsed)
                self.resetSignal.emit()
        else:
            self.startClicked = True

    def stopButtonSetup(self):
        # Stop Button initialized in format
        self.stopButton = QPushButton(self)
        self.stopButton.setMinimumSize(QSize(0, 25))
        font = QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        self.stopButton.setFont(font)
        self.stopButton.setObjectName("stopButton")
        self.verticalLayout_7.addWidget(self.stopButton)
        self.stopButton.setText("STOP")

        # When button is pressed, activates mentioned function
        self.stopButton.pressed.connect(self.stopButtonClicked)

    def stopButtonClicked(self):
        # Asks the user to confirm their decision to stop the timer
        if self.startClicked:
            reply = QMessageBox.question(self, "Confirmation", "Are you sure you want to stop the timer?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.startClicked = False


# Temporary setup for the Variable Inputs, currently just for the UI
class VariableInputWidget(QWidget):
    valueSignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup for the general frame of the input widget
        self.variablesInputFrame = QFrame(self)
        self.variablesInputFrame.setFrameShape(QFrame.StyledPanel)
        self.variablesInputFrame.setFrameShadow(QFrame.Raised)
        self.variablesInputFrame.setObjectName("variablesInputFrame")
        self.verticalLayout_8 = QVBoxLayout(self.variablesInputFrame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")

        # Setup dictionary that will hold the input values the user gives
        self.targetValues = {"Temperature": 0, "pH": 0, "Flow Rate": 0}

        # Initializing bool flags that mark the edit ability of each input line
        self.tempEditMade = False
        self.pHEditMade = False
        self.flowEditMade = False

        # Setup for individual input widgets for each variable
        self.tempInputSetup()
        self.pHInputSetup()
        self.flowRateInputSetup()

    def tempInputSetup(self):
        # Setup Variable Frame
        self.tempInputFrame = QFrame(self.variablesInputFrame)
        self.tempInputFrame.setFrameShape(QFrame.StyledPanel)
        self.tempInputFrame.setFrameShadow(QFrame.Raised)
        self.tempInputFrame.setObjectName("tempInputFrame")
        self.verticalLayout_9 = QVBoxLayout(self.tempInputFrame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")

        # Label
        self.tempInputLabel = QLabel(self.tempInputFrame)
        font = QFont()
        font.setFamily("Rockwell")
        font.setPointSize(14)
        font.setBold(False)
        self.tempInputLabel.setFont(font)
        self.tempInputLabel.setObjectName("tempInputLabel")
        self.tempInputLabel.setText("Temperature:")
        self.verticalLayout_9.addWidget(self.tempInputLabel)

        # User inputs the target value for this variable in the line edit
        self.tempInput = QLineEdit(self.tempInputFrame)
        self.tempInput.setMinimumSize(QSize(200, 50))
        self.tempInput.setToolTip("Type in your target value and hit Enter. To edit your input, "
                                  "right click to enable editing.")
        self.tempInput.setObjectName("tempInput")
        self.verticalLayout_9.addWidget(self.tempInput)
        self.verticalLayout_8.addWidget(self.tempInputFrame)

        # Action when user inputs variable, calls enterValue func
        self.tempInput.returnPressed.connect(lambda: self.enterValue(self.tempInput))

    def pHInputSetup(self):
        # Setup Variable Frame
        self.pHInputFrame = QFrame(self.variablesInputFrame)
        self.pHInputFrame.setFrameShape(QFrame.StyledPanel)
        self.pHInputFrame.setFrameShadow(QFrame.Raised)
        self.pHInputFrame.setObjectName("pHInputFrame")
        self.verticalLayout_10 = QVBoxLayout(self.pHInputFrame)
        self.verticalLayout_10.setObjectName("verticalLayout_10")

        # Label
        self.pHInputLabel = QLabel(self.pHInputFrame)
        font = QFont()
        font.setFamily("Rockwell")
        font.setPointSize(14)
        self.pHInputLabel.setFont(font)
        self.pHInputLabel.setObjectName("pHInputLabel")
        self.pHInputLabel.setText("pH:")
        self.verticalLayout_10.addWidget(self.pHInputLabel)

        # User inputs the target value for this variable in the line edit
        self.pHInput = QLineEdit(self.pHInputFrame)
        self.pHInput.setMinimumSize(QSize(200, 50))
        self.pHInput.setToolTip("Type in your target value and hit Enter. To edit your input, "
                                "right click to enable editing.")
        self.pHInput.setObjectName("pHInput")
        self.verticalLayout_10.addWidget(self.pHInput)
        self.verticalLayout_8.addWidget(self.pHInputFrame)

        # Action when user inputs variable, calls enterValue func
        self.pHInput.returnPressed.connect(lambda: self.enterValue(self.pHInput))

    def flowRateInputSetup(self):
        # Setup Variable Frame
        self.flowRateInputFrame = QFrame(self.variablesInputFrame)
        self.flowRateInputFrame.setFrameShape(QFrame.StyledPanel)
        self.flowRateInputFrame.setFrameShadow(QFrame.Raised)
        self.flowRateInputFrame.setObjectName("flowRateInputFrame")
        self.verticalLayout_11 = QVBoxLayout(self.flowRateInputFrame)
        self.verticalLayout_11.setObjectName("verticalLayout_11")

        # Label
        self.flowRateInputLabel = QLabel(self.flowRateInputFrame)
        font = QFont()
        font.setFamily("Rockwell")
        font.setPointSize(14)
        self.flowRateInputLabel.setFont(font)
        self.flowRateInputLabel.setObjectName("flowRateInputLabel")
        self.flowRateInputLabel.setText("Flow Rate:")
        self.verticalLayout_11.addWidget(self.flowRateInputLabel)

        # User inputs the target value for this variable in the line edit
        self.flowRateInput = QLineEdit(self.flowRateInputFrame)
        self.flowRateInput.setMinimumSize(QSize(270, 50))
        self.flowRateInput.setToolTip("Type in your target value and hit Enter. To edit your input, "
                                      "right click to enable editing.")
        self.flowRateInput.setObjectName("flowRateInput")
        self.verticalLayout_11.addWidget(self.flowRateInput)
        self.verticalLayout_8.addWidget(self.flowRateInputFrame)

        # Action when user inputs variable, calls enterValue func
        self.flowRateInput.returnPressed.connect(lambda: self.enterValue(self.flowRateInput))

    # When the user enters a value, sets the value appropriately
    def enterValue(self, variable):
        # Grabbing the input from the line edit and storing it in value
        value = variable.text()

        # Based on which line edit calls this function, will set the given values as their respective Target Value
        if variable == self.flowRateInput:
            self.targetValues["Flow Rate"] = value
            self.flowRateInput.setReadOnly(True)
            self.flowEditMade = True
        elif variable == self.pHInput:
            self.targetValues["pH"] = value
            self.pHInput.setReadOnly(True)
            self.pHEditMade = True
        elif variable == self.tempInput:
            self.targetValues["Temperature"] = value
            self.tempInput.setReadOnly(True)
            self.tempEditMade = True

        # Check that each variable is given an input for Target Value from user
        if (self.targetValues["Temperature"] != 0 and self.targetValues["pH"] != 0 and
                self.targetValues["Flow Rate"] != 0):
            self.valueSignal.emit(self.targetValues)


# Main Window connects whole UI together and other widgets
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralwidget = QWidget(self)
        self.centralframe = QFrame(self.centralwidget)
        self.setupUI()

    def setupUI(self):
        # Setting up the central widget and frame
        self.setObjectName("MainWindow")
        self.resize(1500, 1200)
        self.centralwidget.setObjectName("centralwidget")
        self.centralframe.setGeometry(QRect(0, 0, 1500, 1140))
        self.centralframe.setFrameShape(QFrame.StyledPanel)
        self.centralframe.setFrameShadow(QFrame.Raised)
        self.centralframe.setObjectName("centralframe")
        self.horizontalLayout = QHBoxLayout(self.centralframe)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Side Panel setup
        self.sidePanelFrame = QFrame(self.centralframe)
        self.sidePanelFrame.setFrameShape(QFrame.Box)
        self.sidePanelFrame.setFrameShadow(QFrame.Raised)
        self.sidePanelFrame.setObjectName("sidePanelFrame")
        self.verticalLayout = QVBoxLayout(self.sidePanelFrame)
        self.verticalLayout.setObjectName("verticalLayout")

        # Watch Frame
        self.watchFrame = QFrame(self.sidePanelFrame)
        self.watchFrame.setFrameShape(QFrame.StyledPanel)
        self.watchFrame.setFrameShadow(QFrame.Raised)
        self.watchFrame.setObjectName("watchFrame")

        # Timer Setup
        self.timerWidget = TimerWidget(self.watchFrame)
        self.verticalLayout.addWidget(self.watchFrame)

        # Temp, Flow Rate, pH input widget
        self.inputWidget = VariableInputWidget(self.sidePanelFrame)
        self.verticalLayout.addWidget(self.inputWidget.variablesInputFrame)
        self.horizontalLayout.addWidget(self.sidePanelFrame, 0, Qt.AlignLeft)

        # Data/Graph Tabs Setup
        self.dataWidget = DataWidget(self.centralframe, self.timerWidget, self.inputWidget)
        self.horizontalLayout.addWidget(self.dataWidget.dataPanelFrame)

        # Finish set up central widgets
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 712, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # When user clicks the save button on the menu, saves current data to csv file
        # Sets up the save button
        self.actionSave = QAction(self)
        self.actionSave.setStatusTip("Click this to save the data of your current graphs.")
        self.actionSave.triggered.connect(self.dataWidget.saveData)
        self.actionSave.setObjectName("actionSave")

        # Menu file setup
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.setTitle("File")
        self.actionSave.setText("Save")


if __name__ == '__main__':
    # Main loop to create the UI window and run it for the user to see, ends when they close the window
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
