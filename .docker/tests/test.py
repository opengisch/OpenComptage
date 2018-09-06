from qgis.utils import iface, active_plugins, plugins

if __name__ == "__main__":

    print("Hello!")

    print(active_plugins)
    
    iface.actionExit().trigger()
