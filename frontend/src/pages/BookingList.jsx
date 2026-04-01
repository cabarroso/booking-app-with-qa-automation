import { useNavigate } from "react-router-dom";



function BookingList() {
    const navigate = useNavigate();

    if (!localStorage.getItem("token")) {
        navigate("/login")
    }

    return <h1>Booking List</h1>
}

export default BookingList;