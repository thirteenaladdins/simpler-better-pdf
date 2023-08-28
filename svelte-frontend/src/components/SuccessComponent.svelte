<script>
    export let message = "Conversion successful!"; // default message
</script>

<style>
    .success-container {
        display: flex;
        align-items: center;
        justify-content: center;
        /* height: 100%; */
        height: 20px;
        padding: 20px;
        background-color: #D4EDDA;  
        border: 1px solid #C3E6CB; 
        border-radius: 8px; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
    }

    .success-message {
        font-size: 1.5rem;
        font-weight: bold;
        color: #155724;
    }
</style>

<div class="success-container">
    <div class="success-message">
        {message}
    </div>
</div>
