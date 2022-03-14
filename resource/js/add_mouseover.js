let childNodes = document.getElementsByTagName('body')[0].childNodes;
const func = (c) => {
    if (c === undefined) return;
    for (let i = 0; i < c.length; i++) {
        c[i].addEventListener("mouseover", function (event) {
            event.stopPropagation();
            event.target.style.backgroundColor = "rgba(217,217,243,0.5)";
        });
        func(c[i].childNodes);
    }
}
func(childNodes);