libswresample_arm_sources = files(
  'audio_convert_init.c',
  'resample_init.c',
)

libswresample_arm_optional_sources = {
  'neon_clobber_test' : files('neontest.c'),
}

libswresample_arm_neon_sources = files(
  'audio_convert_neon.S',
  'resample.S',
)

