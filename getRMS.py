"""
functions for calculating statistical properties of LOFAR images
"""
import numpy
import sys
import astropy.io.fits as pyfits


def rms(data):
    """Returns the RMS of the data about the median.
    Args:
        data: a numpy array
    """
    data -= numpy.median(data)
    return numpy.sqrt(numpy.power(data, 2).sum()/len(data))


def clip(data, sigma=3):
    """Remove all values above a threshold from the array.
    Uses iterative clipping at sigma value until nothing more is getting clipped.
    Args:
        data: a numpy array
    """
    raveled = data.ravel()
    median = numpy.median(raveled)
    std = numpy.std(raveled)
    newdata = raveled[numpy.abs(raveled-median) <= sigma*std]
    if len(newdata) and len(newdata) != len(raveled):
        return clip(newdata, sigma)
    else:
        return newdata


def subregion(data, f=4):
    """Returns the inner region of a image, according to f.
    Resulting area is 4/(f*f) of the original.
    Args:
        data: a numpy array
    """
    x, y = data.shape
    f = int(f)
    return data[(int(x/2) - int(x/f)):(int(x/2) + int(x/f)), (int(y/2) - int(y/f)):(int(y/2) + int(y/f))]


def rms_with_clipped_subregion(data, sigma=3, f=4):
    """ returns the rms value of a iterative sigma clipped subsection of an image
    Args:
        data: A numpy array
        sigma: sigma value used for clipping
        f: determines size of subsection, result will be 1/fth of the image size
    """
    return rms(clip(subregion(data, f), sigma))

def read_data(hdu, filename, plane):
    """
    Read and store data from our FITS file.
    NOTE: PyFITS reads the data into an array indexed as [y][x]. We
    take the transpose to make this more intuitively reasonable and
    consistent with (eg) ds9 display of the FitsFile. Transpose back
    before viewing the array with RO.DS9, saving to a FITS file,
    etc.
    """
    data = numpy.float64(hdu.data.squeeze())
    if plane is not None and len(data.shape) > 2:
        data = data[plane].squeeze()
    n_dim = len(data.shape)
    if n_dim != 2:
        #logger.warn("Loaded datacube with %s dimensions, assuming Stokes I and taking plane 0" % n_dim)
        data = data[0, :, :]
    data = data.transpose()
    return data
