import React, { useState } from 'react';
import api from '../services/api';
import BookCard from './BookCard';
import { Form, Button, Alert, Spinner, Row, Col } from 'react-bootstrap';

export default function Recommender() {
  const [query, setQuery] = useState('');
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const getRecommendations = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError('');
    console.log("recommendations called!")
    console.log(books)
    
    try {
      // const {data } = 
      const {books} = await api.getRecommendations(query);
      console.log(books);

      setBooks(Array.isArray(books) ? books : []);
    } catch (err) {
      console.log(err)
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') getRecommendations();
  };

  return (
    <div className="mb-5">
      <Form.Group className="mb-3">
        <Form.Label><h4>Find Similar Books</h4></Form.Label>
        <div className="d-flex gap-2">
          <Form.Control
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter a book title..."
            disabled={loading}
          />
          <Button 
            variant="primary" 
            onClick={getRecommendations}
            disabled={loading || !query.trim()}
          >
            {loading ? <Spinner size="sm" /> : 'Search'}
          </Button>
        </div>
      </Form.Group>

      {error && <Alert variant="danger" dismissible onClose={() => setError('')}>{error}</Alert>}

      <Row xs={1} md={2} lg={3} className="g-4">
        {books.map((book, index) => (
          <Col key={`${book.title}-${index}`}>
            <BookCard book={book} />
            <h1>Hello</h1>
          </Col>
        ))}
      </Row>
    </div>
  );
}