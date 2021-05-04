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

function CheckAvl(){
  var district = document.getElementById("district");
  var date= document.getElementById("date");
  
  var dist_id= district.value
  var sel_date= new Date(date.value).toJSON().slice(0,10).split('-').reverse().join('/')
  var URL =
    "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" +dist_id+"&date="+sel_date;
  
  $.ajax({
    type: "GET",
    url: URL,
    success: function(data) {
      console.log(data);
    },
    dataType: "json"
  });
  
}

function SaveToDB(){
  console.log("ToDo");
}