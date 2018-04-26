$(document).ready(function () {
    $("#create-category-btn").click(function() {
        $("#add-category-modal").modal("show");
    });

    $("#add-category-btn").click(function(e) {
        // Prevent submission
        e.preventDefault();

        // Validate fields
        var addCategoryForm = document.getElementById("add-category-form");
        if(!addCategoryForm.reportValidity()) {
            return;
        }

        // Package the data into an object
        var name = $("input[name='category-name']").val();
        var description = $("textarea[name='category-description']").val();

        var categoryInfo = {
            "name": name,
            "description": description
        };

        console.log("categoryInfo: " + categoryInfo);

        // Send request
        apiCall(
            "/category",
            "POST",
            JSON.stringify(categoryInfo),
            onAddCategorySuccess,
            onAddCategoryError
        )
    });
});

/**
* Handle successful creation of a category
**/
function onAddCategorySuccess(res, status, jqXHR) {
    var responseStatus = parseInt(jqXHR.getResponseHeader("code"));
    if(responseStatus === 200) {
        $("#add-category-modal").modal("hide")

        // FIXME: Update categories client-side
        // Update category list with new list
        console.log("res: " + res.toString());
        console.log("msg: " + res["msg"].toString());
        var newCategories = res["msg"]["categories"];

        updateCategories(newCategories);

    } else {
        if((res["msg"]!==undefined) || (res["msg"]!==null)) {
            $("#category-server-responses").text(res["msg"]);
        }
    }
}

/**
 * Refresh categories
 * @param newCategories
 */
function updateCategories(newCategories) {
    var categoriesDropdown = $("select[name=category]");
    categoriesDropdown.empty();

    var categoryOptions = "";
        newCategories.forEach(function(category) {
            categoryOptions +=
                "<option name"+ category.id +">"
                    + category["name"] +
                "</option>";
        });

    console.log("categoryOptions: " + categoryOptions);

    categoriesDropdown.append(categoryOptions);
}

/**
* Handle any error when adding a category
**/
function onAddCategoryError(res) {
    var errorMsg = JSON.parse(res.responseText);

    if((errorMsg["msg"]!==undefined) || (errorMsg["msg"]!=null)) {
        alert(errorMsg["msg"]);
    }
    $("#add-business-modal").modal("hide");
}