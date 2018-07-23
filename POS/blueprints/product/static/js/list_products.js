let productListApp = new Vue({
    el: '#products-list',
    delimiters: ['[[', ']]'],
    data: {
        products: null
    },
    methods: {
        saveProductDetails: function(index) {
            console.log("Save details of: " + this.products[index].id);
            console.log("Product: ");
            console.log(this.products[index]);
            axios
            .put("/products/" + this.products[index].id, this.products[index])
            .then(
                response => {
                    console.log(response);
                    if (response.headers.code === '200') {
                        this.products = response.data.msg.products;
                    } else {
                        console.log("Could not fetch products");
                    }
                }
            );
        },
        deleteProduct: function(index) {
            console.log("Delete details of: " + this.products[index].name);
            console.log("Product: ");
            console.log(this.products[index]);
            axios
            .delete("/products/" + this.products[index].id, this.products[index])
            .then(
                response => {
                    console.log(response);
                    if (response.headers.code === '200') {
                        this.products = response.data.msg.products;
                    } else {
                        console.log("Could not fetch products");
                    }
                }
            );
        }
    },
    mounted() {
        axios
            .get("/products")
            .then(
                response => {
                    if (response.headers.code === '200') {
                        this.products = response.data.msg.products;
                    } else {
                        console.log("Could not fetch products");
                    }
                }
            );
    }
});
