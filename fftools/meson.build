#### --- GENERATED --- ####

fftools_sources = files(
  'cmdutils.c',
  'opt_common.c',
)

fftools_optional_sources = {
  # MANUAL 'ffmpeg ' : files('ffmpeg_dec.c','ffmpeg_demux.c','ffmpeg_enc.c','ffmpeg_filter.c','ffmpeg_hw.c','ffmpeg_mux.c','ffmpeg_mux_init.c','ffmpeg_opt.c','ffmpeg_sched.c','objpool.c','sync_queue.c','thread_queue.c'),
  # MANUAL 'ffplay ' : files('ffplay_renderer.c'),
}

#### --- END GENERATED --- ####

ffmpeg_sources = files(
  'ffmpeg_dec.c',
  'ffmpeg_demux.c',
  'ffmpeg_enc.c',
  'ffmpeg_filter.c',
  'ffmpeg_hw.c',
  'ffmpeg_mux.c',
  'ffmpeg_mux_init.c',
  'ffmpeg_opt.c',
  'ffmpeg_sched.c',
  'objpool.c',
  'sync_queue.c',
  'thread_queue.c',
  'ffmpeg.c'
)

ffplay_sources = files(
  'ffplay.c',
  'ffplay_renderer.c',
)

ffprobe_sources = files(
  'ffprobe.c'
)

if host_machine.system() == 'windows'
  fftoolsres = windows.compile_resources(files('fftoolsres.rc'),
    depend_files: files('fftools.manifest'),
    include_directories: include_directories('.')
  )

  fftools_sources += fftoolsres
endif
