import os

PATH = '/home/sonya/gunicorn-master/project_atom_app/dataset'


def maybe_update_dataset(ctime):
    """
     Whether dataset can be reloaded
    """
    new_ctime = os.stat(PATH).st_ctime  # update when inode metadata or file content changed, POSIX only

    if ctime == new_ctime:
        return False, ctime
    else:
        ctime = new_ctime
    return True, new_ctime
