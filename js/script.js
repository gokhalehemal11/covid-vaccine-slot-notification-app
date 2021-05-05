function GetDistricts() {
  var s = document.getElementById("state");
  var state = s.value;
  var URL =
    "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + state;

  var districtSelect = document.getElementById("district");
  districtSelect.innerHTML = "";
  var myOption = document.createElement("option");
  myOption.text = "Choose District";
  myOption.value = "";
  districtSelect.add(myOption);

  $.ajax({
    type: "GET",
    url: URL,
    timeout: 6000,
    error: function() {
      $("#errModal").modal("show");
    },
    success: function(data) {
      //console.log(data.districts);
      for (var k in data.districts) {
        var myOption = document.createElement("option");
        myOption.text = data.districts[k].district_name;
        myOption.value = data.districts[k].district_id;
        districtSelect.add(myOption);
      }
    },
    dataType: "json"
  });
}

function CheckAvl() {
  var pincode = document.getElementById("pincode").value;
  var date = document.getElementById("date");
  var sel_date = new Date(date.value)
    .toJSON()
    .slice(0, 10)
    .split("-")
    .reverse()
    .join("/");
  var agelimit = document.querySelector('input[name="radioopt"]:checked').value;
  var AvlRes = document.getElementById("avlres");
  AvlRes.innerHTML = "";

  if (pincode === "") {
    var dataLen = 0;
    var district = document.getElementById("district");
    var dist_id = district.value;

    var CalURL =
      "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" +
      dist_id +
      "&date=" +
      sel_date;

    $.ajax({
      type: "GET",
      url: CalURL,
      timeout: 6000,
      error: function() {
        $("#errModal").modal("show");
      },
      success: function(data) {
        dataLen = data.centers.length;
        var flag = false;
        if (dataLen > 0) {
          var avlslots = 0;
          var nearDate = "";
          var minage = "";

          for (var k in data.centers) {
            //console.log(data.centers[k].sessions);
            for (var session in data.centers[k].sessions) {
              //console.log(data.centers[k].sessions[session].min_age_limit, agelimit);
              if (
                data.centers[k].sessions[session].available_capacity === 0 ||
                data.centers[k].sessions[session].min_age_limit.toString() !==
                  agelimit
              ) {
                continue;
              }
              flag = true;
              avlslots = data.centers[k].sessions[session].available_capacity;
              nearDate = data.centers[k].sessions[session].date;
              minage = data.centers[k].sessions[session].min_age_limit;
            }
            if (flag) {
              var tr = document.createElement("tr");
              tr.innerHTML =
                "<td>" +
                data.centers[k].name +
                "</td><td>" +
                avlslots +
                "</td><td>" +
                nearDate +
                "</td>" +
                minage +
                "</td><td>";
              AvlRes.append(tr);
            }
          }
        } else {
          var tr = document.createElement("tr");
          tr.innerHTML =
            "<td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td>";
          AvlRes.append(tr);
        }
        if (!flag) {
          var tr = document.createElement("tr");
          tr.innerHTML =
            "<td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td>";
          AvlRes.append(tr);
        }
      },
      dataType: "json"
    });

    $("#myModal").modal("show");
  } else {
    var dataLen = 0;
    var CalURL =
      "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" +
      pincode +
      "&date=" +
      sel_date;

    $.ajax({
      type: "GET",
      url: CalURL,
      timeout: 6000,
      error: function() {
        $("#errModal").modal("show");
      },
      success: function(data) {
        dataLen = data.centers.length;
        var flag = false;
        if (dataLen > 0) {
          var avlslots = 0;
          var nearDate = "";
          var minage = "";

          for (var k in data.centers) {
            //console.log(data.centers[k].sessions);
            for (var session in data.centers[k].sessions) {
              //console.log(data.centers[k].sessions[session].min_age_limit, agelimit);
              if (
                data.centers[k].sessions[session].available_capacity === 0 ||
                data.centers[k].sessions[session].min_age_limit.toString() !==
                  agelimit
              ) {
                continue;
              }
              flag = true;
              avlslots = data.centers[k].sessions[session].available_capacity;
              nearDate = data.centers[k].sessions[session].date;
              minage = data.centers[k].sessions[session].min_age_limit;
            }
            if (flag) {
              var tr = document.createElement("tr");
              tr.innerHTML =
                "<td>" +
                data.centers[k].name +
                "</td><td>" +
                avlslots +
                "</td><td>" +
                nearDate +
                "</td>" +
                minage +
                "</td><td>";
              AvlRes.append(tr);
            }
          }
        } else {
          var tr = document.createElement("tr");
          tr.innerHTML =
            "<td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td>";
          AvlRes.append(tr);
        }
        if (!flag) {
          var tr = document.createElement("tr");
          tr.innerHTML =
            "<td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td><td>" +
            "N/A" +
            "</td>";
          AvlRes.append(tr);
        }
      },
      dataType: "json"
    });

    $("#myModal").modal("show");
  }
}

function SaveToDB() {
  console.log("ToDo");
  $("#myModal").modal("show");
}
