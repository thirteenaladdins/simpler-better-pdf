import * as pdfjsLib from 'pdfjs-dist';

import { PDFViewer, EventBus } from 'pdfjs-dist/web/pdf_viewer.mjs';
import workerSrc from 'pdfjs-dist/build/pdf.worker.min?url';

// Assign worker
pdfjsLib.GlobalWorkerOptions.workerSrc = workerSrc;

// ✅ Assign to globalThis for pdf_viewer.mjs compatibility

export { pdfjsLib, PDFViewer, EventBus };
