function toggleDisplay(id) {
    const myDiv = document.getElementById(id);

    const displaySetting = myDiv.style.display;

    // now toggle the clock and the button text, depending on current state
    if (displaySetting == 'block') {
        myDiv.style.display = 'none';
    }
    else {
        myDiv.style.display = 'block';
    }
}
