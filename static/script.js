"use strict";

  	let cbox=document.getElementById("cbox");
  	let texte=document.getElementById("texte");
  	cbox.onchange=function (ev) {
  		texte.value = cbox.value; 
  	};