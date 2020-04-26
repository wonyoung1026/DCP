$(function () {

    $('#login-register-form-buyer').click(function (e) {
        $('#login-register-form-provider').removeClass('active');
        $("#register-form-for-buyer").delay(100).fadeIn(100);
        $("#register-form-for-provider").fadeOut(100);
        $(this).addClass('active');
        e.preventDefault();
    });

    $('#login-register-form-provider').click(function (e) {
        $('#login-register-form-buyer').removeClass('active');
        $("#register-form-for-provider").delay(100).fadeIn(100);
        $("#register-form-for-buyer").fadeOut(100);
        $(this).addClass('active');
        e.preventDefault();
    });
});


//register for buyer
const registerFormBuyer = document.querySelector('#register-form-for-buyer');
registerFormBuyer.addEventListener('submit', (e) => {
    e.preventDefault();

    //get user info
    const email = registerFormBuyer['register-email-input-for-buyer'].value;
    const password = registerFormBuyer['register-password-input-for-buyer'].value;
    const buyerFlag = true;

    signUp(email, password, buyerFlag);
})

//register for provider
const registerFormProvider = document.querySelector('#register-form-for-provider');
registerFormProvider.addEventListener('submit', (e) => {
    e.preventDefault();

    //get user info
    const email = registerFormProvider['register-email-input-for-provider'].value;
    const password = registerFormProvider['register-password-input-for-provider'].value;
    const buyerFlag = false;

    signUp(email, password, buyerFlag);
})