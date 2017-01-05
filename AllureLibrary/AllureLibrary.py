from AllureListener import AllureListener
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger


class AllureLibrary:
    """
    AllureLibrary secondary library
    
    AllureOutputPath allows for the setting of a specific path where the 
    files should be saved.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.1'

    def __init__(self, AllureOutputPath=None):


        # In case Listener is added via Command Line, then Library should not
        # another one. That would result in duplicate log files for Suite.
        # Since RED runs this class to get the documentation, the Try/Except is needed.
        try:
            AllureListenerActive = BuiltIn().get_variable_value('${AllureListenerActive}', False)
            if AllureListenerActive is False:
                self.ROBOT_LIBRARY_LISTENER = AllureListener(AllureOutputPath, 'Library')
        except:
            pass
        
    def set_output_dir(self, output_dir):
        """
        This is the output method short line.
        
        This is the output method long line.
        """
        print 'set output dir'