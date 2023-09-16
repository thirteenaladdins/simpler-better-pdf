<!-- Here we'll run the new script against the upload script -->

<script>
	import { onMount } from 'svelte';
	// import { createWorker } from 'tesseract.js';
	import * as pdfjs from 'pdfjs-dist';

	// import { mockResponseJson } from '../data/data.js';

	let ocrText = '';
	let pdfDimensions;
	let canvasElement;
	let canvasContainer;
	let words = [];
	let rawWords = []; // Store raw OCR results without scaling
	let uploadedFile;
	let scale = 1;

	// Ensure worker is loaded correctly with Vite
	pdfjs.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.js';

	let nativeWords = [];

	let isOCREnabled = true; // True will show OCR results, False will show native text

	function toggleResults() {
		isOCREnabled = !isOCREnabled;
	}

	onMount(() => {
		const firstCell = document.querySelector('.entity-table td');
		if (firstCell) {
			firstCell.classList.add('active-cell');
			activeCell = firstCell;
		}
		document.addEventListener('click', (event) => {
			// Hide any tooltip that's currently shown
			const existingTooltip = document.querySelector('.tooltip');
			if (existingTooltip) {
				existingTooltip.remove();
			}
		});

		// Event listener for table cell clicks
		document.querySelectorAll('.entity-table td').forEach((cell) => {
			cell.addEventListener('click', function () {
				if (activeCell) {
					activeCell.classList.remove('active-cell');
				}
				this.classList.add('active-cell');

				activeCell = this;
			});
		});

		// Event listener for word clicks in the content div
		document.querySelector('.annotation-interface').addEventListener('click', function (e) {
			// Check if the clicked item is a word (or just some space)
			if (e.target === this && activeCell) {
				// Retrieve the clicked word (assuming spaces between words)
				let range = window.getSelection().getRangeAt(0);
				let selectedText = range.toString().trim();

				if (selectedText) {
					activeCell.textContent = selectedText;
				}
			}
		});

		// Button event listeners
		document.getElementById('prev').addEventListener('click', function () {
			if (pageNum <= 1) return;
			pageNum--;
			renderPage(pageNum);
		});

		document.getElementById('next').addEventListener('click', function () {
			if (pageNum >= pdfDoc.numPages) return;
			pageNum++;
			renderPage(pageNum);
		});
		window.addEventListener('click', handleWindowClick);
		// Clean up the event listener when the component is destroyed
		return () => {
			window.removeEventListener('click', handleWindowClick);
		};
	});

	function renderDataOnCanvas(words, dimensions) {
		// const container = document.getElementById('your-image-container'); // Adjust the ID to match your HTML.

		const canvasWidth = canvasElement.offsetWidth;
		const canvasHeight = canvasElement.offsetHeight;

		const imageWidth = dimensions.width;
		const imageHeight = dimensions.height;

		const scaleX = canvasWidth / imageWidth;
		const scaleY = canvasHeight / imageHeight;

		words.forEach((word) => {
			const scaledLeft = word.bbox.left * scaleX;
			const scaledTop = word.bbox.top * scaleY;
			const scaledWidth = word.bbox.width * scaleX;
			const scaledHeight = word.bbox.height * scaleY;

			const box = document.createElement('div');
			box.className = 'ocr-word';
			box.style.left = scaledLeft + 'px';
			box.style.top = scaledTop + 'px';
			box.style.width = scaledWidth + 'px';
			box.style.height = scaledHeight + 'px';

			// Add any other properties or event listeners to the box here, e.g.:
			box.addEventListener('click', (event) => {
				event.stopPropagation();
				showWordTooltip(word, box);
			});

			box.addEventListener('keydown', (event) => {
				if (event.key === 'Enter' || event.key === ' ') {
					event.preventDefault();
					showWordTooltip(word);
				}
			});

			// Update the word's box creation in renderDataOnCanvas
			box.addEventListener('click', (event) => {
				event.stopPropagation();
				handleWordClick(event, word);
			});

			canvasContainer.appendChild(box);
		});
	}

	// function displayOCRText(text) {
	// 	const ocrDisplay = document.querySelector('.ocr-display');
	// 	ocrDisplay.textContent = text;
	// }

	async function processPDF(file) {
		// fetch request, or axios here
		// ocr/upload file

		try {
			const arrayBuffer = await file.arrayBuffer();
			const loadingTask = pdfjs.getDocument({ data: arrayBuffer });
			const pdf = await loadingTask.promise;
			const page = await pdf.getPage(1);
			const viewport = page.getViewport({ scale });

			if (!canvasElement) {
				throw new Error('Canvas element not found.');
			}

			const dpr = window.devicePixelRatio || 1; // Get device pixel ratio
			canvasElement.width = viewport.width * dpr; // Adjust canvas width
			canvasElement.height = viewport.height * dpr; // Adjust canvas height
			canvasElement.style.width = `${viewport.width}px`; // CSS width to original size
			canvasElement.style.height = `${viewport.height}px`; // CSS height to original size

			const context = canvasElement.getContext('2d');
			context.scale(dpr, dpr); // Scale the drawing context
			context.imageSmoothingEnabled = true;

			canvasElement.height = viewport.height;
			canvasElement.width = viewport.width;

			const renderContext = {
				canvasContext: context,
				viewport
			};

			await page.render(renderContext).promise;

			// Run OCR only if rawWords array is empty
			if (!rawWords.length) {
				// const worker = await createWorker();
				// await worker.loadLanguage('eng');
				// await worker.initialize('eng');
				// const {
				// 	data: { text, words: ocrWords }
				// } = await worker.recognize(canvasElement);
				// ocrText = text;
				// rawWords = ocrWords; // Store the raw results
				// await worker.terminate();
				const formData = new FormData();
				formData.append('file', file);

				// TODO:
				// test server
				const response = await fetch('http://localhost:591/ocr/upload', {
					method: 'POST',
					body: formData
				});

				const responseJson = await response.json();

				console.log('Full response:', responseJson);
				console.log('Response status:', response.status);
				console.log('Response headers:', response.headers);

				const { data: ocrWords, dimensions } = responseJson;

				// ocrText = text; change to ocrResults
				rawWords = ocrWords; // Store the raw resultsff
				console.log(rawWords);
				pdfDimensions = dimensions;
				renderDataOnCanvas(rawWords, pdfDimensions);

				// TODO: ENABLE AGAIN IF NECESSARY
				// Assuming 'ocrText' is the variable holding the returned OCR result
				// const ocrText = ocrWords.map((result) => result.text).join(' ');
				// displayOCRText(ocrText);
			}

			// Extract native text from the PDF:
			const textContent = await page.getTextContent();
			nativeWords = textContent.items.map((item) => {
				const transform = item.transform;
				// PDFJS uses transforms to position the text, with six array elements:
				// [scaleX, skewX, skewY, scaleY, translateX, translateY]
				return {
					text: item.str,
					left: transform[4],
					top: transform[5] - transform[3], // Subtracting scaleY to adjust the top position
					width: item.width,
					height: item.height
				};
			});

			// console.log(nativeWords);
		} catch (error) {
			console.error('Error processing PDF and OCR:', error);
			ocrText = 'Error processing document.';
		}
	}
	let pdfDoc = null;
	let pageNum = 1; // Default page to display is the first one

	let canvas;
	let ctx;

	onMount(() => {
		canvas = document.createElement('canvas');
		ctx = canvas.getContext('2d');
		document.getElementById('pdf-container').appendChild(canvas);
	});

	function renderPage(num) {
		pdfDoc.getPage(num).then(function (page) {
			const viewport = page.getViewport({ scale: scale });
			canvas.height = viewport.height;
			canvas.width = viewport.width;
			const renderContext = {
				canvasContext: ctx,
				viewport: viewport
			};
			page.render(renderContext);
		});

		// Update page counters, buttons' status, etc.
	}

	// Load the PDF
	// pdfjsLib.getDocument('path/to/your/document.pdf').promise.then(function (pdfDoc_) {
	// 	pdfDoc = pdfDoc_;
	// 	renderPage(pageNum);
	// });

	function handleFileChange(event) {
		uploadedFile = event.target.files[0];
		rawWords = []; // Reset rawWords when new file is uploaded
		if (uploadedFile) {
			processPDF(uploadedFile);
		}
	}

	function setScale(newScale) {
		scale = newScale;
		processPDF(uploadedFile); // Only scales and recalculates bounding boxes
	}

	let selectedWord = null; // This will store the word when clicked

	function showWordTooltip(word, bbox) {
		// Check if a tooltip already exists for this word. If so, remove it.
		const existingTooltip = document.querySelector('.tooltip');
		if (existingTooltip) {
			existingTooltip.remove();
		}

		// Create a new tooltip
		let tooltip = document.createElement('div');
		tooltip.className = 'tooltip';
		tooltip.innerText = word.text; // assuming 'word' has a 'text' property with the word's content

		// Get the position and size of the bbox
		const bboxStyle = window.getComputedStyle(bbox);
		const bboxTop = parseFloat(bboxStyle.top);
		const bboxHeight = parseFloat(bboxStyle.height);

		// Set the position of the tooltip
		tooltip.style.left = bboxStyle.left; // same horizontal position as the bbox
		tooltip.style.top = `${bboxTop + bboxHeight}px`; // below the bbox

		tooltip.style.display = 'block'; // show the tooltip

		// Add the tooltip to the container
		canvasContainer.appendChild(tooltip);
	}

	function handleWindowClick(event) {
		// If the target of the click isn't one of the .ocr-word or .tooltip elements
		if (
			!event.target.classList.contains('ocr-word') &&
			!event.target.classList.contains('tooltip')
		) {
			selectedWord = null; // Hide the tooltip
		}
	}

	let annotations = [];
	let currentAnnotation = null; // { start: null, end: null, label: null }

	let activeCell = null;

	function handleWordClick(event, word) {
		event.stopPropagation();

		// Tooltip Handling
		showWordTooltip(word, event.currentTarget);

		// Annotation Handling
		if (currentAnnotation) {
			currentAnnotation.end = word;
			// showLabelPicker(event.clientX, event.clientY);
		} else {
			currentAnnotation = {
				start: word,
				end: null,
				label: null
			};
		}

		// Active Cell Handling
		if (activeCell) {
			activeCell.textContent = word.text;
		}
	}

	// Save or export the annotations in Spacy's format
	function saveAnnotations() {
		let trainingData = annotations.map((annotation) => {
			let sentence = ocrText;
			let startIdx = sentence.indexOf(annotation.start.text);
			let endIdx = sentence.indexOf(annotation.end.text) + annotation.end.text.length;
			return sentence, { entities: [[startIdx, endIdx, annotation.label]] };
		});

		// Do whatever you want with trainingData, like sending it to your backend or saving it locally
		console.log(trainingData);
	}
</script>

<div id="pdf-container">
	<div id="canvas-container" bind:this={canvasContainer}>
		<canvas bind:this={canvasElement} />
		<input type="file" id="pdf-upload" accept=".pdf" on:change={handleFileChange} />
		<button on:click={toggleResults}>
			{isOCREnabled ? 'Show Native Text' : 'Show OCR Results'}
		</button>
		<button id="prev">Previous</button>
		<button id="next">Next</button>
		<div id="pdf-container" />
	</div>
	<div class="action-bar-container">
		<div class="action-bar">
			<div class="border-handle" />
			<div class="content">
				<div class="ocr-display">
					<!-- OCR results will be populated here -->
				</div>
				<div class="annotation-interface">Annotation</div>
				<!-- The entity table -->
				<table class="entity-table">
					<thead>
						<tr>
							<th data-label="HS_CODE">HS CODE</th>
							<th data-label="QUANTITY">Quantity</th>
							<th data-label="NET_WEIGHT">Net Weight</th>
							<th data-label="GROSS_WEIGHT">Gross Weight</th>
							<th data-label="PRODUCT_DESCRIPTION">Product Description</th>
							<th data-label="COO">COO</th>
							<th data-label="UNIT_PRICE">Unit Price</th>
							<th data-label="TOTAL_PRICE">Total Price</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td data-label="HS_CODE" />
							<td data-label="QUANTITY" />
							<td data-label="NET_WEIGHT" />
							<td data-label="GROSS_WEIGHT" />
							<td data-label="PRODUCT_DESCRIPTION" />
							<td data-label="COO" />
							<td data-label="UNIT_PRICE" />
							<td data-label="TOTAL_PRICE" />
						</tr>
					</tbody>
				</table>
				<button on:click={saveAnnotations}>Save Annotations</button>
			</div>
		</div>
	</div>

	<style>
		/* Base Styles */
		#pdf-container {
			display: flex;
			height: 100vh;
			font-family: Open Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu,
				Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
		}

		ul {
			list-style-type: none;
			padding: 0;
		}

		canvas {
			border: 1px solid red;
		}

		table {
			width: 100%;
			border-collapse: collapse;
			margin-top: 20px;
			font-size: 12px;
		}

		table,
		th,
		td {
			border: 1px solid #ccc;
		}

		th,
		td {
			padding: 8px 12px;
			text-align: left;
		}

		.active-cell {
			background-color: #f5f5f5;
		}

		/* PDF Viewer */
		#canvas-container {
			flex: 3;
			position: relative;
			overflow: hidden;
		}

		/* Action Bar */
		.action-bar-container {
			display: flex;
			align-items: stretch;
			flex: 2;
		}

		.action-bar {
			display: flex;
			align-items: stretch;
			width: 100%;
			overflow: hidden;
		}

		.content {
			flex: 1;
			overflow-y: auto;
			padding-left: 20px;
			cursor: default;
		}

		/* Your other styles */

		.border-handle {
			width: 22px; /* 10px buffer on each side + 2px for the border itself */
			height: 100%;
			background: linear-gradient(
				to right,
				transparent 10px,
				#ccc 10px,
				#ccc 12px,
				transparent 12px
			); /* 1px border centered */
			cursor: default; /* default cursor for the handle area */
			position: relative;
			z-index: 2;
		}

		/* Hover effect only on the border itself */
		.border-handle:hover {
			background: linear-gradient(
				to right,
				transparent 10px,
				blue 10px,
				blue 12px,
				transparent 12px
			);
			cursor: ew-resize;
		}

		/* Cursor effect only on the border */
		.border-handle::before,
		.border-handle::after {
			content: '';
			position: absolute;
			top: 0;
			bottom: 0;
			width: 10px;
			z-index: 10;
			cursor: ew-resize; /* Resize cursor only over the sides of the border */
		}

		.border-handle::before {
			left: 0;
		}

		.border-handle::after {
			right: 0;
		}

		/* Your other styles */

		/* OCR Results */
		#ocr-results {
			flex-basis: 250px;
			overflow-y: auto;
			padding-left: 20px;
			border-left: 1px solid #ccc;
		}

		.ocr-word {
			position: absolute;
			border: 2px solid transparent;
			transition: border 0.3s ease;
			z-index: 1000;
		}

		.ocr-word:hover {
			border: 2px solid blue;
			cursor: pointer;
		}

		/* Tooltip */
		.tooltip {
			position: absolute;
			padding: 5px 10px;
			background-color: #000;
			color: #fff;
			border-radius: 4px;
			pointer-events: none;
			transform: translateY(5px);
			font-size: 14px;
			z-index: 10;
		}
	</style>
</div>
