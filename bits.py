#
# python ints are int64
#
# these functions implement shift and rotate for differenet widths
#

def mask(n):
   """Return a bitmask of length n (suitable for masking against an
      int to coerce the size to a given length)
   """
   if n >= 0:
       return 2**n - 1
   else:
       return 0

def unsigned(n, width=32):
   return n % mask(width)
 
def rol(n, rotate=1, width=32):
    """Return a given number of bitwise left rotations of an integer n,
       for a given bit field width.
    """
    rotate %= width
    if rotate < 1:
        return n
    n &= mask(width) ## Should it be an error to truncate here?
    return ((n << rotate) & mask(width)) | (n >> (width - rotate))
 
def ror(n, rotate=1, width=32):
    """Return a given number of bitwise right rotations of an integer n,
       for a given bit field width.
    """
    rotate %= width
    if rotate < 1:
        return n
    n &= mask(width)
    return (n >> rotate) | ((n << (width - rotate)) & mask(width))

def lsl(n, shift, width=32):
    shift %= width
    return (n << shift) & mask(32)

def lsr(n, shift, width=32):
    return unsigned(n, width) >> shift

def asr(n, shift, width=32):
    shift %= width
    return (n >> shift) & mask(32)

#
# generalize this to work for 64 bits
def clz(x):
    if x == 0:
        return 64

    n = 0
    if x <= 0x00000000FFFFFFFF:
        n = n + 32
        x = x << 32
    if x <= 0x0000FFFF:
        n = n + 16
        x = x << 16
    if x <= 0x00FFFFFF:
        n = n + 8
        x = x << 8
    if x <= 0x0FFFFFFF:
        n = n + 4
        x = x << 4
    if x <= 0x3FFFFFFF:
        n = n + 2
        x = x << 2
    if x <= 0x7FFFFFFF:
        n = n + 1
    return n

def checku(u, len):
    max = 1 << len

    assert u < max

    return u & (max - 1)

def checks(i, len):
    min = -(1 << (len-1))
    max = 1 << len

    assert i >= min
    assert i <  max

    return i & (max - 1)



