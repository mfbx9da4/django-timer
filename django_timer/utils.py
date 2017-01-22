import os


def get_last_n_levels_of_path(path, N):
    folders = []
    while 1:
        path, folder = os.path.split(path)

        if folder != "":
            if len(folders) == 0:
                # bottom level remove .py extension
                folder = folder[:-3]
            folders.insert(0, folder)
            if len(folders) == N:
                break
        else:
            break
    return folders
