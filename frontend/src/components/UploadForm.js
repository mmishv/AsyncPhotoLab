import React, {useState} from 'react';

const UploadForm = () => {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('/upload/', {
                method: 'POST', body: formData,
            });
            if (response.ok) {
                alert('Фотография успешно загружена и поставлена в очередь на обработку.');
            } else {
                alert('Произошла ошибка при загрузке фотографии.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (<div>
            <h2>Загрузить фотографию</h2>
            <form onSubmit={handleSubmit}>
                <input type="file" name="file" onChange={handleFileChange}/>
                <button type="submit">Загрузить</button>
            </form>
        </div>);
};

export default UploadForm;
