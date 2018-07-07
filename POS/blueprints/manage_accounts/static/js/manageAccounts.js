function addAdminModal() {
    $("#add-admin-modal").modal("show");
}

function addCashierModal() {
    $("#add-cashier-modal").modal("show");
}

let accountsList = new Vue({
    el: '#accounts-list-area',
    delimiters: ['[[', ']]'],
    data: {
        accounts: null,
        roles: null
    },
    methods: {
        updateAccounts: function() {
            axios
                .put('/manage_accounts/roles', {roles: this.accounts})
                .then(response => {
                    console.log(this.accounts);
                    console.log(response.data);
                    this.accounts = response.data.msg.accounts;
                })
        }
    },
    mounted() {
        axios
            .get('manage_accounts/roles')
            .then(response => {
                console.log(response.data.msg.accounts);
                this.accounts = response.data.msg.accounts;
                this.roles = response.data.msg.roles;
            })
    }
});

let addAdminApp = new Vue({
    el: '#add-admin-modal',
    data: {
        email: null
    },
    methods: {
        addAdmin: function () {
            // Validate fields
            let addAdminForm = document.getElementById("add-admin-form");
            if (!addAdminForm.reportValidity()) {
                return;
            }

            // Package the data into an object
            let email = this.email;

            let adminInfo = {
                "role": "admin",
                "email": email
            };

            axios
                .post("/manage_accounts/roles", adminInfo)
                .then(
                    response => {
                        if (response.headers.code === '200') {
                            $("#add-admin-modal").modal("hide");
                            console.log(response.data.msg.accounts);
                            accountsList.accounts = response.data.msg.accounts;
                            accountsList.roles = response.data.msg.roles;
                            console.log(response.data.msg.roles);
                            // clearAccountsList();
                            // loadAccountsList(res["msg"]["accounts"], res["msg"]["roles"]);
                        }
                        $("#admin-server-responses").text(response.data.msg);
                    }
                );
        }
    }
});

let addCashierApp = new Vue({
    el: '#add-cashier-modal',
    data: {
        email: null
    },
    methods: {
        addCashier: function () {
            // Validate fields
            let addCashierForm = document.getElementById("add-cashier-form");
            if (!addCashierForm.reportValidity()) {
                return;
            }

            // Package the data into an object
            let email = this.email;

            let cashierInfo = {
                "role": "cashier",
                "email": email
            };

            axios
                .post("/manage_accounts/roles", cashierInfo)
                .then(
                    response => {
                        if (response.headers.code === '200') {
                            $("#add-cashier-modal").modal("hide");
                            accountsList.accounts = response.data.msg.accounts;
                            accountsList.roles = response.data.msg.roles;
                        }
                        $("#cashier-server-responses").text(response.data.msg);
                    }
                );
        }
    }
});
