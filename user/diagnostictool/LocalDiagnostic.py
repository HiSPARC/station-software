from Tkinter import *
from hslog import *
import ConfigParser
import collections
import os
import commands
import sys
import ScrolledText


sys.path.insert(1, '../diagnosticchecks')
from checks import *

CONFIG_INI="config.ini"
STATES=[]
errorMessageTxt=''
windowWidth=900
windowHeight=700
ok=0
critical=2
notFound=3

def ReadStepsFromConfig():
	config = ConfigParser.ConfigParser()
	config.read(CONFIG_INI)	
	listSteps = config.items("DiagnosticSteps", raw='true')
	return listSteps
	
def ReadScriptsNameFromConfig():
	config = ConfigParser.ConfigParser()
	config.read(CONFIG_INI)	
	listScripts=config.items("CheckScripts")
	return listScripts
	
def ReadSuggestionFromConfig():
	config = ConfigParser.ConfigParser()
	config.read(CONFIG_INI)	
	listSuggestions=dict(config.items("Suggestions", raw='true'))
	return listSuggestions
	

	
class App:

	def __init__(self,parent):
		
		self.myParent = parent 
		#create the main Frame
		self.myContainer = Frame(parent,width=windowWidth, height=windowHeight) 
		self.myContainer.pack()
		#set fix size for the container
		self.myContainer.pack_propagate(False)

		
		#create top frame
		self.top_frame = Frame(self.myContainer,width=windowWidth, height=85) 
		self.top_frame.pack(side=TOP,fill=BOTH,expand=YES) 
		#set fix size for the top frame
		self.top_frame.pack_propagate(False) 
		
		#add the logo picture
		
		#myCanvas = Canvas(self.top_frame, width=150, height=100)
		#photo = PhotoImage(file="logo.gif")
		#myCanvas.create_image(81,53, image=photo)
		#myCanvas.pack()
		#self.myCanvas = Canvas(self.top_frame, width=170, height=90)
		#self.myCanvas.pack(expand = YES, fill = BOTH)
		#photo = PhotoImage(file="logo.gif")
		#self.myCanvas.create_image(81, 53, image=photo,anchor=CENTER)
		
		#create left frame
		
		self.left_frame = Frame(self.top_frame,borderwidth=1,relief=GROOVE,height=windowHeight-90,width=2*windowWidth/6,padx=10, pady=10)
		self.left_frame.pack(side=LEFT,fill=NONE,expand=1)
		#set fix size for the left frame
		self.left_frame.pack_propagate(False) 
		
		#create right frame
		self.right_frame=Frame(self.top_frame, borderwidth=1,relief=GROOVE,height=windowHeight-90,width=5*windowWidth/6,padx=10, pady=10)
		self.right_frame.pack(side=RIGHT,fill=NONE,expand=1) 
		self.right_frame.pack_propagate(False) 
		
		self.labelResult = Label(self.right_frame, text="Here are the diagnose results!").pack( side=TOP, anchor=W, padx=2, pady=2)
		
		
		# scroll text
		sbar = Scrollbar(self.right_frame)
		self.resultText=Text(self.right_frame,takefocus=0,font=11, relief=SUNKEN)
		sbar.config(command=self.resultText.yview)               
		self.resultText.config(yscrollcommand=sbar.set)           
		sbar.pack(side=RIGHT, fill=Y)                 
		self.resultText.pack(side=LEFT, expand=YES, fill=BOTH)  
		
		
		
		#we then create a label widget, then for each check we create a checkbox
		listOfSteps=ReadStepsFromConfig()
		self.label = Label(self.left_frame, text="Choose the checks you want to run:").pack( side=TOP, anchor=W, padx=2, pady=2)
		x=10
		y=5
		for step in listOfSteps:
			nameButton=str(step[0])
			cbVar = IntVar()
			self.nameButton = Checkbutton(self.left_frame,text= step[0], variable=str(cbVar))
			self.nameButton.pack(side= TOP,anchor=W, padx=x,pady=y)
			#for each checkbox read the select/deselect value from the conf file
			if(int(step[1])==1):
				self.nameButton.select()
			else:
				self.nameButton.deselect()
			STATES.append(cbVar)
		
		#create "start diagnose" button and associate the event handler function
		self.start = Button(self.left_frame)
		self.start["text"] = 'Start diagnostic'
		self.start["command"] = self.buttonClick
		self.start.pack(side=TOP,anchor=W,padx=x,pady=y)
		
		#create the error message label at the bottom of the window
		global errorMessageTxt
		errorMessageTxt=StringVar()
		self.errorMessage = Label(self.left_frame,textvariable=errorMessageTxt,wraplength=5*windowWidth/6-50)
		self.errorMessage.config(fg='red', justify=LEFT) 
		self.errorMessage.pack( side=BOTTOM,anchor=W, padx=x, pady=y)


	def buttonClick(self):
		#delete previous error messages
		errorMessageTxt.set('')
		log('\nStarted diagnostic...')
		#get script names from config
		listOfScripts=ReadScriptsNameFromConfig()
		
		#get list of suggestions from conf file
		listSuggestions=ReadSuggestionFromConfig()
		
		#delete previous results from results textbox
		self.resultText.delete(0.0, END)
		
		iterator=0
		nrExceptions=0
		
		exceptionString='' #string that gathers the error message
		#string that gather result message
		resultString='' 
		resultArray=dict()
		
		for i in STATES:
			if i.get() == 1:
				try:
					res=eval(listOfScripts[iterator][1])()
					resultArray[listOfScripts[iterator]]=res
						
				except Exception:
					nrExceptions=nrExceptions+1
					exceptionString+='%s' %listOfScripts[iterator][1]
					exceptionString+=' ,'
					resultArray[listOfScripts[iterator]]=notFound
					
					
			iterator=iterator+1
		
		iterator=0
		
		#for each of the checks performed, display result in the result textbox
		for check in resultArray:
			resultString+= '\n'
			if resultArray[check]==ok:
				resultString+='Check: '
				resultString+=str(check[0])
				resultString+=' succeeded! \n'
			elif resultArray[check]==critical:
				resultString+='Check: '
				resultString+=str(check[0])
				resultString+=' failed!'
				resultString+='\n-->How to solve it:'
				resultString+= listSuggestions[check[0]]
				resultString+= '.\n'
			else:
				resultString+='Check: '
				resultString+=str(check[0])
				resultString+=' was not found!\n'
			iterator=iterator+1
		
		if nrExceptions!=0:
			textToDisplay='%d functions were not found:' %nrExceptions
			textToDisplay+= exceptionString
			textToDisplay+='\n'
			textToDisplay+= 'Please check the configuration file and checks.py file!'
			errorMessageTxt.set(textToDisplay)
			log(textToDisplay)
		#insert result text into textbox
		log(resultString)
		self.resultText.insert(0.0, resultString)	
	
	
root = Tk()
root.title('HiSparc Local Diagnostic Tool')
root.geometry("%dx%d" %(windowWidth, windowHeight))
root.resizable(width=FALSE, height=FALSE)
app = App(root)

root.mainloop()
