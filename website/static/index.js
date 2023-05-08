$(document).ready(function () {
  // add change event listener to the options
  $("#data_options").change(function () {
    // send an AJAX request to update the plot when options change
    $.ajax({
      url: "/",
      type: "POST",
      data: $("#select-form").serialize(),
      success: function (response) {
        $("#plot-div").html(response.plot_div);
      },
      error: function (error) {
        console.log(error);
      },
    });
  });

  // add change event listener to the time window dropdown
  $("#time-window").change(function () {
    // send an AJAX request to update the plot when time-window change
    $.ajax({
      url: "/",
      type: "POST",
      data: $("#select-form").serialize(),
      success: function (response) {
        $("#plot-div").html(response.plot_div);
      },
      error: function (error) {
        console.log(error);
      },
    });
  });

  // add click event listener to the refresh button
  $("#refresh-btn").click(function () {
    // send an AJAX request to refresh the plot when refresh button is being click
    $.ajax({
      url: "/",
      type: "POST",
      data: $("#select-form").serialize(),
      success: function (response) {
        $("#plot-div").html(response.plot_div);
      },
      error: function (error) {
        console.log(error);
      },
    });
  });

  // add click event listener to the download button
  $("#download-btn").click(function () {
    // Get the selected option from the dropdown
    var selected_option = $("#data_options").val();
    // send an AJAX request to  get the data as CSV
    $.ajax({
      url: "/download_csv",
      type: "POST",
      data: { data_options: selected_option },
      success: function (response) {
        // create a new temporary download link and trigger a click to start download
        response.map((resp) => {
          var link = document.createElement("a");
          link.href = "data:text/csv;charset=utf-8," + encodeURI(resp[1]);
          link.target = "_blank";
          link.download = resp[0] + ".csv";
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        });
      },
      error: function (error) {
        console.log(error);
      },
    });
  });
});
