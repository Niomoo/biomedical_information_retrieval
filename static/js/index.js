function search() {
    let name = document.getElementById("searchForm").elements["searchItem"].value;
    let pattern = name.toLowerCase();
    let l = pattern.length;
    let text = document.getElementById("targetText").innerText.toLowerCase();
    let alterText = document.getElementById("targetText").innerHTML;
    let offset = 0;
    let index;
    console.log(text);
    const indexArray = [];
    while((index = text.indexOf(pattern, offset)) >= 0) {
        indexArray.push(index);
        offset = index + 1;
    }
    console.log(indexArray);
    alterText = text.replaceAll(name, "<span class='badge searchword'>"+name+"</span>");

    console.log(alterText);
    document.getElementById("targetText").innerHTML = alterText;
}
$(function () {
    $("[data-toggle='tooltip']").tooltip();
});
