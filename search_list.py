from import_file import *

__all__ = ["load_agents"]


def load_agents():
    all_agents = {}
    for importer, modname, ispkg in pkgutil.iter_modules(search.__path__):
        if modname != 'agent':
            reload(sys.modules['{0}.{1}'.format('search', modname)])
    for importer, modname, ispkg in pkgutil.iter_modules(search.__path__):
        for name, obj in inspect.getmembers(sys.modules['search.{0}'.format(modname)], inspect.isclass):
            if 'search.{0}'.format(modname) == obj.__module__ and '{0}Class'.format(modname) == name and issubclass(obj, search.Agent):
                all_agents[modname] = obj

    return all_agents
