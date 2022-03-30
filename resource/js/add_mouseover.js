let childNodes = document.getElementsByTagName('body')[0].childNodes;
const addMouseoverEventAll = (children) => {
    if (children === undefined) return;
    for (let i = 0; i < children.length; i++) {
        children[i].addEventListener("mouseover", function (event) {
            event.stopPropagation();
            event.target.style.backgroundColor = "rgba(217,217,243,0.5)";
        });
        addMouseoverEventAll(children[i].childNodes);
    }
}
addMouseoverEventAll(childNodes);