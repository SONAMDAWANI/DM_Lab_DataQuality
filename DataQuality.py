#!/usr/bin/env python
# coding: utf-8

# In[90]:


from datetime import datetime
from constants.CONSTANTS import *
from aia_image_api import imageparam_getter as ipg
import numpy as np
from datetime import timedelta 


# In[91]:


dt_start = datetime.strptime('2012-04-12T16:10:00', '%Y-%m-%dT%H:%M:%S')
dt_stop = dt_start+timedelta(days=0.2)  

dt=dt_start
aia_wave = AIA_WAVE.AIA_171
image_size = IMAGE_SIZE.P2000
param_id = '1'

thereshold=5
lastcorrectmat88=np.zeros((8, 8))

while dt<dt_stop:
    
    xml = ipg.get_aia_imageparam_xml(dt, aia_wave)
    res = ipg.convert_param_xml_to_ndarray(xml)
    entropyValues=res[:,:,(int(param_id)-1):int(param_id)].reshape(64, 64)

    mat88=np.zeros((8, 8))
    for n in range(8):
        for m in range(8):
            aggvalue=0
            for i in range(8*n,(8*n)+8):
                for j in range(8*m,(8*m)+8):
                    aggvalue=aggvalue+entropyValues[i,j]
            cellvalue=aggvalue/64
            mat88[n,m]=cellvalue
    
    if np.all(lastcorrectmat88==np.zeros((8, 8))):
        lastcorrectmat88=mat88
    diffmat_from_last_correct=np.absolute(np.subtract(lastcorrectmat88, mat88))
    diffsum=np.sum(diffmat_from_last_correct)
    
    if diffsum>thereshold:
        print(dt,end=', ')
        print(diffsum)
    else:
        lastcorrectmat88=mat88
    
    dt=dt+timedelta(minutes=6)  


# In[81]:


dt_start = datetime.strptime('2012-04-12T16:10:00', '%Y-%m-%dT%H:%M:%S')
dt_stop = dt_start+timedelta(days=0.2)  

dt=dt_start
aia_wave = AIA_WAVE.AIA_171
image_size = IMAGE_SIZE.P2000
param_id = '1'

while dt<dt_stop:
    
    heatmap = ipg.get_aia_imageparam_jpeg(dt, aia_wave, image_size, param_id)
    heatmap.save('testimg/'+str(dt)+'.png') 
    
    dt=dt+timedelta(minutes=6)  


# In[ ]:




