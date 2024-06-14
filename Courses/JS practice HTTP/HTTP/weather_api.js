function getWeather(cityID) {
    var key = '8db44f8b758f996a9139941aa44f6877';
    cityID = '625143'
    fetch('http://api.openweathermap.org/data/2.5/weather?id=' + cityID + '&appid=' + key)
        .then(function(resp) {
            return resp.json()
        })
        .then(function(data) {
            console.log(data);
        });
}