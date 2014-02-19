import os
import shutil
import xbmc, xbmcgui
	
Addon_NAME='Navi-X freeze fix'
ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92

def LoG(t=''): print Addon_NAME+": "+t
def notification(header="", message="", sleep=5000 ): xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i)" % ( header, message, sleep ) )

class Display(xbmcgui.Window):
	#display a two input dialog box for install and uninstall
	def __init__(self):
		self.background = (xbmc.translatePath('special://home/addons/script.program.Navi-X-freeze-fix/fanart.jpg'))
		self.addControl(xbmcgui.ControlImage(0,0,1280,720, self.background, aspectRatio=2))
		self.strActionInfo = xbmcgui.ControlLabel(520, 300, 300, 300, '', 'font30', '0xFFFF00FF')
		self.addControl(self.strActionInfo)
		self.strActionInfo.setLabel(Addon_NAME)
		self.button0 = xbmcgui.ControlButton(450, 380, 80, 30, "  Fix")
		self.addControl(self.button0)
		self.button1 = xbmcgui.ControlButton(590, 380, 80, 30, " Undo")
		self.addControl(self.button1)
		self.button2 = xbmcgui.ControlButton(750, 380, 80, 30, "  Exit")
		self.addControl(self.button2)
		self.setFocus(self.button0)
		self.button0.controlRight(self.button1)
		self.button0.controlLeft(self.button2)
		self.button1.controlRight(self.button2)
		self.button1.controlLeft(self.button0)
		self.button2.controlRight(self.button0)
		self.button2.controlLeft(self.button1)
		
	def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
		if action == ACTION_NAV_BACK:
			self.close()

	def onControl(self, control):
		if control == self.button0:
			Main().Main_install()
			
		if control == self.button1:
			Main().Main_uninstall()
			
		if control == self.button2:
			self.close()

def message(title, message):
	dialog = xbmcgui.Dialog()
	dialog.ok(title, message)

directory_NaviX = (xbmc.translatePath('special://home/addons/Navi-X'))

class Main():
	#set main vars
	directory_navi_src = (xbmc.translatePath('special://home/addons/Navi-X/src' ))
	fix_dir = (xbmc.translatePath('special://home/addons/script.program.Navi-X-freeze-fix/src' ))
	addon_xml = os.path.join(directory_NaviX, 'addon.xml')
	navix = os.path.join(directory_navi_src,'navix.py')
	navix_old = os.path.join(directory_navi_src,'navix.old')
	fileloader = os.path.join(directory_navi_src,'CFileLoader.py')
	fileloader_old = os.path.join(directory_navi_src,'CFileLoader.old')

	def Main_install(self):
		LoG("hello. install."); 
		#if (os.path.exists(self.navix) != True) or (os.path.exists(self.fileloader) != True):
		if (not os.path.exists(self.navix)==True) or (not os.path.exists(self.fileloader)==True):
			message("Error", "You do not appear to have Navi-X installed.")
			#notification("Error", "You do not appear to have Navi-X installed."); 
		else:
			if os.path.exists(self.navix) == True:
				if os.path.exists(self.navix_old) == True:
					os.remove(self.navix)
				else:
					os.rename(self.navix, self.navix_old)
			shutil.copy2(os.path.join(self.fix_dir,'navix.py'), self.directory_navi_src)
		
			if os.path.exists(self.fileloader) == True:
				if os.path.exists(self.fileloader_old) == True:
					os.remove(self.fileloader)
				else:
					os.rename(self.fileloader, self.fileloader_old)
			shutil.copy2(os.path.join(self.fix_dir,'CFileLoader.py'), self.directory_navi_src)	
			
			message("Success", "The fix has been installed.")
			#notification("Success", "The fix has been installed."); 
			LoG("fix. installed."); 


	def Main_uninstall(self):
		LoG("hello. uninstall."); 
		if (not os.path.exists(self.navix)==True) or (not os.path.exists(self.fileloader)==True):
			notification("Error", "You do not appear to have Navi-X installed."); 
		elif (os.path.exists(self.navix_old) != True) or (os.path.exists(self.fileloader_old) != True):
			message("Error", "You do not appear to have original files to restore from. \nOr have not run this fix before")
			#notification("Error", "You do not appear to have Navi-X freeze fix installed."); 
		else:
			if os.path.exists(self.navix) == True:
				os.remove(self.navix)
				os.rename(self.navix_old, self.navix)
		
			if os.path.exists(self.fileloader) == True:
				os.remove(self.fileloader)
				os.rename(self.fileloader_old,self.fileloader)
					
			message("Success", "The fix has been removed.")
			#notification("Success", "The fix has been removed."); 
			LoG("fix. removed."); 

#check for Navi-X version 3.7.8 in line 4 of addon.xml
if os.path.exists(directory_NaviX) ==True:
	version=''
	with open(Main().addon_xml, 'r') as xml:
		for line in xml:
			if ('"3.7.8"') in line:
				LoG("version. valid."); 
				version = 'valid'
				break
	xml.close()
	if version == 'valid':					
		fix_display = Display()
		fix_display.doModal()
		del fix_display					
	else:  
		message("Notice", "You need Navi-X version 3.7.8 to run this fix.")
else: 
	message("Notice", "Cant find the Navi-X folder. \nPlease install the official Navi-X addon.")

				
#EOF			
