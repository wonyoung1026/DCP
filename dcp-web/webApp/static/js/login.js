$(function () {

    $('#login-register-form-buyer').click(function (e) {
        $('#login-register-form-provider').removeClass('active');
        $("#login-form-for-buyer").delay(100).fadeIn(100);
        $("#login-form-for-provider").fadeOut(100);
        $(this).addClass('active');
        e.preventDefault();
    });

    $('#login-register-form-provider').click(function (e) {
        $('#login-register-form-buyer').removeClass('active');
        $("#login-form-for-provider").delay(100).fadeIn(100);
        $("#login-form-for-buyer").fadeOut(100);
        $(this).addClass('active');
        e.preventDefault();
    });
});


//login for buyer
const loginFormBuyer = document.querySelector('#login-form-for-buyer');
loginFormBuyer.addEventListener('submit', (e) => {
    e.preventDefault();

    //get user info
    const email = loginFormBuyer['email-buyer'].value;
    const password = loginFormBuyer['password-buyer'].value;

    buyerSignIn(email, password);
})

//login for provider
const loginFormProvider = document.querySelector('#login-form-for-provider');
loginFormProvider.addEventListener('submit', (e) => {
    e.preventDefault();

    //get user info
    const email = loginFormProvider['email-provider'].value;
    const password = loginFormProvider['password-provider'].value;

    providerSignIn(email, password);
})