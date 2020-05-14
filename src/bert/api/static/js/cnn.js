$(document).ready(function(){

	let categories = ['us', 'world', 'politics', 'business', 'opinion', 'health', 'entertainment', 'style', 'travel'];

	categories.forEach( c => {
		$.get("/cnn", {category:c})
		.done(function (data){
			results = document.getElementById(c+"-ul");
			for (let i=0; i<5; i++){
				let li = document.createElement("li")
				li.innerHTML = data[i]
				results.appendChild(li)
			}
			console.log(data);
		});
	})
	
	
});
// $(document).ready(function(){
	
// 	$.get("/cnn", {category:'world'})
// 		.done(function (data){
// 			results = document.getElementById("world-ul");
// 			for (let i=0; i<5; i++){
// 				let li = document.createElement("li")
// 				li.innerHTML = data[i]
// 				results.appendChild(li)
// 			}
// 			console.log(data);
// 		});
// });
// $(document).ready(function(){
	
// 	$.get("/cnn", {category:politics})
// 		.done(function (data){
// 			results = document.getElementById("results");
// 			results.innerHTML = data;
// 			console.log(data);
// 		});
// });
// $(document).ready(function(){
	
// 	$.get("/cnn", {category:us})
// 		.done(function (data){
// 			results = document.getElementById("results");
// 			results.innerHTML = data;
// 			console.log(data);
// 		});
// });
// $(document).ready(function(){

// $.get("/cnn", {category:us})
// 	.done(function (data){
// 		results = document.getElementById("results");
// 		results.innerHTML = data;
// 		console.log(data);
// 	});
// });