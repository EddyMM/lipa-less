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
                let product_from_id = getProductById(this.selectedProduct);
                if(product_from_id != null) {
                    this.price = this.quantity * product_from_id.price;
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
                productFromId.price > 0 &&
                productFromId.quantity) {

                let lineItem = {
                    product_id: this.selectedProduct,
                    name: productFromId.name,
                    price: productFromId.price,
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
        }
    }
});

function computeTotal() {
    let total = 0;

    for(x=0; x<checkoutApp.lineItems.length; x++) {
        total += checkoutApp.lineItems[x].price * checkoutApp.lineItems[x].quantity;
    }

    checkoutApp.total = total;
}

function resetProductOptionsApp() {
    productOptionsApp.quantity = 0;
    productOptionsApp.price = 0;
}

function getProductById(productId) {
    for(x=0; x < productOptionsApp.products.length; x++) {
        if(productOptionsApp.products[x].id === parseInt(productId)) {
            return productOptionsApp.products[x];
        }
    }
}
