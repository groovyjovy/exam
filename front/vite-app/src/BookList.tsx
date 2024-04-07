import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardActions, Button, Typography, Grid, Container } from '@mui/material';

interface Book {
  id: number;
  title: string;
  author: string;
}

const BookList = () => {
  const [books, setBooks] = useState<Book[]>([]);

  useEffect(() => {
    fetch('http://localhost:8081/books')
      .then(response => response.json())
      .then(data => setBooks(data));
  }, []);

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom style={{ marginTop: '20px' }}>
        本の一覧
      </Typography>
      <Button variant="contained" color="primary" component={Link} to="/books/new" style={{ marginBottom: '20px' }}>
        新規登録
      </Button>
      <Grid container spacing={3}>
        {books.map(book => (
          <Grid item key={book.id} xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="h2">
                  {book.title}
                </Typography>
                <Typography color="textSecondary">
                  著者: {book.author}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" color="primary" component={Link} to={`/books/${book.id}`}>
                  詳細を見る
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default BookList;
