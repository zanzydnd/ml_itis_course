def construct_html(points, path):
    objects_name_list = []
    body = 'ymaps.ready(init); function init() { var myMap = new ymaps.Map("map", {center: [55.76, 37.64],zoom: 10}); var myGeoObject; var myPolyline;'

    for point_num in path:
        body += 'myGeoObject = new ymaps.GeoObject({geometry: {type: "Point", coordinates: [%s, %s]}}); myMap.geoObjects.add(myGeoObject);\n' % points.get(point_num)


    i = 1
    while i < len(path):
        body += 'myPolyline = new ymaps.GeoObject({geometry: {type: "LineString",coordinates: [[%s, %s],[%s, %s]]}}); myMap.geoObjects.add(myPolyline);\n' % (*points.get(path[i-1]),*points.get(path[i]))
        i += 1

    body += 'myPolyline = new ymaps.GeoObject({geometry: {type: "LineString",coordinates: [[%s, %s],[%s, %s]]}}); myMap.geoObjects.add(myPolyline);\n' % (*points.get(path[len(path) - 1]), *points.get(path[0]))
    body += "}"
    with open("result.html",'w') as w:
        w.write(
            f"""
            <!DOCTYPE html>
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <title>Быстрый старт. Размещение интерактивной карты на странице</title>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                    <script src="https://api-maps.yandex.ru/2.1/?lang=ru_RU" type="text/javascript">
                    </script>
                    <script type="text/javascript">
                    {body}
                    </script>
                    </head>
                    
                    <body>
                    <div id="map" style="width: 600px; height: 400px"></div>
                    
                    </body>
                    
                    </html>
            """
        )