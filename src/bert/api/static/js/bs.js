
$("#submit").click(function(){
    let input_text = $("#textbox").val();
    $.get("/predict", {text:input_text})
        .done(function (data){
            results = document.getElementById("results");
            results.innerHTML = data;
            console.log(data);
        });
});

