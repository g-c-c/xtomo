#from fubini import generate_Shepp_Logan as generate_Shepp_Logan
#from radon import radon_setup as radon_setup
import tomopy
import numpy as np

xp=np

def generate_Shepp_Logan(cube_shape):

   return tomopy.misc.phantom.shepp3d(size=cube_shape, dtype='float32')


def setup_tomo (num_slices, num_angles, num_rays, k_r=1, kernel_type = 'gaussian',width=.5):

    #num_rays=num_rays//2
    num_rays_obj=np.int(np.floor(num_rays*width/2)*2)
    true_obj_shape = (num_slices, num_rays_obj, num_rays_obj)
    true_obj = generate_Shepp_Logan(true_obj_shape)
    
    
    pad_1D        = (num_rays-num_rays_obj)//2
    padding_array = ((0, 0), (pad_1D, pad_1D), (pad_1D, pad_1D))
    #num_rays      = num_rays + pad_1D*2
    
    #print("obj shape before padding", true_obj.shape, "num_angles", num_angles)
    
   #true_obj = xp.lib.pad(true_obj, padding_array, 'constant', constant_values = 0)
    true_obj = xp.pad(true_obj, padding_array, 'constant', constant_values = 0)
    
    theta    = xp.arange(0., 180., 180. / num_angles,dtype='float32')*xp.pi/180.
    
    #theta    = xp.linspace(0, 180., num= num_angles+1)*xp.pi/180.
    #print("theta shape=",theta.shape,"num_angles=",num_angles)
#    eps=np.finfo(xp.float32).eps

#    theta+=eps
    
    kernel_type     = "gaussian"

    
    #radon,iradon,radont = radon_setup(num_rays, theta, xp=xp, kernel_type = 'gaussian', k_r =1)
    
    ############################
    # generate data
    #data = radon(true_obj)
    #return radon, iradon, radont, true_obj, data, theta
    return true_obj, theta
