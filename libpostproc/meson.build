kwargs = {'prefix': '#include "libpostproc/version.h"'} + get_version_define_kwargs

libpostproc_majorver = cc.get_define('LIBPOSTPROC_VERSION_MAJOR', kwargs: kwargs)
minorver = cc.get_define('LIBPOSTPROC_VERSION_MINOR', kwargs: kwargs)
microver = cc.get_define('LIBPOSTPROC_VERSION_MICRO', kwargs: kwargs)

libpostproc_version = f'@libpostproc_majorver@.@minorver@.@microver@'

#### --- GENERATED --- ####

libpostproc_sources = files(
  'postprocess.c',
  'version.c',
)

libpostproc_headers = files(
  'postprocess.h',
  'version.h',
  'version_major.h',
)

#### --- END GENERATED --- ####

# Version file
ver_conf = configuration_data()
ver_conf.set('majorver', libpostproc_majorver)
ver_conf.set('minorver', minorver)
ver_conf.set('microver', microver)

install_headers(libpostproc_headers, subdir: 'libpostproc')

libpostproc_ver = configure_file(
  input: 'libpostproc.v.in',
  output: 'libpostproc.ver',
  configuration: ver_conf,
)
