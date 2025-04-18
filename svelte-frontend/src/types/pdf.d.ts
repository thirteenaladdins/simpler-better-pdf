declare module '../../../public/pdfjs-dist/build/pdf.mjs' {
    export const GlobalWorkerOptions: {
        workerSrc: string;
    };

    export function getDocument(options: {
        url: string;
        cMapUrl?: string;
        cMapPacked?: boolean;
    }): {
        promise: Promise<PDFDocumentProxy>;
    };
}

interface PDFDocumentProxy {
    numPages: number;
    destroy(): void;
    getPage(pageNumber: number): Promise<PDFPageProxy>;
}

interface PDFPageProxy {
    getViewport(options: { scale: number }): PDFViewport;
    render(options: {
        canvasContext: CanvasRenderingContext2D;
        viewport: PDFViewport;
    }): {
        promise: Promise<void>;
        cancel(): void;
    };
}

interface PDFViewport {
    width: number;
    height: number;
} 