function GetDistricts() {
  var s = document.getElementById("state");
  var state = s.value;
  var URL =
    "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + state;
  console.log(URL);

  var districtSelect = document.getElementById("district");
  districtSelect.innerHTML = "";
  var myOption = document.createElement("option");
  myOption.text = "Choose District";
  myOption.value = "";
  districtSelect.add(myOption);

  $.ajax({
    type: "GET",
    url: URL,
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
