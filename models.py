class Scan(object):
    def __init__(self, store=None, product=None, timestamp=None):
        self.store = store
        self.product = product
        self.timestamp = timestamp

class Store(object):
    def __init__(self, name=None, state=None, lat=None, lon=None):
        self.name = name
        self.state = state
        self.lat = lat
        self.lon = lon

class Product(object):
    def __init__(self, name=None, image=None):
        self.name = name
        self.image = image
