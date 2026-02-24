kwargs = {'prefix': '#include "libswscale/version.h"'} + get_version_define_kwargs

libswscale_majorver = cc.get_define('LIBSWSCALE_VERSION_MAJOR', kwargs: kwargs)
minorver = cc.get_define('LIBSWSCALE_VERSION_MINOR', kwargs: kwargs)
microver = cc.get_define('LIBSWSCALE_VERSION_MICRO', kwargs: kwargs)

libswscale_version = f'@libswscale_majorver@.@minorver@.@microver@'

#### --- GENERATED --- ####

libswscale_sources = files(
  'alphablend.c',
  'hscale.c',
  'hscale_fast_bilinear.c',
  'gamma.c',
  'half2float.c',
  'input.c',
  'options.c',
  'output.c',
  'rgb2rgb.c',
  'slice.c',
  'swscale.c',
  'swscale_unscaled.c',
  'utils.c',
  'version.c',
  'yuv2rgb.c',
  'vscale.c',
)

libswscale_headers = files(
  'swscale.h',
  'version.h',
  'version_major.h',
)

libswscale_shlib_sources = files(
  'log2_tab.c',
)

libswscale_tests = [
  ['colorspace', files('tests/colorspace.c')],
  ['floatimg_cmp', files('tests/floatimg_cmp.c')],
  ['pixdesc_query', files('tests/pixdesc_query.c')],
  # MANUAL ['swscale', files('tests/swscale.c')],
]

#### --- END GENERATED --- ####

# Version file
ver_conf = configuration_data()
ver_conf.set('majorver', libswscale_majorver)
ver_conf.set('minorver', minorver)
ver_conf.set('microver', microver)

install_headers(libswscale_headers, subdir: 'libswscale')

libswscale_ver = configure_file(
  input: 'libswscale.v.in',
  output: 'libswscale.ver',
  configuration: ver_conf,
)

subdir('aarch64')
subdir('arm')
subdir('x86')
