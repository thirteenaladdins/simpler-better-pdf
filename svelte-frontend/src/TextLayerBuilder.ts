class TextLayerBuilder {
    #enablePermissions = false;
    #onAppend = null;
    #renderingDone = false;
    #textLayer = null;
    static #textLayers = new Map();
    static #selectionChangeAbortController = null;
    constructor({
      pdfPage,
      highlighter = null,
      accessibilityManager = null,
      enablePermissions = false,
      onAppend = null
    }) {
      this.pdfPage = pdfPage;
      this.highlighter = highlighter;
      this.accessibilityManager = accessibilityManager;
      this.#enablePermissions = enablePermissions === true;
      this.#onAppend = onAppend;
      this.div = document.createElement("div");
      this.div.tabIndex = 0;
      this.div.className = "textLayer";
    }
    async render({
      viewport,
      textContentParams = null
    }) {
      if (this.#renderingDone && this.#textLayer) {
        this.#textLayer.update({
          viewport,
          onBefore: this.hide.bind(this)
        });
        this.show();
        return;
      }
      this.cancel();
      this.#textLayer = new TextLayer({
        textContentSource: this.pdfPage.streamTextContent(textContentParams || {
          includeMarkedContent: true,
          disableNormalization: true
        }),
        container: this.div,
        viewport
      });
      const {
        textDivs,
        textContentItemsStr
      } = this.#textLayer;
      this.highlighter?.setTextMapping(textDivs, textContentItemsStr);
      this.accessibilityManager?.setTextMapping(textDivs);
      await this.#textLayer.render();
      this.#renderingDone = true;
      const endOfContent = document.createElement("div");
      endOfContent.className = "endOfContent";
      this.div.append(endOfContent);
      this.#bindMouse(endOfContent);
      this.#onAppend?.(this.div);
      this.highlighter?.enable();
      this.accessibilityManager?.enable();
    }
    hide() {
      if (!this.div.hidden && this.#renderingDone) {
        this.highlighter?.disable();
        this.div.hidden = true;
      }
    }
    show() {
      if (this.div.hidden && this.#renderingDone) {
        this.div.hidden = false;
        this.highlighter?.enable();
      }
    }
    cancel() {
      this.#textLayer?.cancel();
      this.#textLayer = null;
      this.highlighter?.disable();
      this.accessibilityManager?.disable();
      TextLayerBuilder.#removeGlobalSelectionListener(this.div);
    }
    #bindMouse(end) {
      const {
        div
      } = this;
      div.addEventListener("mousedown", () => {
        div.classList.add("selecting");
      });
      div.addEventListener("copy", event => {
        if (!this.#enablePermissions) {
          const selection = document.getSelection();
          event.clipboardData.setData("text/plain", removeNullCharacters(normalizeUnicode(selection.toString())));
        }
        stopEvent(event);
      });
      TextLayerBuilder.#textLayers.set(div, end);
      TextLayerBuilder.#enableGlobalSelectionListener();
    }
    static #removeGlobalSelectionListener(textLayerDiv) {
      this.#textLayers.delete(textLayerDiv);
      if (this.#textLayers.size === 0) {
        this.#selectionChangeAbortController?.abort();
        this.#selectionChangeAbortController = null;
      }
    }
    static #enableGlobalSelectionListener() {
      if (this.#selectionChangeAbortController) {
        return;
      }
      this.#selectionChangeAbortController = new AbortController();
      const {
        signal
      } = this.#selectionChangeAbortController;
      const reset = (end, textLayer) => {
        textLayer.append(end);
        end.style.width = "";
        end.style.height = "";
        textLayer.classList.remove("selecting");
      };
      let isPointerDown = false;
      document.addEventListener("pointerdown", () => {
        isPointerDown = true;
      }, {
        signal
      });
      document.addEventListener("pointerup", () => {
        isPointerDown = false;
        this.#textLayers.forEach(reset);
      }, {
        signal
      });
      window.addEventListener("blur", () => {
        isPointerDown = false;
        this.#textLayers.forEach(reset);
      }, {
        signal
      });
      document.addEventListener("keyup", () => {
        if (!isPointerDown) {
          this.#textLayers.forEach(reset);
        }
      }, {
        signal
      });
      var isFirefox, prevRange;
      document.addEventListener("selectionchange", () => {
        const selection = document.getSelection();
        if (selection.rangeCount === 0) {
          this.#textLayers.forEach(reset);
          return;
        }
        const activeTextLayers = new Set();
        for (let i = 0; i < selection.rangeCount; i++) {
          const range = selection.getRangeAt(i);
          for (const textLayerDiv of this.#textLayers.keys()) {
            if (!activeTextLayers.has(textLayerDiv) && range.intersectsNode(textLayerDiv)) {
              activeTextLayers.add(textLayerDiv);
            }
          }
        }
        for (const [textLayerDiv, endDiv] of this.#textLayers) {
          if (activeTextLayers.has(textLayerDiv)) {
            textLayerDiv.classList.add("selecting");
          } else {
            reset(endDiv, textLayerDiv);
          }
        }
        isFirefox ??= getComputedStyle(this.#textLayers.values().next().value).getPropertyValue("-moz-user-select") === "none";
        if (isFirefox) {
          return;
        }
        const range = selection.getRangeAt(0);
        const modifyStart = prevRange && (range.compareBoundaryPoints(Range.END_TO_END, prevRange) === 0 || range.compareBoundaryPoints(Range.START_TO_END, prevRange) === 0);
        let anchor = modifyStart ? range.startContainer : range.endContainer;
        if (anchor.nodeType === Node.TEXT_NODE) {
          anchor = anchor.parentNode;
        }
        const parentTextLayer = anchor.parentElement?.closest(".textLayer");
        const endDiv = this.#textLayers.get(parentTextLayer);
        if (endDiv) {
          endDiv.style.width = parentTextLayer.style.width;
          endDiv.style.height = parentTextLayer.style.height;
          anchor.parentElement.insertBefore(endDiv, modifyStart ? anchor : anchor.nextSibling);
        }
        prevRange = range.cloneRange();
      }, {
        signal
      });
    }
  }