function addGPU(listGPU, element){
    element.innerHTML = "";
    for(i =0; i<listGPU.length; ++i){
        element.innerHTML += listGPU[i]["processor"]
        element.innerHTML += "<br>"
    }
}

function addElementByList(listInput, element){
    element.innerHTML = "";
    for(i =0; i<listInput.length; ++i){
        element.innerHTML += listInput[i]
        element.innerHTML += "<br>"
    }

}

function getFullInstanceDetail(){
    // Hide other cards and display Full Instance Detail Card
    document.getElementById("full-instance-detail-card").style.display = "block";
    document.getElementById("instance-detail-card").style.display = "none";
    
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    // Indicate searching
    var fullInstanceDetailElement = document.getElementById("full-instance-detail");
    var fullInstanceDetailErrorElement = document.getElementById("full-instance-detail-err");

    fullInstanceDetailElement.style.display = "none";
    fullInstanceDetailErrorElement.style.display = "block";
    fullInstanceDetailErrorElement.style.color = "black";
    fullInstanceDetailErrorElement.innerHTML = "Searching...";

    var http = new XMLHttpRequest();
    var url = "/user/vm/"+vmID+"/full";
    http.open('GET', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            switch(http.status){
                case 200:
                    var res = JSON.parse(http.responseText);
                    var output = res.output;
                    console.log(res.output);
                    fullInstanceDetailElement.style.display = "block";
                    fullInstanceDetailErrorElement.style.display = "none";
                    fullInstanceDetailElement.innerHTML = output;
                    break;
                default:
                    var errMsg = "Unable to find full instance detail."
                    fullInstanceDetailElement.style.display = "none";
                    fullInstanceDetailErrorElement.style.display = "block";
                    fullInstanceDetailErrorElement.style.color = "red";
                    fullInstanceDetailErrorElement.innerHTML = errMsg;
                    break;
            }
        }
    }
    http.send();

}

function getInstanceDetail(){
    // Hide other cards and display Full Instance Detail Card
    document.getElementById("full-instance-detail-card").style.display = "none";
    document.getElementById("instance-detail-card").style.display = "block";

}


function sellVM(){
    var xhr = new XMLHttpRequest();

    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    var vmPrice = document.getElementById("instance-sell-price").value;
    
    var gpuPrices = document.getElementsByName("gpu-sell-price");
    var gpuList = []
    for (i =0; i<gpuPrices.length; i++){
        gpuList.push({
            "id":   gpuPrices[i].getAttribute('gpu-id'),
            "price": gpuPrices[i].value
        })
    }


    var data = {
      "preregisteredID":  vmID,
      "vmPrice": vmPrice,
      "gpu": gpuList
    }
    
    document.getElementById("sell-vm-modal-body").innerHTML = "Setting up your machine. Please wait..."

    var url = "/provider/vm";
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data))
    xhr.onreadystatechange = function(){
      // Operation is complete
      if(this.readyState==4){
        // Status : success
        if(this.status== 201){
            alert(JSON.parse(this.response).message)
            location.replace("/console/provider/dashboard")
          
        } else{
        // Status : fail
        document.getElementById("sell-vm-modal-body").innerHTML = "Failed";
        document.getElementById("sell-vm-modal-body").style.color = "red";

          alert(JSON.parse(this.response).message)
        }
      } 
    }
  }