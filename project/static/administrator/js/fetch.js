
// var delete_btn = document.querySelector("#delete_btn")
// delete_btn.addEventListener('click', deleteFunction)

function deleteFunction(value){
	console.log(value)
	var element = document.querySelector('.'+value)
	var token = document.querySelector("input[name=csrfmiddlewaretoken]").value
	// var token = document.querySelector("#token").value
	// console.log(token)
	var url = 'http://127.0.0.1:9000/administrator/deleteposts/'
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
	console.log(token)
	var url = 'http://127.0.0.1:9000/administrator/viewdetails/'
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
		var data = JSON.parse(data.msg)
		var data = data[0].fields
		// var image = data.image
		var img_link = 'http://127.0.0.1:9000/media/'
		var img = img_link+ data.image

		document.querySelector("#post_img1").src = img
	document.querySelector("#main_img").src = img

	})
}
