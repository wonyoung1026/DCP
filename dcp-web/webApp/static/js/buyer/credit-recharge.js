
function validate(){
    var credit = +document.getElementById("chargeAmount").value;
    if(isNaN(credit) || credit < 0){
	document.getElementById("modalcharge").innerHTML = ("Amount you entered is invalid! Please enter again.<br/>");
	document.getElementById("modal-btn-col").innerHTML = '<button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>';
    }
    else{
    document.getElementById("rechargeAmount").innerHTML = credit;
    document.getElementById("modal-btn-col").innerHTML = '<button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button><a class="btn btn-primary" href="#" onclick ="rechargeAmount()"id="final-purchase-btn">Confirm</a>';

    }
    }
function rechargeAmount(){
    var credit = document.getElementById("chargeAmount").value;
    var url = "/buyer/billing/"+credit+"/recharge";
    var http = new XMLHttpRequest();
    http.open('GET', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var modalBody = document.getElementById("modalcharge");
            var modalButton = document.getElementById("modal-btn-col");
            var res = JSON.parse(http.response)
            switch(http.status){
                case 202:
                    modalBody.innerHTML = ("Credit has been charged! Please wait for some time");
                    modalButton.innerHTML = '<button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>';
                    window.location = "/console/buyer/dashboard"
                    break;
                default:
                    modalBody.innerHTML = res.message;
                    modalButton.innerHTML = "";
                    break;
            }
        }
    }
    http.send();


}
