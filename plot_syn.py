import elastic
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# New C matrix
tensor_string = """ 
     29.76    11.55     9.76       0    -0.69      0  
     11.55    34.71    11.45       0     3.96      0  
      9.76    11.45    30.45       0    -2.34      0  
         0        0        0    14.36      0    -1.88 
     -0.69     3.96    -2.34       0    14.24      0  
         0        0        0    -1.88      0    20.19 
"""

# Initialize material with new elastic tensor
material1 = elastic.Elastic(tensor_string)

# Young's Modulus and Linear Compressibility
print("Young's Modulus:", material1.Young_2(np.pi / 2, 0))
print("Linear Compressibility:", material1.LC_2(np.pi / 2, np.pi / 4))

young_110 = material1.Young_2(np.pi / 2, np.pi / 4)
print("Young's Modulus along [110]:", young_110)
#%%
# Polar plot of Young's modulus in the (xy), (yz), and (zx) planes
phi = np.linspace(0, 2 * np.pi, 100)
f = np.vectorize(material1.Young_2)

r_xy = f(np.pi / 2, phi)
r_yz = f(phi - np.pi/2, np.pi/2)
r_zx = f(phi, 0)


fig, axes = plt.subplots(1, 3, subplot_kw={'projection': 'polar'}, figsize=(15, 5))

# Font settings
title_font = {'fontsize': 14, 'fontweight': 'bold', 'family': 'sans-serif'}
label_font = {'fontsize': 3, 'fontweight': 'bold'}  # Fontsize 3 might be too small

axes[0].plot(phi, r_xy, color='b', linewidth=3)
axes[0].grid(True)
axes[0].set_title("XY Plane", fontdict=title_font)

axes[1].plot(phi, r_yz, color='b', linewidth=3)
axes[1].grid(True)
axes[1].set_title("YZ Plane", fontdict=title_font)
axes[2].plot(phi, r_zx, color='b', linewidth=3)
axes[2].grid(True)
axes[2].set_title("ZX Plane", fontdict=title_font)

plt.tight_layout()
# plt.show()

# axes[0].plot(phi, r_xy, color='b', linewidth=3)
# axes[0].grid(True)
# axes[0].set_title("XY Plane", fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontname': 'sans-serif'})

# axes[1].plot(phi, r_yz, color='b', linewidth=3)
# axes[1].grid(True)
# axes[1].set_title("YZ Plane", fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontname': 'sans-serif'})

# axes[2].plot(phi, r_zx, color='b', linewidth=3)
# axes[2].grid(True)
# axes[2].set_title("ZX Plane", fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontname': 'sans-serif'})


plt.savefig("BH_SYn_ElasticOrtho_Youngs_Modulus_Polar_All.png", dpi=600)
#%%
# # 3D Polar Plot
from matplotlib import cm, colors
from scipy.interpolate import interp2d
def spherical_grid(npoints=500):
    theta = np.linspace(0, np.pi, npoints)
    phi = np.linspace(0, 2 * np.pi, npoints)
    return np.meshgrid(theta, phi)

def spherical_coord(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

theta, phi = spherical_grid()
r = f(theta, phi)  # Ensure 'f' is defined and vectorized

# Interpolate `r` for even smoother transitions
# theta_fine = np.linspace(0, np.pi, 1000)
# phi_fine = np.linspace(0, 2 * np.pi, 1000)
# interp_func = interp2d(theta[:,0], phi[0,:], r, kind='cubic')
# r_fine = interp_func(theta_fine, phi_fine)
# theta_fine, phi_fine = np.meshgrid(theta_fine, phi_fine)

x, y, z = spherical_coord(r, theta, phi)
# x, y, z = spherical_coord(r_fine, theta_fine, phi_fine)
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection="3d")

# Smooth 3D Surface Plot
# surf = ax.plot_surface(x, y, z, cmap='gist_rainbow', edgecolor='none',
#                         linewidth=0, antialiased=True, shade=True, alpha=0.9)

# Normalize `r` values for colormap scaling
norm = colors.Normalize(vmin=20, vmax=35)
cmap = cm.turbo  # Use a vibrant colormap

# Surface plot with color mapping based on `r` values
surf = ax.plot_surface(x, y, z, facecolors=cmap(norm(r)), edgecolor='none', 
                        linewidth=0, antialiased=True, shade=True)

# Add colorbar
mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])
cbar = plt.colorbar(mappable, shrink=0.6, aspect=10)
cbar.set_ticks(np.arange(20, 36, 5))
cbar.set_label("Young's Modulus (GPa)", fontsize=14, fontweight='bold')


ax.grid(False)
# Bold Axis Labels
ax.set_xlabel("X Axis", fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel("Y Axis", fontsize=14, fontweight='bold', labelpad=10)
ax.set_zlabel("Z Axis", fontsize=14, fontweight='bold', labelpad=10)

# Move ticks to left
ax.xaxis.set_tick_params(direction='in', width=3, labelsize=12)
ax.yaxis.set_tick_params(direction='in', width=3, labelsize=12)
ax.zaxis.set_tick_params(direction='in', width=3, labelsize=12)

ax.tick_params(axis='both', which='major', labelsize=12, width=2, length=6)
ax.tick_params(axis='z', which='major', labelsize=12, width=2, length=6)

# Thicker Grid for better visibility
# ax.grid(True, linewidth=1.5)

# Adjust view for better visualization
ax.view_init(elev=35, azim=135)

# Save high-resolution images
plt.savefig("BH_SYn_Youngs_Modulus_Polar_3D_color_bar.png", dpi=600, bbox_inches='tight', transparent=True)
# plt.savefig("BH_SYn.png", dpi=600, bbox_inches='tight', transparent=True)

plt.show()


#%%

# def spherical_grid(npoints=200):
#     theta = np.linspace(0, np.pi, npoints)
#     phi = np.linspace(0, 2 * np.pi, npoints)
#     return np.meshgrid(theta, phi)

# def spherical_coord(r, theta, phi):
#     x = r * np.sin(theta) * np.cos(phi)
#     y = r * np.sin(theta) * np.sin(phi)
#     z = r * np.cos(theta)
#     return x, y, z

# theta, phi = spherical_grid()
# r = f(theta, phi)
# x, y, z = spherical_coord(r, theta, phi)

# fig = plt.figure(figsize=(9, 9))
# ax = plt.axes(projection="3d")
# ax.plot_surface(x, y, z, cmap='rainbow',edgecolor='none',linewidth=0, 
#                         antialiased=True, shade=True)

# ax.grid(False)
# # ax.set_xticks([])
# # ax.set_yticks([])
# # ax.set_zticks([])
# # ax.set_frame_on(False)  # Removes the box around the plot

# # Adjust view for better visualization
# ax.view_init(elev=30, azim=45)

# plt.savefig("BH_SYn_Youngs_Modulus_Polar_3D.png", dpi=600)
# plt.savefig("BH_SYn.png", dpi=600)
#%%
# Voigt, Reuss, and Hill Averages
avg_Voigt, avg_Reuss, avg_Hill = material1.averages()
print("Voigt:", avg_Voigt)
print("Reuss:", avg_Reuss)
print("Hill:", avg_Hill)

def averages_dataframe(mat):
    return pd.DataFrame(mat.averages(),
                        columns=["bulk (GPa)", "Young (GPa)", "shear (GPa)", "Poisson"],
                        index=["Voigt", "Reuss", "Hill"])

print(averages_dataframe(material1))

def elasticEigenvalues(mat):
    return np.sort(np.linalg.eig(mat.CVoigt)[0])

print(elasticEigenvalues(material1))
if np.all(elasticEigenvalues(material1) > 0):
    print('The material is mechanically stable')

#%%
# Poisson's Ratio in XY Plane
# phi_xy = np.linspace(0, 2 * np.pi, 200)
# min_poisson_xy, max_poisson_xy = [], []
# for p in phi_xy:
#     res = material1.Poisson3D(np.pi/2, p)  # Returns (min, _, max, ...)
#     min_poisson_xy.append(res[0])
#     max_poisson_xy.append(res[2])

# fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
# ax.plot(phi_xy, min_poisson_xy, color='b', label='Min Poisson Ratio')
# ax.plot(phi_xy, max_poisson_xy, color='r', label='Max Poisson Ratio')
# ax.set_title("Poisson's Ratio in XY Plane (θ = π/2)", pad=20)
# ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.15))
# plt.savefig("BH_SYn_ElasticOrtho_Poisson_XY.png", dpi=600)
# plt.show()

#%%


phi_xy = np.linspace(0, 2 * np.pi, 100)
f = np.vectorize(lambda x: material1.shear2D([np.pi / 2, x]))
r = f(phi_xy)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(phi_xy, r[0], color='b')
ax.plot(phi_xy, r[1], color='r')
ax.grid(True)

plt.show()

#%%


# Assuming `material1.shear2D` is defined similarly
phi = np.linspace(0, 2 * np.pi, 100)

# XY Plane (already implemented)
f_xy = np.vectorize(lambda x: material1.shear2D([np.pi / 2, x]))
r_xy = f_xy(phi)

# YZ Plane
f_yz = np.vectorize(lambda x: material1.shear2D([x-np.pi/2, np.pi/2]))
r_yz = f_yz(phi)


# ZX Plane
f_zx = np.vectorize(lambda x: material1.shear2D([x, 0]))
r_zx = f_zx(phi)


fig, axs = plt.subplots(1, 3, subplot_kw={'projection': 'polar'}, figsize=(15, 5))

title_font = {'fontsize': 14, 'fontweight': 'bold', 'family': 'sans-serif'}
label_font = {'fontsize': 3, 'fontweight': 'bold'}  # Fontsize 3 might be too small

axs[0].plot(phi, r_xy[0], color='b', label='Min Shear')
axs[0].plot(phi, r_xy[1], color='r', label='Max Shear')
axs[0].set_title("XY Plane",fontdict=title_font)
axs[0].legend()



axs[1].plot(phi, r_yz[0], color='b')
axs[1].plot(phi, r_yz[1], color='r')
axs[1].set_title("YZ Plane",fontdict=title_font)



axs[2].plot(phi, r_zx[0], color='b')
axs[2].plot(phi, r_zx[1], color='r')
axs[2].set_title("ZX Plane",fontdict=title_font)

for ax in axs:
    ax.grid(True)

# plt.show()

plt.savefig("BH_SYn_ElasticOrtho_Shear_Modulus_Polar_All.png", dpi=600)
