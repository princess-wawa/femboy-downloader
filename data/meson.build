install_data(
  'femboydownloader.desktop',
  install_dir: join_paths(get_option('datadir'), 'applications')
)

install_data(
  'icon.png',
  install_dir: join_paths(get_option('datadir'), 'icons', 'hicolor', '128x128', 'apps')
)


pkgdatadir = join_paths(get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'femboydownloader')



ui_sources = ['main.ui', 'preferences.ui']
install_data(ui_sources, install_dir: join_paths(moduledir, 'data'))
