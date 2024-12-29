from struct import *
import sys, os

def dump(image_file_path):
    with open(image_file_path, 'rb') as f:
        inbuf = f.read()
    outbuf = inbuf[40:]
    with open('out.img', 'wb') as outf:
        outf.write(outbuf)

def is_fdi(image_file_path):
    """
    typedef struct {
        BYTE   offset[8];
        BYTE   fddtype[4];
        BYTE   headersize[4];
        BYTE   fddsize[4];
        BYTE   sectorsize[4];
        BYTE   sectors[4];
        BYTE   surfaces[4];
        BYTE   cylinders[4];
    } HDXHDR;
    intel dwords - little endian
    """
    size = os.path.getsize(image_file_path)
    with open(image_file_path, 'rb') as f:
        raw_header = f.read(8)
        offset = unpack('<1Q', raw_header)
        raw_header = f.read(32)
        headersize, fddsize, sectorsize, sectors, surfaces, cylinders = unpack('<8L', raw_header)
        print('offset = %d' % offset)
        print('header size = %d' % headersize)
        print('fdd size = %d' % fddsize)
        print('sector size = %d' % sectorsize)
        print('sectors = %d' % sectors)
        print('surfaces = %d' % surfaces)
        print('cylinders = %d' % cylinders)

        if cylinders > 100 or cylinders < 10:
            return (False, 'Ridiculous cylinder count: %d' % cylinders)
        if size > 1265664:
            return (False, 'Too big to be an FDI: %d' % size)

        # look for suspicious pad bytes

        return (True, '')

if __name__ == '__main__':
    # work as a command-line utility to analyze multiple maybe-FDI images
    if len(sys.argv) < 2:
        print('Usage: %s [disk images]' % sys.argv[0])
    for arg in sys.argv[1:]:
        # (result, why) = is_fdi(arg)
        # if not result:
        #     print('%s: no (%s)' % (arg, why))
        # else:
        #     print('%s: yes' % arg)
        dump(arg)