
import React, { useState, useContext, useEffect } from 'react';
import { FaFileVideo } from "react-icons/fa6";
import "./Option.css"
import { Form, Button,InputGroup } from 'react-bootstrap';
function LocalFileBox({ onClick, isSelected,goBack }) {


    if (isSelected==true) {
        return (
            <div className='localFileSelected'>
                <h3 style={{marginTop:"1em"}}>Transcreva Videos do seu computador</h3 >
              <FileUploadForm />
                <div onClick={goBack}>Voltar </div>
            </div>
        );
    }


    return (
        <div onClick={onClick}  className='localfile box'>
           <div className='title'>
            Escolha um arquivo do seu computador
           </div>
           <div className='icon-box'>
                <FaFileVideo></FaFileVideo>
            </div>
        </div>
    );
}
function FileUploadForm() {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        console.log('Selected file:', e.target.files[0]);
    };  
    const [selectedLanguage, setSelectedLanguage] = useState('');
    const [translateToEnglish, setTranslateToEnglish] = useState(false);

    const handleLanguageChange = (e) => {
        setSelectedLanguage(e.target.value);
    };

    const handleTranslateChange = (e) => {
        setTranslateToEnglish(e.target.checked);
    };

   

    const handleSubmit = (e) => {
        e.preventDefault();
        if (file) {
            console.log('Uploading file:', file);
            // call backend here
        }
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formFile">
                <Form.Label>Escolha um arquivo</Form.Label>
                <InputGroup>
                    <Form.Control type="file" onChange={handleFileChange} />
                    <Button variant="primary" type="submit" disabled={!file}>
                        Upload
                    </Button>
                </InputGroup>
            </Form.Group>
                   
            <Form.Group controlId="formLanguage">
                    <Form.Label>Select Language</Form.Label>
                    <Form.Control as="select" value={selectedLanguage} onChange={handleLanguageChange}>
                        <option value="">Selecione a linguagem</option>
                        <option value="pt">Portuguese</option>
                        <option value="pt"> Ojibwa</option>
                        <option value="en">English</option>
                        <option value="fr">French</option>
                        <option value="es">Spanish</option>
                        <option value="de">German</option>
                        <option value="it">Italian</option>
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId="formTranslate">
                    <Form.Check type="checkbox" label="Traduzir para ingles" checked={translateToEnglish} onChange={handleTranslateChange} />
                </Form.Group>
        </Form>
    );
}

export default LocalFileBox;