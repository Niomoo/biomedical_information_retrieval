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

document.addEventListener("DOMContentLoaded", function () {
    var tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    var tooltipList = tooltipTriggerList.map(function (element) {
      return new bootstrap.Tooltip(element);
    });
});

const currentLocation = location.href;
const menuItem = document.getElementsByClassName("nav-link");
const menuLength = menuItem.length;
for (let i = 0; i < menuLength; i++) {
  if (menuItem[i].href === currentLocation) {
    menuItem[i].className += " active";
  }
}