pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'femboydownloader')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('moduledir', moduledir)

configure_file(
  input: 'femboydownloader.in',
  output: 'femboydownloader',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

femboydownloader_sources = [
  'buttons.py',
  'main.py',
  'reddit.py',
  'set_wallpaper',
  'settings.py',
  'tools.py'
]

install_data(femboydownloader_sources, install_dir: join_paths(moduledir, 'src'))
