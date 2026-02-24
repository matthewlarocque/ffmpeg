libswresample_aarch64_sources = files(
  'audio_convert_init.c',
  'resample_init.c',
)

libswresample_aarch64_optional_sources = {
  'neon_clobber_test' : files('neontest.c'),
}

libswresample_aarch64_neon_sources = files(
  'audio_convert_neon.S',
  'resample.S',
)

