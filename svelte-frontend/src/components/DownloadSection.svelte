<script>
    import { goto } from '$app/navigation'

    import DownloadButton from "./DownloadButton.svelte";
    import RefreshIcon from "../icons/refresh-cw.svelte";
    import { sessionData } from '../store/sessionStore';

    let sessionResponse;

    sessionData.subscribe(value => {
        sessionResponse = value;
    });

    // Instead of directly binding data to these, you should derive them from sessionResponse.
    let fileData = sessionResponse?.data;
    let fileType = sessionResponse?.filetype;
    let fileName = sessionResponse?.filename;

    function refreshPage() {
        goto('/')
    } 
</script>

<style>
    * {
        border: 1px solid black;
        border-radius: 10px;
        padding-left: 36px;
    }

    .download-section {
        display: flex;           /* Use flexbox */
        align-items: center;     /* Vertically center items */
        gap: 10px;               /* Gap between items */
        margin-bottom: 20px;
    }
    
    .refresh-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center; /* Center the content horizontally */
        box-sizing: border-box;
        padding: 0 16px;
        margin: 4px;
        height: 36px;
        background: none; /* Remove background */
        color: #6366F1; 
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        font-weight: 500;
        border: none;
        border-radius: 4px;
        overflow: hidden;
        outline: none;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;

    }

    .refresh-icon:hover {
        transform: translateY(-2px);
    }

    .refresh-icon:active {
        transform: translateY(1px);
    }
</style>

<!-- TODO: move this to the right side  -->
<div class="download-section">
    <DownloadButton data={fileData} filename={fileName} filetype={fileType}  />
    <button class="refresh-icon" on:click={() => refreshPage()}>
        <RefreshIcon/>
    </button>
    
</div>
