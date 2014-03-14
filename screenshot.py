import win32gui,win32con,win32process,autopy,time,re,subprocess
from autopy import bitmap,mouse

###screenshot_process_id

class WindowMgr:				#Has methods to find CFlow window handler, maximize that window, take screenshot, and search for bitmaps there
    """Encapsulates some calls to the winapi for window management"""
    def __init__ (self):
        """Constructor"""
        self._handle = None
        self._process_id = None
        self._pos= None
        self._screenshot= None
    def find_window(self, class_name, window_name = None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd,wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if win32process.GetWindowThreadProcessId(hwnd)[1]==self._process_id:
            if self._handle == None:
                self._handle = hwnd
            #print hwnd
        #print(win32process.GetWindowThreadProcessId(hwnd))

    def find_window_wildcard(self, wildcard='C:\\\\Program Files\\\\BD Accuri'):###THIS CHANGES FROM COMPUTER TO COMPUTER.
        """search for window with wildcard in its title"""
        self._handle = None
        cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process_list=[]
        for line in proc.stdout:
            process_list.append(line)
        regex=re.compile(wildcard)
        CFlow_process=[l for l in process_list for m in [regex.search(l)] if m]
        if len(CFlow_process)!=1:
            print('error! Could not locate CFlow process correctly')
        else:
            process_id=re.search('\s+(\d+)\s+',CFlow_process[0])
            self._process_id=int(process_id.group(1))
            win32gui.EnumWindows(self._window_enum_callback,'')
  
    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.ShowWindow(self._handle, win32con.SW_MINIMIZE)
        #print(self._handle)
        win32gui.ShowWindow(self._handle, win32con.SW_SHOWMAXIMIZED)
    def find_button_coordinates(self, button):
        """get coordinates where there is match between button bitmap and screen. They are stored in self._pos"""
        if self._screenshot==None:				#Only take screenshot if there is none in memory
            self.retake_screenshot()
        button=autopy.bitmap.Bitmap.open(button)
        self._pos = self._screenshot.find_bitmap(button)
    def retake_screenshot(self):
        """take screenshot again"""
#        self.maximize_window()
        autopy.mouse.move(1,1)
        autopy.mouse.move(0,0)
        time.sleep(0.5)
        self._screenshot=autopy.bitmap.capture_screen()
    def maximize_window(self):
        """Maximize window given in the handler"""
        self.find_window_wildcard()								#This here could change sometime, and it would make the program fail. It corresponds to
        if not self._handle:									#the program's title on the menu bar.
            print('CFlow not open! (no handle)')
            return
        self.set_foreground()
        time.sleep(0.5)

class MouseMvr:				#Has methods to move mouse and click buttons
    """Encapsulates some calls to the mouse module from autopy"""
    def __init__ (self):
        """Constructor"""
        self._position = None
    def click(self):
        """left-click"""
        autopy.mouse.click()
    def move(self,position):
        """left-click a certain position, indicated via a list of two elements"""
        autopy.mouse.move(position[0],position[1])
