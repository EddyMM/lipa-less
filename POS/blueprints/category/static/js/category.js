/**
 * Vue instance to manage category addition from products form
 */
let categoryAddition = new Vue({
    el: '#add-category-modal',
    delimiters: ['[[', ']]'],
    data: {
        category_name: null,
        category_description: null
    },
    methods: {
        addCategory: function () {
            // Validate fields
            let addCategoryForm = document.getElementById("add-category-form");
            if (!addCategoryForm.reportValidity()) {
                return;
            }

            // Package the data into an object

            let categoryInfo = {
                "name": this.category_name,
                "description": this.category_description
            };

            axios
                .post("/category", categoryInfo)
                .then(
                    response => {
                        if (response.headers.code === '200') {
                            $("#add-category-modal").modal("hide");
                            // categories = response.data.msg.categories;
                        }
                        $("#category-server-responses").text(response.data.msg);
                    }
                );
        }
    }
});

jQuery(function() {
    $("#create-new-category-btn").on("click", function() {
        $("#add-category-modal").modal("show");
    });
});


/**
 * Handles add category click event
 * @param e
 */
function onAddCategoryClickHandler(e) {
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
        onError
    )
}


/**
* Handle successful creation of a category
**/
function onAddCategorySuccess(res, status, jqXHR) {
    var responseStatus = parseInt(jqXHR.getResponseHeader("code"));
    if(responseStatus === 200) {
        $("#add-category-modal").modal("hide");

        // Update category list with new list
        console.log("res: " + res.toString());
        console.log("msg: " + res["msg"].toString());
        var newCategories = res["msg"]["categories"];

        // TODO: Refresh categories list on client-side
        updateCategories(newCategories);

    } else {
        if((res["msg"]!==undefined) || (res["msg"]!==null)) {
            $("#category-server-responses").text(res["msg"]);
        }
    }
}

function updateCategories(categories) {
    // TODO Reload categories
    console.log(categories);
}


/**
* Handle api call error
**/
function onError(res) {
    var errorMsg = JSON.parse(res.responseText);

    if((errorMsg["msg"]!==undefined) || (errorMsg["msg"]!=null)) {
        alert(errorMsg["msg"]);
    }
    $("#add-category-modal").modal("hide");
}
