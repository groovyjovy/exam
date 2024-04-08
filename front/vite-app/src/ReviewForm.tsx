// src/ReviewForm.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { TextField, Button, Container, Typography, Box } from '@mui/material';

interface ReviewFormProps {
  mode: 'create' | 'edit';
}

const ReviewForm = ({ mode }: ReviewFormProps) => {
  const [reviewer_name, setReviewerName] = useState('');
  const [content, setContent] = useState('');
  const [rating, setRating] = useState('');
  const navigate = useNavigate();
  const { bookId, reviewId } = useParams<{ bookId: string, reviewId?: string }>();

  useEffect(() => {
    if (mode === 'edit' && reviewId) {
      fetch(`http://localhost:8081/api/v1/books/${bookId}/reviews/${reviewId}`)
        .then(response => response.json())
        .then(data => {
          setReviewerName(data.reviewer_name);
          setContent(data.content);
          setRating(data.rating.toString());
        });
    }
  }, [bookId, reviewId, mode]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const reviewData = { reviewer_name, content, rating: Number(rating) };
    const endpoint = mode === 'create' ? `http://localhost:8081/api/v1/books/${bookId}/reviews` : `http://localhost:8081/api/v1/books/${bookId}/reviews/${reviewId}`;
    const method = mode === 'create' ? 'POST' : 'PUT';

    fetch(endpoint, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ review: reviewData }),
    }).then(response => {
      if (response.ok) {
        navigate(`/books/${bookId}/reviews`);
      } else {
        alert('Failed to process review');
      }
    });
  };

  return (
    <Container maxWidth="sm">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          {mode === 'create' ? 'レビューを追加' : 'レビューを編集'}
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="レビュアー名"
            fullWidth
            margin="normal"
            value={reviewer_name}
            onChange={e => setReviewerName(e.target.value)}
          />
          <TextField
            label="内容"
            fullWidth
            margin="normal"
            value={content}
            onChange={e => setContent(e.target.value)}
          />
          <TextField
            label="評価"
            fullWidth
            margin="normal"
            type="number"
            value={rating}
            onChange={e => setRating(e.target.value)}
          />
          <Box mt={2}>
            <Button type="submit" color="primary" variant="contained">
              {mode === 'create' ? '登録' : '更新'}
            </Button>
            <Button variant="outlined" component={Link} to={`/books/${bookId}/reviews`} style={{ marginLeft: '16px' }}>
              キャンセル
            </Button>
          </Box>
        </form>
      </Box>
    </Container>
  );
};

export default ReviewForm;
