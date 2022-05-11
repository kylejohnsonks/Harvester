//Add Solution Reading function 
function add_sr(event) {
  // event.preventDefault();
  let values = [];
  for (const feature of [].slice.call(document.getElementsByClassName("add_sr"))){
    values.push(feature.value);
  }
  // console.log(values);
  url = '/measurements/solution/';
  for (const value in values) {
    url+=values[value]+'/';
  }
  url=url.slice(0,-1);
  console.log(url)
  // window.location.href=url;
  fetch(url)
    .then(response => response.json())
    // .then(result => console.log(result))
    .then(result=>document.getElementById("result").innerHTML='<h4>'+result+'</h4>');
  }
//watch for Button click 
d3.select("#add_sr_button").on("click", add_sr);


//Add Seed Lot function 
function add_sl(event) {
  // event.preventDefault();
  let values = [];
  for (const feature of [].slice.call(document.getElementsByClassName("add_seed_lot"))){
    values.push(feature.value);
  }
  // console.log(values);
  url = '/measurements/seedlot/';
  for (const value in values) {
    url+=values[value]+'/';
  }
  url=url.slice(0,-1);
  // window.location.href=url;
  fetch(url)
    .then(response => response.json())
    // .then(result => console.log(result))
    .then(result=>document.getElementById("result").innerHTML='<h4>'+result+'</h4>');
  }
//watch for Button click 
d3.select("#add_sl_button").on("click", add_sl);

//Populate Drop down menus
async function dropdowns(event) {
  let response = await fetch('/dropdowns')
  let dropdowns = await response.json()
  console.log(dropdowns.pt_ids, dropdowns.pt_types, dropdowns.pt_varieties)

  //build plant types options list
  for (i=0; i < dropdowns.pt_types.length; i++){
    var opt = document.createElement("option");
    document.getElementById("plant_type").innerHTML += '<option id="' + i + '" value="' + dropdowns.pt_types[i] + '">'+dropdowns.pt_types[i]+'</option>';
  }
  //build plant varieties options list
  for (i=0; i < dropdowns.pt_varieties.length; i++){
    var opt = document.createElement("option");
    document.getElementById("plant_variety").innerHTML += '<option id="' + i + '" value="' + dropdowns.pt_varieties[i] + '">'+dropdowns.pt_varieties[i]+'</option>';
  }    
}
//fetch dropdown info on page load
d3.select(window).on("load", dropdowns)





//add varieties and provinces variables
// var varieties = ['Barbera','Bordeaux-style Red Blend','Bordeaux-style White Blend','Cabernet Franc','Cabernet Sauvignon','Champagne Blend','Chardonnay','Corvina','Dolcetto','Garganega','Gewurztraminer','Glera','Grenache','Malbec','Meritage','Merlot','Moscato','Mourvedre','Nebbiolo','Nero dAvola','Petit Verdot','Petite Sirah','Pinot Blanc','Pinot Grigio','Pinot Gris','Pinot Noir','Red Blend','Rhone-style Red Blend','Rhone-style White Blend','Riesling','Rose','Sangiovese','Sangiovese Grosso','Sauvignon Blanc','Sparkling Blend','Syrah','Tempranillo','Vermentino','Viognier','White Blend','Zinfandel']
// var provinces = ['Alsace','Aquitaine','Burgundy','California','Champagne-Ardenne','New York','Oregon','Piemonte','Sicilia','Tuscany','Veneto','Washington']

// //build provinces options list
// for (i=0; i < provinces.length; i++){
//   var opt = document.createElement("option");
//   document.getElementById("provops").innerHTML += '<option id="' + i + '" value="' + provinces[i] + '">'+provinces[i]+'</option>';
// }

// //build varieties options list
// for (i=0; i < varieties.length; i++){
//   var opt = document.createElement("option");
//   document.getElementById("vrtyops").innerHTML += '<option id="' + i + '" value="' + varieties[i] + '">'+varieties[i]+'</option>';
// }