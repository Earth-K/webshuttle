let childNodes = document.getElementsByTagName('body')[0].childNodes;
const func = (c) => {
    if (c === undefined) return;
    for (let i = 0; i < c.length; i++) {
        c[i].addEventListener("mouseout", function (event) {
            event.stopPropagation();
            if (event.target.getAttribute("selected") === null
                || event.target.getAttribute("selected") === "false") {
                event.target.style.backgroundColor = event.target.getAttribute("data-originBackgroundColor");
            }
        });
        func(c[i].childNodes);
    }
}
func(childNodes);