import React, {useEffect, useState} from 'react';
import '../styles/UploadForm.css';
import {Link} from "react-router-dom";
import axios from "axios";

const UploadForm = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [resultData, setResultData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!selectedFile) {
            alert('Пожалуйста, сначала загрузите фото');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            setIsLoading(true);
            const response = await fetch('/upload/', {
                method: 'POST', body: formData,
            });

            if (!(response.ok)) {
                alert('Произошла ошибка при загрузке фотографии.');
                setIsLoading(false);
            } else {
                const data = await response.json();
                await getResultData(data.task_id);
            }
        } catch (error) {
            console.error('Error:', error);
            setIsLoading(false);
        }
    };

    const getResultData = async (task_id) => {
        try {
            const response = await fetch(`/result/${task_id}`, {
                method: 'GET',
            });

            if (response.ok) {
                const data = JSON.parse(await response.json());
                console.log("Received data from the server:", data);
                setResultData(data);
                setIsLoading(false);
            } else {
                alert('Произошла ошибка при получении результата.');
                setIsLoading(false);
            }
        } catch (error) {
            console.error('Error:', error);
            setIsLoading(false);
        }
    };


    const handleDownloadResult = async (task_id) => {
        try {
            const response = await fetch(`/download/${task_id}`, {
                method: 'GET',
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(new Blob([blob]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', `processed_${task_id}.jpg`);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } else if (response.status === 404) {
                alert('Результат обработки фотографии не найден.');
            } else {
                alert('Произошла ошибка при скачивании результата.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Произошла ошибка при скачивании результата.');
        }
    };


    useEffect(() => {
        if (selectedFile) {
            setResultData(null);
        }
    }, [selectedFile]);
    const handleLogout = async () => {
        try {
            const userEmail = localStorage.getItem('user_email');
            await axios.post(`/logout/?email=${userEmail}`);
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_email');
            window.location.href = '/';
        } catch (error) {
            console.error('Error logging out:', error);
        }
    };
    const isAuthenticated = localStorage.getItem('access_token');

    return (<div className="upload-container">
        <div className="nav">
            {isAuthenticated ? (<><a href="/photos" className="main-link">
                Ранее обработанные
            </a>
                <Link to="#" className="main-link" onClick={handleLogout}>Logout</Link> </>) : (<>
                <Link to="/login" className="main-link">Login</Link>
                <Link to="/signup" className="main-link">Signup</Link>
            </>)}
        </div>
        <div className="upload-form">
            <h2>Загрузить фотографию</h2>
            <form onSubmit={handleSubmit}>
                <div className="button-container form-buttons">
                    <label htmlFor="file-input" className="file-label">
                        Выберите файл
                        <input type="file" id="file-input" onChange={handleFileChange}/>
                    </label>
                    <button type="submit" className="upload-button">
                        Загрузить
                    </button>
                </div>
            </form>
            {selectedFile && <div className="selected-file-name">Выбранный файл: {selectedFile.name}</div>}
        </div>
        <div className="upload-result">
            <h2>Обработанный результат</h2>
            <div className="result-frame">
                {isLoading ? (<div className="loading-message">Обработка
                                                               фотографии...</div>) : resultData && resultData.result ? (

                    <img
                        className="result-image"
                        src={`data:image/jpeg;base64,${resultData.result}`}
                        alt="Обработанный результат"
                    />) : (<div className="upload-placeholder">Пожалуйста, загрузите фото</div>)}
            </div>
            {resultData && resultData.result && (
                <button className="save-button" onClick={() => handleDownloadResult(resultData.task_id)}>
                    Скачать результат
                </button>)}
        </div>
    </div>);
};

export default UploadForm;
