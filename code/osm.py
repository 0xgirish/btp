import osmium as osm
import pandas as pd

# An obstacle contains nodes (lat, lon) which forms a polygon and has height >= 12
class Obstacle:
    def __init__(self, nodes):
        self.nodes = list()

    # draw the polygon with nodes on the figure
    def draw(self, fig):
        # TODO: draw logic here
        pass

# ShopHandler extract restaurant's locations from the osm file
class ShopHandler(osm.SimpleHandler):
    def __init__(self, region=None):
        osm.SimpleHandler.__init__(self)
        self.region = region
        self.osm_data = list()
        self.obstacles = list() # contains list of all the building which have height >= 12 m

#   add nodes which are restaurants
    def node(self, n):
        if ShopHandler.is_restaurant(n):
            self.osm_data.append(ShopHandler.getLocation(n.location))

#   check for buildings with height greater then 12m
    def way(self, w):
        if ShopHandler.is_obstacle(w):
#           TODO: extract polygon from the obstacle
            pass

#   create csv file for shops and obstacles
#   TODO: create csv file for obstacles
    def to_csv(self):
        data_columns = ['lat', 'lon']
        df = pd.DataFrame(self.osm_data, columns=data_columns)
        df.to_csv(f'csv/{self.region}/shops.csv')
        return df

    @staticmethod
    def is_obstacle(w):
        for tag in w.tags:
            if tag.k == 'building:height' and float(tag.v) >= 12:
                return True and w.is_closed()
        return False

    @staticmethod
    def is_restaurant(elem):
        for tag in elem.tags:
            if tag.v == 'restaurant':
                return True
        return False

    @staticmethod
    def getLocation(location):
        return [float(location.lat), float(location.lon)]

