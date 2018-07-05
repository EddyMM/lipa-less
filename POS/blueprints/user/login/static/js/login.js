// /**
// * Handle successful login
// **/
// function onLoginSuccess(res, code, jqXHR) {
//     var responseStatus = parseInt(jqXHR.getResponseHeader("code"));
//     console.log("Response: " + JSON.stringify(res));
//     if(responseStatus === 200) {
//         window.location = "/business";
//         return;
//     }
//
//     if((res["msg"]!==undefined) || (res["msg"]!==null)) {
//         $("#server-responses").text(res["msg"]);
//     }
// }
//
// /**
// * Handle any error when logging in a user
// **/
// function onLoginError(res) {
//     var errorMsg = JSON.parse(res.responseText);
//     console.log(errorMsg);
//
//     if((errorMsg["msg"]!==undefined) || (errorMsg["msg"]!=null)) {
//         alert(errorMsg["msg"]);
//     }
//     // $("#org-modal").modal("hide");
// }
//
// $(document).ready(function (){
//     // $(".main-content").niceScroll();
//
//     $("#login-btn").click(function(ele) {
//         // Prevent submission
//         ele.preventDefault();
//
//         // Validate fields
//         var loginForm = document.getElementById("login-form");
//         if(!loginForm.reportValidity()) {
//             return;
//         }
//
//         // Package the data into an object
//         var email = $("input[name='email']").val();
//         var password = $("input[name='password']").val();
//
//         var loginInfo = {
//             "email": email,
//             "password": password
//         };
//
//         // Make AJAX API call
//         apiCall(
//             "/login",  'POST',
//             JSON.stringify(loginInfo),
//             onLoginSuccess,
//             onLoginError
//         );
//     });
// });

/**
 * Vue instance to manage login operations
 */
let loginApp = new Vue({
    el: '#login-form',
    data: {
        email: null,
        password: null
    },
    methods: {
        sendUserInfo: function () {
            // Validate fields
            let loginForm = document.getElementById("login-form");
            if(!loginForm.reportValidity()) {
                return;
            }

            let loginInfo = {
                "email": this.email,
                "password": this.password
            };

            // Use axios plugin to m ake POST request to server
            axios
                .post('/login',
                        loginInfo)
                .then(response => {
                    if(response.headers.code === '200') {
                        window.location = "/business";
                    }
                    this.$refs.serverResponses.innerHTML = response.data.msg;
                })
        }
    }
});
