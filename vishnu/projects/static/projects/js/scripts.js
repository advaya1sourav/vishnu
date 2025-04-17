document.addEventListener("DOMContentLoaded", function () {
    const filterBtn = document.getElementById("filter-btn");
    const filtersDropdown = document.getElementById("filters-dropdown");

    filterBtn.addEventListener("click", function () {
        filtersDropdown.classList.toggle("show");
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", function (event) {
        if (!filtersDropdown.contains(event.target) && !filterBtn.contains(event.target)) {
            filtersDropdown.classList.remove("show");
        }
    });
});



document.addEventListener("DOMContentLoaded", function () {
    const timeRange = document.querySelector("input[name='time_commitment']");
    const timeValue = document.getElementById("time-commitment-value");

    if (timeRange) {
        timeRange.addEventListener("input", function () {
            timeValue.textContent = this.value + " days";
        });
    }
});
