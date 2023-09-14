import * as pdfjs from 'pdfjs-dist';

const loadingTask = pdfjs.getDocument('path_to_your_pdf.pdf');

loadingTask.promise.then(function(pdf) {
  const pageNumber = 1; // or loop through all pages
  return pdf.getPage(pageNumber);
}).then(function(page) {
  const scale = 1.5;
  const viewport = page.getViewport({ scale: scale });

  const canvas = document.getElementById('pdf-canvas');
  const context = canvas.getContext('2d');
  canvas.height = viewport.height;
  canvas.width = viewport.width;

  const renderContext = {
    canvasContext: context,
    viewport: viewport
  };
  page.render(renderContext);
});
