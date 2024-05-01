import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SunDistanceCalculator = () => {
    const [coordinates, setCoordinates] = useState(null);
    const [sunDistance, setSunDistance] = useState(null);

    useEffect(() => {
        // Get user's coordinates
        navigator.geolocation.getCurrentPosition(
            (position) => {
                setCoordinates({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
            },
            (error) => {
                console.error('Error getting user coordinates:', error);
            }
        );
    }, []);

    useEffect(() => {
        if (coordinates) {
            axios.get(`https://api.ipgeolocation.io/astronomy?apiKey=8120a83825cb46159d19d052c86f78dc&lat=${coordinates.latitude}&long=${coordinates.longitude}`)
                .then(response => {

                    const { sun_distance } = response.data;
                    setSunDistance(sun_distance);
                })
                .catch(error => {
                    console.error('Error fetching astronomical data:', error);
                });
        }
    }, [coordinates]);

    return (
        <div>
            {sunDistance && (
                <p>Your distance to the Sun: {sunDistance} kilometers</p>
            )}
        </div>
    );
};

export default SunDistanceCalculator;
