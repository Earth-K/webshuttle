let childNodes = document.getElementsByTagName('body')[0].childNodes;
const func = (c) => {
    if (c === undefined) return;
    for (let i = 0; i < c.length; i++) {
        c[i].addEventListener("mouseover", function (event) {
            event.stopPropagation();
            event.target.style.border = "3px solid rgba(217,217,243,90)";
        });
        func(c[i].childNodes);
    }
}
func(childNodes);