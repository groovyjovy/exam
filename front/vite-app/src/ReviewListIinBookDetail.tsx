// src/ReviewList.tsx
import { Link } from 'react-router-dom';
import { List, ListItem, ListItemText, Button, Typography } from '@mui/material';

interface Review {
  id: number;
  reviewer_name: string;
  content: string;
  rating: number;
}

interface ReviewListProps {
  reviews: Review[];
  bookId: string;
}

const ReviewListinBookDetail = ({ reviews, bookId }: ReviewListProps) => {
  const safeReviews = reviews || [];

  return (
    <div>
      <Typography variant="h6" gutterBottom>
        レビュー
      </Typography>
      <List>
        {safeReviews.slice(0, 3).map(review => (
          <ListItem key={review.id}>
            <ListItemText primary={review.reviewer_name} secondary={`${review.content.substring(0, 100)}`} />
          </ListItem>
        ))}
      </List>
      {
        <Button component={Link} to={`/books/${bookId}/reviews`}>
          レビュー一覧を見る
        </Button>
      }
    </div>
  );
};

export default ReviewListinBookDetail;
