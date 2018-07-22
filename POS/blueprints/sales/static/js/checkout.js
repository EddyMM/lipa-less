/**
 * total app
 */
let totalApp = new Vue({
    el: "#totalApp",
    data: {
        total: 0,
        amountPaid: 0,
        change: 0
    },
    methods: {}
});

let productOptionsApp = new Vue({
    el: '#productSelectionApp',
    delimiters: ['[[', ']]'],
    data: {
        products: null,
        selectedProduct: null,
        quantity: 0,
        price: 0,
    },
    methods: {
        changePriceFromQuantity: function changePriceFromQuantity() {
            if(this.selectedProduct >= 0) {
                this.price = this.quantity * this.products[this.selectedProduct-1].price;
            }
        },
        addLineItem: function () {
            if(this.selectedProduct > 0 &&
                this.products[this.selectedProduct-1].name != null &&
                this.products[this.selectedProduct-1].name !== "" &&
                this.products[this.selectedProduct-1].price > 0 &&
                this.products[this.selectedProduct-1].quantity) {

                let lineItem = {
                    product_id: this.selectedProduct,
                    name: this.products[this.selectedProduct-1].name,
                    price: this.products[this.selectedProduct-1].price,
                    quantity: this.quantity
                };

                console.log(lineItem);

                checkoutApp.lineItems.push(lineItem);
                computeTotal();
            }
        }
    },
    mounted() {
        axios
            .get('/products')
            .then(response => {
                this.products = response.data.msg.products;
            });
    }
});

/**
 * Checkout app
 */
let checkoutApp = new Vue({
    el: "#checkoutApp",
    data: {
        lineItems: []
    },
    methods: {

    }
});

function computeTotal() {
    let total = 0;

    for(x=0; x<checkoutApp.lineItems.length; x++) {
        total += checkoutApp.lineItems[x].price * checkoutApp.lineItems[x].quantity;
    }

    console.log("Compute Total: " + total);

    totalApp.total = total;
}