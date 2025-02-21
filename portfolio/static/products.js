// State
const resultsDiv = document.querySelector("#results")
let skip = 0;
const previous = document.body.querySelector("#previousButton")
previous.style.visibility = "hidden"
const next = document.body.querySelector("#nextButton")
const shopDisplay = document.body.querySelector("#shopDisplay")

// Next button on click iterates to the next 30 items
// Hides when reached the last set of items
next.addEventListener("click", function (){
    skip+=30;
    previous.style.visibility = "visible"
    main();
    if (skip >= 180) {
        next.style.visibility = "hidden"
    }
})

// Previous button on click iterates to the previous 30 items
// Hidden on the first 30 items
previous.addEventListener("click", function (){
    skip-=30;
    main()
    if (skip == 0){
        previous.style.visibility = "hidden"
    }
    next.style.visibility = "visible"
})

// Get's all products from dummyjson
// Skips according to the next/previous buttons
async function getAllProducts(){
    let response = await fetch(`https://dummyjson.com/products?skip=${skip}`);
    let data = await response.json();
    return data;
}

// Main function firstly sets innerHTML to empty so when the next/prev.
// Buttons are pressed they are "removed"
// This function fills the resultsDiv using DOM manipulation
async function main()
{
    resultsDiv.innerHTML = ""

    let allProducts = await getAllProducts();
    console.log(allProducts);
    console.log(allProducts.products[2].id);
    for (let i = 0; i < allProducts.products.length; i++){
        let card = document.createElement("div");
        let img = document.createElement("img");
        let info = document.createElement("div");
        let title = document.createElement("h4");
        let price = document.createElement("h5");
        let p = document.createElement("p");


        // Img dimensions
        img.style = "height: 200px; width: 200px;"


        // classes added
        card.classList.add("card");
        img.classList.add("itemImg");
        info.classList.add("info");
        price.classList.add("price");
        p.classList.add("description");


        // src changed
        img.src = `${allProducts.products[i].images}`
        p.innerText = `${allProducts.products[i].description}`;
        price.innerHTML = `Price: ${allProducts.products[i].price}`;
        title.innerText = allProducts.products[i].title;
        img.alt = `Image of ${allProducts.products[i].title}`

        // appending
        resultsDiv.append(card);
        card.append(img);
        card.append(info);
        info.append(title);
        info.append(price);
        info.append(p);
    }
}

main()
