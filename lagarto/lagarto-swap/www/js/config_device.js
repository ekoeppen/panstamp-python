/* Copyright (c) Daniel Berenguer (panStamp) 2012 */

/**
 * Update table fields
 */
function updateValues()
{
  var mote_addr = getUrlVars()["address"];

  var jsonDoc = getJsonDoc();
  var swapnet = jsonDoc.network;
  swapnet.motes.forEach(function(mote)
  {
	  if (mote.address == mote_addr)
	  document.getElementById("motename").value = mote.name;
	  document.getElementById("developer").value = mote.manufacturer;
	  document.getElementById("moteaddr").value = mote_addr;
  });
}