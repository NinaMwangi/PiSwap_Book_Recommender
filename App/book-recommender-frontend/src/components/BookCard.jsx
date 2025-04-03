import React from 'react';
import { Card } from 'react-bootstrap';
import { faBookOpen } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';


export default function BookCard({ book }) {
  return (
    <Card className="h-100 shadow-sm">
      {book.image_url ? (
        <Card.Img 
          variant="top" 
          src={book.image_url} 
          alt={book.title}
          className="book-cover"
        />
      ) : (
        <div className="text-center p-4 bg-light">
          {/* <FontAwesomeIcon 
            icon={faBookOpen} 
            size="4x" 
            className="text-muted" 
          /> */}
          <img src={book.metadata.image_url} alt="" />
        </div>
      )}
      <Card.Body className="d-flex flex-column">
        <Card.Title className="text-truncate">{book.title}</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">
          {book.metadata.author || 'Unknown Author'}
        </Card.Subtitle>
        <Card.Text className="mt-auto">
          <small className="text-muted">
            {book.publisher && `${book.publisher} • `}
            {book.year || ''}
          </small>
        </Card.Text>
        
      </Card.Body>
    </Card>
  );
}