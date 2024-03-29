let productAddition = new Vue({
    el: "#add-product-form",
    delimiters: ['[[', ']]'],
    data: {
        name: null,
        description: null,
        buying_price: null,
        selling_price: null,
        quantity: null,
        reorder_level: null,
        categories: null,
        category: null,
    },
    methods: {
        addProduct: function () {
            // Validate fields
            let addProductForm = document.getElementById("add-product-form");
            if (!addProductForm.reportValidity()) {
                return;
            }

            // Package the data into an object

            let productInfo = {
                name: this.name,
                description: this.description,
                buying_price: this.buying_price,
                selling_price: this.selling_price,
                quantity: this.quantity,
                reorder_level: this.reorder_level,
                category_id: this.category,
            };

            console.log(productInfo);

            axios
                .post("/product", productInfo)
                .then(
                    response => {
                        if (response.headers.code === '200') {
                            console.log("Added product!");
                            window.location = "/products/manage";
                        }
                        $("#product-server-responses").text(response.data.msg);
                    }
                );
        }
    },
    mounted() {
        axios
            .get('/categories')
            .then(response => {
                this.categories = response.data.msg.categories;
            });
    }
});

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
                            productAddition.categories = response.data.msg.categories;
                        }
                        $("#category-server-responses").text(response.data.msg);
                    }
                );
        }
    }
});

jQuery(function () {
    /**
     * Event handlers
    */

    // Category addition modal
    $("#create-category-btn").on("click", function() {
        $("#add-category-modal").modal("show");
    });

    // Supplier addition
    $("#create-supplier-btn").on("click", function() {
        $("#add-supplier-modal").modal("show");
    });

    // Manufacturer addition
    $("#create-manufacturer-btn").on("click", function() {
        $("#add-manufacturer-modal").modal("show");
    });
});