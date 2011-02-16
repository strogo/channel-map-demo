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

For the demo, scans are simulated from a few sample products and stores.

## Using the Demo

This demo requires the Google App Engine SDK. 

1. Check out the code and `cd` into that directory
2. Start your local server: `dev_appserver.py .`
3. Visit the map page at `http://localhost:8080/`
4. In another tab, launch the mock scan submission service at `http://localhost:8080/scan`
5. Watch the simulated scans come in. 

You can open the map in multiple web browsers to see the channel API
push the same updates to multiple clients.

Since channels can only stay open for 2 hours, it is necessary to periodically re-establish a new channel connection. This is accomplished by sending a 'refresh' JSON message to the client. In this demo, that causes the page to reload, which is the simplest way to re-establish a channel. This is accomplished with a cron.yaml entry that runs once an hour.

To demo this behavior, the channel refresh timeout has been set very
low, to one minute. Since cron does not run in the SDK, you must
trigger it manually. Do this by visiting
`http://localhost:8080/cleanup` in another window. If your web browser
has been on the map page for more than one minute, it will refresh.

## License

This code is copyright Best Buy and licensed under the AGPL. See LICENSE.txt for details.
