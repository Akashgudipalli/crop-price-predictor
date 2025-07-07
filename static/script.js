console.log("script.js is loaded");

const crops = ["wheat", "rice", "maize", "cotton", "sugarcane", "banana", "soybean", "onion", "tomato", "potato", "mustard", "groundnut", "barley", "bajra", "jowar", "apple", "mango", "grapes", "pulses", "millets"];
const soils = ["alluvial", "black", "red", "sandy", "clay", "loamy", "peaty", "saline", "laterite", "marshy"];
const statesCities = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar"],
    "Kerala": ["Kochi", "Trivandrum", "Kollam"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"]
};
const stateDistricts = {
    "Andhra Pradesh": ["Anantapur", "Chittoor", "Guntur"],
    "Telangana": ["Hyderabad", "Ranga Reddy", "Warangal"],
    "Maharashtra": ["Pune", "Nagpur", "Thane"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar"],
    "Kerala": ["Kollam", "Kozhikode", "Ernakulam"],
    "Uttar Pradesh": ["Agra", "Lucknow", "Varanasi"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur"],
    "Gujarat": ["Ahmedabad", "Surat", "Rajkot"]
};

function populateSelect(id, options) {
    const select = document.getElementById(id);
    select.innerHTML = ""; // Clear existing
    options.forEach(val => {
        const opt = document.createElement("option");
        opt.value = val;
        opt.text = val;
        select.appendChild(opt);
    });
    if (window.jQuery) {
        $(`#${id}`).select2({ placeholder: `Select ${id}` });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("Populating dropdowns...");
    populateSelect("cropSelect", crops);
    populateSelect("soilSelect", soils);
    populateSelect("stateSelect", Object.keys(statesCities));

    const stateSelect = document.getElementById("stateSelect");
    const districtSelect = document.getElementById("districtSelect");

    stateSelect.addEventListener("change", () => {
        const selectedState = stateSelect.value;
        districtSelect.innerHTML = "<option value=''>Select District</option>";
        if (stateDistricts[selectedState]) {
            stateDistricts[selectedState].forEach(dist => {
                const opt = document.createElement("option");
                opt.value = dist;
                opt.text = dist;
                districtSelect.appendChild(opt);
            });
            $('#districtSelect').select2();
            $('#districtSelect').val(null).trigger("change");
        } else {
            console.log("No districts found for state:", selectedState);
        }
    });
});



document.getElementById("predictForm").addEventListener("submit", function (e) {
    e.preventDefault();  // ✅ Prevent page refresh

    const crop = document.getElementById("cropSelect").value;
    const soil = document.getElementById("soilSelect").value;
    const state = document.getElementById("stateSelect").value;

    const data = { crop, soil, state };

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById("result").innerHTML = `<strong>Predicted Price:</strong> ₹${result.price}`;
    })
    .catch(error => {
        console.error("Prediction error:", error);
        document.getElementById("result").innerHTML = `<span style="color:red;">Prediction failed.</span>`;
    });
});
