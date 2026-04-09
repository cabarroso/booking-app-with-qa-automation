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
    const [errors, setErrors] = useState({});
    const [apiError, setApiError] = useState(null)
    const [loading, setLoading] = useState(false);

    // Field level validation
    const validateField = (name, value) => {
        let error = "";

        if (name === "firstname" && !value.trim()) {
            error = "First name is required";
        }

        if (name === "lastname" && !value.trim()) {
            error = "Last name is required";
        }

        if (name === "totalprice") {
            if (value === "") error = "Price is required";
            else if (isNaN(value)) error = "Must be a number";
            else if (Number(value) < 0) error = "Cannot be negative";
        }

        if (name === "checkin" && !value) {
            error = "Check-in date required";
        }

        if (name === "checkout" && !value) {
            error = "Check-out date required";
        }

        return error
    };

    // Form-level validation (cross-field logic)
    const validateForm = () => {
        let newErrors = {};

        Object.keys(form).forEach(key => {
            const error = validateField(key, form[key]);
            if (error) newErrors[key] = error
        });

        // Cross-field validation
        if (form.checkin && form.checkout) {
            if (new Date(form.checkout) < new Date(form.checkin)) {
                newErrors.checkout = "Checkout cannot be before check-in";
            }
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = e => {
        const { name, value, type, checked } = e.target;

        const newValue = type === "checkbox" ? checked : value

        setForm({
            ...form,
            [name]: newValue
        });

        // Validate on change (instant feedback)
        const error = validateField(name, newValue);

        setErrors({
            ...errors,
            [name]: error
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Block submission if invalid
        if (!validateForm()) return;

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
            setApiError(null)
            alert("Booking created!");
            navigate("/bookings")
        } catch (err) {
            setApiError(err.response?.data?.message || "Unknown error");
        } finally {
            setLoading(false);
        }
    };

    return(<div>
            <h2>Create Booking</h2>
            <form onSubmit={handleSubmit}>

                <label htmlFor="firstname">First Name</label>
                <input id="firstname" name="firstname" onChange={handleChange} />
                {errors.firstname && <p>{errors.firstname}</p>}

                <label htmlFor="lastname">Last Name</label>
                <input id="lastname" name="lastname" onChange={handleChange} />
                {errors.lastname && <p>{errors.lastname}</p>}

                <label htmlFor="totalprice">Total Price</label>
                <input id="totalprice" name="totalprice" type="number" onChange={handleChange} />
                {errors.totalprice && <p>{errors.totalprice}</p>}

                <label>
                    Deposit Paid
                    <input id="depositpaid" name="depositpaid" type="checkbox" onChange={handleChange} />
                </label>

                <label htmlFor="checkin">Check In</label>
                <input id="checkin" name="checkin" type="date" onChange={handleChange} />
                {errors.checkin && <p>{errors.checkin}</p>}

                <label htmlFor="checkout">Check Out</label>
                <input id="checkout" name="checkout" type="date" onChange={handleChange} />
                {errors.checkout && <p>{errors.checkout}</p>}

                <label htmlFor="additionalneeds">Additional Needs</label>
                <input id="additionalneeds" name="additionalneeds" onChange={handleChange} />

                <button type="submit" data-testid="submit-booking" disabled={loading}>
                    {loading ? "Creating..." : "Create Booking"}
                </button>
            </form>
            {apiError && <p data-testid="error-message">{apiError}</p>}
        </div>
    );
}

export default BookingForm;