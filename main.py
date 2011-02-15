from datetime import datetime
import os
import random
import uuid

from django.utils import simplejson

from google.appengine.api import channel
from google.appengine.api import memcache 
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util



from models import Scan, Store, Product

STORES = [Store(name='Stillwater', state='OK', lat=36.14249, lon=-97.05415),
          Store(name='Holyoke', state='MA', lat=42.169613, lon=-72.643005),
          Store(name='Chelsea', state='NY', lat=40.74194, lon=-73.99295),
          Store(name='Reston', state='VA', lat=38.961487, lon=-77.356522),
          Store(name='Apple Valley', state='CA', lat=33.698444, lon=-117.82413),
          Store(name='Temecula', state='CA', lat=33.482292, lon=-117.08905),
          Store(name='Avon', state='IN', lat=39.765411, lon=-86.345963),
          Store(name='Maple Grove', state='MN', lat=45.093018, lon=-93.442375),
          Store(name='Lansing', state='IL', lat=41.584328, lon=-87.557167),
          Store(name='South County', state='MO', lat=38.510273, lon=-90.33017),
          Store(name='Ocala', state='FL', lat=29.165569, lon=-82.167549),
          Store(name='Flower Mound', state='TX', lat=33.06926, lon=-97.080109),
          Store(name='Missoula', state='MT', lat=46.889271, lon=-114.03745),
          Store(name='Las Vegas II', state='NV', lat=36.196686, lon=-115.24034),
          Store(name='Beaverton', state='OR', lat=45.497982, lon=-122.80905),
          Store(name='Yakima', state='WA', lat=46.567719, lon=-120.48235),
          Store(name='Fargo', state='ND', lat=46.857113, lon=-96.842743),
          Store(name='Aurora', state='CO', lat=39.697807, lon=-104.82673)]

PRODUCTS = [Product(name='Raymarine C90W Chartplotter GPS', image='http://images.bestbuy.com/BestBuy_US/images/products/1063/1063733_sc.jpg'),
            Product(name='SunBriteTV 32" Class / 720p / 60Hz / Outdoor LCD HDTV with Articulating Wall Mount', image='http://images.bestbuy.com/BestBuy_US/images/products/8848/8848937_rc.jpg'),
            Product(name='Brother MFC-9450cdn Network-Ready Color All-in-One Laser Printer', image='http://images.bestbuy.com/BestBuy_US/images/products/9534/9534202_rc.jpg'),
            Product(name='Fierce Audio Power and Signal Installation Kit', image='http://images.bestbuy.com/BestBuy_US/images/products/8848/8848937_rc.jpg')]


class ScanHandler(webapp.RequestHandler):
    def get(self):
        push_to_channels(random_scan())

        path = os.path.join(os.path.dirname(__file__), 'templates', 'scan.html')
        self.response.out.write(template.render(path, {}))
    
class MapHandler(webapp.RequestHandler):
    def get(self):
        channel_id = uuid.uuid4().hex
        token = channel.create_channel(channel_id)

        channels = simplejson.loads(memcache.get('channels') or '{}')
    
        channels[channel_id] = str(datetime.now())

        memcache.set('channels', simplejson.dumps(channels))

        template_values = {
            'token': token
        }

        path = os.path.join(os.path.dirname(__file__), 'templates', 'map.html')
        self.response.out.write(template.render(path, template_values))

class ChannelCleanupHandler(webapp.RequestHandler):
    def get(self):
        delete_inactive_channels()

        self.response.out.write("Deleted old channels")

def random_scan():
    return Scan(store=random.choice(STORES),
                product=random.choice(PRODUCTS),
                timestamp=datetime.now())

def push_to_channels(scan):
    content = '''
    <div class="infowindowcontent">
      <table>
      <tr>
      <td class="prod_img">
        <img src="%(image)s"/>
      </td>
      <td class="prod_info">
        <strong>%(product_name)s</strong><br/><em>%(timestamp)s</em><br><em>%(store_name)s, %(state)s
      </td>
      </tr>
      </table>
    </div>''' % { 'product_name': scan.product.name,
                  'timestamp' : scan.timestamp.strftime('%I:%M %p'),
                  'store_name': scan.store.name,
                  'state': scan.store.state,
                  'image': scan.product.image }
            
    message = {'lat': scan.store.lat,
               'lon': scan.store.lon,
               'content': content}

    channels = simplejson.loads(memcache.get('channels') or '{}')
    
    for channel_id in channels.iterkeys():
        encoded_message = simplejson.dumps(message)

        channel.send_message(channel_id, encoded_message)

def delete_inactive_channels():
    channels = simplejson.loads(memcache.get('channels') or '{}')

    now = datetime.now()
    for channel_id, created in channels.items():
        
        dt = datetime.strptime(created.split(".")[0], "%Y-%m-%d %H:%M:%S")

        if (now - dt) > timedelta(minutes=60):
            del channels[channel_id]
            
            message = {'refresh': 'y'}
            channel.send_message(channel_id, simplejson.dumps(message))
                
        memcache.set('channels', simplejson.dumps(channels))

def main():
    application = webapp.WSGIApplication([('/', MapHandler),
                                          ('/scan', ScanHandler),
                                          ('/cleanup', ChannelCleanupHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
