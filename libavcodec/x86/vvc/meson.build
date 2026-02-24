#### --- GENERATED --- ####

libavcodec_x86_vvc_optional_sources = {
  'vvc_decoder' : files('vvcdsp_init.c'), # MANUAL
}

libavcodec_x86_vvc_x86asm_optional_sources = {
  'vvc_decoder' : files('vvc_alf.asm','vvc_dmvr.asm','vvc_mc.asm','vvc_of.asm','vvc_sad.asm'), # MANUAL
}

#### --- END GENERATED --- ####

if conf.get('x86_64', 0) == 1
  # Alternatively,
  # panic: ../libavcodec/x86/simple_idct10.asm: assertion cv8_state.source_files != NULL failed at output/codeview.c:512
  libavcodec_x86_vvc_x86asm_optional_sources += {
    'vvc_decoder': libavcodec_x86_vvc_x86asm_optional_sources ['vvc_decoder'] + files('vvc_alf.asm', 'vvc_dmvr.asm', 'vvc_of.asm', 'vvc_sad.asm'),
  }
endif
