// src/ReviewDetail.tsx
import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Card, CardContent, Typography, Container, Box, Button } from '@mui/material';

interface Review {
  id: number;
  reviewer_name: string;
  content: string;
  rating: number;
}

const ReviewDetail = () => {
  const { bookId, reviewId } = useParams<{ bookId: string, reviewId: string }>();
  const navigate = useNavigate();
  const [review, setReview] = useState<Review | null>(null);

  useEffect(() => {
    if (bookId && reviewId) {
      fetch(`http://localhost:8081/api/v1/books/${bookId}/reviews/${reviewId}`)
        .then(response => response.json())
        .then(setReview);
    }
  }, [bookId, reviewId]);

  const handleDelete = () => {
    if (bookId && reviewId) {
      fetch(`http://localhost:8081/api/v1/books/${bookId}/reviews/${reviewId}`, {
        method: 'DELETE',
      }).then(() => navigate(`/books/${bookId}/reviews`));
    }
  };

  if (!review) return <Typography>Loading...</Typography>;

  return (
    <Container maxWidth="sm">
      <Box my={4}>
        <Card raised>
          <CardContent>
            <Typography variant="h4" component="h2" gutterBottom>
              {review.reviewer_name}'s Review
            </Typography>
            <Typography variant="body1" component="p" style={{ marginTop: '16px' }}>
              {review.content}
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              Rating: {review.rating}
            </Typography>
            <Box mt={2}>
              <Button variant="contained" color="primary" component={Link} to={`/books/${bookId}/reviews/${reviewId}/edit`}>
                編集
              </Button>
              <Button variant="contained" color="secondary" onClick={handleDelete} style={{ marginLeft: '16px' }}>
                削除
              </Button>
              <Button variant="outlined" color="secondary" component={Link} to={`/books/${bookId}/reviews`} style={{ marginLeft: '16px' }}>
                レビュー一覧に戻る
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default ReviewDetail;
