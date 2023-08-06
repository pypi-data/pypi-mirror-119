from copy import deepcopy
from typing import Optional
from deemon.utils import startup
from deemon.core.exceptions import ValueNotAllowed, UnknownValue, PropertyTypeMismatch
import logging
from pathlib import Path
import json

logger = logging.getLogger(__name__)

ALLOWED_VALUES = {
    'bitrate': {1: "128", 3: "320", 9: "FLAC"},
    'alerts': [True, False],
    'record_type': ['all', 'album', 'ep', 'single']
}

DEFAULT_CONFIG = {
    "check_update": 1,
    "debug_mode": False,
    "query_limit": 5,
    "ranked_duplicates": True,
    "prompt_no_matches": True,
    "new_releases": {
        "by_release_date": True,
        "release_max_age": 90
    },
    "global": {
        "bitrate": "320",
        "alerts": False,
        "record_type": "all",
        "download_path": "",
        "email": ""
    },
    "deemix": {
        "path": "",
        "arl": ""
    },
    "smtp_settings": {
        "server": "",
        "port": 465,
        "username": "",
        "password": "",
        "from_addr": ""
    },
    "plex": {
        "base_url": "",
        "token": "",
        "library": ""
    }
}


class Config(object):
    _CONFIG_FILE: Optional[Path] = startup.get_config()
    _CONFIG: Optional[dict] = None

    def __init__(self):
        if not Config._CONFIG_FILE.exists():
            self.__create_default_config()

        if Config._CONFIG is None:
            with open(Config._CONFIG_FILE, 'r') as f:
                try:
                    Config._CONFIG = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    logger.exception(f"An error occured while reading from config: {e}")
                    raise

            if self.validate() > 0:
                self.__write_modified_config()

            # Set as default profile for init
            self.set('profile_id', 1, validate=False)

    @staticmethod
    def __create_default_config():
        with open(Config._CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

    @staticmethod
    def __write_modified_config():
        with open(Config._CONFIG_FILE, 'w') as f:
            json.dump(Config._CONFIG, f, indent=4)

    @staticmethod
    def validate():
        modified = 0

        def find_position(d, key):
            for k, v in d.items():
                if isinstance(v, dict):
                    next = find_position(v, key)
                    if next:
                        return [k] + next
                elif k == key:
                    return [k]

        def migrate_old_config(old_config, new_config):
            nonlocal modified
            # Old key > new key
            migration_map = [
                {'plex_baseurl': 'base_url'},
                {'plex_token': 'token'},
                {'plex_library': 'library'},
                {'deemix_path': 'path'},
                {'debug_mode': 'debug_mode'},
                {'arl': 'arl'},
                {'smtp_recipient': 'email'},
                {'smtp_server': 'server'},
                {'smtp_user': 'username'},
                {'smtp_pass': 'password'},
                {'smtp_port': 'port'},
                {'smtp_sender': 'from_addr'},
                {'bitrate': 'bitrate'},
                {'alerts': 'alerts'},
                {'record_type': 'record_type'},
                {'download_path': 'download_path'},
                {'release_by_date': 'by_release_date'},
                {'release_max_days': 'release_max_age'}
            ]
            for mlist in migration_map:
                for old, new in mlist.items():
                    if not old_config.get(old):
                        continue
                    opos = find_position(old_config, old) or [old]
                    npos = find_position(new_config, new) or [new]
                    usertmp_old = old_config
                    usertmp_new = new_config
                    if len(opos):
                        for i in opos[:-1]:
                            usertmp_old = usertmp_old.setdefault(i, {})
                    if len(npos):
                        for i in npos[:-1]:
                            usertmp_new = usertmp_new.setdefault(i, {})
                    logger.debug("Migrating " + ':'.join([str(x) for x in opos]) + " -> " + ':'.join(
                        [str(x) for x in npos]))
                    usertmp_new[npos[-1]] = usertmp_old[opos[-1]]
                    modified += 1
            return new_config

        def test_values(dict1, dict2):
            nonlocal modified
            for key, value in dict1.items():
                if key in dict2.keys():
                    if isinstance(dict1[key], dict):
                        test_values(dict1[key], dict2[key])
                    else:
                        if key in ALLOWED_VALUES:
                            if isinstance(ALLOWED_VALUES[key], dict):
                                if value in ALLOWED_VALUES[key].keys():
                                    dict1_tmp = dict1
                                    pos = find_position(dict1_tmp, key)
                                    for i in pos[:-1]:
                                        dict1_tmp = dict1.setdefault(i, {})
                                    dict1_tmp[key] = ALLOWED_VALUES[key][value]
                                    modified += 1
                                elif value in ALLOWED_VALUES[key].values():
                                    continue
                                else:
                                    raise UnknownValue(
                                        f"Unknown value in config - '{key}': {value} (type: {type(value).__name__})")
                            elif not isinstance(dict1[key], type(dict2[key])):
                                if isinstance(dict2[key], bool):
                                    if dict1[key] == 1:
                                        dict1[key] = True
                                        modified += 1
                                    if dict1[key] == 0:
                                        dict1[key] = False
                                        modified += 1
                                else:
                                    raise UnknownValue(
                                        f"Unknown value in config - '{key}': {value} (type: {type(value).__name__})")
                        elif not isinstance(dict1[key], type(dict2[key])):
                            if isinstance(dict2[key], bool):
                                if dict1[key] == 1:
                                    dict1[key] = True
                                    modified += 1
                                if dict1[key] == 0:
                                    dict1[key] = False
                                    modified += 1
                            else:
                                raise PropertyTypeMismatch(
                                    f"Invalid type in config - '{str(key)}' incorrectly set as {type(value).__name__}")
                        else:
                            pass

        print("Loading configuration, please wait...")
        Config._CONFIG = migrate_old_config(Config._CONFIG, deepcopy(DEFAULT_CONFIG))
        test_values(Config._CONFIG, DEFAULT_CONFIG)
        return modified

    @staticmethod
    def get_config_file() -> Path:
        return Config._CONFIG_FILE

    @staticmethod
    def get_config() -> dict:
        return Config._CONFIG

    @staticmethod
    def plex_baseurl() -> str:
        return Config._CONFIG.get('plex').get('base_url')

    @staticmethod
    def plex_token() -> str:
        return Config._CONFIG.get('plex').get('token')

    @staticmethod
    def plex_library() -> str:
        return Config._CONFIG.get('plex').get('library')

    @staticmethod
    def download_path() -> str:
        return Config._CONFIG.get('global').get('download_path')

    @staticmethod
    def deemix_path() -> str:
        return Config._CONFIG.get('deemix').get('path')

    @staticmethod
    def arl() -> str:
        return Config._CONFIG.get('deemix').get('arl')

    @staticmethod
    def release_by_date() -> bool:
        return Config._CONFIG.get('new_releases').get('by_release_date')

    @staticmethod
    def release_max_days() -> int:
        return Config._CONFIG.get('new_releases').get('release_max_age')

    @staticmethod
    def bitrate() -> str:
        return Config._CONFIG.get('global').get('bitrate')

    @staticmethod
    def alerts() -> bool:
        return Config._CONFIG.get('global').get('alerts')

    @staticmethod
    def record_type() -> str:
        return Config._CONFIG.get('global').get('record_type')

    @staticmethod
    def smtp_server() -> str:
        return Config._CONFIG.get('smtp_settings').get('server')

    @staticmethod
    def smtp_port() -> int:
        return Config._CONFIG.get('smtp_settings').get('port')

    @staticmethod
    def smtp_user() -> str:
        return Config._CONFIG.get('smtp_settings').get('username')

    @staticmethod
    def smtp_pass() -> str:
        return Config._CONFIG.get('smtp_settings').get('password')

    @staticmethod
    def smtp_sender() -> str:
        return Config._CONFIG.get('smtp_settings').get('from_addr')

    @staticmethod
    def smtp_recipient() -> list:
        return Config._CONFIG.get('global').get('email')

    @staticmethod
    def check_update() -> int:
        return Config._CONFIG.get('check_update')

    @staticmethod
    def debug_mode() -> bool:
        return Config._CONFIG.get('debug_mode')

    @staticmethod
    def profile_id() -> int:
        return Config._CONFIG.get('profile_id')

    @staticmethod
    def update_available() -> int:
        return Config._CONFIG.get('update_available')

    @staticmethod
    def query_limit() -> int:
        return Config._CONFIG.get('query_limit')

    @staticmethod
    def ranked_duplicates() -> int:
        return Config._CONFIG.get('ranked_duplicates')

    @staticmethod
    def prompt_no_matches() -> bool:
        return Config._CONFIG.get('prompt_no_matches')

    @staticmethod
    def allowed_values(prop) -> list:
        return ALLOWED_VALUES.get(prop)

    @staticmethod
    def find_position(d, property):
        for k, v in d.items():
            if isinstance(v, dict):
                next = Config.find_position(v, property)
                if next:
                    return [k] + next
            elif k == property:
                return [k]

    @staticmethod
    def set(property, value, validate=True):
        if not validate:
            Config._CONFIG[property] = value
        if Config._CONFIG.get(property):
            if property in ALLOWED_VALUES:
                if value in ALLOWED_VALUES[property]:
                    Config._CONFIG[property] = value
                    return
                raise ValueNotAllowed(f"Property {property} requires one of "
                                      f"{', '.join(ALLOWED_VALUES[property])}, not {value}.")

            if isinstance(value, type(Config._CONFIG[property])):
                Config._CONFIG[property] = value
                return
            else:
                raise PropertyTypeMismatch(f"Type mismatch while setting {property} "
                                           f"to {value} (type: {type(value).__name__})")

        else:
            property_path = Config.find_position(Config._CONFIG, property)
            tmpConfig = Config._CONFIG
            for k in property_path[:-1]:
                tmpConfig = tmpConfig.setdefault(k, {})
            if property in ALLOWED_VALUES:
                if isinstance(ALLOWED_VALUES[property], dict):
                    if value in [str(x) for x in ALLOWED_VALUES[property].values()]:
                        tmpConfig[property_path[-1]] = value
                        return
                if value in ALLOWED_VALUES[property]:
                    tmpConfig[property_path[-1]] = value
                    return
                raise ValueNotAllowed(f"Property {property} requires one of "
                                      f"'{', '.join(str(x) for x in ALLOWED_VALUES[property])}', "
                                      f"not {value} of type {type(value)}.")

            if isinstance(value, type(tmpConfig[property])):
                tmpConfig[property] = value
                return
            else:
                raise PropertyTypeMismatch(f"Type mismatch while setting {property} "
                                           f"to {value} (type: {type(value).__name__})")


class LoadProfile(object):
    def __init__(self, profile: dict):
        logger.debug(f"Loaded config for profile {str(profile['id'])} ({str(profile['name'] )})")
        # Rename keys to match config
        profile["profile_id"] = profile.pop("id")
        profile["base_url"] = profile.pop("plex_baseurl")
        profile["token"] = profile.pop("plex_token")
        profile["library"] = profile.pop("plex_library")

        # Append to config for debug output; Remove profile name from dict
        Config.set("profile_name", profile.pop("name"), validate=False)

        for key, value in profile.items():
            if value is None:
                continue
            Config.set(key, value)

        logger.debug("=========== CONFIG ===========")
        for key, value in Config.get_config().items():
            if key in ['smtp_settings']:
                continue
            if isinstance(value, dict):
                for k, v in value.items():
                    if k in ['arl', 'email']:
                        continue
                    logger.debug(f"{key}/{k}: {v}")
            else:
                logger.debug(f"{key}: {value}")
        logger.debug("==============================")
