# Demo: Google App Engine Channel API with Google Maps

This is a demo showing how to send updates to multiple connected
clients using the Google App Engine [Channel API](http://code.google.com/appengine/docs/python/channel/overview.html). 
The messages are used to display a product on a Google Map.

The weakness of the implementation is that there is a race condition
with adding or removing clients to the JSON object in
memcache. However, it works as a simple demo.

This code was extracted from the [BBYScan map](http://www.bbyscan.com/map)
which displays live QR code scans from Best Buy stores. For more details about the BBYScan
project, [read our blog post](http://bbyopen.com/2011/01/bbyscan-mobile-code-scan-map).

## License

This code is copyright Best Buy and licensed under the AGPL. See LICENSE.txt for details.
