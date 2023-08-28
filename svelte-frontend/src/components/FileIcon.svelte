<script>
    import FileIcon from '../icons/file.svg'

    export let filename = ""; // Default value is an empty string
    export let size = 0; // Default value is 0
    
    let isHovering = false; // to track the hover state

    let tooltip; // Reference to the tooltip element
    let filenameDiv; // Reference to the filename div

    function adjustTooltipPosition() {
        if (tooltip && filenameDiv) {
            const rect = filenameDiv.getBoundingClientRect();

            if (rect.right + tooltip.offsetWidth > window.innerWidth) {
                tooltip.style.left = "auto";
                tooltip.style.right = "0";
            } else {
                tooltip.style.left = "50%";
                tooltip.style.transform = "translateX(-50%)";
            }
        }
    }
</script>

<style>
    .drop-icon {
        width: 120px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        position: relative; 
    }
    
    .filename {
        width: 80%;
        font-size: 0.8rem;
        font-weight: 500;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        margin-top: 0.5rem;
    }

    .filesize {
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }

    .tooltip {
        position: absolute;
        top: 100%; 
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        white-space: nowrap;
        z-index: 10; 
    }

    /* .drop-icon:hover .tooltip {
        display: block;
    } */
</style>

<div class="drop-icon" >
    <img src={FileIcon} alt="Selected file" class="pointer-events-none select-none" />
    <div 
        bind:this={filenameDiv}
        class="filename" 
        on:mouseover={() => { isHovering = true; adjustTooltipPosition(); }} 
        on:mouseout={() => isHovering = false}
    >
        {filename}
    </div>
    {#if isHovering}
        <div bind:this={tooltip} class="tooltip">{filename}</div>
    {/if}
    <div class="filesize">{Math.round(size / 1000)} KB</div>
</div>

<!-- TODO: fix styling tooltip being displayed off screen. 
adjust colours etc
-->