import React from 'react';
import ReactDOM from 'react-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import App from './App';
import './index.css'

ReactDOM.render(
    <GoogleOAuthProvider clientId="810708335744-6b9l170hisc5nmbi32uao7r5gb8fqm7a.apps.googleusercontent.com">
        <React.StrictMode>
            <App/>
        </React.StrictMode>
    </GoogleOAuthProvider>,
    document.getElementById('root')
);