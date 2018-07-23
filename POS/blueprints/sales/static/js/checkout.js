let productOptionsApp = new Vue({
    el: '#productSelectionApp',
    delimiters: ['[[', ']]'],
    data: {
        products: null,
        selectedProduct: null,
        quantity: 0,
        selling_price: 0,
    },
    methods: {
        changePriceFromQuantity: function changePriceFromQuantity() {
            if(this.selectedProduct >= 0) {
                let product_from_id = getProductById(this.selectedProduct);
                if(product_from_id != null) {
                    this.selling_price = this.quantity * product_from_id.selling_price;
                } else {
                    console.log("No product by id: " + this.selectedProduct);
                }
            }
        },
        addLineItem: function () {
            let productFromId =  getProductById(this.selectedProduct)
            if(productFromId != null && this.selectedProduct > 0 &&
                productFromId.name != null &&
                productFromId.name !== "" &&
                productFromId.selling_price > 0 &&
                productFromId.quantity) {

                let lineItem = {
                    product_id: this.selectedProduct,
                    name: productFromId.name,
                    selling_price: productFromId.selling_price,
                    quantity: this.quantity
                };

                checkoutApp.lineItems.push(lineItem);
                computeTotal();
                resetProductOptionsApp();
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
    delimiters: ['[[', ']]'],
    data: {
        lineItems: [],
        total: 0,
        amountPaid: 0,
        change: 0
    },
    methods: {
        removeLineItem: function(index) {
            this.$delete(this.lineItems, index);
            computeTotal();
        },
        checkoutItems: function() {
          console.log("Checking out items");
          let sales_transaction_request = {
              transaction: {
                  amount_given: this.amountPaid
              },
              line_items: this.lineItems
          };
          axios
            .post("/sales", sales_transaction_request)
            .then(
            response => {
                if (response.headers.code === '200') {
                    console.log("Successfully checked out items!");
                } else {
                    console.log("Error checking out items: " + response.data.msg);
                }
            });
        },
        computeChange: function() {
            this.change = this.amountPaid - this.total;
        }
    }
});

function computeTotal() {
    let checkout_total = 0;

    for(x=0; x<checkoutApp.lineItems.length; x++) {
        checkout_total += checkoutApp.lineItems[x].selling_price * checkoutApp.lineItems[x].quantity;
    }

    checkoutApp.total = checkout_total;
}

function resetProductOptionsApp() {
    productOptionsApp.quantity = 0;
    productOptionsApp.selling_price = 0;
}

function getProductById(productId) {
    for(x=0; x < productOptionsApp.products.length; x++) {
        if(productOptionsApp.products[x].id === parseInt(productId)) {
            return productOptionsApp.products[x];
        }
    }
}
