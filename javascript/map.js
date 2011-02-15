MapDemo = function() {
  var scans = [];
  var map = null;
  var centerUSALat = 39.50;
  var centerUSALon = -96.0;

  function onMessage(message) {
    var scan = JSON.parse(message.data);

    // this channel is expired. Reload to get a new token.
    if (scan.refresh) {
      window.location.reload();
      return;
    }

    var infoWindow = new google.maps.InfoWindow(
      {content: scan.content,
       disableAutoPan: true,
       position: new google.maps.LatLng(scan.lat, scan.lon)});

    infoWindow.open(map);
    setTimeout(function() { infoWindow.close(); }, 10000);
  };

  return {
    setUp: function(token) {
      var mapOptions = {
        zoom: 5,
        center: new google.maps.LatLng(centerUSALat, centerUSALon),
        disableDefaultUI: true,
        keyboardShortcuts: false,
        draggable: false,
        mapTypeId: google.maps.MapTypeId.SATELLITE
      };

      map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

      var channel = new goog.appengine.Channel(token);
      var handlers = {
        'onopen': function() { },
        'onmessage': onMessage
      };
      var socket = channel.open(handlers);
    }
  };
}();
