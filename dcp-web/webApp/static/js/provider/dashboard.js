
var dashboardCTX = document.getElementById("dashboard-chart");
var fUnit = "HKD";

var chartData = JSON.parse(document.getElementById("dashboard-chart-data").dataset.xy);
var xData = []
var yData = []
for (const [key, value] of Object.entries(chartData)) {
  xData.push(key);
  yData.push(value);
}

createChart(dashboardCTX, xData, yData, fUnit, "");
