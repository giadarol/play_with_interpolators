import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

import myfilemanager as mfm
import mystyle as ms
from TricubicInterpolation import tricubic_interpolation as ti

import PyPIC.PyPIC_Scatter_Gather as PyPICSC
import PyPIC.geom_impact_poly as poly

ob = mfm.myloadmat_to_obj('pinch_cut.mat')

interp2d = True 


i_slice = 250
z_obs = ob.zg[i_slice]

if interp2d:
    for kk, zz in enumerate(ob.zg):
        ob.rho[kk, :, :] = ob.rho[i_slice, :, :]
        ob.phi[kk, :, :] = ob.phi[i_slice, :, :]
        ob.Ex[kk, :, :] = ob.Ex[i_slice, :, :]
        ob.Ey[kk, :, :] = ob.Ey[i_slice, :, :]


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

# 2D PIC

assert((ob.xg[1] - ob.xg[0]) == (ob.yg[1] - ob.yg[0]))
na = np.array
chamb = poly.polyg_cham_geom_object({'Vx':na([ob.xg[-1], ob.xg[0], ob.xg[0], ob.xg[-1]]),
                                       'Vy':na([ob.yg[-1], ob.yg[-1], ob.yg[0],ob.yg[0]]),
                                       'x_sem_ellip_insc':1e-3,
                                       'y_sem_ellip_insc':1e-3})

pic = PyPICSC.PyPIC_Scatter_Gather(xg=ob.xg, yg=ob.yg)
pic.phi = ob.phi[i_slice, :, :]
pic.efx = ob.Ex[i_slice, :, :]
pic.efy = ob.Ey[i_slice, :, :]
pic.rho = ob.rho[i_slice, :, :]

Ex_picint, _ = pic.gather(x_tint, y_tint)

####
#ob_rho_interp = scipy.interpolate.interp2d(ob.xg, ob.yg, ob.rho.T)


#####


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
ax33.plot(ob.xg, ob.Ex[i_slice, :, j_obs], '.')

ax32.plot(x_tint, phi_tint,'r-')

ax33.plot(x_tint, Ex_tint, 'r-')
ax33.plot(x_tint, Ex_picint, 'g--')


plt.show()
