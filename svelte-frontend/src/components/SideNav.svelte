<script>
    
    import { selectedItem } from '../store/selectedItemStore.js';

    function toggleHighlight(itemName) {
        if ($selectedItem !== itemName) {
        selectedItem.set(itemName);
        }
  }

    let isNavOpen = false;
    let showTools = true;
    let isDarkMode = false;


    // let highlightedItem = 'luxuryGoods';

    // function toggleHighlight(itemName) {
    // if (highlightedItem !== itemName) {
    //     highlightedItem = itemName;
    //     }
    // }


    // function toggleTheme() {
    //     isDarkMode = !isDarkMode;
    //     document.body.classList.toggle('dark-mode', isDarkMode);
    // }

</script>

<style>
    /* Small devices (landscape phones, 576px and up) */
/* @media only screen and (max-width: 576px) {  
  .sidebar-list {
    display: flex;
    align-items: center;
    justify-content: center;
  }
} */

/* Medium devices (tablets, 768px and up) The navbar toggle appears at this breakpoint */
/* @media (min-width: 768px) {
  
} */

/* Large devices (desktops, 992px and up) */
/* @media only screen and (min-width: 992px) {
} */

/* Extra large devices (large desktops, 1200px and up) */
/* @media (min-width: 1200px) {} */



.font-sans {
    font-family: system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;
}

.sidebar-hidden {
  visibility: hidden;
} 

.sidebar-item {
  list-style: none;
}

.sidenav {
    display: flex;
    padding-top: 16px;
    /* background-color: #E7491D; */
    /* background-color: rgb(255, 117, 4); */
    /* border-right: 1px solid black; */
    flex-direction: column; /* Stacks children vertically */
    /* justify-content: space-between;  */
    height: 100%; /* Use 100% of the parent's height */
}


/* Centering text inside .sidebar-button */
.sidebar-button {
    /* ... (your existing styles inside this class) ... */
    line-height: 36px; /* This should match the height of the button for vertical centering */
}

/* Style the settings button similar to .sidebar-button */
.sidenav button {
    display: inline-block;
    list-style: none;
    border: 1px solid transparent;
    border-radius: 4px;
    /* background-color: transparent; */
    padding: 0 10px;
    margin: 4px;
    /* margin-top: 10px; */
    /* min-width: 8rem; */
    /* height: 36px; */
    line-height: 36px;
    vertical-align: middle;
    /* text-align: center; */
    /* background-color: #fff; */
    color: rgb(var(--pure-material-primary-rgb,115,125,176));
    color: rgb(134,143,186);
    font-size: 14px;
    font-weight: 400;
    cursor: pointer;
    transition: box-shadow .2s;
    text-decoration: none; /* To remove the underline from the anchor tag */
}

.sidenav button:hover {

    /* background-color: rgb(255, 165, 92); */
    background-color: rgb(225, 232, 240);
    color: rgb(42,91,252);
    /* background-color: aliceblue; */
}

/* .sidenav button:active {
    background-color: rgb(225, 232, 240);
    color: rgb(42,91,252);
} */

.sidebar-title {
    font-size: 0.75rem;
    padding: 0 10px;
    margin: 4px;
    color: rgb(167,175,215);
    
}

/* if sidebar links clicked */
.sidenav button.on-selected-sidebar {
    background-color: rgb(225, 232, 240);
    color: rgb(42,91,252);
}

/* .on-selected-sidebar {
    background-color: rgb(225, 232, 240);
    color: rgb(42,91,252);
} */

.tools-content {
    /* width: 10px; */
}

</style>

<!-- <button on:click={() => isNavOpen = !isNavOpen}>{isNavOpen ? 'Close' : 'Open'} Side Nav</button> -->

<!-- maybe the toggle is what I want -->
<!-- <div class="sidenav" class:active={isNavOpen}> -->

    <div class="sidenav">
        <span class="sidebar-title font-sans">TOOLS</span>
    
        <button 
            on:click={() => toggleHighlight('Luxury Goods')} 
            class="sidebar-button font-sans {$selectedItem === 'Luxury Goods' ? 'on-selected-sidebar' : ''}">
            Luxury Goods
        </button>
             
        <button 
            on:click={() => toggleHighlight('ALS Header')} 
            class="sidebar-button font-sans {$selectedItem === 'ALS Header' ? 'on-selected-sidebar' : ''}">
            ALS Header
        </button>
    </div>
                      



    <!-- </div> -->


    <!-- come back and implement this -->
    <!-- <button on:click={toggleTheme}>Toggle Theme</button> -->

    <!-- TODO: add scrolling to this and implement -->
    <!-- <a href="#">Settings</a> -->

    
    <!-- add toggle here -->
    




