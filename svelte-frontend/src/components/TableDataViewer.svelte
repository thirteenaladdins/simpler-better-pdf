<script>
	import Papa from 'papaparse';
	import { sessionData } from '../store/sessionStore';

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
</script>

<!-- Your style code remains unchanged -->
<div class="summaries font-sans">
	<div><b>Total Lines: </b></div>
	<div><b>Total:</b> {columnSum}</div>
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
					{#each parsedData[0] as headerCell}
						<th>{headerCell}</th>
					{/each}
				</tr>
			{/if}
		</thead>
		<tbody>
			{#each parsedData.slice(1) as row}
				<tr>
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
		/* max-height: 100vh; */
		max-height: calc(100vh - 100px);
		overflow-y: auto;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		margin: 20px 0;
	}

	th,
	td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: left;
	}

	tbody tr {
		background-color: white;
	}

	tbody tr:nth-child(2n) {
		background-color: #f2f2f2;
	}

	tbody tr:hover {
		background-color: #6366f1;
	}

	.font-sans {
		font-family: Open Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu,
			Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
	}

	.table {
		font-size: 14px;
		text-overflow: ellipsis;
		height: 10px;
	}

	.summaries {
		display: flex;
		margin-bottom: 20px;
		gap: 10px;
		padding-top: 10px;
		font-size: 12px;
	}
</style>
