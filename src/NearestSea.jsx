import React, { useState, useEffect } from 'react';
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';
import ClipLoader from "react-spinners/ClipLoader";
import './NearestSea.css';
import { useNavigate } from 'react-router-dom';
import markerIconPng from "leaflet/dist/images/marker-icon.png"
import 'leaflet/dist/leaflet.css';

const icon = new L.Icon({
    iconUrl: markerIconPng,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    shadowSize: [41, 41]
});

const NearestSea = () => {
    const [currentPosition, setCurrentPosition] = useState(null);
    const [nearestSea, setNearestSea] = useState(null);
    const [seaName, setSeaName] = useState("");
    const [distanceToSea, setDistanceToSea] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const success = (position) => {
            const { latitude, longitude } = position.coords;
            setCurrentPosition([latitude, longitude]);

            const radius = 600000;
            const query = `[out:json][timeout:25];
                (
                    node["place"="sea"](around:${radius},${latitude},${longitude});
                    way["place"="sea"](around:${radius},${latitude},${longitude});
                    relation["place"="sea"](around:${radius},${latitude},${longitude});
                );
                out center;`;

            setLoading(true);
            fetch(`https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    setLoading(false);
                    const nearestSeaNode = data.elements.reduce((nearest, sea) => {
                        const seaLat = sea.center ? sea.center.lat : sea.lat;
                        const seaLon = sea.center ? sea.center.lon : sea.lon;
                        const seaDistance = L.latLng(latitude, longitude).distanceTo(L.latLng(seaLat, seaLon));
                        return !nearest || seaDistance < nearest.distance ? { sea, distance: seaDistance } : nearest;
                    }, null);

                    if (nearestSeaNode) {
                        const { sea, distance } = nearestSeaNode;
                        const lat = sea.center ? sea.center.lat : sea.lat;
                        const lon = sea.center ? sea.center.lon : sea.lon;
                        setNearestSea([lat, lon]);
                        setSeaName(sea.tags.name || 'Unnamed Sea');
                        setDistanceToSea(distance);
                    }
                })
                .catch(error => {
                    setLoading(false);
                    console.error('Error fetching nearest sea:', error);
                });
        };

        const error = () => alert('Error getting current position. Please permit location information and refresh the page.');

        navigator.geolocation && navigator.geolocation.getCurrentPosition(success, error);
    }, []);

    const goToThirdPage = () => {
        navigate('/sun');
    };

    if (!currentPosition || loading) {
        return (
            <div className="full-center">
                <ClipLoader color="#123abc" loading={loading} size={150} />
                <p>Loading...</p>
            </div>
        );
    }

    return (
        <div className="container" >
            <div style={{ height: '20px', }} />

            <MapContainer center={currentPosition} zoom={6} style={{ height: '500px', margin: '0px 50px', borderRadius: '30px', paddingTop: '20px' }}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={currentPosition} icon={icon}>
                    <Popup>You are here</Popup>
                </Marker>
                {nearestSea && (
                    <>
                        <Marker position={nearestSea} icon={icon}>
                            <Popup>{`Nearest Sea: ${seaName}`}</Popup>
                        </Marker>
                        <Polyline positions={[currentPosition, nearestSea]} color="blue" />
                    </>
                )}
            </MapContainer>

            <div className="sea-name">
                Nearest Sea: {seaName} {distanceToSea !== null && (
                    <span>({(distanceToSea / 1000).toFixed(2)} km away)</span>
                )}
            </div>

            <button onClick={goToThirdPage} className="navigate-button">
                Calculate Distance to Core of the Sun
            </button>

        </div>
    );
};

export default NearestSea;
