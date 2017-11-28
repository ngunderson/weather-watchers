var $devicesHeader = $('#devices-header');
var $devices = $('#devices');
var $addDeviceForm = $('#add-device-form');
var $addDevError = $('#add-dev-error')

$addDeviceForm.submit(function(event) {
    $.ajax({
        url: '/devices',
        type: 'POST',
        data: $(this).serialize()
    }).done(function(res){
        getDevices()
	$addDeviceForm[0].reset();
	$addDevError.text('');
    }).fail(function(){
	$addDevError.text('(Invalid device information or password.)');
    });
    event.preventDefault();
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
    var str = '<tr dev-id="' + device.id + '"><td>' + device.id + '</td>';
    str += '<td>' + device.latitude + '</td>';
    str += '<td>' + device.longitude + '</td>';
    str += '<td><select>' + weatherHTML(device.weather) + '</select></td>';
    str += '<td><input type="password" name="password"></td>'
    str += '<td><button class="delete">X</button></td></tr>';

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
	    $devicesHeader.text('(' + Object.keys(data).length  +')');
	    data.forEach(function(device) {
		$devices.append(deviceHTML(device));
	    })
        }
    });
}

$devices.on('click', '.delete', function() {
    $row = $(this).closest('tr');
    $password = $row.find('input');
    console.log("password value", $password.val());
    $.ajax({
        url: '/devices/' + $row.attr('dev-id'),
        type: 'DELETE',
	headers: {'password': $password.val()},
        success: function() {
            $row.fadeOut(300, function() {
                $(this).remove();
		getDevices();
            });
        },
	error:  function (jqXHR, exception) {
	    $password.val('');
	}
    });

});

/* Load Page Data */
getDevices()
