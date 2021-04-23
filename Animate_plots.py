import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
import numpy as np 
from glob import glob
from astropy.io import fits
"""
	The basic idea of this script is simple: animation module contains a function called
	ArtistAnimation, which has the following syntax: 
		anim = animation.ArtistAnimation(fig, im, interval=20, blit=True) 
	
	fig: figure over which the plot is done. This you already must have.
	im: Sequence of axis over time. You must have an `ax` for a single plot. 
		This ax must be updated every time, and `im` must be a list of such axis. 
	interval: the time in milliseconds between two frames.
	blit: Apparently makes the plots better, if `True`.

	This script will show you how to save animation for time series of one wavelength. 
	If you want to save time series of all the plots together as subplots, make sure:
		1. The axes are correctly passed.
		2. The cadence of data is accounted for.

	NOTE: You will need ffmpeg codec for doing this.
"""
def Generate_from_center(centreval,stepsize,n_elements):
	'''
	    This function give you the min and max value in arcsec of the FOV.
	'''
	interval=int((n_elements+1)/2)*stepsize
	minval=centreval-interval
	maxval=centreval+interval
	return [minval,maxval]
def PlotData(image_data,image_header,ax,fig,**kwargs):
	'''
	    Hold on, this looks complicated! What does it do?
	    This function takes in something called a subplot axis, and plots an image in that axis alone.
	    For example, if there are 4 plots arranged as a grid in a given figure, it is called a subplot. This function
	'''
	x_=Generate_from_center(image_header['XCEN'],image_header['CDELT1'],image_data.shape[0])
	y_=Generate_from_center(image_header['YCEN'],image_header['CDELT2'],image_data.shape[1])
	im = ax.imshow(image_data,origin='lower',extent=x_+y_,**kwargs)
	ax.set_title("%s %d $\AA$"%(image_header['T_OBS'],image_header['WAVELNTH']),fontsize=20)
	ax.set_xlabel('Solar Longitude (Solar-X) in %s'%(image_header['CUNIT1']),fontsize=20)
	ax.set_ylabel('Solar Latitude (Solar-Y) in %s'%(image_header['CUNIT2']),fontsize=20)
	try:
	    fig.colorbar(im,ax=ax,label='Pixel intensity (%s)'%(image_header['PIXLUNIT']),fraction=0.04).ax.tick_params(labelsize=20)
	except: 
	    fig.colorbar(im,ax=ax,label='Pixel intensity (%s)'%(image_header['BUNIT']),fraction=0.04).ax.tick_params(labelsize=20)
	return ax 

image_path=sorted(glob('aia193/*')) #This line loads the paths of all images in `aia193/`

fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(15,15))
im=[] #This list contains all the axes.
for path in image_path:
	image=fits.open(path)[0]
	im_data=image.data
	im_header=image.header 
	tmp_ax=PlotData(im_data,im_header,ax,fig,cmap='hot')
	im.append(tmp_ax)

anim = animation.ArtistAnimation(fig, im, interval=20, blit=True) 

# save the animation as mp4 video file 
anim.save('AIA193.mp4') 
