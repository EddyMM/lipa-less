/**
* Handle successful registration of a new organization
**/
function onSignupSuccess(res, status) {
    console.log("Request status: " + status);
    console.log("Response status code: " + res[1]);

    var responseStatus = res[1];
    if(responseStatus == 200) {
        window.location = "/business";
        return;
    }

    if((res[0]["msg"]!==undefined) || (res[0]["msg"]!==null)) {
        $("#server-responses").text(res[0]["msg"]);
    }
}

/**
* Handle any error when registering a new organization
**/
function onSignupError(res) {
    var errorMsg = JSON.parse(res.responseText);
    console.log(errorMsg);

    if((errorMsg["msg"]!==undefined) || (errorMsg["msg"]!=null)) {
        alert(errorMsg["msg"]);
    }
    // $("#org-modal").modal("hide");
}

/**
 * Alerts the user that the password and confirm password field values
 * do not match
 */
function showPasswordMismatchAlert() {
    ($("#confirm-password-mismatch")).text("Passwords do not match");
}

function removePasswordMismatchAlert() {
    ($("#confirm-password-mismatch")).text("");
}

$(document).ready(function (){
    $(".main-content").niceScroll();

    $("#sign-up-btn").click(function(ele) {
        // Prevent submission
        ele.preventDefault();

        // Validate fields
        var signupForm = document.getElementById("signup-form");
        if(!signupForm.reportValidity()) {
            return;
        }

        // Compare passwords
        var password = $("input[name='password']").val();
        var confirmPassword=  $("input[name='confirm-password']").val();

        if(password === confirmPassword) {
            removePasswordMismatchAlert();
        } else {
            showPasswordMismatchAlert();
            return;
        }

        // Package the data into an object
        var name = $("input[name='name']").val();
        var email = $("input[name='email']").val();
        var signupInfo = {
            "name": name,
            "email": email,
            "password": password
        };

        // Make AJAX API call
        apiCall(
            "/signup",
            JSON.stringify(signupInfo),
            onSignupSuccess,
            onSignupError
        );
    });
});
