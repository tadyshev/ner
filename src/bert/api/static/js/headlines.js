$(document).ready(function () {

    let categories = ['business',
        'entertainment',
        'general',
        'health',
        'science',
        'sports',
        'technology',
    ];

    categories.forEach(c => {
        $.get("/news", {category: c})
            .done(function (data) {
                spinner = document.getElementById(c+"-spinner");
                spinner.parentNode.removeChild(spinner)

                results = document.getElementById(c + "-ul");
                for (let i = 0; i < 5; i++) {
                    let li = document.createElement("li")
                    li.innerHTML = data[i]
                    results.appendChild(li)
                }
            });
    })


});