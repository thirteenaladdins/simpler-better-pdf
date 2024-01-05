


export function handleDragEnter(event) {
    event.preventDefault();
    event.stopPropagation();
    dragCounter++;
    if (dragCounter === 1) {
        // Only highlight once
        highlight(event);
    }
}


// function handleDragEnter(event) {
//     event.preventDefault();
//     event.stopPropagation();
//     dragCounter++;
//     if (dragCounter === 1) {
//         // Only highlight once
//         highlight(event);
//     }
// }

// function handleDragLeave(event) {
//     event.preventDefault();
//     event.stopPropagation();
//     dragCounter--;
//     if (dragCounter === 0) {
//         unhighlight();
//     }
// }