import React, { useState } from 'react';
import api from '../services/api';
import { Button, Alert, Spinner, ProgressBar } from 'react-bootstrap';

export default function Uploader({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState({ text: '', variant: 'success' });
  const [isLoading, setIsLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    
    setIsLoading(true);
    setMessage({ text: '', variant: 'success' });
    
    try {
     const response =  await api.uploadCSV(file, (progressEvent) => {
        const percent = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setProgress(percent);
      });
      
      setMessage({ 
        text: `<div>Data uploaded successfully!</div>
        Retraining started... <br/>
        New records: ${response.data.new_records} <br/>
        Total records: ${response.data.total_records} <br/>
        Duplicates removed: ${response.data.duplicates_removed}`, 
        variant: 'success' 
      });
      onUploadComplete?.();
    } catch (err) {
      setMessage({ 
        text: err.message, 
        variant: 'danger' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mb-5 p-3 border rounded">
      <h4 className="mb-3">Upload New Book Data</h4>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-3 form-control"
        disabled={isLoading}
      />
      
      <div className="d-flex align-items-center gap-2">
        <Button
          variant="success"
          onClick={handleUpload}
          disabled={!file || isLoading}
        >
          {isLoading ? (
            <>
              <Spinner size="sm" className="me-2" />
              Uploading...
            </>
          ) : 'Upload CSV'}
        </Button>
        
        {progress > 0 && progress < 100 && (
          <ProgressBar 
            now={progress} 
            label={`${progress}%`} 
            style={{ flex: 1 }} 
          />
        )}
      </div>
      
      {message.text && (
        <Alert variant={message.variant} className="mt-3" >
          <div dangerouslySetInnerHTML={{ __html: message.text }} />
        </Alert>
      )}
    </div>
  );
}