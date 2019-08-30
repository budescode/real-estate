
// var delete_btn = document.querySelector("#delete_btn")
// delete_btn.addEventListener('click', deleteFunction)

var plan = document.querySelector("#plan_img")
var post_img1 = document.querySelector("#post_img1")
plan.addEventListener("click", changeImg)
post_img1.addEventListener("click", changeImg)


function changeImg(){
document.querySelector("#main_img").src = this.src
}


function deleteFunction(value){
	console.log(value)
	var data = "post"+value
	var element = document.querySelector("[class= " +  data+ "]")
	element.remove()
	var token = document.querySelector("input[name=csrfmiddlewaretoken]").value
	// var token = document.querySelector("#token").value
	console.log(token)
	var url = 'http://anandrathi.pythonanywhere.com/administrator/deleteposts/'
	let  formData = new FormData()
	formData.append('post_pk', value)


	fetch(url,
	{
	body: new URLSearchParams(formData),
	method: 'post',
	headers:{
	'X-CSRFTOKEN': token
	}


	}).then(res => res.json()).then(function(data) {

		console.log(data)
	})
}
function viewDetails(value){

	var token = document.querySelector("input[name=csrfmiddlewaretoken]").value
	// var token = document.querySelector("#token").value
	console.log(value)
	var url = 'http://anandrathi.pythonanywhere.com/administrator/viewdetails/'
	let  formData = new FormData()
	formData.append('post_pk', value)


	fetch(url,
	{
	body: new URLSearchParams(formData),
	method: 'post',
	headers:{
	'X-CSRFTOKEN': token
	}


	}).then(res => res.json()).then(function(data) {
		var qs = JSON.parse(data.data)
		var data = qs[0].fields
		var pk = qs.pk
		// var image = data.image

		var img_link = 'http://anandrathi.pythonanywhere.com/media/'
		var img = img_link+ data.image


		document.querySelector("#post_img1").src = img
		// document.querySelector("#post_img1").src = img
		document.querySelector("#plan_img").src = img_link+data.plan
		document.querySelector("#main_img").src = img
		document.querySelector("#address").innerHTML = data.address
		document.querySelector("#property_type").innerHTML = data.Property_type
		document.querySelector("#Price").innerHTML = data.Price
		// document.querySelector("#user").innerHTML = data.Price
		document.querySelector("#Bedrooms").innerHTML = data.Bedrooms
		document.querySelector("#Bathrooms").innerHTML = data.Bathrooms
		document.querySelector("#Car_spaces").innerHTML = data.Car_spaces
		document.querySelector("#new_or_established").innerHTML = data.new_or_established

		document.querySelector("#Swimming_pool").innerHTML = data.Swimming_pool
		document.querySelector("#Garage").innerHTML = data.Garage
		document.querySelector("#Balcony").innerHTML = data.Balcony
		document.querySelector("#Outdoor_area").innerHTML = data.Outdoor_area
		document.querySelector("#Undercover_parking").innerHTML = data.Undercover_parking

		document.querySelector("#Shed").innerHTML = data.Shed
		document.querySelector("#Fully_fenced").innerHTML = data.Fully_fenced
		document.querySelector("#Outdoor_spa").innerHTML = data.Outdoor_spa
		document.querySelector("#Tennis_court").innerHTML = data.Tennis_court
		document.querySelector("#Ensuite").innerHTML = data.Ensuite

		document.querySelector("#DishWasher").innerHTML = data.DishWasher
		document.querySelector("#Study").innerHTML = data.Study
		document.querySelector("#Built_in_robes").innerHTML = data.Built_in_robes
		document.querySelector("#Alarm_system").innerHTML = data.Alarm_system
		document.querySelector("#Broadband").innerHTML = data.Broadband

		document.querySelector("#Floorboards").innerHTML = data.Floorboards
		document.querySelector("#Gym").innerHTML = data.Gym
		document.querySelector("#Rumpus_room").innerHTML = data.Rumpus_room
		document.querySelector("#Workshop").innerHTML = data.Workshop
		document.querySelector("#Air_conditioning").innerHTML = data.Air_conditioning

		document.querySelector("#Solar_panels").innerHTML = data.Solar_panels
		document.querySelector("#Heating").innerHTML = data.Heating
		document.querySelector("#High_energy_efficiency").innerHTML = data.High_energy_efficiency
		document.querySelector("#Water_tank").innerHTML = data.Water_tank
		document.querySelector("#Solar_hot_water").innerHTML = data.Solar_hot_water



	})
}
