import streamlit as st
import streamlit.components.v1 as components

# HTML, CSS, and JavaScript for the registration form
form_html = """
<style>
   @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans&display=swap');
    body, h2, label, input, select, button {
        font-family: 'Josefin Sans', sans-serif;
    }
    .form-container {
        max-width: 800px;
        padding: 20px;
        border-radius: 8px;
        color: #981AD3FF;
        box-shadow: 0px 0px 10px #aaa;
        background:#E2ECF0FF;
        margin: auto;
    }
    h2{
      text-align: center;
    }
    input, select {
        width: 100%;
        padding: 8px;
        margin: 8px 0;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .btn {
        width: 100%;
        padding: 10px;
        margin: 8px 0;
        background: #981AD3FF;
        color: white;
        border: none;
        cursor: pointer;
        border-radius: 10px;
    }
    .btn:hover {
        background: #7208A3FF;;
    }
    .error { color: black; font-size: 12px; }
</style>

<div class="form-container">
    <h2>Create an account</h2>
    <form id="registerForm" onsubmit="return validateForm()" method="post">
        <label>First Name:</label>
        <input type="text" id="first_name" placeholder="Enter your first name" required>

        <label>Last Name:</label>
        <input type="text" id="last_name" placeholder="Enter your last name" required>

        <label>Username:</label>
        <input type="text" id="username" placeholder="Choose a username" required>
       
        <label>Identifier:</label>
        <input type="text" id="identifier" placeholder="Enter your identifier" required>
    
        <label>Password:</label>
        <input type="password" id="password" placeholder="Enter a strong password" required>

        <label>Confirm Password:</label>
        <input type="password" id="confirm_password" placeholder="Re-enter password" required>
        <p class="error" id="error_msg"></p>
        
        <label>Email:</label>
        <input type="email" id="email" placeholder="Enter your email" required>

        <label>Phone Number:</label>
        <input type="text" id="phone_number" placeholder="Enter your phone number" required>
        
      
        
        <label>Address:</label>
        <input type="text" id="address" placeholder="Enter your address" required>

        <label>Is active:</label>
        <select id="Is_active" required>
            <option value="">Is this user active?</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
        </select>
        
        <label>Role:</label>
        <select id="role" required>
            <option value="">Select your role</option>
            <option value="Client">Client</option>
            <option value="Role">Role</option>
            <option value="Agent">Agent</option>
        </select>
        
        <button type="submit" class="btn">Create Account</button>
    </form>
</div>

<script>
    function validateForm() {
        var firstName = document.getElementById("first_name").value;
        var lastName = document.getElementById("last_name").value;
        var username = document.getElementById("username").value;
        var identifier = document.getElementById("identifier").value;
        var email = document.getElementById("email").value;
        var address = document.getElementById("address").value;
        var phoneNumber = document.getElementById("phone_number").value;
        var pass = document.getElementById("password").value;
        var confirmPass = document.getElementById("confirm_password").value;
        var errorMsg = document.getElementById("error_msg");

        // Password validation
        if (pass.length < 6) {
            errorMsg.innerText = "Password must be at least 6 characters long.";
            return false;
        }
        if (pass !== confirmPass) {
            errorMsg.innerText = "Passwords do not match!";
            return false;
        }
        
        if (identifier.length < 3 ) {
            alert("Identifier must be at least 3 characters long.");
            return false;
        }

        if (username.length < 3) {
            alert("Username must be at least 3 characters long.");
            return false;
        }

        alert("Registration Successful!");
        return true;
    }
</script>
"""

# Display form in Streamlit
st.title("User Registration Form", )
components.html(form_html, height=1200)
