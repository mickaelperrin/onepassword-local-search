from os import unlink as os_unlink, path as os_path


def pytest_sessionfinish(session, exitstatus):
    import glob
    for file in glob.glob(os_path.join(os_path.dirname(__file__), '.*_cached')):
        os_unlink(file)