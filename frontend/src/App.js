import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import PhotoList from './components/PhotoList';
import UploadForm from './components/UploadForm';
import Login from "./components/Login";
import Signup from "./components/Signup";

const App = () => {
    return (<Router>
        <div>
            <Routes>
                <Route path="/" element={<UploadForm/>}/>
                <Route path="/photos" element={<PhotoList/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/signup" element={<Signup/>}/>
            </Routes>
        </div>
    </Router>);
};

export default App;