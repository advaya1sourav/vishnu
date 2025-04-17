document.addEventListener("DOMContentLoaded", function () {
    const timeRange = document.querySelector("input[name='time_commitment']");
    const timeValue = document.getElementById("time-commitment-value");

    if (timeRange) {
        timeRange.addEventListener("input", function () {
            timeValue.textContent = this.value + " days";
        });
    }
});
