/**
* Handle successful addition of an admin
**/
function onAddAdminSuccess(res) {
    var responseStatus = res["status"];
    if(responseStatus === 200) {
        console.log(res["msg"]);
        $("#add-admin-modal").modal("hide");
        clearAccountsList();
        loadAccountsList(res["msg"]["accounts"], res["msg"]["roles"]);
    } else {
        if((res["msg"]!==undefined) || (res["msg"]!==null)) {
            $("#admin-server-responses").text(res["msg"]);
        }
    }
}

/**
* Handle any error when adding an admin
**/
function onAddAdminError(res) {
    var errorMsg = JSON.parse(res.responseText);

    if((errorMsg["msg"]!==undefined) || (errorMsg["msg"]!=null)) {
        alert(errorMsg["msg"]);
    }
    $("#add-admin-modal").modal("hide");
}

/**
* Handle successful addition of a cashier
**/
function onAddCashierSuccess(res) {
    var responseStatus = res["status"];
    if(responseStatus === 200) {
        console.log(res["msg"]);
        $("#add-cashier-modal").modal("hide");
        clearAccountsList();
        loadAccountsList(res["msg"]["accounts"], res["msg"]["roles"]);
    } else {
        if((res["msg"]!==undefined) || (res["msg"]!==null)) {
            $("#cashier-server-responses").text(res["msg"]);
        }
    }
}

/**
* Handle any error when adding a cashier
**/
function onAddCashierError(res) {
    var errorMsg = JSON.parse(res.responseText);

    if((errorMsg["msg"]!==undefined) || (errorMsg["msg"]!=null)) {
        alert(errorMsg["msg"]);
    }
    $("#add-cashier-modal").modal("hide");
}

function clearAccountsList() {
    $("#accounts-list-items").empty();
}

function loadAccountsList(accounts, roles) {
    accounts.forEach(function(account) {
        var roleOptions = "";

        roles.forEach(function(role) {
            roleOptions += ((account.role===role.name)?
                '<option value="'+ role.name +'" selected>' + role.name + '</option>':
                    '<option value="'+ role.name +'">' + role.name + '</option>'
            );
        });

        $("#accounts-list-items").append(
            '<div class="account row">\
                <div class="col-4">\
                    <select name="role">'+
                        roleOptions
                    +'</select>\
                </div>\
                <div class="col-4">\
                    <label id="'+ account.id +'">'+ account.name +'</label>\
                </div>\
                <div class="col-4">\
                    <input name="deactivated" type="checkbox" '+ ((account.deactivated)?'checked':'') +'>\
                </div>\
            </div>'
        );
    });
}


$(document).ready(function () {
    // Create modal add admin functionality
    $("#add-admin-box").click(function() {
        $("#add-admin-modal").modal("show");
    });

    // Create modal add cashier functionality
    $("#add-cashier-box").click(function() {
        $("#add-cashier-modal").modal("show");
    });

    // Configure add admin button
    $("#add-admin-btn").click(function(ele) {
        // Prevent submission
        ele.preventDefault();

        // Validate fields
        var addAdminForm = document.getElementById("add-admin-form");
        if(!addAdminForm.reportValidity()) {
            return;
        }

        // Package the data into an object
        var email = $("input[name='admin-email']").val();

        var adminInfo = {
            "role": "admin",
            "email": email
        };

        // Make AJAX API call
        apiCall(
            "/manage_accounts/role", 'POST',
            JSON.stringify(adminInfo),
            onAddAdminSuccess,
            onAddAdminError
        );
    });

    // Configure add cashier button
    $("#add-cashier-btn").click(function(ele) {
        // Prevent submission
        ele.preventDefault();

        // Validate fields
        var addCashierForm = document.getElementById("add-cashier-form");
        if(!addCashierForm.reportValidity()) {
            return;
        }

        // Package the data into an object
        var email = $("input[name='cashier-email']").val();

        var adminInfo = {
            "role": "cashier",
            "email": email
        };

        // Make AJAX API call
        apiCall(
            "/manage_accounts/role", 'POST',
            JSON.stringify(adminInfo),
            onAddCashierSuccess,
            onAddCashierError
        );
    });

    // Configure modify roles button
    $("#modify-roles-btn").click(function(ele) {
        // Prevent submission
        ele.preventDefault();

        // Validate fields
        var modifyRolesForm = document.getElementById("modify-roles-form");
        if(!modifyRolesForm.reportValidity()) {
            return;
        }

        var roles = {
            roles:[]
        };

        $(".account").each(function() {
            // Single account item
            // Get info
            // Start with role
            var role = $(this).find("select").val();
            // Then the user id
            var id = $(this).find("label").attr("id");
            // Then the deactivation status
            var deactivated = $(this).find("input[type='checkbox']").is(":checked");

            roles.roles.push(
                {
                    emp_id: id,
                    role: role,
                    deactivated: deactivated
                }
            );
        });

        // Make AJAX API call
        apiCall(
            "/manage_accounts/role", 'PUT',
            JSON.stringify(roles),
            onAddCashierSuccess,
            onAddCashierError
        );
    });chrom
});
