def classFactory(iface):
    """Load Comptages class from file comptages.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from .comptages import Comptages
    return Comptages(iface)
