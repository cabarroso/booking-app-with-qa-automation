import { useState, useEffect } from "react";
import API from "../api";
import { useNavigate } from "react-router-dom";



function BookingForm() {
    const navigate = useNavigate();

    useEffect(() => {
        if (!localStorage.getItem("token")) {
            navigate("/login");
        }
    }, []);
    
    const [form, setForm] = useState({
        firstname: "",
        lastname: "",
        totalprice: 0,
        depositpaid: false,
        checkin: "",
        checkout: "",
        additionalneeds: ""
    });
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;

        setForm({
            ...form,
            [name]: type === "checkbox" ? checked : value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const payload = {
            first_name: form.firstname,
            last_name: form.lastname,
            total_price: Number(form.totalprice),
            deposit_paid: form.depositpaid,
            check_in: form.checkin,
            check_out: form.checkout,
            additional_needs: form.additionalneeds
        };

        try {
            await API.post("/bookings", payload);
            setError(null)
            alert("Booking created!");
            navigate("/bookings")
        } catch (err) {
            setError(err.response?.data?.message || "unknown error");
        } finally {
            setLoading(false);
        }
    };

    return(<div>
            <h2>Create Booking</h2>
            <form onSubmit={handleSubmit}>
                <input name="firstname" onChange={handleChange} />
                <input name="lastname" onChange={handleChange} />
                <input name="totalprice" type="number" onChange={handleChange} />
                <label>
                    Deposit Paid
                    <input name="depositpaid" type="checkbox" onChange={handleChange} />
                </label>
                <input name="checkin" type="date" onChange={handleChange} />
                <input name="checkout" type="date" onChange={handleChange} />
                <input name="additionalneeds" onChange={handleChange} />

                <button type="submit" data-testid="submit-booking" disabled={loading}>
                    {loading ? "Creating..." : "Create Booking"}
                </button>
            </form>
            {error && <p data-testid="error-message">{error}</p>}
        </div>
    );
}

export default BookingForm;