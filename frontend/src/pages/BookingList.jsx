import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import API from "../api";



function BookingList() {

    const navigate = useNavigate();

    const [BookingList, setBookings] = useState([]);

    const fetchBookings = async () => {
        try {
            const response = await API.get("/bookings");
            setBookings(response.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        if (!localStorage.getItem("token")) {
            navigate("/login");
        }
        
        fetchBookings();
    }, []);

    const deleteBooking = async id => {
        try {
            await API.delete(`/bookings/${id}`);
            fetchBookings(); //refresh list
        } catch (err) {
            console.err(err);
        }
    };

    return (
        <div>
            <h2>Bookings</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Total Cost</th>
                        <th>Deposit Paid</th>
                        <th>Check In</th>
                        <th>Check Out</th>
                        <th>Additional Needs</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {BookingList.map(b => (
                        <tr className="booking" key={b.id} data-testid={`booking-row-${b.id}`}>
                            <td className="booking-id">{b.id}</td>
                            <td className="first-name">{b.first_name}</td>
                            <td className="last-name">{b.last_name}</td>
                            <td className="total-price">{b.total_price}</td>
                            <td className="deposit-paid">{b.deposit_paid.toString()}</td>
                            <td className="check-in">{b.check_in}</td>
                            <td className="check-out">{b.check_out}</td>
                            <td className="additional-needs">{b.additional_needs}</td>
                            <td>
                                <button onClick={() => deleteBooking(b.id)}>
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default BookingList;