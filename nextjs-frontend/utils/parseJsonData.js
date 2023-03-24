const parseJsonData = (jsonData) => {
  // console.log(jsonData);
  // console.log('first entry', jsonData[0]);
  // const fileType = 'text/csv'

  try {
    const replacer = (key, value) => (value === null ? '' : value); // specify how you want to handle null values here
    const headers = Object.keys(jsonData[0]);
    // console.log(headers)

    let csv = jsonData.map((row) => headers
      .map((fieldName) => JSON.stringify(row[fieldName], replacer))
      .join(','));
    csv.unshift(headers);
    csv = csv.join('\r\n');
    // console.log(csv)

    // this runs once per file, I just one it overall for the one file
    return csv;

  } catch {
    // FIXME: add proper error handling
    // add file name here?
    // TODO - add error message to screen
    // add error to screen
    console.log('Something went wrong converting json to csv.');
    return null;
  }

  // return <Download fileName={filename} csv={csv} />
};

// return additional data here
// return csv data here
// generate file name here?
// return file type here?

export default parseJsonData;
