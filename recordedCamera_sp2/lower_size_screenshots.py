import glob
import os
from PIL import Image


sequenceDIR = '/Users/jona/sofa/build/screenshots/'
resizeFactor = 0.5
resizedSize = (int(resizeFactor*1530),int(resizeFactor*1200))
list_of_files = glob.glob(sequenceDIR+'*') # * means all if need specific format then *.csv
for f in list_of_files:
    foo = Image.open(f)
    foo.save(f,optimize=True,quality=90)
#    foo = foo.resize(resizedSize, Image.ANTIALIAS)
#    foo.save(f)

