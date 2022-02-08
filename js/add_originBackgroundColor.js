let childNodes = document.getElementsByTagName('body')[0].childNodes;
const func = (c) => {
    if (c === undefined) return;
    for (let i = 0; i < c.length; i++) {
        c[i].setAttribute("data-originBackgroundColor", c[i].style.backgroundColor);
        func(c[i].childNodes);
    }
}
func(childNodes);