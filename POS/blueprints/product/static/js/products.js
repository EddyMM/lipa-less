jQuery(function () {
    /**
     * Event handlers
    */

    // Category addition
    $("#create-category-btn").on("click", function() {
        $("#add-category-modal").modal("show");
    });
    $("#add-category-btn").on("click", function(e) {
        onAddCategoryClickHandler(e);
    });

    // Supplier addition
    $("#create-supplier-btn").on("click", function() {
        $("#add-supplier-modal").modal("show");
    });
    $("#add-supplier-btn").on("click", function(e) {
        onAddSupplierClickHandler(e);
    });

    // Manufacturer addition
    $("#create-manufacturer-btn").on("click", function() {
        $("#add-manufacturer-modal").modal("show");
    });
    $("#add-manufacturer-btn").on("click", function(e) {
        onAddManufacturerClickHandler(e);
    });

    // Product addition
    jQuery("#add-product-btn").on("click", function(e) {
        onAddProductClickHandler(e);
    })
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
 * Handles add supplier on click event
 */
function onAddSupplierClickHandler(e) {
    // Prevent submission
    e.preventDefault();

    // Validate fields
    var addSupplierForm = document.getElementById("add-supplier-form");
    if(!addSupplierForm.reportValidity()) {
        return;
    }

    // Package the data into an object
    var name = $("input[name='supplier-name']").val();
    var contactPerson = $("input[name='supplier-contact-person']").val();
    var contactNumber = $("input[name='supplier-contact-number']").val();

    var supplierInfo = {
        "name": name,
        "contact_person": contactPerson,
        "contact_number": contactNumber
    };

    console.log("supplierInfo: " + supplierInfo);

    // Send request
    apiCall(
        "/supplier",
        "POST",
        JSON.stringify(supplierInfo),
        onAddSupplierSuccess,
        onError
    );
}

/**
 * Handles add manufacturer on click event
 */
function onAddManufacturerClickHandler(e) {
    // Prevent submission
    e.preventDefault();

    // Validate fields
    var addManufacturerForm = document.getElementById("add-manufacturer-form");
    if(!addManufacturerForm.reportValidity()) {
        return;
    }

    // Package the data into an object
    var name = jQuery("input[name='manufacturer-name']").val();

    var manufacturerInfo = {
        "name": name
    };

    console.log("manufacturerInfo: " + manufacturerInfo);

    // Send request
    apiCall(
        "/manufacturer",
        "POST",
        JSON.stringify(manufacturerInfo),
        onAddManufacturerSuccess,
        onError
    );
}

function onAddProductClickHandler(e) {
    // Prevent submission
    e.preventDefault();

    // Validate fields
    var addProductForm = document.getElementById("add-product-form");
    if(!addProductForm.reportValidity()) {
        return;
    }

    // Package the data into an object
    var name = jQuery("input[name='product-name']").val();
    var description = jQuery("textarea[name='product-description']").val();
    var buyingPrice = jQuery("input[name='buying-price']").val();
    var sellingPrice = jQuery("input[name='selling-price']").val();
    var quantity = jQuery("input[name='quantity']").val();
    var reorderLevel = jQuery("input[name='reorder-level']").val();
    var expirationDate = jQuery("input[name='expiration-date']").val();
    var categories = (document.getElementById("category-options")).options;
    var categoryId = categories[categories.selectedIndex].value;
    var suppliers = (document.getElementById("supplier-options")).options;
    var supplierId = suppliers[suppliers.selectedIndex].value;
    var manufacturers = (document.getElementById("manufacturer-options")).options;
    var manufacturerId = manufacturers[manufacturers.selectedIndex].value;


    var productInfo = {
        "name": name,
        "description": description,
        "buying_price": buyingPrice,
        "selling_price": sellingPrice,
        "quantity": quantity,
        "reorder_level": reorderLevel,
        "expiration_date": expirationDate,
        "category_id": categoryId,
        "supplier_id": supplierId,
        "manufacturer_id": manufacturerId
    };

    // Send request
    apiCall(
        "/product",
        "POST",
        JSON.stringify(productInfo),
        onAddProductSuccess,
        onError
    );
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

        updateCategories(newCategories);

    } else {
        if((res["msg"]!==undefined) || (res["msg"]!==null)) {
            $("#category-server-responses").text(res["msg"]);
        }
    }
}

/**
* Handle successful creation of a supplier
**/
function onAddSupplierSuccess(res, status, jqXHR) {
    var responseStatus = parseInt(jqXHR.getResponseHeader("code"));
    if(responseStatus === 200) {
        $("#add-supplier-modal").modal("hide");

        // Update supplier list with new list
        console.log("res: " + res.toString());
        console.log("msg: " + res["msg"].toString());
        var newSuppliers = res["msg"]["suppliers"];

        updateSuppliers(newSuppliers);

    } else {
        if((res["msg"]!==undefined) || (res["msg"]!==null)) {
            $("#supplier-server-responses").text(res["msg"]);
        }
    }
}

/**
* Handle successful creation of a supplier
**/
function onAddManufacturerSuccess(res, status, jqXHR) {
    var responseStatus = parseInt(jqXHR.getResponseHeader("code"));
    if(responseStatus === 200) {
        $("#add-manufacturer-modal").modal("hide");

        // Update supplier list with new list
        console.log("res: " + res.toString());
        console.log("msg: " + res["msg"].toString());
        var newManufacturers = res["msg"]["manufacturers"];

        updateManufacturers(newManufacturers);

    } else {
        if((res["msg"]!==undefined) || (res["msg"]!==null)) {
            $("#manufacturer-server-responses").text(res["msg"]);
        }
    }
}

function onAddProductSuccess(res, status, jqXHR) {
    var responseStatus = parseInt(jqXHR.getResponseHeader("code"));
    if(responseStatus === 200) {
        // Update supplier list with new list
        console.log("res: " + res);
        console.log("msg: " + res["msg"]);

        // noinspection JSUnresolvedFunction
        // noinspection JSUnresolvedVariable
        window.location = Flask.url_for('products_bp.products');

    } else {
        if((res["msg"]!==undefined) || (res["msg"]!==null)) {
            $("#product-server-responses").text(res["msg"]);
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
                "<option value="+ category.id +">"
                    + category["name"] +
                "</option>";
        });

    console.log("categoryOptions: " + categoryOptions);

    categoriesDropdown.append(categoryOptions);
}

/**
 * Refresh suppliers
 * @param newSuppliers
 */
function updateSuppliers(newSuppliers) {
    var suppliersDropdown = $("select[name=supplier]");
    suppliersDropdown.empty();

    var supplierOptions = "";
        newSuppliers.forEach(function(supplier) {
            supplierOptions +=
                "<option value="+ supplier.id +">"
                    + supplier["name"] +
                "</option>";
        });

    console.log("supplierOptions: " + supplierOptions);

    suppliersDropdown.append(supplierOptions);
}

/**
 * Refresh suppliers
 * @param newManufacturers
 */
function updateManufacturers(newManufacturers) {
    var manufacturersDropdown = jQuery("select[name=manufacturer]");
    manufacturersDropdown.empty();

    var manufacturerOptions = "";
        newManufacturers.forEach(function(manufacturer) {
            manufacturerOptions +=
                "<option value="+ manufacturer.id +">"
                    + manufacturer["name"] +
                "</option>";
        });

    console.log("manufacturerOptions: " + manufacturerOptions);

    manufacturersDropdown.append(manufacturerOptions);
}


/**
* Handle api call error
**/
function onError(res) {
    var errorMsg = JSON.parse(res.responseText);

    if((errorMsg["msg"]!==undefined) || (errorMsg["msg"]!=null)) {
        alert(errorMsg["msg"]);
    }
    $("#add-product-modal").modal("hide");
}