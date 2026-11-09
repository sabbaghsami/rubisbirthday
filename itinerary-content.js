// Apply the editable page copy without interpreting it as HTML.
const content = window.ITINERARY_CONFIG;
document.title = content.page_title;
document.querySelectorAll('[data-text]').forEach(element => {
  element.textContent = content[element.dataset.text];
});
const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_COMMENT);
const placeholders = [];
while (walker.nextNode()) {
  if (walker.currentNode.data.startsWith('text:')) placeholders.push(walker.currentNode);
}
placeholders.forEach(node => node.replaceWith(document.createTextNode(content[node.data.slice(5)])));
for (const attribute of ['aria-label', 'alt', 'href', 'src']) {
  document.querySelectorAll(`[data-config-${attribute}]`).forEach(element => {
    element.setAttribute(attribute, content[element.getAttribute(`data-config-${attribute}`)]);
  });
}

// Each stop's collage is editable from the same config as its wording.
for (let stop = 1; stop <= 6; stop++) {
  const image = document.createElement('img');
  image.className = 'stop-photo';
  image.src = content[`stop_${stop}_photo_path`];
  image.alt = content[`stop_${stop}_photo_description`];
  image.loading = 'lazy';
  image.width = 1536;
  image.height = 1024;
  document.querySelector(`#stop-${stop} .detail`).prepend(image);
}
