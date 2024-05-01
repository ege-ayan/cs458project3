import React, { useState, useEffect } from 'react';

const SunDistanceCalculator = () => {
    const [latitude, setLatitude] = useState('');
    const [longitude, setLongitude] = useState('');
    const [distanceToSun, setDistanceToSun] = useState(null);

    const calculateDistanceToSun = () => {
        // Calculate distance to Sun's core using provided coordinates
        // You would need a formula or library for this calculation
        // The formula would need to take into account the changing positions of the Sun and Earth
        // For simplicity, let's assume the distance is calculated in kilometers
        const distance = calculateDistance(latitude, longitude);
        setDistanceToSun(distance);
    };

    const calculateDistance = (lat, long) => {
        // Placeholder function for distance calculation
        // Replace this with actual calculation using appropriate formula or library
        // For simplicity, returning a random distance between 100,000 km and 150,000 km
        return Math.floor(Math.random() * (150000 - 100000 + 1)) + 100000;
    };

    useEffect(() => {
        // Fetch user's GPS coordinates automatically when component mounts
        // For demonstration purposes, this is a placeholder function
        // In real-world scenario, you would use a library like Geolocation API
        const fetchUserCoordinates = () => {
            // Placeholder function for fetching GPS coordinates
            // Replace this with actual implementation using Geolocation API
            // For demonstration, setting random coordinates within valid ranges
            const randomLatitude = Math.random() * (90 - (-90)) - 90;
            const randomLongitude = Math.random() * (180 - (-180)) - 180;
            setLatitude(randomLatitude.toFixed(6));
            setLongitude(randomLongitude.toFixed(6));
        };

        fetchUserCoordinates();
    }, []);

    const handleManualSubmit = (e) => {
        e.preventDefault();
        calculateDistanceToSun();
    };

    const handleAutomaticSubmit = () => {
        // Fetch GPS coordinates and calculate distance to Sun
        // This would use Geolocation API in a real-world scenario
        navigator.geolocation.getCurrentPosition(
            (position) => {
                setLatitude(position.coords.latitude.toFixed(6));
                setLongitude(position.coords.longitude.toFixed(6));
                calculateDistanceToSun();
            },
            (error) => {
                console.error('Error getting user location:', error);
            }
        );
    };

    return (
        <div>
            <h1>Sun Distance Calculator</h1>
            <form onSubmit={handleManualSubmit}>
                <label>
                    Enter Latitude:
                    <input
                        type="number"
                        value={latitude}
                        onChange={(e) => setLatitude(e.target.value)}
                    />
                </label>
                <br />
                <label>
                    Enter Longitude:
                    <input
                        type="number"
                        value={longitude}
                        onChange={(e) => setLongitude(e.target.value)}
                    />
                </label>
                <br />
                <button type="submit">Calculate Distance</button>
            </form>
            <button onClick={handleAutomaticSubmit}>Use My Location</button>
            {distanceToSun !== null && (
                <p>Distance to Sun's core: {distanceToSun} kilometers</p>
            )}
        </div>
    );
};

export default SunDistanceCalculator;
