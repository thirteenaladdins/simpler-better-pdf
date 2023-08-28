
<script>

  import { createEventDispatcher } from 'svelte';

  // COMPONENTS
  import UploadIcon from '../icons/upload.svg';
  import FileIcon from '../components/FileIcon.svelte'
  
  // API
  import processAllFiles from '../utils/processAllFiles';

  const dispatch = createEventDispatcher();

  // STORE
  import { selectedItem } from '../store/selectedItemStore';

  let currentSelectedItem = $selectedItem;

  selectedItem.subscribe(value => {
    currentSelectedItem = value;
    // Do something with currentSelectedItem
  });




  async function handleFileUpload(selectedFiles, selectedOption) {
    try {
        const responseData = await processAllFiles(selectedFiles, selectedOption);
        console.log(responseData)
        
        if (responseData) {
            dispatch('uploadSuccess', responseData);
        } else {
            // handle error or lack of expected response here
            dispatch('uploadFailed', { message: "Unexpected response from server" });
        }
    } catch (error) {
        dispatch('uploadFailed', error);
    }
}
  
  const count = 100;
  const formats = ['pdf'];

  let fileInput;
  let selectedFiles = [];
  let dropArea;


  function onClickHandler() {
      fileInput.click();
  }

  function highlight() {
      dropArea.style.backgroundColor = "#e0e4f3";
  }

  function unhighlight() {
      dropArea.style.backgroundColor = "";
  }

  function handleKeyDown() {

  }

  function handleDrop(event) {
      event.preventDefault();
      const droppedFiles = event.dataTransfer?.files ?? [];
      selectedFiles = Array.from(droppedFiles);
      console.log(selectedFiles);
  }

  function handleFiles(event) {
      selectedFiles = Array.from(event.target.files);
      console.log(selectedFiles);
  }
</script>


  
<style>
    .file-upload-container {
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
        height: 25rem;
        width: 40rem;
        border: 1px solid black;
        border-radius: 10px;
    }
    
    .drop-area-full {
        display: flex;
        flex-direction: column; /* Changed to column for vertical alignment of icon and text */
        text-align: center;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        height: 20rem;
        width: 36rem;
        padding: 1rem;
        font-size: 0.9rem;
        
        overflow-wrap: normal;
        word-break: normal;
        border: 2px dashed #a5b4fc;
        cursor: pointer;
        border-radius: 10px; /* Added for rounded borders */
        /* background-color: #f5f7fd;  */
        /* Light background color for better contrast */
        transition: background-color 0.3s; /* Smooth transition for hover effect */
    }

    .drop-area-full:hover {

        background-color: #a5b4fc;
        cursor: pointer;
    }

    .drop-area-full.file-selected {
      /* Override or remove certain styles when a file is selected */
      display: flex;
      flex-direction: column; /* Changed to column for vertical alignment of icon and text */
      align-items: flex-start;  /* Start items from the left */
      justify-content: flex-start;  /* Start items from the top */
      overflow-wrap: normal;
      word-break: normal;
      border: 2px dashed #a5b4fc;
      
      /* cursor: pointer; */
      border-radius: 10px; /* Added for rounded borders */
      /* background-color: #f5f7fd;  */
      /* Light background color for better contrast */
      transition: background-color 0.3s; /* Smooth transition for hover effect */
    }

    .drop-area-full.file-selected:hover {
        background-color: #fafafa;
        cursor: default;
    }


    .drop-icon {
        margin-bottom: 1rem; /* Spacing between the icon and text */
    }


  .file-list {
      display: flex;
      flex-direction: row; 
      flex-wrap: wrap;
      align-items: flex-start;  /* Start items from the top */
      justify-content: flex-start;  /* Start items from the left */
      /* max-height: 200px; */
      /* overflow-y: auto; */
      margin-top: 1rem;
      width: 100%;
  }

  .upload-button {
    margin: 10px;
  }

  .upload-button:disabled {
    background-color: #d1d5db;
    cursor: not-allowed;
    }

  .title {
    font-weight: 500;
  }

  .font-sans {
    font-family: Open Sans,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Fira Sans,Droid Sans,Helvetica Neue,sans-serif;
  }
  
</style>


<!-- REWORK THIS - add feature to add additional files into dropbox -->

<div class="file-upload-container font-sans">
<p class="title">File Upload</p>
<div 
  role="button"
  bind:this={dropArea} 
  class="drop-area-full"
  on:click={selectedFiles.length === 0 ? onClickHandler : undefined}
  on:dragenter={highlight}
  on:dragover={highlight}
  on:dragleave={unhighlight}
  on:drop={selectedFiles.length === 0 ? handleDrop : undefined}
  on:keydown={handleKeyDown}
  class:file-selected={selectedFiles.length > 0} 
  tabindex=0
>
  <input 
      bind:this={fileInput}
      multiple 
      type="file" 
      bind:files={selectedFiles} 
      accept="application/pdf" 
      style="display: none;" 
      on:change={handleFiles}
  />

  {#if selectedFiles.length === 0}
      <img src={UploadIcon} alt="Drop your files here" class="pointer-events-none select-none drop-icon" />
      <div class="pointer-events-none select-none text-sm">
          Click to choose a file or drag it here
      </div>
  {/if}

  <div class="file-list">
      {#each selectedFiles as file (file.name)}
          <FileIcon filename={file.name} size={file.size} type={file.type} />
      {/each}
  </div>
</div>



<!-- after success, then load the component -->

<!-- <button on:click={handleFileUpload(selectedFiles, 'Luxury Goods')} class="upload-button">Upload</button> -->


<button 
    on:click={handleFileUpload(selectedFiles, $selectedItem)} 
    class="upload-button"
    disabled={selectedFiles.length === 0}
>
    Upload
</button>

</div>



<!-- when you press upload it transmits the selected files as normal -->
<!-- processAllfiles, pass selectedFiles to this function -->

<!-- elif request.form["option"] == "ALS Header": -->

<!-- TODO -->
<!-- by selecting from the navbar we need to figure out how to pass that information here -->

<!-- TODO: 
  when the
- Add scrollable div 
- Add icons
- Add editing capabilities later on 
  do not reset file list unless explicitely asked to do so
-->
