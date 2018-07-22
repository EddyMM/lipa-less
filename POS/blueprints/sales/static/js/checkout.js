/**
 * Products search app
 */
Vue.component('select-search', {
    template: '#my-template',
    delimiters: ['[[', ']]'],
    props: {
        value: {
            required: true
        },
        items: {
            type: Array,
            required: false
        },
        returns: {
            type: String,
            default: 'id'
        },
        shows: {
            type: String,
            required: true
        },
        firstLabel: {
            type: String,
            default: 'Please select'
        },
        firstDisabled: {
            type: Boolean,
            default: true
        },
        search: {
            type: String,
            default: ''
        },
        addBtn: {
            type: Boolean,
            default: false
        }
    },
    data: function data() {
        return {
            searchQuery: '',
            addedItem: this.value || 0,
            selectedItem: this.value || 0
        };
    },

    computed: {
        columns: function columns() {
            if (!this.items.length) return [];
            return Object.keys(this.items[0]);
        },
        searchColumns: function searchColumns() {
            if (!this.search.length) return this.columns;
            return this.search.split('|');
        },
        searchedItems: function searchedItems() {
            var _this = this;

            if (!this.searchQuery) {
                this.selectedItem = 0;
                if (this.addedItem !== 0 && this.checkItemExists(this.addedItem)) this.selectedItem = this.addedItem;else this.addedItem = 0;
                return this.items;
            }

            var items = this.items.filter(function (item) {
                return _this.searchColumns.some(function (column) {
                    return String(item[column]).toLowerCase().indexOf(_this.searchQuery.toLowerCase()) > -1;
                });
            });

            if (items.length) this.selectedItem = items[0][this.returns];else this.selectedItem = 0;

            return items;
        }
    },
    methods: {
        checkItemExists: function checkItemExists(item) {
            return _.map(this.items, this.returns).indexOf(item) > -1;
        },
        addItem: function addItem() {
            //if(this.selectedItem == 0) return
            this.addedItem = this.selectedItem;
            let selectedProduct = productOptionsApp.products[this.addedItem - 1]
            console.log(selectedProduct);
            console.log(selectedProduct.price);
            productOptionsApp.selectedProduct = selectedProduct;
            productOptionsApp.price = productOptionsApp.quantity * selectedProduct.price;

            if (this.addedItem === 0 && this.firstDisabled) return;

            this.$emit('input', this.addedItem);
            this.$emit('selected');
        },
        prevItem: function prevItem() {
            var _this2 = this;

            if (!this.items.length) return;

            var i = this.searchedItems.map(function (itm) {
                return itm[_this2.returns];
            }).indexOf(this.selectedItem);

            if (i == 0) {
                if (this.firstDisabled) this.selectedItem = this.searchedItems[this.searchedItems.length - 1][this.returns];else this.selectedItem = 0;
            } else if (this.selectedItem == 0) this.selectedItem = this.searchedItems[this.searchedItems.length - 1][this.returns];else this.selectedItem = this.searchedItems[i - 1][this.returns];
        },
        nextItem: function nextItem() {
            var _this3 = this;

            if (!this.items.length) return;

            var i = this.searchedItems.map(function (itm) {
                return itm[_this3.returns];
            }).indexOf(this.selectedItem);

            if (i == this.searchedItems.length - 1) {
                if (this.firstDisabled) this.selectedItem = this.searchedItems[0][this.returns];else this.selectedItem = 0;
            } else this.selectedItem = this.searchedItems[i + 1][this.returns];
        },
        close: function close() {
            this.$emit('close ');
        },
        formOptionText: function formOptionText(item) {
            var j = [];
            var s = this.shows.split('|');
            s.forEach(function (x) {
                return j.push(item[x]);
            });

            return j.join(' | ');
        },
        getCount: function getCount() {
            return this.firstDisabled ? this.searchedItems.length : this.searchedItems.length + 1;
        },
        manualChange: function manualChange() {
            this.addedItem = this.selectedItem;
            this.$emit('input', this.addedItem);
        }
    }
});

let productOptionsApp = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        products: null,
        selectedProduct: null,
        quantity: 0,
        price: 0,
        firstExample: 0,
        secondExample: 0,
        thirdExample: 0,
        fourthExample: 0
    },
    methods: {
        thirdExampleSelected: function thirdExampleSelected() {
            alert('Result: ' + this.thirdExample);
        },
        changePriceFromQuantity: function changePriceFromQuantity() {
            console.log("Quantity enter");
            if(productOptionsApp.selectedProduct != null) {
                productOptionsApp.price = productOptionsApp.quantity * productOptionsApp.selectedProduct.price;
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
        searchItemName: null,
        searchItemQuantity: null,
        searchItemPrice: null
    },
    methods: {

    }
});