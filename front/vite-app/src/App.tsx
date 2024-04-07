import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BookList from './BookList';
import BookDetail from './BookDetail';
import BookForm from './BookForm';
import ReviewList from './ReviewList'
import ReviewDetail from './ReviewDetail';
import ReviewForm from './ReviewForm';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/books" element={<BookList />} />
          <Route path="/books/new" element={<BookForm mode="create" />} />
          <Route path="/books/:id" element={<BookDetail />} />
          <Route path="/books/:id/edit" element={<BookForm mode="edit" />} />
          <Route path="/books/:bookId/reviews" element={<ReviewList />} />
          <Route path="/books/:bookId/reviews/new" element={<ReviewForm mode="create" />} />
          <Route path="/books/:bookId/reviews/:reviewId" element={<ReviewDetail />} />
          <Route path="/books/:bookId/reviews/:reviewId/edit" element={<ReviewForm mode="edit" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
