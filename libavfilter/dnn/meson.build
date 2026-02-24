libavfilter_dnn_optional_sources = {
  'dnn' : files('dnn_interface.c','dnn_io_proc.c','queue.c','safe_queue.c','dnn_backend_common.c'),
  'libopenvino' : files('dnn_backend_openvino.c'),
  'libtensorflow' : files('dnn_backend_tf.c'),
  'libtorch' : files('dnn_backend_torch.cpp'),
}

languages_map += {
  'libtorch': ['cpp'],
}
