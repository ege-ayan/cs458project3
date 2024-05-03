import React, { useState } from 'react';
import axios from 'axios';
import './DistanceToSun.css';
import { useNavigate } from 'react-router-dom';

const DistanceToSun = () => {
    const [latitude, setLatitude] = useState('');
    const [longitude, setLongitude] = useState('');
    const [sunDistance, setSunDistance] = useState(null);
    const navigate = useNavigate();

    const fetchSunDistance = (lat, long) => {
        axios.get(`https://api.ipgeolocation.io/astronomy?apiKey=8120a83825cb46159d19d052c86f78dc&lat=${lat}&long=${long}`)
            .then(response => {
                const { sun_distance } = response.data;
                setSunDistance(sun_distance);

            })
            .catch(error => {
                alert('Error fetching astronomical data:', error);
                alert('Failed to fetch data. Please check your inputs and try again.');
            });
    };

    const handleManualSubmit = () => {
        if (!latitude || !longitude) {
            alert('Please enter both latitude and longitude.');
            return;
        }
        fetchSunDistance(latitude, longitude);
    };

    const handleGPSSubmit = () => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                fetchSunDistance(position.coords.latitude, position.coords.longitude);
            },
            (error) => {
                console.error('Error getting user coordinates:', error);
                alert('GPS access denied. Please enable GPS or enter coordinates manually.');
            }
        );
    };

    const goToSecondPage = () => {
        navigate('/nearest-sea');
    };

    return (
        <div className="sun-container">

            <div>
                <h1 className="title">Distance to Sun's Core Calculator</h1>

            </div>

            <div className="inputs">
                <input
                    type="text"
                    placeholder="Latitude"
                    value={latitude}
                    onChange={(e) => setLatitude(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Longitude"
                    value={longitude}
                    onChange={(e) => setLongitude(e.target.value)}
                />
                <button onClick={handleManualSubmit}>Calculate</button>
            </div>
            <div className="gps-button">
                <button onClick={handleGPSSubmit}>Calculate from GPS</button>
            </div>
            <div className="result">
                {sunDistance && (
                    <p>Your distance to the Sun: {sunDistance} kilometers</p>
                )

                }
                {
                    !sunDistance && (
                        <p>Enter your position or use GPS to Calculate!</p>
                    )
                }

            </div>

            <button onClick={goToSecondPage} className="navigate-button">
                Find the Nearest Sea
            </button>


        </div>
    );
};

export default DistanceToSun;
