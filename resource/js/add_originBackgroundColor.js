let childNodes = document.getElementsByTagName('body')[0].childNodes;
const addOriginBackgroundAttributeAll = (children) => {
    if (children === undefined) return;
    for (let i = 0; i < children.length; i++) {
        children[i].setAttribute("data-originBackgroundColor", children[i].style.backgroundColor);
        addOriginBackgroundAttributeAll(children[i].childNodes);
    }
}
addOriginBackgroundAttributeAll(childNodes);