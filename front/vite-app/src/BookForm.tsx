// src/BookForm.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { TextField, Button, Container, Typography, Box, Card, CardContent } from '@mui/material';

interface BookFormProps {
  mode: 'create' | 'edit';
}

const BookForm = ({ mode }: BookFormProps) => {
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [price, setPrice] = useState('');
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();

  useEffect(() => {
    if (mode === 'edit') {
      fetch(`http://localhost:8081/api/v1/books/${id}`)
        .then(response => response.json())
        .then(data => {
          setTitle(data.title);
          setAuthor(data.author);
          setPrice(data.price.toString());
        });
    }
  }, [id, mode]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const bookData = { title, author, price: Number(price) };

    const endpoint = mode === 'create' ? 'http://localhost:8081/api/v1/books' : `http://localhost:8081/api/v1/books/${id}`;
    const method = mode === 'create' ? 'POST' : 'PUT';

    fetch(endpoint, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ book: bookData }),
    }).then(response => {
      if (response.ok) {
        navigate('/books');
      } else {
        alert('Failed to process book');
      }
    });
  };

  return (
    <Container maxWidth="sm">
      <Box my={4}>
        <Card raised>
          <CardContent>
            <Typography variant="h4" component="h1" gutterBottom>
              {mode === 'create' ? '新規登録' : '本の編集'}
            </Typography>
            <form onSubmit={handleSubmit}>
              <TextField
                label="タイトル"
                fullWidth
                margin="normal"
                value={title}
                onChange={e => setTitle(e.target.value)}
              />
              <TextField
                label="著者"
                fullWidth
                margin="normal"
                value={author}
                onChange={e => setAuthor(e.target.value)}
              />
              <TextField
                label="価格"
                fullWidth
                margin="normal"
                type="number"
                value={price}
                onChange={e => setPrice(e.target.value)}
              />
              <Box mt={2}>
                <Button type="submit" color="primary" variant="contained">
                  {mode === 'create' ? '登録' : '更新'}
                </Button>
                <Button variant="outlined" component={Link} to="/books" style={{ marginLeft: '16px' }}>
                  一覧に戻る
                </Button>
              </Box>
            </form>
          </CardContent>
        </Card>  
      </Box>
    </Container>
  );
};

export default BookForm;
