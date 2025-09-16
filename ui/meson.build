pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'femboydownloader')

#desktop_utils = find_program('desktop-file-validate', required: false)
#if desktop_utils.found()
#  test('Validate desktop file', desktop_utils, args: [desktop_file])
#endif

ui_sources = ['icon.png', 'main.ui', 'preferences.ui']

install_data(ui_sources, install_dir: join_paths(moduledir, 'ui'))
