import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

import myfilemanager as mfm
import mystyle as ms
from TricubicInterpolation import tricubic_interpolation as ti

ob = mfm.myloadmat_to_obj('pinch_cut.mat')


i_slice = 250
z_obs = ob.zg[i_slice]

# Interpolation
tinterp = ti.Tricubic_Interpolation(A=ob.phi.transpose(1,2,0), x0=ob.xg[0], y0=ob.yg[0], z0=ob.zg[0],
        dx=ob.xg[1]-ob.xg[0], dy=ob.yg[1]-ob.yg[0], dz=ob.zg[1]-ob.zg[0])

x_tint = np.linspace(-5e-4, 5e-4, 1000)
y_tint = 0.*x_tint
z_tint = 0.*x_tint + z_obs

phi_tint = 0.*x_tint
Ex_tint = 0.*x_tint

for ii, (xx, yy, zz) in enumerate(zip(x_tint, y_tint, z_tint)):
    phi_tint[ii] = tinterp.val(xx, yy, zz)
    Ex_tint[ii] = -tinterp.ddx(xx, yy, zz)


# Plotting
plt.close('all')
ms.mystyle_arial()
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
fig3.set_facecolor('w')
ax31 = fig3.add_subplot(3,1,1, sharex=ax1)
ax32 = fig3.add_subplot(3,1,2, sharex=ax31)
ax33 = fig3.add_subplot(3,1,3, sharex=ax31)

ax31.plot(ob.xg, ob.rho[i_slice, :, j_obs], '.-')
ax32.plot(ob.xg, ob.phi[i_slice, :, j_obs],'.-')
ax33.plot(ob.xg, ob.Ex[i_slice, :, j_obs], '.-')

ax32.plot(x_tint, phi_tint,'r-')
ax33.plot(x_tint, Ex_tint, 'r-')


plt.show()
