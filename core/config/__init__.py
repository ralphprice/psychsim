"""config -- data-file-first configuration loading (town profiles, module params)."""
from .townprofile import TownProfile
from .loader import (load_town_profile, load_town_profiles, load_module_params,
                     load_roles, dataclass_from_dict,
                     DATA_DIR, TOWNTYPES_DIR, MODULES_DIR, ROLES_DIR)

__all__ = ["TownProfile", "load_town_profile", "load_town_profiles",
           "load_module_params", "load_roles", "dataclass_from_dict",
           "DATA_DIR", "TOWNTYPES_DIR", "MODULES_DIR", "ROLES_DIR"]
