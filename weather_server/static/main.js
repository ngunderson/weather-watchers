var $devicesHeader = $('#devices-header');
var $devices = $('#devices');
var $addDeviceForm = $('#add-device-form');

$addDeviceForm.submit(function(event) {
    $.ajax({
        url: '/devices',
        type: 'POST',
        data: $(this).serialize()
    }).done(function(res){
        getDevices()
    }).fail(function(){
        console.error("An error occurred, the files couldn't be created.");
    });
    event.preventDefault()
})

function weatherHTML(weather) {
    var str = '';

    weather.reverse().forEach(function(entry) {
	time = new Date(entry.time).toLocaleString();
	str += '<option> ' + time + ' -- ' + entry.temp + ' F</option>';
    });

    return str;
}

function deviceHTML(device) {
    var str = '<tr><td>' + device.id + '</td>';
    str += '<td>' + device.latitude + '</td>';
    str += '<td>' + device.longitude + '</td>';
    str += '<td><select>' + weatherHTML(device.weather) + '</select></tr>';

    return str
}

function getDevices() {
    /* Clear existing devices */
    $devices.empty();
    /* Retrieve all devices */
    $.ajax({
        url: '/devices',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
	    $devicesHeader.text('(' + Object.keys(data).length  +')')
	    data.forEach(function(device) {
		console.log("in func")
		$devices.append(deviceHTML(device));
	    })
        }
    });
}

/* Load Page Data */
getDevices()
