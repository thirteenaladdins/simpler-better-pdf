import { React, useRef, useEffect, useState, Fragment } from 'react'
import { useFilePicker } from 'use-file-picker'
import ListItem from '../components/ListItem'
import DownloadIcon from '../public/download.svg'
import FrownIcon from '../public/frown.svg'
import Spinner from '../public/tail-spin.svg'
import Image from 'next/image'
import axios from 'axios'

// come back and sort out all the design

const initialState = {
  fileSelection: null,
  selectedFile: 'default_component',
  returnedData: false,
  loading: false,
  downloadFile: false,
}

const count = 50
const formats = ['pdf']

const Extractor = () => {
  const [state, setState] = useState(initialState)

  const uploadFile = async (file) => {
    // let url = 'http://localhost:8080/api/processfile'
    // for production
    let url = 'https://luxury-goods-backend.herokuapp.com/api/processfile'
    let formData = new FormData()

    formData.append('file', file)

    let response = await axios.post(url, formData, {
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
    // .catch((err) => {
    //   if (err.response.status === 500) {
    //     console.log('Something went wrong')
    //   }
    // })

    return response
  }

  // instead of dealing with json we're using json array
  const processAllFiles = async (files) => {
    var responses = []

    for (const file of files) {
      try {
        const responseData = await uploadFile(file).catch((err) => {})
        responses.push(responseData.data)
      } catch {
        ;(error) => {
          if (error.response.status === 500) {
            console.log(err)
            return error
          }
        }
      }
    }

    const combinedResponses = [].concat.apply([], responses)
    // console.log(responses)
    // setState({ ...state, returnedData: true })
    const csvFormattedData = parseJsonData(combinedResponses)
    // console.log(csvFormattedData)
    return csvFormattedData
  }

  function handleDrop(e) {
    let files = e.dataTransfer.files
    const fileList = [...e.dataTransfer.files]

    if (count && count < files.length) {
      console.log(
        `Only ${count} file${count !== 1 ? 's' : ''} can be uploaded at a time`
      )
      return
    }

    if (
      formats &&
      fileList.some(
        (file) =>
          !formats.some((format) =>
            file.name.toLowerCase().endsWith(format.toLowerCase())
          )
      )
    ) {
      console.log(
        `Only the following file formats are acceptable: ${formats.join(', ')}`
      )
      setState({ ...state, fileSelection: 'invalid_file_component' })
      return
    }

    setState({
      ...state,
      selectedFile: files,
      fileSelection: 'list_component',
    })
    return files
  }

  function handleFiles(e) {
    console.log(e)
    // let files = e.files
    const files = [...e]
    // console.log(files)

    // How do I display this message?

    // ##### count the number of files
    // if (count && count < files.length) {
    //   console.log(
    //     `Only ${count} file${count !== 1 ? 's' : ''} can be uploaded at a time`
    //   )
    //   return
    // }

    // if (
    //   formats &&
    //   fileList.some(
    //     (file) =>
    //       !formats.some((format) =>
    //         file.name.toLowerCase().endsWith(format.toLowerCase())
    //       )
    //   )
    // ) {
    //   console.log(
    //     `Only the following file formats are acceptable: ${formats.join(', ')}`
    //   )
    //   setState({ ...state, fileSelection: 'invalid_file_component' })
    //   return
    // }

    setState({
      ...state,
      selectedFile: files,
      fileSelection: 'list_component',
    })
    return files
  }

  // for each of these -
  // we also need a spinner when we're waiting for the response
  const renderSwitch = (currentState) => {
    switch (currentState) {
      case 'download_component':
        return <Download />
      case 'list_component':
        return <ListView />
      case 'loading_component':
        return <LoadingView />
      case 'invalid_file_component':
        return <WrongFileMessage />
      case 'default_component':
        return <DropArea />
      default:
        return <DropArea />
    }
  }

  // const DropSwitcher = () => {
  //   return state.validFile ? <DropArea /> : <WrongFileMessage />
  // }

  function DropArea() {
    const ref = useRef(null)
    const inputFile = useRef(null)

    // const [files, errors, openFileSelector] = useFilePicker({
    //   multiple: true,
    //   accept: '.ics,.pdf',
    // })

    useEffect(() => {
      const dropArea = ref.current
      ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
        dropArea.addEventListener(eventName, preventDefaults, false)
      })

      dropArea.addEventListener('drop', handleDrop, false)
      ;['dragenter', 'dragover'].forEach((eventName) => {
        dropArea.addEventListener(eventName, highlight, false)
      })
      ;['dragleave', 'drop'].forEach((eventName) => {
        dropArea.addEventListener(eventName, unhighlight, false)
      })

      // dropArea.addEventListener('click', chooseFiles, false)

      function preventDefaults(e) {
        e.preventDefault()
        e.stopPropagation()
        // console.log('Dragged')
      }
      // I want to add this class to the drop area only
      function highlight(e) {
        dropArea.classList.add('bg-indigo-300')
      }

      function unhighlight(e) {
        dropArea.classList.remove('bg-indigo-300')
      }

      // function chooseFiles() {
      //   ref.current.click()
      // }

      // const onChangeFile = (event) => {
      //   event.stopPropagation()
      //   event.preventDefault()
      //   var file = event.target.files[0]
      //   console.log(file)
      //   // this.setState({ file }) /// if you want to upload latter
      // }

      // what does this mean and how does it work?
      // when should I remove listener?
      return () => {
        // dropArea.removeEventListener('dragenter', handleDrag)
        // dropArea.removeEventListener('dragleave', handleDrag)
        // dropArea.removeEventListener('dragover', handleDrag)
        // dropArea.removeEventListener('drop', handleDrag)
        dropArea.removeEventListener('drop', handleDrop, false)
      }
    }, [])

    const onClickHandler = () => {
      inputFile.current.click()
      // handleDrop(e)
    }

    // responsive window width - if it's less than 640px change width
    const handleResize = () => {
      if (window.innerWidth < 640) {
        // setState({ ...state, width: '100%' })
      } else {
        // setState({ ...state, width: '50%' })
      }
    }

    return (
      <div
        ref={ref}
        className="drop-area-full flex
        cursor-pointer flex-col items-center justify-center break-normal
        border-2 border-dashed border-indigo-300 text-center
        font-sans"
        onClick={onClickHandler}
      >
        <input
          multiple
          type="file"
          id="file"
          ref={inputFile}
          accept="application/pdf"
          style={{ display: 'none' }}
          onChange={(e) => handleFiles(e.target.files)}
        />
        <div>
          <Image
            className="pointer-events-none select-none"
            src={DownloadIcon}
            priority
            alt="Drop your files here"
            layout="raw"
          />
          <div className="pointer-events-none select-none text-sm">
            Click to choose a file or drag it here
          </div>
        </div>
      </div>
    )
  }

  function WrongFileMessage() {
    const ref = useRef(null)

    function startAgain() {
      setState({ ...state, fileSelection: 'default_component' })
    }

    useEffect(() => {
      const wrongFileBox = ref.current

      wrongFileBox.addEventListener('click', preventDefaults, false)

      function preventDefaults(e) {
        e.preventDefault()
        e.stopPropagation()
        // console.log('Dragged')
      }

      wrongFileBox.addEventListener('click', startAgain, false)

      // remove listeners
    })

    return (
      <div
        ref={ref}
        className="drop-area flex w-8/12
        cursor-pointer flex-col items-center justify-center break-normal
        border-2 border-dashed border-red-300 bg-red-300
        text-center font-sans"
      >
        <Image
          className="pointer-events-none select-none"
          src={FrownIcon}
          priority
          alt="Not a pdf file"
          layout="raw"
        />
        <div className="pointer-events-none select-none text-sm">
          Pdf files only. Try again.
        </div>
      </div>
    )
  }
  // I want this to last for a couple of seconds
  // and should it be ternary operator?

  function LoadingView() {
    return (
      <div className="indigo-300">
        <Image
          className="fill-indigo-300"
          src={Spinner}
          priority
          alt="Loading..."
        />
      </div>
    )
  }

  function ListView() {
    return (
      <Fragment>
        <div className="flex w-64 flex-col items-center rounded-lg shadow">
          <div className="scrollbar overflow-auto border border-2">
            <ul className="p-0">
              {[...state.selectedFile].map((file, index) => (
                // here we should import the custom style component
                <ListItem key={index} fileName={file.name} />
              ))}
            </ul>
          </div>
          <div>
            <button
              className="bottom-0 mt-auto rounded border-none 
              bg-indigo-500 py-2 px-4 font-bold
              text-white hover:bg-indigo-300"
              onClick={async () => {
                setState({ ...state, fileSelection: 'loading_component' })
                const processFiles = await processAllFiles([
                  ...state.selectedFile,
                ])
                setState({
                  ...state,
                  fileSelection: 'download_component',
                  returnedData: processFiles,
                })
              }}
            >
              Extract
            </button>
          </div>
        </div>
      </Fragment>
    )
  }

  const parseJsonData = (json_data) => {
    try {
      console.log(json_data)
      const replacer = (key, value) => (value === null ? '' : value) // specify how you want to handle null values here
      const headers = Object.keys(json_data[0])
      // console.log(headers)

      let csv = json_data.map((row) =>
        headers
          .map((fieldName) => JSON.stringify(row[fieldName], replacer))
          .join(',')
      )
      csv.unshift(headers)
      csv = csv.join('\r\n')
      // console.log(csv)
      return csv
    } catch {
      // add file name here?
      console.log('Something went wrong with a file.')
      // this doesn't break now - but instead returns undefined
    }

    // return <Download fileName={filename} csv={csv} />
  }

  function Download() {
    function refreshPage() {
      window.location.reload(false)
    }

    return (
      <div className="w-64 items-center shadow">
        <div className="">
          <a
            // tabIndex="0"
            className="mb-4 mt-4 box-border inline-block rounded bg-indigo-500 
            px-4 text-center text-sm
            font-normal uppercase leading-5 text-white 
            no-underline hover:bg-indigo-300 "
            // generate name file
            download={'export.csv'}
            // here we're passing the json data returned from the function
            // encode uri component
            href={
              'data:text/csv;charset=utf-8,%EF%BB%BF' +
              encodeURIComponent(state.returnedData)
            }
          >
            {/* <img src={DownloadIcon} className="download-icon" /> */}
            <i className="fas fa-arrow-down" /> Download
          </a>
        </div>

        {/* instead of resetting page - refresh */}
        <button
          className="box-border inline-block 
          cursor-pointer rounded border-none bg-indigo-500
          py-2 px-4 text-center text-sm
          font-normal uppercase leading-5 
          text-white no-underline hover:bg-indigo-300"
          onClick={refreshPage}
        >
          Convert another?
        </button>
      </div>
    )
  }

  return (
    <div
      className="main-container flex 
  h-72 w-full justify-center
  break-normal font-sans
  "
    >
      {renderSwitch(state.fileSelection)}
    </div>
  )
}

export default Extractor

{
  /* #### Come back to this #### */
}
{
  /* <form className="my-form">
          <input
            type="file"
            id="fileElem"
            multiple
            accept="application/pdf,application/vnd.ms-excel"
            // here we add the function to process the files I think.
            // onchange={handleFiles(this.files)}
          />
          <label className="button" htmlFor="fileElem">
            Select some files
          </label>
        </form> */
}

{
  /* <input type="file" id="files" name="files" multiple></input> */
}
{
  /* <ul className=""></ul> */
}

// TODO
// file state object needs to be editable.
// add files, rearrange files in the array,
// remove files from the
// update the view
