window.addEventListener('load', hideCategoryForm)
const select_category = document.querySelector('#id_category')
const category_form = document.querySelector('#div_id_brand')
const register_button = document.querySelector('#register_button')
const select_brand = document.querySelector('#id_brand')
const phone_number = document.querySelector('#id_phone_number')





// const select = document.querySelector('#id_select')

select_category.addEventListener('change', Category)
select_brand.addEventListener('change', Brand)
phone_number.addEventListener('input', ValidatePhone)


function Category(){
	const register_button = document.querySelector('#register_button')

	var selectIndex = document.querySelector('#id_category').selectedIndex;
	var selected = document.querySelector('#id_category').options[selectIndex].text;
	var brandIndex = document.querySelector('#id_brand').selectedIndex;
	var brand = document.querySelector('#id_brand').options[brandIndex].text;
	
	// register_button.removeAttribute("disabled");
	if(selected == 'Seller' && brand=='---------'){
		register_button.disabled = true
	}
	else{
		register_button.disabled = false
	}


	console.log(selected, brand)
	if (selected == 'Seller'){
		category_form.style.display='block';


	}

	// if (selected == 'Buyer'){
	// 	category_form.style.display='none';


	// }
	else{
		category_form.style.display='none';	
	}
}

function hideCategoryForm(){

	const number_hint = document.querySelector('#hint_id_phone_number')
	var paragraph = document.createElement("P"); 

	var textnode = document.createTextNode("Write a complete phone number");         // Create a text node
 
	                           // Append the text to <li>
	var paragraph2 = document.createElement("P"); 
	var textnode2 = document.createTextNode("Phone numbers must start with +910");         // Create a text node to make sure phone number is a number
	paragraph2.appendChild(textnode2)
	 
	                              // Append the text to <li>
	paragraph.appendChild(textnode);                              // Append the text to <li>
	number_hint.appendChild(paragraph); 
	number_hint.appendChild(paragraph2); 

	// document.querySelector('#hint_id_phone_number p').style.color = 'red';

	$("#hint_id_phone_number p:nth-child(1)").css("color", "red");
	$("#hint_id_phone_number p:nth-child(2)").css("color", "red");

	$("#hint_id_phone_number p:nth-child(1)").css("display", "none");
	$("#hint_id_phone_number p:nth-child(2)").css("display", "none");


	 
	var selectIndex = document.querySelector('#id_category').selectedIndex;
	var selected = document.querySelector('#id_category').options[selectIndex].text;
	console.log(selected)
	if (selected == 'Seller'){
		category_form.style.display='block';


	}

	// if (selected == 'Buyer'){
	// 	category_form.style.display='none';


	// }
	else{
		category_form.style.display='none';	
	}
	console.log('Hidden')

}

function Brand(){
	const register_button = document.querySelector('#register_button')
	const selectIndex = document.querySelector('#id_category').selectedIndex;
	const selected = document.querySelector('#id_category').options[selectIndex].text;
	const brandIndex = document.querySelector('#id_brand').selectedIndex;
	const brand = document.querySelector('#id_brand').options[brandIndex].text;

	if (selected=='Seller' && brand !='---------'){
		register_button.disabled=false

	}
	else{
		register_button.disabled=true
	}
	
	
}

function ValidatePhone(){
	const phone_number = document.querySelector('#id_phone_number').value.length
	const phone_number_value = document.querySelector('#id_phone_number').value
	const first_number = phone_number_value.slice(0, 4)
	const register_button = document.querySelector('#register_button')

	if (phone_number != 13){
		document.querySelector('#register_button').disabled=true
		
		document.querySelector('#hint_id_phone_number p').style.display = 'block';
		
	}
	else if (phone_number == 13){
		console.log('ok')
		document.querySelector('#hint_id_phone_number p').style.display = 'none';
		register_button.disabled=false
	}

	if (first_number != "+910"){
		$("#hint_id_phone_number p:nth-child(2)").css("display", "block");
		register_button.disabled=true
	}
	else{
		$("#hint_id_phone_number p:nth-child(2)").css("display", "none");
		register_button.disabled=false
	}
	console.log(first_number, phone_number)

}