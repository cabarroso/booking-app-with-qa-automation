import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import BookingList from "./pages/BookingList";
import BookingForm from "./pages/BookingForm";

function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/bookings" element={<BookingList />} />
      <Route path="/create" element={<BookingForm />} />
    </Routes>
    </BrowserRouter>
  )
}

export default App;