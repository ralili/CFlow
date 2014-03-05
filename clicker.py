import CFlow,autopy,os,time,shutil,datetime
from autopy import key



class click:
    """Encapsulates some calls to the winapi for window management"""
    def __init__(self,image_directory='C:/Users/rumarc/Desktop/Images'):
        """Constructor"""
        self._windowMgr=CFlow.WindowMgr()
        self._mouseMvr=CFlow.MouseMvr()
        self.counter=0
        self.image_directory=image_directory
    def run(self,image_file="run_button_ready.png"):
        """Constructor"""
        self._windowMgr.retake_screenshot()
        try:
            self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#Name of the button image
        except IOError:
            print('Image file not found. Quitting..')
            autopy.alert.alert('Image file not found. Quitting..')
            return
        if self._windowMgr._pos == None:
            autopy.alert.alert('CFlow not ready to take measurements')
        else:
            position=(self._windowMgr._pos[0]+73,self._windowMgr._pos[1]+22)
            self._mouseMvr.move(position)
            self._mouseMvr.click()
            self.counter=self.counter+1
            if self.checking_end_of_measurements()==1:
                self.save()
            else:
                return 'stuff took too long. Quitting..'
    def sample(self,image_file="sample_button2.png"):
        """Constructor"""
        self._windowMgr.retake_screenshot()
        try:
            self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#Name of the button image
        except IOError:
            print('Image file not found. Quitting..')
            autopy.alert.alert('Image file not found. Quitting..')
            return
        if self._windowMgr._pos == None:
            autopy.alert.alert('CFlow not open, no button positions available')
        else:
            x_offset=(self.counter%12)*24
            y_offset=(self.counter/12)*24
            position=(self._windowMgr._pos[0]+x_offset+36,self._windowMgr._pos[1]+y_offset+8)	#position changed to bring to center of button
            self._mouseMvr.move(position)
            self._mouseMvr.click()
    def save(self):   # It needs to have been saved once already!!
        """Constructor"""
        self._windowMgr.maximize_window()
        key.tap(key.K_ALT)
        key.tap(key.K_RETURN)
        key.tap(key.K_DOWN)
        key.tap(key.K_DOWN)
        key.tap(key.K_DOWN)
        key.tap(key.K_RETURN)
        #key.tap(key.K_RETURN); 
    def export(self):
        self._windowMgr.maximize_window()
        key.tap(key.K_ALT)
        key.tap(key.K_RETURN)
        for i in range(9):
            key.tap(key.K_DOWN)
        key.tap(key.K_RETURN)
        time.sleep(0.2)
        key.tap(key.K_RETURN)

    def backflush(self,image_file="backflush.png"):
        """Constructor"""
        self._windowMgr.retake_screenshot()
        try:
            self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#Name of the button image
        except IOError:
            print('Image file not found. Quitting..')
            autopy.alert.alert('Image file not found. Quitting..')
            return
        if self._windowMgr._pos == None:
            autopy.alert.alert('Not ready to backflush')
        else:
            position=(self._windowMgr._pos[0]+32,self._windowMgr._pos[1]+24) #add position offset
            self._mouseMvr.move(position)
            self._mouseMvr.click()
            if self.checking_end_of_measurements()==1:
                return
            else:
                return 'stuff took too long. Quitting..'

    def checking_end_of_measurements(self,image_file_ready="cytometer_ready.png"):##Add the checking whether CFlow is maximized. What if just don't minimize every time?
        """Constructor"""
        time.sleep(5)
        done=0
        too_much_time=0
        while not done:
            too_much_time=too_much_time+1
            time.sleep(5)
            self._windowMgr.retake_screenshot()			#This causes CFlow to maximize its window every 5seconds, which is kind of anoying. Maybe just check if it is maximized?
            try:
                self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file_ready))	#Name of the button image
            except IOError:
                print('Image file not found. Quitting..')
                #autopy.alert.alert('Image file not found. Quitting..')
                return
            if self._windowMgr._pos != None:
                #print self._windowMgr._pos
                #autopy.alert.alert('measurements done')
                done=1
                return 1
            else:
#                try:
#                    self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file_not_ready))	#Name of the button image
#                except IOError:
#                    print('Image file not found. Quitting..')
#                    #autopy.alert.alert('Image file not found. Quitting..')
#                    return
#                if self._windowMgr._pos == None:
#                    
#                    
#                    
                if too_much_time>30:
                    print('Measurement takes too much time. Quitting..')
                    #autopy.alert.alert('Measurement takes too much time. Quitting..')
                    done=1
                    return 0
    def moveFiles(self,desktop_dir,destination_dir,CFlow_dir='FCS Exports'):
###move files from the folder that CFlow automatically makes to a specified folder.
        dir = os.path.join(desktop_dir,CFlow_dir)					#Find path to CFlow generated directory
        automatic_CFlow_directory=[name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]		#Find folder inside the directory. There should only be one.
        automatic_CFlow_directory=os.path.join(dir,automatic_CFlow_directory[0])									#Get complete path to the folder where fcs files are
        [shutil.copy2(os.path.join(automatic_CFlow_directory,name),destination_dir) for name in os.listdir(automatic_CFlow_directory)]	#move fcs files to new directory. If they are already present, they are replaced.
        shutil.rmtree(automatic_CFlow_directory)																			#Remove the directory where the fcs files were. CHANGE TO SHUTIL.RMTREE()
		####IT WORKS. TO TEST IT, ONE CAN USE THE FOLLOWING DIRECTORIES
		##desktop_dir='C:\\Users\\rumarc\\Desktop'
		##CFlow_dir='CFlow-FCS Exports'
		##dir = os.path.join(desktop_dir,CFlow_dir)
    def set_measuring_times(self,day,hour,minute,frequency,num_samples):#frequency is in minutes
        self.measuring_times=[]
        time_today=datetime.datetime.now()
        starting_time=datetime.datetime(time_today.year,time_today.month,day,hour,minute,second=0) #User input is only day,hour,minute,second
        number_samples=num_samples
        for i in range(number_samples):
            self.measuring_times.append(starting_time+datetime.timedelta(minutes=frequency*i))
        print('The measuring times will be:')
        for i in range(len(self.measuring_times)):
            print ('\n %s \n'%(self.measuring_times[i]))
    def set_waiting_time(self):
        if len(self.measuring_times)>self.counter:
            self.waiting_time=(self.measuring_times[self.counter]-datetime.datetime.now()).total_seconds()
            if self.waiting_time<0:
                print('timepoint %s already passed. Waiting for the next one'%(str(self.measuring_times[self.counter]))) #If timepoint has passed, wait for the next one (or should we just measure right away?)
                self.counter=self.counter+1
                self.set_waiting_time()
            else:
                return 0						#This indicates that experiment is NOT done, and that there is a next measurement.
        else:
            print('Experiment is done!!')
            return 1						#This indicates that experiment IS done. Close everything.
#    def set_led_times(self,day,hour,minute,frequency,num_samples):#frequency is in minutes
#        self.measuring_times=[]
#        time_today=datetime.datetime.now()
#        starting_time=datetime.datetime(time_today.year,time_today.month,day,hour,minute,second=0) #User input is only day,hour,minute,second
#        number_samples=num_samples
#        for i in range(number_samples):
#            self.measuring_times.append(starting_time+datetime.timedelta(minutes=frequency*i))
#        print('The measuring times will be:')
#        for i in range(len(self.measuring_times)):
#            print ('\n %s \n'%(self.measuring_times[i]))