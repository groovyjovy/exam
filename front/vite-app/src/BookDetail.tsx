// src/BookDetail.tsx
import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Card, CardContent, Typography, Container, Box, Button } from '@mui/material';
import ReviewListInBookDetail from './ReviewListIinBookDetail';

interface Book {
  id: number;
  title: string;
  author: string;
  price: number;
}

interface Review {
  id: number;
  reviewer_name: string;
  content: string;
  rating: number;
}

const BookDetail = () => {
  const { id } = useParams<{ id: string }>();
  const [book, setBook] = useState<Book | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`http://localhost:8081/api/v1/books/${id}`)
      .then(response => response.json())
      .then(data => setBook(data));

    fetch(`http://localhost:8081/api/v1/books/${id}/reviews`)
      .then(response => response.json())
      .then(data => setReviews(data));
  }, [id]);

  const handleDelete = () => {
    fetch(`http://localhost:8081/api/v1/books/${id}`, {
      method: 'DELETE',
    }).then(() => navigate('/books'));
  };

  if (!id) return <Typography>Book ID is undefined.</Typography>;
  if (!book) return <Typography>Loading...</Typography>;

  return (
    <Container maxWidth="sm">
      <Box my={4}>
        <Card raised>
          <CardContent>
            <Typography variant="h4" component="h2" gutterBottom>
              {book.title}
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              著者: {book.author}
            </Typography>
            <Typography variant="body1" component="p" style={{ marginTop: '16px' }}>
              価格: ${book.price}
            </Typography>

            <ReviewListInBookDetail reviews={reviews} bookId={id} />

            <Box mt={2}>
              <Button variant="contained" color="primary" component={Link} to={`/books/${book.id}/edit`}>
                編集
              </Button>
              <Button variant="contained" color="secondary" onClick={handleDelete} style={{ marginLeft: '16px' }}>
                削除
              </Button>
              <Button variant="outlined" component={Link} to="/books" style={{ marginLeft: '16px' }}>
                一覧に戻る
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default BookDetail;
