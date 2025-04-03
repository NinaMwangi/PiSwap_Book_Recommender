import React from 'react';
import Recommender from './components/Recommender';
import Uploader from './components/Uploader';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

export default function App() {
  return (
    <div className="container py-4">
      <h1 className="text-center mb-5">Book Recommender System</h1>
      <Uploader />
      <Recommender />
    </div>
  );
}