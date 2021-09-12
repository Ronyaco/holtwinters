var thisChart;


var graphsOptions = [
    {
      balloonText: "[[prediction]]",
      bullet: "round",
      title: "Prediction",
      valueField: "prediction",
      fillAlphas: 0,
      lineColor: "#31aeef",
      lineThickness: 2,
      negativeLineColor: "#31aeef",
      position: "top",
    },
    {
      balloonText: "[[values]]",
      bullet: "round",
      title: "Historical Data",
      valueField: "values",
      fillAlphas: 0,
      lineColor: "#9656e7",
      lineThickness: 2,
      negativeLineColor: "#c69cfd",
    },
  ];

  function buildData(data){
    var chart; 
    var response = JSON.parse(data);
    response.data.forEach((item) =>
      item.prediction == 0
        ? (item.prediction = undefined)
        : (item.prediction = item.prediction)
    );
    response.data.forEach((item) =>
      item.values == 0 ? (item.values = undefined) : (item.values = item.values)
    );
    return response.data; 
  }
  

function loadChart(data) {
  if ($("#amlinechart4").length) {
      chart = AmCharts.makeChart("amlinechart4", {
      type: "serial",
      theme: "light",
      legend: {
        useGraphSettings: true,
      },
      dataProvider: data,
      categoryField: "date",
      startDuration: 0.5,
      graphs: graphsOptions,
      chartCursor: {
        cursorAlpha: 0,
        zoomable: false,
      },
      categoryField: "date",
      indexAxis: {
        gridPosition: "date",
        axisAlpha: 0,
        fillAlpha: 0.05,
        fillColor: "#000000",
        gridAlpha: 0,
        position: "top",
      },
      export: {
        enabled: false,
      },
    });
  }
return chart;
}

function getData() {
  var request = {
    start_date: $("#start_date").val(),
    end_date: $("#end_date").val(),
  };
  return $.ajax({
    crossDomain: true,
    type: "POST",
    url: "http://127.0.0.1:5000/predict",
    data: JSON.stringify(request),
    contentType: "application/json",
    dataType: "json",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    success: function (response) {
      return response;
    },
  });
}

$("#prediction_button").click(function (e) {
    e.preventDefault();
 getData().then(function (data) {
      console.log(data);
      thisChart.dataProvider = buildData(data)
      thisChart.validateData();
    });

  });

function initChart() {
  getData().then(function (data) {
    console.log(data);
    thisChart = loadChart(buildData(data));
  });
}

initChart();
