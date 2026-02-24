libswscale_x86_sources = files(
  'rgb2rgb.c',
  'swscale.c',
  'yuv2rgb.c',
)

libswscale_x86_optional_sources = {
  'xmm_clobber_test' : files('w64xmmtest.c'),
}

libswscale_x86_x86asm_sources = files(
  'input.asm',
  'output.asm',
  'scale.asm',
  'scale_avx2.asm',
  'range_convert.asm',
  'rgb_2_rgb.asm',
  'yuv_2_rgb.asm',
  'yuv2yuvX.asm',
)

libswscale_x86_mmx_sources = files(
  'hscale_fast_bilinear_simd.c',
)

