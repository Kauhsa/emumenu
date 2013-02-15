import os
import shlex
from subprocess import Popen, PIPE
from configreader import read_config


def launch(command, pipe=True, input_s=""):
    if pipe:
        p = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    else:
        p = Popen(shlex.split(command), universal_newlines=True)
    out, _ = p.communicate(input_s)
    return out.strip()


if __name__ == '__main__':
    home = os.getenv('USERPROFILE') or os.getenv('HOME')
    config_file_path = os.path.join(home, '.emumenu.yaml')
    with open(config_file_path, 'r') as f:
        config = read_config(f)

    dmenu_command = config['command']

    groups = '\n'.join(config['groups'].group_names)
    group = launch(dmenu_command, input_s=groups)
    if group:
        items = '\n'.join(config['groups'].groups[group].entry_names)
        item = launch(dmenu_command, input_s=items)
        if item:
            cmd = config['groups'].groups[group].entries[item]
            launch(cmd, pipe=False)

