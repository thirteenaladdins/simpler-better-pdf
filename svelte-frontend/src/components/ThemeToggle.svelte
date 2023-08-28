
<!-- Todo: come back and implement this -->
<script>
    let isDarkMode = false;

    function toggleTheme() {
        isDarkMode = !isDarkMode;
        document.body.classList.toggle('dark-mode', isDarkMode);
        // If you want to remember the user's theme preference
        // using local storage or similar, you can do so here.
    }
</script>

<style>
    button {
        /* You can customize the appearance of the button here */
    }
</style>

<button on:click={toggleTheme}>
    {isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
</button>
