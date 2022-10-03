function searchNearest() {
  let name = document.getElementById("searchNearestForm").elements["searchNearestItem"].value;
  let pattern = name.toLowerCase();
  let l = pattern.length;
  let originText = document.getElementById("targetNearestText").innerText;
  let text = originText.toLowerCase();
  let alterText = document.getElementById("targetNearestText").innerHTML;
  let offset = 0;
  let index;
  let divbox = document.getElementById("targetBox");
  let hint = document.getElementById("hint");
  if(hint != null){
      hint.style.display = "none";
  }
  const indexArray = [];
  while ((index = text.indexOf(pattern, offset)) >= 0) {
    indexArray.push(index);
    offset = index + 1;
  }
  if (indexArray.length > 0) {
    alterText = originText.replaceAll(name, "<span class='badge searchword'>" + name + "</span>");
  }
  else {
    all_words = text.split(" ");
    minDis = 9999;
    target = '';
    for(let i = 0; i < all_words.length; i++) {
        let d = minDistance(all_words[i], pattern);
        if(d < minDis) {
            minDis = d;
            target = all_words[i];
        }
    }
    divbox.innerHTML += "<p id='hint' class='text-start mt-2 mb-0'><i>There's no result for <mark>" + name + "</mark>, so show the results for <mark>"+ target +"</mark>: </i></p>";
    alterText = originText.replaceAll(target, "<span class='badge searchword'>" + target + "</span>");
  }
  console.log(indexArray);
  console.log(alterText);
  document.getElementById("targetNearestText").innerHTML = alterText;
}

function minDistance(s1, s2) {
  const len1 = s1.length;
  const len2 = s2.length;

  let matrix = [];
  for (let i = 0; i <= len1; i++) {
    matrix[i] = new Array();
    for (let j = 0; j <= len2; j++) {
      if (i == 0) {
        matrix[i][j] = j;
      } else if (j == 0) {
        matrix[i][j] = i;
      } else {
        let cost = 0;
        if (s1[i - 1] != s2[j - 1]) {
          cost = 1;
        }
        const temp = matrix[i - 1][j - 1] + cost;
        matrix[i][j] = Math.min(
          matrix[i - 1][j] + 1,
          matrix[i][j - 1] + 1,
          temp
        );
      }
    }
  }
  return matrix[len1][len2];
}