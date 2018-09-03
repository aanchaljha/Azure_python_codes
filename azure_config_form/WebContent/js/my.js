function selectProjectPart(part) {
	if (part == "yes") {
		document.getElementById("programName").style.visibility='visible';
		document.getElementById("programNameValue").style.visibility='visible';
	}
	else{
		document.getElementById("programName").style.visibility='hidden';
		document.getElementById("programNameValue").style.visibility='hidden';
	}
}