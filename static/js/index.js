function search() {
    let name = document.getElementById("searchForm").elements["searchItem"].value;
    let pattern = name.toLowerCase();
    let l = pattern.length;
    let text = document.getElementById("targetText").innerText;
    let alterText = document.getElementById("targetText").innerHTML;
    let offset = 0;
    let index;
    const indexArray = [];
    while((index = text.indexOf(pattern, offset)) >= 0) {
        indexArray.push(index);
        offset = index + 1;
    }
    console.log(indexArray);
    alterText = text.replaceAll(pattern, "<span class='searchword'>"+pattern+"</span>");

    console.log(alterText);
    document.getElementById("targetText").innerHTML = alterText;
}
