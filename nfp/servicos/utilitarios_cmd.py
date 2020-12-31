import subprocess
import time
import os


def executar_comando(command, *args, shell=False, debug=False):
    try:
        sp = subprocess.Popen([command, *args], close_fds=True, **_subprocess_args())
        res, err = sp.communicate()
        time.sleep(5)
        if debug:
            return res, err
    except Exception as e:
        print('Erro ao executar comando {}'.format(command))
        raise e


def _subprocess_args(include_stdout=True):
    if hasattr(subprocess, 'STARTUPINFO'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}
    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env})
    return ret
