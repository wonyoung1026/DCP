function visualizeCPUUtil(xData, yData){
  
  var cpuUtilCTX = document.getElementById("vm-cpu-util-chart");
  var bUnit = "%";

  createChart(cpuUtilCTX, xData, yData, "", bUnit);
}

function visualizeMemoryUtil(xData, yData){
  var memoryUtilCTX = document.getElementById("vm-memory-util-chart");
  var bUnit = "%";
  createChart(memoryUtilCTX, xData, yData, "",bUnit);
}
function visualizeNetwork(xData, yData){
  var networkCTX = document.getElementById("vm-network-chart");
  var bUnit = "B/s";
  createChart(networkCTX, xData, yData, "", bUnit);
}

function visualizeNumberOfContainers(xData, yData){
  var networkCTX = document.getElementById("vm-number-of-containers-chart");
  var bUnit = "";
  createChart(networkCTX, xData, yData, "", bUnit);
}
