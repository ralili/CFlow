import os,time,shutil,datetime,logging
from autopy import key,mouse
from CFlow.screenshot import *
##Optimize button_not_found.


class click:
    """Encapsulates some calls to the winapi for window management"""
    def __init__(self,sample_counter=0,image_directory='C:/Users/rumarc/Desktop/Images'):#Change directory where C6 images are stored
        """Constructor"""
        self._windowMgr=WindowMgr()
        self.time_counter=0
        self.sample_counter=sample_counter
        self.image_directory=image_directory
        self.export_counter=0
    def run(self,image_file="run_button_ready.png"):
        """Constructor"""
        self._windowMgr.retake_screenshot()
        try:
            self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#path to the image
        except IOError:
            logging.warning('Image file Run Button not found. Quitting..')
            return
        if self._windowMgr._pos == None:
            logging.warning('CFlow not ready to take measurements')
            if not self.button_not_found(image_file):
                return
        position=(self._windowMgr._pos[0]+73,self._windowMgr._pos[1]+22)
        mouse.move(position[0],position[1])
        mouse.click()
        self.time_counter=self.time_counter+1
        self.sample_counter=self.sample_counter+1
        self.delete_events()			#delete every 2 seconds, 5 times. Delete the first 10 seconds of measurement.
        if self.checking_end_of_measurements()==1:
            logging.info('measurement %d done',self.time_counter)
            self.add_sample_well_description()
            self.save()
        else:
            self.pause_cytometer()
            self.add_sample_well_description()
            self.save()
            logging.info('Running cytometer measurements took too long (more 5 minutes). Measurements were paused and proceeding to next step',self.time_counter)
            return
    def sample(self,image_file="sample_button2.png"):
        #self._windowMgr.maximize_window()
        """Constructor"""
        self._windowMgr.retake_screenshot()
        try:
            self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#path to the image
        except IOError:
            logging.warning('Image file Sample Button not found. Proceeding to next step..')
            return
        if self._windowMgr._pos == None:
            logging.warning('CFlow not open, no button positions available')
            if not self.button_not_found(image_file):
                return
        x_offset=(self.sample_counter%12)*24
        y_offset=(self.sample_counter/12)*24
        position=(self._windowMgr._pos[0]+x_offset+36,self._windowMgr._pos[1]+y_offset+8)	#position changed to bring to center of button
        mouse.move(position[0],position[1])
        mouse.click()
    def save(self):   # It needs to have been saved once already!!
        """Constructor"""
#        self._windowMgr.maximize_window()		##REMOVE
        key.tap(key.K_RETURN)
        time.sleep(0.1)
        key.tap(key.K_ALT)
        time.sleep(0.1)
        for i in range(3):
            key.tap(key.K_DOWN)
            time.sleep(0.1)
        key.tap(key.K_RETURN)
        time.sleep(2)
    def export(self):
#        self._windowMgr.maximize_window()		##REMOVE
        key.tap(key.K_RETURN)
        time.sleep(0.1)
        key.tap(key.K_ALT)
        time.sleep(0.1)
        for i in range(9):
            key.tap(key.K_DOWN)
            time.sleep(0.1)
        key.tap(key.K_RETURN)
        time.sleep(0.3)
        key.tap(key.K_RETURN)
        time.sleep(1)
    def backflush(self,image_file="backflush.png"):
        """Constructor"""
        self._windowMgr.retake_screenshot()
        try:
            self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#path to the image
        except IOError:
            logging.warning('Image file Backflush not found. Proceeding to next step..')
            return
        if self._windowMgr._pos == None:
            logging.warning('Not ready to backflush')
            if not self.button_not_found(image_file):
                return
        position=(self._windowMgr._pos[0]+32,self._windowMgr._pos[1]+24) #add position offset
        mouse.move(position[0],position[1])
        mouse.click()
        if self.checking_end_of_measurements()==1:
            return
        else:
            logging.warning('backflushing took too long. Moving on..')
            return
    def checking_end_of_measurements(self,image_file_ready="cytometer_ready.png"):##Add the checking whether CFlow is maximized. What if just don't minimize every time?
        """Constructor"""
        time.sleep(5)
        done=0
        too_much_time=0
        while not done:
            too_much_time=too_much_time+1
            time.sleep(5)				#Every how many seconds too_much_time increases by one unit
            self._windowMgr.retake_screenshot()
            try:
                self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file_ready))	#Name of the button image
            except IOError:
                logging.warning('Image file Cytometer Ready not found. Quitting..')
                return
            if self._windowMgr._pos != None:
                done=1
                return 1
            else:
                if too_much_time>60:					#When cytometer takes more than 5 minutes, pause operation and move on. too_much_time increases one unit every 5 seconds.
                    done=1
                    return 0
    def moveFiles(self,desktop_dir,destination_dir,CFlow_dir='FCS Exports'):
###move files from the folder that CFlow automatically makes to a specified folder.
        dir = os.path.join(desktop_dir,CFlow_dir)					#Find path to CFlow generated directory
        if os.path.exists(dir) and os.path.exists(destination_dir):
            automatic_CFlow_directory=[name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]		#Find folder inside the directory. There should only be one.
            if len(automatic_CFlow_directory)>0:
                self.export_counter=0
                automatic_CFlow_directory=os.path.join(dir,automatic_CFlow_directory[0])									#Get complete path to the folder where fcs files are
                if os.path.exists(automatic_CFlow_directory):
                    [shutil.copy2(os.path.join(automatic_CFlow_directory,name),destination_dir) for name in os.listdir(automatic_CFlow_directory)]	#move fcs files to new directory. If they are already present, they are replaced.
                    shutil.rmtree(automatic_CFlow_directory)																			#Remove the directory where the fcs files were. CHANGE TO SHUTIL.RMTREE()
                else:
                    logging.warning('Specified CFlow directory (where it exports) could not be found')
            elif self.export_counter!=1:
                logging.warning('Error. No files found to export. Trying to export once more')
#                self._windowMgr.maximize_window()
                self.export_counter=1
                self.export()
                time.sleep(2)
                self.moveFiles(desktop_dir,destination_dir,CFlow_dir)
            else:
                logging.warning('Error. Still no files found to export')
                self.export_counter=0
        else:
            logging.warning('specified paths for Desktop or Output could not be found')
    def set_measuring_times(self,day,hour,minute,frequency,num_samples):#frequency is in minutes
        self.measuring_times=[]
        time_today=datetime.datetime.now()
        starting_time=datetime.datetime(time_today.year,time_today.month,day,hour,minute,second=0) #User input is only day,hour,minute,second
        for i in range(num_samples):
            self.measuring_times.append(starting_time+datetime.timedelta(minutes=frequency*i))
        measuring_times_string='\n'
        for i in self.measuring_times:
            measuring_times_string=measuring_times_string+'  '+str(i)+'\n'
        logging.info('The measuring times will be: %s',measuring_times_string)
    def set_waiting_time(self):
        if len(self.measuring_times)>self.time_counter:
            self.waiting_time=(self.measuring_times[self.time_counter]-datetime.datetime.now()).total_seconds()
            if self.waiting_time<0:
                logging.warning('timepoint %s already passed. Waiting for the next one'%(str(self.measuring_times[self.time_counter]))) #If timepoint has passed, wait for the next one (or should we just measure right away?)
                self.time_counter=self.time_counter+1
                self.sample_counter=self.sample_counter+1
                self.set_waiting_time()
            else:
                return 0						#This indicates that experiment is NOT done, and that there is a next measurement.
        else:
            logging.info('Experiment is done!!')
            return 1						#This indicates that experiment IS done. Close everything.
    def delete_events(self,frequency=2,repetitions=5,image_file="delete_events.png"):##Frequency is how many seconds to erase every time. Repetitions is how many times to erase
        """Constructor"""
        self._windowMgr.retake_screenshot()
        try:
            self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#path to the image
        except IOError:
            logging.warning('Image file Delete Events not found. Quitting..')
            return
        if self._windowMgr._pos == None:
            logging.warning('Could not delete events. Button not found on screen')
        else:
            time.sleep(15)
            for i in range(repetitions):
                time.sleep(frequency)
                position=(self._windowMgr._pos[0]+32,self._windowMgr._pos[1]+15) #add position offset
                mouse.move(position[0],position[1])
                time.sleep(0.1)
                mouse.click()
                time.sleep(0.4)
                key.tap(key.K_RETURN)
    def pause_cytometer(self,image_file="pause.png"):
        """Constructor"""
        self._windowMgr.retake_screenshot()
        try:
            self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#path to the image
        except IOError:
            logging.warning('Image file Pause not found. Quitting..')
            return
        if self._windowMgr._pos == None:
            logging.warning('Could not pause cytometer operation. Button not found on screen')
            if not self.button_not_found(image_file):
                return
        position=(self._windowMgr._pos[0]+50,self._windowMgr._pos[1]+10) #add position offset
        mouse.move(position[0],position[1])
        mouse.click()
    def add_sample_well_description(self,image_file="sample_well_description.png"):
        """Constructor"""
        self._windowMgr.retake_screenshot()
        try:
            self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#path to the image
        except IOError:
            logging.warning('Image file Sample Well Description not found. Quitting..')
            return
        if self._windowMgr._pos == None:
            logging.warning('Could not add sample well description. Button not found on screen')
            if not self.button_not_found(image_file):
                return
        position=(self._windowMgr._pos[0]+80,self._windowMgr._pos[1]+8) #add position offset
        mouse.move(position[0],position[1])
        mouse.click()
        time.sleep(0.5)
        sample_time=datetime.datetime.now()
        sample_time=''.join([str(sample_time.hour),'h',str(sample_time.minute),'m'])
        key.type_string(sample_time)
    def button_not_found(self,image_file,image_location='C://Users//rumarc//Desktop//Results'):		#Path where error image is saved needs to be set!!
        """Constructor"""
        ####Save screenshot. Wait 10s and try to find image again. If none found, warning and continue.
        sample_time=datetime.datetime.now()
        self._windowMgr._screenshot.save(os.path.join(image_location,''.join(['error',str(sample_time.hour),'h',str(sample_time.minute),'m','.bmp'])))#Save the error screenshot
        time.sleep(10)
        self._windowMgr.retake_screenshot()
        self._windowMgr.find_button_coordinates(os.path.join(self.image_directory,image_file))	#path to the image
        if self._windowMgr._pos == None:
            logging.warning('Image file was still not found. Operation will proceed, skipping this step.')
            return 0
        return 1