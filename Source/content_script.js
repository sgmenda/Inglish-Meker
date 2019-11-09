const url = chrome.runtime.getURL('mapping.json');

let mapping = {}

fetch(url)
    .then((response) => response.json())
    .then((json) => {mapping = json; walk(document.body);});

function walk(node) 
{
	// I stole this function from here:
	// http://is.gd/mwZp7E
	
	var child, next;
	
	var tagName = node.tagName ? node.tagName.toLowerCase() : "";
	if (tagName == 'input' || tagName == 'textarea') {
		return;
	}
	if (node.classList && node.classList.contains('ace_editor')) {
		return;
	}

	switch ( node.nodeType )  
	{
		case 1:  // Element
		case 9:  // Document
		case 11: // Document fragment
			child = node.firstChild;
			while ( child ) 
			{
				next = child.nextSibling;
				walk(child);
				child = next;
			}
			break;

		case 3: // Text node
			handleText(node);
			break;
	}
}

function splitWith(textList, delimiter) {
	let result = []
	
	for (let text of textList) {
		let res = text.toLowerCase().split(delimiter)
		for (let i of res) {
			result.push(i)
			result.push(delimiter)
		}
		let r = result.pop()
	}
	return result
}

function handleText(textNode) 
{
	var v = textNode.nodeValue;
	
	let rlist = splitWith(splitWith(splitWith(splitWith(splitWith(splitWith(splitWith([v], ","), "-"), "'"), "’"), "—"), "."), " ")

	let result = ""
	for (let i of rlist) {
		if (mapping[i.trim()]){
			i = mapping[i.trim()]
		} else {
			// i = i.toUpperCase()
		}
		result += i
	}

	textNode.nodeValue = result;
}
