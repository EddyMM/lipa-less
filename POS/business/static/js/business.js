/**
* Handle successful registration of a new business
**/
function onAddBusinessSuccess(res) {
    var responseStatus = res["status"];
    if(responseStatus === 200) {
        window.location = "/dashboard/" + res["business_id"]
    } else {
        if((res["msg"]!==undefined) || (res["msg"]!==null)) {
            $("#server-responses").text(res["msg"]);
        }
    }
}

/**
* Handle any error when registering a new business
**/
function onAddBusinessError(res) {
    var errorMsg = JSON.parse(res.responseText);

    if((errorMsg["msg"]!==undefined) || (errorMsg["msg"]!=null)) {
        alert(errorMsg["msg"]);
    }
    $("#add-business-modal").modal("hide");
}

$(document).ready(function (){
    // $(".main-content").niceScroll();

    // Create modal business form functionality
    $("#create-business-btn").click(function() {
        $("#add-business-modal").modal("show");
    });

    // Configure add business button
    $("#add-business-btn").click(function(ele) {
        // Prevent submission
        ele.preventDefault();

        // Validate fields
        var addBusinessForm = document.getElementById("add-business-form");
        if(!addBusinessForm.reportValidity()) {
            return;
        }

        // Package the data into an object
        var name = $("input[name='name']").val();
        var contactNumber = $("input[name='contact-number']").val();

        var businessInfo = {
            "name": name,
            "contact-number": contactNumber
        };

        // Make AJAX API call
        apiCall(
            "/business",
            JSON.stringify(businessInfo),
            onAddBusinessSuccess,
            onAddBusinessError
        );
    });

    // Configure select business button
    $("#select-business-btn").click(function(ele) {
        // Prevent submission
        ele.preventDefault();

        // Validate fields
        var selectBusinessForm = document.getElementById("select-business-form");
        if(!selectBusinessForm.reportValidity()) {
            return;
        }

        // Load dashboard using business id
        var business_id = $("input[name='business']:checked").val();
        window.location = "/dashboard/" + business_id;
    });
});
