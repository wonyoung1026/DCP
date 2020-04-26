function getFullInstanceDetail(){
    // Hide other cards and display Full Instance Detail Card
    document.getElementById("full-instance-detail-card").style.display = "block";
    document.getElementById("instance-detail-card").style.display = "none";
    document.getElementById("monitoring-card").style.display = "none";

    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    
    
    var url = "/user/vm/"+vmID+"/full";
    
    // Indicate searching
    var fullInstanceDetailElement = document.getElementById("full-instance-detail");
    var fullInstanceDetailErrorElement = document.getElementById("full-instance-detail-err");
    
    fullInstanceDetailElement.style.display = "none";
    fullInstanceDetailErrorElement.style.display = "block";
    fullInstanceDetailErrorElement.style.color = "black";
    fullInstanceDetailErrorElement.innerHTML = "Searching...";
    
    var http = new XMLHttpRequest();
    http.open('GET', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response);
            switch(http.status){
                case 200:
                    var output = res.output;
                    
                    fullInstanceDetailElement.style.display = "block";
                    fullInstanceDetailErrorElement.style.display = "none";
                    fullInstanceDetailElement.innerHTML = output;
                    break;
                default:
                    fullInstanceDetailElement.style.display = "none";
                    fullInstanceDetailErrorElement.style.display = "block";
                    fullInstanceDetailErrorElement.style.color = "red";
                    fullInstanceDetailErrorElement.innerHTML = res.message;
                    break;
            }
        }
    }
    http.send();
}


function getInstanceDetail(){
    // Hide other cards and display Full Instance Detail Card
    document.getElementById("instance-detail-card").style.display = "block";
    document.getElementById("full-instance-detail-card").style.display = "none";
    document.getElementById("monitoring-card").style.display = "none";
}

function getMonitoring(){
    // Hide other cards and display Full Instance Detail Card

    document.getElementById("monitoring-card").style.display = "block";
    document.getElementById("instance-detail-card").style.display = "none";
    document.getElementById("full-instance-detail-card").style.display = "none";
    
    var iframeElement = document.getElementById("monitoring-iframe")
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");

    // Get url 
    var http = new XMLHttpRequest();
    var url = "/user/vm/"+vmID+"/monitor"
    http.open('GET', url, true);
    http.onreadystatechange = function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response);
            iframeElement.src = res.output;
        }
    }
    http.send()
}

// =============================================
// Deprecated
// =============================================
// function getMonitoring(){
//     // Hide other cards and display Full Instance Detail Card
//     document.getElementById("monitoring-card").style.display = "block";
//     document.getElementById("instance-detail-card").style.display = "none";
//     document.getElementById("full-instance-detail-card").style.display = "none";

//     var monitoringElement = document.getElementById("monitoring");
//     var monitoringErrorElement = document.getElementById("monitoring-err");
    
//     var http = new XMLHttpRequest();
//     var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
//     var url = "/user/vm/"+vmID+"/monitoring";
    
//     http.open('GET', url, true);
//     http.onreadystatechange= function(){
//         if(http.readyState == 4){
//             var res = JSON.parse(http.response)
//             switch(http.status){
//                 case 200:
//                     output = res['output'];
//                     console.log(output)
//                     visualizeCPUUtil(output['time'], output["cpuUtils"])
//                     visualizeMemoryUtil(output['time'], output["memoryUtils"])
//                     visualizeNetwork(output['time'], output["networks"])
//                     visualizeNumberOfContainers(output['time'],output['numOfContainers'])
//                     break;
//                 default:
                    
//                     monitoringElement.style.display = "none";
//                     monitoringErrorElement.style.display = "block";
//                     monitoringErrorElement.style.color = "red";
//                     monitoringErrorElement.innerHTML = res.message;

//                     break;
//             }
//         }
//     }
//     http.send();
// }

function addElementByList(listInput, element){
    element.innerHTML = "";
    for(i =0; i<listInput.length; ++i){
        element.innerHTML += listInput[i]
        element.innerHTML += "<br>"
    }

}


function addVMTableRowHandlers(){
    var table = document.getElementById("vm-table");
    var rows = table.getElementsByTagName("tr");

    function addStatus(intStatus, element){
        switch(intStatus){
            case 0:
                element.innerHTML = "<span class='btn btn-success'></span> Running";
                break;
            case 1:
                element.innerHTML = "<span class='btn btn-primary'></span> Pending";
                break;
            case 2:
                element.innerHTML = "<span class='btn btn-warning'></span> Unstable";
                break;
            case 3:
                element.innerHTML = "<span class='btn btn-danger'></span> Disconnected";
                break;
            default:
                break;
    
        }
    
    }
    function addGPU(listGPU, element){
        element.innerHTML = "";
        for(i =0; i<listGPU.length; ++i){
            element.innerHTML += "<span class='col-md-1 instance-detail-inner-key'>Processor</span>"
            element.innerHTML += "<span class='col-md-3 instance-detail-inner-value'>" + listGPU[i]["processor"] +"</span>"
            element.innerHTML += "<span class='col-md-1 instance-detail-inner-key'>Price</span>"
            element.innerHTML += "<span class='col-md-3 instance-detail-inner-value'>"+ listGPU[i]['price'] +"</span>"
            element.innerHTML += "<span class='col-md-1 instance-detail-inner-key'>Status</span>"
            element.innerHTML += "<span class='col-md-3 instance-detail-inner-value'>"+ addGPUStatus(listGPU[i]['status'])+"</span>"
            element.innerHTML += "<br>"
    
        }
    }
    function addGPUStatus(intStatus){
        html = ""
        switch(intStatus){
            case 0:
                html += "<span class='btn btn-primary'></span> Vacant";
                break;
            case 1:
                html +=  "<span class='btn btn-danger'></span> Occupied";
                break;
        }
        return html
    }

    for (i=0; i< rows.length; i++){
        var currentRow = table.rows[i];
        var createClickHandler = function(row) {
            return function(){
                // Hide other cards
                document.getElementById("instance-detail-card").style.display = "block";
                document.getElementById("monitoring-card").style.display = "none";
                document.getElementById("full-instance-detail-card").style.display = "none";
                
                // Indicate searching
                var instanceDetailElement = document.getElementById("instance-detail");
                var instanceDetailErrorElement = document.getElementById("instance-detail-err");
                
                var vmID = row.getAttribute("vm-id");
                instanceDetailElement.setAttribute("vm-id", vmID);

                instanceDetailElement.style.display = "none";
                instanceDetailErrorElement.style.display = "block";
                instanceDetailErrorElement.style.color = "black";
                instanceDetailErrorElement.innerHTML = "Searching...";

                
                var http = new XMLHttpRequest();
                var url = "/user/vm/"+vmID
                
                // set vm-id as attribute to 
                
                http.open('GET', url, true);
                http.onreadystatechange = function(){
                    if(http.readyState == 4){
                        var res = JSON.parse(http.response);
                        switch(http.status){
                            // Load vm details on success
                            case 200:
                                instanceDetailElement.style.display = "block";
                                instanceDetailErrorElement.style.display = "none";
                            
                                var output = res.output;
                                console.log(output);
                                
                                // VM id
                                document.getElementById("instance-detail-instance-id").innerHTML = output.id;
                                
                                // Provider email
                                document.getElementById("instance-detail-provider-email").innerHTML = output.providerEmail;
                                
                                // Number of cores
                                document.getElementById("instance-detail-core").innerHTML = output.processor.length;

                                // Processor
                                var processorElement = document.getElementById("instance-detail-processor");
                                addElementByList(output.processor, processorElement);

                                // Memory
                                var memoryElement = document.getElementById("instance-detail-memory");
                                addElementByList(output.memory, memoryElement);
                                
                                // Memory
                                var diskElement = document.getElementById("instance-detail-disk");
                                addElementByList(output.disk, diskElement);

                                // GPU
                                var gpuElement = document.getElementById("instance-detail-gpu");
                                addGPU(output.gpu, gpuElement);
                                
                                // Price
                                document.getElementById("instance-detail-price").innerHTML = output.price;

                                // Status
                                var statusElement = document.getElementById("instance-detail-status");
                                addStatus(output.status, statusElement);

                                // Number of disconnections
                                document.getElementById("instance-detail-disconnection").innerHTML = output.numberOfDisconnections;
                                
                                // Registered Time
                                document.getElementById("instance-detail-registered-time").innerHTML = output.createdOn;
                                
                                // Add to my list button
                                if(output.isFavorite){
                                    document.getElementById("delete-favorite-btn").style.display = 'block';
                                    document.getElementById("add-favorite-btn").style.display = 'none';
                                }
                                else{
                                    document.getElementById("delete-favorite-btn").style.display = 'none';
                                    document.getElementById("add-favorite-btn").style.display = 'block';
                                }
                                break;
                            default:
                                instanceDetailElement.style.display = "none";
                                instanceDetailErrorElement.style.display = "block";
                                instanceDetailErrorElement.style.color = "red";
                                instanceDetailErrorElement.innerHTML = res.message;
                                break;
                        }
                    } 
                    
                }
                http.send();


            }
        }
        currentRow.onclick = createClickHandler(currentRow);
    }
}

function addToFavorites(){
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    var url = "/user/vm/"+vmID+"/favorite";
    var http = new XMLHttpRequest();
    
    http.open('POST', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var modalBody = document.getElementById("add-to-list-modal-body");
            var res = JSON.parse(http.response)
            switch(http.status){
                case 201:
                    document.getElementById("delete-favorite-btn").style.display = 'block';
                    document.getElementById("add-favorite-btn").style.display = 'none';
                    break;
                default:
                    modalBody.innerHTML = res.message;
                    break;
            }
        }
    }
    http.send();

}

function deleteFromFavorites(){
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    var url = "/user/vm/"+vmID+"/favorite";
    var http = new XMLHttpRequest();

    http.open('DELETE', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var modalBody = document.getElementById("delete-from-list-modal-body");
            var res = JSON.parse(http.response)
            switch(http.status){
                case 203:
                    document.getElementById("delete-favorite-btn").style.display = 'none';
                    document.getElementById("add-favorite-btn").style.display = 'block';
                    break;
                default:
                    modalBody.innerHTML = res.message;
                    break;
            }
        }
    }
    http.send();

}

// --------------------------------------------------------
// Buyer purchase flow
// --------------------------------------------------------
function getBaseImageModal(){
    var url = "/user/vm/base-image";
    var http = new XMLHttpRequest();

    http.open('GET', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var baseImageDropdownElement = document.getElementById("base-image-modal-dropdown");
            var res = JSON.parse(http.response)
            switch(http.status){
                case 200:
                    var baseImages = res.output;
                    console.log(baseImages);
                    baseImageDropdownElement.innerHTML = "";
                    for (i = 0; i<baseImages.length; ++i){
                        baseImageDropdownElement.innerHTML += 
                        "<a base-image-name="+baseImages[i].name+ " base-image-id="+baseImages[i].id+" class='dropdown-item' href='javascript:void(0)''> \
                        <span style='font-weight:bold;'>"+baseImages[i].name+"</span> \
                        <br> \
                        <span>" + baseImages[i].description+"</span> \
                        </a>"
                    }
                    addBaseImageDropdownRowHandlers();
                    break;
                default:
                    modalBody.innerHTML = res.message;
                    break;
            }
        }
    }
    http.send();
}

function addBaseImageDropdownRowHandlers(){
    var dropdown = document.getElementById("base-image-modal-dropdown");
    var rows = dropdown.getElementsByTagName("a");
    var dropdownMenuButton = document.getElementById("dropdownMenuButton");
    var gpuModalButton = document.getElementById("get-select-gpu-modal-button");

    for (i=0; i<rows.length; i++){
        var currentRow = rows[i];

        var createClickHandler = function(row){
            return function(){
                var baseImageID = row.getAttribute("base-image-id");
                dropdownMenuButton.setAttribute("selected-id", baseImageID);
                dropdownMenuButton.innerHTML = row.getAttribute("base-image-name");
                gpuModalButton.setAttribute("data-toggle", "modal");
                gpuModalButton.setAttribute("data-target", "#selectGPUModal");
                gpuModalButton.setAttribute("data-dismiss", "modal");
            }
        }
        currentRow.onclick = createClickHandler(currentRow);
    }

}

function getGPUModal(){
    // validate 
    var selectedID = document.getElementById("dropdownMenuButton").getAttribute("selected-id");
    if(!selectedID){
        var selectBaseImageModalErr = document.getElementById("err-select-base-image-modal");
        selectBaseImageModalErr.innerHTML = "Please select a base image"
        return 
    }

    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    var selectGPUModalBody = document.getElementById("select-gpu-modal-body")
    selectGPUModalBody.innerHTML = "Loading GPUs..."
    var url = "/buyer/vm/"+vmID +"/gpu"
    var http = new XMLHttpRequest();

    http.open('GET', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response)
            selectGPUModalBody.innerHTML=""
            switch(http.status){
                case 200:
                    var gpuList = res.output;
                    console.log(gpuList)
                    if (gpuList.length == 0){
                        selectGPUModalBody.innerHTML = "No GPU!";
                        break;
                    }
                    selectGPUModalBody.innerHTML = ""
                    for (i=0;i<gpuList.length; i++){
                        if(gpuList[i].status == 0){
                            selectGPUModalBody.innerHTML += 
                            "<div class='funkyradio-default'> \
                                <input type='checkbox' name='checkbox' processor="+gpuList[i].processor+" id="+gpuList[i].id+" price="+gpuList[i].price+" /> \
                                <label for="+gpuList[i].id+">"+gpuList[i].processor+" [HKD"+gpuList[i].price+"]</label>\
                            </div> \
                            "

                        }
                        else{
                            selectGPUModalBody.innerHTML += 
                            "<div class='funkyradio-danger'> \
                                <input disabled='disabled' type='checkbox' name='checkbox' id="+gpuList[i].id+" /> \
                                <label for="+gpuList[i].id+">"+gpuList[i].processor+" [HKD"+gpuList[i].price+"]</label>\
                            </div> \
                            "
                        }
                    }
                    break;
                default:

                    break;
            }

        }
    }
    http.send();
}

function getConfirmPurchaseModal(){
    var checkboxList = document.getElementById("select-gpu-modal-body").getElementsByTagName("input");
    var confirmPriceList = document.getElementById("confirm-price-list");
    var instanceDetailPrice = parseInt(document.getElementById("instance-detail-price").innerHTML);
    var totalPrice = instanceDetailPrice;

    confirmPriceList.innerHTML =               
    "<div class='row'> \
    <div class='col-md-2'></div> \
    <div class='col-md-6' style='font-weight:bold;'> \
      Provider basic rate : \
    </div> \
    <div class='col-md-4'> \
    HKD " + instanceDetailPrice +" \
    </div> \
    </div> \
    "

    for (i =0; i<checkboxList.length; ++i){
        if (checkboxList[i].checked){
            var price = checkboxList[i].getAttribute("price")
            var processor = checkboxList[i].getAttribute("processor")

            confirmPriceList.innerHTML += 
            "<div class='row' > \
            <div class='col-md-2'></div> \
            <div class='col-md-6' style='font-weight:bold;'> \
                GPU #"+i+ "  "+ processor+"  \
            </div> \
            <div class='col-md-4' > \
                HKD "+ price+" \
            </div> \
            </div>"
            totalPrice += parseInt(price);

        }

    }

    confirmPriceList.innerHTML +=
    "<br> \
    <div class='row' > \
    <div class='col-md-5'></div> \
    <div class='col-md-3' style='font-weight:bold;'> \
        Total Price  \
    </div> \
    <div class='col-md-4' style='font-weight:bold'> \
        HKD "+ totalPrice+" \
    </div> \
    </div>"
}
function confirmPurchase(){
    var checkboxList = document.getElementById("select-gpu-modal-body").getElementsByTagName("input");
    var gpuIDs = []
    for (i=0;i<checkboxList.length; i++){
        if (checkboxList[i].checked){
            gpuIDs.push(checkboxList[i].getAttribute("id"));
        }
    }
    
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    var baseImageID = document.getElementById("dropdownMenuButton").getAttribute("selected-id");
    
    // Loading
    document.getElementById("final-confirmation-modal-body").style.color = "black";
    document.getElementById("final-confirmation-modal-body").innerHTML = "Processing your request...";
    
    
    var url = "/buyer/vm/purchase"
    var http = new XMLHttpRequest();
    var data = JSON.stringify({'virtualMachineID': vmID, 'gpuIDs': gpuIDs, 'baseImageID': baseImageID})
    
    http.open('POST', url, true);
    http.setRequestHeader('Content-Type', 'application/json');
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response);
            switch(http.status){
                case 201:
                    document.getElementById("final-confirmation-modal-body").style.color = "black";
                    document.getElementById("final-confirmation-modal-body").innerHTML = res.message;
                    break;
                default:
                    document.getElementById("final-confirmation-modal-body").style.color = "red";
                    document.getElementById("final-confirmation-modal-body").innerHTML = res.message;
                    break;
            }
        }
    }
    http.send(data);

}
// --------------------------------------------------------
// Call the dataTables jQuery plugin
// --------------------------------------------------------
$(document).ready(function() {
    $('#dataTable').DataTable();
    addVMTableRowHandlers();
  });
  
  