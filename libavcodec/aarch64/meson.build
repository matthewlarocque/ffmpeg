#### --- GENERATED --- ####

libavcodec_aarch64_optional_sources = {
  'aac_decoder' : files('aacpsdsp_init_aarch64.c','sbrdsp_init_aarch64.c'),
  'ac3dsp' : files('ac3dsp_init_aarch64.c'),
  'dca_decoder' : files('synth_filter_init.c'),
  'fdctdsp' : files('fdctdsp_init_aarch64.c'),
  'fmtconvert' : files('fmtconvert_init.c'),
  'h264chroma' : files('h264chroma_init_aarch64.c'),
  'h264dsp' : files('h264dsp_init_aarch64.c'),
  'h264pred' : files('h264pred_init.c'),
  'h264qpel' : files('h264qpel_init_aarch64.c'),
  'hpeldsp' : files('hpeldsp_init_aarch64.c'),
  'idctdsp' : files('idctdsp_init_aarch64.c'),
  'me_cmp' : files('me_cmp_init_aarch64.c'),
  'mpegaudiodsp' : files('mpegaudiodsp_init.c'),
  'mpegvideoenc' : files('mpegvideoencdsp_init.c'),
  'neon_clobber_test' : files('neontest.c'),
  'opus_decoder' : files('opusdsp_init.c'),
  'pixblockdsp' : files('pixblockdsp_init_aarch64.c'),
  'rv40_decoder' : files('rv40dsp_init_aarch64.c'),
  'vc1dsp' : files('vc1dsp_init_aarch64.c'),
  'videodsp' : files('videodsp_init.c'),
  'vorbis_decoder' : files('vorbisdsp_init.c'),
  'vp8dsp' : files('vp8dsp_init_aarch64.c'),
  'vp9_decoder' : files('vp9dsp_init_10bpp_aarch64.c','vp9dsp_init_12bpp_aarch64.c','vp9mc_aarch64.S','vp9dsp_init_aarch64.c'),
}

libavcodec_aarch64_armv8_optional_sources = {
  'videodsp' : files('videodsp.S'),
}

libavcodec_aarch64_neon_optional_sources = {
  'aac_decoder' : files('sbrdsp_neon.S','aacpsdsp_neon.S'),
  'ac3dsp' : files('ac3dsp_neon.S'),
  'dca_decoder' : files('synth_filter_neon.S'),
  'fdctdsp' : files('fdctdsp_neon.S'),
  'fmtconvert' : files('fmtconvert_neon.S'),
  'h264chroma' : files('h264cmc_neon.S'),
  'h264dsp' : files('h264dsp_neon.S','h264idct_neon.S'),
  'h264pred' : files('h264pred_neon.S'),
  'h264qpel' : files('h264qpel_neon.S','hpeldsp_neon.S'),
  'hevc_decoder' : files('hevcdsp_deblock_neon.S','hevcdsp_idct_neon.S','hevcdsp_init_aarch64.c'), # MANUAL
  'hpeldsp' : files('hpeldsp_neon.S'),
  'idctdsp' : files('idctdsp_neon.S','simple_idct_neon.S'),
  'me_cmp' : files('me_cmp_neon.S'),
  'mpegaudiodsp' : files('mpegaudiodsp_neon.S'),
  'mpegvideoenc' : files('mpegvideoencdsp_neon.S'),
  'opus_decoder' : files('opusdsp_neon.S'),
  'pixblockdsp' : files('pixblockdsp_neon.S'),
  'vc1dsp' : files('vc1dsp_neon.S'),
  'vorbis_decoder' : files('vorbisdsp_neon.S'),
  'vp8dsp' : files('vp8dsp_neon.S'),
  'vp9_decoder' : files('vp9itxfm_16bpp_neon.S','vp9itxfm_neon.S','vp9lpf_16bpp_neon.S','vp9lpf_neon.S','vp9mc_16bpp_neon.S','vp9mc_neon.S'),
}

#### --- END GENERATED --- ####

subdir('vvc')

libavcodec_aarch64_optional_sources += libavcodec_aarch64_vvc_optional_sources
libavcodec_aarch64_neon_optional_sources += libavcodec_aarch64_vvc_neon_optional_sources

if conf.get('hevc_decoder') == 1
  libavcodec_aarch64_neon_optional_sources += {
    'hevc_decoder': libavcodec_aarch64_neon_optional_sources ['hevc_decoder'] + files('h26x/epel_neon.S','h26x/qpel_neon.S','h26x/sao_neon.S')
  }
elif conf.get('vvc_decoder') == 1
  libavcodec_x86_optional_sources += {
    'vvc_decoder': libavcodec_aarch64_neon_optional_sources ['vvc_decoder'] + files('h26x/epel_neon.S','h26x/qpel_neon.S','h26x/sao_neon.S')
  }
endif
