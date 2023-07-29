import React, {useState} from 'react';


const PhotoList = () => {
    const [photos, setPhotos] = useState([]);
    return (<div>
            <h2>Обработанные фотографии</h2>
            <ul>
                {photos.map((photo) => (<li key={photo.id}>
                        <img src={photo.url} alt={`Processed-${photo.id}`}/>
                    </li>))}
            </ul>
        </div>);
};

export default PhotoList;
