<script>
    import TableDataViewer from "../../components/TableDataViewer.svelte";
    import DownloadSection from "../../components/DownloadSection.svelte";
</script>

<style>
    body, html {
    margin: 0;
    padding: 0;
    height: 100%;
    overflow-y: auto;
    }

    .container {
    display: flex;
    align-items: start;
    width: 100%;

}

.left-div {
    flex: 4;
    /* background-color: lightblue; */
    height: 100%;
    overflow: auto;
}

.right-div {
    flex: 1;
    /* background-color: lightcoral; */
    height: 100%;
    padding-left: 16px;
}


</style>

<div class="container">
    <div class="left-div">
        <TableDataViewer></TableDataViewer>
    </div>
    <div class="right-div">
        <DownloadSection></DownloadSection>
    </div>
</div>
