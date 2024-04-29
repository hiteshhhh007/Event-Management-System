const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

function validateForm(formId) {
        var form = $('#' + formId);

        // Check if any field is empty
        if (form.find(':input[required]').filter(function () {
            return $(this).val().trim() === '';
        }).length > 0) {
            alert('Please fill in all required fields.');
            return false; // Prevent form submission
        }

        return true; // Allow form submission
    }

    // Event handler for signup form submission
    $('#signup-form').submit(function (e) {
        if (!validateForm('signup-form')) {
            e.preventDefault(); // Prevent the form from submitting if validation fails
        }
    });

    // Event handler for login form submission
    $('#login-form').submit(function (e) {
        if (!validateForm('login-form')) {
            e.preventDefault(); // Prevent the form from submitting if validation fails
        }
    });