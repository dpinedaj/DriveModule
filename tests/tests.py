import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.myDrive import MyDrive

    
drive = MyDrive()
drive.ls('1fOLDnCggE-9NMRi2GjKX-RlWcx5QHN97',verbose=True)
    
