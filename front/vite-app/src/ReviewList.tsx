// src/ReviewListPage.tsx
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { List, ListItem, ListItemText, Button, Typography, Container } from '@mui/material';

interface Review {
  id: number;
  reviewer_name: string;
  content: string;
  rating: number;
}

const ReviewList = () => {
  const { bookId } = useParams<{ bookId: string }>();
  const [reviews, setReviews] = useState<Review[]>([]);

  useEffect(() => {
    if (bookId) {
      fetch(`http://localhost:8081/api/v1/books/${bookId}/reviews`)
        .then(response => response.json())
        .then(setReviews);
    }
  }, [bookId]);

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        レビュー一覧
      </Typography>
      <Button variant="contained" color="primary" component={Link} to={`/books/${bookId}/reviews/new`}>
        レビューを追加
      </Button>
      <List>
        {reviews.map(review => (
          <ListItem key={review.id} button component={Link} to={`/books/${bookId}/reviews/${review.id}`}>
            <ListItemText primary={review.reviewer_name} secondary={`${review.content.substring(0, 100)}...`} />
          </ListItem>
        ))}
      </List>
      <Button variant="outlined" color="secondary" component={Link} to={`/books/${bookId}`}>
        本の詳細に戻る
      </Button>
    </Container>
  );
};

export default ReviewList;
