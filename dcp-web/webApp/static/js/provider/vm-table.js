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
                    fullInstanceDetailElement.style.display = "block";
                    fullInstanceDetailErrorElement.style.display = "none";
                    fullInstanceDetailElement.innerHTML = res.output;
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
    
//     alert(url)
//     http.open('GET', url, true);
//     http.onreadystatechange= function(){
//         if(http.readyState == 4){
//             var res = JSON.parse(http.response)
//             switch(http.status){
//                 case 200:
//                     output = res.output;
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

    function addElementByList(listInput, element){
        element.innerHTML = "";
        for(i =0; i<listInput.length; ++i){
            element.innerHTML += listInput[i]
            element.innerHTML += "<br>"
        }

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
                var url = "/provider/vm/"+vmID
                
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
                                
                                // VM name
                                document.getElementById("instance-detail-name").innerHTML = output.name;
                                
                                // VM IP address
                                document.getElementById("instance-detail-ip").innerHTML = output.ipAddress;
                                // Container
                                document.getElementById("instance-detail-container").innerHTML = output.numberOfContainers;
                                
                                // Total earnings
                                document.getElementById("instance-detail-earnings").innerHTML = output.dueEarnings + "/" + output.totalEarnings ;
                                
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
                                if(output.isHidden){
                                    document.getElementById("show-btn").style.display = 'inline-block';
                                    document.getElementById("hide-btn").style.display = 'none';
                                }
                                else{
                                    document.getElementById("show-btn").style.display = 'none';
                                    document.getElementById("hide-btn").style.display = 'inline-block';

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


function hideFromMarketplace(){
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    var url = "/provider/vm/"+vmID+"/hide";
    var http = new XMLHttpRequest();

    http.open('GET', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response)
            switch(http.status){
                case 200:
                    document.getElementById("show-btn").style.display = 'inline-block';
                    document.getElementById("hide-btn").style.display = 'none';
                    break;
                default:

                    alert(res.message);
                    break;
            }
        }
    }
    http.send();


}

function showOnMarketplace(){
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    var url = "/provider/vm/"+vmID+"/show";
    var http = new XMLHttpRequest();

    http.open('GET', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response)
            switch(http.status){
                case 200:
                    document.getElementById("show-btn").style.display = 'none';
                    document.getElementById("hide-btn").style.display = 'inline-block';
                    break;
                default:
                    alert(res.message);
                    break;
            }
        }
    }
    http.send();


}

function modifyOthersConfirm(){
    var priceInputElement = document.getElementById("instance-detail-price-input")
    var nameInputElement = document.getElementById("instance-detail-name-input")
    
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");

    var data = JSON.stringify({'name': nameInputElement.value, 'price': priceInputElement.value})
    var url = "/provider/vm/"+vmID;
    var http = new XMLHttpRequest();
    http.open('UPDATE', url, true);
    http.setRequestHeader('Content-Type', 'application/json');
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response)
            switch(http.status){
                case 202:
                    window.location.reload(false);

                    break;
                default:
                    var instanceDetailElement = document.getElementById("instance-detail");
                    var instanceDetailErrorElement = document.getElementById("instance-detail-err");

                    instanceDetailElement.style.display = "none";
                    instanceDetailErrorElement.style.display = "block";
                    instanceDetailErrorElement.style.color = "red";
                    instanceDetailErrorElement.innerHTML = res.message;
                    break;
            }
        }
    }
    http.send(data);
}

function modifyOthersClose(){
    var nameInputElement = document.getElementById("instance-detail-name-input");
    var nameElement = document.getElementById("instance-detail-name");

    var priceInputElement = document.getElementById("instance-detail-price-input");
    var priceElement = document.getElementById("instance-detail-price");

    nameInputElement.style.display = "none";
    nameElement.style.display = "block";
    
    priceInputElement.style.display = "none";
    priceElement.style.display = "block";

    document.getElementById("modify-btn-col").style.display = "none";
    document.getElementById("btn-col").style.display = "block";
}


function modifyOthers(){
    // Name
    var nameInputElement = document.getElementById("instance-detail-name-input")
    var nameElement = document.getElementById("instance-detail-name")
    var oldName = nameElement.innerHTML;
    
    // Price
    var priceInputElement = document.getElementById("instance-detail-price-input")
    var priceElement = document.getElementById("instance-detail-price")
    var oldPrice = priceElement.innerHTML;

    nameInputElement.style.display = "block";
    nameInputElement.setAttribute("value", oldName);
    nameElement.style.display = "none";
    

    priceInputElement.style.display = "block";
    priceInputElement.setAttribute("value", oldPrice);
    priceElement.style.display = "none";


    document.getElementById("modify-btn-col").style.display = "block";
    document.getElementById("btn-col").style.display = "none";


}

function modifyIP(){
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");
    var ip = document.getElementById("provider-modify-vm-ip").value;
    var url = '/console/provider/vm/marketplace/sell2?ip='+ip +"&vmID="+vmID;
    alert(url)
    window.location = url;
}

function terminateVM(){
    var vmID = document.getElementById("instance-detail").getAttribute("vm-id");

    var url = "/provider/vm/"+vmID;
    var http = new XMLHttpRequest();
    http.open('DELETE', url, true);
    http.onreadystatechange= function(){
        
        if(http.readyState == 4){
            var res = JSON.parse(http.response)
            alert(res.message)
            switch(http.status){
                
                case 203:
                    window.location.reload(true);
                    break;
                default:
                    break;
            }
        }
    }
    http.send();

}


// Call the dataTables jQuery plugin
$(document).ready(function() {
    $('#dataTable').DataTable();
    addVMTableRowHandlers();
  });
  
  