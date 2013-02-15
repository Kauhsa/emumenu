import os
import yaml
import shlex

class ConfigException(Exception):
    pass


def read_config(stream):
    config = {}
    config_file = yaml.load(stream)
    config['groups'] = Groups(config_file['groups'])
    config['command'] = config_file['command']
    return config


class Groups:
    def __init__(self, section):
        groups = [Group(group) for group in section]
        self.groups = dict((group.name, group) for group in groups)
        self.group_names = sorted(self.groups.keys())


class Group:
    def __init__(self, section):
        self.name = section['name']
        self.entries = self._load_entries(section['entries'])
        self.entry_names = sorted(self.entries.keys())

    def _load_entries(self, entries_section):
        entry_dict = {}
        for entry in entries_section:
            for name, cmd in get_items(entry):
                entry_dict[name] = cmd
        return entry_dict


def get_items(entry):
    if 'folder' in entry:
        return folder_items(entry['folder'])
    elif 'single' in entry:
        return single_item(entry['single'])
    else:
        raise ConfigException('entries section entry is not valid')


def folder_items(folder_entry):
    files = [f for f in os.listdir(folder_entry['path']) if any(f.endswith('.' + ext) for ext in folder_entry['filters'])]
    return [(f, folder_entry['cmd'] % shlex.quote(os.path.join(folder_entry['path'], f))) for f in files]


def single_item(single_entry):
    return [(single_entry['name'], single_entry['cmd'])]
