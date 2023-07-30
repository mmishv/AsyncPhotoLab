import React, {useEffect, useState} from 'react';
import '../styles/PhotoList.css';

const PhotoList = () => {
    const [photos, setPhotos] = useState([]);

    useEffect(() => {
        fetch('/photos/processed/')
            .then(response => response.json())
            .then(data => setPhotos(JSON.parse(data)))
            .catch(error => console.error('Error:', error));
    }, []);

    return (<div className="photo-list">
        <div className="photo-list-header">
            <h2>Обработанные фотографии</h2>
            <a href="/" className="home-link">На главную</a>
        </div>
        <div className="photo-grid">
            {photos.map((photo) => (<div className="photo-card" key={photo.id}>
                <img src={`data:image/jpeg;base64,${photo.photo_bytes}`} alt={`Processed-${photo.id}`}/>
                <div className="date">Дата добавления: {photo.timestamp}</div>
            </div>))}
        </div>
    </div>);
};

export default PhotoList;
