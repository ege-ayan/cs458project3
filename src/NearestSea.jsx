import React, { useState, useEffect } from 'react';
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet'; // Import Leaflet for distance calculation

const NearestSea = () => {
    const [currentPosition, setCurrentPosition] = useState(null);
    const [nearestSea, setNearestSea] = useState(null);
    const [seaName, setSeaName] = useState(""); // State to store the name of the nearest sea
    const [loading, setLoading] = useState(true); // State to track loading state

    useEffect(() => {
        const success = (position) => {
            const { latitude, longitude } = position.coords;
            setCurrentPosition([latitude, longitude]);

            const radius = 600000; // 600 km radius to search for seas
            const query = `[out:json][timeout:25];
                (
                    node["place"="sea"](around:${radius},${latitude},${longitude});
                    way["place"="sea"](around:${radius},${latitude},${longitude});
                    relation["place"="sea"](around:${radius},${latitude},${longitude});
                );
                out center;`;

            setLoading(true); // Set loading state to true when fetching data

            fetch(`https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    setLoading(false); // Set loading state to false when data is fetched
                    if (data.elements && data.elements.length > 0) {
                        // Filter the nearest sea
                        const nearestSeaNode = data.elements.reduce((nearest, sea) => {
                            const seaLat = sea.center ? sea.center.lat : sea.lat;
                            const seaLon = sea.center ? sea.center.lon : sea.lon;
                            const seaDistance = L.latLng(latitude, longitude).distanceTo(L.latLng(seaLat, seaLon));
                            if (!nearest || seaDistance < nearest.distance) {
                                return { sea, distance: seaDistance };
                            }
                            return nearest;
                        }, null);

                        if (nearestSeaNode) {
                            const { sea } = nearestSeaNode;
                            const lat = sea.center ? sea.center.lat : sea.lat;
                            const lon = sea.center ? sea.center.lon : sea.lon;
                            setNearestSea([lat, lon]);
                            setSeaName(sea.tags.name || 'Unnamed Sea');
                            console.log("Nearest Sea Name:", sea.tags.name); // Log the name of the sea
                        }
                    } else {
                        console.log("No sea found within the given radius.");
                    }
                })
                .catch(error => {
                    setLoading(false); // Set loading state to false on error
                    console.error('Error fetching nearest sea:', error);
                });
        };

        const error = () => {
            console.error('Error getting current position');
        };

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(success, error);
        } else {
            console.error('Geolocation is not supported by this browser');
        }
    }, []);

    if (!currentPosition || loading) {
        // Show loading indicator while fetching data
        return (
            <div style={{ textAlign: 'center' }}>
                <p>Loading...</p>
            </div>
        );
    }

    const mapCenter = currentPosition;

    return (
        <div>
            <MapContainer center={mapCenter} zoom={5} style={{ height: '400px' }}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {currentPosition && (
                    <Marker position={currentPosition}>
                        <Popup>You are here</Popup>
                    </Marker>
                )}
                {nearestSea && (
                    <>
                        <Marker position={nearestSea}>
                            <Popup>{`Nearest Sea: ${seaName}`}</Popup>
                        </Marker>
                        <Polyline positions={[currentPosition, nearestSea]} color="blue" />
                    </>
                )}
            </MapContainer>
            <div style={{ textAlign: 'center', marginTop: '10px', fontSize: '18px', fontWeight: 'bold' }}>
                Nearest Sea: {seaName}
            </div>
        </div>
    );
};

export default NearestSea;
