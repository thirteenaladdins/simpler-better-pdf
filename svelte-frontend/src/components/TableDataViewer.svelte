<script>
	import Papa from 'papaparse';
	import { sessionData } from '../store/sessionStore';
	import { onMount } from 'svelte';

	let sessionResponse;

	sessionData.subscribe((value) => {
		sessionResponse = value;
	});

	let fileData = sessionResponse?.data;
	let fileType = sessionResponse?.filetype;
	let fileName = sessionResponse?.filename;

	let parsedData = [];
	let columnSum = 0;
	let uniqueValues = new Set();
	let totalNetWeight = 0;
	let totalGrossWeight = 0;
	let totalQuantity = 0;
	let totalCartons = 0;
	let totalsLine = 0;
	let uniqueValueCount = 0; // Initial value

	// Use reactive statement to react to changes in `fileData`
	$: if (fileData) {
		// Reset accumulators
		columnSum = 0;
		totalNetWeight = 0;
		totalGrossWeight = 0;
		totalQuantity = 0;
		totalCartons = 0;
		uniqueValueCount = 0;

		Papa.parse(fileData, {
			complete: function (results) {
				parsedData = results.data;

				// Define the column indexes based on your CSV headers
				let columnIndexValue = parsedData[0].indexOf('Value');
				let columnIndexNetWeight = parsedData[0].indexOf('Total Net Weight');
				let columnIndexGrossWeight = parsedData[0].indexOf('Total Gross Weight');
				let columnIndexQuantity = parsedData[0].indexOf('Quantity');
				let columnIndexCartons = parsedData[0].indexOf('Total Cartons');

				for (let i = 1; i < parsedData.length; i++) {
					let row = parsedData[i];

					if (columnIndexValue !== -1 && row[columnIndexValue] && !isNaN(row[columnIndexValue])) {
						columnSum += parseFloat(row[columnIndexValue]);
					}

					if (
						columnIndexNetWeight !== -1 &&
						row[columnIndexNetWeight] &&
						!isNaN(row[columnIndexNetWeight])
					) {
						totalNetWeight += parseFloat(row[columnIndexNetWeight]);
					}
					if (
						columnIndexGrossWeight !== -1 &&
						row[columnIndexGrossWeight] &&
						!isNaN(row[columnIndexGrossWeight])
					) {
						totalGrossWeight += parseFloat(row[columnIndexGrossWeight]);
					}
					if (
						columnIndexQuantity !== -1 &&
						row[columnIndexQuantity] &&
						!isNaN(row[columnIndexQuantity])
					) {
						totalQuantity += parseFloat(row[columnIndexQuantity]);
					}
					if (
						columnIndexCartons !== -1 &&
						row[columnIndexCartons] &&
						!isNaN(row[columnIndexCartons])
					) {
						totalCartons += parseFloat(row[columnIndexCartons]);
					}
				}

				uniqueValueCount = uniqueValues.size;
			}
		});
	}

	function handleRowClick(event) {
		const row = event.currentTarget; // Get the clicked row
		const rect = row.getBoundingClientRect(); // Get row's position and size
		const beforeWidth = parseFloat(window.getComputedStyle(row, '::before').width); // Get ::before width

		// If the click was within the ::before pseudo-element's area, toggle the highlighted-row class
		if (event.clientX < rect.left + beforeWidth) {
			row.classList.toggle('highlighted-row');
		}
	}
</script>

<!-- Your style code remains unchanged -->
<div class="summaries font-sans">
	<div><b>Total Lines: </b></div>
	<div><b>Total:</b> {columnSum.toFixed(2)}</div>
	<!-- <div>Unique Values: {uniqueValueCount}</div> -->
	<div><b>Total Net Weight:</b> {totalNetWeight}</div>
	<div><b>Total Gross Weight:</b> {totalGrossWeight}</div>
	<div><b>Total Quantity:</b> {totalQuantity}</div>
	<div><b>Total Cartons:</b> {totalCartons}</div>
</div>

<div class="table-data-viewer font-sans">
	<table class="table">
		<thead>
			{#if parsedData.length > 0}
				<tr>
					<th>#</th>
					<!-- Added this extra header for the row number indicator -->
					{#each parsedData[0] as headerCell}
						<th>{headerCell}</th>
					{/each}
				</tr>
			{/if}
		</thead>
		<tbody>
			{#each parsedData.slice(1) as row}
				<tr on:click={handleRowClick}>
					{#each row as cell}
						<td>{cell}</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.table-data-viewer {
		max-height: calc(100vh - 100px);
		overflow-y: auto;
		position: relative;
		counter-reset: rowNumber; /* Initialize the counter */
	}

	.summaries {
		display: flex;
		/* height: 100%; */
		gap: 10px;
		padding: 16px;
		font-size: 14px;
		background-color: #6366f1;
		color: white;
	}

	.highlighted-row {
		background-color: #ffe58f !important;
		/* Use any color you prefer for highlighting. The !important is to override any other background color styles. */
	}

	tbody tr::before {
		content: counter(rowNumber); /* Display the current count */
		counter-increment: rowNumber; /* Increment the counter */
		display: table-cell; /* Make it behave like a table cell */
		padding: 8px;
		border: 1px solid #ddd;
		text-align: right; /* Align the number to the right side of its cell */
		width: 1.5em; /* Adjust width as necessary */
		font-weight: bold;
	}

	tbody tr:hover::before {
		border: 1px solid #9fb5fc;
		background-color: #e7e9fc; /* Slight background change for clarity on hover */
	}

	table {
		border-collapse: separate;
		border-spacing: 0;
	}

	th,
	td {
		border-right: 1px solid #ddd;
		border-bottom: 1px solid #ddd;
		padding: 8px;
		text-align: left;
	}

	th:first-child,
	td:first-child {
		border-left: 1px solid #ddd; /* Add left border for the first cell */
	}

	tr:first-child th {
		border-top: 1px solid #ddd; /* Add top border for the first row */
	}

	thead th {
		position: sticky;
		top: 0;
		z-index: 10;
		background-color: #f2f2f2;
		box-shadow: 0 2px 2px -1px rgba(0, 0, 0, 0.1);
	}

	th,
	td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: left;
	}

	/* Overlap the tbody's first row with the sticky header */
	tbody {
		margin-top: -1px;
	}

	tbody tr {
		background-color: white;
	}

	tbody tr:nth-child(2n) {
		background-color: #f2f2f2;
	}

	/* Header cells hover effect */
	thead th:hover {
		border: 1px solid #9fb5fc;
		background-color: #e7e9fc; /* Slight background change for clarity on hover */
	}

	tbody td:hover {
		border: 1px solid #9fb5fc;
		background-color: #e7e9fc; /* Slight background change for clarity on hover */
	}

	.font-sans {
		font-family: Open Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu,
			Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
	}

	.table {
		font-size: 14px;
		text-overflow: ellipsis;
		height: 10px;
		width: 5px;
	}

	table td,
	table th {
		overflow: hidden;
		text-overflow: ellipsis; /* this will display '...' if the content is too long for the cell */
		white-space: nowrap; /* this will prevent the content from wrapping onto the next line */
	}
</style>
