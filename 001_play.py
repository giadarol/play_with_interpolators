import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

import myfilemanager as mfm

try:
    del ob
except:
    print('Did not manage to delete...')

ob = mfm.myloadmat_to_obj('pinch_pic_data_mean2.mat')

i_zero = np.argmin(np.abs(ob.xg))
j_zero = np.argmin(np.abs(ob.yg))

N_keep_h = 100
N_keep_v = 90

dict_new_file = {}
dict_new_file['Ex' ] = ob.Ex[:, i_zero-N_keep_h:i_zero+N_keep_h+1, j_zero-N_keep_v:j_zero+N_keep_v+1] 
dict_new_file['Ey' ] = ob.Ey[:, i_zero-N_keep_h:i_zero+N_keep_h+1, j_zero-N_keep_v:j_zero+N_keep_v+1] 
dict_new_file['phi'] = ob.phi[:, i_zero-N_keep_h:i_zero+N_keep_h+1, j_zero-N_keep_v:j_zero+N_keep_v+1] 
dict_new_file['rho'] = ob.rho[:, i_zero-N_keep_h:i_zero+N_keep_h+1, j_zero-N_keep_v:j_zero+N_keep_v+1] 
dict_new_file['xg' ] = ob.xg[i_zero-N_keep_h:i_zero+N_keep_h+1] 
dict_new_file['yg' ] = ob.yg[j_zero-N_keep_v:j_zero+N_keep_v+1]
dict_new_file['zg' ] = ob.zg


i_slice = 250


plt.close('all')
ax1 =  None
# fig1 = plt.figure(1)
# ax1 = fig1.add_subplot(1,1,1)
# ax1.pcolormesh(ob.xg, ob.yg, ob.rho[i_slice, :, :].T)
# 
# fig2 = plt.figure(2)
# ax2 = fig2.add_subplot(1,1,1, sharex=ax1)
# ax2.pcolormesh(ob.xg, ob.yg, ob.Ex[i_slice, :, :].T)

y_obs = 0.
j_obs = np.argmin(np.abs(ob.yg - y_obs))

fig3 = plt.figure(3)
ax31 = fig3.add_subplot(3,1,1, sharex=ax1)
ax32 = fig3.add_subplot(3,1,2, sharex=ax31)
ax33 = fig3.add_subplot(3,1,3, sharex=ax31)

ax31.plot(ob.xg, ob.rho[i_slice, :, j_zero])
ax32.plot(ob.xg, ob.phi[i_slice, :, j_zero])
ax33.plot(ob.xg, ob.Ex[i_slice, :, j_zero])


plt.show()
