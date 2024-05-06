import geocoder

def get_user_location():
    # Get the user's current location using the geocoder module
    location = geocoder.ip('me')

    if location:
        print("Your current location:")
        print("Latitude:", location.latlng[0])
        print("Longitude:", location.latlng[1])
    else:
        print("Unable to retrieve location.")

# Call the function to get the user's location
get_user_location()
