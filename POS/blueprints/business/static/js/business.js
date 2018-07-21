function showCreateBusinessModal() {
    $("#add-business-modal").modal("show");
}

let addBusinessApp = new Vue({
    el: '#add-business-form',
    data: {
        name: null,
        contactNumber: null
    },
    methods: {
        addBusiness: function() {
            // Validate fields
            let addBusinessForm = document.getElementById("add-business-form");
            if(!addBusinessForm.reportValidity()) {
                return;
            }

            // Capture business info
            let businessInfo = {
                "name": this.name,
                "contact_number": this.contactNumber
            };

            console.log(businessInfo);

            axios
                .post("/business", businessInfo)
                .then(response => {
                    if(response.headers.code === '200') {
                        window.location = "/dashboard";
                    }
                    this.$refs.serverResponses.innerHTML = response.data.msg;
                })
        }
    }
});

let selectBusiness = new Vue({
    el: '#select-business-form',
    data: {},
    methods: {
        selectBusiness: function() {
            // Validate fields
            let selectBusinessForm = document.getElementById("select-business-form");
            if(!selectBusinessForm.reportValidity()) {
                return;
            }

            // Load dashboard using business id
            let business_id = $("input[name='business']:checked").val();
            window.location = "/business/select/" + business_id;
        }
    }
});