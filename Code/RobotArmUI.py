# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import wx
from Adafruit_PWM_Servo_Driver import PWM
import time
import json
from time import sleep
# import RasPiBot

# Test servo screen - 0 = servo neutral position
# servo_list = [["Head", 0], ["Neck", 0], ["Left shoulder", 0], ["Left bicep", 0],
              #["Left hand", 0], ["Left hip", 0], ["Left knee", 0], ["Left ankle", 0],
              #["Right shoulder", 0], ["Right bicep", 0], ["Right hand", 0], ["Right hip", 0],
              #["Right knee", 0],["Right ankle", 0]]

servo_list = []

pwm = PWM(0x40)
servoMin = 150
servoMax = 600
minAngle = -90
maxAngle = 90

pwm.setPWMFreq(50)


class ServoButton(wx.Button):
    def __init__(self, servo_id, servo_pos, myframe, *args, **kwargs):
        wx.Button.__init__(self, *args, **kwargs)
        self.servo_id = servo_id
        self.servo_pos = servo_pos
        self.frame = myframe
        self.logger = myframe.logger
        self.change = myframe.my_change_val

    def DegreesToPulseLength(self, degrees, in_min, in_max, out_min,out_max):
        return ((degrees - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def Rotate(self, servoindex, value):
        print("Inside Rotate " + str(servoindex) + " value " + str(value))
        if (servoindex < 0 or servoindex > 15):
            print("Invalid servo number (0-15)")
        elif value < - 90 or value > 90:
            print("Invalid rotation angle (-90 - 90")
        else:
            print(value, servo_list[servoindex][1], minAngle, maxAngle,
                                                    servoMin, servoMax)

            pulseLength = self.DegreesToPulseLength(value, minAngle, maxAngle,
                                                    servoMin, servoMax)
            print(pulseLength)
            pwm.setPWM(servoindex, 50, pulseLength)

    def OnButton(self, e):
        def get_index(mylist, searchstr):
            return [y[0] for y in mylist].index(searchstr)

        def update_val(index):
            if index == 0:
                frame.servo_val_0.SetValue(str(servo_list[0][1]))
            if index == 1:
                frame.servo_val_1.SetValue(str(servo_list[1][1]))
            if index == 2:
                frame.servo_val_2.SetValue(str(servo_list[2][1]))
            if index == 3:
                frame.servo_val_3.SetValue(str(servo_list[3][1]))
            if index == 4:
                frame.servo_val_4.SetValue(str(servo_list[4][1]))
            if index == 5:
                frame.servo_val_5.SetValue(str(servo_list[5][1]))
            if index == 6:
                frame.servo_val_6.SetValue(str(servo_list[6][1]))
            if index == 7:
                frame.servo_val_7.SetValue(str(servo_list[7][1]))
            if index == 8:
                frame.servo_val_8.SetValue(str(servo_list[8][1]))
            if index == 9:
                frame.servo_val_9.SetValue(str(servo_list[9][1]))
            if index == 10:
                frame.servo_val_10.SetValue(str(servo_list[10][1]))
            if index == 11:
                frame.servo_val_11.SetValue(str(servo_list[11][1]))
            if index == 12:
                frame.servo_val_12.SetValue(str(servo_list[12][1]))
            if index == 13:
                frame.servo_val_13.SetValue(str(servo_list[13][1]))

        # Send command to servo hat here
        if self.servo_id[-2:] == "up":
            servo_name = self.servo_id[:(len(self.servo_id) - 3)]
            myindex = get_index(servo_list, servo_name)
            servo_list[myindex][1] += frame.my_change_val
            direction = '+'
            update_val(myindex)
            # rotate up - positif
            print("Rotate " + str(myindex) + " val " + str(frame.my_change_val))
            self.Rotate(myindex, servo_list[myindex][1])

        else:
            servo_name = self.servo_id[:(len(self.servo_id) - 5)]
            myindex = get_index(servo_list, servo_name)
            servo_list[myindex][1] -= frame.my_change_val
            direction = '-'
            update_val(myindex)
            # rotate down - négatif
            print("Rotate " + str(myindex) + " val -" + str(frame.my_change_val))
            self.Rotate(myindex, servo_list[myindex][1])

        self.logger.AppendText(" Click on {} - pos = {} {} {} = {}\n".format(self.servo_id, str(self.servo_pos), direction, frame.my_change_val, servo_list[myindex][1]))


class MyRobotUi(wx.Frame):
    # Interface visuelle pour déboguage du RasPiBot.py
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 800))

        BUTTON_SIZE = (160, 30); X1_POS = 30; X2_POS = 200; Y_POS = 40

        self.panel = wx.Panel(self, pos=(X1_POS, Y_POS)) # up button panel
        self.panel2 = wx.Panel(self, pos=(X2_POS, Y_POS)) # down button panel
        self.panel3 = wx.Panel(self, pos=(370, 40)) # servo value panel
        self.panel3.SetBackgroundColour('LIGHT GREY')
        self.radiopanel = wx.Panel(self, pos=(50, 5), size=(300, 30))
        self.logger = wx.TextCtrl(self, pos=(470, 20), size=(300, 600), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.rb1 = wx.RadioButton(self.radiopanel, -1, '1 degré', (10, 7), style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self.radiopanel, -1, '5 degré', (90, 7))
        self.rb3 = wx.RadioButton(self.radiopanel, -1, '10 degré', (170, 7))

        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)

        my_input_size = (50, 24)
        nbr_servo = len(servo_list)
        print(nbr_servo)
        # Beaucoup de repetition de code ici, a refactoré eventuellement
        self.sizer_ver_03 = wx.BoxSizer(wx.VERTICAL)
        myborder = 3.2
        
        if (nbr_servo > 0):
            self.servo_val_0 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[0][1]))
            self.sizer_ver_03.Add(self.servo_val_0, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 1):
            self.servo_val_1 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[1][1]))
            self.sizer_ver_03.Add(self.servo_val_1, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 2):
            self.servo_val_2 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[2][1]))
            self.sizer_ver_03.Add(self.servo_val_2, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 3):
            self.servo_val_3 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[3][1]))
            self.sizer_ver_03.Add(self.servo_val_3, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 4):
            self.servo_val_4 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[4][1]))
            self.sizer_ver_03.Add(self.servo_val_4, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 5):
            self.servo_val_5 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[5][1]))
            self.sizer_ver_03.Add(self.servo_val_5, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 6):
            self.servo_val_6 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[6][1]))
            self.sizer_ver_03.Add(self.servo_val_6, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 7):
            self.servo_val_7 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[7][1]))
            self.sizer_ver_03.Add(self.servo_val_7, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 8):
            self.servo_val_8 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[8][1]))
            self.sizer_ver_03.Add(self.servo_val_8, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 9):
            self.servo_val_9 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                           value=str(servo_list[9][1]))
            self.sizer_ver_03.Add(self.servo_val_9, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder) 
            
        if (nbr_servo > 10):
            self.servo_val_10 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                            value=str(servo_list[10][1]))
            self.sizer_ver_03.Add(self.servo_val_10, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 11):
            self.servo_val_11 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                            value=str(servo_list[11][1]))
            self.sizer_ver_03.Add(self.servo_val_11, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 12):
            self.servo_val_12 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                            value=str(servo_list[12][1]))
            self.sizer_ver_03.Add(self.servo_val_12, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
            
        if (nbr_servo > 13):
            self.servo_val_13 = wx.TextCtrl(self.panel3, size=my_input_size, style=wx.TE_READONLY,
                                            value=str(servo_list[13][1]))
            self.sizer_ver_03.Add(self.servo_val_13, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=myborder)
        
        self.panel3.SetSizerAndFit(self.sizer_ver_03)
        self.my_change_val = 1
        self.buttons = []

        for servo in servo_list:
            mybutton = ServoButton(servo_id=str(servo[0]) + " up", servo_pos=servo[1], parent=self.panel,
                                   label=str(servo[0])+" up", size=BUTTON_SIZE, myframe=self)
            mybutton.Bind(wx.EVT_BUTTON, mybutton.OnButton)
            self.buttons.append(mybutton)

        self.sizer_ver = wx.BoxSizer(wx.VERTICAL)

        for button in self.buttons:
            self.sizer_ver.Add(button)
        self.panel.SetSizerAndFit(self.sizer_ver)

        self.buttons = []
        for servo in servo_list:
            mybutton = ServoButton(servo_id=str(servo[0]) + " down", servo_pos=servo[1], parent=self.panel2,
                                   label=str(servo[0]) + " down", size=BUTTON_SIZE, myframe=self)
            mybutton.Bind(wx.EVT_BUTTON, mybutton.OnButton)
            self.buttons.append(mybutton)

        self.sizer_ver_02 = wx.BoxSizer(wx.VERTICAL)
        for button in self.buttons:
            self.sizer_ver_02.Add(button)
        self.panel2.SetSizerAndFit(self.sizer_ver_02)

        self.CreateStatusBar()  # A Statusbar in the bottom of the window

        # creation du menu
        progmenu = wx.Menu()
        robotmenu = wx.Menu()
        sequencemenu = wx.Menu()

        menu_item_about = progmenu.Append(wx.ID_ABOUT, "&A propos", " Information sur RasPiBot UI")
        progmenu.AppendSeparator()
        menu_item_exit = progmenu.Append(wx.ID_EXIT, "Q&uitter", " Quitté le programme")

        menu_item_robot_new = robotmenu.Append(wx.ID_ANY, "New", "Module New robot")
        menu_item_robot_load = robotmenu.Append(wx.ID_ANY, "Load", "Module load robot")
        menu_item_robot_edit = robotmenu.Append(wx.ID_ANY, "Edit", "Module edit robot")

        menu_item_sequenceur_new = sequencemenu.Append(wx.ID_ANY, "New", "Module New")
        menu_item_sequenceur_load = sequencemenu.Append(wx.ID_ANY, "load", " Module load")
        menu_item_sequenceur_edit = sequencemenu.Append(wx.ID_ANY, "Edit", " Module edit")

        # Création de la barre de menu.
        menuBar = wx.MenuBar()
        menuBar.Append(progmenu, "&Programme")  # rajout de fichier au MenuBar
        menuBar.Append(robotmenu, "&Robot")  # rajout de Robot au MenuBar
        menuBar.Append(sequencemenu, "&Sequenceur")  # rajout de Sequenceur au MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Show(True)

        # set events
        self.Bind(wx.EVT_MENU, self.on_about, menu_item_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_item_exit)
        
        self.Bind(wx.EVT_MENU, self.on_LoadRobot, menu_item_robot_load)
        self.Bind(wx.EVT_MENU, self.on_NewRobot, menu_item_robot_new)
        self.Bind(wx.EVT_MENU, self.on_EditRobot, menu_item_robot_edit)

        self.Bind(wx.EVT_MENU, self.on_LoadSequence, menu_item_sequenceur_load)
        self.Bind(wx.EVT_MENU, self.on_NewSequence, menu_item_sequenceur_new)
        self.Bind(wx.EVT_MENU, self.on_EditSequence, menu_item_sequenceur_edit)
        
        self.Show(True)

    def on_about(self, e):
        print("On about clicked")
        dlg = wx.MessageDialog(self, "RasPiBot Robot Arm by Andre Cooke", "About", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def on_exit(self, e):
        self.Close(True)  # Close the frame.

    def on_LoadRobot(self, event):
		self.logger.AppendText(" Selected on Load Robot \n")

    def on_NewRobot(self, event):
		self.logger.AppendText(" Selected on New Robot \n")
		
    def on_EditRobot(self, event):
		self.logger.AppendText(" Selected on Edit Robot \n")
		
    def on_LoadSequence(self, event):
		self.logger.AppendText(" Selected on Load Sequence \n")

    def on_NewSequence(self, event):
		self.logger.AppendText(" Selected on New Sequence \n")
		
    def on_EditSequence(self, event):
		self.logger.AppendText(" Selected on Edit Sequence \n")		

    def click_on(self, event):
		name = event.GetEventObject().bname
		self.logger.AppendText(" Click on object with Id {} {} \n".format(event.GetId(), name))

    def OnRadiogroup(self, e):
        rb = e.GetEventObject()
        myval = int(rb.GetLabel()[:2].strip())
        self.my_change_val = myval
        self.logger.AppendText(" changé valeur a {} \n".format(myval))

class Methods():
    def saveRobot(servo_list, filename):
        json_format = json.dumps(servo_list)
        with open(filename, 'w') as outfile: 
            outfile.write(json_format)
            
    def loadRobot(self, filename):
        with open(filename) as json_file:
            return json.load(json_file)

myMethods = Methods()
servo_list = myMethods.loadRobot('RaspiArm.robot')

app = wx.App(False)
frame = MyRobotUi(None, 'Robot UI')

app.MainLoop()
