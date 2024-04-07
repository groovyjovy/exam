import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BookList from './BookList';
import BookForm from './BookForm';
import BookDetail from './BookDetail';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/books" element={<BookList />} />
          <Route path="/books/:id" element={<BookDetail />} />
          <Route path="/books/new" element={<BookForm mode="create" />} />
          <Route path="/books/:id/edit" element={<BookForm mode="edit" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
