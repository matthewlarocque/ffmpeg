libavutil_x86_sources = files(
  'cpu.c',
  'fixed_dsp_init.c',
  'float_dsp_init.c',
  'imgutils_init.c',
  'lls_init.c',
)

libavutil_x86_optional_sources = {
  'pixelutils' : files('pixelutils_init.c'),
  'x86asm' : files('tx_float_init.c'),
}

libavutil_x86_x86asm_sources = files(
  'cpuid.asm',
  'fixed_dsp.asm',
  'float_dsp.asm',
  'imgutils.asm',
  'lls.asm',
  'tx_float.asm',
)

libavutil_x86_x86asm_optional_sources = {
  'mmx_external' : files('emms.asm'), # MANUAL
  'pixelutils' : files('pixelutils.asm'),
}

