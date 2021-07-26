let map;

var options = {
    center: {
        lat: 6.4453, lng: 3.2634
    },
    zoom: 6
}

var users = [
    {
        'name': 'David',
        'center': {
            'lat': 6.4411476, 
            'lng': 3.2565705
        }
    },
    {
        'name': 'John',
        'center': {
            'lat': 6.454846499999999,
            'lng': 3.257618
        }
    },
    {
        'name': 'Pete',
        'center': {
            'lat': 6.474086600000001,
            'lng': 3.2953874
        }
    },
    {
        'name': 'Mike',
        'center': {
            'lat': 6.464244,
            'lng': 3.3045587
        }
    }
]




function initMap() {
    var options = {
        center: {
            lat: 6.4453, lng: 3.2634
        },
        zoom: 11
    }

    map = new google.maps.Map(document.getElementById("map"), options);

    for ( var i = 0; i < 4; i++) {
        const marker = new google.maps.Marker({
            position: users[i].center,
            
            map: map,
        });
    
        const detialWindow = new google.maps.InfoWindow({
            content: `<div class='name'>
                        <a href="#">Hello</a>
                    </div>
            `
        });

        
    
        marker.addListener('mouseover', () => {
            detialWindow.open(map, marker);
        });
    
    }

    };
