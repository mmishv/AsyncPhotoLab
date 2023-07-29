import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import PhotoList from './components/PhotoList';
import UploadForm from './components/UploadForm';

const App = () => {
    return (<Router>
            <div>
                <Routes>
                    <Route path="/" element={<UploadForm/>}/>
                    <Route path="/photos" element={<PhotoList/>}/>
                </Routes>
            </div>
        </Router>);
};

export default App;