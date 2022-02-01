let childNodes = document.getElementsByTagName('body')[0].childNodes;
const func = (c) => {
    if (c === undefined) return;
    for (let i = 0; i < c.length; i++) {
        c[i].addEventListener("mouseleave", function (event) {
            event.stopPropagation();
            if (event.target.getAttribute("selected") === null
                || event.target.getAttribute("selected") === "false") {
                event.target.style.border = "";
            }
        });
        func(c[i].childNodes);
    }
}
func(childNodes);