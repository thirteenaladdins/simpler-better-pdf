<script>
	import SideNav from "../components/SideNav.svelte";
	import DropAreaFileUpload from "../components/DropAreaFileUpload.svelte";
    import NavigationBar from "../components/NavigationBar.svelte";
    import SuccessComponent from "../components/SuccessComponent.svelte";
    import SuccessPage from "../components/SuccessPage.svelte";
    import Footer from "../components/Footer.svelte";

    import { version } from "../utils/version.js"

    console.log("App version:", version);


    let uploadSuccessful = false; // Indicate if the upload was successful
    let responseData = null
    let errorMessage = ""

    function handleSuccess(event) {
        uploadSuccessful = true; // Set to true on successful upload
        responseData = event.detail
    }

    function handleError(event) {
        errorMessage = event.detail.message || "An error occurred.";
    }   
</script>

<style>

    body {
        background:#fafafa;
    }

    body, html {
    margin: 0;
    padding: 0;
    height: 100%;
    overflow-y: auto;
}


    .uniformWidth {
        width: 100%; /* Set to the desired width, using 100% as an example here */
        max-width: 40rem; /* Assuming you want a maximum width. Adjust as per your requirement. */
    }


    .container {
        display: flex;
        align-items: center; /* Vertically center content */
        padding-top: 15vh;
        justify-content: center;
        margin: 0 auto;

    }

    .content {
        flex: 1;
        display: flex;
        /* justify-content: space-between; */

    }


    .successWrapper {
        display: flex;
        /* flex-direction: column; */
        justify-content: center;
        width: 100%;
    }

    .dropArea {
        flex: 1; 
        display: flex;
        align-items: center; 
        justify-content: center;
    }
</style>

<!-- TODO: implement "success" notification at the top of the page -->

<NavigationBar></NavigationBar>
<div class="content">
    <SideNav></SideNav>
    <div class="container uniformWidth">
        {#if uploadSuccessful}
            <div class="successWrapper"> <!-- Apply the common class here -->
                
                <SuccessPage data={responseData} />
            </div>
        {:else}
            <div class="dropArea uniformWidth"> <!-- Apply the common class here too -->
                <DropAreaFileUpload on:uploadSuccess={handleSuccess} on:uploadFailed={handleError}></DropAreaFileUpload>
            </div>
        {/if}

        {#if errorMessage}
            <p>{errorMessage}</p>
        {/if}
    </div>
</div>
