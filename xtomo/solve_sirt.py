#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import numpy as xp

# mask out outer tomogram and sinogram
import numpy as np

def masktomo(num_rays,xp,width=.65):
    
    xx=xp.array([range(-num_rays//2, num_rays//2)])
    msk_sino=(xp.abs(xx)<(num_rays//2*width)).astype('float32')
    
    msk_sino.shape=(1,1,num_rays)
    
    xx=xx**2
    rr2=xx+xx.T
    msk_tomo=rr2<(num_rays//2*width*1.02)**2
    msk_tomo.shape=(1,num_rays,num_rays)
    return msk_tomo, msk_sino

def sirtMcalc(radon,radont,shape,xp):
    # compute the tomogram and sinogram of all ones
    # if R (radon) is a matrix sum_rows R = R*1= radon(1) 
    #                  sum_cols R = RT*1 = radont(1) 
    # we need to clip outside a mask of interest
    
    num_rays=shape[2]
    num_angles=shape[1]
    
    msk_tomo,msk_sino=masktomo(num_rays,xp,width=.65)
    
    eps=xp.finfo(xp.float32).eps
    #t1=tomo0*0+1.
    S1=radon(xp.ones((1,num_rays,num_rays),dtype='float32'))
    S1=1./xp.clip(S1,eps*10,None)*msk_sino
    T1=radont(xp.ones((1,num_angles,1),dtype='float32')*msk_sino)
    T1=1./xp.clip(T1,eps,None)*msk_tomo
    return T1,S1


def sirtBB(radon, radont, sino_data, xp, max_iter=30, alpha=1, verbose=0, useRC=False,BBstep=True):
      
    nrm0 = xp.linalg.norm(sino_data)
    if nrm0 == 0:
        nrm0=1

        num_rays=sino_data.shape[2]
        num_slices=sino_data.shape[0]
        
        tomo=xp.zeros((num_slices,num_rays,num_rays),dtype=(sino_data).dtype)
        return tomo,0.
        
    if useRC:
        C,R=sirtMcalc(radon,radont,(sino_data).shape,xp)
        iradon= lambda x: C*radont(R*x)
    else: 
        iradon=radont

    tomo = iradon(sino_data)
    
    alphai=0
    #print("verbose",verbose>0)

    for i in range(max_iter):
        

        
        residual =  radon(tomo) - sino_data 
        rnrm=xp.linalg.norm(residual)/nrm0
       
        grad = iradon(residual)

        # BB step  (alternating)  
        #print(i)
        if BBstep and i>0:

            #print(i)#np.mod(i,2)<1)
            if np.mod(i,2)<1:
                alpha=xp.linalg.norm(tomo-tomo_old)**2/xp.inner((tomo-tomo_old).ravel(),(grad-grad_old).ravel())
                alphai=1
            else:
                alpha=xp.inner((tomo-tomo_old).ravel(),(grad-grad_old).ravel())/xp.linalg.norm(grad-grad_old)**2
                alphai=2
#
        tomo_old=tomo+0
        
        
        tomo -=  grad*alpha
        
        grad_old=grad+0
        
        if verbose >0:
            title = "SIRT-BB iter=%d, alpha=%g, alphai=%g rnrm=%g" %(i, alpha, alphai, rnrm)
            print(title )
            #print(np.mod(i,2)<1)
            if verbose >1:
                plt.imshow(t2i(tomo))
                plt.title(title)
                plt.show()
    return tomo,rnrm

#
#def sirt(radon, radont, sino_data, max_iter=30, factor=1, verbose=0):
#
#    xp=np
#
#    
#    nrm0 = np.linalg.norm(sino_data)
#
#    # prepare the left and right matrix 
#    
#    T1,S1=sirtMcalc(radon,radont,xp.shape(sino_data),xp)
#
#    radont1= lambda x: T1*radont(S1*x)
#
#
#    
#    tomo = radont1(sino_data)
#    
#
#
#    for i in range(max_iter):
#        
#
#        sino_sim = radon(tomo)
#        
#        residual = sino_data - sino_sim
#        rnrm=np.linalg.norm(residual)/nrm0
#        
#        if verbose >0:
#            title = "SIRT iter=%d, rnrm=%g" %(i, rnrm)
#            print(title )
#            if verbose >1:
#                plt.imshow(t2i(tomo))
#                plt.title(title)
#                plt.show()
#
#                
#        step = radont1(residual)
#
#        step *= factor
#        
#        tomo +=  step
#        
#        
#
#    return tomo,rnrm