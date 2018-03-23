/**
* Handle successful registration of a new organization
**/
function onLoginSuccess(res) {
    var responseStatus = res["status"];
    console.log("Response: " + JSON.stringify(res));
    if(responseStatus === 200) {
        window.location = "/business";
        return;
    }

    if((res["msg"]!==undefined) || (res["msg"]!==null)) {
        $("#server-responses").text(res["msg"]);
    }
}

/**
* Handle any error when registering a new organization
**/
function onLoginError(res) {
    var errorMsg = JSON.parse(res.responseText);
    console.log(errorMsg);

    if((errorMsg["msg"]!==undefined) || (errorMsg["msg"]!=null)) {
        alert(errorMsg["msg"]);
    }
    // $("#org-modal").modal("hide");
}

$(document).ready(function (){
    $(".main-content").niceScroll();

    $("#login-btn").click(function(ele) {
        // Prevent submission
        ele.preventDefault();

        // Validate fields
        var loginForm = document.getElementById("login-form");
        if(!loginForm.reportValidity()) {
            return;
        }

        // Package the data into an object
        var email = $("input[name='email']").val();
        var password = $("input[name='password']").val();

        var loginInfo = {
            "email": email,
            "password": password
        };

        // Make AJAX API call
        apiCall(
            "/login",
            JSON.stringify(loginInfo),
            onLoginSuccess,
            onLoginError
        );
    });
});
