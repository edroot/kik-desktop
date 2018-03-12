from pkgutil import get_data


def load_stylesheet(name):
    return get_data('kik_desktop_legacy', name).decode('unicode_escape')
